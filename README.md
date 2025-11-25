# 🧠 Multi-Source Intelligence Assistant

A powerful **RAG-powered** (Retrieval-Augmented Generation) content analysis system that enables intelligent questioning, summarization, and comparison of multiple web sources. Built with Streamlit, LangChain, and Ollama for completely **local AI inference** - no API keys required!

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.51+-red.svg)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.4+-green.svg)](https://langchain.com)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-orange.svg)](https://ollama.ai)

---

## 🎯 Features

### 📊 Analysis Tools
- **Multi-source web scraping** - Extract content from any webpage with intelligent parsing
- **RAG-based question answering** - Ask questions across multiple sources with semantic search
- **Source comparison & synthesis** - Analyze how different sources report on the same topic
- **Conversational memory** - Context-aware conversations that remember previous exchanges

### 🎨 Content Generation
- **Smart summaries** - Generate summaries in 3 tones (casual, formal, ELI5) and 3 lengths (short, medium, long)
- **Sentiment analysis** - Per-source sentiment and emotional tone analysis
- **Citation tracking** - Automatic source attribution for all responses
- **Context-aware responses** - Uses RAG to ground answers in your ingested content

---

## 📸 Screenshots

### Welcome Screen
![Welcome Screen](screenshots/welcome.jpg)

### Data Ingestion
![Data Ingestion](screenshots/ingestion.jpg)

### Chat Interface
![Chat Interface](screenshots/chat.jpg)

### Summary Generation
![Summary Generation](screenshots/summary.jpg)

### Source Comparison
![Source Comparison](screenshots/comparison.jpg)

### Sentiment Analysis
![Sentiment Analysis](screenshots/sentiment-analysis.jpg)

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **Ollama** ([Download here](https://ollama.ai))
- **Git**

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/RageebRidwan/News-Intelligence-Assistant.git
   cd News-Intelligence-Assistant
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Pull required Ollama models**
   ```bash
   ollama pull llama3.2
   ollama pull nomic-embed-text
   ```

5. **Start Ollama** (keep it running in the background)
   ```bash
   ollama serve
   ```

6. **Run the application**
   ```bash
   streamlit run frontend/app.py
   ```

7. **Open your browser** to `http://localhost:8501`

---

## 📁 Project Structure

```
news-intelligence-assistant/
│
├── backend/
│   ├── __init__.py
│   ├── scraper.py           # Web scraping module
│   ├── rag_pipeline.py      # RAG & vector store management
│   ├── chat_engine.py       # Conversational AI engine
│   └── prompts.py           # Prompt engineering templates
│
├── frontend/
│   └── app.py               # Streamlit UI
│
├── screenshots/             # Application screenshots
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Frontend** | Streamlit |
| **LLM Framework** | LangChain |
| **Local LLM** | Ollama (Llama 3.2) |
| **Embeddings** | Nomic Embed Text |
| **Vector Store** | FAISS |
| **Web Scraping** | BeautifulSoup4 + Requests |
| **Language** | Python 3.11+ |

---

## 💡 How It Works

1. **Scrape Content**: Enter URLs in the sidebar, and the system extracts main content from each webpage
2. **Build Knowledge Base**: Content is chunked, embedded using Nomic Embed, and stored in a FAISS vector database
3. **Semantic Search**: When you ask questions, the system retrieves the most relevant chunks using similarity search
4. **Generate Responses**: Llama 3.2 uses the retrieved context to generate accurate, cited answers
5. **Maintain Context**: Conversation memory allows for multi-turn dialogues with context awareness

---

## 🎓 Use Cases

- **Research**: Quickly analyze and compare multiple articles on the same topic
- **News Analysis**: Get different perspectives on current events from various sources
- **Content Curation**: Summarize long-form content in different styles
- **Fact Checking**: Compare claims across multiple sources
- **Sentiment Tracking**: Understand emotional framing of topics across sources

---

## 🔒 Privacy & Security

- **100% Local**: All AI inference happens locally via Ollama - no data sent to external APIs
- **No API Keys Required**: Unlike cloud-based LLMs, this runs entirely on your machine
- **Your Data Stays Yours**: Scraped content and vector stores remain on your local system

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

---

## 📝 License

This project is open source and available under the MIT License.

---

## 👤 Author

**Rageeb Ridwan**

- GitHub: [@RageebRidwan](https://github.com/RageebRidwan)
- Project Link: [https://github.com/RageebRidwan/News-Intelligence-Assistant](https://github.com/RageebRidwan/News-Intelligence-Assistant)

---

## 🙏 Acknowledgments

- **Ollama** - For making local LLMs accessible
- **LangChain** - For the RAG framework
- **Streamlit** - For the amazing UI framework
- **FAISS** - For efficient vector search

---

## 📧 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

<div align="center">

**Built with ❤️ using Local AI**

*No API keys. No cloud. Just pure local intelligence.*

</div>
