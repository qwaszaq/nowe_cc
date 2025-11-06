"""
Test Jina Embeddings for Semantic Financial Table Extraction

Validates that Jina can semantically match Polish financial terms
even when exact text doesn't match.
"""

from sentence_transformers import SentenceTransformer
import numpy as np

def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def test_jina_semantic_matching():
    print("=" * 80)
    print("JINA EMBEDDINGS TEST: Semantic Financial Term Matching")
    print("=" * 80)
    print()

    print("Loading Jina Embeddings model...")
    # Use jina-embeddings-v2-base-en (multilingual support)
    model = SentenceTransformer('jinaai/jina-embeddings-v2-base-en', trust_remote_code=True)
    print("✅ Model loaded")
    print()

    # Define what we're looking for (in multiple languages)
    queries = {
        'total_assets': "total assets suma aktywów aktywa razem balance sheet total",
        'current_assets': "current assets aktywa obrotowe aktywa bieżące short-term assets",
        'current_liabilities': "current liabilities zobowiązania krótkoterminowe zobowiązania bieżące",
        'equity': "equity kapitał własny shareholder equity",
        'revenue': "revenue przychody sales income",
        'net_profit': "net profit zysk netto net income earnings"
    }

    # Pre-compute query embeddings
    print("Computing query embeddings...")
    query_embeddings = {}
    for key, query_text in queries.items():
        query_embeddings[key] = model.encode(query_text, normalize_embeddings=True)
    print(f"✅ {len(query_embeddings)} query embeddings ready")
    print()

    # Test cases: Polish financial terms from actual reports
    test_rows = [
        # Balance Sheet items
        "Aktywa razem 1,234,567 1,100,000",
        "Rzeczowe aktywa trwałe 456,789 450,000",
        "Aktywa obrotowe 789,012 650,000",
        "Zobowiązania krótkoterminowe 300,000 320,000",
        "Kapitał własny 600,000 550,000",
        "Środki pieniężne i ich ekwiwalenty 150,000 140,000",

        # Income Statement items
        "Przychody ze sprzedaży 2,500,000 2,300,000",
        "Zysk netto 180,000 160,000",
        "Zysk operacyjny (EBIT) 250,000 220,000",
        "Koszty sprzedaży 1,800,000 1,700,000",

        # Edge cases
        "Suma aktywów (total assets) 1,234,567 1,100,000",  # Mixed language
        "Kapitał (equity) razem 600,000 550,000",  # Partial match
    ]

    print("-" * 80)
    print("SEMANTIC MATCHING RESULTS")
    print("-" * 80)
    print()

    threshold = 0.60  # Similarity threshold
    matches = 0
    total = len(test_rows)

    for i, row_text in enumerate(test_rows, 1):
        print(f"Test {i}: {row_text}")

        # Get embedding for this row
        row_embedding = model.encode(row_text, normalize_embeddings=True)

        # Find best matching query
        best_match = None
        best_score = 0.0

        for key, query_embedding in query_embeddings.items():
            similarity = cosine_similarity(row_embedding, query_embedding)

            if similarity > best_score:
                best_score = similarity
                best_match = key

        if best_score >= threshold:
            print(f"  ✅ Matched: {best_match.replace('_', ' ').title()}")
            print(f"     Confidence: {best_score:.3f}")
            matches += 1
        else:
            print(f"  ❌ No match (best: {best_match}, score: {best_score:.3f})")
        print()

    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    print(f"Total test rows: {total}")
    print(f"Successful matches: {matches}")
    print(f"Match rate: {matches/total*100:.1f}%")
    print(f"Threshold used: {threshold:.2f}")
    print()

    if matches / total >= 0.8:
        print("✅ SUCCESS: Jina semantic matching is effective for Polish financial terms!")
        print("   Recommendation: Integrate into Alex agent for table extraction")
    else:
        print("🟡 PARTIAL: Semantic matching works but may need tuning")
        print(f"   Consider: Lower threshold or better query phrases")
    print()

    return {
        'total': total,
        'matches': matches,
        'match_rate': matches / total
    }

if __name__ == "__main__":
    try:
        results = test_jina_semantic_matching()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
