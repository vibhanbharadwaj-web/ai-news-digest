import os
from dotenv import load_dotenv
from google import genai
import feedparser

# Load API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# Gemini client
client = genai.Client(api_key=api_key)


# Fetch AI news
rss_url = "https://www.artificialintelligence-news.com/feed/"

feed = feedparser.parse(rss_url)

# Get first 3 news articles
articles = []

for entry in feed.entries[:3]:
    articles.append({
        "title": entry.title,
        "link": entry.link,
        "summary": entry.description
    })


# Send news to Gemini
news_text = ""

for article in articles:
    news_text += f"""
Title: {article['title']}
Description: {article['summary']}
"""


response = client.models.generate_content(
    model="gemini-flash-lite-latest",
    contents=f"""
Summarize these AI news articles.
Give:
- Title
- 2-3 line summary
- Key takeaway

News:
{news_text}
"""
)

digest = response.text

print(digest)

with open("ai_news_digest.txt", "w", encoding="utf-8") as file:
    file.write(digest)

print("\nDigest saved successfully!")
