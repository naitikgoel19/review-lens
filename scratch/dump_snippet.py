import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import urllib.request
import re

url = "https://opencorporates.com/companies?q=indigo"
req = urllib.request.Request(
    url,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }
)

html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")

# Find the first occurrence of /companies/
pos = html.find('/companies/')
if pos != -1:
    print(html[max(0, pos-200):pos+600])
