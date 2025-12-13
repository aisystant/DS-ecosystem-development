#!/usr/bin/env python3
"""Collect metrics about content/ after normalization and dedup steps.
Writes ops/metrics_report.md and prints a short summary.
"""
from pathlib import Path
import re
import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'content'
REPORT = ROOT / 'ops' / 'metrics_report.md'

REQ_KEYS = ['type', 'status', 'created', 'layer', 'scope']


def split_frontmatter(text):
    m = re.match(r"^(?:---\n(.*?)\n---\n)?(.*)$", text, re.S)
    if not m:
        return {}, text
    fm = m.group(1)
    body = m.group(2)
    if not fm:
        return {}, body
    try:
        data = yaml.safe_load(fm) or {}
    except Exception:
        data = {}
    return data, body


def main():
    md_files = list(CONTENT.rglob('*.md'))
    total = len(md_files)

    missing_keys = 0
    key_counts = {k: 0 for k in REQ_KEYS}
    status_counts = {}
    alias_count = 0
    suggested_count = 0

    for p in md_files:
        txt = p.read_text(encoding='utf-8')
        fm, body = split_frontmatter(txt)
        if not isinstance(fm, dict):
            fm = {}
        for k in REQ_KEYS:
            if k in fm:
                key_counts[k] += 1
            else:
                missing_keys += 1
        st = fm.get('status') or 'none'
        status_counts[st] = status_counts.get(st, 0) + 1
        if fm.get('aliases'):
            alias_count += 1
        if fm.get('suggested_canonical'):
            suggested_count += 1

    # read dedup report if exists
    dedup_summary = 'not found'
    dedup_path = ROOT / 'ops' / 'dedup_report.md'
    clusters = 0
    if dedup_path.exists():
        txt = dedup_path.read_text(encoding='utf-8')
        m = re.search(r"Обнаружено кластеров дублей:\s*(\d+)", txt)
        if m:
            clusters = int(m.group(1))
            dedup_summary = f'{clusters} clusters'

    lines = []
    lines.append('# Metrics report')
    lines.append('')
    lines.append(f'- Total markdown files: {total}')
    lines.append(f'- Required frontmatter keys present counts:')
    for k,v in key_counts.items():
        lines.append(f'  - {k}: {v}')
    lines.append(f'- Files with any missing required key (approx): {missing_keys}')
    lines.append(f'- Files with `aliases`: {alias_count}')
    lines.append(f'- Files with `suggested_canonical`: {suggested_count}')
    lines.append('- Status distribution:')
    for s,v in sorted(status_counts.items(), key=lambda x:-x[1]):
        lines.append(f'  - {s}: {v}')
    lines.append(f'- Deduplication summary: {dedup_summary}')

    REPORT.write_text('\n'.join(lines), encoding='utf-8')
    print('\n'.join(lines[:10]))
    print('...')


if __name__ == '__main__':
    main()
