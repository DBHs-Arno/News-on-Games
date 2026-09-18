# 🎮 Game Data Hub (News on Games)

An automated, lightweight global gaming news aggregator and tech insights web engine. This platform periodically pulls publicly available RSS feeds from major gaming publications and displays them in a centralized interface.

---

## ⚖️ Legal Disclaimer & Non-Commercial Notice

* **Educational & Research Purpose Only:** This project was developed solely as a personal portfolio project for learning data science, web scraping, and automated pipeline workflows (CI/CD via GitHub Actions).
* **Non-Commercial Use:** This site is strictly non-profit and non-commercial. No monetization, advertising, or paid services are associated with this project.
* **Content Ownership & Attribution:** All news articles, titles, and excerpts belong entirely to their respective content creators and publications (e.g., IGN, Eurogamer, Polygon). Each article card provides a direct link back to the original source to attribute proper credit and drive traffic to the publishers.
* **No Copyright Infringement Intended:** This platform operates in compliance with standard Web RSS usage guidelines. If you are a copyright holder and wish to have your feed removed from this aggregator, please open an issue in this repository, and it will be removed immediately.

---

## 🛠️ Tech Stack & Architecture

- **Frontend:** HTML5, Modern CSS (Flexbox & CSS Variables), JavaScript (Fetch API)
- **Data Pipeline:** Python 3 (`feedparser`, `BeautifulSoup4`)
- **Hosting & Automation:** GitHub Pages & GitHub Actions

---

## 🚀 How It Works

1. A Python scraper script executes periodically via GitHub Actions.
2. Public RSS feeds are fetched, sanitized, and stored as structured `news.json` data.
3. The static web page fetches `news.json` on client load to render the latest news cards dynamically.
