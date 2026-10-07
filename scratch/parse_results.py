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

# Extract each li
items = re.findall(r"<li\s+class=['\"][^'\"]*search-result\s+company[^'\"]*['\"][^>]*>(.*?)</li>", html, re.DOTALL)
print(f"Total parsed results: {len(items)}")

for i, it in enumerate(items[:10]):
    # Match link: href="/companies/([a-z_0-9]+)/([^"]+)"
    link_match = re.search(r'href="/companies/([a-z_0-9]+)/([^"]+)"[^>]*>([^<]+)</a>', it)
    if link_match:
        jur = link_match.group(1)
        num = link_match.group(2)
        name = link_match.group(3).strip().replace("&quot;", '"').replace("&amp;", '&')
        # Extract country/jurisdiction in parentheses
        country_match = re.search(r'\(([^)]+)\)', it)
        country = country_match.group(1) if country_match else jur.upper()
        print(f"[{i+1}] Name: {name} | Jur: {jur} | Number: {num} | Country: {country}")
