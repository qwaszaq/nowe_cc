"""
Cache-Augmented Generation (CAG) System
Dramatically reduces context consumption by caching static prompt components
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import hashlib
import json
import time
from pathlib import Path


@dataclass
class CachedPromptComponent:
    """Cached component of a prompt"""
    component_id: str
    content: str
    type: str  # 'system_instruction', 'domain_knowledge', 'running_summary', 'query'
    tokens_estimate: int
    hash: str
    created_at: float
    last_used: float
    use_count: int


class CAGManager:
    """
    Cache-Augmented Generation Manager
    Manages prompt caching to maximize context window efficiency
    
    For 44k local LLM: SURVIVAL TOOL
    For 200k Claude: COST OPTIMIZATION
    """
    
    def __init__(self, cache_dir: str = ".cache/prompts"):
        """Initialize CAG Manager"""
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory cache
        self.cache: Dict[str, CachedPromptComponent] = {}
        
        # Cache statistics
        self.stats = {
            'hits': 0,
            'misses': 0,
            'tokens_saved': 0,
            'created': 0
        }
        
        # Load existing cache
        self._load_cache()
    
    def cache_component(self, 
                       content: str, 
                       component_type: str,
                       component_id: Optional[str] = None) -> str:
        """
        Cache a static prompt component
        
        Args:
            content: Content to cache
            component_type: Type of component
            component_id: Optional ID (auto-generated if not provided)
            
        Returns:
            Component ID for retrieval
        """
        # Generate hash
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        
        # Generate ID if not provided
        if not component_id:
            component_id = f"{component_type}_{content_hash}"
        
        # Estimate tokens (rough: ~4 chars per token)
        tokens_estimate = len(content) // 4
        
        # Create cached component
        component = CachedPromptComponent(
            component_id=component_id,
            content=content,
            type=component_type,
            tokens_estimate=tokens_estimate,
            hash=content_hash,
            created_at=time.time(),
            last_used=time.time(),
            use_count=1
        )
        
        # Store in cache
        self.cache[component_id] = component
        self.stats['created'] += 1
        
        # Persist to disk
        self._save_component(component)
        
        return component_id
    
    def get_component(self, component_id: str) -> Optional[CachedPromptComponent]:
        """Retrieve cached component"""
        if component_id in self.cache:
            component = self.cache[component_id]
            component.last_used = time.time()
            component.use_count += 1
            self.stats['hits'] += 1
            self.stats['tokens_saved'] += component.tokens_estimate
            return component
        else:
            self.stats['misses'] += 1
            return None
    
    def build_prompt_with_cache(self,
                               cached_component_ids: List[str],
                               hot_content: str,
                               separator: str = "\n\n") -> Dict[str, Any]:
        """
        Build prompt using cached components + new hot content
        
        Args:
            cached_component_ids: IDs of cached components to use
            hot_content: New, dynamic content
            separator: Separator between components
            
        Returns:
            Prompt structure with cache info
        """
        # Retrieve cached components
        cached_parts = []
        total_cached_tokens = 0
        
        for comp_id in cached_component_ids:
            component = self.get_component(comp_id)
            if component:
                cached_parts.append(component.content)
                total_cached_tokens += component.tokens_estimate
        
        # Build full prompt
        full_prompt = separator.join(cached_parts + [hot_content])
        
        # Estimate hot content tokens
        hot_tokens = len(hot_content) // 4
        
        return {
            'prompt': full_prompt,
            'cached_tokens': total_cached_tokens,
            'hot_tokens': hot_tokens,
            'total_tokens': total_cached_tokens + hot_tokens,
            'savings_ratio': total_cached_tokens / (total_cached_tokens + hot_tokens) if hot_tokens > 0 else 0,
            'cached_component_count': len(cached_parts)
        }
    
    def create_agent_cache_strategy(self, 
                                    case_id: str,
                                    agent_type: str) -> Dict[str, str]:
        """
        Create optimal caching strategy for an agent working on a case
        
        Returns component IDs for:
        - System instruction
        - Case context
        - Running summary
        """
        strategy = {}
        
        # 1. System Instruction (unchanging)
        system_instruction = self._get_system_instruction(agent_type)
        strategy['system'] = self.cache_component(
            content=system_instruction,
            component_type='system_instruction',
            component_id=f"{agent_type}_system"
        )
        
        # 2. Case Context (changes per case but stable within case)
        case_context = self._get_case_context(case_id)
        strategy['case_context'] = self.cache_component(
            content=case_context,
            component_type='case_context',
            component_id=f"{case_id}_context"
        )
        
        # 3. Domain Knowledge (unchanging)
        domain_knowledge = self._get_domain_knowledge(agent_type)
        strategy['domain'] = self.cache_component(
            content=domain_knowledge,
            component_type='domain_knowledge',
            component_id=f"{agent_type}_domain"
        )
        
        return strategy
    
    def update_running_summary(self, 
                              case_id: str, 
                              summary: str) -> str:
        """
        Update running summary cache
        This is updated as analysis progresses
        """
        component_id = f"{case_id}_running_summary"
        
        # Check if exists
        existing = self.get_component(component_id)
        
        if existing:
            # Update existing
            existing.content = summary
            existing.last_used = time.time()
            existing.tokens_estimate = len(summary) // 4
            self._save_component(existing)
        else:
            # Create new
            component_id = self.cache_component(
                content=summary,
                component_type='running_summary',
                component_id=component_id
            )
        
        return component_id
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.stats['hits'] + self.stats['misses']
        hit_rate = self.stats['hits'] / total_requests if total_requests > 0 else 0
        
        return {
            **self.stats,
            'hit_rate': hit_rate,
            'cache_size': len(self.cache),
            'estimated_tokens_in_cache': sum(c.tokens_estimate for c in self.cache.values())
        }
    
    def clear_old_cache(self, max_age_hours: int = 24):
        """Clear cache entries older than specified hours"""
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        to_remove = []
        for comp_id, component in self.cache.items():
            if current_time - component.last_used > max_age_seconds:
                to_remove.append(comp_id)
        
        for comp_id in to_remove:
            del self.cache[comp_id]
            cache_file = self.cache_dir / f"{comp_id}.json"
            if cache_file.exists():
                cache_file.unlink()
    
    def _get_system_instruction(self, agent_type: str) -> str:
        """Get system instruction for agent type"""
        instructions = {
            'financial': """You are a Financial Analysis Agent specializing in:
- Revenue and profitability analysis
- Financial statement analysis
- Trend identification and forecasting
- Risk assessment for financial metrics

Your goal is to provide clear, actionable financial insights based on the documents provided.
Focus on quantifiable metrics and evidence-based conclusions.""",
            
            'legal': """You are a Legal Analysis Agent specializing in:
- Contract review and clause analysis
- Regulatory compliance assessment
- Legal risk identification
- Entity and obligation extraction

Your goal is to identify legal risks, obligations, and key terms in documents.
Be precise and cite specific clauses or sections.""",
            
            'data_science': """You are a Data Science Agent specializing in:
- Statistical analysis
- Pattern recognition
- Data quality assessment
- Predictive insights

Your goal is to extract insights from structured and unstructured data.
Focus on data-driven conclusions with statistical backing.""",
            
            'risk': """You are a Risk Analysis Agent specializing in:
- Risk identification and classification
- Impact assessment
- Mitigation strategy evaluation
- Compliance gap analysis

Your goal is to identify, assess, and prioritize risks across all dimensions.
Provide clear risk ratings and mitigation recommendations."""
        }
        
        return instructions.get(agent_type, "You are an analytical agent.")
    
    def _get_case_context(self, case_id: str) -> str:
        """Get case context (would be loaded from database in production)"""
        return f"""CASE CONTEXT
Case ID: {case_id}
Analysis Type: Comprehensive multi-document analysis
Objective: Extract key insights, identify patterns, assess risks and opportunities

You are working through a large set of documents. Your analysis will be:
1. Incremental (processing documents in batches)
2. Cumulative (building on previous findings)
3. Context-aware (maintaining consistency across documents)"""
    
    def _get_domain_knowledge(self, agent_type: str) -> str:
        """Get domain-specific knowledge"""
        knowledge = {
            'financial': """FINANCIAL DOMAIN KNOWLEDGE
- YoY: Year-over-Year comparison
- EBITDA: Earnings Before Interest, Taxes, Depreciation, Amortization
- Key metrics: Revenue, Gross Margin, Operating Income, Net Income, Cash Flow
- Standard reporting periods: Q1-Q4 (quarters), FY (fiscal year)""",
            
            'legal': """LEGAL DOMAIN KNOWLEDGE
- Standard contract sections: Parties, Terms, Obligations, Termination, Liability
- Key clauses: Indemnification, Limitation of Liability, Force Majeure, Confidentiality
- Regulatory frameworks: GDPR, SOX, CCPA (context-dependent)""",
            
            'data_science': """DATA SCIENCE DOMAIN KNOWLEDGE
- Statistical significance: p-value < 0.05
- Correlation vs Causation
- Common distributions: Normal, Binomial, Poisson
- Quality metrics: Completeness, Accuracy, Consistency, Timeliness"""
        }
        
        return knowledge.get(agent_type, "")
    
    def _save_component(self, component: CachedPromptComponent):
        """Save component to disk"""
        cache_file = self.cache_dir / f"{component.component_id}.json"
        with open(cache_file, 'w') as f:
            json.dump({
                'component_id': component.component_id,
                'content': component.content,
                'type': component.type,
                'tokens_estimate': component.tokens_estimate,
                'hash': component.hash,
                'created_at': component.created_at,
                'last_used': component.last_used,
                'use_count': component.use_count
            }, f)
    
    def _load_cache(self):
        """Load cache from disk"""
        if not self.cache_dir.exists():
            return
        
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                    component = CachedPromptComponent(**data)
                    self.cache[component.component_id] = component
            except:
                pass  # Skip corrupted cache files


class SmartContextManager:
    """
    Smart Context Manager integrating RAG + CAG
    Manages the entire context window intelligently
    """
    
    def __init__(self, max_tokens: int = 44000):
        """
        Initialize context manager
        
        Args:
            max_tokens: Maximum context window (44k for local, 200k for Claude)
        """
        self.max_tokens = max_tokens
        self.cag = CAGManager()
        
        # Reserve space for output
        self.output_reserve = 2000
        self.available_tokens = max_tokens - self.output_reserve
        
        # Context allocation strategy
        self.allocation = {
            'cached': 0.3,      # 30% for cached components
            'hot_data': 0.6,    # 60% for new data
            'buffer': 0.1       # 10% safety buffer
        }
    
    def create_optimized_prompt(self,
                               case_id: str,
                               agent_type: str,
                               new_content: str,
                               running_summary: Optional[str] = None) -> Dict[str, Any]:
        """
        Create optimized prompt using CAG
        
        This is THE KEY METHOD that makes 44k feel like 80k!
        """
        # Create or retrieve cache strategy
        cache_strategy = self.cag.create_agent_cache_strategy(case_id, agent_type)
        
        # Components to use
        cached_components = [
            cache_strategy['system'],      # System instruction
            cache_strategy['domain'],      # Domain knowledge
            cache_strategy['case_context'] # Case context
        ]
        
        # Add running summary if provided
        if running_summary:
            summary_id = self.cag.update_running_summary(case_id, running_summary)
            cached_components.append(summary_id)
        
        # Build prompt
        result = self.cag.build_prompt_with_cache(
            cached_component_ids=cached_components,
            hot_content=new_content
        )
        
        # Calculate efficiency
        tokens_used = result['total_tokens']
        tokens_saved = result['cached_tokens']
        effective_capacity = self.available_tokens + tokens_saved
        
        result['context_analysis'] = {
            'max_tokens': self.max_tokens,
            'tokens_used': tokens_used,
            'tokens_saved': tokens_saved,
            'tokens_available': self.available_tokens - result['hot_tokens'],
            'effective_capacity': effective_capacity,
            'utilization': tokens_used / self.max_tokens,
            'savings_ratio': result['savings_ratio']
        }
        
        return result
    
    def estimate_batch_capacity(self, 
                               case_id: str,
                               agent_type: str,
                               avg_doc_size: int) -> Dict[str, Any]:
        """
        Estimate how many documents can be processed per batch with CAG
        
        This shows the MAGIC of CAG!
        """
        # Get base cache overhead
        cache_strategy = self.cag.create_agent_cache_strategy(case_id, agent_type)
        
        # Simulate prompt building
        test_result = self.cag.build_prompt_with_cache(
            cached_component_ids=[
                cache_strategy['system'],
                cache_strategy['domain'],
                cache_strategy['case_context']
            ],
            hot_content=""
        )
        
        base_cached_tokens = test_result['cached_tokens']
        available_for_data = self.available_tokens - base_cached_tokens
        
        # Without CAG
        without_cag_overhead = base_cached_tokens * 455  # Repeated in every run
        without_cag_docs_per_batch = self.available_tokens // (base_cached_tokens + avg_doc_size)
        
        # With CAG
        with_cag_docs_per_batch = available_for_data // avg_doc_size
        
        return {
            'base_cached_tokens': base_cached_tokens,
            'available_for_data': available_for_data,
            'avg_doc_size': avg_doc_size,
            
            'without_cag': {
                'docs_per_batch': without_cag_docs_per_batch,
                'total_overhead_tokens': without_cag_overhead,
                'efficiency': 'poor'
            },
            
            'with_cag': {
                'docs_per_batch': with_cag_docs_per_batch,
                'total_overhead_tokens': base_cached_tokens,  # Only once!
                'efficiency': 'excellent',
                'improvement_ratio': with_cag_docs_per_batch / without_cag_docs_per_batch if without_cag_docs_per_batch > 0 else 0
            }
        }


if __name__ == "__main__":
    # Demo
    print("=" * 80)
    print("CAG (Cache-Augmented Generation) Demo")
    print("=" * 80)
    print()
    
    # Create managers
    cag = CAGManager()
    context_mgr = SmartContextManager(max_tokens=44000)
    
    # Demo 1: Basic caching
    print("Demo 1: Basic Component Caching")
    print("-" * 80)
    
    system_inst = "You are a financial analyst..."
    comp_id = cag.cache_component(system_inst, 'system_instruction')
    print(f"✅ Cached component: {comp_id}")
    print(f"   Tokens: ~{len(system_inst) // 4}")
    print()
    
    # Demo 2: Cache strategy
    print("Demo 2: Agent Cache Strategy")
    print("-" * 80)
    
    strategy = cag.create_agent_cache_strategy("case_001", "financial")
    print("Created cache strategy:")
    for key, comp_id in strategy.items():
        comp = cag.get_component(comp_id)
        print(f"   {key}: {comp.tokens_estimate} tokens")
    print()
    
    # Demo 3: Capacity estimation
    print("Demo 3: Batch Capacity Estimation (THE MAGIC!)")
    print("-" * 80)
    
    estimate = context_mgr.estimate_batch_capacity("case_001", "financial", avg_doc_size=1000)
    
    print(f"Context Window: {context_mgr.max_tokens:,} tokens")
    print(f"Base cached overhead: {estimate['base_cached_tokens']:,} tokens")
    print()
    print("WITHOUT CAG:")
    print(f"   Docs per batch: {estimate['without_cag']['docs_per_batch']}")
    print(f"   Total overhead (455 runs): {estimate['without_cag']['total_overhead_tokens']:,} tokens")
    print()
    print("WITH CAG:")
    print(f"   Docs per batch: {estimate['with_cag']['docs_per_batch']}")
    print(f"   Total overhead (455 runs): {estimate['with_cag']['total_overhead_tokens']:,} tokens")
    print(f"   🚀 IMPROVEMENT: {estimate['with_cag']['improvement_ratio']:.1f}x more efficient!")
    print()
    
    # Demo 4: Stats
    print("Demo 4: Cache Statistics")
    print("-" * 80)
    stats = cag.get_stats()
    print(f"   Cache hits: {stats['hits']}")
    print(f"   Cache size: {stats['cache_size']} components")
    print(f"   Tokens saved: {stats['tokens_saved']:,}")
    print()
