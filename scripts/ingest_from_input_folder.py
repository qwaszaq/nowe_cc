"""
Ingest PDFs from input folder into Qdrant for RAG
Auto-detects company name and year from PDF filenames

Usage:
1. Drop PDFs in data/documents/input/ with naming format:
   - CompanyName_Report_YYYY.pdf
   - CompanyName_YYYY.pdf
   - Or any format with company name and year

2. Run: python3 scripts/ingest_from_input_folder.py

3. Script will:
   - Auto-detect company and year from filename
   - Create collection: company_name_multi_year
   - Ingest all PDFs for that company
"""

import sys
from pathlib import Path
import re
sys.path.append(str(Path(__file__).parent.parent))

from src.rag.document_loader import DocumentLoader
from src.rag.qdrant_vector_store import QdrantVectorStore
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def extract_company_and_year(filename: str) -> tuple:
    """
    Extract company name and year from filename - FLEXIBLE format

    Works with ANY filename - extracts year if present, uses full filename as company name

    Examples:
    - "report.pdf" → ("report", None)
    - "company_2024.pdf" → ("company", 2024)
    - "Grupa Azoty Directors Report 2024.pdf" → ("Grupa Azoty Directors Report", 2024)
    - "anything_you_want.pdf" → ("anything_you_want", None)

    Returns:
        tuple: (company_name, year) - year can be None
    """
    # Remove file extension
    name = filename.rsplit('.', 1)[0]  # Handles .pdf, .PDF, any extension

    # Try to extract year (4 digits between 1900-2099)
    year = None
    year_match = re.search(r'\b(19\d{2}|20\d{2})\b', name)
    if year_match:
        year = int(year_match.group(1))
        # Remove year from company name
        company_name = name[:year_match.start()].strip() + name[year_match.end():].strip()
    else:
        company_name = name

    # Clean up company name
    # Remove extra spaces, underscores, dashes
    company_name = re.sub(r'[_-]+', ' ', company_name)  # Replace _ or - with space
    company_name = re.sub(r'\s+', ' ', company_name)    # Collapse multiple spaces
    company_name = company_name.strip()

    # If empty after cleaning, use original filename
    if not company_name:
        company_name = name

    return company_name, year


def group_pdfs_by_company(input_dir: Path) -> dict:
    """
    Group PDFs by company name

    Returns:
        dict: {company_name: [(pdf_path, year), ...]}
    """
    companies = {}

    for pdf_path in input_dir.glob('*'):
        # Accept any file type (PDF, DOCX, TXT, etc.)
        if pdf_path.is_dir():
            continue

        company, year = extract_company_and_year(pdf_path.name)

        # Company name always extracted (uses filename if nothing else)
        if company not in companies:
            companies[company] = []

        companies[company].append((pdf_path, year))

    return companies


def ingest_company_pdfs(company_name: str, pdf_list: list):
    """
    Ingest all PDFs for a specific company

    Args:
        company_name: Company name (e.g., "Grupa Azoty")
        pdf_list: List of (pdf_path, year) tuples
    """
    print(f"\n{'=' * 80}")
    print(f"INGESTING COMPANY: {company_name}")
    print(f"{'=' * 80}")
    print(f"Found {len(pdf_list)} PDF(s)")
    print()

    # Sort by year
    pdf_list_sorted = sorted(pdf_list, key=lambda x: x[1])

    # Create collection name (company_name_multi_year)
    collection_name = f"{company_name.lower().replace(' ', '_')}_multi_year"

    print(f"Collection name: {collection_name}")
    print(f"Years: {', '.join(str(year) for _, year in pdf_list_sorted)}")
    print()

    # Initialize document loader and vector store
    loader = DocumentLoader(chunk_size=750, chunk_overlap=100)
    vector_store = QdrantVectorStore(
        collection_name=collection_name,
        qdrant_url="http://localhost:6333",
        use_reranker=True
    )

    logger.info(f"Collection initialized: {collection_name}")

    # Load and ingest all reports
    total_chunks = 0
    ingestion_results = []

    for pdf_path, year in pdf_list_sorted:
        print(f"\n{'-' * 80}")
        print(f"Ingesting {year} - {pdf_path.name}")
        print(f"{'-' * 80}")

        try:
            # Load PDF into chunks
            chunks = loader.load_annual_report(
                pdf_path=pdf_path,
                company=company_name,
                year=year
            )

            # Ingest chunks into Qdrant
            vector_store.ingest_documents(
                company=company_name,
                year=year,
                chunks=chunks
            )

            chunk_count = len(chunks)
            total_chunks += chunk_count

            ingestion_results.append({
                "year": year,
                "file": pdf_path.name,
                "status": "success",
                "chunks": chunk_count
            })

            print(f"✅ {year} {pdf_path.name}: Ingested {chunk_count} chunks")

        except Exception as e:
            logger.error(f"❌ {year} {pdf_path.name}: Ingestion failed - {e}")
            import traceback
            traceback.print_exc()
            ingestion_results.append({
                "year": year,
                "file": pdf_path.name,
                "status": "failed",
                "chunks": 0,
                "error": str(e)
            })

    # Summary for this company
    print(f"\n{'=' * 80}")
    print(f"INGESTION SUMMARY: {company_name}")
    print(f"{'=' * 80}")
    print()

    success_count = sum(1 for r in ingestion_results if r["status"] == "success")
    failed_count = sum(1 for r in ingestion_results if r["status"] == "failed")

    print(f"Total PDFs: {len(pdf_list_sorted)}")
    print(f"✅ Successfully ingested: {success_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"📊 Total chunks: {total_chunks:,}")
    print(f"🗄️  Collection: {collection_name}")
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

    return {
        "company": company_name,
        "collection": collection_name,
        "total_pdfs": len(pdf_list_sorted),
        "total_chunks": total_chunks,
        "success_count": success_count,
        "failed_count": failed_count,
        "results": ingestion_results
    }


def main():
    """Main ingestion workflow"""
    print("=" * 80)
    print("AUTOMATED PDF INGESTION FROM INPUT FOLDER")
    print("=" * 80)
    print()

    input_dir = Path("data/documents/input")

    # Check if input directory exists
    if not input_dir.exists():
        print(f"❌ Input directory not found: {input_dir}")
        print(f"   Creating directory...")
        input_dir.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {input_dir}")
        print()
        print(f"📝 Usage:")
        print(f"   1. Copy PDFs to: {input_dir}/")
        print(f"   2. Filename format: CompanyName_Report_YYYY.pdf")
        print(f"   3. Run this script again")
        print()
        return

    # Find all documents (any file type)
    doc_files = [f for f in input_dir.iterdir() if f.is_file()]

    if not doc_files:
        print(f"📂 Input directory: {input_dir}")
        print(f"❌ No files found")
        print()
        print(f"📝 Usage:")
        print(f"   1. Copy documents to: {input_dir}/")
        print(f"   2. ANY filename works! Examples:")
        print(f"      - report.pdf")
        print(f"      - Company Report 2024.pdf")
        print(f"      - annual_report.docx")
        print(f"      - financial-data.txt")
        print()
        print(f"   📌 Year optional: If filename contains YYYY (1900-2099), it will be extracted")
        print()
        return

    print(f"📂 Input directory: {input_dir}")
    print(f"📄 Found {len(doc_files)} file(s)")
    print()

    # Group documents by company
    companies = group_pdfs_by_company(input_dir)

    if not companies:
        print("❌ No documents could be processed")
        return

    print(f"🏢 Detected {len(companies)} company(ies):")
    for company, pdfs in companies.items():
        years = [year for _, year in pdfs if year is not None]
        if years:
            years_sorted = sorted(years)
            year_range = f"covering {min(years_sorted)}-{max(years_sorted)}" if len(years_sorted) > 1 else f"year {years_sorted[0]}"
        else:
            year_range = "no year specified"
        print(f"   - {company}: {len(pdfs)} file(s) {year_range}")
    print()

    # Ask for confirmation
    response = input("Proceed with ingestion? (y/n): ")
    if response.lower() != 'y':
        print("Ingestion cancelled.")
        return

    print()

    # Ingest each company
    all_results = []
    for company, pdfs in companies.items():
        result = ingest_company_pdfs(company, pdfs)
        all_results.append(result)

    # Final summary
    print("=" * 80)
    print("OVERALL SUMMARY")
    print("=" * 80)
    print()

    total_pdfs = sum(r["total_pdfs"] for r in all_results)
    total_chunks = sum(r["total_chunks"] for r in all_results)
    total_success = sum(r["success_count"] for r in all_results)
    total_failed = sum(r["failed_count"] for r in all_results)

    print(f"Companies processed: {len(all_results)}")
    print(f"Total PDFs: {total_pdfs}")
    print(f"✅ Successfully ingested: {total_success}")
    print(f"❌ Failed: {total_failed}")
    print(f"📊 Total chunks: {total_chunks:,}")
    print()

    print("Collections created:")
    for result in all_results:
        print(f"  - {result['collection']} ({result['total_chunks']:,} chunks)")
    print()

    print("✅ Ingestion complete!")
    print()
    print("Next steps:")
    print("  1. Test RAG retrieval with your collection")
    print("  2. Generate intelligence reports:")
    print("     python3 scripts/test_multi_agent_multi_year.py")
    print()


if __name__ == "__main__":
    main()
