"""
RAG Service for intelligence analysis
Provides context-aware querying during report generation
"""

from typing import List, Dict, Any, Optional
import logging

from .qdrant_vector_store import QdrantVectorStore

logger = logging.getLogger(__name__)


class RAGService:
    """
    Service for RAG-enhanced queries during intelligence analysis
    Uses Qdrant with E5 embeddings and BGE reranker
    """

    def __init__(
        self,
        qdrant_url: str = "http://localhost:6333",
        use_reranker: bool = True
    ):
        self.vector_store = QdrantVectorStore(
            qdrant_url=qdrant_url,
            use_reranker=use_reranker
        )
        logger.info("RAGService initialized with Qdrant")

    def get_context_for_question(
        self,
        question: str,
        company: str,
        years: Optional[List[int]] = None,
        top_k: int = 3
    ) -> str:
        """
        Get relevant context from documents for a specific question

        Args:
            question: Analyst question (e.g., "Why did margins decline?")
            company: Company name
            years: Filter by specific years (None = all years)
            top_k: Number of chunks to retrieve

        Returns:
            Formatted context string with source citations
        """
        logger.info(f"RAG query: '{question}' for {company} (years={years})")

        all_results = []

        if years and len(years) > 1:
            # Query each year separately and combine
            for year in years:
                results = self.vector_store.search(
                    query=question,
                    company=company,
                    year=year,
                    top_k=max(1, top_k // len(years))
                )
                all_results.extend(results)

            # Sort by score
            all_results.sort(key=lambda x: x['score'], reverse=True)
            results = all_results[:top_k]

        elif years and len(years) == 1:
            # Single year
            results = self.vector_store.search(
                query=question,
                company=company,
                year=years[0],
                top_k=top_k
            )

        else:
            # All years
            results = self.vector_store.search(
                query=question,
                company=company,
                year=None,
                top_k=top_k
            )

        # Format context
        if not results:
            logger.warning(f"No relevant context found for: {question}")
            return "No relevant context found in documents."

        context_parts = []

        for i, result in enumerate(results, 1):
            source_file = result['metadata'].get('source_file', 'Unknown')
            page = result['metadata'].get('page', '?')
            year = result['metadata'].get('year', '?')
            section_type = result.get('section_type', 'unknown').replace('_', ' ').title()
            score = result['score']

            source_citation = f"[Source {i}: {source_file}, Year {year}, Page {page}, Section: {section_type}, Relevance: {score:.2f}]"
            content = result['content']

            context_parts.append(f"{source_citation}\n{content}")

        context = "\n\n---\n\n".join(context_parts)

        logger.info(f"Retrieved {len(results)} relevant chunks (avg score: {sum(r['score'] for r in results) / len(results):.3f})")

        return context

    def enhance_financial_analysis(
        self,
        metric: str,
        trend: str,
        company: str,
        years: List[int]
    ) -> str:
        """
        Get context to explain a financial metric trend

        Args:
            metric: Financial metric (e.g., "profitability", "liquidity")
            trend: Observed trend (e.g., "declining", "improving")
            company: Company name
            years: Years to search

        Returns:
            Context explaining the trend
        """
        question = f"Why did {metric} {trend}? What were the key drivers, challenges, and management explanations?"

        return self.get_context_for_question(question, company, years, top_k=3)

    def get_risk_context(
        self,
        risk_type: str,
        company: str,
        years: List[int]
    ) -> str:
        """
        Get context about specific risks

        Args:
            risk_type: Type of risk (e.g., "liquidity risk", "operational risk")
            company: Company name
            years: Years to search

        Returns:
            Context about the risk
        """
        question = f"What are the {risk_type} factors? What mitigation strategies are mentioned? What are the key concerns?"

        return self.get_context_for_question(question, company, years, top_k=3)

    def get_strategy_context(
        self,
        topic: str,
        company: str,
        years: List[int]
    ) -> str:
        """
        Get context about strategic initiatives

        Args:
            topic: Strategic topic (e.g., "growth strategy", "sustainability initiatives")
            company: Company name
            years: Years to search

        Returns:
            Context about strategy
        """
        question = f"What is the company's {topic}? What are the key initiatives, goals, and management priorities?"

        return self.get_context_for_question(question, company, years, top_k=3)

    def get_management_discussion(
        self,
        topic: str,
        company: str,
        years: List[int]
    ) -> str:
        """
        Get management discussion and analysis context

        Args:
            topic: Topic to search (e.g., "financial performance", "market conditions")
            company: Company name
            years: Years to search

        Returns:
            Context from MD&A sections
        """
        question = f"What does management say about {topic}? What explanations and outlook are provided?"

        return self.get_context_for_question(question, company, years, top_k=3)

    def is_data_available(self, company: str, year: Optional[int] = None) -> bool:
        """
        Check if RAG data is available for a company/year

        Args:
            company: Company name
            year: Optional year filter

        Returns:
            True if data exists
        """
        documents = self.vector_store.list_ingested_documents()

        for doc in documents:
            if doc['company'].lower() == company.lower():
                if year is None or doc['year'] == year:
                    return True

        return False

    def list_available_documents(self) -> List[Dict[str, Any]]:
        """
        List all documents in RAG system

        Returns:
            List of documents with metadata
        """
        return self.vector_store.list_ingested_documents()


# Helper function for easy ingestion
def ingest_annual_report(
    pdf_path,
    company: str,
    year: int,
    qdrant_url: str = "http://localhost:6333"
):
    """
    Ingest a single annual report into RAG system

    Args:
        pdf_path: Path to PDF
        company: Company name
        year: Year
        qdrant_url: Qdrant server URL
    """
    from .document_loader import DocumentLoader
    from .qdrant_vector_store import QdrantVectorStore

    logger.info(f"Ingesting {company} {year} report from {pdf_path}")

    # Load and chunk document (750 chars with 100 overlap)
    loader = DocumentLoader(chunk_size=750, chunk_overlap=100)
    chunks = loader.load_annual_report(pdf_path, company, year)

    if not chunks:
        logger.error("No chunks extracted from document")
        return False

    # Ingest into Qdrant
    vector_store = QdrantVectorStore(qdrant_url=qdrant_url)
    vector_store.ingest_documents(company, year, chunks)

    logger.info(f"✅ Ingested {len(chunks)} chunks for {company} ({year})")
    return True
