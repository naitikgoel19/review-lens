import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import os, json
sys.path.insert(0, os.path.abspath('backend'))

from company_service import company_service

with open('data/seed_data.json', 'r', encoding='utf-8') as f:
    db = json.load(f)

for q in ["indigo", "IndiGo", "razorpay", "microsoft", "apple", "amazon", "tata"]:
    res = company_service.search_companies(
        query=q,
        page=1,
        limit=5,
        platform_companies=db.get("companies", []),
        platform_products=db.get("products", []),
        platform_reviews=db.get("reviews", []),
    )
    primary = res.get("primary")
    results = res.get("results", [])
    print(f"\n================ QUERY: '{q}' ================")
    if primary:
        print(f"PRIMARY MATCH:")
        print(f"  Name: {primary.get('name')}")
        print(f"  Legal: {primary.get('legal_name')}")
        print(f"  Country: {primary.get('country')}")
        print(f"  Industry: {primary.get('industry')}")
        print(f"  Status: {primary.get('status')}")
        print(f"  Platform Data: {primary.get('has_platform_data')}")
        print(f"  Source: {primary.get('source')}")
    else:
        print("NO PRIMARY MATCH FOUND")

    print(f"TOTAL RESULTS: {len(results)}")
    for idx, r in enumerate(results[:3], 1):
        print(f"  {idx}. {r.get('name')} | Legal: {r.get('legal_name')} | {r.get('country')}")
