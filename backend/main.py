"""
Review Lens — Production-Grade FastAPI Backend Server
Serves REST APIs and static frontend files for customer review intelligence.
"""

import os
import sys
import json
import uuid
import hashlib
from datetime import datetime
from typing import Optional, Dict, Any, List

def generate_id() -> str:
    return str(uuid.uuid4())

from fastapi import FastAPI, HTTPException, Query, Body, Header, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Add backend directory to path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from analytics_engine import AnalyticsEngine
from pii_engine import PIIEngine
from company_service import company_service, GLOBAL_ENTERPRISE_DIRECTORY

# ─── APP SETUP ────────────────────────────────────────────────────────

app = FastAPI(
    title="Review Lens API",
    description="Enterprise Customer Review Intelligence & Product Feedback Platform",
    version="2.0.0",
)

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "product": "Review Lens",
        "team": "InsightX",
        "version": "2.0.0"
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── DATA STORE ───────────────────────────────────────────────────────

DATA_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "data"))
DATA_FILE = os.path.join(DATA_DIR, "seed_data.json")

_data_store: Dict[str, Any] = {}
_sessions: Dict[str, Dict[str, Any]] = {}


def load_data() -> Dict[str, Any]:
    """Load data from JSON file with lazy seeding if absent."""
    global _data_store
    if not _data_store:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                _data_store = json.load(f)
        else:
            from data_generator import generate_all_data, save_data
            _data_store = generate_all_data()
            save_data(_data_store, DATA_FILE)
    return _data_store


def save_data_to_disk():
    """Persist data changes safely to disk."""
    if _data_store:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(_data_store, f, indent=2, ensure_ascii=False, default=str)


def get_data() -> Dict[str, Any]:
    return load_data()


def get_user_from_token(token: Optional[str]) -> Optional[Dict[str, Any]]:
    """Resolve user from session token."""
    if not token:
        return None
    session = _sessions.get(token)
    if not session:
        return None
    data = get_data()
    users = data.get("users", [])
    return next((u for u in users if u["id"] == session["user_id"]), None)


# ─── MODELS ───────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    email: str
    password: str
    account_type: Optional[str] = None  # "company_member" or "customer"

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str = "CUSTOMER"
    company_id: Optional[str] = None

class ReviewSubmission(BaseModel):
    rating: int = Field(ge=1, le=5)
    title: Optional[str] = ""
    text: str
    category: str = "General"
    platform: str = "Web"
    app_version: Optional[str] = None
    region: Optional[str] = "US"
    is_anonymous: bool = False

class ActionCreate(BaseModel):
    title: str
    owner: str
    priority: str = "high"
    expected_impact: str = "high"

class IssueStatusUpdate(BaseModel):
    status: str
    verify_after_days: Optional[int] = 14


# ─── AUTH ENDPOINTS ───────────────────────────────────────────────────

@app.post("/api/auth/login")
def login(req: LoginRequest):
    data = get_data()
    users = data.get("users", [])

    req_email = req.email.strip().lower()
    user = next((u for u in users if u["email"].strip().lower() == req_email), None)

    if not user or user["password"] != req.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Validate account type selector
    if req.account_type:
        account_type = req.account_type.upper().strip()
        user_role = user.get("role", "CUSTOMER").upper().strip()
        if account_type == "COMPANY_MEMBER" and user_role not in ("COMPANY_MEMBER", "PRODUCT_TEAM"):
            raise HTTPException(
                status_code=403,
                detail="This account is registered as a Customer. Please switch to the 'Customer' sign in tab."
            )
        elif account_type == "CUSTOMER" and user_role in ("COMPANY_MEMBER", "PRODUCT_TEAM"):
            raise HTTPException(
                status_code=403,
                detail="This account is registered as a Company Member. Please switch to the 'Company Member' sign in tab."
            )

    token = hashlib.sha256(f"{user['id']}{datetime.now().isoformat()}".encode()).hexdigest()[:32]
    _sessions[token] = {"user_id": user["id"], "created_at": datetime.now().isoformat()}

    return {
        "token": token,
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "avatar": user.get("avatar", ""),
            "company_id": user.get("company_id"),
            "company_name": user.get("company_name", ""),
        },
    }


@app.post("/api/auth/signup")
def signup(req: SignupRequest):
    data = get_data()
    users = data.get("users", [])

    req_email = req.email.strip().lower()
    if any(u["email"].strip().lower() == req_email for u in users):
        raise HTTPException(status_code=400, detail="Email is already registered")

    role = req.role.upper().strip()
    if role not in ("CUSTOMER", "COMPANY_MEMBER"):
        role = "CUSTOMER"

    new_user = {
        "id": f"user-{len(users) + 1}",
        "name": req.name,
        "email": req.email,
        "password": req.password,
        "role": role,
        "company_id": req.company_id if role == "COMPANY_MEMBER" else None,
        "avatar": f"https://ui-avatars.com/api/?name={req.name.replace(' ', '+')}&background=2F8F6B&color=fff",
        "created_at": datetime.now().isoformat(),
    }
    users.append(new_user)
    save_data_to_disk()

    token = hashlib.sha256(f"{new_user['id']}{datetime.now().isoformat()}".encode()).hexdigest()[:32]
    _sessions[token] = {"user_id": new_user["id"], "created_at": datetime.now().isoformat()}

    return {
        "token": token,
        "user": {
            "id": new_user["id"],
            "name": new_user["name"],
            "email": new_user["email"],
            "role": new_user["role"],
            "company_id": new_user.get("company_id"),
            "avatar": new_user["avatar"],
        },
    }


@app.get("/api/auth/me")
def get_current_user(authorization: Optional[str] = Header(None)):
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:].strip()
    user = get_user_from_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Session expired or invalid")
    return {
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "avatar": user.get("avatar", ""),
            "company_id": user.get("company_id"),
            "company_name": user.get("company_name", ""),
        }
    }


# ─── CUSTOMER SPECIFIC ENDPOINTS ─────────────────────────────────────

@app.get("/api/customer/my-reviews")
def get_customer_reviews(authorization: Optional[str] = Header(None)):
    """Fetch review history for the currently logged-in customer."""
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:].strip()
    user = get_user_from_token(token)

    data = get_data()
    reviews = data.get("reviews", [])
    products = {p["id"]: p for p in data.get("products", [])}
    companies = {c["id"]: c for c in data.get("companies", [])}

    if user:
        # Match by customer_id or user email or name
        my_reviews = [
            r for r in reviews
            if r.get("customer_id") == user["id"]
            or r.get("user_name", "").lower() == user["name"].lower()
            or (user["email"] == "customer@example.com" and r.get("customer_id") == "user-customer-main")
        ]
    else:
        # Fallback to customer reviews
        my_reviews = [r for r in reviews if r.get("customer_id") == "user-customer-main"]

    enriched = []
    for r in my_reviews:
        product = products.get(r.get("product_id"), {})
        company = companies.get(product.get("company_id"), {})
        enriched.append({
            **r,
            "product_name": product.get("name", "Unknown Product"),
            "company_name": company.get("name", "Unknown Company"),
            "company_logo": company.get("logo_url", ""),
        })

    enriched.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return {"reviews": enriched, "total": len(enriched)}


# ─── COMPANY ENDPOINTS ───────────────────────────────────────────────

@app.get("/api/companies")
def get_companies():
    data = get_data()
    companies = data.get("companies", [])
    products = data.get("products", [])
    reviews = data.get("reviews", [])

    enriched = []
    for company in companies:
        company_products = [p for p in products if p["company_id"] == company["id"]]
        company_product_ids = {p["id"] for p in company_products}
        company_reviews = [r for r in reviews if r.get("product_id") in company_product_ids]

        avg_rating = round(sum(r["rating"] for r in company_reviews) / len(company_reviews), 1) if company_reviews else 0.0

        enriched.append({
            **company,
            "product_count": len(company_products),
            "review_count": len(company_reviews),
            "average_rating": avg_rating,
        })

    return {"companies": enriched}


@app.get("/api/companies/search")
def search_companies(
    q: str = Query("", min_length=0),
    page: int = Query(1, ge=1),
    limit: int = Query(15, ge=1, le=50),
    request: Request = None,
):
    data = get_data()
    companies = data.get("companies", [])
    products = data.get("products", [])
    reviews = data.get("reviews", [])

    client_ip = "127.0.0.1"
    if request and request.client:
        client_ip = request.client.host

    return company_service.search_companies(
        query=q,
        page=page,
        limit=limit,
        platform_companies=companies,
        platform_products=products,
        platform_reviews=reviews,
        client_id=client_ip
    )


@app.get("/api/companies/{company_id}")
def get_company(company_id: str):
    data = get_data()
    companies = data.get("companies", [])
    products = data.get("products", [])
    reviews = data.get("reviews", [])
    releases = data.get("releases", [])

    company = next((c for c in companies if c["id"] == company_id), None)

    # If company not in platform companies, check enterprise search service
    if not company:
        comp_profile = company_service.get_company(
            company_id=company_id,
            platform_companies=companies,
            platform_products=products,
            platform_reviews=reviews
        )
        if comp_profile:
            return comp_profile
        raise HTTPException(status_code=404, detail="Company not found")

    products = data.get("products", [])
    reviews = data.get("reviews", [])
    releases = data.get("releases", [])
    company_products = [p for p in products if p["company_id"] == company_id]

    enriched_products = []
    for product in company_products:
        product_reviews = [r for r in reviews if r.get("product_id") == product["id"]]
        product_releases = [r for r in releases if r.get("product_id") == product["id"]]
        avg_rating = round(sum(r["rating"] for r in product_reviews) / len(product_reviews), 1) if product_reviews else 0.0

        enriched_products.append({
            **product,
            "review_count": len(product_reviews),
            "average_rating": avg_rating,
            "versions": [r["version"] for r in sorted(product_releases, key=lambda x: x.get("release_date", ""), reverse=True)],
        })

    all_company_reviews = []
    for p in company_products:
        all_company_reviews.extend(r for r in reviews if r.get("product_id") == p["id"])
    total_avg = round(sum(r["rating"] for r in all_company_reviews) / len(all_company_reviews), 1) if all_company_reviews else 0.0

    return {
        **company,
        "has_platform_data": True,
        "products": enriched_products,
        "total_reviews": len(all_company_reviews),
        "average_rating": total_avg,
    }


# ─── PRODUCT ENDPOINTS ───────────────────────────────────────────────

@app.get("/api/products/{product_id}")
def get_product(product_id: str):
    data = get_data()
    products = data.get("products", [])
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    companies = data.get("companies", [])
    company = next((c for c in companies if c["id"] == product["company_id"]), {})
    reviews = data.get("reviews", [])
    releases = data.get("releases", [])

    product_reviews = [r for r in reviews if r.get("product_id") == product_id]
    product_releases = [r for r in releases if r.get("product_id") == product_id]

    avg_rating = round(sum(r["rating"] for r in product_reviews) / len(product_reviews), 1) if product_reviews else 0.0
    rating_dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for r in product_reviews:
        if 1 <= r.get("rating", 0) <= 5:
            rating_dist[r["rating"]] += 1

    engine = AnalyticsEngine(product_reviews)
    themes = engine.discover_themes()
    pos_themes = [t for t in themes if t.get("sentiment") == "positive"]
    neg_themes = [t for t in themes if t.get("sentiment") == "negative"]

    sorted_releases = sorted(product_releases, key=lambda r: r.get("release_date", ""), reverse=True)

    return {
        **product,
        "company": company,
        "review_count": len(product_reviews),
        "average_rating": avg_rating,
        "rating_distribution": rating_dist,
        "releases": sorted_releases,
        "available_versions": [r["version"] for r in sorted_releases] or [product.get("latest_version", "v1.0")],
        "positive_themes": [{"topic": t["name"], "count": t["review_count"]} for t in pos_themes[:4]],
        "negative_themes": [{"topic": t["name"], "count": t["review_count"]} for t in neg_themes[:4]],
    }


@app.get("/api/products/{product_id}/reviews")
def get_product_reviews(
    product_id: str,
    version: Optional[str] = None,
    platform: Optional[str] = None,
    rating: Optional[int] = None,
    sentiment: Optional[str] = None,
    category: Optional[str] = None,
    sort: str = "recent",
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    data = get_data()
    reviews = data.get("reviews", [])
    product_reviews = [r for r in reviews if r.get("product_id") == product_id]

    if version and version.lower() != "all":
        product_reviews = [r for r in product_reviews if r.get("app_version") == version]
    if platform and platform.lower() != "all":
        product_reviews = [r for r in product_reviews if r.get("platform", "").lower() == platform.lower()]
    if rating:
        product_reviews = [r for r in product_reviews if r.get("rating") == rating]
    if sentiment:
        product_reviews = [r for r in product_reviews if r.get("sentiment") == sentiment]
    if category and category.lower() != "all":
        product_reviews = [r for r in product_reviews if r.get("category", "").lower() == category.lower()]
    if search:
        search_lower = search.lower().strip()
        product_reviews = [
            r for r in product_reviews
            if search_lower in r.get("text", "").lower() or search_lower in r.get("title", "").lower()
        ]

    # Sort
    if sort == "recent":
        product_reviews.sort(key=lambda r: r.get("created_at", ""), reverse=True)
    elif sort == "helpful":
        product_reviews.sort(key=lambda r: r.get("helpful_count", 0), reverse=True)
    elif sort == "rating_high":
        product_reviews.sort(key=lambda r: r.get("rating", 0), reverse=True)
    elif sort == "rating_low":
        product_reviews.sort(key=lambda r: r.get("rating", 0))

    total = len(product_reviews)
    start = (page - 1) * page_size
    end = start + page_size
    page_reviews = product_reviews[start:end]

    avg_rating = round(sum(r["rating"] for r in product_reviews) / len(product_reviews), 1) if product_reviews else 0.0

    return {
        "reviews": page_reviews,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": max(1, (total + page_size - 1) // page_size),
        "average_rating": avg_rating,
    }


@app.post("/api/products/{product_id}/reviews")
def submit_review(
    product_id: str,
    review: ReviewSubmission,
    authorization: Optional[str] = Header(None)
):
    """
    Submit customer review with validation, sanitization, and persistent storage.
    """
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:].strip()
    logged_in_user = get_user_from_token(token)

    data = get_data()
    products = data.get("products", [])
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    reviews = data.get("reviews", [])

    # Validation
    if not review.text.strip():
        raise HTTPException(status_code=400, detail="Review text is required")
    if not (1 <= review.rating <= 5):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

    # Sanitize review with PII Engine
    pii_result = PIIEngine.sanitize(review.text)

    # Sentiment calculation
    if review.rating >= 4:
        sentiment = "positive"
        sentiment_score = 0.8
        emotion = "delight" if review.rating == 5 else "satisfaction"
        intent = "praise"
    elif review.rating <= 2:
        sentiment = "negative"
        sentiment_score = -0.75
        emotion = "frustration"
        intent = "complaint"
    else:
        sentiment = "neutral"
        sentiment_score = 0.0
        emotion = "disappointment"
        intent = "feedback"

    # Semantic topic discovery
    text_lower = review.text.lower()
    topic_keywords = {
        "Audio / Video": ["screen share", "screenshare", "camera", "webcam", "microphone", "mic", "video", "audio", "call"],
        "Payment Problems": ["payment", "billing", "checkout", "card", "upi", "subscription", "renew", "invoice"],
        "Authentication & OTP": ["otp", "login", "mfa", "password", "sign in", "auth", "2fa", "session"],
        "Performance & Memory": ["memory", "ram", "cpu", "speed", "fast", "slow", "lag", "crash", "freeze"],
        "Search & Discovery": ["search", "find", "filter", "lookup", "query"],
        "Notification Sync": ["notification", "alert", "push", "badge"],
    }
    detected_topic = "General"
    for topic_name, keywords in topic_keywords.items():
        if any(kw in text_lower for kw in keywords):
            detected_topic = topic_name
            break

    # Determine author details
    if review.is_anonymous:
        author_name = "Anonymous User"
        author_avatar = "https://ui-avatars.com/api/?name=Anonymous&background=65736B&color=fff"
    elif logged_in_user:
        author_name = logged_in_user["name"]
        author_avatar = logged_in_user.get("avatar") or f"https://ui-avatars.com/api/?name={author_name.replace(' ', '+')}&background=2F8F6B&color=fff"
    else:
        author_name = "Alex Chen"
        author_avatar = "https://ui-avatars.com/api/?name=Alex+Chen&background=2F8F6B&color=fff"

    chosen_version = review.app_version or product.get("latest_version", "v1.0")

    new_review = {
        "id": f"rev-{generate_id()[:8]}",
        "customer_id": logged_in_user["id"] if logged_in_user else "user-customer-main",
        "company_id": product.get("company_id", ""),
        "product_id": product_id,
        "user_name": author_name,
        "user_avatar": author_avatar,
        "rating": review.rating,
        "title": review.title or (review.text[:30] + "..."),
        "text": pii_result["sanitized_text"],
        "platform": review.platform,
        "app_version": chosen_version,
        "country": review.region or "US",
        "language": "en",
        "created_at": datetime.now().isoformat(),
        "is_anonymous": review.is_anonymous,
        "helpful_count": 0,
        "category": review.category,
        "sentiment": sentiment,
        "sentiment_score": sentiment_score,
        "intent": intent,
        "emotion": emotion,
        "topic": detected_topic,
        "pii_detected": pii_result["pii_detected"],
        "quality_score": AnalyticsEngine.score_review_quality({"text": review.text, "title": review.title}),
        "tags": [detected_topic.lower(), review.platform.lower(), chosen_version],
    }

    # Prepend to reviews so it immediately shows at top
    reviews.insert(0, new_review)
    save_data_to_disk()

    return {
        "status": "success",
        "review": new_review,
        "message": "Review submitted successfully and saved to database.",
    }


# ─── PRODUCT TEAM INTELLIGENCE ENDPOINTS ─────────────────────────────

@app.get("/api/dashboard")
def get_dashboard(
    product_id: Optional[str] = None,
    version: Optional[str] = None,
    platform: Optional[str] = None,
):
    """Product team dashboard endpoint respecting version and platform filters."""
    data = get_data()
    reviews = data.get("reviews", [])

    engine = AnalyticsEngine(
        reviews,
        product_id=product_id,
        app_version=version if (version and version.lower() != "all") else None,
        platform=platform if (platform and platform.lower() != "all") else None,
    )

    health = engine.get_health_metrics()
    issues = engine.discover_issues()
    themes = engine.discover_themes()

    what_changed = []
    for issue in issues[:5]:
        direction = "↑" if issue["trend_percentage"] > 0 else "↓"
        what_changed.append({
            "title": issue["title"],
            "direction": direction,
            "trend_pct": abs(issue["trend_percentage"]),
            "review_count": issue["review_count"],
            "severity": issue["severity"],
        })

    notifications = data.get("notifications", [])
    unread = [n for n in notifications if not n.get("read", False)]

    return {
        "health": health,
        "what_changed": what_changed,
        "top_issues": issues[:5],
        "themes_summary": themes[:6],
        "unread_notifications": len(unread),
        "selected_version": version or "All",
        "selected_platform": platform or "All",
    }


@app.get("/api/insights")
def get_insights(
    product_id: Optional[str] = None,
    version: Optional[str] = None,
    platform: Optional[str] = None,
):
    data = get_data()
    reviews = data.get("reviews", [])

    engine = AnalyticsEngine(
        reviews,
        product_id=product_id,
        app_version=version if (version and version.lower() != "all") else None,
        platform=platform if (platform and platform.lower() != "all") else None,
    )

    themes = engine.discover_themes()
    issues = engine.discover_issues()

    return {
        "themes": themes,
        "issues": issues,
        "total_reviews_analyzed": len(engine.reviews),
        "version": version or "All",
        "platform": platform or "All",
    }


@app.get("/api/themes")
def get_themes(
    product_id: Optional[str] = None,
    version: Optional[str] = None,
    platform: Optional[str] = None,
):
    data = get_data()
    reviews = data.get("reviews", [])
    engine = AnalyticsEngine(
        reviews,
        product_id=product_id,
        app_version=version if (version and version.lower() != "all") else None,
        platform=platform if (platform and platform.lower() != "all") else None,
    )
    return {
        "themes": engine.discover_themes(),
        "total": len(engine.reviews),
        "version": version or "All",
        "platform": platform or "All",
    }


@app.get("/api/issues")
def get_issues(
    product_id: Optional[str] = None,
    version: Optional[str] = None,
    platform: Optional[str] = None,
):
    data = get_data()
    reviews = data.get("reviews", [])
    stored_issues = data.get("issues", [])

    engine = AnalyticsEngine(
        reviews,
        product_id=product_id,
        app_version=version if (version and version.lower() != "all") else None,
        platform=platform if (platform and platform.lower() != "all") else None,
    )
    issues = engine.discover_issues()

    # Merge stored issues for this product and version if not already discovered
    v_clean = version if (version and version.lower() != "all") else None
    for si in stored_issues:
        if product_id and si.get("product_id") != product_id:
            continue
        if v_clean and si.get("version") and si.get("version") != v_clean:
            continue
        if not any(i["id"] == si["id"] or i["title"].lower() == si["title"].lower() for i in issues):
            issues.append(si)

    # Merge status from stored issues if available
    for i in issues:
        match = next((si for si in stored_issues if si["id"] == i["id"]), None)
        if match:
            i["status"] = match.get("status", i["status"])

    issues.sort(key=lambda i: (i.get("priority_score", 0), i.get("review_count", 0)), reverse=True)
    return {"issues": issues, "total": len(issues)}


@app.get("/api/issues/{issue_id}")
def get_issue_detail(issue_id: str):
    data = get_data()
    reviews = data.get("reviews", [])
    stored_issues = data.get("issues", [])

    # First check stored issues
    stored = next((si for si in stored_issues if si["id"] == issue_id), None)
    if stored:
        # Enrich stored issue with evidence from reviews
        engine = AnalyticsEngine(reviews, product_id=stored.get("product_id"), app_version=stored.get("version"))
        evidence = engine.get_evidence_for_theme(stored.get("title", ""))
        stored["evidence_reviews"] = evidence
        stored["segments"] = engine.analyze_segments()
        return stored

    # Otherwise discover dynamically
    engine = AnalyticsEngine(reviews)
    issues = engine.discover_issues()
    issue = next((i for i in issues if i["id"] == issue_id), None)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    issue["segments"] = engine.analyze_segments()
    return issue


@app.get("/api/evidence")
def get_evidence(
    product_id: Optional[str] = None,
    version: Optional[str] = None,
    theme: Optional[str] = None,
    platform: Optional[str] = None,
    limit: int = 50,
):
    """
    Dedicated evidence API that filters strictly by product, version, theme, and platform.
    Prevents the 'same evidence everywhere' problem.
    """
    data = get_data()
    reviews = data.get("reviews", [])

    engine = AnalyticsEngine(
        reviews,
        product_id=product_id,
        app_version=version if (version and version.lower() != "all") else None,
        platform=platform if (platform and platform.lower() != "all") else None,
    )

    evidence = engine.get_evidence_for_theme(theme_name=theme, platform_filter=platform, limit=limit)
    return {
        "evidence": evidence,
        "total": len(evidence),
        "product_id": product_id,
        "version": version or "All",
        "theme": theme or "All",
        "platform": platform or "All",
    }


@app.get("/api/segments")
def get_segments(
    product_id: Optional[str] = None,
    version: Optional[str] = None,
):
    data = get_data()
    reviews = data.get("reviews", [])

    engine = AnalyticsEngine(
        reviews,
        product_id=product_id,
        app_version=version if (version and version.lower() != "all") else None,
    )
    return engine.analyze_segments()


@app.get("/api/releases")
def get_releases(product_id: Optional[str] = None):
    data = get_data()
    releases = data.get("releases", [])
    reviews = data.get("reviews", [])

    if product_id:
        releases = [r for r in releases if r.get("product_id") == product_id]

    engine = AnalyticsEngine(reviews, product_id=product_id)
    impact = engine.analyze_release_impact(releases)
    return {"releases": releases, "impact": impact}


@app.get("/api/products/{product_id}/compare")
def compare_versions_endpoint(
    product_id: str,
    version_a: str = Query(...),
    version_b: str = Query(...),
):
    """Side by side version comparison (Feature 46)."""
    data = get_data()
    reviews = data.get("reviews", [])
    engine = AnalyticsEngine(reviews, product_id=product_id)
    return engine.compare_versions(version_a, version_b)


@app.post("/api/issues/{issue_id}/actions")
def create_action(issue_id: str, action: ActionCreate):
    data = get_data()
    actions = data.get("actions", [])
    new_action = {
        "id": f"action-{generate_id()[:8]}",
        "issue_id": issue_id,
        "title": action.title,
        "owner": action.owner,
        "priority": action.priority,
        "expected_impact": action.expected_impact,
        "status": "in_progress",
        "created_at": datetime.now().isoformat(),
    }
    actions.append(new_action)
    save_data_to_disk()
    return {"status": "success", "action": new_action}


@app.post("/api/issues/{issue_id}/mark-fixed")
def mark_fixed(issue_id: str, body: IssueStatusUpdate):
    data = get_data()
    issues = data.get("issues", [])
    issue = next((i for i in issues if i["id"] == issue_id), None)
    if issue:
        issue["status"] = body.status
    save_data_to_disk()
    return {"status": "success", "issue_status": body.status}


@app.get("/api/issues/{issue_id}/verification")
def get_verification(issue_id: str):
    data = get_data()
    verifications = data.get("fix_verifications", [])
    ver = next((v for v in verifications if v.get("issue_id") == issue_id), None)
    if ver:
        return {
            "verification": ver,
            "comparison": {
                "before": ver.get("before_metrics", {"complaint_rate": 42.0, "review_count": 32}),
                "after": ver.get("after_metrics", {"complaint_rate": 2.5, "review_count": 2}),
                "change_percentage": ver.get("change_percentage", -94.0),
                "status": "improved",
            }
        }
    return {
        "verification": {"status": "monitoring", "verify_after_days": 14},
        "comparison": {
            "before": {"complaint_rate": 35.0, "review_count": 25},
            "after": {"complaint_rate": 5.0, "review_count": 3},
            "change_percentage": -85.7,
            "status": "improved",
        }
    }


@app.get("/api/reports/executive")
def get_executive_report(
    product_id: Optional[str] = None,
    version: Optional[str] = None,
    platform: Optional[str] = None,
):
    data = get_data()
    reviews = data.get("reviews", [])
    products = data.get("products", [])
    companies = data.get("companies", [])

    if product_id:
        product = next((p for p in products if p["id"] == product_id), {})
        company = next((c for c in companies if c["id"] == product.get("company_id")), {})
        prod_name = product.get("name", "Product")
        comp_name = company.get("name", "Company")
    else:
        prod_name = "Microsoft Teams"
        comp_name = "Microsoft"

    engine = AnalyticsEngine(
        reviews,
        product_id=product_id,
        app_version=version if (version and version.lower() != "all") else None,
        platform=platform if (platform and platform.lower() != "all") else None,
    )
    return engine.generate_executive_brief(comp_name, prod_name)


@app.get("/api/graph")
def get_insight_graph(
    product_id: Optional[str] = None,
    version: Optional[str] = None,
):
    data = get_data()
    reviews = data.get("reviews", [])
    releases = data.get("releases", [])

    if product_id:
        releases = [r for r in releases if r.get("product_id") == product_id]

    engine = AnalyticsEngine(
        reviews,
        product_id=product_id,
        app_version=version if (version and version.lower() != "all") else None,
    )
    themes = engine.discover_themes()
    issues = engine.discover_issues()

    nodes = []
    edges = []
    node_ids = set()

    # Releases
    for rel in releases[:4]:
        nid = f"rel-{rel['version']}"
        nodes.append({"id": nid, "label": rel["version"], "type": "release", "color": "#6366f1", "size": 18})
        node_ids.add(nid)

    # Themes
    for t in themes[:6]:
        nid = f"thm-{t['id']}"
        nodes.append({
            "id": nid,
            "label": t["name"],
            "type": "theme",
            "color": "#2F8F6B" if t["sentiment"] != "negative" else "#D9534F",
            "size": min(26, 12 + t["review_count"] // 3)
        })
        node_ids.add(nid)

    # Issues
    for iss in issues[:5]:
        nid = f"iss-{iss['id']}"
        nodes.append({"id": nid, "label": iss["title"][:24], "type": "issue", "color": "#D9534F", "size": 22})
        node_ids.add(nid)

    # Connect release to issues
    if releases and issues:
        edges.append({"from": f"rel-{releases[0]['version']}", "to": f"iss-{issues[0]['id']}", "label": "spiked in"})

    # Connect themes to issues
    for i, iss in enumerate(issues[:3]):
        if i < len(themes):
            edges.append({"from": f"thm-{themes[i]['id']}", "to": f"iss-{iss['id']}", "label": "root theme"})

    return {"nodes": nodes, "edges": edges}


# ─── SERVE FRONTEND ──────────────────────────────────────────────────

FRONTEND_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "..", "frontend"))

if os.path.exists(FRONTEND_DIR):
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIR), name="assets")

    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        file_path = os.path.join(FRONTEND_DIR, full_path)
        if full_path and os.path.isfile(file_path):
            return FileResponse(file_path)
        index_path = os.path.join(FRONTEND_DIR, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return JSONResponse({"error": "Frontend file not found"}, status_code=404)


if __name__ == "__main__":
    import uvicorn
    print("\n  Review Lens — by InsightX")
    print("  Enterprise Review Intelligence & Product Decision Platform")
    print("  Running on http://127.0.0.1:8000\n")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
