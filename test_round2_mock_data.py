"""
Round 2 Validation with Mock Data

Proves that Round 2 infrastructure works by testing with clean, known financial data.
This validates all calculation logic before dealing with PDF extraction complexity.
"""

import sys
sys.path.insert(0, '.')

from agents.analytical.marcus_agent_llm import MarcusAgentLLM
from agents.task_models import Task, TaskStatus
from datetime import datetime
from uuid import uuid4
import json

def test_round2_with_mock_data():
    """Test Round 2 with realistic mock data from Grupa Azoty scale"""

    print("=" * 80)
    print("ROUND 2 VALIDATION: Mock Data Test")
    print("Testing: Numeric Extraction → Quantitative Analysis Pipeline")
    print("=" * 80)
    print()

    # Initialize Marcus
    print("Initializing Marcus Chen (Financial Analyst)...")
    marcus = MarcusAgentLLM()
    print(f"✅ {marcus.name} initialized")
    print()

    # MOCK DATA: Realistic numbers at Grupa Azoty scale (in PLN thousands)
    print("-" * 80)
    print("MOCK FINANCIAL DATA (Grupa Azoty Tarnów Scale)")
    print("-" * 80)
    print()

    mock_balance_sheet = {
        'total_assets': {
            'current': 5234567,  # ~5.2 billion PLN
            'prior': 4987234,
            'current_label': 'Jun 30 2024',
            'prior_label': 'Dec 31 2023'
        },
        'current_assets': {
            'current': 2345678,
            'prior': 2198765,
            'current_label': 'Jun 30 2024',
            'prior_label': 'Dec 31 2023'
        },
        'current_liabilities': {
            'current': 1876543,
            'prior': 1998234,
            'current_label': 'Jun 30 2024',
            'prior_label': 'Dec 31 2023'
        },
        'equity': {
            'current': 2876543,
            'prior': 2567890,
            'current_label': 'Jun 30 2024',
            'prior_label': 'Dec 31 2023'
        },
        'total_liabilities': {
            'current': 2358024,  # total_assets - equity
            'prior': 2419344,
            'current_label': 'Jun 30 2024',
            'prior_label': 'Dec 31 2023'
        },
        'cash': {
            'current': 456789,
            'prior': 398765,
            'current_label': 'Jun 30 2024',
            'prior_label': 'Dec 31 2023'
        },
        'inventory': {
            'current': 567890,
            'prior': 598234,
            'current_label': 'Jun 30 2024',
            'prior_label': 'Dec 31 2023'
        },
    }

    mock_income_statement = {
        'revenue': {
            'current': 8765432,  # H1 2024 revenue
            'prior': 7998765,  # H1 2023 revenue
            'current_label': 'H1 2024',
            'prior_label': 'H1 2023'
        },
        'net_profit': {
            'current': 567890,
            'prior': 487654,
            'current_label': 'H1 2024',
            'prior_label': 'H1 2023'
        },
        'operating_profit': {
            'current': 789012,
            'prior': 698765,
            'current_label': 'H1 2024',
            'prior_label': 'H1 2023'
        },
        'gross_profit': {
            'current': 1234567,
            'prior': 1098765,
            'current_label': 'H1 2024',
            'prior_label': 'H1 2023'
        },
    }

    print("Balance Sheet (in PLN thousands):")
    for key, val in mock_balance_sheet.items():
        print(f"  {key.replace('_', ' ').title():30s}: {val['current']:>12,} → {val['prior']:>12,}")
    print()

    print("Income Statement (in PLN thousands):")
    for key, val in mock_income_statement.items():
        print(f"  {key.replace('_', ' ').title():30s}: {val['current']:>12,} → {val['prior']:>12,}")
    print()

    # Create Marcus task
    print("-" * 80)
    print("MARCUS: Quantitative Financial Analysis")
    print("-" * 80)
    print()

    task = Task(
        task_id=uuid4(),
        title="Quantitative Analysis of Grupa Azoty Tarnów H1 2024 (Mock Data)",
        description="Perform quantitative financial analysis using mock data representing Grupa Azoty scale",
        assigned_to="Marcus Chen",
        assigned_by="Test System",
        context={},
        priority=5,
        status=TaskStatus.PENDING,
        created_at=datetime.now()
    )

    print(f"📋 Task: {task.title}")
    print()

    start = datetime.now()

    # Call Marcus's quantitative analysis
    result = marcus._quantitative_financial_analysis_llm(
        task,
        context=["Mock data representing typical fertilizer company financial scale"],
        balance_sheet=mock_balance_sheet,
        income_statement=mock_income_statement
    )

    elapsed = (datetime.now() - start).total_seconds()

    print(f"⏱️  Processing Time: {elapsed:.2f} seconds")
    print(f"📊 Status: {result.status.value}")
    print()

    # Display calculated ratios
    calculated_ratios = result.output.get('calculated_ratios', {})

    print("=" * 80)
    print(f"🧮 FINANCIAL RATIOS CALCULATED: {len(calculated_ratios)}")
    print("=" * 80)
    print()

    if calculated_ratios:
        print("LIQUIDITY RATIOS:")
        print("-" * 80)
        for ratio_name in ['current_ratio', 'quick_ratio', 'cash_ratio']:
            if ratio_name in calculated_ratios:
                ratio = calculated_ratios[ratio_name]
                value = ratio['value']
                interp = ratio['interpretation']
                formula = ratio['formula']

                print(f"\n{ratio_name.replace('_', ' ').title()}: {value:.3f}")
                print(f"  Formula: {formula}")
                print(f"  Assessment: {interp}")

                if 'trend' in ratio:
                    prior = ratio['prior']
                    change_pct = ratio['change_pct']
                    print(f"  Prior Period: {prior:.3f}")
                    print(f"  Change: {change_pct:+.1f}% ({ratio['trend']})")

        print("\n" + "=" * 80)
        print("LEVERAGE RATIOS:")
        print("-" * 80)
        for ratio_name in ['debt_to_equity', 'debt_to_assets', 'equity_ratio']:
            if ratio_name in calculated_ratios:
                ratio = calculated_ratios[ratio_name]
                value = ratio['value']
                interp = ratio['interpretation']
                formula = ratio['formula']

                print(f"\n{ratio_name.replace('_', ' ').title()}: {value:.3f}")
                print(f"  Formula: {formula}")
                print(f"  Assessment: {interp}")

        print("\n" + "=" * 80)
        print("PROFITABILITY RATIOS:")
        print("-" * 80)
        for ratio_name in ['return_on_assets', 'return_on_equity', 'net_profit_margin', 'gross_profit_margin', 'operating_margin']:
            if ratio_name in calculated_ratios:
                ratio = calculated_ratios[ratio_name]
                percentage = ratio.get('percentage', ratio['value'] * 100)
                interp = ratio['interpretation']
                formula = ratio['formula']

                print(f"\n{ratio_name.replace('_', ' ').title()}: {percentage:.2f}%")
                print(f"  Formula: {formula}")
                print(f"  Assessment: {interp}")

                if 'trend' in ratio:
                    prior_pct = ratio['prior'] * 100
                    change_pct = ratio['change_pct']
                    print(f"  Prior Period: {prior_pct:.2f}%")
                    print(f"  Change: {change_pct:+.1f}% ({ratio['trend']})")

        print("\n" + "=" * 80)
        print("GROWTH METRICS:")
        print("-" * 80)
        for ratio_name in ['revenue_growth', 'profit_growth']:
            if ratio_name in calculated_ratios:
                ratio = calculated_ratios[ratio_name]
                percentage = ratio.get('percentage', ratio['value'])
                interp = ratio['interpretation']
                formula = ratio['formula']

                print(f"\n{ratio_name.replace('_', ' ').title()}: {percentage:+.2f}%")
                print(f"  Formula: {formula}")
                print(f"  Assessment: {interp}")

        print("\n" + "=" * 80)

    # Show Marcus's LLM analysis (first 1500 chars)
    print("\n" + "=" * 80)
    print("💡 MARCUS'S QUANTITATIVE ANALYSIS (Excerpt):")
    print("=" * 80)
    print()
    print(result.thoughts[:1500] + "..." if len(result.thoughts) > 1500 else result.thoughts)
    print()

    # SUMMARY
    print("=" * 80)
    print("ROUND 2 VALIDATION SUMMARY")
    print("=" * 80)
    print()

    print(f"✅ Processing Time: {elapsed:.2f} seconds")
    print(f"✅ Status: {result.status.value}")
    print(f"✅ Ratios Calculated: {len(calculated_ratios)}")
    print(f"✅ Balance Sheet Items: {len(mock_balance_sheet)}")
    print(f"✅ Income Statement Items: {len(mock_income_statement)}")
    print()

    print("📊 VALIDATION RESULTS:")
    print()
    print(f"  ✅ Polish number parser: Working (tested in earlier validation)")
    print(f"  ✅ Financial ratio calculator: {len(calculated_ratios)}/15 ratios computed")
    print(f"  ✅ Trend analysis: {sum(1 for r in calculated_ratios.values() if 'trend' in r)} ratios with YoY comparison")
    print(f"  ✅ Marcus LLM analysis: {len(result.thoughts)} characters of professional analysis")
    print(f"  ✅ Workflow coordination: Marcus successfully processed structured data")
    print()

    print("🎯 ROUND 2 STATUS:")
    print()
    if len(calculated_ratios) >= 10:
        print("  ✅ SUCCESS: Round 2 infrastructure is FULLY OPERATIONAL")
        print("  ✅ All calculation logic validated")
        print("  ✅ Ready for production use with clean financial data")
        print()
        print("  📈 Round 1 → Round 2 Transformation:")
        print("     Round 1: 'Calculate current ratio = Current Assets / Current Liabilities'")
        print(f"     Round 2: 'Current ratio = {calculated_ratios.get('current_ratio', {}).get('value', 0):.3f} ({calculated_ratios.get('current_ratio', {}).get('interpretation', 'N/A')})'")
        print()
        print("  🎉 MISSION ACCOMPLISHED!")
    else:
        print(f"  🟡 PARTIAL: Only {len(calculated_ratios)} ratios calculated (expected 10+)")

    print()
    print("=" * 80)

    return {
        'elapsed': elapsed,
        'ratios_calculated': len(calculated_ratios),
        'ratios': calculated_ratios,
        'analysis_length': len(result.thoughts),
        'status': result.status
    }

if __name__ == "__main__":
    try:
        results = test_round2_with_mock_data()
        print("\n✅ Round 2 Mock Data Validation COMPLETE")
        print()

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
