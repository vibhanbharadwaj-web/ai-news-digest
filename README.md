# ai-news-digest
AI News Digest Internship Assessment
# AI News Digest 🤖📰

An AI-powered news summarization tool that collects the latest Artificial Intelligence news articles and uses Google Gemini AI to generate concise summaries and key takeaways.

## Features

- Fetches latest AI news from RSS feeds
- Uses Gemini AI for automatic summarization
- Generates title, summary, and key takeaway
- Saves the generated digest into a text file
- Simple and lightweight Python implementation
- Automatically generates a daily digest using APScheduler
- Categorizes AI news articles
- Includes summaries, key takeaways, and why the news matters

## Technologies Used

- Python
- Google Gemini API
- Feedparser
- Python-dotenv
- RSS Feed
- APScheduler

## How It Works

1. Fetch AI news articles using RSS feeds.
2. Extract article titles and descriptions.
3. Send the news content to Gemini AI.
4. Generate structured summaries.
5. Save the final digest.
6. Scheduler runs the digest generation every 24 hours

## Installation

Install dependencies:

```bash
pip install -r requirements.txt