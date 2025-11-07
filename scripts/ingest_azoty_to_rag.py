"""
Ingest Grupa Azoty 2023 annual report into Qdrant RAG system
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.rag_service import ingest_annual_report

# Path to Azoty 2023 PDF
PDF_PATH = Path("data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2023.pdf")

if __name__ == "__main__":
    print("=" * 80)
    print("INGESTING GRUPA AZOTY 2023 ANNUAL REPORT INTO RAG SYSTEM")
    print("=" * 80)
    print()

    if not PDF_PATH.exists():
        print(f"❌ ERROR: PDF not found at {PDF_PATH}")
        sys.exit(1)

    print(f"PDF Path: {PDF_PATH}")
    print(f"Company: Grupa Azoty S.A.")
    print(f"Year: 2023")
    print(f"Chunk Size: 750 characters")
    print(f"Chunk Overlap: 100 characters")
    print(f"Vector Store: Qdrant (http://localhost:6333)")
    print(f"Collection: rag_documents")
    print()

    print("Starting ingestion...")
    print()

    success = ingest_annual_report(
        pdf_path=PDF_PATH,
        company="Grupa Azoty S.A.",
        year=2023,
        qdrant_url="http://localhost:6333"
    )

    if success:
        print()
        print("=" * 80)
        print("✅ INGESTION COMPLETE")
        print("=" * 80)
        print()
        print("Next step: Test RAG queries using scripts/test_rag_queries.py")
    else:
        print()
        print("❌ INGESTION FAILED")
        sys.exit(1)
