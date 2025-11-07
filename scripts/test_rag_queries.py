"""
Test RAG queries on ingested Grupa Azoty 2023 data
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.rag_service import RAGService

if __name__ == "__main__":
    print("=" * 80)
    print("TESTING RAG QUERIES ON GRUPA AZOTY 2023")
    print("=" * 80)
    print()

    # Initialize RAG service
    rag = RAGService(qdrant_url="http://localhost:6333", use_reranker=True)

    # Test queries
    test_queries = [
        {
            "type": "Financial Health",
            "question": "Why did liquidity decline? What are the cash flow issues?"
        },
        {
            "type": "Risk Assessment",
            "question": "What are the main financial risks facing the company?"
        },
        {
            "type": "Strategy",
            "question": "What is the company's growth strategy and key initiatives?"
        },
        {
            "type": "Operations",
            "question": "What challenges does the company face in operations?"
        }
    ]

    for i, query_info in enumerate(test_queries, 1):
        print(f"\n{'=' * 80}")
        print(f"QUERY {i}/{len(test_queries)}: {query_info['type']}")
        print(f"{'=' * 80}")
        print(f"Question: {query_info['question']}")
        print()

        # Get context
        context = rag.get_context_for_question(
            question=query_info['question'],
            company="Grupa Azoty S.A.",
            years=[2023],
            top_k=3
        )

        print("Retrieved Context:")
        print("-" * 80)
        print(context)
        print()

    print("=" * 80)
    print("RAG QUERY TEST COMPLETE")
    print("=" * 80)
    print()
    print("Next: Integrate RAG with intelligence service for enhanced reports")
