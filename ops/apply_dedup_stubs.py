#!/usr/bin/env python3
"""Replace exact-duplicate markdown files with archive stubs pointing to canonical files.

Behavior:
- For each .md in content/, compute normalized body (strip frontmatter, collapse whitespace).
- Group files by normalized body. For groups with >1 file:
  - Choose canonical file (longest body length).
  - For other files, replace content with frontmatter:
    - keep/merge created & layer & scope if present
    - set status: archived
    - add aliases: include original basename
    - add redirect_to: canonical relative path
    - short body: 'Перенесено в [[<canonical basename>]]'
- Update canonical frontmatter to include aliases of removed files.
- Write a report to ops/dedup_applied.md
"""
from pathlib import Path
import re
import yaml
import datetime

CONTENT = Path('content')
REPORT = Path('ops') / 'dedup_applied.md'
TODAY = datetime.date.today().isoformat()

def read_text(p):
    return p.read_text(encoding='utf-8')

def write_text(p, s):
    p.write_text(s, encoding='utf-8')

def parse_frontmatter(text):
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            raw = parts[1]
            body = parts[2]
            try:
                data = yaml.safe_load(raw)
                if data is None:
                    data = {}
            except Exception:
                data = {}
            return data, body
    return {}, text

def build_frontmatter(d):
    return '---\n' + yaml.safe_dump(d, allow_unicode=True, sort_keys=False) + '---\n'

# gather files
md_files = list(CONTENT.rglob('*.md'))
norm_map = {}
orig_meta = {}

for p in md_files:
    text = read_text(p)
    fm, body = parse_frontmatter(text)
    # normalized body
    nb = re.sub(r'\s+', ' ', body).strip()
    key = nb
    norm_map.setdefault(key, []).append(p)
    orig_meta[str(p)] = fm

# find exact groups
groups = [g for g in norm_map.values() if len(g) > 1]
report_lines = ["# Applied dedup stubs report\n"]
report_lines.append(f"Found {len(groups)} exact duplicate clusters")
changed = []

for idx, group in enumerate(groups, 1):
    # choose canonical = largest file body length
    sizes = [(p, len(re.sub(r'\s+',' ', parse_frontmatter(read_text(p))[1]).strip())) for p in group]
    canonical = max(sizes, key=lambda x: x[1])[0]
    report_lines.append(f"\n## Cluster {idx}: {len(group)} files")
    report_lines.append(f"Canonical: {canonical}")
    # gather aliases to add
    aliases = set(orig_meta.get(str(canonical), {}).get('aliases', []) or [])
    for p,lenp in sorted(sizes, key=lambda x: -x[1]):
        report_lines.append(f"- {p} ({lenp} chars)")
    for p,l in sizes:
        if p == canonical:
            continue
        # get meta of duplicate
        fm_dup, body_dup = parse_frontmatter(read_text(p))
        # record alias name (basename without ext)
        aliases.add(p.stem)
        # prepare stub frontmatter
        new_fm = {}
        # preserve created/layer/scope if present
        if 'created' in fm_dup:
            new_fm['created'] = fm_dup['created']
        else:
            new_fm['created'] = TODAY
        new_fm['type'] = fm_dup.get('type','doc')
        new_fm['status'] = 'archived'
        new_fm['layer'] = fm_dup.get('layer','methodology')
        new_fm['scope'] = fm_dup.get('scope','local-edge')
        new_fm['redirect_to'] = str(canonical).replace('\\','/')
        new_fm['aliases'] = [p.stem]
        # write stub body
        stub_body = f"Перенесено в [[{canonical.name}]]\n"
        write_text(p, build_frontmatter(new_fm) + '\n' + stub_body)
        changed.append(p)
    # update canonical aliases
    if aliases:
        fm_can, body_can = parse_frontmatter(read_text(canonical))
        existing = fm_can.get('aliases') or []
        if isinstance(existing, str):
            existing = [existing]
        for a in aliases:
            if a not in existing and a != canonical.stem:
                existing.append(a)
        fm_can['aliases'] = existing
        # ensure required keys
        if 'type' not in fm_can:
            fm_can['type'] = 'doc'
        if 'status' not in fm_can:
            fm_can['status'] = 'active'
        if 'created' not in fm_can:
            fm_can['created'] = TODAY
        write_text(canonical, build_frontmatter(fm_can) + body_can.lstrip('\n'))

report_lines.append(f"\nTotal files converted to stubs: {len(changed)}")
REPORT.write_text('\n'.join(report_lines), encoding='utf-8')
print(f'Applied stubs for {len(changed)} files; report written to {REPORT}')
