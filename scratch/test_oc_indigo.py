import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import urllib.request
import urllib.parse
import re

urls = [
    ("indigo & in", "https://opencorporates.com/companies?q=indigo&jurisdiction_code=in"),
    ("indigo in India", "https://opencorporates.com/companies?q=indigo+india"),
    ("indigo aviation", "https://opencorporates.com/companies?q=indigo+aviation"),
    ("interglobe aviation", "https://opencorporates.com/companies?q=interglobe+aviation"),
]

for label, url in urls:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    try:
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='replace')
        items = re.findall(r"<li\s+class=['\"][^'\"]*search-result\s+company[^'\"]*['\"][^>]*>(.*?)</li>", html, re.DOTALL)
        print(f"\n=== {label} ({len(items)} results) ===")
        for it in items[:6]:
            m = re.search(r'href="/companies/([a-z0-9_]+)/([^"]+)"[^>]*>([^<]+)</a>', it)
            if m:
                country_m = re.search(r'\(([^)]+)\)', it)
                country = country_m.group(1) if country_m else m.group(1)
                print(f"  {m.group(3).strip()} | {country} | {m.group(1)}/{m.group(2)}")
    except Exception as e:
        print(f"Error for {label}: {e}")
