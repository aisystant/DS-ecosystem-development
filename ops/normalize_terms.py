#!/usr/bin/env python3
"""Normalize agreed terminology across markdown files (dry-run by default).

Usage:
  python ops/normalize_terms.py        # dry-run, writes ops/term_norm_proposals.md
  python ops/normalize_terms.py --apply   # apply changes and commit

Behaviour:
- Only replaces in markdown body (not YAML frontmatter).
- Skips fenced code blocks and inline code spans.
- Applies a conservative mapping derived from 'Терминологическая согласованность 0.4.md'.
"""
from pathlib import Path
import re
import argparse
import difflib
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'content'
PROPOSAL = ROOT / 'ops' / 'term_norm_proposals.md'

# Conservative mapping: variant -> canonical
MAPPING = {
    # Proof-of-Impact variants
    r"\bPoI\b": "Proof-of-Impact",
    r"\bПоИ\b": "Proof-of-Impact",
    r"\bсистема\s+доказательства\s+вклада\b": "Proof-of-Impact",
    # ИИ-ассистент variants
    r"\bAI-ассистент\b": "ИИ-ассистент",
    r"\bИИ\s*ассистент\b": "ИИ-ассистент",
    r"\bИИ-агент\b": "ИИ-ассистент",
    # Frontmatter variants
    r"\bфронтматтер\b": "Frontmatter",
    r"\bYAML-?заголовок\b": "Frontmatter",
    r"\bметаданные\b": "Frontmatter",
    # Docs-as-Code
    r"\bDocAsCode\b": "Docs-as-Code",
    r"\bдокументы-как-код\b": "Docs-as-Code",
    # Exocortex / Экзокортекс
    r"\bexocortex\b": "Экзокортекс",
    r"\bэкзо-?кортекс\b": "Экзокортекс",
    r"\bэкзокортекс\b": "Экзокортекс",
}


def replace_preserving_case(match, replacement):
    s = match.group(0)
    # if all upper
    if s.isupper():
        return replacement.upper()
    # if capitalized
    if s[0].isupper():
        return replacement[0].upper() + replacement[1:]
    return replacement


def process_text(text):
    # Skip YAML frontmatter
    fm = ''
    body = text
    if text.startswith('---'):
        parts = text.split('---', 2)
        if len(parts) >= 3:
            fm = parts[1]
            body = parts[2]

    # Remove fenced code blocks temporarily
    fences = {}
    def fence_repl(m):
        key = f"__FENCE_{len(fences)}__"
        fences[key] = m.group(0)
        return key
    body_nofences = re.sub(r"```[\s\S]*?```", fence_repl, body)

    # Replace inline code spans with placeholders
    inlines = {}
    def inline_repl(m):
        key = f"__INLINE_{len(inlines)}__"
        inlines[key] = m.group(0)
        return key
    body_noinline = re.sub(r"`[^`]*`", inline_repl, body_nofences)

    orig = body_noinline
    new = orig
    for pat, rep in MAPPING.items():
        new = re.sub(pat, lambda m: replace_preserving_case(m, rep), new, flags=re.IGNORECASE)

    # restore inline and fences
    for k,v in inlines.items():
        new = new.replace(k, v)
    for k,v in fences.items():
        new = new.replace(k, v)

    # reassemble
    if fm:
        return '---\n' + fm + '---\n' + new
    return new


def collect_proposals():
    proposals = []
    for p in CONTENT.rglob('*.md'):
        txt = p.read_text(encoding='utf-8')
        new = process_text(txt)
        if new != txt:
            # produce small diff
            diff = '\n'.join(difflib.unified_diff(txt.splitlines(), new.splitlines(), lineterm=''))
            proposals.append((p.relative_to(ROOT).as_posix(), diff))
    return proposals


def apply_changes(proposals):
    changed = []
    for path, diff in proposals:
        p = ROOT / path
        txt = p.read_text(encoding='utf-8')
        new = process_text(txt)
        if new != txt:
            p.write_text(new, encoding='utf-8')
            changed.append(path)
    return changed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()

    proposals = collect_proposals()
    PROPOSAL.write_text('# Terminology normalization proposals\n\n', encoding='utf-8')
    with PROPOSAL.open('a', encoding='utf-8') as f:
        for path, diff in proposals:
            f.write(f'## {path}\n')
            f.write('```diff\n')
            f.write(diff or '(no textual diff)')
            f.write('\n```\n\n')

    print(f'Proposals found for {len(proposals)} files, written to {PROPOSAL}')

    if args.apply and proposals:
        changed = apply_changes(proposals)
        if changed:
            # commit changes
            subprocess.run(['git', 'add'] + changed, check=False)
            subprocess.run(['git', 'commit', '-m', 'chore(content): terminology normalization (automated)'], check=False)
            subprocess.run(['git', 'push'], check=False)
        print(f'Applied changes to {len(changed)} files')


if __name__ == '__main__':
    main()
