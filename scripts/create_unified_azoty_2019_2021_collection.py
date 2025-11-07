"""
Create unified Qdrant collection for Grupa Azoty 2019-2021 data

This script ingests all 6 PDFs (2 per year) into one unified collection
for proper benchmark comparison.
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

# PDF files with their years
PDF_FILES = [
    ("data/documents/input/Grupa_Azoty_Financial_Statements_2019.pdf", 2019),
    ("data/documents/input/Grupa_Azoty_Directors_Report_2019.pdf", 2019),
    ("data/documents/input/Grupa_Azoty_Financial_Statements_2020.pdf", 2020),
    ("data/documents/input/Grupa_Azoty_Directors_Report_2020.pdf", 2020),
    ("data/documents/input/Grupa_Azoty_Financial_Statements_2021.pdf", 2021),
    ("data/documents/input/Grupa_Azoty_Directors_Report_2021.pdf", 2021),
]

COMPANY = "Grupa Azoty"
COLLECTION_NAME = "azoty_2019_2021_multi_year"


def main():
    """Ingest all 2019-2021 PDFs into unified collection"""

    print("=" * 80)
    print("CREATING UNIFIED COLLECTION: azoty_2019_2021_multi_year")
    print("=" * 80)
    print()
    print(f"Company: {COMPANY}")
    print(f"Years: 2019-2021")
    print(f"PDFs: {len(PDF_FILES)}")
    print(f"Collection: {COLLECTION_NAME}")
    print()

    # Initialize document loader and vector store
    loader = DocumentLoader(chunk_size=750, chunk_overlap=100)
    vector_store = QdrantVectorStore(
        collection_name=COLLECTION_NAME,
        qdrant_url="http://localhost:6333",
        use_reranker=True
    )

    logger.info(f"Collection initialized: {COLLECTION_NAME}")

    total_chunks = 0
    ingestion_results = []

    for pdf_path, year in PDF_FILES:
        pdf_file = Path(pdf_path)

        if not pdf_file.exists():
            logger.error(f"PDF not found: {pdf_path}")
            continue

        print(f"\n{'-' * 80}")
        print(f"Processing: {pdf_file.name} ({year})")
        print(f"{'-' * 80}")

        try:
            # Load PDF into chunks
            chunks = loader.load_annual_report(
                pdf_path=pdf_file,
                company=COMPANY,
                year=year
            )

            # Ingest chunks into Qdrant
            vector_store.ingest_documents(
                company=COMPANY,
                year=year,
                chunks=chunks
            )

            chunk_count = len(chunks)
            total_chunks += chunk_count

            ingestion_results.append({
                "year": year,
                "file": pdf_file.name,
                "status": "success",
                "chunks": chunk_count
            })

            print(f"✅ {year} {pdf_file.name}: Ingested {chunk_count:,} chunks")

        except Exception as e:
            logger.error(f"❌ {year} {pdf_file.name}: Ingestion failed - {e}")
            import traceback
            traceback.print_exc()
            ingestion_results.append({
                "year": year,
                "file": pdf_file.name,
                "status": "failed",
                "chunks": 0,
                "error": str(e)
            })

    # Summary
    print(f"\n{'=' * 80}")
    print(f"INGESTION COMPLETE")
    print(f"{'=' * 80}")
    print()

    success_count = sum(1 for r in ingestion_results if r["status"] == "success")
    failed_count = sum(1 for r in ingestion_results if r["status"] == "failed")

    print(f"Total PDFs: {len(PDF_FILES)}")
    print(f"✅ Successfully ingested: {success_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"📊 Total chunks: {total_chunks:,}")
    print(f"🗄️  Collection: {COLLECTION_NAME}")
    print()

    # Detailed results
    print("Results by year:")
    for result in ingestion_results:
        status_icon = "✅" if result["status"] == "success" else "❌"
        year = result["year"]
        chunks = result["chunks"]
        file = result["file"]

        if result["status"] == "success":
            print(f"  {status_icon} {year}: {chunks:,} chunks - {file}")
        else:
            error = result.get("error", "Unknown error")
            print(f"  {status_icon} {year}: FAILED - {file}")
            print(f"      Error: {error}")

    print()
    print(f"✅ Collection ready for benchmark testing!")
    print()


if __name__ == "__main__":
    main()
