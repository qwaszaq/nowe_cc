"""
Test script to verify Gap #1 (RAG collection routing) is fixed
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.rag.rag_service import RAGService

print("=" * 80)
print("TESTING GAP #1 FIX: RAG Collection Routing")
print("=" * 80)
print()

# Test 1: Verify RAGService accepts collection_name parameter
print("Test 1: Initialize RAGService with custom collection name...")
try:
    rag = RAGService(collection_name='azoty_multi_year')
    print("✅ RAGService initialized successfully with 'azoty_multi_year' collection")
except Exception as e:
    print(f"❌ FAILED: {e}")
    sys.exit(1)

print()

# Test 2: Verify RAG retrieves results from correct collection
print("Test 2: Query RAG for context (should find results in azoty_multi_year)...")
try:
    context = rag.get_context_for_question(
        'Why did profitability decline?',
        'Grupa Azoty S.A.',
        years=[2024]
    )

    if len(context) > 100 and "No relevant context found" not in context:
        print("✅ SUCCESS - RAG retrieved context from azoty_multi_year collection")
        print(f"   Context length: {len(context)} characters")
        print()
        print("Context preview (first 500 chars):")
        print("-" * 80)
        print(context[:500])
        print("...")
    else:
        print(f"❌ FAILED - No context retrieved (got: {context[:100]})")
        sys.exit(1)

except Exception as e:
    print(f"❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 80)
print("✅ GAP #1 FIX VERIFIED - RAG collection routing works correctly")
print("=" * 80)
