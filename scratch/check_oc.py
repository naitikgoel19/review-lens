import urllib.request
import re

url = "https://opencorporates.com/companies?q=indigo"
req = urllib.request.Request(
    url,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }
)

resp = urllib.request.urlopen(req, timeout=10)
html = resp.read().decode("utf-8")

# Let's inspect links with /companies/
links = re.findall(r'href="(/companies/[a-z_0-9]+/[^"]+)"[^>]*>([^<]+)</a>', html)
print(f"Total links matching /companies/: {len(links)}")
for href, text in links[:15]:
    print(href, "->", text.strip())
