import httpx
from config import NEWSAPI_KEY

CATEGORY_MAP = {
    "Artificial Intelligence": [
        "ai", "machine learning", "gpt", "llm", "neural network",
        "deep learning", "openai", "chatgpt", "copilot", "gemini"
    ],
    "Startups & Business": [
        "startup", "funding", "ipo", "venture capital", "acquire", "valuation"
    ],
    "Gadgets & Hardware": [
        "smartphone", "laptop", "gpu", "chip", "apple", "samsung", "wearable", "device"
    ],
    "Cybersecurity": [
        "cyber", "hack", "vulnerability", "ransomware", "data breach", "malware"
    ],
    "Software & Programming": [
        "javascript", "python", "api", "framework", "open source", "github", "devops"
    ],
    "Science & Emerging Tech": [
        "quantum", "biotech", "space", "nuclear", "fusion", "nanotech", "robotics"
    ]
}

NON_TECH_KEYWORDS = [
    "politics", "election", "sport", "celebrity", "weather", "recipe", "fashion"
]


def is_tech_article(article: dict) -> bool:
    """Filter out articles clearly not about technology."""
    text = (article.get("title", "") + " " + article.get("description", "")).lower()
    return not any(word in text for word in NON_TECH_KEYWORDS)


def assign_category(article: dict) -> str:
    """Return the best tech category for an article."""
    text = (
        article.get("title", "") + " "
        + article.get("description", "") + " "
        + (article.get("content", "") or "")
    ).lower()
    for category, keywords in CATEGORY_MAP.items():
        if any(kw in text for kw in keywords):
            return category
    return "Other Tech"


def _hash_url(url: str) -> str:
    """Generate a short unique ID from a URL."""
    import hashlib
    import base64
    return base64.urlsafe_b64encode(
        hashlib.sha256(url.encode()).digest()[:8]
    ).decode().rstrip("=")


async def fetch_and_process_news() -> list[dict]:
    """
    1. Fetch 100 technology articles from NewsAPI
    2. Apply strict tech filter
    3. Categorise each article
    4. Return up to 50 processed articles (summary = description)
    """
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "technology",
        "language": "en",
        "pageSize": 100,
        "sortBy": "publishedAt",
        "apiKey": NEWSAPI_KEY,
    }

    async with httpx.AsyncClient() as http_client:
        resp = await http_client.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

    if data.get("status") != "ok":
        raise Exception(f"NewsAPI error: {data.get('message', 'unknown error')}")

    articles = data.get("articles", [])

    # Remove articles missing mandatory fields
    articles = [
        a for a in articles
        if a.get("title") and a.get("url") and a.get("urlToImage") and a.get("publishedAt")
    ]

    # Tech-only filter
    articles = [a for a in articles if is_tech_article(a)]

    # Deduplicate by url
    seen = set()
    deduped = []
    for a in articles:
        if a["url"] not in seen:
            seen.add(a["url"])
            deduped.append(a)
    articles = deduped

    processed = []
    for article in articles:
        if len(processed) >= 50:
            break

        category = assign_category(article)
        # Discard generic "Other Tech" after we already have 30 good ones
        if category == "Other Tech" and len(processed) > 30:
            continue

        processed.append({
            "id": _hash_url(article["url"]),
            "title": article["title"],
            "description": article.get("description", ""),
            "url": article["url"],
            "image": article["urlToImage"],
            "source": article.get("source", {}).get("name", "Unknown"),
            "publishedAt": article["publishedAt"],
            "category": category,
            "summary": article.get("description", ""),   # no AI, just use description
        })
        print(f"Processed: {article['title'][:60]}")

    print(f"Final processed count: {len(processed)}")
    return processed
