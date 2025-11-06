"""
Test Jina Embeddings on REAL Grupa Azoty Balance Sheet Rows

This tests semantic matching against actual text extracted from the PDF,
not idealized test data.
"""

from sentence_transformers import SentenceTransformer
from src.document_processing.pdf_parser import PDFParser
import numpy as np

def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def test_jina_on_real_azoty():
    print("=" * 80)
    print("JINA EMBEDDINGS: Real Grupa Azoty Balance Sheet Test")
    print("=" * 80)
    print()

    # Load Jina model
    print("Loading Jina model...")
    model = SentenceTransformer('jinaai/jina-embeddings-v2-base-en', trust_remote_code=True)
    print("✅ Model loaded")
    print()

    # Parse actual Grupa Azoty report
    print("Parsing Grupa Azoty 2024 report...")
    parser = PDFParser()
    doc = parser.parse('data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2024.pdf')
    print(f"✅ PDF parsed: {doc.num_pages} pages")
    print()

    if 'balance_sheet' not in doc.financial_statements:
        print("❌ Balance sheet not found!")
        return

    balance_sheet = doc.financial_statements['balance_sheet']
    print(f"Balance Sheet Location: Page {balance_sheet.page}")
    print(f"Rows in table: {len(balance_sheet.rows)}")
    print(f"Headers: {balance_sheet.headers}")
    print()

    # Query embeddings
    queries = {
        'total_assets': "total assets suma aktywów aktywa razem balance sheet total",
        'current_assets': "current assets aktywa obrotowe aktywa bieżące short-term assets",
        'equity': "equity kapitał własny shareholder equity",
        'revenue': "revenue przychody sales",
    }

    print("Computing query embeddings...")
    query_embeddings = {}
    for key, query_text in queries.items():
        query_embeddings[key] = model.encode(query_text, normalize_embeddings=True)
    print(f"✅ {len(query_embeddings)} query embeddings ready")
    print()

    print("-" * 80)
    print("SEMANTIC MATCHING ON REAL ROWS")
    print("-" * 80)
    print()

    threshold = 0.60
    matches_found = 0

    for i, row in enumerate(balance_sheet.rows):
        if not row:
            continue

        # Combine all non-empty cells in row
        row_text = ' '.join([str(cell) for cell in row if cell and str(cell).strip()])

        if not row_text or len(row_text) < 3:
            continue

        # Encode row
        try:
            row_embedding = model.encode(row_text, normalize_embeddings=True)
        except:
            continue

        # Find best match
        best_match = None
        best_score = threshold

        for key, query_embedding in query_embeddings.items():
            similarity = cosine_similarity(row_embedding, query_embedding)

            if similarity > best_score:
                best_score = similarity
                best_match = key

        if best_match:
            print(f"Row {i:2d}: {row_text[:70]}")
            print(f"  ✅ Matched: {best_match.replace('_', ' ').title()}")
            print(f"     Confidence: {best_score:.3f}")
            print(f"     Full row: {row}")
            print()
            matches_found += 1

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print(f"Total rows in balance sheet: {len(balance_sheet.rows)}")
    print(f"Non-empty rows: {sum(1 for r in balance_sheet.rows if any(cell for cell in r if cell))}")
    print(f"Matches found: {matches_found}")
    print()

    if matches_found > 0:
        print("✅ SUCCESS: Jina found semantic matches in real Azoty data!")
        print("   This proves the semantic matching works on actual Polish financial reports.")
    else:
        print("🟡 NO MATCHES: Jina didn't find matches (possible causes:)")
        print("   - Text quality issues in PDF extraction")
        print("   - Table structure too complex")
        print("   - Need to check individual row content")

    print()

    # Show sample of non-matched rows for debugging
    print("-" * 80)
    print("SAMPLE ROWS FOR DEBUGGING (first 10 non-empty):")
    print("-" * 80)
    count = 0
    for i, row in enumerate(balance_sheet.rows):
        row_text = ' '.join([str(cell) for cell in row if cell and str(cell).strip()])
        if row_text and len(row_text) > 3:
            print(f"Row {i:2d}: {row_text}")
            count += 1
            if count >= 10:
                break

if __name__ == "__main__":
    test_jina_on_real_azoty()
