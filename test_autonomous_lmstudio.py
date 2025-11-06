#!/usr/bin/env python3
"""
Test Autonomous System with REAL LMStudio
"""

import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from src.autonomous.autonomous_orchestrator import AutonomousOrchestrator
import tempfile
import os


def create_test_documents():
    """Create test documents in temp folder"""
    temp_dir = tempfile.mkdtemp(prefix="destiny_test_")
    
    # Financial document
    with open(os.path.join(temp_dir, "Q4_2023_Revenue_Report.txt"), 'w') as f:
        f.write("""
Q4 2023 Financial Report

Revenue: $10.5M (up 25% YoY)
EBITDA: $3.2M (30.5% margin)
Operating Income: $2.8M
Net Income: $2.1M

Key Highlights:
- Strong growth in Enterprise segment
- Improved margins due to operational efficiency
- Successful product launches in Q4

Outlook for 2024: Positive growth trajectory expected.
""")
    
    # Legal document
    with open(os.path.join(temp_dir, "Service_Agreement.txt"), 'w') as f:
        f.write("""
SERVICE AGREEMENT

This Agreement is entered into as of January 1, 2024.

PARTIES:
- Client: ABC Corporation
- Provider: XYZ Services Inc.

TERMS:
1. Services: Provider shall provide consulting services
2. Duration: 12 months
3. Fee: $50,000 per month
4. Termination: 30 days notice required

OBLIGATIONS:
- Provider shall maintain confidentiality
- Client shall provide necessary resources

LIMITATIONS:
- Liability limited to fees paid in prior 6 months
- No warranty beyond express terms
""")
    
    # Technical document
    with open(os.path.join(temp_dir, "System_Architecture.txt"), 'w') as f:
        f.write("""
SYSTEM ARCHITECTURE SPECIFICATION

Overview:
Multi-tier architecture with microservices

Components:
- Frontend: React SPA
- API Gateway: Node.js
- Backend Services: Python microservices
- Database: PostgreSQL + Redis
- Message Queue: RabbitMQ

Scalability:
- Horizontal scaling supported
- Load balancing with Nginx
- Auto-scaling based on metrics

Security:
- OAuth 2.0 authentication
- TLS encryption
- API rate limiting
""")
    
    return temp_dir


def main():
    print("=" * 80)
    print("AUTONOMOUS SYSTEM TEST - WITH REAL LMSTUDIO")
    print("=" * 80)
    print()
    
    # Create test documents
    print("📝 Creating test documents...")
    test_dir = create_test_documents()
    print(f"   Created in: {test_dir}")
    print()
    
    try:
        # Create orchestrator
        orchestrator = AutonomousOrchestrator()
        
        # Process folder
        print("\n" + "=" * 80)
        print("STARTING AUTONOMOUS ANALYSIS")
        print("=" * 80)
        print()
        
        results = orchestrator.process_folder(
            folder_path=test_dir,
            case_id="test_lmstudio_001"
        )
        
        # Print results
        print("\n" + "=" * 80)
        print("RESULTS")
        print("=" * 80)
        print()
        
        print(f"📊 Case ID: {results['case_id']}")
        print(f"📁 Folder: {results['folder']}")
        print(f"📄 Files: {results['summary']['total_files']}")
        print(f"🎯 Tasks: {results['summary']['total_tasks']}")
        print(f"✅ Successful agents: {results['summary']['successful_agents']}")
        print()
        
        if results['findings']:
            print("🔍 Key Findings:")
            for i, finding in enumerate(results['findings'], 1):
                print(f"\n{i}. [{finding['agent'].upper()}] {finding['category']}")
                print(f"   Confidence: {finding['confidence']:.1%}")
                print(f"   {finding['output'][:200]}...")
        
        print("\n" + "=" * 80)
        print("TEST COMPLETE")
        print("=" * 80)
        
        # Check if LMStudio was used
        llm_used = orchestrator.llm is not None
        print(f"\n🔌 LMStudio Used: {'✅ YES' if llm_used else '❌ NO (fallback mode)'}")
        
        if llm_used:
            print("\n🎉 SUCCESS! System is using REAL LMStudio!")
        else:
            print("\n⚠️  Running in fallback mode. Check LMStudio connection.")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        import shutil
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
            print(f"\n🧹 Cleaned up test directory")


if __name__ == "__main__":
    main()
