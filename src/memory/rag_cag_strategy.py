"""
RAG + CAG Integration Strategy
Complete implementation of Retrieval-Augmented + Cache-Augmented Generation
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from pathlib import Path
import time

from src.memory.cache_augmented_generation import CAGManager, SmartContextManager
from src.data.embedding_pipeline import DualEmbeddingSystem
from src.data.smart_router import SmartDatabaseRouter


@dataclass
class ProcessingStrategy:
    """Strategy for processing large document sets"""
    total_documents: int
    estimated_tokens_per_doc: int
    context_window: int
    batch_size: int
    total_batches: int
    use_cag: bool
    use_hierarchical_summary: bool


class RAGCAGOrchestrator:
    """
    Complete RAG + CAG Orchestrator
    
    Solves the 44k vs 200k problem by:
    1. RAG: Retrieving only relevant data (hot)
    2. CAG: Caching static components (cold)
    3. Hierarchical summarization
    4. Iterative refinement
    """
    
    def __init__(self, 
                 context_window: int = 44000,
                 use_cag: bool = True):
        """
        Initialize RAG+CAG orchestrator
        
        Args:
            context_window: Available context (44k local, 200k Claude)
            use_cag: Enable Cache-Augmented Generation
        """
        self.context_window = context_window
        self.use_cag = use_cag
        
        # Initialize components
        self.context_mgr = SmartContextManager(max_tokens=context_window)
        self.cag = CAGManager()
        self.embeddings = DualEmbeddingSystem()
        self.db_router = SmartDatabaseRouter()
        
        # Tracking
        self.stats = {
            'total_batches_processed': 0,
            'total_tokens_used': 0,
            'total_tokens_saved_by_cag': 0,
            'total_documents_processed': 0
        }
    
    def create_processing_strategy(self,
                                  case_id: str,
                                  agent_type: str,
                                  documents: List[Dict[str, Any]]) -> ProcessingStrategy:
        """
        Create optimal processing strategy for a set of documents
        
        This is THE BRAIN of the system!
        """
        total_docs = len(documents)
        
        # Estimate average document size
        avg_doc_size = sum(len(doc.get('content', '')) for doc in documents) // (total_docs * 4)  # ~4 chars/token
        
        if self.use_cag:
            # With CAG: maximize data processing
            capacity_estimate = self.context_mgr.estimate_batch_capacity(
                case_id,
                agent_type,
                avg_doc_size
            )
            batch_size = capacity_estimate['with_cag']['docs_per_batch']
        else:
            # Without CAG: conservative estimate
            # Reserve 20% for instructions each time
            available = int(self.context_window * 0.8)
            batch_size = max(1, available // avg_doc_size)
        
        total_batches = (total_docs + batch_size - 1) // batch_size
        
        # Decide if we need hierarchical summarization
        use_hierarchical = total_batches > 10
        
        return ProcessingStrategy(
            total_documents=total_docs,
            estimated_tokens_per_doc=avg_doc_size,
            context_window=self.context_window,
            batch_size=batch_size,
            total_batches=total_batches,
            use_cag=self.use_cag,
            use_hierarchical_summary=use_hierarchical
        )
    
    def process_large_document_set(self,
                                   case_id: str,
                                   agent_type: str,
                                   documents: List[Dict[str, Any]],
                                   query: Optional[str] = None) -> Dict[str, Any]:
        """
        Process large document set using RAG + CAG
        
        This is the FULL IMPLEMENTATION of the strategy!
        
        Flow:
        1. Create optimal strategy
        2. Setup CAG cache
        3. Process in batches (RAG for retrieval)
        4. Maintain running summary (CAG cached)
        5. Final synthesis
        """
        print(f"\n{'='*80}")
        print(f"RAG+CAG Processing: {len(documents)} documents")
        print(f"Context Window: {self.context_window:,} tokens")
        print(f"Agent: {agent_type}")
        print(f"{'='*80}\n")
        
        # Step 1: Create strategy
        strategy = self.create_processing_strategy(case_id, agent_type, documents)
        
        print(f"📋 Strategy:")
        print(f"   Batch size: {strategy.batch_size} docs/batch")
        print(f"   Total batches: {strategy.total_batches}")
        print(f"   CAG enabled: {'✅' if strategy.use_cag else '❌'}")
        print(f"   Hierarchical summary: {'✅' if strategy.use_hierarchical_summary else '❌'}")
        print()
        
        # Step 2: Setup CAG cache
        if self.use_cag:
            cache_strategy = self.cag.create_agent_cache_strategy(case_id, agent_type)
            print(f"💾 CAG Cache setup:")
            for key, comp_id in cache_strategy.items():
                comp = self.cag.get_component(comp_id)
                print(f"   {key}: {comp.tokens_estimate:,} tokens cached")
            print()
        
        # Step 3: Process batches
        batch_summaries = []
        running_summary = ""
        
        for batch_idx in range(strategy.total_batches):
            start_idx = batch_idx * strategy.batch_size
            end_idx = min(start_idx + strategy.batch_size, len(documents))
            batch_docs = documents[start_idx:end_idx]
            
            print(f"📦 Batch {batch_idx + 1}/{strategy.total_batches} ({len(batch_docs)} docs)")
            
            # RAG: Query-focused retrieval (if query provided)
            if query:
                relevant_docs = self._rag_retrieve(batch_docs, query, top_k=min(5, len(batch_docs)))
            else:
                relevant_docs = batch_docs
            
            # Process batch
            batch_result = self._process_batch(
                case_id=case_id,
                agent_type=agent_type,
                documents=relevant_docs,
                running_summary=running_summary,
                batch_idx=batch_idx
            )
            
            batch_summaries.append(batch_result['summary'])
            running_summary = batch_result['running_summary']
            
            # Update stats
            self.stats['total_batches_processed'] += 1
            self.stats['total_documents_processed'] += len(relevant_docs)
            if 'tokens_saved' in batch_result:
                self.stats['total_tokens_saved_by_cag'] += batch_result['tokens_saved']
            
            print(f"   ✅ Processed: {batch_result['findings_count']} findings")
            if 'tokens_saved' in batch_result:
                print(f"   💰 CAG saved: {batch_result['tokens_saved']:,} tokens")
            print()
        
        # Step 4: Final synthesis
        print(f"🔄 Final synthesis...")
        final_result = self._synthesize_final_results(
            case_id=case_id,
            agent_type=agent_type,
            batch_summaries=batch_summaries,
            running_summary=running_summary,
            strategy=strategy
        )
        
        # Step 5: Stats
        self._print_final_stats(strategy)
        
        return final_result
    
    def _rag_retrieve(self, 
                     documents: List[Dict[str, Any]], 
                     query: str, 
                     top_k: int = 5) -> List[Dict[str, Any]]:
        """
        RAG: Retrieve most relevant documents using semantic search
        """
        # Embed query
        query_embedding = self.embeddings.embed(query).embedding
        
        # Score documents
        scored_docs = []
        for doc in documents:
            content = doc.get('content', '')
            if not content:
                continue
            
            doc_embedding = self.embeddings.embed(content).embedding
            
            # Simple cosine similarity
            similarity = self._cosine_similarity(query_embedding, doc_embedding)
            scored_docs.append((similarity, doc))
        
        # Sort and return top-k
        scored_docs.sort(reverse=True, key=lambda x: x[0])
        return [doc for _, doc in scored_docs[:top_k]]
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity"""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5
        return dot_product / (norm1 * norm2) if norm1 and norm2 else 0.0
    
    def _process_batch(self,
                      case_id: str,
                      agent_type: str,
                      documents: List[Dict[str, Any]],
                      running_summary: str,
                      batch_idx: int) -> Dict[str, Any]:
        """Process single batch with CAG optimization"""
        
        # Prepare hot content (new data)
        hot_content = f"BATCH {batch_idx + 1} DOCUMENTS:\n\n"
        for i, doc in enumerate(documents, 1):
            content = doc.get('content', '')[:500]  # Truncate for demo
            hot_content += f"Document {i}:\n{content}\n\n"
        
        hot_content += "\nTask: Analyze these documents and extract key findings."
        
        # Build optimized prompt with CAG
        if self.use_cag:
            prompt_result = self.context_mgr.create_optimized_prompt(
                case_id=case_id,
                agent_type=agent_type,
                new_content=hot_content,
                running_summary=running_summary if running_summary else None
            )
            
            prompt = prompt_result['prompt']
            tokens_saved = prompt_result.get('tokens_saved', 0)
        else:
            # Without CAG: build prompt manually
            system_inst = self.cag._get_system_instruction(agent_type)
            prompt = f"{system_inst}\n\n{hot_content}"
            tokens_saved = 0
        
        # Simulate LLM call (in production, call actual LLM here)
        # findings = self.llm.complete(prompt)
        findings = f"Analysis of batch {batch_idx + 1}: Found {len(documents)} documents with relevant information."
        
        # Create summary
        batch_summary = f"Batch {batch_idx + 1}: {findings}"
        
        # Update running summary
        new_running_summary = running_summary + "\n" + batch_summary if running_summary else batch_summary
        
        return {
            'batch_idx': batch_idx,
            'summary': batch_summary,
            'running_summary': new_running_summary,
            'findings_count': len(documents),
            'tokens_saved': tokens_saved
        }
    
    def _synthesize_final_results(self,
                                 case_id: str,
                                 agent_type: str,
                                 batch_summaries: List[str],
                                 running_summary: str,
                                 strategy: ProcessingStrategy) -> Dict[str, Any]:
        """Final synthesis of all batch results"""
        
        # For hierarchical summarization
        if strategy.use_hierarchical_summary:
            # Summarize the summaries
            final_summary = self._hierarchical_summarize(batch_summaries)
        else:
            final_summary = running_summary
        
        return {
            'case_id': case_id,
            'agent_type': agent_type,
            'strategy': strategy,
            'batch_summaries': batch_summaries,
            'final_summary': final_summary,
            'stats': self.stats.copy()
        }
    
    def _hierarchical_summarize(self, summaries: List[str]) -> str:
        """Hierarchical summarization of summaries"""
        # Group summaries into clusters
        # Then summarize each cluster
        # Finally, summarize the cluster summaries
        # (Simplified for demo)
        return "Final synthesis: " + " | ".join(summaries[:5]) + "..."
    
    def _print_final_stats(self, strategy: ProcessingStrategy):
        """Print final statistics"""
        print(f"\n{'='*80}")
        print("FINAL STATISTICS")
        print(f"{'='*80}")
        print(f"Documents processed: {self.stats['total_documents_processed']}")
        print(f"Batches processed: {self.stats['total_batches_processed']}")
        
        if self.use_cag:
            print(f"Tokens saved by CAG: {self.stats['total_tokens_saved_by_cag']:,}")
            
            # Calculate what would have been without CAG
            without_cag = strategy.total_batches * 4000  # Assume 4k overhead per batch
            savings_percent = (self.stats['total_tokens_saved_by_cag'] / without_cag * 100) if without_cag > 0 else 0
            
            print(f"Efficiency improvement: {savings_percent:.1f}%")
            print(f"\n🚀 CAG made {self.context_window:,} tokens feel like {self.context_window + self.stats['total_tokens_saved_by_cag']:,} tokens!")
        print(f"{'='*80}\n")


if __name__ == "__main__":
    # Demo
    print("=" * 80)
    print("RAG + CAG Complete Strategy Demo")
    print("=" * 80)
    print()
    
    # Create orchestrator for LOCAL LLM (44k)
    orchestrator_local = RAGCAGOrchestrator(context_window=44000, use_cag=True)
    
    # Simulate 100 documents
    documents = [
        {'id': f'doc_{i}', 'content': f'Document {i} content ' * 100}
        for i in range(100)
    ]
    
    # Process with RAG+CAG
    result = orchestrator_local.process_large_document_set(
        case_id="demo_case",
        agent_type="financial",
        documents=documents,
        query="financial performance"
    )
    
    print("✅ Processing complete!")
    print(f"Final summary: {result['final_summary'][:200]}...")
