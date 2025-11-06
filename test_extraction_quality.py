"""
Extraction Quality Test: E5 + Camelot on Real Azoty Data

Tests the complete extraction pipeline and reports quality metrics.
"""

import sys
sys.path.insert(0, '.')

from src.document_processing.pdf_parser import PDFParser
from agents.analytical.alex_agent_llm import AlexAgentLLM
import requests
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_e5_embedding(text: str, lm_studio_url: str = "http://192.168.200.226:1234"):
    try:
        response = requests.post(
            f"{lm_studio_url}/v1/embeddings",
            json={"model": "intfloat/e5-large-v2", "input": text},
            timeout=10
        )
        if response.status_code == 200:
            embedding = np.array(response.json()['data'][0]['embedding'])
            return embedding / np.linalg.norm(embedding)
    except:
        pass
    return None

def test_extraction_quality():
    print("=" * 80)
    print("EXTRACTION QUALITY TEST: E5 + Camelot on Real Azoty Data")
    print("=" * 80)
    print()

    # Step 1: Parse PDF with Camelot
    print("STEP 1: PDF PARSING (Camelot Fallback)")
    print("-" * 80)

    parser = PDFParser()
    doc = parser.parse('data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2024.pdf')

    print(f"✅ PDF parsed: {doc.num_pages} pages")
    print(f"   Tables found: {len(doc.tables)}")
    print(f"   Financial statements: {list(doc.financial_statements.keys())}")
    print()

    if 'balance_sheet' not in doc.financial_statements:
        print("❌ Balance sheet not found!")
        return

    balance_sheet = doc.financial_statements['balance_sheet']
    print(f"Balance Sheet: Page {balance_sheet.page}, {len(balance_sheet.rows)} rows")
    print()

    # Step 2: Check data quality
    print("STEP 2: DATA QUALITY ASSESSMENT")
    print("-" * 80)

    total_cells = 0
    empty_cells = 0
    cells_with_numbers = 0

    for row in balance_sheet.rows:
        for cell in row:
            total_cells += 1
            cell_str = str(cell).strip()

            if not cell_str:
                empty_cells += 1
            elif any(char.isdigit() for char in cell_str):
                cells_with_numbers += 1

    empty_pct = (empty_cells / total_cells * 100) if total_cells > 0 else 0
    numeric_pct = (cells_with_numbers / total_cells * 100) if total_cells > 0 else 0

    print(f"Total cells: {total_cells}")
    print(f"Empty cells: {empty_cells} ({empty_pct:.1f}%)")
    print(f"Cells with numbers: {cells_with_numbers} ({numeric_pct:.1f}%)")
    print()

    if numeric_pct > 10:
        print(f"✅ GOOD EXTRACTION: {numeric_pct:.1f}% of cells have numeric data")
    elif numeric_pct > 5:
        print(f"🟡 FAIR EXTRACTION: {numeric_pct:.1f}% of cells have numeric data")
    else:
        print(f"❌ POOR EXTRACTION: Only {numeric_pct:.1f}% of cells have numeric data")

    print()

    # Step 3: Sample rows
    print("STEP 3: SAMPLE ROWS (First 10 Non-Empty)")
    print("-" * 80)

    sample_count = 0
    for i, row in enumerate(balance_sheet.rows):
        row_text = ' '.join([str(cell) for cell in row if cell and str(cell).strip()])
        if row_text and len(row_text) > 3:
            print(f"Row {i:2d}: {row_text[:100]}")
            sample_count += 1
            if sample_count >= 10:
                break

    print()

    # Step 4: E5 Semantic Matching
    print("STEP 4: E5 SEMANTIC MATCHING")
    print("-" * 80)

    # Load E5 query embeddings
    queries = {
        'total_assets': "total assets suma aktywów aktywa razem balance sheet total",
        'current_assets': "current assets aktywa obrotowe aktywa bieżące short-term assets",
        'fixed_assets': "fixed assets aktywa trwałe non-current assets",
        'current_liabilities': "current liabilities zobowiązania krótkoterminowe",
        'equity': "equity kapitał własny shareholder equity",
        'cash': "cash środki pieniężne cash equivalents",
    }

    query_embeddings = {}
    for key, query_text in queries.items():
        emb = get_e5_embedding(query_text)
        if emb is not None:
            query_embeddings[key] = emb

    print(f"Loaded {len(query_embeddings)} E5 query embeddings")
    print()

    threshold = 0.65
    matches_found = 0

    for i, row in enumerate(balance_sheet.rows):
        row_text = ' '.join([str(cell) for cell in row if cell and str(cell).strip()])
        if not row_text or len(row_text) < 3:
            continue

        row_embedding = get_e5_embedding(row_text)
        if row_embedding is None:
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
            print(f"  ✅ Matched: {best_match.replace('_', ' ').title()} (confidence: {best_score:.3f})")
            print(f"  Full row: {row}")
            print()
            matches_found += 1

            if matches_found >= 5:  # Show first 5 matches
                break

    print(f"E5 matches found: {matches_found}")
    print()

    # Step 5: Numeric Extraction Test
    print("STEP 5: NUMERIC EXTRACTION TEST")
    print("-" * 80)

    # Use Alex's parser
    def parse_polish_number(text):
        """Parse Polish number format"""
        import re
        if not text or not isinstance(text, str):
            return None

        # Clean and convert
        text = text.strip()
        # Remove currency and units
        text = re.sub(r'(PLN|EUR|USD|zł|tys\.?|mln\.?|mld\.?)', '', text)
        # Remove parentheses (used for negatives)
        is_negative = '(' in text
        text = text.replace('(', '').replace(')', '')
        # Space as thousand separator, comma as decimal
        text = text.replace(' ', '').replace(',', '.')

        try:
            value = float(text)
            return -value if is_negative else value
        except:
            return None

    extracted_numbers = []

    for row in balance_sheet.rows:
        row_text = ' '.join([str(cell) for cell in row if cell and str(cell).strip()])
        if not row_text:
            continue

        for cell in row:
            value = parse_polish_number(str(cell))
            if value is not None and abs(value) > 1:  # Filter out small values
                extracted_numbers.append((row_text[:50], value))
                break  # One number per row

    print(f"Numbers extracted: {len(extracted_numbers)}")
    if extracted_numbers:
        print("\nSample extracted numbers:")
        for text, value in extracted_numbers[:10]:
            print(f"  {text:50s} → {value:>12,.2f}")

    print()

    # FINAL SUMMARY
    print("=" * 80)
    print("EXTRACTION QUALITY SUMMARY")
    print("=" * 80)
    print()

    print("📊 METRICS:")
    print(f"   Tables extracted: {len(doc.tables)}")
    print(f"   Balance sheet rows: {len(balance_sheet.rows)}")
    print(f"   Numeric cell density: {numeric_pct:.1f}%")
    print(f"   E5 semantic matches: {matches_found}")
    print(f"   Numbers extracted: {len(extracted_numbers)}")
    print()

    print("🎯 QUALITY ASSESSMENT:")
    print()

    score = 0
    max_score = 5

    # Criterion 1: Numeric density
    if numeric_pct > 15:
        print("  ✅ Numeric Density: Excellent (>15%)")
        score += 1
    elif numeric_pct > 5:
        print("  🟡 Numeric Density: Fair (5-15%)")
        score += 0.5
    else:
        print("  ❌ Numeric Density: Poor (<5%)")

    # Criterion 2: E5 matches
    if matches_found >= 5:
        print("  ✅ E5 Semantic Matching: Working (5+ matches)")
        score += 1
    elif matches_found >= 2:
        print("  🟡 E5 Semantic Matching: Partial (2-4 matches)")
        score += 0.5
    else:
        print("  ❌ E5 Semantic Matching: Failed (<2 matches)")

    # Criterion 3: Number extraction
    if len(extracted_numbers) >= 10:
        print("  ✅ Number Extraction: Excellent (10+ numbers)")
        score += 1
    elif len(extracted_numbers) >= 5:
        print("  🟡 Number Extraction: Fair (5-9 numbers)")
        score += 0.5
    else:
        print("  ❌ Number Extraction: Poor (<5 numbers)")

    # Criterion 4: Balance sheet found
    if 'balance_sheet' in doc.financial_statements:
        print("  ✅ Balance Sheet Detection: Success")
        score += 1
    else:
        print("  ❌ Balance Sheet Detection: Failed")

    # Criterion 5: Rows with data
    non_empty_rows = sum(1 for r in balance_sheet.rows if any(cell and str(cell).strip() for cell in r))
    if non_empty_rows >= 20:
        print(f"  ✅ Row Count: Good ({non_empty_rows} non-empty rows)")
        score += 1
    elif non_empty_rows >= 10:
        print(f"  🟡 Row Count: Fair ({non_empty_rows} non-empty rows)")
        score += 0.5
    else:
        print(f"  ❌ Row Count: Low ({non_empty_rows} non-empty rows)")

    print()
    print(f"📈 OVERALL SCORE: {score}/{max_score} ({score/max_score*100:.0f}%)")
    print()

    if score >= 4:
        print("✅ EXCELLENT: Extraction quality is production-ready")
        print("   Recommendation: Proceed to Phase 3 (Learning System)")
    elif score >= 3:
        print("🟡 GOOD: Extraction works but needs refinement")
        print("   Recommendation: Debug specific extraction issues")
    elif score >= 2:
        print("🟠 FAIR: Extraction partially works")
        print("   Recommendation: Consider alternative extraction methods")
    else:
        print("❌ POOR: Extraction quality insufficient")
        print("   Recommendation: Use mock data or simpler PDFs")

    print()
    print("=" * 80)

    return {
        'numeric_pct': numeric_pct,
        'e5_matches': matches_found,
        'numbers_extracted': len(extracted_numbers),
        'score': score,
        'max_score': max_score
    }

if __name__ == "__main__":
    try:
        results = test_extraction_quality()
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
