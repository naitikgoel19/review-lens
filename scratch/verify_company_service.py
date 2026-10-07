import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import os
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, os.path.join(PROJECT_DIR, 'backend'))

from company_service import company_service

# Load platform data
seed_file = os.path.join(PROJECT_DIR, 'data', 'seed_data.json')
with open(seed_file, 'r', encoding='utf-8') as f:
    db = json.load(f)

plat_companies = db.get('companies', [])
plat_products = db.get('products', [])
plat_reviews = db.get('reviews', [])

test_queries = [
    "indigo",
    "IndiGo",
    "razorpay",
    "swiggy",
    "paytm",
    "phonepe",
    "tata motors",
    "microsoft",
    "apple",
    "xyz999nonexistentco"
]

print("=" * 60)
print("TESTING COMPANY SEARCH SERVICE")
print("=" * 60)

for q in test_queries:
    res = company_service.search_companies(
        query=q,
        page=1,
        limit=5,
        platform_companies=plat_companies,
        platform_products=plat_products,
        platform_reviews=plat_reviews
    )
    results = res.get("results", [])
    total = res.get("total", 0)
    source = res.get("source", "")
    print(f"\nQuery: '{q}' -> Total: {total}, Results on page 1: {len(results)}, Source: {source}")
    for idx, c in enumerate(results[:3], 1):
        c_type = c.get("type", "company")
        c_name = c.get("name")
        c_id = c.get("id")
        has_plat = c.get("has_platform_data", False)
        prod_count = c.get("product_count", 0)
        review_count = c.get("review_count", 0)
        print(f"  {idx}. [{c_type}] {c_name} (ID: {c_id}) | Platform data: {has_plat} (Products: {prod_count}, Reviews: {review_count})")

print("\n" + "=" * 60)
print("TESTING GET_COMPANY FOR DISCOVERED COMPANY (ext-...)")
print("=" * 60)
# Test getting the first result from indigo query
indigo_res = company_service.search_companies("indigo", limit=1)
if indigo_res.get("results"):
    sample_id = indigo_res["results"][0]["id"]
    print(f"Fetching details for: {sample_id}")
    comp_detail = company_service.get_company(
        sample_id,
        platform_companies=plat_companies,
        platform_products=plat_products,
        platform_reviews=plat_reviews
    )
    if comp_detail:
        print(f"SUCCESS: Retrieved {comp_detail.get('name')}")
        print(f"  Jurisdiction: {comp_detail.get('jurisdiction')}")
        print(f"  Number: {comp_detail.get('company_number')}")
        print(f"  Has platform data: {comp_detail.get('has_platform_data')}")
        print(f"  Products: {len(comp_detail.get('products', []))}")
        print(f"  Message: {comp_detail.get('message')}")
    else:
        print("FAILED to get company details!")
