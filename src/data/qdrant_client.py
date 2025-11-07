"""
Qdrant Vector Database Client
Paweł Kowalski
2025-11-05
"""

import urllib.request
import urllib.error
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import hashlib


@dataclass
class QdrantSearchResult:
    """Qdrant search result"""
    document_id: str
    chunk_id: int
    content: str
    score: float
    metadata: Dict[str, Any]


class QdrantClient:
    """
    Qdrant vector database client for scalable semantic search
    
    Features:
    - Store embeddings at scale (100k+ vectors)
    - Fast semantic search
    - Advanced filtering
    - Collection management
    
    Use when:
    - Case has 100k+ documents
    - Need advanced similarity search
    - PostgreSQL performance degraded
    """
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6333,
        collection_name: str = "destiny_embeddings"
    ):
        """
        Initialize Qdrant client
        
        Args:
            host: Qdrant host
            port: Qdrant port
            collection_name: Collection name
        """
        self.base_url = f"http://{host}:{port}"
        self.collection_name = collection_name
        self.available = self._check_availability()
        
        if self.available:
            self._ensure_collection()
    
    def _check_availability(self) -> bool:
        """Check if Qdrant is available"""
        try:
            # Qdrant doesn't have /health, use root endpoint
            req = urllib.request.Request(f"{self.base_url}/")
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status == 200
        except:
            return False
    
    def _ensure_collection(self):
        """Ensure collection exists"""
        # Check if collection exists
        try:
            req = urllib.request.Request(
                f"{self.base_url}/collections/{self.collection_name}"
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                return  # Collection exists
        except urllib.error.HTTPError as e:
            if e.code == 404:
                # Create collection
                self._create_collection()
    
    def _create_collection(self):
        """Create Qdrant collection"""
        data = {
            "vectors": {
                "size": 1024,
                "distance": "Cosine"
            }
        }
        
        req = urllib.request.Request(
            f"{self.base_url}/collections/{self.collection_name}",
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='PUT'
        )
        
        try:
            with urllib.request.urlopen(req, timeout=10):
                print(f"✅ Qdrant collection created: {self.collection_name}")
        except Exception as e:
            print(f"⚠️  Qdrant collection creation failed: {e}")
    
    def store_embedding(
        self,
        document_id: str,
        chunk_id: int,
        content: str,
        embedding: List[float],
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store embedding in Qdrant
        
        Args:
            document_id: Document identifier
            chunk_id: Chunk number
            content: Text content
            embedding: Embedding vector
            metadata: Optional metadata
            
        Returns:
            Point ID
        """
        if not self.available:
            raise Exception("Qdrant not available")
        
        # Generate unique ID
        point_id = hashlib.md5(f"{document_id}_{chunk_id}".encode()).hexdigest()
        
        # Prepare payload
        payload = {
            "document_id": document_id,
            "chunk_id": chunk_id,
            "content": content
        }
        
        if metadata:
            payload.update(metadata)
        
        # Store point
        data = {
            "points": [
                {
                    "id": point_id,
                    "vector": embedding,
                    "payload": payload
                }
            ]
        }
        
        req = urllib.request.Request(
            f"{self.base_url}/collections/{self.collection_name}/points",
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='PUT'
        )
        
        with urllib.request.urlopen(req, timeout=10):
            return point_id
    
    def batch_store_embeddings(self, records: List[Dict[str, Any]]) -> int:
        """
        Batch store embeddings
        
        Args:
            records: List of embedding records
            
        Returns:
            Number of records stored
        """
        if not self.available:
            raise Exception("Qdrant not available")
        
        points = []
        for rec in records:
            point_id = hashlib.md5(
                f"{rec['document_id']}_{rec['chunk_id']}".encode()
            ).hexdigest()
            
            payload = {
                "document_id": rec['document_id'],
                "chunk_id": rec['chunk_id'],
                "content": rec['content'],
                "case_id": rec.get('case_id'),
                "model_used": rec.get('model_used')
            }
            
            if rec.get('metadata'):
                payload.update(rec['metadata'])
            
            points.append({
                "id": point_id,
                "vector": rec['embedding'],
                "payload": payload
            })
        
        # Batch upsert
        data = {"points": points}
        
        req = urllib.request.Request(
            f"{self.base_url}/collections/{self.collection_name}/points",
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='PUT'
        )
        
        with urllib.request.urlopen(req, timeout=30):
            return len(points)
    
    def semantic_search(
        self,
        query_embedding: List[float],
        case_id: Optional[str] = None,
        limit: int = 10,
        score_threshold: float = 0.7
    ) -> List[QdrantSearchResult]:
        """
        Semantic search in Qdrant
        
        Args:
            query_embedding: Query vector
            case_id: Optional case filter
            limit: Max results
            score_threshold: Minimum score
            
        Returns:
            List of search results
        """
        if not self.available:
            raise Exception("Qdrant not available")
        
        # Build search request
        data = {
            "vector": query_embedding,
            "limit": limit,
            "score_threshold": score_threshold,
            "with_payload": True
        }
        
        # Add filter if case_id provided
        if case_id:
            data["filter"] = {
                "must": [
                    {
                        "key": "case_id",
                        "match": {"value": case_id}
                    }
                ]
            }
        
        req = urllib.request.Request(
            f"{self.base_url}/collections/{self.collection_name}/points/search",
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            return [
                QdrantSearchResult(
                    document_id=hit['payload']['document_id'],
                    chunk_id=hit['payload']['chunk_id'],
                    content=hit['payload']['content'],
                    score=hit['score'],
                    metadata=hit['payload']
                )
                for hit in result.get('result', [])
            ]
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get collection information"""
        if not self.available:
            return {"available": False}
        
        try:
            req = urllib.request.Request(
                f"{self.base_url}/collections/{self.collection_name}"
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                return data.get('result', {})
        except:
            return {"error": "Failed to get collection info"}
    
    def delete_collection(self):
        """Delete collection"""
        if not self.available:
            return False
        
        req = urllib.request.Request(
            f"{self.base_url}/collections/{self.collection_name}",
            method='DELETE'
        )
        
        try:
            with urllib.request.urlopen(req, timeout=10):
                print(f"✅ Collection deleted: {self.collection_name}")
                return True
        except:
            return False


def test_qdrant_client():
    """Test Qdrant client"""
    print("🧪 Testing Qdrant Client...\n")
    
    # Initialize
    print("1. Connecting to Qdrant...")
    client = QdrantClient()
    
    if not client.available:
        print("   ⚠️  Qdrant not available - start with: docker-compose up -d qdrant")
        return
    
    print("   ✅ Qdrant connected")
    
    # Get collection info
    print("\n2. Collection info...")
    info = client.get_collection_info()
    print(f"   Vectors: {info.get('vectors_count', 0)}")
    print(f"   Status: {info.get('status', 'unknown')}")
    
    # Store test embedding
    print("\n3. Storing test embedding...")
    test_embedding = [0.1] * 1024
    point_id = client.store_embedding(
        document_id="test_doc_001",
        chunk_id=0,
        content="Test content for Qdrant semantic search.",
        embedding=test_embedding,
        metadata={"test": True, "case_id": "test_case"}
    )
    print(f"   ✅ Stored: {point_id}")
    
    # Semantic search
    print("\n4. Semantic search...")
    results = client.semantic_search(
        query_embedding=test_embedding,
        case_id="test_case",
        limit=5
    )
    print(f"   ✅ Found {len(results)} results")
    if results:
        print(f"   Top result: {results[0].content[:50]}... (score: {results[0].score:.3f})")
    
    # Batch store
    print("\n5. Batch store test...")
    batch_records = [
        {
            "document_id": f"batch_doc_{i}",
            "chunk_id": 0,
            "content": f"Batch content {i}",
            "embedding": [0.1 + i*0.01] * 1024,
            "case_id": "batch_test"
        }
        for i in range(5)
    ]
    stored = client.batch_store_embeddings(batch_records)
    print(f"   ✅ Batch stored: {stored} embeddings")
    
    print("\n✅ Qdrant tests complete!")


if __name__ == "__main__":
    test_qdrant_client()
