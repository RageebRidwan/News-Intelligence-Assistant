"""
RAG Pipeline Module - Vector Store and Retrieval System
Uses Ollama embeddings + FAISS for semantic search
"""

from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List, Dict
import os


class RAGPipeline:
    """
    Retrieval-Augmented Generation pipeline
    Manages document ingestion, embedding, and retrieval
    """

    def __init__(self, model: str = "nomic-embed-text"):
        """
        Initialize RAG pipeline with Ollama embeddings

        Args:
            model: Ollama embedding model name (default: nomic-embed-text)
        """
        self.embeddings = OllamaEmbeddings(model=model)
        self.vector_store = None
        self.documents = []

        # Text splitter for chunking
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
        )

    def ingest_documents(self, scraped_data: List[Dict[str, str]]):
        """
        Process scraped content and create vector store

        Args:
            scraped_data: List of dicts from scraper with 'content', 'url', 'title', 'source_name'
        """
        # Convert scraped data to LangChain Documents
        documents = []
        for data in scraped_data:
            if data["success"] and data["content"]:
                # Create document with metadata
                doc = Document(
                    page_content=data["content"],
                    metadata={
                        "source": data["source_name"],
                        "url": data["url"],
                        "title": data["title"],
                    },
                )
                documents.append(doc)

        if not documents:
            raise ValueError("No valid documents to process")

        # Split documents into chunks
        self.documents = self.text_splitter.split_documents(documents)

        # Create vector store
        self.vector_store = FAISS.from_documents(self.documents, self.embeddings)

        print(
            f"✅ Ingested {len(documents)} documents, split into {len(self.documents)} chunks"
        )

    def retrieve_relevant_chunks(self, query: str, k: int = 5) -> List[Document]:
        """
        Retrieve most relevant chunks for a query

        Args:
            query: User's question
            k: Number of chunks to retrieve

        Returns:
            List of relevant Document chunks with metadata
        """
        if not self.vector_store:
            raise ValueError(
                "No documents ingested yet. Call ingest_documents() first."
            )

        # Semantic search
        relevant_docs = self.vector_store.similarity_search(query, k=k)
        return relevant_docs

    def get_context_with_sources(self, query: str, k: int = 5) -> Dict:
        """
        Get relevant context formatted with source attribution

        Args:
            query: User's question
            k: Number of chunks to retrieve

        Returns:
            Dict with 'context' (formatted string) and 'sources' (list of unique sources)
        """
        relevant_docs = self.retrieve_relevant_chunks(query, k)

        # Format context with source citations
        context_parts = []
        sources_seen = set()

        for i, doc in enumerate(relevant_docs, 1):
            source = doc.metadata.get("source", "Unknown")
            title = doc.metadata.get("title", "Unknown Title")
            url = doc.metadata.get("url", "")

            context_parts.append(
                f"[Source {i}: {source} - {title}]\n{doc.page_content}\n"
            )
            sources_seen.add((source, title, url))

        return {
            "context": "\n".join(context_parts),
            "sources": [
                {"source": s, "title": t, "url": u} for s, t, u in sources_seen
            ],
        }

    def get_all_sources(self) -> List[Dict]:
        """
        Get list of all ingested sources

        Returns:
            List of source metadata dicts
        """
        if not self.documents:
            return []

        sources = {}
        for doc in self.documents:
            source_name = doc.metadata.get("source", "Unknown")
            if source_name not in sources:
                sources[source_name] = {
                    "source": source_name,
                    "title": doc.metadata.get("title", "Unknown"),
                    "url": doc.metadata.get("url", ""),
                }

        return list(sources.values())


# Test function
if __name__ == "__main__":
    # Example usage (no API key needed with Ollama!)
    rag = RAGPipeline()

    # Sample data
    sample_data = [
        {
            "content": "This is a test article about AI.",
            "url": "https://example.com",
            "title": "AI Article",
            "source_name": "example.com",
            "success": True,
        }
    ]

    rag.ingest_documents(sample_data)
    results = rag.get_context_with_sources("Tell me about AI")
    print(results["context"])
