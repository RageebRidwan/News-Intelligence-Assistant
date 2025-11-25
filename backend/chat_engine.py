"""
Chat Engine Module - Conversational AI with Memory
Manages conversation flow, memory, and LLM interactions
"""

from langchain_ollama import ChatOllama
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain_classic.memory import ConversationBufferMemory
from typing import Dict, List
from backend import prompts


class ChatEngine:
    """
    Conversational AI engine with memory and context awareness
    """

    def __init__(self, rag_pipeline, model: str = "llama3.2"):
        """
        Initialize chat engine

        Args:
            rag_pipeline: Initialized RAGPipeline instance
            model: Ollama model name (default: llama3.2)
        """
        self.llm = ChatOllama(
            model=model,
            temperature=0.3,  # Lower temp for factual responses
        )

        self.rag_pipeline = rag_pipeline

        # Conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True, output_key="answer"
        )

        # Custom prompt template
        self.qa_prompt = PromptTemplate(
            input_variables=["context", "chat_history", "question"],
            template=prompts.QA_SYSTEM_PROMPT,
        )

    def ask(self, question: str) -> Dict:
        """
        Ask a question and get an answer with sources

        Args:
            question: User's question

        Returns:
            Dict with 'answer', 'sources', 'context_used'
        """
        # Get relevant context
        context_data = self.rag_pipeline.get_context_with_sources(question, k=5)

        # Format chat history
        chat_history = self._format_chat_history()

        # Generate prompt
        formatted_prompt = prompts.format_qa_prompt(
            context=context_data["context"],
            chat_history=chat_history,
            question=question,
        )

        # Get LLM response
        response = self.llm.invoke(formatted_prompt)
        answer = response.content

        # Save to memory
        self.memory.save_context({"input": question}, {"answer": answer})

        return {
            "answer": answer,
            "sources": context_data["sources"],
            "context_used": context_data["context"],
        }

    def compare_sources(self) -> str:
        """
        Generate a comparison analysis of all sources

        Returns:
            Formatted comparison report
        """
        if not self.rag_pipeline.documents:
            return "No sources to compare."

        # Get all sources
        sources = self.rag_pipeline.get_all_sources()

        # Compile content by source
        sources_content = []
        for source in sources:
            source_name = source["source"]
            # Get chunks from this source
            source_chunks = [
                doc.page_content
                for doc in self.rag_pipeline.documents
                if doc.metadata.get("source") == source_name
            ]
            content = "\n".join(source_chunks[:3])  # First 3 chunks per source
            sources_content.append(f"**{source_name}:**\n{content}\n")

        # Create source breakdown format
        source_breakdown = "\n".join(
            [f"- {s['source']}: {s['title']}" for s in sources]
        )

        # Generate comparison prompt
        prompt = prompts.format_comparison_prompt(
            sources_content="\n---\n".join(sources_content),
            source_breakdown=source_breakdown,
        )

        # Get LLM response
        response = self.llm.invoke(prompt)
        return response.content

    def generate_summary(self, tone: str = "casual", length: str = "medium") -> str:
        """
        Generate a summary of all content

        Args:
            tone: 'formal', 'casual', or 'eli5'
            length: 'short', 'medium', or 'long'

        Returns:
            Generated summary
        """
        if not self.rag_pipeline.documents:
            return "No content to summarize."

        # Combine all content
        all_content = "\n\n".join(
            [doc.page_content for doc in self.rag_pipeline.documents[:10]]
        )

        # Generate prompt
        prompt = prompts.format_summary_prompt(all_content, tone, length)

        # Get LLM response
        response = self.llm.invoke(prompt)
        return response.content

    def analyze_sentiment(self) -> List[Dict]:
        """
        Analyze sentiment for each source

        Returns:
            List of sentiment analyses per source
        """
        sources = self.rag_pipeline.get_all_sources()
        results = []

        for source in sources:
            source_name = source["source"]
            # Get content from this source
            source_chunks = [
                doc.page_content
                for doc in self.rag_pipeline.documents
                if doc.metadata.get("source") == source_name
            ]
            content = "\n".join(source_chunks[:2])  # First 2 chunks

            # Generate prompt
            prompt = prompts.format_sentiment_prompt(content, source_name)

            # Get analysis
            response = self.llm.invoke(prompt)

            results.append({"source": source_name, "analysis": response.content})

        return results

    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear()

    def _format_chat_history(self) -> str:
        """Format chat history for prompt"""
        try:
            messages = self.memory.load_memory_variables({})
            history = messages.get("chat_history", [])

            formatted = []
            for msg in history[-6:]:  # Last 3 exchanges (6 messages)
                role = "Human" if msg.type == "human" else "Assistant"
                formatted.append(f"{role}: {msg.content}")

            return "\n".join(formatted) if formatted else "No previous conversation"
        except:
            return "No previous conversation"


# Test
if __name__ == "__main__":
    from rag_pipeline import RAGPipeline

    # Initialize RAG (no API key needed!)
    rag = RAGPipeline()

    # Sample data
    sample_data = [
        {
            "content": "AI is transforming industries.",
            "url": "https://example.com",
            "title": "AI Revolution",
            "source_name": "example.com",
            "success": True,
        }
    ]

    rag.ingest_documents(sample_data)

    # Initialize chat
    chat = ChatEngine(rag)

    # Test query
    result = chat.ask("What is AI doing?")
    print(result["answer"])
