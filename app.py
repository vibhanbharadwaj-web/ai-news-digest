import streamlit as st
import feedparser
from datetime import datetime
import os
import re
import html
from dotenv import load_dotenv
from google import genai

# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="AI News Digest",
    page_icon="🤖",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background-color: #fff7fb;
}

.news-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    margin: 18px 0;
    border-left: 5px solid #ff6b9d;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}

.news-card h3 {
    color: #8e44ad;
    margin-top: 0;
}

.news-card p {
    color: #444444;
    line-height: 1.6;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD GEMINI API KEY
# ==========================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

# ==========================================
# HEADER
# ==========================================

st.html("""
<div style="
    background: linear-gradient(135deg, #ff6b9d, #c77dff, #ff9ecb);
    padding: 45px;
    border-radius: 22px;
    text-align: center;
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 8px 25px rgba(199,125,255,0.25);
">

    <h1 style="
        font-size: 44px;
        margin: 0 0 10px 0;
        color: white;
    ">
        🤖 AI News Digest
    </h1>

    <p style="
        font-size: 20px;
        margin: 5px;
        color: white;
    ">
        AI-powered daily news summarizer
    </p>

    <p style="
        font-size: 16px;
        margin: 8px;
        color: white;
    ">
        📰 Fetch • ✨ Summarize • 🏷️ Categorize • 💡 Understand
    </p>

</div>
""")

# ==========================================
# FETCH AI NEWS
# ==========================================

rss_url = "https://www.artificialintelligence-news.com/feed/"

feed = feedparser.parse(rss_url)

articles = []

for entry in feed.entries[:5]:

    raw_summary = entry.get("description", "")

    # Decode HTML entities
    clean_summary = html.unescape(raw_summary)

    # Remove HTML tags
    clean_summary = re.sub(
        r"<[^>]*>",
        "",
        clean_summary
    )

    # Decode HTML entities again
    clean_summary = html.unescape(clean_summary)

    # Remove extra whitespace
    clean_summary = " ".join(
        clean_summary.split()
    )

    articles.append({
        "title": entry.get(
            "title",
            "Untitled Article"
        ),
        "link": entry.get(
            "link",
            "#"
        ),
        "summary": clean_summary
    })

# ==========================================
# STATISTICS
# ==========================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📰 Articles",
        len(articles)
    )

with col2:
    st.metric(
        "📡 Source",
        "AI News"
    )

with col3:
    st.metric(
        "📅 Date",
        datetime.now().strftime("%d %b %Y")
    )

st.divider()

# ==========================================
# LATEST AI NEWS
# ==========================================

st.subheader("📰 Latest AI News")

if not articles:

    st.warning(
        "⚠️ No news articles found. "
        "Please try again later."
    )

else:

    for article in articles:

        # Escape content before displaying as HTML
        safe_title = html.escape(
            article["title"]
        )

        safe_summary = html.escape(
            article["summary"][:500]
        )

        st.markdown(
            f"""
            <div class="news-card">

                <h3>{safe_title}</h3>

                <p>
                    {safe_summary}...
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.link_button(
            "🔗 Read Original Article",
            article["link"]
        )

# ==========================================
# AI DIGEST
# ==========================================

st.divider()

st.subheader("✨ AI-Powered Summary")

if st.button(
    "✨ Generate AI Digest",
    use_container_width=True
):

    if not api_key:

        st.error(
            "❌ Gemini API key not found. "
            "Please check your Streamlit Secrets."
        )

    elif not articles:

        st.warning(
            "⚠️ No articles available "
            "to summarize."
        )

    else:

        try:

            # Create Gemini client
            client = genai.Client(
                api_key=api_key
            )

            # Prepare news text
            news_text = ""

            for article in articles:

                news_text += f"""

Title:
{article['title']}

Description:
{article['summary']}

Source URL:
{article['link']}

--------------------------------
"""

            # Generate AI digest
            with st.spinner(
                "🤖 Gemini is summarizing the latest AI news..."
            ):

                response = client.models.generate_content(

                    model="gemini-flash-lite-latest",

                    contents=f"""
You are an AI news analyst.

Create a professional and easy-to-understand
AI Daily Digest from the following news articles.

For EVERY article provide:

1. Title
2. Category
3. Summary
4. Key Takeaway
5. Why it matters
6. Source

Use categories such as:

- LLMs
- AI Research
- Open Source
- Product Launches
- Funding
- Robotics
- AI Tools
- Regulation
- Cybersecurity
- Infrastructure
- Agentic AI
- Other

Important instructions:

- Keep each summary concise.
- Use simple language.
- Do not invent information.
- Base the digest only on the provided articles.
- Clearly separate each article.
- Make the result professional and suitable for a portfolio project.

News articles:

{news_text}
"""
                )

            # ======================================
            # DISPLAY RESULT
            # ======================================

            st.success(
                "✅ Digest generated successfully!"
            )

            st.markdown(
                "## 🧠 AI Generated Digest"
            )

            st.markdown(
                response.text
            )

            # ======================================
            # SAVE DIGEST
            # ======================================

            date = datetime.now().strftime(
                "%d %B %Y"
            )

            digest = f"""# AI Daily Digest

Date: {date}

{response.text}
"""

            with open(
                "ai_news_digest.txt",
                "w",
                encoding="utf-8"
            ) as file:

                file.write(digest)

            st.success(
                "💾 Digest saved to ai_news_digest.txt"
            )

        except Exception as e:

            st.error(
                f"❌ Error generating AI digest: {e}"
            )

# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "🤖 AI News Digest • Built with Python, "
    "Gemini, Feedparser & Streamlit"
)