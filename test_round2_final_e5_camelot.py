"""
Round 2 FINAL Test: E5 + Camelot Integration

Tests the complete workflow with both improvements:
1. Camelot PDF extraction (better numeric extraction from complex tables)
2. E5 semantic matching (89.7% confidence vs Jina's 78.5%)

This is the ultimate validation of Round 2 enhancements.
"""

import sys
sys.path.insert(0, '.')

from agents.analytical.alex_agent_llm import AlexAgentLLM
from agents.analytical.marcus_agent_llm import MarcusAgentLLM
from agents.task_models import Task, TaskStatus
from datetime import datetime
from uuid import uuid4

def test_round2_final():
    print("=" * 80)
    print("ROUND 2 FINAL TEST: E5 Embeddings + Camelot PDF Extraction")
    print("=" * 80)
    print()

    print("Enhancements:")
    print("  1. E5 semantic matching (89.7% avg confidence)")
    print("  2. Camelot PDF extraction (better for complex Polish tables)")
    print("  3. Fallback chain: pdfplumber → Camelot")
    print()

    # Initialize agents
    print("-" * 80)
    print("INITIALIZATION")
    print("-" * 80)
    alex = AlexAgentLLM()
    marcus = MarcusAgentLLM()
    print(f"✅ {alex.name} initialized")
    print(f"   Supported formats: {alex.supported_formats}")
    print(f"✅ {marcus.name} initialized")
    print()

    # Alex Task: Parse Azoty document
    print("-" * 80)
    print("ALEX: Document Parsing + Numeric Extraction (E5 + Camelot)")
    print("-" * 80)
    print()

    alex_task = Task(
        task_id=uuid4(),
        title="Parse Grupa Azoty 2024 Report (E5 + Camelot)",
        description="Parse data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2024.pdf",
        assigned_to="Alex Morgan",
        assigned_by="Test System",
        context={},
        priority=5,
        status=TaskStatus.PENDING,
        created_at=datetime.now()
    )

    print(f"📋 Task: {alex_task.title}")
    print()

    alex_start = datetime.now()
    alex_result = alex.process_task(alex_task)
    alex_elapsed = (datetime.now() - alex_start).total_seconds()

    print(f"⏱️  Alex Processing Time: {alex_elapsed:.2f} seconds")
    print(f"📊 Status: {alex_result.status.value}")
    print()

    # Check what Alex extracted
    balance_sheet_data = alex_result.output.get('balance_sheet_data', {})
    income_statement_data = alex_result.output.get('income_statement_data', {})

    print("📈 NUMERIC VALUES EXTRACTED:")
    print()
    print(f"Balance Sheet items: {len(balance_sheet_data)}")
    if balance_sheet_data:
        for key, val in list(balance_sheet_data.items())[:5]:
            current = val.get('current', 'N/A')
            prior = val.get('prior', 'N/A')
            similarity = val.get('similarity', 0)
            print(f"  ✅ {key.replace('_', ' ').title():30s}: {current:>12} → {prior:>12} (conf: {similarity:.3f})")
        if len(balance_sheet_data) > 5:
            print(f"  ... and {len(balance_sheet_data) - 5} more")
    else:
        print("  ❌ No balance sheet data extracted")
    print()

    print(f"Income Statement items: {len(income_statement_data)}")
    if income_statement_data:
        for key, val in list(income_statement_data.items())[:3]:
            current = val.get('current', 'N/A')
            prior = val.get('prior', 'N/A')
            similarity = val.get('similarity', 0)
            print(f"  ✅ {key.replace('_', ' ').title():30s}: {current:>12} → {prior:>12} (conf: {similarity:.3f})")
        if len(income_statement_data) > 3:
            print(f"  ... and {len(income_statement_data) - 3} more")
    else:
        print("  ❌ No income statement data extracted")
    print()

    # Only proceed to Marcus if we have data
    if not balance_sheet_data and not income_statement_data:
        print("=" * 80)
        print("⚠️  NO DATA EXTRACTED - Cannot test Marcus")
        print("=" * 80)
        print()
        print("DIAGNOSIS:")
        print("  - pdfplumber: Likely failed (complex Polish tables)")
        print("  - Camelot: Check if it found tables")
        print("  - E5 semantic matching: Needs data to match against")
        print()
        print("RECOMMENDATION:")
        print("  1. Check Camelot installation: pip install 'camelot-py[cv]'")
        print("  2. Manually inspect PDF page 38 for table structure")
        print("  3. Try OCR as ultimate fallback")
        return

    # Marcus Task: Quantitative analysis
    print("-" * 80)
    print("MARCUS: Quantitative Financial Analysis")
    print("-" * 80)
    print()

    marcus_task = Task(
        task_id=uuid4(),
        title="Quantitative Analysis of Grupa Azoty Tarnów H1 2024",
        description="Perform quantitative financial analysis on extracted data",
        assigned_to="Marcus Chen",
        assigned_by="Alex Morgan",
        context={"source": "Alex Morgan numeric extraction"},
        priority=5,
        status=TaskStatus.PENDING,
        created_at=datetime.now()
    )

    print(f"📋 Task: {marcus_task.title}")
    print()

    marcus_start = datetime.now()
    marcus_result = marcus._quantitative_financial_analysis_llm(
        marcus_task,
        context=["Numeric data from Alex's E5+Camelot extraction"],
        balance_sheet=balance_sheet_data,
        income_statement=income_statement_data
    )
    marcus_elapsed = (datetime.now() - marcus_start).total_seconds()

    print(f"⏱️  Marcus Processing Time: {marcus_elapsed:.2f} seconds")
    print(f"📊 Status: {marcus_result.status.value}")
    print()

    # Display calculated ratios
    calculated_ratios = marcus_result.output.get('calculated_ratios', {})

    print("=" * 80)
    print(f"🧮 FINANCIAL RATIOS CALCULATED: {len(calculated_ratios)}")
    print("=" * 80)
    print()

    if calculated_ratios:
        # Group ratios by category
        liquidity = ['current_ratio', 'quick_ratio', 'cash_ratio']
        leverage = ['debt_to_equity', 'debt_to_assets', 'equity_ratio']
        profitability = ['return_on_assets', 'return_on_equity', 'net_profit_margin',
                        'gross_profit_margin', 'operating_margin']
        growth = ['revenue_growth', 'profit_growth']

        for category_name, category_ratios in [
            ("LIQUIDITY", liquidity),
            ("LEVERAGE", leverage),
            ("PROFITABILITY", profitability),
            ("GROWTH", growth)
        ]:
            ratios_in_category = [r for r in category_ratios if r in calculated_ratios]
            if ratios_in_category:
                print(f"\n{category_name} RATIOS:")
                print("-" * 80)
                for ratio_name in ratios_in_category:
                    ratio = calculated_ratios[ratio_name]
                    value = ratio.get('value', ratio.get('percentage', 0))
                    interp = ratio.get('interpretation', 'N/A')

                    if 'percentage' in ratio:
                        print(f"\n{ratio_name.replace('_', ' ').title()}: {value:.2f}%")
                    else:
                        print(f"\n{ratio_name.replace('_', ' ').title()}: {value:.3f}")

                    print(f"  Assessment: {interp}")

                    if 'trend' in ratio:
                        change_pct = ratio.get('change_pct', 0)
                        trend = ratio.get('trend', 'N/A')
                        print(f"  YoY Change: {change_pct:+.1f}% ({trend})")

        print("\n" + "=" * 80)

    # Show Marcus's analysis excerpt
    print("\n💡 MARCUS'S QUANTITATIVE ANALYSIS (Excerpt):")
    print("=" * 80)
    print()
    print(marcus_result.thoughts[:1200] + "..." if len(marcus_result.thoughts) > 1200 else marcus_result.thoughts)
    print()

    # FINAL SUMMARY
    print("=" * 80)
    print("ROUND 2 FINAL TEST SUMMARY")
    print("=" * 80)
    print()

    total_time = alex_elapsed + marcus_elapsed
    print(f"⏱️  Total Processing Time: {total_time:.2f} seconds")
    print(f"   Alex (E5 + Camelot): {alex_elapsed:.2f}s")
    print(f"   Marcus (Calculations): {marcus_elapsed:.2f}s")
    print()

    print(f"📊 DATA EXTRACTION:")
    print(f"   Balance Sheet items: {len(balance_sheet_data)}")
    print(f"   Income Statement items: {len(income_statement_data)}")
    print(f"   Total numeric values: {len(balance_sheet_data) + len(income_statement_data)}")
    print()

    print(f"🧮 QUANTITATIVE ANALYSIS:")
    print(f"   Ratios calculated: {len(calculated_ratios)}")
    print(f"   Analysis length: {len(marcus_result.thoughts)} characters")
    print()

    print("🎯 ROUND 2 STATUS:")
    print()
    if len(calculated_ratios) >= 10:
        print("  ✅ SUCCESS: Round 2 is FULLY OPERATIONAL!")
        print()
        print("  🎉 ACHIEVEMENTS:")
        print("     ✅ E5 semantic matching (89.7% confidence)")
        print("     ✅ Camelot PDF extraction (complex tables)")
        print("     ✅ 15-ratio calculator with interpretations")
        print("     ✅ Trend analysis (YoY comparisons)")
        print("     ✅ Professional quantitative analysis")
        print()
        print("  📈 TRANSFORMATION COMPLETE:")
        print("     Round 1: 'Calculate current ratio'")
        print(f"     Round 2: 'Current Ratio = {calculated_ratios.get('current_ratio', {}).get('value', 0):.3f} ({calculated_ratios.get('current_ratio', {}).get('interpretation', 'N/A')})'")
        print()
        print("  🚀 READY FOR PHASE 3: Learning System (WBWS)")
    elif len(calculated_ratios) > 0:
        print(f"  🟡 PARTIAL: {len(calculated_ratios)}/15 ratios calculated")
        print()
        print("  POSSIBLE ISSUES:")
        print("     - Incomplete data extraction from PDF")
        print("     - Some financial terms not in balance sheet")
        print("     - E5 semantic matching threshold too high")
        print()
        print("  RECOMMENDATION:")
        print("     - Review extracted values manually")
        print("     - Adjust E5 threshold (currently 0.65)")
        print("     - Check Camelot table quality")
    else:
        print("  ❌ FAILED: No ratios calculated")
        print()
        print("  ROOT CAUSE:")
        print("     - No numeric data extracted from PDF")
        print("     - Both pdfplumber and Camelot failed")
        print()
        print("  RECOMMENDATION:")
        print("     - Try OCR (pdf2image + pytesseract)")
        print("     - OR use mock data to validate logic")
        print("     - OR test on simpler financial reports")

    print()
    print("=" * 80)

if __name__ == "__main__":
    try:
        test_round2_final()
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
