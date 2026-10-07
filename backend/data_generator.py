"""
Review Lens — Production-Grade Data Generator
Generates realistic, persistent multi-company review intelligence data.
Supports 12 realistic enterprise companies with active products, multiple versions,
semantically accurate reviews, themes, issues, and test accounts.
"""

import json
import random
import uuid
import datetime
from datetime import timedelta
import os

def generate_id():
    return str(uuid.uuid4())

def get_avatar(name):
    clean_name = name.replace(" ", "+")
    return f"https://ui-avatars.com/api/?name={clean_name}&background=2F8F6B&color=fff"

def get_date_in_range(days_ago_start, days_ago_end=0):
    now = datetime.datetime.now()
    start_date = now - timedelta(days=days_ago_start)
    end_date = now - timedelta(days=days_ago_end)
    diff = max(1, (end_date - start_date).days)
    random_days = random.randrange(diff)
    random_date = start_date + timedelta(days=random_days)
    return random_date.replace(
        hour=random.randint(0, 23),
        minute=random.randint(0, 59),
        second=random.randint(0, 59)
    ).isoformat()

def generate_all_data():
    random.seed(42)
    now = datetime.datetime.now()

    # ─────────────────────────────────────────────────────────────────
    # 1. COMPANIES (At least 12 realistic companies)
    # ─────────────────────────────────────────────────────────────────
    companies = [
        {
            "id": "c-microsoft",
            "name": "Microsoft",
            "description": "Global leader in software, cloud computing, enterprise platforms, and productivity services.",
            "industry": "Enterprise Software & Cloud",
            "website": "microsoft.com",
            "logo_url": get_avatar("Microsoft"),
            "verified": True,
            "created_at": (now - timedelta(days=730)).isoformat()
        },
        {
            "id": "c-google",
            "name": "Google",
            "description": "Multinational technology company specializing in internet-related services, cloud, and search.",
            "industry": "Internet & Cloud Services",
            "website": "google.com",
            "logo_url": get_avatar("Google"),
            "verified": True,
            "created_at": (now - timedelta(days=730)).isoformat()
        },
        {
            "id": "c-adobe",
            "name": "Adobe",
            "description": "Leader in digital media creativity tools, document management, and digital marketing software.",
            "industry": "Creative & Document Software",
            "website": "adobe.com",
            "logo_url": get_avatar("Adobe"),
            "verified": True,
            "created_at": (now - timedelta(days=730)).isoformat()
        },
        {
            "id": "c-nvidia",
            "name": "NVIDIA",
            "description": "Pioneer in accelerated computing, GPU hardware, AI platforms, and interactive digital graphics.",
            "industry": "Semiconductors & AI Platforms",
            "website": "nvidia.com",
            "logo_url": get_avatar("NVIDIA"),
            "verified": True,
            "created_at": (now - timedelta(days=730)).isoformat()
        },
        {
            "id": "c-apple",
            "name": "Apple",
            "description": "Designer and manufacturer of consumer electronics, operating systems, and subscription cloud services.",
            "industry": "Consumer Tech & Operating Systems",
            "website": "apple.com",
            "logo_url": get_avatar("Apple"),
            "verified": True,
            "created_at": (now - timedelta(days=730)).isoformat()
        },
        {
            "id": "c-amazon",
            "name": "Amazon",
            "description": "Global cloud computing powerhouse (AWS), e-commerce platform, and digital streaming provider.",
            "industry": "Cloud Computing & Services",
            "website": "amazon.com",
            "logo_url": get_avatar("Amazon"),
            "verified": True,
            "created_at": (now - timedelta(days=730)).isoformat()
        },
        {
            "id": "c-spotify",
            "name": "Spotify",
            "description": "Audio streaming and media services provider connecting creators with millions of listeners globally.",
            "industry": "Audio & Media Streaming",
            "website": "spotify.com",
            "logo_url": get_avatar("Spotify"),
            "verified": True,
            "created_at": (now - timedelta(days=730)).isoformat()
        },
        {
            "id": "c-netflix",
            "name": "Netflix",
            "description": "Entertainment subscription streaming service offering films, television series, and games.",
            "industry": "Entertainment Streaming",
            "website": "netflix.com",
            "logo_url": get_avatar("Netflix"),
            "verified": True,
            "created_at": (now - timedelta(days=730)).isoformat()
        },
        {
            "id": "c-notion",
            "name": "Notion",
            "description": "All-in-one connected workspace for notes, project management, wikis, and team collaboration.",
            "industry": "Productivity & Collaboration",
            "website": "notion.so",
            "logo_url": get_avatar("Notion"),
            "verified": True,
            "created_at": (now - timedelta(days=730)).isoformat()
        },
        {
            "id": "c-phonepe",
            "name": "PhonePe",
            "description": "India's leading digital payments and financial technology platform processing billions of UPI transactions.",
            "industry": "Fintech & Payments",
            "website": "phonepe.com",
            "logo_url": get_avatar("PhonePe"),
            "verified": True,
            "created_at": (now - timedelta(days=730)).isoformat()
        },
        {
            "id": "c-zomato",
            "name": "Zomato",
            "description": "Food delivery, restaurant discovery, and quick commerce platform connecting millions of foodies.",
            "industry": "Food Tech & Logistics",
            "website": "zomato.com",
            "logo_url": get_avatar("Zomato"),
            "verified": True,
            "created_at": (now - timedelta(days=730)).isoformat()
        },
        {
            "id": "c-swiggy",
            "name": "Swiggy",
            "description": "Leading on-demand convenience platform offering food delivery, grocery instamart, and dining services.",
            "industry": "On-demand Food & Quick Commerce",
            "website": "swiggy.com",
            "logo_url": get_avatar("Swiggy"),
            "verified": True,
            "created_at": (now - timedelta(days=730)).isoformat()
        }
    ]

    # ─────────────────────────────────────────────────────────────────
    # 2. PRODUCTS & RELEASES DEFINITIONS
    # With realistic statuses: LIVE, BETA, MAINTENANCE, DEPRECATED, ARCHIVED
    # ─────────────────────────────────────────────────────────────────
    products_catalog = [
        # Microsoft
        {
            "company_id": "c-microsoft",
            "id": "p-microsoft-teams",
            "name": "Microsoft Teams",
            "description": "Enterprise workspace for real-time video meetings, voice calls, persistent chat, and collaboration.",
            "category": "Collaboration & Communication",
            "status": "LIVE",
            "versions": [
                {"version": "v5.3", "label": "v5.3 (Current)", "days_ago": 10, "changelog": "Performance enhancements, smoother screen sharing, and optimized memory footprint."},
                {"version": "v5.2", "label": "v5.2 (Previous)", "days_ago": 35, "changelog": "New billing management portal, upgraded authentication protocols, and notifications sync."},
                {"version": "v5.1", "label": "v5.1 (Previous)", "days_ago": 65, "changelog": "Enhanced audio routing, meeting breakout rooms, and OneDrive file picker redesign."},
                {"version": "v5.0", "label": "v5.0 (Archived)", "days_ago": 110, "changelog": "Major architecture migration to WebView2 client runtime."}
            ]
        },
        {
            "company_id": "c-microsoft",
            "id": "p-microsoft-365",
            "name": "Microsoft 365",
            "description": "Integrated cloud-powered productivity suite featuring Word, Excel, PowerPoint, and Exchange.",
            "category": "Office Productivity",
            "status": "LIVE",
            "versions": [
                {"version": "v16.88", "label": "v16.88 (Current)", "days_ago": 15, "changelog": "Copilot integration and spreadsheet calculation performance boost."},
                {"version": "v16.87", "label": "v16.87 (Previous)", "days_ago": 45, "changelog": "Document autosave reliability fixes."},
                {"version": "v16.86", "label": "v16.86 (Previous)", "days_ago": 80, "changelog": "Dark mode support for document canvas."}
            ]
        },
        {
            "company_id": "c-microsoft",
            "id": "p-microsoft-copilot",
            "name": "Microsoft Copilot",
            "description": "Generative AI assistant embedded across Windows, web, and enterprise workflows.",
            "category": "Artificial Intelligence",
            "status": "LIVE",
            "versions": [
                {"version": "v2.4", "label": "v2.4 (Current)", "days_ago": 8, "changelog": "GPT-4o model integration and faster web grounded searches."},
                {"version": "v2.3", "label": "v2.3 (Previous)", "days_ago": 38, "changelog": "Enterprise data protection controls and citations formatting."},
                {"version": "v2.2", "label": "v2.2 (Previous)", "days_ago": 70, "changelog": "Image generation and file upload support."}
            ]
        },
        {
            "company_id": "c-microsoft",
            "id": "p-microsoft-onedrive",
            "name": "OneDrive",
            "description": "Secure enterprise cloud storage, real-time file synchronization, and backup solution.",
            "category": "Cloud Storage",
            "status": "LIVE",
            "versions": [
                {"version": "v24.1", "label": "v24.1 (Current)", "days_ago": 12, "changelog": "Selective sync performance improvements and offline access cache fixes."},
                {"version": "v24.0", "label": "v24.0 (Previous)", "days_ago": 42, "changelog": "New visual photo gallery and shared links management."}
            ]
        },
        {
            "company_id": "c-microsoft",
            "id": "p-microsoft-edge",
            "name": "Microsoft Edge",
            "description": "Fast, secure web browser with built-in productivity tools, vertical tabs, and AI assistance.",
            "category": "Web Browser",
            "status": "LIVE",
            "versions": [
                {"version": "v128.0", "label": "v128.0 (Current)", "days_ago": 14, "changelog": "Chromium 128 upgrade, sleeping tabs memory reduction."},
                {"version": "v127.0", "label": "v127.0 (Previous)", "days_ago": 44, "changelog": "Enhanced PDF viewer markup tools."}
            ]
        },
        {
            "company_id": "c-microsoft",
            "id": "p-microsoft-azure",
            "name": "Azure",
            "description": "Comprehensive cloud computing platform offering over 200 products and cloud services.",
            "category": "Cloud Computing",
            "status": "LIVE",
            "versions": [
                {"version": "v4.2", "label": "v4.2 (Current)", "days_ago": 20, "changelog": "Azure Resource Graph speedups and mobile portal improvements."},
                {"version": "v4.1", "label": "v4.1 (Previous)", "days_ago": 55, "changelog": "Cost analysis forecast widgets."}
            ]
        },
        {
            "company_id": "c-microsoft",
            "id": "p-microsoft-visual-studio",
            "name": "Visual Studio",
            "description": "Rich integrated development environment (IDE) for building mission-critical software.",
            "category": "Developer Tools",
            "status": "LIVE",
            "versions": [
                {"version": "v17.10", "label": "v17.10 (Current)", "days_ago": 25, "changelog": "C++ standard library speedups and git repository manager improvements."},
                {"version": "v17.9", "label": "v17.9 (Previous)", "days_ago": 75, "changelog": "Generated breakpoint debugging upgrades."}
            ]
        },
        {
            "company_id": "c-microsoft",
            "id": "p-microsoft-outlook",
            "name": "Outlook",
            "description": "Enterprise email, calendaring, and contact management platform.",
            "category": "Email & Calendar",
            "status": "MAINTENANCE",
            "versions": [
                {"version": "v16.89", "label": "v16.89 (Current)", "days_ago": 30, "changelog": "Security updates and calendar invite sync patches."}
            ]
        },

        # Google
        {
            "company_id": "c-google",
            "id": "p-google-chrome",
            "name": "Google Chrome",
            "description": "Fast, simple, and secure web browser built for the modern web.",
            "category": "Web Browser",
            "status": "LIVE",
            "versions": [
                {"version": "v128.0", "label": "v128.0 (Current)", "days_ago": 10, "changelog": "Tab group synchronization and safety check enhancements."},
                {"version": "v127.0", "label": "v127.0 (Previous)", "days_ago": 40, "changelog": "Memory saver mode optimizations."}
            ]
        },
        {
            "company_id": "c-google",
            "id": "p-google-meet",
            "name": "Google Meet",
            "description": "High-quality video calling for teams, classrooms, and family gatherings.",
            "category": "Video Conferencing",
            "status": "LIVE",
            "versions": [
                {"version": "v2024.08", "label": "v2024.08 (Current)", "days_ago": 15, "changelog": "Low-light video enhancement and noise cancellation upgrades."},
                {"version": "v2024.07", "label": "v2024.07 (Previous)", "days_ago": 45, "changelog": "Companion mode companion screen sharing."}
            ]
        },
        {
            "company_id": "c-google",
            "id": "p-google-workspace",
            "name": "Google Workspace",
            "description": "Cloud-native productivity and collaboration tools including Docs, Sheets, Drive, and Gmail.",
            "category": "Productivity Suite",
            "status": "LIVE",
            "versions": [
                {"version": "v2024.3", "label": "v2024.3 (Current)", "days_ago": 18, "changelog": "Gemini in Docs side panel integration."},
                {"version": "v2024.2", "label": "v2024.2 (Previous)", "days_ago": 50, "changelog": "Sheets formula suggestions accelerator."}
            ]
        },
        {
            "company_id": "c-google",
            "id": "p-google-cloud",
            "name": "Google Cloud Platform",
            "description": "Suite of modular cloud services including computing, data storage, analytics, and machine learning.",
            "category": "Cloud Infrastructure",
            "status": "LIVE",
            "versions": [
                {"version": "v4.8", "label": "v4.8 (Current)", "days_ago": 22, "changelog": "BigQuery Studio UI improvements and Cloud Run deployment dashboard."},
                {"version": "v4.7", "label": "v4.7 (Previous)", "days_ago": 60, "changelog": "IAM recommender notifications."}
            ]
        },

        # Adobe
        {
            "company_id": "c-adobe",
            "id": "p-adobe-photoshop",
            "name": "Photoshop",
            "description": "Industry standard image editing, photo retouching, and digital painting software.",
            "category": "Digital Art & Photo Editing",
            "status": "LIVE",
            "versions": [
                {"version": "v25.11", "label": "v25.11 (Current)", "days_ago": 12, "changelog": "Generative Fill powered by Firefly 3, selection brush tool."},
                {"version": "v25.10", "label": "v25.10 (Previous)", "days_ago": 48, "changelog": "Adjustment brush tool and font browser refresh."}
            ]
        },
        {
            "company_id": "c-adobe",
            "id": "p-adobe-acrobat",
            "name": "Acrobat Reader",
            "description": "The trusted global standard for viewing, printing, signing, and annotating PDFs.",
            "category": "Document Management",
            "status": "LIVE",
            "versions": [
                {"version": "v24.002", "label": "v24.002 (Current)", "days_ago": 16, "changelog": "Acrobat AI Assistant document summary enhancements."},
                {"version": "v24.001", "label": "v24.001 (Previous)", "days_ago": 52, "changelog": "Electronic signatures audit log viewer."}
            ]
        },
        {
            "company_id": "c-adobe",
            "id": "p-adobe-premiere",
            "name": "Premiere Pro",
            "description": "Professional non-linear video editing software for film, TV, and web creators.",
            "category": "Video Editing",
            "status": "LIVE",
            "versions": [
                {"version": "v24.5", "label": "v24.5 (Current)", "days_ago": 20, "changelog": "Text-based video editing updates and color management workflow."},
                {"version": "v24.4", "label": "v24.4 (Previous)", "days_ago": 60, "changelog": "Hardware acceleration for ProRes RAW export."}
            ]
        },
        {
            "company_id": "c-adobe",
            "id": "p-adobe-illustrator",
            "name": "Illustrator",
            "description": "Vector graphics software used for logos, icons, drawings, typography, and illustrations.",
            "category": "Vector Graphics",
            "status": "LIVE",
            "versions": [
                {"version": "v28.6", "label": "v28.6 (Current)", "days_ago": 25, "changelog": "Generative Shape Fill and enhanced dimension tool."}
            ]
        },

        # NVIDIA
        {
            "company_id": "c-nvidia",
            "id": "p-nvidia-app",
            "name": "NVIDIA App",
            "description": "Essential companion for PC gamers and creators with unified GPU control center.",
            "category": "Gaming & Utilities",
            "status": "LIVE",
            "versions": [
                {"version": "v11.0.1", "label": "v11.0.1 (Current)", "days_ago": 15, "changelog": "GeForce Game Ready driver quick update and AV1 120 FPS recording."},
                {"version": "v11.0.0", "label": "v11.0.0 (Previous)", "days_ago": 55, "changelog": "Unified redesigned overlay and RTX HDR filter."}
            ]
        },
        {
            "company_id": "c-nvidia",
            "id": "p-nvidia-geforce-now",
            "name": "GeForce NOW",
            "description": "Cloud gaming service transforming ordinary hardware into high-performance GeForce RTX gaming rigs.",
            "category": "Cloud Gaming",
            "status": "LIVE",
            "versions": [
                {"version": "v2.0.65", "label": "v2.0.65 (Current)", "days_ago": 18, "changelog": "4K 120 FPS streaming stability improvements and game pass account sync."},
                {"version": "v2.0.64", "label": "v2.0.64 (Previous)", "days_ago": 58, "changelog": "Ultra-low latency reflex mode."}
            ]
        },
        {
            "company_id": "c-nvidia",
            "id": "p-nvidia-omniverse",
            "name": "Omniverse",
            "description": "Modular platform for building and operating OpenUSD-based 3D applications and industrial digital twins.",
            "category": "3D Simulation & AI",
            "status": "BETA",
            "versions": [
                {"version": "v2024.1", "label": "v2024.1 (Current)", "days_ago": 30, "changelog": "USD Composer physics engine updates and RTX real-time ray tracing."}
            ]
        },

        # Spotify
        {
            "company_id": "c-spotify",
            "id": "p-spotify-spotify-music",
            "name": "Spotify Music",
            "description": "Digital music streaming service with access to millions of songs and curated playlists.",
            "category": "Music Streaming",
            "status": "LIVE",
            "versions": [
                {"version": "v8.9.60", "label": "v8.9.60 (Current)", "days_ago": 10, "changelog": "Lossless audio preview and AI DJ voice enhancements."},
                {"version": "v8.9.50", "label": "v8.9.50 (Previous)", "days_ago": 40, "changelog": "Queue management redesign."}
            ]
        },

        # Netflix
        {
            "company_id": "c-netflix",
            "id": "p-netflix-streaming",
            "name": "Netflix Streaming",
            "description": "Watch TV shows, movies, documentaries, and award-winning Netflix originals.",
            "category": "Video Streaming",
            "status": "LIVE",
            "versions": [
                {"version": "v9.42", "label": "v9.42 (Current)", "days_ago": 12, "changelog": "Spatial audio expanded library and my-list category filters."},
                {"version": "v9.41", "label": "v9.41 (Previous)", "days_ago": 45, "changelog": "Downloads for you optimization."}
            ]
        },

        # Notion
        {
            "company_id": "c-notion",
            "id": "p-notion-workspace",
            "name": "Notion Workspace",
            "description": "Connected workspace where better, faster work happens with docs, projects, and wikis.",
            "category": "Productivity",
            "status": "LIVE",
            "versions": [
                {"version": "v2.44", "label": "v2.44 (Current)", "days_ago": 14, "changelog": "Notion AI automated database autofill and formula 2.0 upgrades."},
                {"version": "v2.43", "label": "v2.43 (Previous)", "days_ago": 49, "changelog": "Calendar two-way sync."}
            ]
        },

        # PhonePe
        {
            "company_id": "c-phonepe",
            "id": "p-phonepe-payments",
            "name": "PhonePe Payments",
            "description": "Instant UPI money transfer, bill recharges, merchant QR payments, and digital wallets.",
            "category": "Fintech & Payments",
            "status": "LIVE",
            "versions": [
                {"version": "v5.6.2", "label": "v5.6.2 (Current)", "days_ago": 8, "changelog": "UPI Lite automatic recharge and biometric transaction approval."},
                {"version": "v5.6.1", "label": "v5.6.1 (Previous)", "days_ago": 36, "changelog": "Credit on UPI integration and transaction receipt sharing."}
            ]
        },

        # Zomato
        {
            "company_id": "c-zomato",
            "id": "p-zomato-food-delivery",
            "name": "Zomato Food Delivery",
            "description": "Discover top restaurants, track live food delivery, and enjoy delicious dining deals.",
            "category": "Food Delivery",
            "status": "LIVE",
            "versions": [
                {"version": "v17.4", "label": "v17.4 (Current)", "days_ago": 11, "changelog": "Live GPS delivery partner tracking and multi-restaurant cart."},
                {"version": "v17.3", "label": "v17.3 (Previous)", "days_ago": 42, "changelog": "Veg mode toggle and dietary allergy warnings."}
            ]
        },

        # Swiggy
        {
            "company_id": "c-swiggy",
            "id": "p-swiggy-food",
            "name": "Swiggy Food",
            "description": "Order food from your favorite local restaurants with lightning-fast doorstep delivery.",
            "category": "Food Delivery",
            "status": "LIVE",
            "versions": [
                {"version": "v14.2", "label": "v14.2 (Current)", "days_ago": 9, "changelog": "Swiggy One membership benefits integration and Bolt 10-minute delivery."},
                {"version": "v14.1", "label": "v14.1 (Previous)", "days_ago": 39, "changelog": "Group ordering with split bill."}
            ]
        }
    ]

    # Build products list and releases list
    products = []
    releases = []
    product_dict = {}

    for pdef in products_catalog:
        pid = pdef["id"]
        latest_ver = pdef["versions"][0]["version"]
        product_obj = {
            "id": pid,
            "company_id": pdef["company_id"],
            "name": pdef["name"],
            "description": pdef["description"],
            "category": pdef["category"],
            "status": pdef["status"],
            "latest_version": latest_ver,
            "last_updated": (now - timedelta(days=pdef["versions"][0]["days_ago"])).isoformat(),
            "logo_url": get_avatar(pdef["name"])
        }
        products.append(product_obj)
        product_dict[pid] = product_obj

        for vdef in pdef["versions"]:
            rel_date = (now - timedelta(days=vdef["days_ago"])).isoformat()
            release_obj = {
                "id": generate_id(),
                "product_id": pid,
                "version": vdef["version"],
                "release_date": rel_date,
                "label": vdef["label"],
                "changelog": vdef["changelog"]
            }
            releases.append(release_obj)

    # ─────────────────────────────────────────────────────────────────
    # 3. TEST USERS
    # Including mandatory:
    # product@microsoft.com / Microsoft@123 (COMPANY_MEMBER for Microsoft)
    # customer@example.com / Customer@123 (CUSTOMER)
    # ─────────────────────────────────────────────────────────────────
    users = [
        # Microsoft Accounts
        {
            "id": "user-msft-product",
            "email": "product@microsoft.com",
            "password": "Microsoft@123",
            "name": "Microsoft Product Team",
            "role": "COMPANY_MEMBER",
            "company_id": "c-microsoft",
            "company_name": "Microsoft",
            "avatar": get_avatar("Microsoft Team"),
            "created_at": (now - timedelta(days=365)).isoformat()
        },
        {
            "id": "user-msft-sarah",
            "email": "sarah.chen@microsoft.com",
            "password": "Teams@2026",
            "name": "Sarah Chen",
            "role": "COMPANY_MEMBER",
            "company_id": "c-microsoft",
            "company_name": "Microsoft",
            "avatar": get_avatar("Sarah Chen"),
            "created_at": (now - timedelta(days=300)).isoformat()
        },
        {
            "id": "user-msft-marcus",
            "email": "marcus.vance@microsoft.com",
            "password": "Marcus@2026",
            "name": "Marcus Vance",
            "role": "COMPANY_MEMBER",
            "company_id": "c-microsoft",
            "company_name": "Microsoft",
            "avatar": get_avatar("Marcus Vance"),
            "created_at": (now - timedelta(days=250)).isoformat()
        },
        # Google Account
        {
            "id": "user-google-david",
            "email": "david.kim@google.com",
            "password": "Google@123",
            "name": "David Kim",
            "role": "COMPANY_MEMBER",
            "company_id": "c-google",
            "company_name": "Google",
            "avatar": get_avatar("David Kim"),
            "created_at": (now - timedelta(days=280)).isoformat()
        },
        # Adobe Account
        {
            "id": "user-adobe-elena",
            "email": "elena.rostova@adobe.com",
            "password": "Adobe@123",
            "name": "Elena Rostova",
            "role": "COMPANY_MEMBER",
            "company_id": "c-adobe",
            "company_name": "Adobe",
            "avatar": get_avatar("Elena Rostova"),
            "created_at": (now - timedelta(days=240)).isoformat()
        },
        # NVIDIA Account
        {
            "id": "user-nvidia-jensen",
            "email": "jensen.huang@nvidia.com",
            "password": "Nvidia@123",
            "name": "Jensen Huang",
            "role": "COMPANY_MEMBER",
            "company_id": "c-nvidia",
            "company_name": "NVIDIA",
            "avatar": get_avatar("Jensen Huang"),
            "created_at": (now - timedelta(days=320)).isoformat()
        },
        # Amazon Account
        {
            "id": "user-amazon-andy",
            "email": "andy.jassy@amazon.com",
            "password": "Amazon@123",
            "name": "Andy Jassy",
            "role": "COMPANY_MEMBER",
            "company_id": "c-amazon",
            "company_name": "Amazon",
            "avatar": get_avatar("Andy Jassy"),
            "created_at": (now - timedelta(days=310)).isoformat()
        },
        # Customer Accounts
        {
            "id": "user-customer-main",
            "email": "customer@example.com",
            "password": "Customer@123",
            "name": "Alex Chen",
            "role": "CUSTOMER",
            "avatar": get_avatar("Alex Chen"),
            "created_at": (now - timedelta(days=180)).isoformat()
        },
        {
            "id": "user-customer-priya",
            "email": "priya.patel@example.com",
            "password": "Priya@123",
            "name": "Priya Patel",
            "role": "CUSTOMER",
            "avatar": get_avatar("Priya Patel"),
            "created_at": (now - timedelta(days=120)).isoformat()
        },
        {
            "id": "user-customer-jordan",
            "email": "jordan.lee@example.com",
            "password": "Jordan@123",
            "name": "Jordan Lee",
            "role": "CUSTOMER",
            "avatar": get_avatar("Jordan Lee"),
            "created_at": (now - timedelta(days=90)).isoformat()
        },
        {
            "id": "user-demo-customer",
            "email": "demo@reviewlens.ai",
            "password": "demo123",
            "name": "Alex Chen",
            "role": "CUSTOMER",
            "avatar": get_avatar("Alex Chen"),
            "created_at": (now - timedelta(days=180)).isoformat()
        },
        {
            "id": "user-demo-team",
            "email": "team@reviewlens.ai",
            "password": "team123",
            "name": "Sarah Johnson",
            "role": "COMPANY_MEMBER",
            "company_id": "c-microsoft",
            "company_name": "Microsoft",
            "avatar": get_avatar("Sarah Johnson"),
            "created_at": (now - timedelta(days=200)).isoformat()
        }
    ]

    # ─────────────────────────────────────────────────────────────────
    # 4. REVIEW SEEDING WITH SPECIFIC VERSION THEMES
    # ─────────────────────────────────────────────────────────────────
    platforms = ["Android", "iOS", "Windows", "Web"]
    regions = ["US", "IN", "EU", "UK", "CA"]
    names_pool = [
        "David Miller", "Sarah Jenkins", "Michael Chang", "Emily Watson",
        "Rahul Sharma", "Priya Nair", "Amit Patel", "Neha Gupta",
        "Vikram Reddy", "Sneha Joshi", "Marcus Vance", "Elena Rostova",
        "James O'Connor", "Aisha Khan", "Carlos Gomez", "Chloe Martin"
    ]

    reviews = []

    # Curated version-specific review recipes for Microsoft Teams
    # v5.3: Balanced release — solid audio/video and search, but contains real negative feedback
    v53_recipes = [
        # Audio / Video (Positive)
        {"text": "Screen sharing is much smoother now! Zero lag during our 40-person department all-hands call.", "rating": 5, "platform": "Web", "theme": "Audio / Video", "sentiment": "positive"},
        {"text": "Webcam quality and video rendering feels significantly crisper compared to the previous release.", "rating": 5, "platform": "Windows", "theme": "Audio / Video", "sentiment": "positive"},
        {"text": "Audio echo cancellation works brilliantly even without wearing my headset.", "rating": 4, "platform": "Web", "theme": "Audio / Video", "sentiment": "positive"},
        {"text": "Screen share frame rate is great on Android tablet during client presentations.", "rating": 5, "platform": "Android", "theme": "Audio / Video", "sentiment": "positive"},
        {"text": "Video call connects in under two seconds. Solid improvement on iOS.", "rating": 5, "platform": "iOS", "theme": "Audio / Video", "sentiment": "positive"},
        # Search & Discovery (Positive)
        {"text": "Search across channels and direct messages is lightning fast. Found old files instantly.", "rating": 5, "platform": "Web", "theme": "Search & Discovery", "sentiment": "positive"},
        {"text": "The new message filter in search results saved me hours looking for quarterly sprint notes.", "rating": 4, "platform": "Windows", "theme": "Search & Discovery", "sentiment": "positive"},
        {"text": "Channel search autocomplete works reliably on Android mobile now.", "rating": 4, "platform": "Android", "theme": "Search & Discovery", "sentiment": "positive"},
        # Performance & Memory (Positive)
        {"text": "Memory usage dropped from 2.4 GB down to 700 MB on Windows. Massive improvement!", "rating": 5, "platform": "Windows", "theme": "Performance & Memory", "sentiment": "positive"},
        {"text": "The new client launches in 2 seconds flat. Laptop fans don't sound like jet engines anymore.", "rating": 5, "platform": "Web", "theme": "Performance & Memory", "sentiment": "positive"},
        # Meaningful Negative & Neutral reviews in v5.3 (Essential for realistic analytics & Issues detection)
        {"text": "Notifications are delayed on Android lockscreen by several minutes in power-saving mode.", "rating": 2, "platform": "Android", "theme": "Notification Sync", "sentiment": "negative"},
        {"text": "Push notifications sometimes show up 30 seconds late on Android, causing missed call alerts.", "rating": 1, "platform": "Android", "theme": "Notification Sync", "sentiment": "negative"},
        {"text": "Badges for unread messages do not clear until app is manually killed on Android.", "rating": 2, "platform": "Android", "theme": "Notification Sync", "sentiment": "negative"},
        {"text": "Client window becomes blurry when dragged between 4K monitor and laptop display on Windows 11.", "rating": 2, "platform": "Windows", "theme": "Display Scaling", "sentiment": "negative"},
        {"text": "High DPI scaling causes tiny font in chat input box on secondary monitor.", "rating": 2, "platform": "Windows", "theme": "Display Scaling", "sentiment": "negative"},
        {"text": "Calendar meeting invites from external Outlook contacts take 10 minutes to sync on Web.", "rating": 2, "platform": "Web", "theme": "Calendar Sync", "sentiment": "negative"},
        {"text": "Shared calendar widget occasionally spins indefinitely on Safari browser.", "rating": 3, "platform": "Web", "theme": "Calendar Sync", "sentiment": "neutral"},
        {"text": "Microphone input gain resets to 50% automatically after each meeting.", "rating": 3, "platform": "Windows", "theme": "Audio / Video", "sentiment": "neutral"},
        {"text": "Emoji reaction picker opens with a slight 1-second pause on iOS.", "rating": 3, "platform": "iOS", "theme": "UI / Usability", "sentiment": "neutral"},
        {"text": "Meeting transcription is mostly accurate, though struggles with technical jargon.", "rating": 3, "platform": "Web", "theme": "Audio / Video", "sentiment": "neutral"}
    ]

    # v5.2: Plagued with Payment Problems, Authentication & OTP failures, Mobile Battery drain
    v52_recipes = [
        # Payment Problems (Severe Negative)
        {"text": "Payment checkout timed out when renewing our Teams Essentials workspace subscription.", "rating": 1, "platform": "Web", "theme": "Payment Problems", "sentiment": "negative"},
        {"text": "Credit card was charged twice but billing portal still says license payment failed.", "rating": 1, "platform": "Web", "theme": "Payment Problems", "sentiment": "negative"},
        {"text": "UPI payment gateway keeps returning gateway error 504 on business invoice renewal.", "rating": 1, "platform": "Android", "theme": "Payment Problems", "sentiment": "negative"},
        {"text": "Cannot add corporate credit card; form throws generic validation error without explanation.", "rating": 2, "platform": "Windows", "theme": "Payment Problems", "sentiment": "negative"},
        {"text": "Monthly subscription payment failed and locked out 12 of our team members on Monday morning.", "rating": 1, "platform": "Web", "theme": "Payment Problems", "sentiment": "negative"},
        {"text": "Subscription billing page freezes completely during invoice download on iOS.", "rating": 2, "platform": "iOS", "theme": "Payment Problems", "sentiment": "negative"},
        {"text": "Invoice PDF export generated blank rows for taxes.", "rating": 3, "platform": "Web", "theme": "Payment Problems", "sentiment": "neutral"},
        # Authentication & OTP (Severe Negative)
        {"text": "Endless login loop: keeps redirecting between Microsoft login and MFA prompt.", "rating": 1, "platform": "Web", "theme": "Authentication & OTP", "sentiment": "negative"},
        {"text": "OTP verification SMS takes over 15 minutes to arrive, by which time the session token expired.", "rating": 1, "platform": "Android", "theme": "Authentication & OTP", "sentiment": "negative"},
        {"text": "Authenticator push approval doesn't register on iOS; forced to enter password 4 times.", "rating": 1, "platform": "iOS", "theme": "Authentication & OTP", "sentiment": "negative"},
        {"text": "Session expired error appears every morning, requiring full 2FA credentials re-entry.", "rating": 2, "platform": "Windows", "theme": "Authentication & OTP", "sentiment": "negative"},
        {"text": "Single Sign-On (SSO) fails when connecting from external VPN networks.", "rating": 2, "platform": "Windows", "theme": "Authentication & OTP", "sentiment": "negative"},
        {"text": "Biometric login fingerprint prompt crashes the Android app on cold launch.", "rating": 1, "platform": "Android", "theme": "Authentication & OTP", "sentiment": "negative"},
        {"text": "MFA prompt works on desktop but requires re-authentication twice on tablet.", "rating": 3, "platform": "Android", "theme": "Authentication & OTP", "sentiment": "neutral"},
        # Mobile Battery Drain
        {"text": "Teams drains 40% phone battery in a single 45-minute conference call. Phone gets burning hot.", "rating": 1, "platform": "Android", "theme": "Mobile Battery Drain", "sentiment": "negative"},
        {"text": "Massive background battery drain on iOS even when no meetings are active.", "rating": 2, "platform": "iOS", "theme": "Mobile Battery Drain", "sentiment": "negative"},
        {"text": "Battery impact is noticeable during long calls, though low-power mode helps slightly.", "rating": 3, "platform": "iOS", "theme": "Mobile Battery Drain", "sentiment": "neutral"}
    ]

    # v5.1: Audio / Video glitches, Bluetooth headset disconnects, Electron RAM hogging
    v51_recipes = [
        # Audio / Video issues (Negative)
        {"text": "Microphone keeps randomly auto-muting during customer demos. Very embarrassing.", "rating": 1, "platform": "Windows", "theme": "Audio / Video", "sentiment": "negative"},
        {"text": "Bluetooth headset disconnects every time someone starts screensharing in meeting.", "rating": 1, "platform": "Windows", "theme": "Audio / Video", "sentiment": "negative"},
        {"text": "Severe audio echo and robotic voice distortion when more than 5 participants speak.", "rating": 2, "platform": "Web", "theme": "Audio / Video", "sentiment": "negative"},
        {"text": "Webcam video feed freezes for 10 seconds whenever a PowerPoint slide changes.", "rating": 2, "platform": "Windows", "theme": "Audio / Video", "sentiment": "negative"},
        {"text": "Audio delay of nearly 3 seconds between Android speakerphone and desktop participants.", "rating": 1, "platform": "Android", "theme": "Audio / Video", "sentiment": "negative"},
        {"text": "Call connects fine over high-speed Ethernet, but degrades rapidly over Wi-Fi.", "rating": 3, "platform": "Windows", "theme": "Audio / Video", "sentiment": "neutral"},
        # File Sharing & OneDrive (Mixed/Negative)
        {"text": "File attachment upload throws error 0x8004 when attaching files from OneDrive folders.", "rating": 2, "platform": "Web", "theme": "File Sharing & OneDrive", "sentiment": "negative"},
        {"text": "Shared Excel sheet in meeting chat won't open in live co-authoring mode.", "rating": 2, "platform": "Windows", "theme": "File Sharing & OneDrive", "sentiment": "negative"},
        {"text": "File preview takes around 8-10 seconds to render large PDF presentations.", "rating": 3, "platform": "Web", "theme": "File Sharing & OneDrive", "sentiment": "neutral"},
        # Performance / Memory
        {"text": "Teams consumes 2.8 GB of RAM and slows down my entire workstation.", "rating": 1, "platform": "Windows", "theme": "Performance & Memory", "sentiment": "negative"},
        {"text": "Average memory footprint is around 1.2 GB. It's tolerable on 32GB RAM machines.", "rating": 3, "platform": "Windows", "theme": "Performance & Memory", "sentiment": "neutral"}
    ]

    # v5.0: Tenant switching bugs, Legacy preview bugs
    v50_recipes = [
        {"text": "Switching between guest tenant organizations takes up to 45 seconds and logs out chat.", "rating": 2, "platform": "Web", "theme": "Tenant Switching", "sentiment": "negative"},
        {"text": "Calendar meeting invites from external Outlook contacts never sync to the Teams agenda.", "rating": 2, "platform": "Windows", "theme": "Calendar Sync", "sentiment": "negative"},
        {"text": "Initial preview version is sluggish and search takes forever.", "rating": 2, "platform": "Windows", "theme": "General Performance", "sentiment": "negative"},
        {"text": "Basic messaging works, but organization switcher dropdown has noticeable lag.", "rating": 3, "platform": "Web", "theme": "Tenant Switching", "sentiment": "neutral"},
        {"text": "Usable for internal team chat, but waiting on calendar and meeting polish.", "rating": 3, "platform": "Windows", "theme": "General Performance", "sentiment": "neutral"}
    ]

    # Add specific curated recipes for Teams across versions
    def inject_recipes(recipe_list, version_name, target_count=50):
        for idx in range(target_count):
            base = recipe_list[idx % len(recipe_list)]
            name = names_pool[(idx * 3 + random.randint(0, 5)) % len(names_pool)]
            rating = base["rating"]
            sentiment = base["sentiment"]
            score = 0.8 if sentiment == "positive" else (-0.75 if sentiment == "negative" else 0.0)

            # slight variations in text
            variations = [
                base["text"],
                f"Update review for {version_name}: {base['text']}",
                f"{base['text']} Really noticeable in day to day workflow."
            ]
            chosen_text = variations[idx % len(variations)]
            title = chosen_text.split(".")[0][:40]

            rev = {
                "id": generate_id(),
                "customer_id": "user-customer-main" if idx == 0 and version_name == "v5.3" else f"user-gen-{idx}",
                "company_id": "c-microsoft",
                "product_id": "p-microsoft-teams",
                "app_version": version_name,
                "user_name": name,
                "user_avatar": get_avatar(name),
                "rating": rating,
                "title": title,
                "text": chosen_text,
                "platform": base["platform"],
                "country": regions[idx % len(regions)],
                "language": "en",
                "created_at": get_date_in_range(
                    15 if version_name == "v5.3" else (40 if version_name == "v5.2" else (70 if version_name == "v5.1" else 115)),
                    1 if version_name == "v5.3" else (20 if version_name == "v5.2" else (50 if version_name == "v5.1" else 95))
                ),
                "is_anonymous": random.random() > 0.85,
                "helpful_count": random.randint(2, 48),
                "category": "Bug" if rating <= 2 else ("Performance" if "Performance" in base["theme"] else "General"),
                "sentiment": sentiment,
                "sentiment_score": score,
                "intent": "complaint" if rating <= 2 else ("praise" if rating >= 4 else "suggestion"),
                "emotion": "frustration" if rating <= 2 else ("delight" if rating >= 4 else "satisfaction"),
                "topic": base["theme"],
                "pii_detected": False,
                "quality_score": random.randint(75, 98),
                "tags": [base["theme"].lower(), base["platform"].lower(), version_name]
            }
            reviews.append(rev)

    inject_recipes(v53_recipes, "v5.3", target_count=65)
    inject_recipes(v52_recipes, "v5.2", target_count=75)
    inject_recipes(v51_recipes, "v5.1", target_count=60)
    inject_recipes(v50_recipes, "v5.0", target_count=45)

    # ─────────────────────────────────────────────────────────────────
    # Generative reviews for other products across companies
    # ─────────────────────────────────────────────────────────────────
    sample_review_templates = {
        "p-google-chrome": [
            ("Tab grouping and memory reduction works like a charm.", 5, "positive", "Tabs & Performance"),
            ("Occasional tab freeze when playing 4K 60fps video on Web.", 2, "negative", "Video Playback"),
            ("Memory saver is okay, though inactive tabs take 2 seconds to reload.", 3, "neutral", "Memory Saver"),
            ("Extensions syncing smoothly between Mac and Windows.", 5, "positive", "Extensions & Sync")
        ],
        "p-adobe-photoshop": [
            ("Generative fill in version 25.11 produces mind-blowing realism.", 5, "positive", "Generative AI"),
            ("Scratch disk full error pops up despite 80GB free SSD space.", 2, "negative", "Storage & Memory"),
            ("New UI workspace layout takes time getting used to, standard tools work fine.", 3, "neutral", "UI & Workflow"),
            ("Adjustment brush saves so much masking time.", 4, "positive", "Tools & Workflow")
        ],
        "p-nvidia-app": [
            ("Unified control panel replaces GeForce Experience perfectly.", 5, "positive", "Control Panel & UI"),
            ("AV1 encoding recording produces crystal clear 120 FPS game clips.", 5, "positive", "Video Capture"),
            ("App settings layout is decent, but missing a few legacy multi-display tweaks.", 3, "neutral", "Settings & Display"),
            ("RTX HDR filter caused black screen on multi-monitor setup.", 2, "negative", "Driver Compatibility")
        ],
        "p-phonepe-payments": [
            ("UPI Lite payment succeeds in 1 second without typing PIN.", 5, "positive", "UPI Lite & Speed"),
            ("Payment deducted from bank account but pending on merchant QR.", 1, "negative", "Payment Timeout"),
            ("Regular transfers work fine, but monthly statement PDF download is slow.", 3, "neutral", "Bank Statement"),
            ("App hangs when switching between bank accounts on Android.", 2, "negative", "App Stability")
        ],
        "p-zomato-food-delivery": [
            ("Food delivered hot in 18 minutes. Rider tracking was spot on.", 5, "positive", "Delivery Speed"),
            ("Delivery partner marked order delivered 5 minutes before arriving.", 2, "negative", "Delivery Accuracy"),
            ("Standard delivery experience, food was decent, nothing remarkable.", 3, "neutral", "Delivery Quality"),
            ("Great discounts with gold membership at local restaurant.", 4, "positive", "Deals & Offers")
        ],
        "p-spotify-spotify-music": [
            ("AI DJ recommendations are scarily accurate to my taste.", 5, "positive", "AI DJ & Playlists"),
            ("Podcast episode download stopped midway on mobile network.", 2, "negative", "Offline Downloads"),
            ("Audio playback is reliable, but playlist shuffle could offer more variety.", 3, "neutral", "Playback Quality")
        ],
        "p-notion-workspace": [
            ("Formulas 2.0 and automated database properties make project tracking a breeze.", 5, "positive", "Databases & Formulas"),
            ("Page loading latency on large workspaces with 500+ subpages.", 2, "negative", "Page Loading Speed"),
            ("Template gallery is convenient, though initial mobile workspace load takes 4 seconds.", 3, "neutral", "Mobile Performance")
        ]
    }

    # Generate additional reviews across all other products to reach ~3,500 total realistic reviews
    for p in products:
        pid = p["id"]
        cid = p["company_id"]
        if pid == "p-microsoft-teams":
            continue # already populated with rich test recipes

        # Determine number of reviews for this product
        p_count = random.randint(80, 160)
        p_releases = [r for r in releases if r["product_id"] == pid]
        templates = sample_review_templates.get(pid, [
            (f"Works as expected, happy with the {p['name']} updates.", 4, "positive", "General Quality"),
            (f"Decent performance for routine workflows, though room for polish.", 3, "neutral", "General Usability"),
            (f"Minor bug during initial setup in latest update.", 2, "negative", "Setup & Config"),
            (f"Standard features perform adequately on daily tasks.", 3, "neutral", "Feature Set"),
            (f"Very reliable service and clean modern interface.", 5, "positive", "Interface & Speed")
        ])

        for j in range(p_count):
            tpl = templates[j % len(templates)]
            rel = p_releases[j % len(p_releases)]
            name = names_pool[random.randint(0, len(names_pool) - 1)]
            plat = platforms[j % len(platforms)]
            reg = regions[j % len(regions)]
            rating = tpl[1]
            sentiment = tpl[2]
            score = 0.8 if sentiment == "positive" else -0.7

            rev = {
                "id": generate_id(),
                "customer_id": f"user-gen-{cid}-{j}",
                "company_id": cid,
                "product_id": pid,
                "app_version": rel["version"],
                "user_name": name,
                "user_avatar": get_avatar(name),
                "rating": rating,
                "title": tpl[0].split(".")[0][:35],
                "text": tpl[0],
                "platform": plat,
                "country": reg,
                "language": "en",
                "created_at": get_date_in_range(45, 0),
                "is_anonymous": random.random() > 0.8,
                "helpful_count": random.randint(0, 30),
                "category": "Bug" if rating <= 2 else "General",
                "sentiment": sentiment,
                "sentiment_score": score,
                "intent": "complaint" if rating <= 2 else "praise",
                "emotion": "frustration" if rating <= 2 else "delight",
                "topic": tpl[3],
                "pii_detected": False,
                "quality_score": random.randint(70, 95),
                "tags": [tpl[3].lower(), plat.lower(), rel["version"]]
            }
            reviews.append(rev)

    # Sort reviews chronologically
    reviews.sort(key=lambda r: r["created_at"], reverse=True)

    # ─────────────────────────────────────────────────────────────────
    # 5. DERIVED THEMES & ISSUES
    # ─────────────────────────────────────────────────────────────────
    themes = []
    issues = []
    actions = []
    fix_verifications = []

    # Teams specific themes for each version
    teams_themes = [
        # v5.3 themes
        {"id": "theme-teams-53-audio", "product_id": "p-microsoft-teams", "version": "v5.3", "name": "Audio / Video", "review_count": 25, "sentiment": "positive", "trend": "up", "priority": "high", "topic": "Audio / Video"},
        {"id": "theme-teams-53-search", "product_id": "p-microsoft-teams", "version": "v5.3", "name": "Search & Discovery", "review_count": 18, "sentiment": "positive", "trend": "up", "priority": "medium", "topic": "Search & Discovery"},
        {"id": "theme-teams-53-perf", "product_id": "p-microsoft-teams", "version": "v5.3", "name": "Performance & Memory", "review_count": 16, "sentiment": "positive", "trend": "up", "priority": "high", "topic": "Performance & Memory"},
        {"id": "theme-teams-53-notif", "product_id": "p-microsoft-teams", "version": "v5.3", "name": "Notification Sync", "review_count": 6, "sentiment": "negative", "trend": "stable", "priority": "low", "topic": "Notification Sync"},

        # v5.2 themes
        {"id": "theme-teams-52-payment", "product_id": "p-microsoft-teams", "version": "v5.2", "name": "Payment Problems", "review_count": 32, "sentiment": "negative", "trend": "up", "priority": "critical", "topic": "Payment Problems"},
        {"id": "theme-teams-52-auth", "product_id": "p-microsoft-teams", "version": "v5.2", "name": "Authentication & OTP", "review_count": 28, "sentiment": "negative", "trend": "up", "priority": "critical", "topic": "Authentication & OTP"},
        {"id": "theme-teams-52-battery", "product_id": "p-microsoft-teams", "version": "v5.2", "name": "Mobile Battery Drain", "review_count": 15, "sentiment": "negative", "trend": "stable", "priority": "high", "topic": "Mobile Battery Drain"},

        # v5.1 themes
        {"id": "theme-teams-51-audio", "product_id": "p-microsoft-teams", "version": "v5.1", "name": "Audio / Video", "review_count": 28, "sentiment": "negative", "trend": "up", "priority": "critical", "topic": "Audio / Video"},
        {"id": "theme-teams-51-files", "product_id": "p-microsoft-teams", "version": "v5.1", "name": "File Sharing & OneDrive", "review_count": 18, "sentiment": "negative", "trend": "stable", "priority": "high", "topic": "File Sharing & OneDrive"},
        {"id": "theme-teams-51-perf", "product_id": "p-microsoft-teams", "version": "v5.1", "name": "Performance & Memory", "review_count": 14, "sentiment": "negative", "trend": "stable", "priority": "medium", "topic": "Performance & Memory"},

        # v5.0 themes
        {"id": "theme-teams-50-tenant", "product_id": "p-microsoft-teams", "version": "v5.0", "name": "Tenant Switching", "review_count": 22, "sentiment": "negative", "trend": "stable", "priority": "high", "topic": "Tenant Switching"},
        {"id": "theme-teams-50-calendar", "product_id": "p-microsoft-teams", "version": "v5.0", "name": "Calendar Sync", "review_count": 15, "sentiment": "negative", "trend": "stable", "priority": "medium", "topic": "Calendar Sync"}
    ]
    themes.extend(teams_themes)

    # Teams specific issues
    teams_issues = [
        # v5.3 issues
        {
            "id": "issue-teams-53-notif",
            "product_id": "p-microsoft-teams",
            "version": "v5.3",
            "title": "Delayed Push Notifications on Android 14",
            "description": "Background notification delivery delayed by up to 5 minutes on Android devices when power-saving mode is active.",
            "severity": "high",
            "status": "in_progress",
            "review_count": 14,
            "trend_percentage": 22,
            "affected_platforms": {"Android": 14},
            "affected_versions": {"v5.3": 14},
            "affected_countries": {"US": 8, "IN": 4, "EU": 2},
            "priority_score": 68,
            "priority_breakdown": {"volume": 20, "severity": 18, "trend": 14, "affected_users": 10, "recency": 6},
            "root_cause_type": "observed",
            "root_cause_description": "Android 14 standby bucket restrictions suspend WebSocket listener when client is backgrounded.",
            "recommended_action": "Migrate background push wakeups to High Priority FCM payload with local alarm manager.",
            "suggested_owner": "Mobile Platform & Notifications Team",
            "expected_impact": "Restores immediate incoming call alerts for 4.2M Android users",
            "created_at": (now - timedelta(days=12)).isoformat(),
            "updated_at": now.isoformat()
        },
        {
            "id": "issue-teams-53-scaling",
            "product_id": "p-microsoft-teams",
            "version": "v5.3",
            "title": "High-DPI Multi-Monitor Window Blur",
            "description": "Client UI rasterization degrades into blurry text when dragged between 4K UHD monitors and 1080p laptop displays.",
            "severity": "medium",
            "status": "detected",
            "review_count": 9,
            "trend_percentage": 15,
            "affected_platforms": {"Windows": 9},
            "affected_versions": {"v5.3": 9},
            "affected_countries": {"US": 5, "UK": 2, "EU": 2},
            "priority_score": 54,
            "priority_breakdown": {"volume": 14, "severity": 15, "trend": 11, "affected_users": 8, "recency": 6},
            "root_cause_type": "inferred",
            "root_cause_description": "Per-monitor DPI v2 awareness message dropped during desktop compositor cross-monitor handoff.",
            "recommended_action": "Enable dynamic WM_DPICHANGED handler in native Electron shell wrapper.",
            "suggested_owner": "Windows Client Experience Team",
            "expected_impact": "Resolves display friction on dual-monitor executive workstations",
            "created_at": (now - timedelta(days=9)).isoformat(),
            "updated_at": now.isoformat()
        },
        {
            "id": "issue-teams-53-calendar",
            "product_id": "p-microsoft-teams",
            "version": "v5.3",
            "title": "External Attendee Calendar Sync Latency",
            "description": "Meeting invites created by external Microsoft 365 tenants take up to 10 minutes to populate channel calendar tab.",
            "severity": "medium",
            "status": "investigating",
            "review_count": 7,
            "trend_percentage": 10,
            "affected_platforms": {"Web": 5, "Windows": 2},
            "affected_versions": {"v5.3": 7},
            "affected_countries": {"US": 4, "IN": 3},
            "priority_score": 46,
            "priority_breakdown": {"volume": 12, "severity": 12, "trend": 10, "affected_users": 7, "recency": 5},
            "root_cause_type": "observed",
            "root_cause_description": "Webhook backpressure queue on Exchange Graph delta synchronization during morning peak hours.",
            "recommended_action": "Introduce partitioned Kafka consumer groups for cross-tenant calendar webhooks.",
            "suggested_owner": "Exchange & Calendar Integration Team",
            "expected_impact": "Reduces external meeting sync latency from 10 minutes to under 8 seconds",
            "created_at": (now - timedelta(days=7)).isoformat(),
            "updated_at": now.isoformat()
        },
        # v5.2 issues
        {
            "id": "issue-teams-52-payment",
            "product_id": "p-microsoft-teams",
            "version": "v5.2",
            "title": "Payment Gateway Timeout on Subscription Renewal",
            "description": "Enterprise workspace renewal transactions failing with gateway 504 timeouts, preventing user license allocations.",
            "severity": "critical",
            "status": "fixed",
            "review_count": 32,
            "trend_percentage": 42,
            "affected_platforms": {"Web": 22, "Windows": 6, "Android": 4},
            "affected_versions": {"v5.2": 32},
            "affected_countries": {"US": 18, "IN": 8, "EU": 6},
            "priority_score": 92,
            "priority_breakdown": {"volume": 28, "severity": 25, "trend": 18, "affected_users": 13, "recency": 8},
            "root_cause_type": "observed",
            "root_cause_description": "Microservice timeout in billing proxy when validating corporate tax exemptions.",
            "recommended_action": "Deploy retry queue on commerce proxy and increase timeout ceiling to 10s.",
            "suggested_owner": "Commerce & Billing Team",
            "expected_impact": "Recovers $240K/month in interrupted renewals",
            "created_at": (now - timedelta(days=28)).isoformat(),
            "updated_at": now.isoformat()
        },
        {
            "id": "issue-teams-52-auth",
            "product_id": "p-microsoft-teams",
            "version": "v5.2",
            "title": "Endless MFA Loop & Expired OTP Tokens",
            "description": "Users repeatedly prompted for multi-factor authentication due to expired token caching on Safari and mobile web.",
            "severity": "critical",
            "status": "in_progress",
            "review_count": 28,
            "trend_percentage": 35,
            "affected_platforms": {"Web": 15, "Android": 8, "iOS": 5},
            "affected_versions": {"v5.2": 28},
            "affected_countries": {"US": 14, "EU": 8, "IN": 6},
            "priority_score": 88,
            "priority_breakdown": {"volume": 26, "severity": 24, "trend": 17, "affected_users": 12, "recency": 9},
            "root_cause_type": "inferred",
            "root_cause_description": "Cross-domain session cookie partitioning in modern browsers invalidates auth token.",
            "recommended_action": "Migrate authentication handshake to Storage Access API and extend OTP TTL.",
            "suggested_owner": "Identity & Security Team",
            "expected_impact": "Eliminates 90% of repeated sign-in support tickets",
            "created_at": (now - timedelta(days=25)).isoformat(),
            "updated_at": now.isoformat()
        },
        {
            "id": "issue-teams-51-audio",
            "product_id": "p-microsoft-teams",
            "version": "v5.1",
            "title": "Bluetooth Headset Disconnects During Screen Sharing",
            "description": "Audio driver renegotiation crashes Bluetooth A2DP profile when desktop compositor begins screen capture.",
            "severity": "critical",
            "status": "fixed",
            "review_count": 28,
            "trend_percentage": -45,
            "affected_platforms": {"Windows": 20, "Web": 8},
            "affected_versions": {"v5.1": 28},
            "affected_countries": {"US": 16, "UK": 8, "CA": 4},
            "priority_score": 85,
            "priority_breakdown": {"volume": 25, "severity": 23, "trend": 16, "affected_users": 13, "recency": 8},
            "root_cause_type": "observed",
            "root_cause_description": "Exclusive mode lock on WASAPI audio device during capture initialization.",
            "recommended_action": "Switch audio subsystem capture hook to shared audio endpoint mode.",
            "suggested_owner": "Media & Audio Team",
            "expected_impact": "Resolves call interruptions for 180K daily headset users",
            "created_at": (now - timedelta(days=60)).isoformat(),
            "updated_at": now.isoformat()
        }
    ]
    issues.extend(teams_issues)

    # Actions for teams
    actions.append({
        "id": "action-1-payment",
        "issue_id": "issue-teams-52-payment",
        "title": "Deploy resilient billing proxy retry logic",
        "owner": "Sarah Johnson",
        "priority": "critical",
        "expected_impact": "High",
        "status": "completed",
        "created_at": (now - timedelta(days=20)).isoformat()
    })
    actions.append({
        "id": "action-2-auth",
        "issue_id": "issue-teams-52-auth",
        "title": "Implement Storage Access API for session cookies",
        "owner": "Identity Team",
        "priority": "high",
        "expected_impact": "High",
        "status": "in_progress",
        "created_at": (now - timedelta(days=15)).isoformat()
    })

    # Fix verification
    fix_verifications.append({
        "id": "verify-issue-teams-52-payment",
        "issue_id": "issue-teams-52-payment",
        "action_id": "action-1-payment",
        "status": "verified",
        "verify_after_days": 14,
        "before_metrics": {"complaint_rate": 42.0, "review_count": 32},
        "after_metrics": {"complaint_rate": 2.5, "review_count": 2},
        "change_percentage": -94.0,
        "verified_at": (now - timedelta(days=2)).isoformat()
    })

    # Notifications
    notifications = [
        {
            "id": generate_id(),
            "type": "issue_alert",
            "title": "High Volume Payment Failures Detected in v5.2",
            "description": "32 negative reviews flagged payment timeout in Teams Essentials checkout.",
            "severity": "critical",
            "read": False,
            "created_at": (now - timedelta(days=26)).isoformat(),
            "related_issue_id": "issue-teams-52-payment"
        },
        {
            "id": generate_id(),
            "type": "fix_verified",
            "title": "Fix Verified: Payment Gateway Timeouts Reduced by 94%",
            "description": "Post-release telemetry confirms failure rate dropped to near zero.",
            "severity": "success",
            "read": True,
            "created_at": (now - timedelta(days=2)).isoformat(),
            "related_issue_id": "issue-teams-52-payment"
        }
    ]

    return {
        "companies": companies,
        "products": products,
        "releases": releases,
        "reviews": reviews,
        "themes": themes,
        "issues": issues,
        "actions": actions,
        "fix_verifications": fix_verifications,
        "users": users,
        "notifications": notifications
    }

def save_data(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_data(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

if __name__ == '__main__':
    data = generate_all_data()
    out_path = 'C:/Users/tusha/.gemini/antigravity/scratch/review-lens/data/seed_data.json'
    save_data(data, out_path)
    print(f"Generated: {len(data['companies'])} companies, {len(data['products'])} products, {len(data['reviews'])} reviews, {len(data['releases'])} releases")
