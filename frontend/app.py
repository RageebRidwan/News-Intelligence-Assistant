"""
Multi-Source Intelligence Assistant - Streamlit Frontend
Interactive UI for RAG-based news/content analysis
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


from backend.scraper import WebScraper
from backend.rag_pipeline import RAGPipeline
from backend.chat_engine import ChatEngine

# Page config
st.set_page_config(
    page_title="Multi-Source Intelligence Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .source-card {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin-bottom: 0.5rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Initialize session state
if "rag_pipeline" not in st.session_state:
    st.session_state.rag_pipeline = None
if "chat_engine" not in st.session_state:
    st.session_state.chat_engine = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "sources_ingested" not in st.session_state:
    st.session_state.sources_ingested = []

# Header
st.markdown(
    '<div class="main-header">🧠 Multi-Source Intelligence Assistant</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">RAG-powered content analysis with conversational AI</div>',
    unsafe_allow_html=True,
)

# Sidebar - Data Ingestion
with st.sidebar:
    st.header("📥 Data Ingestion")

    st.markdown("**Enter URLs to analyze** (one per line)")
    urls_input = st.text_area(
        "URLs",
        height=150,
        placeholder="https://example.com/article1\nhttps://example.com/article2",
        label_visibility="collapsed",
    )

    col1, col2 = st.columns(2)
    with col1:
        scrape_button = st.button("🔍 Scrape & Ingest", use_container_width=True)
    with col2:
        clear_button = st.button("🗑️ Clear Data", use_container_width=True)

    # Handle scraping
    if scrape_button:
        if urls_input.strip():
            urls = [url.strip() for url in urls_input.split("\n") if url.strip()]

            with st.spinner("Scraping URLs..."):
                scraper = WebScraper()
                scraped_data = scraper.scrape_multiple(urls)

            # Check for successful scrapes
            successful = [d for d in scraped_data if d["success"]]

            if successful:
                with st.spinner("Building vector store..."):
                    st.session_state.rag_pipeline = RAGPipeline()
                    st.session_state.rag_pipeline.ingest_documents(successful)
                    st.session_state.chat_engine = ChatEngine(
                        st.session_state.rag_pipeline
                    )
                    st.session_state.sources_ingested = (
                        st.session_state.rag_pipeline.get_all_sources()
                    )

                st.success(f"✅ Ingested {len(successful)} sources successfully!")
                st.rerun()
            else:
                st.error(
                    "❌ Failed to scrape any URLs. Check your links and try again."
                )
        else:
            st.warning("⚠️ Please enter at least one URL")

    # Handle clear
    if clear_button:
        st.session_state.rag_pipeline = None
        st.session_state.chat_engine = None
        st.session_state.chat_history = []
        st.session_state.sources_ingested = []
        st.success("🗑️ Data cleared!")
        st.rerun()

    # Show ingested sources
    if st.session_state.sources_ingested:
        st.divider()
        st.subheader("📚 Ingested Sources")
        for source in st.session_state.sources_ingested:
            with st.expander(f"🔗 {source['source']}"):
                st.markdown(f"**Title:** {source['title']}")
                st.markdown(f"**URL:** [{source['url']}]({source['url']})")

# Main content area
if st.session_state.chat_engine is None:
    # Welcome screen
    st.info("👋 **Welcome!** Enter URLs in the sidebar to get started.")

    st.markdown("### 🎯 Features")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        **📊 Analysis Tools:**
        - Multi-source web scraping
        - RAG-based question answering
        - Source comparison & synthesis
        - Conversational memory
        """
        )

    with col2:
        st.markdown(
            """
        **🎨 Content Generation:**
        - Smart summaries (3 tones, 3 lengths)
        - Sentiment analysis per source
        - Citation tracking
        - Context-aware responses
        """
        )

    st.markdown("### 🚀 How to Use")
    st.markdown(
        """
    1. **Add URLs** in the sidebar (news articles, blog posts, any web content)
    2. **Scrape & Ingest** to build your knowledge base
    3. **Ask questions** or use analysis tools in the tabs below
    4. **Compare sources** to see different perspectives
    """
    )

else:
    # Tabs for different features
    tab1, tab2, tab3, tab4 = st.tabs(
        ["💬 Chat", "📝 Summaries", "🔍 Compare Sources", "📊 Sentiment Analysis"]
    )

    # Tab 1: Chat Interface
    with tab1:
        st.subheader("💬 Ask Questions")

        # Chat history display
        for i, (role, message) in enumerate(st.session_state.chat_history):
            if role == "user":
                st.markdown(f"**You:** {message}")
            else:
                st.markdown(f"**Assistant:** {message}")

        # Chat input
        user_question = st.text_input(
            "Ask a question about your sources:",
            placeholder="What are the main points discussed?",
            key="chat_input",
        )

        col1, col2 = st.columns([4, 1])
        with col1:
            ask_button = st.button("🚀 Ask", use_container_width=True)
        with col2:
            clear_chat_button = st.button("🗑️ Clear Chat", use_container_width=True)

        if ask_button and user_question:
            with st.spinner("Thinking..."):
                result = st.session_state.chat_engine.ask(user_question)

            # Add to history
            st.session_state.chat_history.append(("user", user_question))
            st.session_state.chat_history.append(("assistant", result["answer"]))

            # Show sources used
            with st.expander("📚 Sources Referenced"):
                for source in result["sources"]:
                    st.markdown(
                        f"- **{source['source']}**: [{source['title']}]({source['url']})"
                    )

            st.rerun()

        if clear_chat_button:
            st.session_state.chat_history = []
            st.session_state.chat_engine.clear_memory()
            st.rerun()

    # Tab 2: Summary Generation
    with tab2:
        st.subheader("📝 Generate Summaries")

        col1, col2 = st.columns(2)
        with col1:
            tone = st.selectbox(
                "Tone",
                ["casual", "formal", "eli5"],
                help="Choose how the summary should be written",
            )
        with col2:
            length = st.selectbox(
                "Length", ["short", "medium", "long"], help="Choose summary length"
            )

        if st.button("✨ Generate Summary", use_container_width=True):
            with st.spinner("Generating summary..."):
                summary = st.session_state.chat_engine.generate_summary(
                    tone=tone, length=length
                )

            st.markdown("### Summary")
            st.markdown(summary)

            # Download option
            st.download_button(
                label="💾 Download Summary",
                data=summary,
                file_name=f"summary_{tone}_{length}.txt",
                mime="text/plain",
            )

    # Tab 3: Source Comparison
    with tab3:
        st.subheader("🔍 Compare Sources")

        st.markdown("Analyze how different sources report on the same topic:")

        if st.button("🔬 Generate Comparison", use_container_width=True):
            with st.spinner("Analyzing sources..."):
                comparison = st.session_state.chat_engine.compare_sources()

            st.markdown("### Comparison Report")
            st.markdown(comparison)

            # Download option
            st.download_button(
                label="💾 Download Comparison",
                data=comparison,
                file_name="source_comparison.txt",
                mime="text/plain",
            )

    # Tab 4: Sentiment Analysis
    with tab4:
        st.subheader("📊 Sentiment Analysis")

        if st.button("🎭 Analyze Sentiment", use_container_width=True):
            with st.spinner("Analyzing sentiment..."):
                sentiments = st.session_state.chat_engine.analyze_sentiment()

            st.markdown("### Per-Source Sentiment")

            for sentiment in sentiments:
                with st.expander(f"📰 {sentiment['source']}", expanded=True):
                    st.markdown(sentiment["analysis"])

# Footer
st.divider()
st.markdown(
    """
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    Built with Streamlit • Powered by Ollama (Llama3.2 + Nomic Embed) • RAG Pipeline with FAISS
</div>
""",
    unsafe_allow_html=True,
)
