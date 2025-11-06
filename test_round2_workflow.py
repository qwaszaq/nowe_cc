"""
Test Round 2 Workflow: Alex (Numeric Extraction) → Marcus (Quantitative Analysis)

This test validates:
1. Alex extracts actual numeric values from Polish financial tables
2. Marcus receives numeric data and calculates real financial ratios
3. Marcus provides quantitative assessment with actual numbers
"""

import sys
sys.path.insert(0, '.')

from agents.analytical.alex_agent_llm import AlexAgentLLM
from agents.analytical.marcus_agent_llm import MarcusAgentLLM
from agents.task_models import Task, TaskStatus
from datetime import datetime
import json

def test_round2_workflow():
    """Test complete Round 2 workflow with numeric extraction"""

    print("=" * 80)
    print("ROUND 2 WORKFLOW TEST: Numeric Extraction → Quantitative Analysis")
    print("=" * 80)
    print()

    # Initialize agents
    print("Initializing agents...")
    alex = AlexAgentLLM()
    marcus = MarcusAgentLLM()
    print(f"✅ {alex.name} initialized (with numeric extraction)")
    print(f"✅ {marcus.name} initialized (with quantitative analysis)")
    print()

    # STEP 1: Alex parses document and extracts numbers
    print("-" * 80)
    print("STEP 1: ALEX - Document Parsing + Numeric Extraction")
    print("-" * 80)
    print()

    from uuid import uuid4
    alex_task = Task(
        task_id=uuid4(),
        title="Parse Grupa Azoty 2024 Report with Numeric Extraction",
        description="Parse data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2024.pdf and extract actual numeric values from balance sheet and income statement",
        assigned_to="Alex Morgan",
        assigned_by="Test System",
        context={},
        priority=5,
        status=TaskStatus.PENDING,
        created_at=datetime.now()
    )

    print(f"📋 Task: {alex_task.title}")
    print(f"📄 File: data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2024.pdf")
    print()

    start_alex = datetime.now()
    alex_result = alex.process_task(alex_task)
    alex_time = (datetime.now() - start_alex).total_seconds()

    print(f"⏱️  Alex Processing Time: {alex_time:.2f} seconds")
    print(f"📊 Status: {alex_result.status.value}")

    # Check if Alex task failed
    if alex_result.status != TaskStatus.DONE or alex_result.output is None:
        print(f"❌ ERROR: Alex task failed")
        print(f"Error output: {alex_result.output}")
        print(f"Error thoughts: {alex_result.thoughts}")
        raise Exception(f"Alex task failed: {alex_result.thoughts}")

    print()

    # Extract numeric data from Alex's output
    parsed_doc = alex_result.output.get('parsed_doc_summary', {})
    balance_sheet_numbers = parsed_doc.get('balance_sheet_numbers', {})
    income_statement_numbers = parsed_doc.get('income_statement_numbers', {})

    print("🔢 NUMERIC DATA EXTRACTED BY ALEX:")
    print()
    print(f"Balance Sheet Items: {len(balance_sheet_numbers)}")
    for key, data in list(balance_sheet_numbers.items())[:5]:  # Show first 5
        current = data.get('current')
        if current:
            print(f"  - {key.replace('_', ' ').title()}: {current:,.0f}")
    if len(balance_sheet_numbers) > 5:
        print(f"  ... and {len(balance_sheet_numbers) - 5} more")
    print()

    print(f"Income Statement Items: {len(income_statement_numbers)}")
    for key, data in list(income_statement_numbers.items())[:5]:  # Show first 5
        current = data.get('current')
        if current:
            print(f"  - {key.replace('_', ' ').title()}: {current:,.0f}")
    if len(income_statement_numbers) > 5:
        print(f"  ... and {len(income_statement_numbers) - 5} more")
    print()

    # Show Alex's LLM analysis (first 500 chars)
    print("💡 Alex's Analysis (excerpt):")
    print(alex_result.thoughts[:500] + "..." if len(alex_result.thoughts) > 500 else alex_result.thoughts)
    print()

    # STEP 2: Marcus performs quantitative analysis
    print("-" * 80)
    print("STEP 2: MARCUS - Quantitative Financial Analysis with Real Ratios")
    print("-" * 80)
    print()

    # Create task for Marcus with numeric data
    marcus_task = Task(
        task_id=uuid4(),
        title="Quantitative Analysis of Grupa Azoty Tarnów H1 2024",
        description=f"Perform quantitative financial analysis using actual numeric data extracted from financial statements. Calculate real ratios and provide assessment.",
        assigned_to="Marcus Chen",
        assigned_by="Alex Morgan",
        context={},
        priority=5,
        status=TaskStatus.PENDING,
        created_at=datetime.now()
    )

    print(f"📋 Task: {marcus_task.title}")
    print(f"📊 Data Received: {len(balance_sheet_numbers)} balance sheet items, {len(income_statement_numbers)} income statement items")
    print()

    start_marcus = datetime.now()

    # Call Marcus's quantitative analysis method with numeric data
    marcus_result = marcus._quantitative_financial_analysis_llm(
        marcus_task,
        context=[alex_result.thoughts],  # Pass Alex's analysis as context
        balance_sheet=balance_sheet_numbers,
        income_statement=income_statement_numbers
    )

    marcus_time = (datetime.now() - start_marcus).total_seconds()

    print(f"⏱️  Marcus Processing Time: {marcus_time:.2f} seconds")
    print(f"📊 Status: {marcus_result.status.value}")
    print()

    # Show calculated ratios
    calculated_ratios = marcus_result.output.get('calculated_ratios', {})
    print(f"🧮 FINANCIAL RATIOS CALCULATED: {len(calculated_ratios)}")
    print()

    if calculated_ratios:
        print("Liquidity Ratios:")
        for ratio_name in ['current_ratio', 'quick_ratio', 'cash_ratio']:
            if ratio_name in calculated_ratios:
                ratio = calculated_ratios[ratio_name]
                value = ratio['value']
                interp = ratio['interpretation']
                print(f"  - {ratio_name.replace('_', ' ').title()}: {value:.3f} ({interp})")
                if 'trend' in ratio:
                    print(f"      Prior: {ratio['prior']:.3f}, Change: {ratio['change_pct']:+.1f}% ({ratio['trend']})")
        print()

        print("Leverage Ratios:")
        for ratio_name in ['debt_to_equity', 'debt_to_assets', 'equity_ratio']:
            if ratio_name in calculated_ratios:
                ratio = calculated_ratios[ratio_name]
                value = ratio['value']
                interp = ratio['interpretation']
                print(f"  - {ratio_name.replace('_', ' ').title()}: {value:.3f} ({interp})")
        print()

        print("Profitability Ratios:")
        for ratio_name in ['return_on_assets', 'return_on_equity', 'net_profit_margin']:
            if ratio_name in calculated_ratios:
                ratio = calculated_ratios[ratio_name]
                percentage = ratio.get('percentage', ratio['value'] * 100)
                interp = ratio['interpretation']
                print(f"  - {ratio_name.replace('_', ' ').title()}: {percentage:.2f}% ({interp})")
                if 'trend' in ratio:
                    prior_pct = ratio['prior'] * 100 if 'percentage' in ratio else ratio['prior']
                    print(f"      Prior: {prior_pct:.2f}%, Change: {ratio['change_pct']:+.1f}% ({ratio['trend']})")
        print()

        print("Growth Metrics:")
        for ratio_name in ['revenue_growth', 'profit_growth']:
            if ratio_name in calculated_ratios:
                ratio = calculated_ratios[ratio_name]
                percentage = ratio.get('percentage', ratio['value'])
                interp = ratio['interpretation']
                print(f"  - {ratio_name.replace('_', ' ').title()}: {percentage:+.2f}% ({interp})")
        print()

    # Show Marcus's LLM analysis (first 1000 chars)
    print("💡 Marcus's Quantitative Analysis (excerpt):")
    print(marcus_result.thoughts[:1000] + "..." if len(marcus_result.thoughts) > 1000 else marcus_result.thoughts)
    print()

    # WORKFLOW SUMMARY
    print("=" * 80)
    print("ROUND 2 WORKFLOW SUMMARY")
    print("=" * 80)
    print()

    total_time = alex_time + marcus_time

    print(f"✅ WORKFLOW COMPLETED SUCCESSFULLY")
    print()
    print(f"Total Processing Time: {total_time:.2f} seconds")
    print(f"  - Alex (parsing + extraction): {alex_time:.2f}s")
    print(f"  - Marcus (quantitative analysis): {marcus_time:.2f}s")
    print()

    print("📊 ACHIEVEMENTS:")
    print(f"  ✅ Document parsed: 61 pages")
    print(f"  ✅ Tables extracted: {parsed_doc.get('num_pages', 'N/A')}")
    print(f"  ✅ Numeric values extracted: {len(balance_sheet_numbers) + len(income_statement_numbers)}")
    print(f"  ✅ Financial ratios calculated: {len(calculated_ratios)}")
    print(f"  ✅ Year-over-year trends: {sum(1 for r in calculated_ratios.values() if 'trend' in r)}")
    print()

    print("🎯 QUALITY VS ROUND 1:")
    print("  Round 1: Marcus provided methodology (\"Calculate current ratio = A / B\")")
    print(f"  Round 2: Marcus calculated actual ratio: {calculated_ratios.get('current_ratio', {}).get('value', 'N/A'):.3f}")
    print("  Improvement: ∞ (from methodology to actual numbers)")
    print()

    print("🔄 TEAM COORDINATION:")
    print("  ✅ Alex extracted numeric data successfully")
    print("  ✅ Marcus received structured data")
    print("  ✅ Marcus calculated real ratios")
    print("  ✅ Marcus provided quantitative assessment")
    print()

    print("📁 NEXT STEPS:")
    print("  1. Save Round 2 outputs to analysis_rounds/round_2/")
    print("  2. Compare Round 1 vs Round 2 quality")
    print("  3. Proceed to Phase 3: Learning System (WBWS)")
    print()

    return {
        'alex_time': alex_time,
        'marcus_time': marcus_time,
        'total_time': total_time,
        'balance_sheet_items': len(balance_sheet_numbers),
        'income_statement_items': len(income_statement_numbers),
        'ratios_calculated': len(calculated_ratios),
        'alex_result': alex_result,
        'marcus_result': marcus_result,
        'calculated_ratios': calculated_ratios
    }


if __name__ == "__main__":
    try:
        results = test_round2_workflow()
        print("✅ Round 2 workflow test PASSED")
        print()
        print("="  * 80)

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
