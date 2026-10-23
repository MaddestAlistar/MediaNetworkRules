#!/usr/bin/env python3
"""Generate NON production routing snippets from audited CSV rules."""
import csv
import ipaddress
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
rows=list(csv.DictReader((ROOT/'rules'/'domains.csv').open(encoding='utf-8',newline='')))
for r in rows:
    assert r['type'] in ('DOMAIN', 'DOMAIN-SUFFIX')
    assert r['policy'] in ('DIRECT','PROXY','REJECT')
    assert r['pattern'] and '/' not in r['pattern'] and '://' not in r['pattern']
cidrs=[]
for line in (ROOT/'rules'/'lan-cidrs.txt').read_text().splitlines():
    line=line.strip()
    if not line or line.startswith('#'): continue
    network=ipaddress.ip_network(line, strict=True)
    if not network.is_private: raise ValueError('Public CIDR requires explicit review: '+line)
    cidrs.append(line)
out=ROOT/'generated'
out.mkdir(exist_ok=True)
surge=['# LiangYou: Surge rule lines (insert into [Rule]); template ONLY']+[f"{r['type']},{r['pattern']},{r['policy']}" for r in rows]+[f"IP-CIDR,{c},DIRECT,no-resolve" for c in cidrs]
(out/'surge-rules.conf').write_text('\n'.join(surge)+'\n',encoding='utf-8')
clash=['# LiangYou: Clash rule-provider classical payload; set rule-provider policy in your full config','payload:']+[f"  - '{r['type']},{r['pattern']}'" for r in rows]+[f"  - 'IP-CIDR,{c},no-resolve'" for c in cidrs]
(out/'clash-provider.yaml').write_text('\n'.join(clash)+'\n',encoding='utf-8')
qx=['# LiangYou: Quantumult X filter_local snippets (replace demo hosts first)','[filter_local]']+[f"host-suffix,{r['pattern']},{r['policy'].lower()}" for r in rows]+[f"ip-cidr,{c},direct,no-resolve" for c in cidrs]
(out/'quanx-filter.conf').write_text('\n'.join(qx)+'\n',encoding='utf-8')
print(f"Generated 3 files from {len(rows)} domains and {len(cidrs)} LAN ranges")
