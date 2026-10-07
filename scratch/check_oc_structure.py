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

# Let's inspect the list items with class company or search_result
# Usually <li class="search-result company"> or similar
items = re.findall(r'<li[^>]*class="[^"]*search-result[^"]*"[^>]*>(.*?)</li>', html, re.DOTALL)
print("Search result list items count:", len(items))

if not items:
    # Try another pattern
    items = re.findall(r'<li[^>]*class="[^"]*company[^"]*"[^>]*>(.*?)</li>', html, re.DOTALL)
    print("Alternative li.company count:", len(items))

for i, it in enumerate(items[:5]):
    print(f"\n--- ITEM {i+1} ---")
    print(it[:400])
