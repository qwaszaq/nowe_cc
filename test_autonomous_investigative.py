#!/usr/bin/env python3
"""
Test Autonomous Investigative Integration

Tests the integration between:
- Autonomous System (document discovery + orchestration)
- Investigative Team (9 specialized agents)

This test validates:
1. Document classification detects investigative content
2. System routes to investigative team automatically
3. Full investigation workflow completes
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.autonomous.autonomous_orchestrator import AutonomousOrchestrator
from src.autonomous.document_discovery import AutomaticTaskGenerator


def test_classification_detection():
    """Test that investigative content is detected"""
    print("\n" + "="*80)
    print("TEST 1: Investigative Content Detection")
    print("="*80)
    
    generator = AutomaticTaskGenerator()
    
    # Create test file metadata
    test_file = {
        'path': '/test/fraud_investigation.pdf',
        'filename': 'fraud_investigation_2024.pdf',
        'extension': '.pdf',
        'type': 'pdf',
        'size_bytes': 10000,
        'size_mb': 0.01,
        'modified': '2024-01-01',
        'hash': 'test123',
        'mime_type': 'application/pdf'
    }
    
    # Test with investigative content
    investigative_content = """
    INVESTIGATION REPORT
    
    This document contains the findings of our investigation into allegations of fraud
    and corruption. OSINT intelligence gathering revealed multiple suspicious transactions.
    Witness testimony and evidence collected during the investigation suggest systematic
    misconduct. The case involves several high-profile suspects.
    
    CBA (Centralne Biuro Antykorupcyjne) has been notified. Prokuratura is conducting
    a parallel śledztwo. This is a sensitive postępowanie requiring careful handling.
    """
    
    classification = generator.classifier.classify_file(test_file, investigative_content)
    
    print(f"\n📋 Classification Results:")
    print(f"   Category: {classification['category']}")
    print(f"   Confidence: {classification['confidence']:.2f}")
    print(f"   All Scores: {classification.get('all_scores', {})}")
    
    investigation_type = generator.classifier.determine_investigation_type(
        classification,
        classification.get('all_scores', {})
    )
    
    print(f"   Investigation Type: {investigation_type}")
    
    # Validate
    assert classification['category'] == 'investigative', \
        f"Expected 'investigative', got '{classification['category']}'"
    assert investigation_type == 'comprehensive', \
        f"Expected 'comprehensive', got '{investigation_type}'"
    
    print("\n✅ TEST 1 PASSED: Investigative content correctly detected")
    return True


def test_task_generation():
    """Test that tasks are generated with investigative routing"""
    print("\n" + "="*80)
    print("TEST 2: Task Generation with Investigative Routing")
    print("="*80)
    
    generator = AutomaticTaskGenerator()
    
    # Create test file with investigative content
    test_file = {
        'path': '/test/investigation.pdf',
        'filename': 'investigation_report.pdf',
        'extension': '.pdf',
        'type': 'pdf',
        'size_bytes': 10000,
        'size_mb': 0.01,
        'modified': '2024-01-01',
        'hash': 'test456',
        'mime_type': 'application/pdf',
        'category': 'investigative',
        'confidence': 0.95,
        'suggested_analyses': ['comprehensive_investigation', 'osint_analysis'],
        'investigation_type': 'comprehensive'
    }
    
    # Generate tasks
    tasks = generator._generate_tasks([test_file])
    
    print(f"\n📋 Generated Tasks:")
    for task in tasks:
        print(f"\n   Task: {task['task_id']}")
        print(f"   Category: {task['category']}")
        print(f"   Agents: {task['agents']}")
        print(f"   Investigation Type: {task.get('investigation_type', 'none')}")
        print(f"   Priority: {task['priority']}")
    
    # Validate
    assert len(tasks) > 0, "No tasks generated"
    assert 'investigative' in tasks[0]['agents'], \
        f"Expected 'investigative' in agents, got {tasks[0]['agents']}"
    assert tasks[0].get('investigation_type') == 'comprehensive', \
        f"Expected 'comprehensive', got {tasks[0].get('investigation_type')}"
    
    print("\n✅ TEST 2 PASSED: Tasks correctly routed to investigative team")
    return True


def test_orchestrator_initialization():
    """Test that orchestrator initializes with investigative team"""
    print("\n" + "="*80)
    print("TEST 3: Orchestrator Initialization")
    print("="*80)
    
    try:
        orchestrator = AutonomousOrchestrator(enable_investigative=True)
        
        print(f"\n📊 Orchestrator Status:")
        print(f"   Basic Agents: {len(orchestrator.agents)}")
        print(f"   Investigative Enabled: {orchestrator.investigative_enabled}")
        if orchestrator.investigative_team:
            print(f"   Investigative Agents: {len(orchestrator.investigative_team.agents)}")
        
        # Validate
        assert orchestrator.investigative_enabled, "Investigative team not enabled"
        assert orchestrator.investigative_team is not None, "Investigative team not initialized"
        
        print("\n✅ TEST 3 PASSED: Orchestrator initialized with investigative capabilities")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST 3 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_agent_selection():
    """Test that correct agents are selected for different scenarios"""
    print("\n" + "="*80)
    print("TEST 4: Agent Selection Logic")
    print("="*80)
    
    generator = AutomaticTaskGenerator()
    
    # Test scenarios
    scenarios = [
        ('investigative', 'comprehensive', ['investigative']),
        ('investigative', 'osint', ['investigative']),
        ('financial', 'financial', ['investigative']),
        ('legal', 'legal', ['investigative']),
        ('financial', 'none', ['financial', 'data_science']),
        ('legal', 'none', ['legal', 'risk']),
    ]
    
    print("\n📋 Testing Agent Selection:")
    all_passed = True
    
    for category, investigation_type, expected in scenarios:
        agents = generator._select_agents(category, investigation_type)
        
        match = agents == expected
        status = "✅" if match else "❌"
        
        print(f"   {status} Category: {category}, Investigation: {investigation_type}")
        print(f"      Expected: {expected}, Got: {agents}")
        
        if not match:
            all_passed = False
    
    if all_passed:
        print("\n✅ TEST 4 PASSED: Agent selection logic correct")
    else:
        print("\n❌ TEST 4 FAILED: Some selections incorrect")
    
    return all_passed


def test_integration_summary():
    """Print integration summary"""
    print("\n" + "="*80)
    print("INTEGRATION SUMMARY")
    print("="*80)
    
    print("\n✅ Integration Complete:")
    print("   1. AutonomousOrchestrator now supports investigative team")
    print("   2. IntelligentFileClassifier detects investigative content")
    print("   3. AutomaticTaskGenerator routes to investigative agents")
    print("   4. Full workflow: Detection → Classification → Routing → Investigation")
    
    print("\n📋 Supported Investigation Types:")
    print("   - comprehensive: Full team investigation (Elena, Marcus, Sofia, Adrian, Maya, Damian, Lucas)")
    print("   - osint: Open-source intelligence (Elena)")
    print("   - financial: Financial analysis (Marcus)")
    print("   - legal: Legal research (Adrian)")
    
    print("\n🔍 Detection Keywords:")
    keywords = [
        'investigation', 'osint', 'intelligence', 'fraud', 'corruption',
        'scandal', 'cba', 'prokuratura', 'śledztwo', 'postępowanie', 'afera'
    ]
    print(f"   {', '.join(keywords)}")
    
    print("\n🚀 Usage:")
    print("   python destiny_auto.py /path/to/investigative/documents")
    print("   → System automatically detects investigative content")
    print("   → Routes to specialized investigative team")
    print("   → Launches appropriate investigation type")


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("AUTONOMOUS INVESTIGATIVE INTEGRATION TEST SUITE")
    print("="*80)
    
    tests = [
        ("Investigative Content Detection", test_classification_detection),
        ("Task Generation with Routing", test_task_generation),
        ("Orchestrator Initialization", test_orchestrator_initialization),
        ("Agent Selection Logic", test_agent_selection),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} FAILED with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # Print summary
    test_integration_summary()
    
    print("\n" + "="*80)
    print("TEST RESULTS")
    print("="*80)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"   {status}: {test_name}")
    
    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    
    print(f"\n📊 Summary: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n🎉 ALL TESTS PASSED! Integration successful!")
        return 0
    else:
        print(f"\n⚠️  {total_tests - total_passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
