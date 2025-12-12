#!/usr/bin/env python3
"""Normalize frontmatter and fix wikilinks based on 0.4 reports.

Usage: python ops/normalize_content.py

What it does:
- Walks content/ for .md files
- Ensures YAML frontmatter exists with required keys
- Parses Противоречия и несогласованности 0.4.md to get candidate broken links
- Attempts to resolve those names to existing files by filename or H1 title
- Replaces wikilinks [[Old Name]] -> [[Target Basename]] across content files
- Adds `aliases:` to target file frontmatter for preserved old titles
- Outputs metrics (files changed, wikilinks replaced, frontmatter fixes)

Note: This is a best-effort automated pass. Ambiguous cases are logged to stdout for manual review.
"""

import os
import re
import sys
import io
import datetime
import yaml
from pathlib import Path
import difflib

CONTENT_DIR = Path('content')
REPORT_PATH = Path('content') / '0. Управление' / '0.4. Автоматические отчёты ИИ' / 'Противоречия и несогласованности 0.4.md'
REQUIRED_KEYS = ['type','status','created','layer','scope']
TODAY = datetime.date.today().isoformat()

# helpers

def read_text(p):
    return p.read_text(encoding='utf-8')


def write_text(p, s):
    p.write_text(s, encoding='utf-8')


def has_frontmatter(text):
    return text.startswith('---\n')


def parse_frontmatter(text):
    if not has_frontmatter(text):
        return {}, text
    parts = text.split('---', 2)
    if len(parts) < 3:
        return {}, text
    raw = parts[1]
    body = parts[2]
    try:
        data = yaml.safe_load(raw)
        if data is None:
            data = {}
    except Exception:
        data = {}
    return data, body


def build_frontmatter(data):
    return '---\n' + yaml.safe_dump(data, allow_unicode=True, sort_keys=False) + '---\n'


# 1) build file index: basename (no ext) -> path, and H1 title -> path
file_index = {}
title_index = {}
md_files = list(CONTENT_DIR.rglob('*.md'))
for p in md_files:
    basename = p.name
    key = basename
    file_index[key] = p
    # read H1
    text = read_text(p)
    # find first H1
    m = re.search(r'^#\s+(.+)$', text, flags=re.M)
    if m:
        title = m.group(1).strip()
        title_index[title] = p

print(f'Indexed {len(md_files)} markdown files under content/')

# 2) parse report for candidate broken document names
broken_names = set()
if REPORT_PATH.exists():
    rp = read_text(REPORT_PATH)
    # find table rows that look like | <num> | <Документ> | ... |
    for line in rp.splitlines():
        parts = [c.strip() for c in line.split('|')]
        if len(parts) >= 3:
            doc = parts[2]
            # heuristic: if doc contains non-empty and not just header
            if doc and not doc.lower().startswith('документ') and '---' not in doc:
                # clean
                doc = re.sub(r'`|\[|\]|\.|\s+$','',doc)
                doc = doc.strip()
                if doc:
                    broken_names.add(doc)
else:
    print('Report file not found:', REPORT_PATH)

print('Found', len(broken_names), 'candidate broken-names from report')

# attempt to resolve broken names
resolved = {}
unresolved = []
for name in sorted(broken_names):
    # try exact basename match and several normalized variants
    candidates = []
    def normalize(n):
        s = n
        # remove code-ish artifacts like 'md' suffix, stray punctuation and numeric noise
        s = re.sub(r"\bmd\b", "", s, flags=re.IGNORECASE)
        s = re.sub(r"[\d]+", "", s)
        s = re.sub(r"[_\-]+", " ", s)
        s = re.sub(r"[^\w\s\u0400-\u04FF]", " ", s)
        s = re.sub(r"\s+", " ", s).strip()
        return s

    variants = set()
    variants.add(name)
    variants.add(name + '.md')
    norm = normalize(name)
    variants.add(norm)
    variants.add(norm + '.md')
    variants.add(norm.replace(' ', ''))
    # also try lowercased and title-cased
    variants.add(name.lower())
    variants.add(norm.lower())

    # search for candidates using variants
    for v in variants:
        if not v:
            continue
        # try with exact basename in index
        if v in file_index:
            candidates.append(file_index[v])
        # try exact title
        if v in title_index:
            candidates.append(title_index[v])
        # try substring match in basenames
        for k,vk in file_index.items():
            try:
                if v.lower() in k.lower():
                    candidates.append(vk)
            except Exception:
                pass
        # try substring in titles
        for t,p in title_index.items():
            try:
                if v.lower() in t.lower():
                    candidates.append(p)
            except Exception:
                pass
    # dedupe candidates
    candidates = list(dict.fromkeys(candidates))
    if len(candidates)==1:
        resolved[name] = candidates[0]
    elif len(candidates)>1:
        # pick the shortest path (heuristic)
        resolved[name] = sorted(candidates, key=lambda p: len(str(p)))[0]
    else:
        unresolved.append(name)

print('Resolved', len(resolved), 'names,', len(unresolved), 'unresolved')
if unresolved:
    print('Unresolved examples:', unresolved[:10])

# 2b) Try fuzzy-matching for unresolved names using titles and basenames
fuzzy_resolved = {}
still_unresolved = []
for name in unresolved:
    # build candidate pool: basenames and titles
    candidates = list(file_index.values()) + list(title_index.values())
    # unique
    candidates = list(dict.fromkeys(candidates))
    # prepare keys for matching
    keys = [str(p.name) for p in candidates] + [t for t in title_index.keys()]
    # use difflib to find close matches
    match = difflib.get_close_matches(name, keys, n=1, cutoff=0.65)
    if match:
        m = match[0]
        # find corresponding path
        target = None
        # check filenames
        for p in candidates:
            if p.name == m:
                target = p
                break
        # check titles
        if target is None:
            if m in title_index:
                target = title_index[m]
        if target:
            fuzzy_resolved[name] = target
        else:
            still_unresolved.append(name)
    else:
        still_unresolved.append(name)

print('Fuzzy-resolved', len(fuzzy_resolved), 'additional names,', len(still_unresolved), 'still unresolved')
if fuzzy_resolved:
    # merge into resolved
    for k,v in fuzzy_resolved.items():
        if k not in resolved:
            resolved[k] = v
    # rebuild unresolved list
    unresolved = still_unresolved
# 3) perform replacements: for each resolved name, replace [[Name]] -> [[TargetBasename]] across files
replacements_made = 0
frontmatter_fixed = 0
aliases_added = 0
files_touched = set()

for name, target_path in resolved.items():
    target_basename = target_path.name
    # ensure target has frontmatter and aliases
    t_text = read_text(target_path)
    fm, body = parse_frontmatter(t_text)
    changed = False
    if not fm:
        fm = {}
        changed = True
    # ensure required keys
    for k in REQUIRED_KEYS:
        if k not in fm:
            if k=='created':
                fm[k] = TODAY
            elif k=='type':
                fm[k] = 'doc'
            elif k=='status':
                fm[k] = 'active'
            elif k=='layer':
                fm[k] = 'methodology'
            elif k=='scope':
                fm[k] = 'local-edge'
            changed = True
    # add aliases list if name not equal
    aliases = fm.get('aliases') or fm.get('alias') or []
    if isinstance(aliases, str):
        aliases = [aliases]
    if name not in aliases and name != target_path.stem:
        aliases.append(name)
        fm['aliases'] = aliases
        aliases_added += 1
        changed = True
    if changed:
        new_text = build_frontmatter(fm) + body.lstrip('\n')
        write_text(target_path, new_text)
        frontmatter_fixed += 1
        files_touched.add(str(target_path))

# scan all md files for occurrences of [[name]] and replace
wikilink_re = re.compile(r"\[\[([^\]]+)\]\]")
for p in md_files:
    text = read_text(p)
    orig = text
    def replace_link(m):
        label = m.group(1).strip()
        # exact match
        if label in resolved:
            return f'[[{resolved[label].name}]]'
        # try fuzzy match
        if label in fuzzy_resolved:
            return f'[[{fuzzy_resolved[label].name}]]'
        return m.group(0)
    new_text = wikilink_re.sub(replace_link, text)
    if new_text != orig:
        write_text(p, new_text)
        # count only actual substitutions
        replacements_made += sum(1 for m in wikilink_re.findall(orig) if m in resolved or m in fuzzy_resolved)
        files_touched.add(str(p))

# 4) Ensure every file has frontmatter with required keys
for p in md_files:
    text = read_text(p)
    fm, body = parse_frontmatter(text)
    changed = False
    if not fm:
        fm = {}
        changed = True
    for k in REQUIRED_KEYS:
        if k not in fm:
            if k=='created':
                fm[k] = TODAY
            elif k=='type':
                fm[k] = 'doc'
            elif k=='status':
                fm[k] = 'draft'
            elif k=='layer':
                fm[k] = 'operations'
            elif k=='scope':
                fm[k] = 'local-edge'
            changed = True
    if changed:
        body_text = body.lstrip('\n')
        new_text = build_frontmatter(fm) + body_text
        write_text(p, new_text)
        frontmatter_fixed += 1
        files_touched.add(str(p))

# summary
print('---')
print('Files touched:', len(files_touched))
print('Frontmatter fixes:', frontmatter_fixed)
print('Aliases added:', aliases_added)
print('Wikilink replacements attempted (approx):', replacements_made)
print('Unresolved broken names:', len(unresolved))
if unresolved:
    for u in unresolved[:30]:
        print('-', u)

print('\nDone. Review changes and run git status / git diff to inspect edits.')
