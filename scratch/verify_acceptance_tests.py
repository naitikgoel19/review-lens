import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import urllib.request
import urllib.parse
import json

BASE_URL = "http://127.0.0.1:8000"

def get(path):
    url = f"{BASE_URL}{path}"
    req = urllib.request.Request(url, headers={"User-Agent": "ReviewLens-AcceptanceTester"})
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode("utf-8"))

print("=" * 70)
print("REVIEW LENS — FINAL ACCEPTANCE VERIFICATION")
print("=" * 70)

tests = [
    ("indigo", "IndiGo", "InterGlobe Aviation Limited", "India"),
    ("IndiGo", "IndiGo", "InterGlobe Aviation Limited", "India"),
    ("razorpay", "Razorpay", "Razorpay Software Private Limited", "India"),
    ("microsoft", "Microsoft", "Microsoft Corporation", "United States"),
    ("apple", "Apple", "Apple Inc.", "United States"),
    ("amazon", "Amazon", "Amazon.com, Inc.", "United States"),
    ("tata", "TCS", "Tata Consultancy Services Limited", "India"),
]

all_passed = True

for query, expected_name, expected_legal, expected_country in tests:
    encoded_q = urllib.parse.quote(query)
    data = get(f"/api/companies/search?q={encoded_q}&limit=5")
    primary = data.get("primary")
    results = data.get("results", [])

    if not primary:
        print(f"[FAIL] Query '{query}': No primary match returned!")
        all_passed = False
        continue

    p_name = primary.get("name")
    p_legal = primary.get("legal_name")
    p_country = primary.get("country")
    p_status = primary.get("status")
    p_plat = primary.get("has_platform_data")
    p_source = primary.get("source")

    name_ok = (expected_name.lower() in p_name.lower())
    country_ok = (expected_country.lower() in p_country.lower())

    if name_ok and country_ok:
        print(f"[✓ PASS] Query '{query}'")
        print(f"         PRIMARY: {p_name} | Legal: {p_legal} | {p_country} | Status: {p_status}")
        print(f"         Source: {p_source} | Platform Verified: {p_plat}")
        print(f"         Other Matches: {len(results) - 1} secondary entities")
    else:
        print(f"[FAIL] Query '{query}': Got {p_name} ({p_country}), expected {expected_name} ({expected_country})")
        all_passed = False

print("\n--- Verifying Company Profile for IndiGo (External Discovery) ---")
indigo_profile = get("/api/companies/c-indigo")
print(f"Name: {indigo_profile.get('name')}")
print(f"Legal Name: {indigo_profile.get('legal_name')}")
print(f"Has Platform Data: {indigo_profile.get('has_platform_data')}")
print(f"Products Count: {len(indigo_profile.get('products', []))}")
print(f"Reviews Count: {indigo_profile.get('total_reviews')}")
print(f"Notice: {indigo_profile.get('message')}")

assert indigo_profile.get('name') == "IndiGo"
assert indigo_profile.get('has_platform_data') == False
assert len(indigo_profile.get('products', [])) == 0
assert indigo_profile.get('total_reviews') == 0
print("[✓ PASS] IndiGo profile correctly shows un-onboarded state with 0 products/reviews!")

print("\n--- Verifying Platform Company (Microsoft) ---")
msft_profile = get("/api/companies/c-microsoft")
print(f"Name: {msft_profile.get('name')}")
print(f"Has Platform Data: {msft_profile.get('has_platform_data')}")
print(f"Products Count: {len(msft_profile.get('products', []))}")
assert msft_profile.get('has_platform_data') == True
assert len(msft_profile.get('products', [])) >= 4
print("[✓ PASS] Microsoft platform telemetry preserved!")

print("\n" + "=" * 70)
if all_passed:
    print("ALL ACCEPTANCE TESTS PASSED WITH 100% SUCCESS!")
else:
    print("SOME ACCEPTANCE TESTS FAILED!")
print("=" * 70)
