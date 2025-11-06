#!/usr/bin/env python3
"""
Test CBA Documents Detection and Classification

Tests the investigative detection on real CBA documents without full system initialization.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.autonomous.document_discovery import AutomaticTaskGenerator


def test_cba_folder():
    """Test CBA document detection"""
    print("\n" + "="*80)
    print("🔍 INVESTIGATIVE SYSTEM TEST - CBA DOCUMENTS")
    print("="*80)
    
    folder_path = "/Users/artur/coursor-agents-destiny-folder/testdocsLLM"
    
    print(f"\n📂 Analyzing folder: {folder_path}")
    print("-" * 80)
    
    # Initialize generator
    generator = AutomaticTaskGenerator()
    
    # Process folder
    try:
        result = generator.process_folder(folder_path)
        
        print("\n" + "="*80)
        print("📊 CLASSIFICATION RESULTS")
        print("="*80)
        
        # Summary
        print(f"\n📄 Total Files: {result['summary']['total']}")
        print(f"📦 Total Size: {result['summary']['total_size_mb']:.2f} MB")
        print(f"\n📋 Files by Type:")
        for file_type, count in result['summary']['by_type'].items():
            print(f"   - {file_type}: {count}")
        
        # Classification breakdown
        print(f"\n🏷️  Classification Breakdown:")
        categories = {}
        investigation_types = {}
        
        for file in result['files']:
            cat = file['category']
            categories[cat] = categories.get(cat, 0) + 1
            
            inv_type = file.get('investigation_type', 'none')
            if inv_type != 'none':
                investigation_types[inv_type] = investigation_types.get(inv_type, 0) + 1
        
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"   - {cat}: {count} files")
        
        if investigation_types:
            print(f"\n🔍 Investigation Types Detected:")
            for inv_type, count in sorted(investigation_types.items(), key=lambda x: x[1], reverse=True):
                print(f"   - {inv_type}: {count} files")
        
        # Detailed file analysis
        print(f"\n" + "="*80)
        print("📝 DETAILED FILE ANALYSIS")
        print("="*80)
        
        investigative_files = [f for f in result['files'] if f['category'] == 'investigative']
        other_files = [f for f in result['files'] if f['category'] != 'investigative']
        
        if investigative_files:
            print(f"\n🔍 INVESTIGATIVE FILES ({len(investigative_files)}):")
            print("-" * 80)
            for i, file in enumerate(investigative_files, 1):
                print(f"\n{i}. {file['filename']}")
                print(f"   Category: {file['category']}")
                print(f"   Confidence: {file['confidence']:.2f}")
                print(f"   Investigation Type: {file.get('investigation_type', 'none')}")
                print(f"   Size: {file['size_mb']:.2f} MB")
                if 'suggested_analyses' in file:
                    print(f"   Suggested Analyses: {', '.join(file['suggested_analyses'][:3])}")
        
        if other_files:
            print(f"\n📄 OTHER FILES ({len(other_files)}):")
            print("-" * 80)
            for i, file in enumerate(other_files, 1):
                print(f"\n{i}. {file['filename']}")
                print(f"   Category: {file['category']}")
                print(f"   Confidence: {file['confidence']:.2f}")
                print(f"   Size: {file['size_mb']:.2f} MB")
        
        # Task generation
        print(f"\n" + "="*80)
        print("📋 GENERATED TASKS")
        print("="*80)
        
        print(f"\nTotal Tasks: {len(result['tasks'])}")
        
        for i, task in enumerate(result['tasks'], 1):
            print(f"\n--- Task {i} ---")
            print(f"Category: {task['category']}")
            print(f"Priority: {task['priority']}/100")
            print(f"Agents: {', '.join(task['agents'])}")
            print(f"Files: {task['file_count']}")
            print(f"Investigation Type: {task.get('investigation_type', 'none')}")
            print(f"Analyses: {', '.join(task['analyses'][:3])}")
            
            if 'investigative' in task['agents']:
                print(f"\n🔍 ✅ ROUTED TO INVESTIGATIVE TEAM!")
        
        # Summary verdict
        print(f"\n" + "="*80)
        print("✅ DETECTION VERDICT")
        print("="*80)
        
        investigative_count = len(investigative_files)
        total_count = len(result['files'])
        
        print(f"\n📊 Detection Rate:")
        print(f"   Investigative: {investigative_count}/{total_count} files ({investigative_count/total_count*100:.1f}%)")
        
        if investigative_count > 0:
            print(f"\n✅ SUCCESS: System detected {investigative_count} investigative documents!")
            print(f"   These will be routed to the Investigative Team (9 specialized agents)")
            print(f"   Investigation types: {', '.join(investigation_types.keys())}")
        else:
            print(f"\n⚠️  No investigative content detected")
            print(f"   Documents will be processed by basic agents")
        
        # What would happen next
        print(f"\n" + "="*80)
        print("🚀 WHAT HAPPENS NEXT (in full system)")
        print("="*80)
        
        for task in result['tasks']:
            if 'investigative' in task['agents']:
                inv_type = task.get('investigation_type', 'comprehensive')
                print(f"\n🔍 Investigation: {task['category']}")
                print(f"   Type: {inv_type}")
                print(f"   Files: {task['file_count']}")
                
                if inv_type == 'comprehensive':
                    print(f"\n   Phases:")
                    print(f"   1. Viktor Kovalenko - Investigation planning")
                    print(f"   2. Elena Volkov - OSINT gathering")
                    print(f"   3. Marcus Chen - Financial analysis")
                    print(f"   4. Sofia Martinez - Market research")
                    print(f"   5. Adrian Kowalski - Legal review")
                    print(f"   6. Maya Patel - Data correlation")
                    print(f"   7. Damian Rousseau - Critical review")
                    print(f"   8. Lucas Rivera - Final report synthesis")
                elif inv_type == 'osint':
                    print(f"   Agent: Elena Volkov (OSINT Specialist)")
                elif inv_type == 'financial':
                    print(f"   Agent: Marcus Chen (Financial Analyst)")
                elif inv_type == 'legal':
                    print(f"   Agent: Adrian Kowalski (Legal Analyst)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_cba_folder()
    sys.exit(0 if success else 1)
