import feedparser

rss_url = "https://feeds.feedburner.com/venturebeat/SZYF"

feed = feedparser.parse(rss_url)

print("\nLatest AI News\n")

for article in feed.entries[:5]:
    print(f"Title: {article.title}")
    print(f"Link: {article.link}")
    print("-" * 60)
