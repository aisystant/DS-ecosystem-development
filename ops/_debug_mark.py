from pathlib import Path
from difflib import SequenceMatcher
import re, yaml

ROOT = Path.cwd()
md_files = list((ROOT / 'content').rglob('*.md'))
MIN_LEN = 200
THRESHOLD = 0.65

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
clusters = []
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
        clusters.append(group)

print('clusters found:', len(clusters))
for idx,group in enumerate(clusters,1):
    print('\nCluster', idx, 'size', len(group))
    # pick canonical
    lengths = [(p, len(bodies[p])) for p in group]
    lengths.sort(key=lambda x: -x[1])
    canonical = Path(lengths[0][0])
    print(' canonical:', canonical)
    for p in group[:40]:
        pp = Path(p)
        txt = pp.read_text(encoding='utf-8')
        fm = {}
        if txt.startswith('---'):
            parts = txt.split('---',2)
            if len(parts)>=3:
                try:
                    fm = yaml.safe_load(parts[1]) or {}
                except Exception:
                    fm = {}
        print(' -', pp, 'status=', fm.get('status'), 'suggested=', fm.get('suggested_canonical'))
