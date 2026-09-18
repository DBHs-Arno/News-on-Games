import feedparser
import json
import re
from bs4 import BeautifulSoup
from datetime import datetime

# Haber çekeceğimiz kaynakların RSS adresleri
RSS_FEEDS = {
    "IGN": "https://feeds.feedburner.com/ign/all",
    "Eurogamer": "https://www.eurogamer.net/feed/news",
    "Polygon": "https://www.polygon.com/rss/index.xml"
}

def clean_html(raw_html):
    """Özetlerdeki HTML etiketlerini temizler."""
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()

def fetch_gaming_news():
    news_list = []

    for source_name, feed_url in RSS_FEEDS.items():
        print(f"Fetching news from {source_name}...")
        feed = feedparser.parse(feed_url)

        # Her kaynaktan en güncel 5 haberi al
        for entry in feed.entries[:5]:
            title = entry.get("title", "No Title")
            link = entry.get("link", "#")
            
            # Tarih bilgisini ayarla
            published = entry.get("published", datetime.now().strftime("%Y-%m-%d"))
            
            # Özet metnini temizle
            summary_raw = entry.get("summary", entry.get("description", ""))
            summary = clean_html(summary_raw)[:200] + "..." # İlk 200 karakter

            news_list.append({
                "title": title,
                "category": source_name,
                "summary": summary,
                "date": published,
                "link": link
            })

    # Toplanan haberleri news.json dosyasına yaz
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(news_list, f, ensure_ascii=False, indent=2)

    print(f"Successfully saved {len(news_list)} news articles to news.json!")

if __name__ == "__main__":
    fetch_gaming_news()
