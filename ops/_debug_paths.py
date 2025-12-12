from pathlib import Path
import re

ROOT = Path.cwd()
text = (ROOT / 'ops' / 'dedup_report.md').read_text(encoding='utf-8')
matches = re.findall(r"(content[\\\\/][^\\\\n|]+?\\\\.md)", text)
print('matches found:', len(matches))
for p in matches[:20]:
    pnorm = Path(p.replace('\\\\','/'))
    full = ROOT / pnorm
    print(pnorm.as_posix(), '->', full.exists())
