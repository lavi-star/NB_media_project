import feedparser
import requests
from bs4 import BeautifulSoup
from typing import List, Dict

class AutoResearcherAgent:
    def __init__(self):
        # High-signal feeds relevant to media, marketing, tech, and creator economics
        self.rss_feeds = [
            "https://techcrunch.com/feed/",
            "https://www.theverge.com/rss/index.xml"
        ]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def fetch_trending_topics(self, max_results_per_feed: int = 3) -> List[Dict[str, str]]:
        """
        Step 1: Parse RSS feeds to extract trending industry headlines and links.
        """
        print("📰 Scanning RSS feeds for trending industry news...")
        discovered_articles = []

        for feed_url in self.rss_feeds:
            try:
                feed = feedparser.parse(feed_url)
                # Safeguard against parsing empty or broken feeds
                entries = feed.entries[:max_results_per_feed]
                
                for entry in entries:
                    discovered_articles.append({
                        "title": entry.get("title", ""),
                        "link": entry.get("link", ""),
                        "summary": entry.get("summary", "")
                    })
            except Exception as e:
                print(f"⚠️ Failed parsing RSS feed {feed_url}: {e}")

        print(f"✅ Discovered {len(discovered_articles)} potential source topics.")
        return discovered_articles

    def scrape_article_content(self, url: str) -> str:
        """
        Step 2: Web-scrape the actual text body of the target article 
        so the LLM has deep context to analyze.
        """
        print(f"🕷️ Web scraping article body: {url}")
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                return "Could not retrieve full article text."

            soup = BeautifulSoup(response.text, "html.parser")
            
            # Extract paragraphs from the main content body
            paragraphs = soup.find_all("p")
            # Join top 8 paragraphs to prevent context window bloat while capturing the essence
            article_text = " ".join([p.get_text() for p in paragraphs[:8]])
            
            # Basic string cleaning
            cleaned_text = " ".join(article_text.split())
            return cleaned_text[:2000] # Cap character length for performance stability
            
        except Exception as e:
            print(f"⚠️ Scraping failed for {url}: {e}")
            return "Context retrieval failed due to connection timeout."

    def execute_auto_research(self) -> List[Dict[str, str]]:
        """
        Combines RSS tracking and deeper web scraping into a single pipeline output.
        """
        raw_topics = self.fetch_trending_topics(max_results_per_feed=2)
        enriched_topics = []

        for topic in raw_topics:
            # Run the scraper on the live URL
            full_context = self.scrape_article_content(topic["link"])
            
            enriched_topics.append({
                "topic_title": topic["title"],
                "source_url": topic["link"],
                "scraped_context": full_context
            })
            
        return enriched_topics

# -------------------------------------------------------------------
# Local Test Block
# -------------------------------------------------------------------
if __name__ == "__main__":
    researcher = AutoResearcherAgent()
    # Run a test cycle to see live web data extraction working
    test_results = researcher.execute_auto_research()
    
    print("\n========================================")
    # Print out the first item to verify the data shape matches expectations
    if test_results:
        print(f"🔥 TEST ITEM SUCCESS:")
        print(f"Title: {test_results[0]['topic_title']}")
        print(f"URL: {test_results[0]['source_url']}")
        print(f"Scraped Context Snippet: {test_results[0]['scraped_context'][:300]}...")
    else:
        print("❌ No articles fetched.")
    print("========================================")