from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from news_service import fetch_and_process_news
from kv_store import kv
import asyncio

app = FastAPI()

# Serve the React build (once we build it) as static files
# We will mount it later after the frontend is built; for now we just define the routes.

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.post("/api/refresh-news")
async def refresh_news():
    """Called by Vercel cron every hour. Fetches, processes and stores articles."""
    articles = await fetch_and_process_news()
    # Store full list
    await kv.set("articles", articles)
    # Store each article individually for detail pages
    for article in articles:
        await kv.set(f"article:{article['id']}", article)
    return {"success": True, "count": len(articles)}

@app.get("/api/articles")
async def get_articles():
    articles = await kv.get("articles")
    if articles is None:
        # First time: trigger a refresh
        articles = await fetch_and_process_news()
        await kv.set("articles", articles)
    return articles

@app.get("/api/articles/{article_id}")
async def get_article(article_id: str):
    article = await kv.get(f"article:{article_id}")
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

# In production, we'll serve the React frontend build
if os.path.exists("../frontend/dist"):
    app.mount("/", StaticFiles(directory="../frontend/dist", html=True), name="frontend")
