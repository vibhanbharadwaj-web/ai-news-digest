import os
from dotenv import load_dotenv
from google import genai
import feedparser
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


def generate_digest():

    # Load API key
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)


    # Fetch AI news
    rss_url = "https://www.artificialintelligence-news.com/feed/"

    feed = feedparser.parse(rss_url)

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
Create an AI Daily Digest.

For each article provide:
- Title
- Category
- Summary
- Key Takeaway
- Why it matters

News:
{news_text}
"""
    )


    date = datetime.now().strftime("%d %B %Y")

    digest = f"""
# AI Daily Digest
Date: {date}

{response.text}
"""


    print(digest)


    with open("ai_news_digest.txt", "w", encoding="utf-8") as file:
        file.write(digest)


    print("Digest saved successfully!")


# Run once immediately
generate_digest()


# Schedule every 24 hours
scheduler = BlockingScheduler()

scheduler.add_job(generate_digest, "interval", days=1)

scheduler.start()