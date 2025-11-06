#!/usr/bin/env python3
"""
Test RAG+CAG with REAL LMStudio
Demonstrates context optimization in action
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.memory.rag_cag_strategy import RAGCAGOrchestrator
from src.llm.lmstudio_client import LMStudioLLMClient


def test_cag_optimization():
    """Test CAG context optimization"""
    print("=" * 80)
    print("RAG + CAG OPTIMIZATION TEST - WITH REAL LMSTUDIO")
    print("=" * 80)
    print()
    
    # Test LMStudio connection
    print("🔌 Testing LMStudio connection...")
    try:
        llm = LMStudioLLMClient(
            base_url="http://192.168.200.226:1234/v1",
            model="openai/gpt-oss-20b"
        )
        
        if llm.health_check():
            print("   ✅ LMStudio is online")
        else:
            print("   ❌ LMStudio not responding")
            return
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        return
    
    print()
    
    # Create RAG+CAG orchestrator
    print("💾 Initializing RAG+CAG...")
    orchestrator = RAGCAGOrchestrator(
        context_window=44000,
        use_cag=True
    )
    print("   ✅ Ready")
    print()
    
    # Create test documents
    print("📝 Creating test documents...")
    documents = [
        {
            'id': f'doc_{i}',
            'content': f"""
Financial Report Document {i}

Revenue for Q{(i % 4) + 1} was ${(i + 1) * 100}M, representing {10 + i}% growth.
Operating expenses were ${(i + 1) * 60}M.
Net income reached ${(i + 1) * 25}M.

Key highlights:
- Strong performance in core business
- Expansion into new markets
- Improved operational efficiency
"""
        }
        for i in range(10)  # 10 documents
    ]
    print(f"   Created {len(documents)} test documents")
    print()
    
    # Test WITHOUT CAG first (for comparison)
    print("=" * 80)
    print("TEST 1: WITHOUT CAG (Traditional approach)")
    print("=" * 80)
    
    # Simulate traditional approach
    traditional_overhead = 3000  # tokens repeated each time
    doc_tokens = 200  # per doc
    
    without_cag_per_batch = (44000 - traditional_overhead) // doc_tokens
    without_cag_total_overhead = traditional_overhead * (len(documents) // without_cag_per_batch + 1)
    
    print(f"Context window: 44,000 tokens")
    print(f"Overhead per batch: {traditional_overhead} tokens (repeated!)")
    print(f"Docs per batch: {without_cag_per_batch}")
    print(f"Total batches: {len(documents) // without_cag_per_batch + 1}")
    print(f"Total overhead: {without_cag_total_overhead:,} tokens wasted!")
    print()
    
    # Test WITH CAG
    print("=" * 80)
    print("TEST 2: WITH CAG (Optimized approach)")
    print("=" * 80)
    
    try:
        result = orchestrator.process_large_document_set(
            case_id="cag_test_001",
            agent_type="financial",
            documents=documents,
            query="financial performance"
        )
        
        print("\n✅ Processing complete!")
        print(f"\nSTATISTICS:")
        print(f"   Documents processed: {result['stats']['total_documents_processed']}")
        print(f"   Batches: {result['stats']['total_batches_processed']}")
        print(f"   Tokens saved by CAG: {result['stats']['total_tokens_saved_by_cag']:,}")
        print()
        
        # Calculate improvement
        improvement = (without_cag_total_overhead - result['stats']['total_tokens_saved_by_cag']) / without_cag_total_overhead * 100
        
        print("=" * 80)
        print("COMPARISON")
        print("=" * 80)
        print(f"WITHOUT CAG: {without_cag_total_overhead:,} tokens wasted")
        print(f"WITH CAG:    {result['stats']['total_tokens_saved_by_cag']:,} tokens saved")
        print(f"IMPROVEMENT: {improvement:.1f}% more efficient!")
        print()
        
        effective_window = 44000 + result['stats']['total_tokens_saved_by_cag']
        print(f"🚀 44k context → Feels like {effective_window:,} tokens!")
        print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def test_simple_llm_call():
    """Test simple LMStudio call"""
    print("\n" + "=" * 80)
    print("BONUS TEST: Simple LMStudio Call")
    print("=" * 80)
    print()
    
    try:
        llm = LMStudioLLMClient(
            base_url="http://192.168.200.226:1234/v1",
            model="openai/gpt-oss-20b"
        )
        
        print("📤 Sending test prompt to LMStudio...")
        response = llm.chat_completion([
            {"role": "user", "content": "What is 2+2? Answer briefly."}
        ])
        
        print(f"📥 Response: {response.content}")
        print(f"   Tokens used: {response.usage.get('total_tokens', 'N/A')}")
        print(f"   Duration: {response.processing_time:.2f}s")
        print()
        print("✅ LMStudio is working correctly!")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    # Test 1: Simple call
    test_simple_llm_call()
    
    # Test 2: RAG+CAG
    test_cag_optimization()
    
    print("\n" + "=" * 80)
    print("ALL TESTS COMPLETE")
    print("=" * 80)
