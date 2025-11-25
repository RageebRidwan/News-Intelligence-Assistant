"""
Web Scraping Module for Multi-Source Intelligence Assistant
Extracts content from any webpage with smart parsing
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from typing import List, Dict
import time


class WebScraper:
    """
    General-purpose web scraper with intelligent content extraction
    """

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def scrape_url(self, url: str) -> Dict[str, str]:
        """
        Scrape a single URL and extract main content

        Args:
            url: The URL to scrape

        Returns:
            Dict with 'url', 'title', 'content', 'source_name'
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            # Extract title
            title = self._extract_title(soup)

            # Extract main content
            content = self._extract_content(soup)

            # Extract source name from URL
            source_name = urlparse(url).netloc.replace("www.", "")

            return {
                "url": url,
                "title": title,
                "content": content,
                "source_name": source_name,
                "success": True,
            }

        except Exception as e:
            return {
                "url": url,
                "title": "Error",
                "content": f"Failed to scrape: {str(e)}",
                "source_name": urlparse(url).netloc.replace("www.", ""),
                "success": False,
            }

    def scrape_multiple(self, urls: List[str]) -> List[Dict[str, str]]:
        """
        Scrape multiple URLs with rate limiting

        Args:
            urls: List of URLs to scrape

        Returns:
            List of scraped content dictionaries
        """
        results = []
        for url in urls:
            result = self.scrape_url(url)
            results.append(result)
            time.sleep(1)  # Rate limiting

        return results

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title with fallbacks"""
        # Try multiple title sources
        title_tags = [
            soup.find("h1"),
            soup.find("title"),
            soup.find("meta", property="og:title"),
        ]

        for tag in title_tags:
            if tag:
                if tag.name == "meta":
                    return tag.get("content", "Unknown Title")
                return tag.get_text().strip()

        return "Unknown Title"

    def _extract_content(self, soup: BeautifulSoup) -> str:
        """
        Extract main content with intelligent parsing
        Tries multiple strategies to find article content
        """
        # Remove unwanted elements
        for element in soup(["script", "style", "nav", "header", "footer", "aside"]):
            element.decompose()

        # Strategy 1: Look for article tag
        article = soup.find("article")
        if article:
            paragraphs = article.find_all("p")
            if paragraphs:
                return "\n\n".join(
                    [
                        p.get_text().strip()
                        for p in paragraphs
                        if len(p.get_text().strip()) > 50
                    ]
                )

        # Strategy 2: Look for main content div
        main_content = soup.find("main") or soup.find(
            "div",
            class_=["main-content", "article-content", "post-content", "entry-content"],
        )
        if main_content:
            paragraphs = main_content.find_all("p")
            if paragraphs:
                return "\n\n".join(
                    [
                        p.get_text().strip()
                        for p in paragraphs
                        if len(p.get_text().strip()) > 50
                    ]
                )

        # Strategy 3: Get all paragraphs (fallback)
        paragraphs = soup.find_all("p")
        if paragraphs:
            # Filter out short paragraphs (likely navigation/ads)
            content_paras = [
                p.get_text().strip()
                for p in paragraphs
                if len(p.get_text().strip()) > 50
            ]
            return "\n\n".join(
                content_paras[:20]
            )  # Limit to first 20 substantial paragraphs

        return "Could not extract content from this page."


# Quick test function
if __name__ == "__main__":
    scraper = WebScraper()

    # Test with a sample URL
    test_url = "https://example.com"
    result = scraper.scrape_url(test_url)

    print(f"Title: {result['title']}")
    print(f"Source: {result['source_name']}")
    print(f"Content Preview: {result['content'][:200]}...")
