import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import re
from typing import Dict, Any, List

def clean_company_display_name(raw_name: str) -> str:
    if not raw_name:
        return ""
    cleaned = raw_name.strip().strip('"\'`«»“”').strip()
    cleaned = re.sub(r'["\'`«»“”]', '', cleaned).strip()
    suffix_pattern = r'''(?ix)
        \s*[\(\[\{]?\s*
        \b(?:
            private\s+limited|pvt\.?\s*ltd\.?|limited|ltd\.?|
            incorporated|inc\.?|corporation|corp\.?|
            llc|l\.l\.c\.?|llp|l\.l\.p\.?|plc|p\.l\.c\.?|
            co\.?|company|
            spółka\s+z\s+ograniczoną\s+odpowiedzialnością|
            spółka\s+z\s+o\.?o\.?|sp\.?\s*z\s*o\.?o\.?|
            gmbh|ag|s\.a\.?|s\.r\.l\.?|s\.l\.?|
            b\.v\.?|n\.v\.?
        )\b
        \s*[\)\]\}]?\s*
    '''
    cleaned = re.sub(suffix_pattern, ' ', cleaned).strip()
    cleaned = re.sub(r'[,.\-_/]+$', '', cleaned).strip()
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    if not cleaned:
        cleaned = raw_name.strip().strip('"\'`«»“”').strip()
    if cleaned.isupper() or cleaned.islower():
        cleaned = cleaned.title()
    return cleaned

def calculate_relevance_score(query: str, company: Dict[str, Any]) -> float:
    q = query.lower().strip()
    name = company.get("name", "").lower().strip()
    legal = company.get("legal_name", "").lower().strip()
    country = company.get("country", "").lower().strip()
    jurisdiction = company.get("jurisdiction_code", "").lower().strip()
    status = company.get("status", "").lower().strip()
    has_platform = company.get("has_platform_data", False)
    cid = company.get("id", "").lower()
    
    score = 0.0
    
    # 1. Exact Name/Brand Match
    if name == q:
        score += 150.0
    elif legal == q:
        score += 130.0
        
    # 2. Known Corporate Relationship (Brand <-> Legal Name)
    if cid == f"c-{q}" or (name == q and legal):
        score += 40.0
        
    # 3. Strong Prefix Match
    if name.startswith(q + " ") or name.startswith(q + "-"):
        score += 80.0
    elif legal.startswith(q + " ") or legal.startswith(q + "-"):
        score += 65.0
        
    # 4. Word boundary match
    words_in_name = re.findall(r'\b\w+\b', name)
    words_in_legal = re.findall(r'\b\w+\b', legal)
    if q in words_in_name:
        if words_in_name and words_in_name[0] == q:
            score += 50.0
        else:
            score += 30.0
    elif q in words_in_legal:
        score += 20.0
        
    # 5. Length penalty for irrelevant extra words
    extra_len = max(0, len(name) - len(q))
    score -= min(40.0, extra_len * 1.5)
    
    # 6. Status: Active vs Inactive
    if "active" in status or "registered" in status:
        score += 25.0
    elif "inactive" in status or "dissolved" in status or "struck" in status:
        score -= 60.0
        
    # 7. Platform Verified
    if has_platform:
        score += 45.0
        
    # 8. Jurisdiction & Market Stature
    major_jurisdictions = {"in", "us", "us_de", "us_ca", "us_wa", "gb", "sg", "de", "ca", "jp", "au"}
    if jurisdiction in major_jurisdictions or country in ["india", "united states", "united kingdom"]:
        score += 15.0
        
    if jurisdiction not in major_jurisdictions and len(words_in_name) > 1:
        score -= 30.0
        
    return score

# Test with candidate list for "indigo"
candidates = [
    {
        "id": "c-indigo",
        "name": "IndiGo",
        "legal_name": "InterGlobe Aviation Limited",
        "country": "India",
        "jurisdiction_code": "in",
        "status": "Active",
        "has_platform_data": False
    },
    {
        "id": "ext-pl-0000195422",
        "name": clean_company_display_name('"INDIGO EUROPE" SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ'),
        "legal_name": '"INDIGO EUROPE" SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ',
        "country": "Poland",
        "jurisdiction_code": "pl",
        "status": "Active",
        "has_platform_data": False
    },
    {
        "id": "ext-pl-0000299030",
        "name": clean_company_display_name('"INDIGO FASHIONS" SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ'),
        "legal_name": '"INDIGO FASHIONS" SPÓŁKA Z OGRANICZONĄ ODPOWIEDZIALNOŚCIĄ',
        "country": "Poland",
        "jurisdiction_code": "pl",
        "status": "Active",
        "has_platform_data": False
    }
]

print("=== SCORING FOR 'indigo' ===")
for c in candidates:
    sc = calculate_relevance_score("indigo", c)
    print(f"Candidate: {c['name']} (Legal: {c['legal_name']}) -> Score: {sc}")

candidates.sort(key=lambda c: calculate_relevance_score("indigo", c), reverse=True)
print("\nRANKED CANDIDATES:")
for idx, c in enumerate(candidates, 1):
    print(f"{idx}. {c['name']} (Legal: {c['legal_name']}, Country: {c['country']})")
