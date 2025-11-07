"""
Embedding Pipeline - Dual Model System
Paweł Kowalski
2025-11-05
"""

import asyncio
import hashlib
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import sys
import os

# Add parent to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from lmstudio_embeddings import LMStudioEmbeddings


@dataclass
class EmbeddingResult:
    """Result of embedding operation"""
    text: str
    embedding: List[float]
    model: str
    dimensions: int
    time_taken: float
    text_hash: str


class DualEmbeddingSystem:
    """
    Dual model embedding system
    
    - E5-Large: General text, multilingual (1024 dims)
    - Jina: Financial/tabular data (1024 dims)
    
    Automatic routing based on content type
    """
    
    def __init__(self, base_url: str = "http://192.168.200.226:1234/v1"):
        """
        Initialize dual embedding system
        
        Args:
            base_url: LMStudio embeddings endpoint
        """
        self.e5_client = LMStudioEmbeddings(
            base_url=base_url,
            model="text-embedding-multilingual-e5-large-instruct"
        )
        
        self.jina_client = LMStudioEmbeddings(
            base_url=base_url,
            model="jina-embeddings-v4-text-retrieval"
        )
        
        # Performance tracking
        self.stats = {
            "e5": {"count": 0, "total_time": 0},
            "jina": {"count": 0, "total_time": 0}
        }
    
    def _is_financial_content(self, text: str, document_type: Optional[str] = None) -> bool:
        """
        Determine if content is financial/tabular
        
        Args:
            text: Text to check
            document_type: Optional explicit document type
            
        Returns:
            True if financial, False otherwise
        """
        if document_type and document_type.lower() in ["financial", "tabular", "accounting", "invoice"]:
            return True
        
        # Check for financial keywords
        financial_keywords = [
            "revenue", "profit", "loss", "expense", "asset", "liability",
            "balance sheet", "income statement", "cash flow", "roi",
            "$", "€", "£", "usd", "eur", "invoice", "payment"
        ]
        
        text_lower = text.lower()
        financial_count = sum(1 for keyword in financial_keywords if keyword in text_lower)
        
        return financial_count >= 2
    
    def route_to_model(self, text: str, document_type: Optional[str] = None) -> str:
        """
        Intelligent routing for CBA documents
        
        Routes to Jina for:
        - Tables and structured data
        - Long documents (>2000 words)
        - Financial/tabular content
        - CBA reports
        
        Routes to E5 for:
        - Short text documents (<500 words)
        - General text without tables
        - Press releases, notes
        
        Args:
            text: Text to embed
            document_type: Optional document type hint
            
        Returns:
            Model name ('e5' or 'jina')
        """
        import re
        
        # 1. Explicit document type hints
        if document_type:
            type_lower = document_type.lower()
            # CBA reports and structured data → Jina
            cba_types = ["cba_report", "financial", "tabular", "statistical", "report", "cba"]
            if any(t in type_lower for t in cba_types):
                return "jina"
            
            # Short text documents → E5
            text_types = ["press_release", "note", "email", "article", "communication"]
            if any(t in type_lower for t in text_types):
                return "e5"
        
        # 2. Check for tables in text
        if self._has_tables(text):
            return "jina"
        
        # 3. Check document length
        word_count = len(text.split())
        if word_count > 2000:
            return "jina"  # Long documents → Jina
        
        # 4. Check for financial/numeric content (existing logic)
        if self._is_financial_content(text, document_type):
            return "jina"
        
        # 5. Default: E5 for general text
        return "e5"
    
    def _has_tables(self, text: str) -> bool:
        """
        Detect if text contains tables
        
        Args:
            text: Text to check
            
        Returns:
            True if tables detected
        """
        import re
        
        # Check for common table patterns
        table_patterns = [
            r'\|\s*\w+.*\|\s*\w+.*\|',  # Markdown table (| col1 | col2 |)
            r'Tabela\s+\d+',              # "Tabela 1"
            r'Table\s+\d+',               # "Table 1"
            r'Statystyka',                 # "Statystyka"
            r'\n\s*\d{1,4}\s+\d{1,4}\s+\d{1,4}',  # Number rows (tab-separated)
            r'\d+\s+\|\s+\d+',            # Number | Number pattern
        ]
        
        for pattern in table_patterns:
            if re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
                return True
        
        return False
    
    def embed(
        self,
        text: str,
        document_type: Optional[str] = None,
        force_model: Optional[str] = None
    ) -> EmbeddingResult:
        """
        Generate embedding with automatic model selection
        
        Args:
            text: Text to embed
            document_type: Optional document type
            force_model: Force specific model ('e5' or 'jina')
            
        Returns:
            EmbeddingResult with embedding and metadata
        """
        import time
        
        # Select model
        if force_model:
            model = force_model
        else:
            model = self.route_to_model(text, document_type)
        
        # Generate embedding
        start_time = time.time()
        
        if model == "jina":
            embedding = self.jina_client.embed(text)
            model_name = "jina-embeddings-v4-text-retrieval"
        else:
            embedding = self.e5_client.embed(text)
            model_name = "text-embedding-multilingual-e5-large-instruct"
        
        elapsed = time.time() - start_time
        
        # Update stats
        self.stats[model]["count"] += 1
        self.stats[model]["total_time"] += elapsed
        
        # Generate hash for deduplication
        text_hash = hashlib.md5(text.encode()).hexdigest()
        
        return EmbeddingResult(
            text=text,
            embedding=embedding,
            model=model_name,
            dimensions=len(embedding),
            time_taken=elapsed,
            text_hash=text_hash
        )
    
    def batch_embed(
        self,
        texts: List[str],
        document_types: Optional[List[str]] = None
    ) -> List[EmbeddingResult]:
        """
        Batch embed multiple texts
        
        Args:
            texts: List of texts to embed
            document_types: Optional list of document types
            
        Returns:
            List of EmbeddingResults
        """
        results = []
        
        for i, text in enumerate(texts):
            doc_type = document_types[i] if document_types else None
            result = self.embed(text, doc_type)
            results.append(result)
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get performance statistics
        
        Returns:
            Dict with stats for both models
        """
        stats = {}
        
        for model in ["e5", "jina"]:
            count = self.stats[model]["count"]
            total_time = self.stats[model]["total_time"]
            
            stats[model] = {
                "embeddings_generated": count,
                "total_time": total_time,
                "avg_time": total_time / count if count > 0 else 0,
                "throughput": count / total_time if total_time > 0 else 0
            }
        
        return stats


class DocumentEmbeddingPipeline:
    """
    Full pipeline for document embedding and storage
    """
    
    def __init__(self):
        """Initialize pipeline"""
        self.embedder = DualEmbeddingSystem()
        self.chunk_size = 8000  # Safe for 44k context
        self.overlap = 500      # Context preservation
    
    def split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences
        
        Args:
            text: Text to split
            
        Returns:
            List of sentences
        """
        # Simple sentence splitter (can be improved with NLTK)
        import re
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def chunk_document(self, text: str) -> List[Dict[str, Any]]:
        """
        Chunk document intelligently
        
        Args:
            text: Document text
            
        Returns:
            List of chunks with metadata
        """
        sentences = self.split_into_sentences(text)
        chunks = []
        current_chunk = []
        current_length = 0
        
        for i, sentence in enumerate(sentences):
            sentence_length = len(sentence)
            
            if current_length + sentence_length > self.chunk_size and current_chunk:
                # Save current chunk
                chunk_text = ". ".join(current_chunk) + "."
                chunks.append({
                    "text": chunk_text,
                    "start_sentence": i - len(current_chunk),
                    "end_sentence": i - 1,
                    "length": current_length
                })
                
                # Start new chunk with overlap
                overlap_sentences = current_chunk[-2:] if len(current_chunk) >= 2 else current_chunk
                current_chunk = overlap_sentences + [sentence]
                current_length = sum(len(s) for s in current_chunk)
            else:
                current_chunk.append(sentence)
                current_length += sentence_length
        
        # Add final chunk
        if current_chunk:
            chunk_text = ". ".join(current_chunk) + "."
            chunks.append({
                "text": chunk_text,
                "start_sentence": len(sentences) - len(current_chunk),
                "end_sentence": len(sentences) - 1,
                "length": current_length
            })
        
        return chunks
    
    def process_document(
        self,
        document: str,
        document_id: str,
        document_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Process entire document into embeddings
        
        Args:
            document: Document text
            document_id: Unique document ID
            document_type: Optional document type
            
        Returns:
            List of embedding records ready for storage
        """
        # Chunk document
        chunks = self.chunk_document(document)
        
        # Generate embeddings
        records = []
        for i, chunk in enumerate(chunks):
            result = self.embedder.embed(chunk["text"], document_type)
            
            record = {
                "document_id": document_id,
                "chunk_id": i,
                "text": chunk["text"],
                "embedding": result.embedding,
                "model": result.model,
                "dimensions": result.dimensions,
                "text_hash": result.text_hash,
                "metadata": {
                    "start_sentence": chunk["start_sentence"],
                    "end_sentence": chunk["end_sentence"],
                    "chunk_length": chunk["length"],
                    "document_type": document_type,
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            records.append(record)
        
        return records


def test_pipeline():
    """Test the embedding pipeline"""
    print("🧪 Testing Embedding Pipeline...")
    
    # Test dual embedding system
    print("\n1. Testing dual embedding system...")
    embedder = DualEmbeddingSystem()
    
    # Test general text
    text1 = "The company's strategic vision focuses on innovation."
    result1 = embedder.embed(text1)
    print(f"   General text → {result1.model} ({result1.dimensions}d) in {result1.time_taken:.3f}s")
    
    # Test financial text
    text2 = "Revenue increased 23% to $4.2M with EBITDA margin of 32%."
    result2 = embedder.embed(text2)
    print(f"   Financial text → {result2.model} ({result2.dimensions}d) in {result2.time_taken:.3f}s")
    
    # Test document pipeline
    print("\n2. Testing document pipeline...")
    pipeline = DocumentEmbeddingPipeline()
    
    test_doc = """
    Financial Analysis Report Q4 2024.
    
    Revenue Performance: The company achieved revenue of $4.2M in Q4, representing 
    a 23% increase year-over-year. This growth was driven by strong performance 
    in the enterprise segment.
    
    Profitability: EBITDA margin improved to 32%, up from 28% in Q3. Operating 
    expenses were well-controlled at 18% of revenue.
    
    Outlook: Management expects continued growth momentum in 2025, with projected 
    revenue growth of 20-25%.
    """
    
    records = pipeline.process_document(test_doc, "doc_001", "financial")
    print(f"   Processed document into {len(records)} chunks")
    for i, record in enumerate(records):
        print(f"   Chunk {i+1}: {len(record['text'])} chars, model={record['model'][:10]}...")
    
    # Stats
    print("\n3. Performance statistics...")
    stats = embedder.get_stats()
    for model, data in stats.items():
        print(f"   {model}: {data['embeddings_generated']} embeddings, "
              f"{data['avg_time']:.3f}s avg, "
              f"{data['throughput']:.1f}/sec throughput")
    
    print("\n✅ Pipeline tests complete!")


if __name__ == "__main__":
    test_pipeline()
