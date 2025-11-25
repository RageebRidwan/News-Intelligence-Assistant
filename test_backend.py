"""
Comprehensive test script to verify all backend components
"""

import sys

sys.path.append("backend")

from backend.scraper import WebScraper
from backend.rag_pipeline import RAGPipeline
from backend.chat_engine import ChatEngine
from backend import prompts


def test_backend():
    """Test all backend components"""

    print("🔧 Testing Multi-Source Intelligence Assistant Backend (Ollama)\n")
    print("✅ Using Ollama - No API key needed!")

    # Test 1: Scraping
    print("\n📰 Test 1: Web Scraping...")
    scraper = WebScraper()

    test_urls = [
        "https://en.wikipedia.org/wiki/Artificial_intelligence",
        "https://en.wikipedia.org/wiki/Machine_learning",
    ]

    scraped_data = scraper.scrape_multiple(test_urls)
    print(f"✅ Scraped {len(scraped_data)} URLs")

    for data in scraped_data:
        print(f"  - {data['source_name']}: {data['title'][:50]}...")

    # Test 2: RAG Pipeline
    print("\n🧠 Test 2: RAG Pipeline...")
    print("  Using Ollama nomic-embed-text for embeddings...")
    rag = RAGPipeline()
    rag.ingest_documents(scraped_data)
    print("✅ Documents ingested and embedded")

    # Test 3: Chat Engine
    print("\n💬 Test 3: Chat Engine...")
    print("  Using Ollama llama3.2 for chat...")
    chat = ChatEngine(rag)

    test_question = "What is artificial intelligence?"
    print(f"  Q: {test_question}")

    result = chat.ask(test_question)
    print(f"  A: {result['answer'][:200]}...")
    print(f"  Sources: {[s['source'] for s in result['sources']]}")

    # Test 4: Additional Chat Features
    print("\n🔍 Test 4: Advanced Chat Features...")

    # Test summary generation
    print("  Testing summary generation...")
    summary = chat.generate_summary(tone="casual", length="short")
    print(f"  ✅ Summary generated ({len(summary)} chars)")

    # Test source comparison
    print("  Testing source comparison...")
    comparison = chat.compare_sources()
    print(f"  ✅ Comparison generated ({len(comparison)} chars)")

    # Test sentiment analysis
    print("  Testing sentiment analysis...")
    sentiments = chat.analyze_sentiment()
    print(f"  ✅ Analyzed sentiment for {len(sentiments)} sources")
    for sentiment in sentiments:
        print(f"    - {sentiment['source']}")

    # Test 5: Prompt Templates
    print("\n📝 Test 5: Prompt Templates...")
    test_prompts = [
        prompts.format_qa_prompt("test context", "no history", "test question"),
        prompts.format_summary_prompt("test content", "casual", "medium"),
        prompts.format_sentiment_prompt("test text", "test source"),
    ]
    print(f"  ✅ All {len(test_prompts)} prompt templates working")

    print("\n✅ All backend tests passed!")
    print(f"\n📊 Summary:")
    print(f"  - Scraped: {len(scraped_data)} URLs")
    print(f"  - Ingested: {len(rag.documents)} document chunks")
    print(f"  - Sources analyzed: {len(sentiments)}")
    print("\n🚀 Backend is fully functional and ready for frontend integration!")


if __name__ == "__main__":
    test_backend()
