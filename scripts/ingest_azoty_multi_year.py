"""
Ingest 3 years of Azoty annual reports into Qdrant for RAG
Phase 3: RAG System Preparation for multi-year analysis
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.rag.document_loader import DocumentLoader
from src.rag.qdrant_vector_store import QdrantVectorStore
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def ingest_multi_year_reports():
    """
    Ingest 6 PDFs (3 years × 2 reports each) into Qdrant
    """
    print("=" * 80)
    print("MULTI-YEAR PDF INGESTION INTO RAG SYSTEM")
    print("Grupa Azoty S.A. - 2022, 2023, 2024")
    print("=" * 80)
    print()

    # Initialize document loader and vector store
    loader = DocumentLoader(chunk_size=750, chunk_overlap=100)
    vector_store = QdrantVectorStore(
        collection_name="azoty_multi_year",
        qdrant_url="http://localhost:6333",
        use_reranker=True
    )

    # PDF paths
    pdf_dir = Path("data/documents/grupa_azoty")

    reports = [
        {
            "year": 2022,
            "type": "financial_statements",
            "path": pdf_dir / "Grupa_Azoty_Consolidated_Financial_Statements_2022.pdf"
        },
        {
            "year": 2022,
            "type": "directors_report",
            "path": pdf_dir / "Grupa_Azoty_Directors_Report_2022.pdf"
        },
        {
            "year": 2023,
            "type": "financial_statements",
            "path": pdf_dir / "Grupa_Azoty_Consolidated_Financial_Statements_2023.pdf"
        },
        {
            "year": 2023,
            "type": "directors_report",
            "path": pdf_dir / "Grupa_Azoty_Directors_Report_2023.pdf"
        },
        {
            "year": 2024,
            "type": "financial_statements",
            "path": pdf_dir / "Grupa_Azoty_Consolidated_Financial_Statements_2024.pdf"
        },
        {
            "year": 2024,
            "type": "directors_report",
            "path": pdf_dir / "Grupa_Azoty_Directors_Report_2024.pdf"
        }
    ]

    # Collection is created automatically in QdrantVectorStore __init__
    logger.info("Collection initialized: azoty_multi_year")

    # Load and ingest all reports
    total_chunks = 0
    ingestion_results = []

    for report in reports:
        year = report["year"]
        doc_type = report["type"]
        pdf_path = report["path"]

        if not pdf_path.exists():
            logger.warning(f"❌ {year} {doc_type}: File not found - {pdf_path}")
            ingestion_results.append({
                "year": year,
                "type": doc_type,
                "status": "missing",
                "chunks": 0
            })
            continue

        print(f"\n{'=' * 80}")
        print(f"Ingesting {year} - {doc_type}")
        print(f"File: {pdf_path.name}")
        print(f"{'=' * 80}")

        try:
            # Load PDF into chunks
            chunks = loader.load_annual_report(
                pdf_path=pdf_path,
                company="Grupa Azoty S.A.",
                year=year
            )

            # Add document type to metadata
            for chunk in chunks:
                chunk.metadata["document_type"] = doc_type

            # Ingest chunks into Qdrant (requires company, year, chunks)
            vector_store.ingest_documents(
                company="Grupa Azoty S.A.",
                year=year,
                chunks=chunks
            )

            chunk_count = len(chunks)
            total_chunks += chunk_count

            ingestion_results.append({
                "year": year,
                "type": doc_type,
                "status": "success",
                "chunks": chunk_count
            })

            print(f"✅ {year} {doc_type}: Ingested {chunk_count} chunks")

        except Exception as e:
            logger.error(f"❌ {year} {doc_type}: Ingestion failed - {e}")
            import traceback
            traceback.print_exc()
            ingestion_results.append({
                "year": year,
                "type": doc_type,
                "status": "failed",
                "chunks": 0,
                "error": str(e)
            })

    # Summary
    print(f"\n{'=' * 80}")
    print("INGESTION SUMMARY")
    print(f"{'=' * 80}")
    print()
    print(f"Total chunks ingested: {total_chunks}")
    print()

    print("By Year and Type:")
    for result in ingestion_results:
        status_icon = "✅" if result["status"] == "success" else "❌"
        print(f"  {status_icon} {result['year']} - {result['type']}: {result['chunks']} chunks")

    # Test retrieval
    print(f"\n{'=' * 80}")
    print("TESTING RETRIEVAL")
    print(f"{'=' * 80}")
    print()

    test_queries = [
        "Why did profitability decline from 2022 to 2024?",
        "What are the main financial risks facing the company?",
        "What is management's strategy to improve performance?"
    ]

    for query in test_queries:
        print(f"\nQuery: \"{query}\"")
        print("-" * 80)

        results = vector_store.search(
            query=query,
            top_k=3,
            company="Grupa Azoty S.A."
        )

        for i, result in enumerate(results, 1):
            print(f"\n  Result {i} (score: {result['score']:.3f}):")
            print(f"    Year: {result['metadata'].get('year', 'N/A')}")
            print(f"    Type: {result['metadata'].get('document_type', 'N/A')}")
            print(f"    Content preview: {result['content'][:200]}...")

    print(f"\n{'=' * 80}")
    print("✅ RAG INGESTION COMPLETE")
    print(f"{'=' * 80}")
    print()
    print("Next Step: Generate analysis reports")
    print("  1. Single-agent: python3 scripts/test_single_agent_multi_year.py")
    print("  2. Multi-agent: python3 scripts/test_multi_agent_multi_year.py")
    print("  3. Claude: python3 scripts/generate_claude_multi_year.py")
    print(f"{'=' * 80}")

    return {
        "total_chunks": total_chunks,
        "results": ingestion_results
    }


if __name__ == "__main__":
    try:
        result = ingest_multi_year_reports()
    except Exception as e:
        logger.error(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
