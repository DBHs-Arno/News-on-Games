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
