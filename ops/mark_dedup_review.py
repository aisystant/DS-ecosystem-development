#!/usr/bin/env python3
"""Mark deduplication cluster candidates as review (variant C).

Reads ops/dedup_report.md to find clusters, selects a canonical file
per cluster (longest body) and sets `status: review` and
`suggested_canonical` in frontmatter for non-canonical files.
"""
from pathlib import Path
import re
import yaml
import sys

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'ops' / 'dedup_report.md'


def split_frontmatter(text):
    m = re.match(r"^(?:---\n(.*?)\n---\n)?(.*)$", text, re.S)
    if not m:
        return None, text
    fm, body = m.group(1), m.group(2)
    if fm is None:
        return {}, body
    try:
        data = yaml.safe_load(fm) or {}
    except Exception:
        data = {}
    return data, body


def write_with_frontmatter(path: Path, fm: dict, body: str):
    fm_text = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False).strip()
    content = f"---\n{fm_text}\n---\n\n{body.lstrip()}"
    path.write_text(content, encoding='utf-8')


def parse_report(report_path: Path):
    text = report_path.read_text(encoding='utf-8')
    import re
    # Parse cluster sizes from headers
    counts = re.findall(r"##\s*Кластер\s*\d+\s*—\s*(\d+)\s*файлов", text)
    cluster_counts = [int(c) for c in counts] if counts else []

    # Find all content path-like fragments (allow wrapped lines)
    raw_matches = re.findall(r"(content[\\/][\\s\\S]*?\\.md)", text, re.I)
    norm = []
    for m in raw_matches:
        s = m.replace('|', ' ')
        s = ' '.join(s.split())
        s = s.replace('\\', '/')
        idx = s.lower().find('.md')
        if idx != -1:
            s = s[:idx+3]
            norm.append(Path(s.strip()))

    # If we found cluster size hints, split normalized list accordingly, otherwise split into single cluster
    clusters = []
    if cluster_counts and sum(cluster_counts) <= len(norm):
        i = 0
        for cnt in cluster_counts:
            group = norm[i:i+cnt]
            # remove duplicates preserving order
            uniq = []
            for p in group:
                if p not in uniq:
                    uniq.append(p)
            if uniq:
                clusters.append(uniq)
            i += cnt
    else:
        if norm:
            # fallback: group all into a single cluster list
            uniq = []
            for p in norm:
                if p not in uniq:
                    uniq.append(p)
            clusters.append(uniq)
    return clusters


def body_length(path: Path):
    if not path.exists():
        return 0
    data = path.read_text(encoding='utf-8')
    fm, body = split_frontmatter(data)
    return len(body.strip())


def ensure_frontmatter(path: Path):
    text = path.read_text(encoding='utf-8')
    fm, body = split_frontmatter(text)
    if not isinstance(fm, dict):
        fm = {}
    return fm, body


def main():
    # Try to parse report first; if parsing yields no clusters, recompute clusters directly.
    clusters = []
    if REPORT.exists():
        try:
            clusters = parse_report(REPORT)
        except Exception:
            clusters = []

    if not clusters:
        # recompute clusters using the same algorithm as ops/deduplicate_content.py
        from difflib import SequenceMatcher
        MIN_LEN = 200
        THRESHOLD = 0.65
        md_files = list((ROOT / 'content').rglob('*.md'))
        def read_body(p: Path):
            txt = p.read_text(encoding='utf-8')
            if txt.startswith('---'):
                parts = txt.split('---', 2)
                if len(parts) >= 3:
                    return parts[2].strip()
            return txt.strip()
        bodies = {str(p): re.sub(r"\s+", ' ', read_body(p)) for p in md_files}
        paths = list(bodies.keys())
        N = len(paths)
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
                ratio = SequenceMatcher(None, a, b).ratio()
                if ratio >= THRESHOLD:
                    group.append(paths[j])
                    visited.add(paths[j])
            if len(group) > 1:
                clusters.append([Path(p) for p in group])

    modified = []
    for cluster in clusters:
        # filter existing files
        files = [p for p in cluster if p.exists()]
        if len(files) <= 1:
            continue
        # choose canonical as longest body
        lengths = [(body_length(p), p) for p in files]
        lengths.sort(reverse=True)
        canonical = lengths[0][1]
        for p in files:
            if p == canonical:
                # ensure canonical has no suggested_canonical
                fm, body = ensure_frontmatter(p)
                fm.pop('suggested_canonical', None)
                if fm.get('status') == 'review':
                    fm['status'] = 'canonical'
                write_with_frontmatter(p, fm, body)
                continue
            fm, body = ensure_frontmatter(p)
            if fm.get('status') == 'archived' or fm.get('status') == 'stub':
                continue
            fm['status'] = 'review'
            rel = canonical.relative_to(ROOT).as_posix()
            fm['suggested_canonical'] = rel
            fm.setdefault('notes', '')
            fm['notes'] = (fm.get('notes','') + '\nMarked by ops/mark_dedup_review.py as cluster candidate').strip()
            write_with_frontmatter(p, fm, body)
            modified.append(p.relative_to(ROOT).as_posix())

    print(f"Clusters processed: {len(clusters)}")
    print(f"Files marked as review: {len(modified)}")
    for m in modified[:200]:
        print(m)


if __name__ == '__main__':
    main()
