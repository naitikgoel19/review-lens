# Review Lens — AI-Powered Customer Review Intelligence Platform

> **"Turn customer reviews into product decisions."**  
> *Read less. Understand more. Fix what matters.*  
> **Team:** InsightX | **Built for:** Microsoft Innovate 2026

---

## 1. Project Overview

**Review Lens** bridges the gap between public customer reviews and internal engineering decision-making. Rather than presenting generic sentiment scores or disconnected metrics, Review Lens provides:

1. **Consumer Experience (Customer View):**
   - Search across verified enterprise companies (Microsoft, Google, Adobe, NVIDIA, Apple, Amazon, and more).
   - Discover live products and active projects with transparent status tracking (`LIVE`, `BETA`, `MAINTENANCE`, `DEPRECATED`).
   - Read authentic customer feedback filtered by version, platform, and rating.
   - Submit rich, persistent reviews targeting specific versions with automatic PII sanitization.
   - Review personal feedback history via **My Reviews**.

2. **Enterprise Experience (Product Team View):**
   - **Version-Specific Telemetry:** Switching between product versions (e.g. `v5.3` vs `v5.2`) updates the entire intelligence suite—sentiment distributions, health metrics, discovered themes, friction points, and graphs.
   - **Evidence Mode:** Every insight and theme links directly to verbatim customer feedback filtered by version and platform, eliminating generic, duplicate evidence.
   - **Platform Breakdown:** Filter evidence and analytics across Android, iOS, Windows, and Web.
   - **Side-by-Side Version Comparison:** Directly compare releases (e.g. `v5.3` vs `v5.2`) to evaluate metric deltas.
   - **Closed-Loop Fix Verification:** Track pre-fix vs post-fix complaint rates with verified telemetry.
   - **Executive Briefs:** Generate deterministic leadership digests ready to copy to clipboard.

---

## 2. Architectural Blueprint

```text
                               ┌─────────────────────────┐
                               │   LOGIN GATEWAY (/login) │
                               └────────────┬────────────┘
                                            │
                    ┌───────────────────────┴───────────────────────┐
                    │                                               │
       [Company Member Tab]                                 [Customer Tab]
                    │                                               │
                    ▼                                               ▼
         PRODUCT TEAM WORKSPACE                              CUSTOMER VIEW
                    │                                               │
  ┌─────────────────┼─────────────────┐                             │
  │ Product Selector│ Version Selector│                             │
  └─────────────────┼─────────────────┘                             ▼
                    │                                        COMPANY SEARCH
        ┌───────────┼───────────┐                        (12 Verified Companies)
        │           │           │                                   │
     Overview    Reviews     Evidence                               ▼
   (Health &    (Version-    (Verbatim                         LIVE PRODUCTS
   Sentiment)   Filtered)    Reviews)                               │
        │           │           │                                   ▼
        └───────────┼───────────┘                            WRITE & PERSIST
                    │                                            REVIEW
                    ▼                                               │
          VERSION COMPARISON                                        │
           (v5.3 vs v5.2)                                           │
                    │                                               │
                    └───────────────────────┬───────────────────────┘
                                            │
                                            ▼
                                ┌───────────────────────┐
                                │ FASTAPI SERVICE LAYER │
                                └───────────┬───────────┘
                                            │
                                            ▼
                                ┌───────────────────────┐
                                │ PERSISTENT DATA LAYER │
                                │   (seed_data.json)    │
                                └───────────────────────┘
```

---

## 3. Technology Stack

- **Backend:** Python 3.13+, FastAPI, Uvicorn, Pydantic v2
- **Analytics & PII Engines:** Custom deterministic scoring engines (`AnalyticsEngine`, `PIIEngine`)
- **Frontend:** React 18, Tailwind CSS, Recharts 2.8, Lucide Icons, Inter font
- **Persistence:** Thread-safe JSON file storage (`data/seed_data.json`) with atomic write updates
- **Testing:** Automated integration test suite (`test_e2e.py`) verifying E2E scenarios A through L

---

## 4. Test Accounts & Authentication

The platform enforces **strict role separation**. There is **no role switching** inside the authenticated application. To switch experiences, users must sign out and choose their respective account type on the Login page.

| Account Type | Email | Password | Assigned Role | Default Experience |
| :--- | :--- | :--- | :--- | :--- |
| **Company Member** | `product@microsoft.com` | `Microsoft@123` | `COMPANY_MEMBER` | Microsoft Product Team Workspace |
| **Customer** | `customer@example.com` | `Customer@123` | `CUSTOMER` | Customer View (Search & Reviews) |
| **Demo Customer** | `demo@reviewlens.ai` | `demo123` | `CUSTOMER` | Customer View |
| **Demo Product Team**| `team@reviewlens.ai` | `team123` | `COMPANY_MEMBER` | Microsoft Product Team Workspace |

---

## 5. Environment Variables (`.env`)

Configure the environment variables in `.env` (or copy from `.env.example`):

```bash
APP_ENV=production
HOST=127.0.0.1
PORT=8000
DEBUG=false
SECRET_KEY=review-lens-secure-hmac-key-2026-prod
DATA_STORAGE_PATH=./data/seed_data.json

# Enterprise SSO / Entra ID Placeholder
AZURE_TENANT_ID=your-azure-tenant-id
AZURE_CLIENT_ID=your-azure-client-id
AZURE_CLIENT_SECRET=your-azure-client-secret

ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

---

## 6. How to Run the Application

### Prerequisites
- Python 3.10+ (tested on Python 3.13)
- Installed dependencies: `fastapi`, `uvicorn`, `pydantic`

### Step 1: Start the Server
From the project root:

```powershell
python backend/main.py
```
*The server will start at `http://127.0.0.1:8000`.*

### Step 2: Open in Browser
Open your browser and navigate to:
```text
http://127.0.0.1:8000
```

The application will immediately present the **Login Page**.

---

## 7. Automated E2E QA Test Suite

To verify all test scenarios (Tests A through L) automatically:

```powershell
python backend/test_e2e.py
```

### Verified Test Scenarios:
- **TEST A — Website Opening:** Unauthenticated access directs exclusively to the Login Page.
- **TEST B — Company Login:** Authenticating as `product@microsoft.com` launches Microsoft Product Team.
- **TEST C — Role Protection:** Customers attempting to log in via the Company Member tab are rejected (403 Forbidden). No role switching is permitted.
- **TEST D — Customer Login:** Authenticating as `customer@example.com` opens Customer View.
- **TEST E — Multi-Company Search:** Searching `Microsoft`, `Google`, `Adobe`, and `NVIDIA` returns verified profiles.
- **TEST F — Live Product Catalog:** Live products show verified statuses (`LIVE`, `MAINTENANCE`, `BETA`, etc.).
- **TEST G & H — Review Creation & Persistence:** Customer review on Teams `v5.3` is persisted to disk and displayed in **My Reviews**.
- **TEST I — Product Team Visibility:** The submitted review is immediately visible to Company Members inspecting Teams `v5.3`.
- **TEST J — Old Version Telemetry:** Switching to `v5.2` displays distinct telemetry (4.4 rating in v5.3 vs 1.3 in v5.2).
- **TEST K — Evidence Mode Correctness:** Selecting `Payment Problems` shows payment reviews; selecting `Authentication & OTP` shows auth reviews.
- **TEST L — Platform Filtering:** Selecting `Android` or `Web` filters evidence exclusively to matching device telemetry.

---

## 8. REST API Structure

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/auth/login` | Authenticate user with role verification |
| `GET` | `/api/auth/me` | Fetch active session profile |
| `GET` | `/api/customer/my-reviews` | Retrieve review history for logged-in customer |
| `GET` | `/api/companies` | List verified companies with aggregate ratings |
| `GET` | `/api/companies/search?q=...` | Case-insensitive multi-company search |
| `GET` | `/api/companies/{id}` | Detailed company profile with live products |
| `GET` | `/api/products/{id}` | Product details and rating distribution |
| `GET` | `/api/products/{id}/reviews` | Fetch reviews with version, platform, & rating filters |
| `POST`| `/api/products/{id}/reviews` | Submit and persist a new customer review |
| `GET` | `/api/dashboard` | Version-specific health metrics & sentiment |
| `GET` | `/api/insights` | Discovered themes and priority issues for version |
| `GET` | `/api/evidence` | Verbatim customer quotes for specific theme & platform |
| `GET` | `/api/products/{id}/compare` | Side-by-side release comparison (e.g. v5.3 vs v5.2) |
| `GET` | `/api/reports/executive` | Executive customer voice brief |
| `GET` | `/api/graph` | Insight relationship topology graph |

---

## 9. Production Deployment Considerations

1. **Database Migration:** For enterprise scale beyond millions of reviews, swap the file-backed JSON store with Azure Cosmos DB, Azure SQL, or PostgreSQL via SQLAlchemy or asyncpg. The repository methods in `main.py` are cleanly isolated.
2. **SSO Integration:** Replace `/api/auth/login` with Microsoft Entra ID (Azure AD) OAuth2 tokens using MSAL Python.
3. **Queue-Based Processing:** Move heavy sentiment and PII batch processing to background Celery / Azure Service Bus workers.
4. **CDN Caching:** Cache public company profiles and product metadata at edge CDN layers while serving real-time reviews dynamically.
