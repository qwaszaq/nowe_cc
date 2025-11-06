#!/usr/bin/env python3
"""
Simple Test: Investigative Content Detection

Tests ONLY the classification logic without full system initialization.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.autonomous.document_discovery import IntelligentFileClassifier, AutomaticTaskGenerator


def test_investigative_classification():
    """Test that investigative keywords are detected"""
    print("\n" + "="*80)
    print("TEST: Investigative Content Classification")
    print("="*80)
    
    classifier = IntelligentFileClassifier()
    
    # Test cases
    test_cases = [
        {
            'name': 'Investigation Report',
            'content': """
                INVESTIGATION REPORT
                This document details our investigation into fraud allegations.
                OSINT intelligence gathering revealed suspicious activity.
                Multiple witnesses provided testimony. Evidence collected.
            """,
            'expected_category': 'investigative',
            'file': {
                'path': '/test/investigation.pdf',
                'filename': 'investigation_report.pdf',
                'extension': '.pdf',
                'type': 'pdf',
                'size_bytes': 10000,
                'size_mb': 0.01,
            }
        },
        {
            'name': 'CBA Report (Polish)',
            'content': """
                RAPORT CBA
                Centralne Biuro Antykorupcyjne prowadzi śledztwo w sprawie korupcji.
                Prokuratura nadzoruje postępowanie. Wykryto aferę korupcyjną.
                Zeznania świadków i zebrane dowody wskazują na przestępstwo.
            """,
            'expected_category': 'investigative',
            'file': {
                'path': '/test/raport_cba.pdf',
                'filename': 'raport_cba_2024.pdf',
                'extension': '.pdf',
                'type': 'pdf',
                'size_bytes': 15000,
                'size_mb': 0.015,
            }
        },
        {
            'name': 'Financial Report (Not Investigative)',
            'content': """
                QUARTERLY FINANCIAL REPORT Q4 2024
                Revenue increased by 25% YoY to $10.5M.
                Profit margins improved to 30.5%.
                Balance sheet shows strong financial position.
            """,
            'expected_category': 'financial',
            'file': {
                'path': '/test/q4_report.xlsx',
                'filename': 'Q4_2024_Financial_Report.xlsx',
                'extension': '.xlsx',
                'type': 'excel',
                'size_bytes': 50000,
                'size_mb': 0.05,
            }
        },
        {
            'name': 'Legal Contract (Not Investigative)',
            'content': """
                SERVICE AGREEMENT
                This contract establishes the terms and conditions between parties.
                Article 1: Scope of services
                Article 2: Payment terms
                Hereby agreed upon by both parties.
            """,
            'expected_category': 'legal',
            'file': {
                'path': '/test/contract.pdf',
                'filename': 'service_agreement.pdf',
                'extension': '.pdf',
                'type': 'pdf',
                'size_bytes': 30000,
                'size_mb': 0.03,
            }
        }
    ]
    
    print("\n📋 Running Classification Tests:\n")
    
    passed = 0
    failed = 0
    
    for test_case in test_cases:
        classification = classifier.classify_file(
            test_case['file'],
            test_case['content']
        )
        
        category = classification['category']
        confidence = classification['confidence']
        expected = test_case['expected_category']
        
        match = category == expected
        status = "✅" if match else "❌"
        
        print(f"{status} {test_case['name']}")
        print(f"   Expected: {expected}, Got: {category} (confidence: {confidence:.2f})")
        
        if 'all_scores' in classification:
            print(f"   Scores: {classification['all_scores']}")
        
        print()
        
        if match:
            passed += 1
        else:
            failed += 1
    
    print("="*80)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*80)
    
    return failed == 0


def test_investigation_type_detection():
    """Test that investigation types are correctly determined"""
    print("\n" + "="*80)
    print("TEST: Investigation Type Detection")
    print("="*80)
    
    classifier = IntelligentFileClassifier()
    
    test_cases = [
        {
            'name': 'Comprehensive Investigation',
            'scores': {
                'investigative': 25,
                'legal': 5,
                'financial': 3
            },
            'category': 'investigative',
            'expected_type': 'comprehensive'
        },
        {
            'name': 'Financial Investigation',
            'scores': {
                'financial': 10,
                'investigative': 5,
                'legal': 2
            },
            'category': 'financial',
            'expected_type': 'financial'
        },
        {
            'name': 'Legal Investigation',
            'scores': {
                'legal': 12,
                'investigative': 4,
                'financial': 1
            },
            'category': 'legal',
            'expected_type': 'legal'
        },
        {
            'name': 'OSINT Only',
            'scores': {
                'investigative': 8,
                'legal': 1,
                'financial': 1
            },
            'category': 'general',
            'expected_type': 'osint'
        },
        {
            'name': 'No Investigation',
            'scores': {
                'financial': 10,
                'investigative': 1,
                'legal': 2
            },
            'category': 'financial',
            'expected_type': 'none'
        }
    ]
    
    print("\n📋 Running Investigation Type Tests:\n")
    
    passed = 0
    failed = 0
    
    for test_case in test_cases:
        classification = {
            'category': test_case['category'],
            'all_scores': test_case['scores']
        }
        
        investigation_type = classifier.determine_investigation_type(
            classification,
            test_case['scores']
        )
        
        expected = test_case['expected_type']
        match = investigation_type == expected
        status = "✅" if match else "❌"
        
        print(f"{status} {test_case['name']}")
        print(f"   Expected: {expected}, Got: {investigation_type}")
        print(f"   Scores: {test_case['scores']}")
        print()
        
        if match:
            passed += 1
        else:
            failed += 1
    
    print("="*80)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*80)
    
    return failed == 0


def test_agent_selection():
    """Test agent selection logic"""
    print("\n" + "="*80)
    print("TEST: Agent Selection Logic")
    print("="*80)
    
    generator = AutomaticTaskGenerator()
    
    test_cases = [
        ('investigative', 'comprehensive', ['investigative']),
        ('investigative', 'osint', ['investigative']),
        ('financial', 'financial', ['investigative']),
        ('legal', 'legal', ['investigative']),
        ('financial', 'none', ['financial', 'data_science']),
        ('legal', 'none', ['legal', 'risk']),
        ('technical', 'none', ['architect', 'developer']),
        ('data', 'none', ['data_science']),
    ]
    
    print("\n📋 Running Agent Selection Tests:\n")
    
    passed = 0
    failed = 0
    
    for category, investigation_type, expected in test_cases:
        agents = generator._select_agents(category, investigation_type)
        
        match = agents == expected
        status = "✅" if match else "❌"
        
        print(f"{status} Category: {category}, Investigation: {investigation_type}")
        print(f"   Expected: {expected}, Got: {agents}")
        print()
        
        if match:
            passed += 1
        else:
            failed += 1
    
    print("="*80)
    print(f"Results: {passed} passed, {failed} failed")
    print("="*80)
    
    return failed == 0


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("INVESTIGATIVE CONTENT DETECTION - TEST SUITE")
    print("="*80)
    print("\nTesting classification and routing logic WITHOUT full system initialization")
    
    tests = [
        ("Investigative Classification", test_investigative_classification),
        ("Investigation Type Detection", test_investigation_type_detection),
        ("Agent Selection", test_agent_selection),
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
    print("\n" + "="*80)
    print("FINAL RESULTS")
    print("="*80)
    
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"   {status}: {test_name}")
    
    total_passed = sum(1 for _, passed in results if passed)
    total_tests = len(results)
    
    print(f"\n📊 Summary: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("\n🎉 ALL TESTS PASSED!")
        print("\n✅ Integration Components Validated:")
        print("   1. Investigative content detection (keywords + scoring)")
        print("   2. Investigation type determination (comprehensive, osint, financial, legal)")
        print("   3. Agent selection and routing (investigative team vs basic agents)")
        return 0
    else:
        print(f"\n⚠️  {total_tests - total_passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
