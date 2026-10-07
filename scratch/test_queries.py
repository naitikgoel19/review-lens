import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import urllib.request
import urllib.parse
import re

for test_q in ["indigo", "razorpay", "swiggy", "paytm", "tata motors"]:
    url = f"https://opencorporates.com/companies?q={urllib.parse.quote(test_q)}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }
    )
    try:
        html = urllib.request.urlopen(req, timeout=10).read().decode("utf-8")
        items = re.findall(r"<li\s+class=['\"][^'\"]*search-result\s+company[^'\"]*['\"][^>]*>(.*?)</li>", html, re.DOTALL)
        print(f"\nQuery '{test_q}' -> {len(items)} results found:")
        for it in items[:3]:
            link_match = re.search(r'href="/companies/([a-z_0-9]+)/([^"]+)"[^>]*>([^<]+)</a>', it)
            if link_match:
                name = link_match.group(3).strip().replace("&quot;", '"').replace("&amp;", '&')
                jur = link_match.group(1)
                num = link_match.group(2)
                country_match = re.search(r'\(([^)]+)\)', it)
                country = country_match.group(1) if country_match else jur.upper()
                print(f"  * {name} | {country} | {jur}/{num}")
    except Exception as e:
        print(f"Query '{test_q}' failed: {e}")
