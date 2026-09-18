import feedparser
import json
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from datetime import datetime

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

def generate_rss_feed(news_list):
    """Toplanan verilerden standart RSS 2.0 (feed.xml) dosyası oluşturur."""
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = "Game Data Hub - Global Gaming News"
    ET.SubElement(channel, "link").text = "https://DBHs-Arno.github.io/News-on-Games/"
    ET.SubElement(channel, "description").text = "Automated Global Gaming News & Tech Insights Feed"
    ET.SubElement(channel, "language").text = "en-us"

    for item in news_list:
        item_elem = ET.SubElement(channel, "item")
        ET.SubElement(item_elem, "title").text = f"[{item['category']}] {item['title']}"
        ET.SubElement(item_elem, "link").text = item['link']
        ET.SubElement(item_elem, "description").text = item['summary']
        ET.SubElement(item_elem, "pubDate").text = str(item['date'])
        ET.SubElement(item_elem, "guid").text = item['link']

    tree = ET.ElementTree(rss)
    ET.indent(tree, space="  ", level=0)
    tree.write("feed.xml", encoding="utf-8", xml_declaration=True)
    print("Successfully generated feed.xml!")

def fetch_gaming_news():
    news_list = []

    for source_name, feed_url in RSS_FEEDS.items():
        print(f"Fetching news from {source_name}...")
        feed = feedparser.parse(feed_url)

        for entry in feed.entries[:5]:
            title = entry.get("title", "No Title")
            link = entry.get("link", "#")
            published = entry.get("published", datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"))
            
            summary_raw = entry.get("summary", entry.get("description", ""))
            summary = clean_html(summary_raw)[:250] + "..."

            news_list.append({
                "title": title,
                "category": source_name,
                "summary": summary,
                "date": published,
                "link": link
            })

    # 1. JSON olarak kaydet (Sitemiz için)
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(news_list, f, ensure_ascii=False, indent=2)
    print(f"Successfully saved {len(news_list)} articles to news.json!")

    # 2. RSS XML olarak kaydet (Dış siteler ve servisler için)
    generate_rss_feed(news_list)

if __name__ == "__main__":
    fetch_gaming_news()
    import json
import re
import xml.etree.ElementTree as ET
from datetime import datetime
import feedparser
from bs4 import BeautifulSoup
from textblob import TextBlob

# Genişletilmiş Haber Kaynakları
RSS_FEEDS = {
    "IGN": "https://feeds.feedburner.com/ign/all",
    "Eurogamer": "https://www.eurogamer.net/feed/news",
    "Polygon": "https://www.polygon.com/rss/index.xml",
    "PC Gamer": "https://www.pcgamer.com/rss/",
    "GameSpot": "https://www.gamespot.com/feeds/news/"
}

# Sık geçen oyun teknolojisi ve platform anahtar kelimeleri
GAMING_KEYWORDS = [
    "Unreal Engine", "Ray Tracing", "DLSS", "PlayStation", "Xbox", "Nintendo",
    "Steam", "AI", "Graphics", "FPS", "Remake", "Cyberpunk", "RPG", "Esports",
    "Patch", "GPU", "Nvidia", "AMD"
]

def clean_html(raw_html):
    if not raw_html:
        return ""
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text().strip()

def calculate_reading_time(text):
    words = len(text.split())
    minutes = max(1, round(words / 200))
    return f"{minutes} min read"

def analyze_sentiment(text):
    """NLP: Metnin duygu analizi skorunu (-1.0 ile +1.0) çıkarır."""
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity
    if polarity > 0.1:
        return "Positive / Hype", round(polarity, 2), "success"
    elif polarity < -0.1:
        return "Critical / Mixed", round(polarity, 2), "danger"
    else:
        return "Neutral / Informative", round(polarity, 2), "info"

def extract_tags(text):
    """Metin içerisinden öne çıkan etiketleri otomasyonla yakalar."""
    found_tags = []
    for kw in GAMING_KEYWORDS:
        if re.search(r'\b' + re.escape(kw) + r'\b', text, re.IGNORECASE):
            found_tags.append(kw)
    if not found_tags:
        found_tags = ["Gaming", "News"]
    return list(set(found_tags))

def fetch_and_process_news():
    processed_news = []
    source_counts = {}
    sentiment_summary = {"Positive / Hype": 0, "Neutral / Informative": 0, "Critical / Mixed": 0}

    for source_name, feed_url in RSS_FEEDS.items():
        print(f"Processing feed: {source_name}...")
        feed = feedparser.parse(feed_url)
        source_counts[source_name] = 0

        for entry in feed.entries[:4]: # Her kaynaktan 4 makale
            title = entry.get("title", "Untitled")
            link = entry.get("link", "#")
            published = entry.get("published", datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT"))
            
            raw_summary = entry.get("summary", entry.get("description", ""))
            clean_summary = clean_html(raw_summary)[:300] + "..." if len(raw_summary) > 300 else clean_html(raw_summary)

            # --- NLP & Data Enrichment ---
            sentiment_label, sentiment_score, sentiment_badge = analyze_sentiment(title + " " + clean_summary)
            tags = extract_tags(title + " " + clean_summary)
            read_time = calculate_reading_time(clean_summary)

            # Metrik biriktirme
            sentiment_summary[sentiment_label] += 1
            source_counts[source_name] += 1

            processed_news.append({
                "id": len(processed_news) + 1,
                "title": title,
                "source": source_name,
                "summary": clean_summary,
                "date": published,
                "link": link,
                "sentiment": {
                    "label": sentiment_label,
                    "score": sentiment_score,
                    "badge": sentiment_badge
                },
                "tags": tags,
                "read_time": read_time
            })

    # --- Data Aggregation (Dashboard Analitiği için) ---
    analytics_data = {
        "last_updated": datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        "total_articles": len(processed_news),
        "sources_breakdown": source_counts,
        "sentiment_distribution": sentiment_summary
    }

    # 1. Enriched news.json
    with open("news.json", "w", encoding="utf-8") as f:
        json.dump(processed_news, f, ensure_ascii=False, indent=2)

    # 2. Analytics JSON for Dashboard
    with open("analytics.json", "w", encoding="utf-8") as f:
        json.dump(analytics_data, f, ensure_ascii=False, indent=2)

    print(f"Pipeline complete! Processed {len(processed_news)} articles with NLP enrichment.")

if __name__ == "__main__":
    fetch_and_process_news()
