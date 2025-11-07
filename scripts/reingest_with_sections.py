"""
Reingest Grupa Azoty 2023 with section detection
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.qdrant_vector_store import QdrantVectorStore
from src.rag.rag_service import ingest_annual_report

# Path to Azoty 2023 PDF
PDF_PATH = Path("data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2023.pdf")

if __name__ == "__main__":
    print("=" * 80)
    print("REINGESTING WITH SECTION DETECTION")
    print("=" * 80)
    print()

    # Delete old data
    print("Deleting old documents...")
    vector_store = QdrantVectorStore(qdrant_url="http://localhost:6333")
    vector_store.delete_documents("Grupa Azoty S.A.", 2023)
    print("✓ Old documents deleted")
    print()

    # Reingest
    print("Reingesting with section detection...")
    success = ingest_annual_report(
        pdf_path=PDF_PATH,
        company="Grupa Azoty S.A.",
        year=2023,
        qdrant_url="http://localhost:6333"
    )

    if success:
        print()
        print("=" * 80)
        print("✅ REINGESTION COMPLETE WITH SECTION METADATA")
        print("=" * 80)
    else:
        print()
        print("❌ REINGESTION FAILED")
        sys.exit(1)
