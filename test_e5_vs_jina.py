"""
Compare E5 (local LM Studio) vs Jina Embeddings on Real Azoty Data

Tests both embedding models to see which provides better semantic discrimination
for Polish financial terms.
"""

import requests
import numpy as np
from sentence_transformers import SentenceTransformer
from src.document_processing.pdf_parser import PDFParser

def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_e5_embedding(text: str, lm_studio_url: str = "http://192.168.200.226:1234") -> np.ndarray:
    """Get embedding from E5 model via LM Studio API"""
    try:
        response = requests.post(
            f"{lm_studio_url}/v1/embeddings",
            json={
                "model": "intfloat/e5-large-v2",  # or whatever E5 model you have loaded
                "input": text
            },
            timeout=10
        )
        response.raise_for_status()
        embedding = response.json()['data'][0]['embedding']
        return np.array(embedding)
    except Exception as e:
        print(f"E5 API error: {e}")
        return None

def test_both_models():
    print("=" * 80)
    print("E5 vs JINA: Real Grupa Azoty Balance Sheet Comparison")
    print("=" * 80)
    print()

    # Load Jina model
    print("Loading Jina model...")
    jina_model = SentenceTransformer('jinaai/jina-embeddings-v2-base-en', trust_remote_code=True)
    print("✅ Jina model loaded")
    print()

    # Test E5 connection
    print("Testing E5 connection to LM Studio...")
    test_embedding = get_e5_embedding("test")
    if test_embedding is not None:
        print(f"✅ E5 connected (embedding dim: {len(test_embedding)})")
    else:
        print("❌ E5 connection failed - check LM Studio is running with E5 model")
        return
    print()

    # Define financial term queries
    queries = {
        'total_assets': "total assets suma aktywów aktywa razem balance sheet total",
        'current_assets': "current assets aktywa obrotowe aktywa bieżące short-term assets",
        'fixed_assets': "fixed assets aktywa trwałe non-current assets long-term assets",
        'current_liabilities': "current liabilities zobowiązania krótkoterminowe zobowiązania bieżące",
        'equity': "equity kapitał własny shareholder equity",
        'cash': "cash środki pieniężne cash equivalents gotówka",
        'inventory': "inventory zapasy stocks",
        'receivables': "receivables należności accounts receivable",
        'revenue': "revenue przychody sales income",
        'net_profit': "net profit zysk netto net income earnings",
        'operating_profit': "operating profit zysk operacyjny EBIT",
        'gross_profit': "gross profit zysk brutto gross margin",
        'total_liabilities': "total liabilities zobowiązania razem suma zobowiązań",
        'intangible_assets': "intangible assets wartości niematerialne goodwill",
        'financial_assets': "financial assets aktywa finansowe investments"
    }

    print("Computing query embeddings...")
    jina_queries = {}
    e5_queries = {}

    for key, query_text in queries.items():
        jina_queries[key] = jina_model.encode(query_text, normalize_embeddings=True)
        e5_queries[key] = get_e5_embedding(query_text)
        if e5_queries[key] is not None:
            e5_queries[key] = e5_queries[key] / np.linalg.norm(e5_queries[key])  # normalize

    print(f"✅ {len(jina_queries)} Jina query embeddings ready")
    print(f"✅ {len(e5_queries)} E5 query embeddings ready")
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
    print()

    # Test on sample rows
    print("-" * 80)
    print("COMPARISON: First 20 Non-Empty Rows")
    print("-" * 80)
    print()

    threshold = 0.55  # Lower threshold to see more matches
    jina_matches = []
    e5_matches = []
    row_count = 0
    max_rows = 20

    for i, row in enumerate(balance_sheet.rows):
        if row_count >= max_rows:
            break

        row_text = ' '.join([str(cell) for cell in row if cell and str(cell).strip()])
        if not row_text or len(row_text) < 3:
            continue

        row_count += 1

        # Get embeddings
        jina_embedding = jina_model.encode(row_text, normalize_embeddings=True)
        e5_embedding = get_e5_embedding(row_text)
        if e5_embedding is None:
            continue
        e5_embedding = e5_embedding / np.linalg.norm(e5_embedding)

        # Find best match for each model
        jina_best = None
        jina_score = threshold
        e5_best = None
        e5_score = threshold

        for key in queries.keys():
            jina_sim = cosine_similarity(jina_embedding, jina_queries[key])
            if jina_sim > jina_score:
                jina_score = jina_sim
                jina_best = key

            e5_sim = cosine_similarity(e5_embedding, e5_queries[key])
            if e5_sim > e5_score:
                e5_score = e5_sim
                e5_best = key

        # Display comparison
        print(f"Row {i:2d}: {row_text[:70]}")

        if jina_best or e5_best:
            if jina_best:
                print(f"  🟦 Jina:  {jina_best.replace('_', ' ').title():30s} (confidence: {jina_score:.3f})")
                jina_matches.append((row_text, jina_best, jina_score))
            else:
                print(f"  🟦 Jina:  No match above threshold")

            if e5_best:
                print(f"  🟩 E5:    {e5_best.replace('_', ' ').title():30s} (confidence: {e5_score:.3f})")
                e5_matches.append((row_text, e5_best, e5_score))
            else:
                print(f"  🟩 E5:    No match above threshold")

            # Highlight when they differ
            if jina_best != e5_best:
                if jina_best and e5_best:
                    print(f"  ⚠️  DIFFER: Jina={jina_best} vs E5={e5_best}")
                print()
        else:
            print(f"  ⚪ Both: No match above threshold")
            print()

    print("=" * 80)
    print("COMPARISON SUMMARY")
    print("=" * 80)
    print()
    print(f"Total rows tested: {row_count}")
    print(f"Jina matches: {len(jina_matches)}")
    print(f"E5 matches: {len(e5_matches)}")
    print()

    # Calculate agreement
    jina_set = set([(match[0], match[1]) for match in jina_matches])
    e5_set = set([(match[0], match[1]) for match in e5_matches])
    agreement = len(jina_set.intersection(e5_set))

    print(f"Agreement rate: {agreement}/{max(len(jina_matches), len(e5_matches))} "
          f"({agreement/max(len(jina_matches), len(e5_matches), 1)*100:.1f}%)")
    print()

    # Analyze confidence scores
    if jina_matches:
        jina_avg = sum([m[2] for m in jina_matches]) / len(jina_matches)
        print(f"Jina average confidence: {jina_avg:.3f}")

    if e5_matches:
        e5_avg = sum([m[2] for m in e5_matches]) / len(e5_matches)
        print(f"E5 average confidence: {e5_avg:.3f}")
    print()

    # Show unique matches
    jina_only = jina_set - e5_set
    e5_only = e5_set - jina_set

    if jina_only:
        print(f"🟦 Jina-only matches ({len(jina_only)}):")
        for text, category in list(jina_only)[:5]:
            print(f"  - {category}: {text[:60]}")
        print()

    if e5_only:
        print(f"🟩 E5-only matches ({len(e5_only)}):")
        for text, category in list(e5_only)[:5]:
            print(f"  - {category}: {text[:60]}")
        print()

    print("=" * 80)
    print("RECOMMENDATION")
    print("=" * 80)
    print()

    # Determine winner
    if len(e5_matches) > len(jina_matches) * 1.2:
        print("🟩 E5 WINS: Found significantly more matches")
        print("   Recommendation: Use E5 for semantic extraction")
    elif len(jina_matches) > len(e5_matches) * 1.2:
        print("🟦 JINA WINS: Found significantly more matches")
        print("   Recommendation: Use Jina for semantic extraction")
    else:
        print("🟨 TIE: Similar performance")
        if e5_matches and jina_matches:
            e5_avg = sum([m[2] for m in e5_matches]) / len(e5_matches)
            jina_avg = sum([m[2] for m in jina_matches]) / len(jina_matches)
            if e5_avg > jina_avg * 1.05:
                print("   E5 has higher average confidence - slight edge")
                print("   Recommendation: Use E5 (local, higher confidence)")
            elif jina_avg > e5_avg * 1.05:
                print("   Jina has higher average confidence - slight edge")
                print("   Recommendation: Use Jina (no external dependency)")
            else:
                print("   Recommendation: Use E5 (local LM Studio, no internet needed)")
    print()

if __name__ == "__main__":
    try:
        test_both_models()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
