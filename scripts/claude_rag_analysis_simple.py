"""
Simple Claude RAG Analysis for Grupa Azoty 2019-2021
Query documents and generate comprehensive investment report
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.rag.qdrant_vector_store import QdrantVectorStore
import anthropic
import os
from datetime import datetime
import time

COMPANY = "Grupa Azoty"
YEARS = [2019, 2020, 2021]
COLLECTION_NAME = "azoty_2019_2021_multi_year"

def main():
    print("=" * 80)
    print(f"CLAUDE RAG ANALYSIS: {COMPANY} {YEARS[0]}-{YEARS[-1]}")
    print("=" * 80)
    print()

    start_time = time.time()

    # Initialize vector store
    print("Initializing Qdrant...")
    vector_store = QdrantVectorStore(
        collection_name=COLLECTION_NAME,
        qdrant_url="http://localhost:6333",
        use_reranker=True
    )

    # Define comprehensive query
    query = f"{COMPANY} financial performance, strategy, risks, and investment outlook {YEARS[0]}-{YEARS[-1]}"

    print(f"Retrieving relevant document chunks...")
    print(f"Query: {query}")
    print()

    # Search for all years
    all_chunks = []
    for year in YEARS:
        print(f"  Searching {year} documents...")
        results = vector_store.search(
            query=query,
            company=COMPANY,
            year=year,
            top_k=15  # Get 15 chunks per year = 45 total
        )
        all_chunks.extend(results)
        print(f"    Retrieved {len(results)} chunks")

    print(f"\nTotal chunks retrieved: {len(all_chunks)}")

    # Format context
    context_parts = []
    for chunk in all_chunks:
        metadata = chunk.get('metadata', {})
        content = chunk.get('content', '')
        source = metadata.get('source', 'Unknown')
        year = metadata.get('year', 'N/A')
        page = metadata.get('page', 'N/A')

        context_parts.append(f"[{source}, Year: {year}, Page: {page}]\n{content}")

    combined_context = "\n\n---\n\n".join(context_parts)

    print(f"Combined context length: {len(combined_context):,} characters")
    print()

    # Generate analysis with Claude
    print("Generating Claude analysis...")
    print()

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    prompt = f"""Based on the following document excerpts from {COMPANY}'s annual reports for {YEARS[0]}-{YEARS[-1]}, generate a comprehensive investment intelligence report.

DOCUMENT CONTEXT:
{combined_context[:100000]}

Your analysis should include:

## 1. Executive Summary
- Overall Assessment Score (0-100)
- Investment Recommendation (STRONG BUY / BUY / HOLD / SELL / STRONG SELL)
- Key findings (3-5 bullets)

## 2. Financial Performance Analysis
- Revenue and profitability trends {YEARS[0]}-{YEARS[-1]}
- Balance sheet strength and asset quality
- Cash flow analysis
- Key financial ratios

## 3. Strategic Evaluation
- Business strategy and execution quality
- Market position and competitive advantages
- Operational efficiency
- Growth initiatives and investments

## 4. Risk Assessment
- Financial risks (leverage, liquidity)
- Operational risks
- Market and industry risks
- Environmental and regulatory risks

## 5. Investment Thesis
- Bull case (3-5 positive factors)
- Bear case (3-5 concerns/risks)
- Base case outlook
- Valuation perspective

## 6. Final Recommendation
- **Overall Assessment Score:** X/100
- **Investment Recommendation:** **[RECOMMENDATION]**
- Rationale (2-3 paragraphs)
- Key catalysts and risks to monitor

Format in clear markdown. Cite specific sources when making claims (e.g., "According to the 2020 Financial Statements, page 45...").

Generate a detailed, data-driven analysis based ONLY on the provided document context."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=16000,
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )

        report = message.content[0].text
        elapsed = time.time() - start_time

        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"output/intelligence_reports/Azoty_ClaudeRAG_{YEARS[0]}_{YEARS[-1]}_{timestamp}.md"
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        Path(output_file).write_text(report)

        print("=" * 80)
        print("✅ CLAUDE RAG ANALYSIS COMPLETE")
        print("=" * 80)
        print()
        print(f"Generation time: {elapsed:.1f}s")
        print(f"Report length: {len(report):,} characters")
        print(f"Document chunks used: {len(all_chunks)}")
        print(f"Context characters: {len(combined_context):,}")
        print()
        print(f"Report saved to: {output_file}")
        print()

        # Show preview
        print("Report Preview (first 1500 chars):")
        print("-" * 80)
        print(report[:1500])
        print("...")
        print("-" * 80)

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
