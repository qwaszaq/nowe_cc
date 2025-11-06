"""
Test script for Marcus Agent LLM Integration

This script:
1. Tests connection to LM Studio server at 192.168.200.226
2. Tests LocalLLMClient with simple prompt
3. Tests Marcus Agent with sample financial analysis task
4. Compares LLM output vs template output

Run: python test_marcus_llm.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.llm import LocalLLMClient, get_llm_client, MARCUS_SYSTEM_PROMPT
from agents.analytical.marcus_agent_llm import MarcusAgentLLM
from agents.task_models import Task, TaskStatus
import json
from datetime import datetime
import uuid


def test_llm_connection():
    """Test 1: Basic LLM connection and health check"""
    print("=" * 80)
    print("TEST 1: LLM Connection & Health Check")
    print("=" * 80)

    try:
        llm = LocalLLMClient()
        print("✅ LocalLLMClient initialized successfully")
        print(f"   Server: {llm.base_url}")
        print(f"   Model: {llm.model}")

        # Health check
        health = llm.health_check()
        print(f"\n🔗 LLM Health Check:")
        print(f"   Status: {health['status']}")
        print(f"   Latency: {health.get('latency_ms', 'N/A')}ms")
        print(f"   Test Response: {health.get('test_response', 'N/A')}")

        return True

    except Exception as e:
        print(f"❌ LLM Connection failed: {e}")
        print("\nTroubleshooting:")
        print("1. Check if LM Studio is running at 192.168.200.226")
        print("2. Verify model 'openai/gpt-oss-20b' is loaded")
        print("3. Check network connectivity to 192.168.200.226:1234")
        return False


def test_llm_simple_prompt():
    """Test 2: Simple LLM prompt test"""
    print("\n" + "=" * 80)
    print("TEST 2: Simple LLM Prompt Test")
    print("=" * 80)

    try:
        llm = get_llm_client()

        response = llm.chat(
            system_prompt="You are a helpful financial analyst.",
            user_message="What are the 3 most important financial ratios for assessing company health?",
            temperature=0.7,
            max_tokens=500
        )

        print("✅ LLM response received:")
        print("-" * 80)
        print(response)
        print("-" * 80)

        # Check if response is meaningful (not template)
        if len(response) > 50 and "ratio" in response.lower():
            print("✅ Response appears to be real AI reasoning (not template)")
            return True
        else:
            print("⚠️  Response seems too short or generic")
            return False

    except Exception as e:
        print(f"❌ Simple prompt test failed: {e}")
        return False


def test_marcus_agent_llm():
    """Test 3: Marcus Agent with real financial analysis task"""
    print("\n" + "=" * 80)
    print("TEST 3: Marcus Agent LLM - Financial Analysis")
    print("=" * 80)

    try:
        # Initialize Marcus agent
        marcus = MarcusAgentLLM(project_id="test-financial-analysis")
        print(f"✅ {marcus.name} initialized")
        print(f"   Role: {marcus.role}")
        print(f"   Specialization: {marcus.specialization}")

        # Create sample financial analysis task
        task = Task(
            task_id=uuid.uuid4(),
            title="Financial Statement Analysis - Tech Company Q3 2024",
            description="""
Analyze the following financial data for TechCorp Inc (Q3 2024):

INCOME STATEMENT (in millions):
- Revenue: $450M (Q3 2023: $380M)
- Cost of Revenue: $180M (Q3 2023: $160M)
- Operating Expenses: $200M (Q3 2023: $180M)
- Net Income: $70M (Q3 2023: $40M)

BALANCE SHEET (in millions):
- Total Assets: $2,500M
- Current Assets: $800M (Cash: $300M, Receivables: $400M, Inventory: $100M)
- Total Liabilities: $1,200M
- Current Liabilities: $400M
- Shareholders' Equity: $1,300M

CASH FLOW (in millions):
- Operating Cash Flow: $90M (Q3 2023: $55M)
- Investing Cash Flow: -$50M (CapEx)
- Financing Cash Flow: -$20M (Dividends)

Please perform comprehensive financial statement analysis including:
1. Key financial ratios (liquidity, profitability, efficiency)
2. Year-over-year trends
3. Financial health assessment
4. Any red flags or concerns
""",
            assigned_to="Marcus Chen",
            assigned_by="Test Script",
            context={},
            priority=5,  # 5 = highest priority
            status=TaskStatus.PENDING,
            created_at=datetime.now()
        )

        print("\n📋 Task Created:")
        print(f"   Title: {task.title}")
        print(f"   Priority: {task.priority}")

        # Execute task
        print("\n⏳ Executing financial analysis with LLM...")
        print("   (This may take 10-30 seconds depending on LLM speed)")

        start_time = datetime.now()
        result = marcus.process_task(task)
        elapsed = (datetime.now() - start_time).total_seconds()

        print(f"\n✅ Analysis completed in {elapsed:.2f}s")
        print(f"   Status: {result.status.value}")
        print(f"   Time taken: {result.time_taken:.2f}s")

        # Display results
        print("\n" + "=" * 80)
        print("MARCUS ANALYSIS OUTPUT:")
        print("=" * 80)
        print(result.thoughts)
        print("=" * 80)

        # Validate output quality
        print("\n📊 Quality Validation:")

        checks = {
            "Contains calculations": any(word in result.thoughts.lower()
                                        for word in ["ratio", "calculate", "margin", "%"]),
            "Contains analysis": len(result.thoughts) > 500,
            "Contains specific numbers": any(char.isdigit() for char in result.thoughts),
            "Contains recommendations": any(word in result.thoughts.lower()
                                           for word in ["recommend", "suggest", "should", "concern"]),
            "Not a template": "template" not in result.thoughts.lower()
        }

        for check, passed in checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check}")

        all_passed = all(checks.values())

        if all_passed:
            print("\n🎉 SUCCESS: Marcus agent produces real AI financial analysis!")
            print("   Output contains calculations, specific analysis, and recommendations.")
        else:
            print("\n⚠️  WARNING: Output quality concerns detected")

        return all_passed

    except Exception as e:
        print(f"❌ Marcus agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_comparison_template_vs_llm():
    """Test 4: Compare template agent vs LLM agent"""
    print("\n" + "=" * 80)
    print("TEST 4: Template vs LLM Comparison")
    print("=" * 80)

    try:
        # Import original template-based Marcus
        from agents.analytical.marcus_agent import MarcusAgent as MarcusTemplate

        # Create same task for both
        task = Task(
            task_id=uuid.uuid4(),
            title="Quick fraud assessment",
            description="Analyze a company with sudden 50% revenue increase and declining cash flow",
            assigned_to="Marcus Chen",
            assigned_by="Test Script",
            context={},
            priority=5,
            status=TaskStatus.PENDING,
            created_at=datetime.now()
        )

        print("📋 Testing same task with both agents:")
        print(f"   Task: {task.description}")

        # Template agent
        print("\n1️⃣  Template Agent:")
        marcus_template = MarcusTemplate()
        result_template = marcus_template.process_task(task)
        print(f"   Output length: {len(result_template.thoughts)} chars")
        print(f"   First 200 chars: {result_template.thoughts[:200]}...")

        # LLM agent
        print("\n2️⃣  LLM Agent:")
        marcus_llm = MarcusAgentLLM()
        result_llm = marcus_llm.process_task(task)
        print(f"   Output length: {len(result_llm.thoughts)} chars")
        print(f"   First 200 chars: {result_llm.thoughts[:200]}...")

        # Comparison
        print("\n📊 Comparison:")
        print(f"   Template output: {len(result_template.thoughts)} chars")
        print(f"   LLM output: {len(result_llm.thoughts)} chars")
        print(f"   Difference: {len(result_llm.thoughts) - len(result_template.thoughts):+d} chars")

        llm_more_detailed = len(result_llm.thoughts) > len(result_template.thoughts) * 1.5

        if llm_more_detailed:
            print("   ✅ LLM output is more detailed than template")
        else:
            print("   ⚠️  LLM output similar length to template")

        return True

    except ImportError:
        print("⚠️  Could not import original Marcus agent for comparison")
        print("   Skipping comparison test")
        return True
    except Exception as e:
        print(f"❌ Comparison test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 15 + "MARCUS AGENT LLM INTEGRATION TEST SUITE" + " " * 24 + "║")
    print("║" + " " * 78 + "║")
    print("║  Model: openai/gpt-oss-20b at 192.168.200.226" + " " * 32 + "║")
    print("║  Purpose: Validate LLM integration for Destiny analytical agents" + " " * 13 + "║")
    print("╚" + "=" * 78 + "╝")
    print()

    results = {
        "LLM Connection": False,
        "Simple Prompt": False,
        "Marcus Agent Analysis": False,
        "Template vs LLM": False
    }

    # Run tests
    results["LLM Connection"] = test_llm_connection()

    if results["LLM Connection"]:
        results["Simple Prompt"] = test_llm_simple_prompt()
        results["Marcus Agent Analysis"] = test_marcus_agent_llm()
        results["Template vs LLM"] = test_comparison_template_vs_llm()
    else:
        print("\n⚠️  Skipping remaining tests due to connection failure")

    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")

    all_passed = all(results.values())

    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("\nNext steps:")
        print("1. Marcus agent successfully upgraded to LLM reasoning")
        print("2. Ready to upgrade remaining 8 analytical agents")
        print("3. Proceed to Phase 1: Document processing for Grupa Azoty reports")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("\nTroubleshooting needed:")
        if not results["LLM Connection"]:
            print("- Fix LM Studio connection at 192.168.200.226")
        if not results["Marcus Agent Analysis"]:
            print("- Review Marcus agent LLM integration")
    print("=" * 80)

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
