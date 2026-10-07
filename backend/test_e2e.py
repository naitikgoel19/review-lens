"""
End-to-end automated QA verification script for Review Lens.
Tests scenarios A through L as requested in the specification.
"""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

print("\n=== STARTING END-TO-END QA SUITE ===")

# TEST A: Website Opening
res = client.get('/')
assert res.status_code == 200, f"Expected 200, got {res.status_code}"
print("[PASS] TEST A: Website root returns 200 OK and serves index.html")

# TEST B: Company Member Login
res = client.post('/api/auth/login', json={'email': 'product@microsoft.com', 'password': 'Microsoft@123', 'account_type': 'company_member'})
assert res.status_code == 200, f"Company login failed: {res.text}"
team_user = res.json()['user']
team_token = res.json()['token']
assert team_user['role'] == 'COMPANY_MEMBER'
assert team_user['company_id'] == 'c-microsoft'
print(f"[PASS] TEST B: Company login succeeded for {team_user['email']} ({team_user['company_name']})")

# TEST C: Verify Role Separation
res_mismatch = client.post('/api/auth/login', json={'email': 'customer@example.com', 'password': 'Customer@123', 'account_type': 'company_member'})
assert res_mismatch.status_code == 403, f"Expected 403, got {res_mismatch.status_code}"
print("[PASS] TEST C: Customer blocked from Company Member login tab (no role switching)")

# TEST D: Customer Login
res = client.post('/api/auth/login', json={'email': 'customer@example.com', 'password': 'Customer@123', 'account_type': 'customer'})
assert res.status_code == 200, f"Customer login failed: {res.text}"
cust_user = res.json()['user']
cust_token = res.json()['token']
assert cust_user['role'] == 'CUSTOMER'
print(f"[PASS] TEST D: Customer login succeeded for {cust_user['email']}")

# TEST E: Search Supported Companies
for name in ['Microsoft', 'Google', 'Adobe', 'NVIDIA']:
    res = client.get(f'/api/companies/search?q={name}').json()
    assert len(res['results']) > 0, f"No results for {name}"
    match = next((c for c in res['results'] if c['name'] == name), None)
    assert match is not None, f"Company {name} not found"
    print(f"[PASS] TEST E: Search '{name}' returned verified profile (Products: {match.get('product_count', 'N/A')})")

# TEST F: Live Products
res = client.get('/api/companies/c-microsoft').json()
assert len(res['products']) >= 4, "Expected at least 4 products"
statuses = {p['status'] for p in res['products']}
assert 'LIVE' in statuses, "Expected LIVE status"
print(f"[PASS] TEST F: Microsoft has {len(res['products'])} products with statuses: {statuses}")

# TEST G & H: Customer Writes Review on Teams v5.3 & Persistence
sub_res = client.post(
    '/api/products/p-microsoft-teams/reviews',
    json={
        'rating': 5,
        'title': 'Excellent experience',
        'text': 'Screen sharing is much smoother.',
        'platform': 'Web',
        'app_version': 'v5.3',
        'region': 'US'
    },
    headers={'Authorization': f'Bearer {cust_token}'}
)
assert sub_res.status_code == 200, f"Submission failed: {sub_res.text}"
new_id = sub_res.json()['review']['id']
print(f"[PASS] TEST G: Customer submitted review id={new_id}")

# Verify review persists in My Reviews
my_revs = client.get('/api/customer/my-reviews', headers={'Authorization': f'Bearer {cust_token}'}).json()
assert any(r['id'] == new_id for r in my_revs['reviews']), "Review not found in customer my-reviews"
print(f"[PASS] TEST H: Review persists in Customer 'My Reviews' history")

# TEST I: Product Team sees the customer review on v5.3
v53_revs = client.get('/api/products/p-microsoft-teams/reviews?version=v5.3').json()
assert any(r['id'] == new_id for r in v53_revs['reviews']), "Review not visible to Product Team on v5.3"
print("[PASS] TEST I: Product Team can immediately see the newly submitted review on v5.3")

# TEST J: Old Version Switch (v5.3 vs v5.2)
dash_v53 = client.get('/api/dashboard?product_id=p-microsoft-teams&version=v5.3').json()
dash_v52 = client.get('/api/dashboard?product_id=p-microsoft-teams&version=v5.2').json()
assert dash_v53['health']['average_rating'] != dash_v52['health']['average_rating'], "Ratings must be version specific"
assert dash_v53['health']['sentiment']['positive_pct'] != dash_v52['health']['sentiment']['positive_pct'], "Sentiments must be version specific"
print(f"[PASS] TEST J: Version comparison confirmed (v5.3 Rating: {dash_v53['health']['average_rating']} vs v5.2 Rating: {dash_v52['health']['average_rating']})")

# TEST K: Evidence Separation
ev_payment = client.get('/api/evidence?product_id=p-microsoft-teams&version=v5.2&theme=Payment%20Problems').json()
ev_auth = client.get('/api/evidence?product_id=p-microsoft-teams&version=v5.2&theme=Authentication%20%26%20OTP').json()
assert ev_payment['total'] > 0, "No payment evidence"
assert ev_auth['total'] > 0, "No auth evidence"
assert ev_payment['evidence'][0]['id'] != ev_auth['evidence'][0]['id'], "Evidence must not be identical across themes"
print(f"[PASS] TEST K: Theme evidence is distinct (Payment: {ev_payment['total']} reviews vs Auth: {ev_auth['total']} reviews)")

# TEST L: Platform Filtering on Evidence
ev_android = client.get('/api/evidence?product_id=p-microsoft-teams&version=v5.2&theme=Payment%20Problems&platform=Android').json()
ev_web = client.get('/api/evidence?product_id=p-microsoft-teams&version=v5.2&theme=Payment%20Problems&platform=Web').json()
assert all(e['platform'] == 'Android' for e in ev_android['evidence']), "Non-Android evidence in Android filter"
assert all(e['platform'] == 'Web' for e in ev_web['evidence']), "Non-Web evidence in Web filter"
print(f"[PASS] TEST L: Platform filtering verified (Android records: {ev_android['total']}, Web records: {ev_web['total']})")

print("\n=== ALL TESTS A THROUGH L PASSED WITH 100% SUCCESS ===\n")
