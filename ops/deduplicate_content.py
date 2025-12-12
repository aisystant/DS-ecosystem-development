#!/usr/bin/env python3
"""Detect near-duplicate Markdown documents in content/ using difflib similarity.
Outputs a report `ops/dedup_report.md` with clusters and a recommended canonical file per cluster.

Usage: python ops/deduplicate_content.py
"""
from pathlib import Path
import difflib
import re

CONTENT = Path('content')
REPORT = Path('ops') / 'dedup_report.md'
MIN_LEN = 200  # skip very short files
THRESHOLD = 0.65

# read all md files
md_files = list(CONTENT.rglob('*.md'))
print(f'Found {len(md_files)} markdown files under content/')

# helper to extract body (strip frontmatter)
def read_body(p: Path):
    txt = p.read_text(encoding='utf-8')
    if txt.startswith('---'):
        parts = txt.split('---', 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return txt.strip()

bodies = {}
for p in md_files:
    body = read_body(p)
    bodies[str(p)] = re.sub(r'\s+', ' ', body)

# compute pairwise similarities (upper-triangular)
paths = list(bodies.keys())
N = len(paths)
clusters = []
visited = set()

for i in range(N):
    if paths[i] in visited:
        continue
    a = bodies[paths[i]]
    if len(a) < MIN_LEN:
        continue
    group = [paths[i]]
    visited.add(paths[i])
    for j in range(i+1, N):
        if paths[j] in visited:
            continue
        b = bodies[paths[j]]
        if len(b) < MIN_LEN:
            continue
        ratio = difflib.SequenceMatcher(None, a, b).ratio()
        if ratio >= THRESHOLD:
            group.append(paths[j])
            visited.add(paths[j])
    if len(group) > 1:
        clusters.append(group)

# refine clusters by picking canonical (largest body length) and compute sizes
report_lines = ["# Дедупликация контента — отчёт\n"]
report_lines.append(f"Всего MD файлов: {N}")
report_lines.append(f"Минимальная длина для сравнения: {MIN_LEN} символов")
report_lines.append(f"Порог похожести: {THRESHOLD}\n")
report_lines.append(f"Обнаружено кластеров дублей: {len(clusters)}\n")

for idx, group in enumerate(clusters, 1):
    report_lines.append(f"## Кластер {idx} — {len(group)} файлов")
    # choose canonical as file with largest length
    lengths = [(p, len(bodies[p])) for p in group]
    canonical = max(lengths, key=lambda x: x[1])[0]
    report_lines.append(f"**Рекомендованный канонический файл:** {canonical}")
    report_lines.append('| Путь | Длина (симв) |')
    report_lines.append('|------|---------------|')
    for p,l in sorted(lengths, key=lambda x: -x[1]):
        report_lines.append(f"| {p} | {l} |")
    report_lines.append('\n')

REPORT.write_text('\n'.join(report_lines), encoding='utf-8')
print(f'Wrote report to {REPORT} with {len(clusters)} clusters')
