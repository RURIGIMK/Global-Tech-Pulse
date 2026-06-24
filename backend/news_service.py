import httpx
from openai import OpenAI
from config import NEWSAPI_KEY, OPENAI_API_KEY

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

client = OpenAI(api_key=OPENAI_API_KEY)

def is_tech_article(article: dict) -> bool:
    text = (article.get("title", "") + " " + article.get("description", "")).lower()
    return not any(word in text for word in NON_TECH_KEYWORDS)

def assign_category(article: dict) -> str:
    text = (
        article.get("title", "") + " "
        + article.get("description", "") + " "
        + (article.get("content", "") or "")
    ).lower()
    for category, keywords in CATEGORY_MAP.items():
        if any(kw in text for kw in keywords):
            return category
    return "Other Tech"

async def fetch_and_process_news() -> list[dict]:
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
    # Keep only articles with mandatory fields
    articles = [a for a in articles if a.get("title") and a.get("url") and a.get("urlToImage") and a.get("publishedAt")]
    # Tech filter
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
        if category == "Other Tech" and len(processed) > 30:
            continue

        try:
            summary = await summarize_with_ai(article)
        except Exception as e:
            print(f"Summarization failed for '{article['title']}': {e}")
            summary = article.get("description", "No summary available.")

        processed.append({
            "id": _hash_url(article["url"]),
            "title": article["title"],
            "description": article.get("description", ""),
            "url": article["url"],
            "image": article["urlToImage"],
            "source": article.get("source", {}).get("name", "Unknown"),
            "publishedAt": article["publishedAt"],
            "category": category,
            "summary": summary,
        })
        print(f"Processed: {article['title'][:60]}")

    return processed

async def summarize_with_ai(article: dict) -> str:
    prompt = (
        "Summarize this tech news article in 3-4 concise paragraphs. "
        "Focus only on key facts, avoid any opinion or extra commentary.\n\n"
        f"Title: {article['title']}\n"
        f"Description: {article.get('description', '')}\n"
        f"Content snippet: {(article.get('content') or article.get('description', ''))[:2000]}"
    )
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a tech journalist summarising articles for a professional news site."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300,
        temperature=0.5,
    )
    return response.choices[0].message.content.strip()

def _hash_url(url: str) -> str:
    import hashlib
    import base64
    return base64.urlsafe_b64encode(hashlib.sha256(url.encode()).digest()[:8]).decode().rstrip("=")
