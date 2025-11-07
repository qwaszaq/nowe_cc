"""
Comprehensive RAG-Based Benchmark: Grupa Azoty 2019-2021
Pure document-based analysis using RAG retrieval
"""

import sys
from pathlib import Path
import time
import json
from datetime import datetime
import anthropic
import os

sys.path.append(str(Path(__file__).parent.parent))

from src.rag.qdrant_vector_store import QdrantVectorStore
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

COMPANY = "Grupa Azoty"
YEARS = [2019, 2020, 2021]
COLLECTION_NAME = "azoty_2019_2021_multi_year"


def run_claude_rag_analysis():
    """Run Claude analysis with RAG context from documents"""
    print("\n" + "=" * 80)
    print("CLAUDE RAG ANALYSIS (Document-Based)")
    print("=" * 80)
    print()

    start_time = time.time()

    # Initialize RAG store
    vector_store = QdrantVectorStore(
        collection_name=COLLECTION_NAME,
        qdrant_url="http://localhost:6333",
        use_reranker=True
    )

    # Initialize Claude
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    # Define comprehensive analysis queries
    analysis_queries = [
        f"{COMPANY} financial performance {YEARS[0]}-{YEARS[-1]}",
        f"{COMPANY} revenue and profitability trends",
        f"{COMPANY} assets and liabilities",
        f"{COMPANY} cash flow and liquidity",
        f"{COMPANY} debt and financial stability",
        f"{COMPANY} strategic initiatives and investments",
        f"{COMPANY} market position and competitive landscape",
        f"{COMPANY} risk factors and challenges",
        f"{COMPANY} operational performance",
        f"{COMPANY} future outlook and strategy"
    ]

    # Retrieve context for all queries
    print("Retrieving context from documents...")
    all_contexts = []

    for query in analysis_queries:
        print(f"  Query: {query[:60]}...")
        chunks = vector_store.search(
            query_text=query,
            top_k=5,
            year_filter=YEARS
        )

        if chunks:
            context = "\n\n".join([
                f"[Source: {chunk.metadata.get('source', 'Unknown')}, Year: {chunk.metadata.get('year', 'N/A')}, Page: {chunk.metadata.get('page', 'N/A')}]\n{chunk.page_content}"
                for chunk in chunks
            ])
            all_contexts.append(f"## Query: {query}\n\n{context}")

    combined_context = "\n\n---\n\n".join(all_contexts)
    print(f"\nRetrieved {len(combined_context)} characters of context from {len(all_contexts)} queries")
    print()

    # Generate comprehensive analysis with Claude
    prompt = f"""You are a senior financial analyst. Based on the document excerpts provided below from {COMPANY}'s annual reports for {YEARS[0]}-{YEARS[-1]}, generate a comprehensive investment intelligence report.

DOCUMENT CONTEXT:
{combined_context[:100000]}  # Limit to 100k chars to stay under context limit

Your analysis should include:

1. **Executive Summary**
   - Overall assessment score (0-100)
   - Investment recommendation (STRONG BUY / BUY / HOLD / SELL / STRONG SELL)
   - Key findings summary

2. **Financial Performance Analysis**
   - Revenue and profitability trends
   - Asset quality and balance sheet strength
   - Cash flow analysis
   - Financial ratios and metrics

3. **Strategic Evaluation**
   - Business strategy and execution
   - Market position and competitive advantages
   - Operational efficiency
   - Growth initiatives

4. **Risk Assessment**
   - Financial risks (leverage, liquidity, volatility)
   - Operational risks
   - Market and industry risks
   - Regulatory and environmental risks

5. **Investment Thesis**
   - Bull case (positive factors)
   - Bear case (concerns and risks)
   - Base case outlook
   - Valuation perspective

6. **Final Recommendation**
   - Overall Assessment Score: X/100
   - Investment Recommendation: **[RECOMMENDATION]**
   - Rationale
   - Key catalysts and risks

Format the report in clear markdown. Cite specific sources when making claims (e.g., "According to the 2020 Financial Statements, page 45...").

Generate a detailed, data-driven analysis based ONLY on the provided document context."""

    print("Generating Claude analysis...")
    print("(This may take 60-120 seconds)")
    print()

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=16000,
            temperature=0,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        report = message.content[0].text
        elapsed = time.time() - start_time

        # Extract metrics
        score = None
        recommendation = None
        for line in report.split('\n'):
            if 'Overall Assessment Score' in line or 'Assessment Score' in line:
                # Extract number before /100
                import re
                match = re.search(r'(\d+)(?:/100)?', line)
                if match:
                    score = int(match.group(1))
            if 'Investment Recommendation' in line and '**' in line:
                parts = line.split('**')
                if len(parts) >= 2:
                    recommendation = parts[1].strip()

        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"output/intelligence_reports/Azoty_ClaudeRAG_2019_2021_{timestamp}.md"
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        Path(output_file).write_text(report)

        print(f"✅ Claude RAG Analysis Complete")
        print(f"   Time: {elapsed:.1f}s")
        print(f"   Score: {score}/100" if score else "   Score: Not extracted")
        print(f"   Recommendation: {recommendation}" if recommendation else "   Recommendation: Not extracted")
        print(f"   Report Length: {len(report):,} chars")
        print(f"   Saved to: {output_file}")

        return {
            "approach": "Claude RAG (Document-Based)",
            "time": elapsed,
            "score": score,
            "recommendation": recommendation,
            "report_length": len(report),
            "report_file": output_file,
            "model": "claude-sonnet-4-20250514",
            "context_chars": len(combined_context),
            "queries_used": len(analysis_queries)
        }

    except Exception as e:
        logger.error(f"Claude RAG analysis failed: {e}", exc_info=True)
        return {
            "approach": "Claude RAG (Document-Based)",
            "time": time.time() - start_time,
            "score": None,
            "recommendation": "FAILED",
            "report_length": None,
            "report_file": None,
            "error": str(e)
        }


def compare_results(claude_rag):
    """Generate comparison report"""
    print("\n" + "=" * 80)
    print("BENCHMARK RESULTS")
    print("=" * 80)
    print()

    print("Analysis Summary:")
    print("-" * 80)
    print(f"Approach: {claude_rag['approach']}")
    print(f"Model: {claude_rag.get('model', 'N/A')}")
    print(f"Time: {claude_rag['time']:.1f}s")
    print(f"Score: {claude_rag['score']}/100" if claude_rag['score'] else "Score: N/A")
    print(f"Recommendation: {claude_rag['recommendation']}")
    print(f"Report Length: {claude_rag['report_length']:,} chars" if claude_rag['report_length'] else "Report Length: N/A")
    print(f"Context Used: {claude_rag.get('context_chars', 0):,} chars")
    print(f"RAG Queries: {claude_rag.get('queries_used', 0)}")
    print("-" * 80)
    print()

    # Save comparison report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    comparison_file = f"output/benchmarks/Azoty_Benchmark_RAG_2019_2021_{timestamp}.json"
    Path(comparison_file).parent.mkdir(parents=True, exist_ok=True)

    comparison_data = {
        "timestamp": timestamp,
        "company": COMPANY,
        "years": YEARS,
        "collection": COLLECTION_NAME,
        "results": {
            "claude_rag": claude_rag
        }
    }

    with open(comparison_file, 'w') as f:
        json.dump(comparison_data, f, indent=2)

    print(f"📊 Benchmark data saved to: {comparison_file}")
    print()

    return comparison_data


def main():
    """Run RAG-based benchmark"""
    print("=" * 80)
    print("COMPREHENSIVE BENCHMARK: GRUPA AZOTY 2019-2021")
    print("RAG-Based Document Analysis")
    print("=" * 80)
    print()
    print(f"Company: {COMPANY}")
    print(f"Years: {YEARS}")
    print(f"Collection: {COLLECTION_NAME}")
    print()

    # Run Claude RAG analysis
    claude_rag = run_claude_rag_analysis()

    # Generate comparison report
    comparison = compare_results(claude_rag)

    print("=" * 80)
    print("BENCHMARK COMPLETE!")
    print("=" * 80)
    print()
    print("Results available in:")
    print("  - Report: output/intelligence_reports/")
    print("  - Benchmark data: output/benchmarks/")
    print()


if __name__ == "__main__":
    main()
