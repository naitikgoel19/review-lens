import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import urllib.request
import urllib.parse
import re

url = 'https://opencorporates.com/companies?q=indigo'
req = urllib.request.Request(
    url,
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }
)
html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
items = re.findall(r'<li\s+class=[\'"][^\'"]*search-result\s+company[^\'"]*[\'"][^>]*>(.*?)</li>', html, re.DOTALL)
for i in range(min(5, len(items))):
    print(f'--- ITEM {i} ---')
    print(items[i].strip())
