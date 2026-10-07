import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import urllib.request
import urllib.parse
import json
import os

BASE_URL = "http://127.0.0.1:8000"

def get(path):
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url, headers={"User-Agent": "ReviewLens-TestRunner"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))

print("==================================================================")
print("REVIEW LENS — GLOBAL COMPANY DISCOVERY VERIFICATION SUITE")
print("==================================================================")

# 1. Health check
health = get("/api/health")
print(f"[✓] Health Check: {health.get('status')} (Version: {health.get('version')})")

# 2. Test key global companies
test_cases = [
    "indigo",
    "IndiGo",
    "razorpay",
    "swiggy",
    "zomato",
    "paytm",
    "phonepe",
    "apple",
    "amazon",
    "tata motors",
    "microsoft"
]

all_passed = True

for q in test_cases:
    encoded = urllib.parse.quote(q)
    data = get(f"/api/companies/search?q={encoded}&limit=5")
    results = data.get("results", [])
    total = data.get("total", 0)
    source = data.get("source", "")

    if len(results) == 0:
        print(f"[FAIL] Query '{q}' returned 0 results!")
        all_passed = False
    else:
        first = results[0]
        name = first.get("name")
        cid = first.get("id")
        has_plat = first.get("has_platform_data")
        print(f"[✓ PASS] Query '{q}': {len(results)} results (Total: {total}, Source: {source})")
        print(f"         First: {name} (ID: {cid}, Has Platform Data: {has_plat})")

# 3. Test company details for an external discovered entity
print("\n--- Testing Company Details Endpoint for Discovered Entity ---")
indigo_data = get("/api/companies/search?q=indigo&limit=1")
if indigo_data.get("results"):
    ext_id = indigo_data["results"][0]["id"]
    comp_detail = get(f"/api/companies/{ext_id}")
    print(f"[✓ PASS] Retrieved details for {ext_id}:")
    print(f"         Name: {comp_detail.get('name')}")
    print(f"         Has Platform Data: {comp_detail.get('has_platform_data')}")
    print(f"         Products: {len(comp_detail.get('products', []))}")
    print(f"         Message: {comp_detail.get('message')}")
    assert comp_detail.get('has_platform_data') == False
    assert len(comp_detail.get('products', [])) == 0

# 4. Test platform company (Microsoft)
print("\n--- Testing Platform Company Details Endpoint (Microsoft) ---")
msft_detail = get("/api/companies/c-microsoft")
print(f"[✓ PASS] Retrieved Microsoft Platform Data:")
print(f"         Name: {msft_detail.get('name')}")
print(f"         Has Platform Data: {msft_detail.get('has_platform_data')}")
print(f"         Products Count: {len(msft_detail.get('products', []))}")
assert msft_detail.get('has_platform_data') == True
assert len(msft_detail.get('products', [])) >= 4

# 5. Verify security (.env and .gitignore)
print("\n--- Testing Security Requirements ---")
gitignore_path = ".gitignore"
if os.path.exists(gitignore_path):
    with open(gitignore_path, "r", encoding="utf-8") as f:
        content = f.read()
        if ".env" in content:
            print("[✓ PASS] .env is properly listed in .gitignore")
        else:
            print("[FAIL] .env is NOT in .gitignore!")
            all_passed = False

# Check frontend files for hardcoded API keys
with open("frontend/app.js", "r", encoding="utf-8") as f:
    f_content = f.read()
    if "OPENCORPORATES_API_TOKEN" in f_content or "api_token" in f_content:
        print("[FAIL] Token reference found in frontend code!")
        all_passed = False
    else:
        print("[✓ PASS] Frontend code has NO token references or keys")

print("\n==================================================================")
if all_passed:
    print("ALL GLOBAL COMPANY DISCOVERY VERIFICATION TESTS PASSED SUCCESSFULLY!")
else:
    print("SOME TESTS FAILED.")
print("==================================================================")
