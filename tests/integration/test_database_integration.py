#!/usr/bin/env python3
"""
Database Integration Tests
Tests all 4 databases with real connections and data persistence
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import time
from typing import List, Dict, Any
import json

print("=" * 80)
print("DATABASE INTEGRATION TESTS")
print("Testing: PostgreSQL, Qdrant, Elasticsearch, Neo4j")
print("=" * 80)
print()

# Import all database clients
try:
    from src.data.postgres_client import PostgresClient
    from src.data.qdrant_client import QdrantClient
    from src.data.elasticsearch_client import ElasticsearchClient
    from src.data.neo4j_client import Neo4jClient
    from src.data.smart_router import SmartDatabaseRouter
    from src.data.embedding_pipeline import DualEmbeddingSystem
    print("✅ All imports successful")
    print()
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)


class DatabaseIntegrationTests:
    """Comprehensive database integration tests"""
    
    def __init__(self):
        self.results = {
            "total": 0,
            "passed": 0,
            "failed": 0,
            "skipped": 0,
            "tests": []
        }
        
        # Initialize clients
        self.postgres = None
        self.qdrant = None
        self.elasticsearch = None
        self.neo4j = None
        self.router = None
        self.embeddings = None
        
    def log_test(self, name: str, status: str, details: str = "", duration: float = 0):
        """Log test result"""
        self.results["total"] += 1
        self.results["tests"].append({
            "name": name,
            "status": status,
            "details": details,
            "duration": duration
        })
        
        if status == "PASS":
            self.results["passed"] += 1
            print(f"  ✅ {name} ({duration:.2f}s)")
        elif status == "FAIL":
            self.results["failed"] += 1
            print(f"  ❌ {name}: {details}")
        elif status == "SKIP":
            self.results["skipped"] += 1
            print(f"  ⏭️  {name}: {details}")
        
        if details and status != "SKIP":
            print(f"     {details}")
    
    def test_1_connectivity(self):
        """Test 1: Database Connectivity"""
        print("\n" + "=" * 80)
        print("TEST 1: Database Connectivity")
        print("=" * 80)
        
        # PostgreSQL
        start = time.time()
        try:
            self.postgres = PostgresClient()
            if self.postgres.health_check():
                self.log_test("PostgreSQL Connection", "PASS", 
                            "Successfully connected to PostgreSQL",
                            time.time() - start)
            else:
                self.log_test("PostgreSQL Connection", "FAIL",
                            "Health check failed")
        except Exception as e:
            self.log_test("PostgreSQL Connection", "FAIL", str(e))
        
        # Qdrant
        start = time.time()
        try:
            self.qdrant = QdrantClient()
            if self.qdrant.health_check():
                self.log_test("Qdrant Connection", "PASS",
                            "Successfully connected to Qdrant",
                            time.time() - start)
            else:
                self.log_test("Qdrant Connection", "FAIL",
                            "Health check failed")
        except Exception as e:
            self.log_test("Qdrant Connection", "FAIL", str(e))
        
        # Elasticsearch
        start = time.time()
        try:
            self.elasticsearch = ElasticsearchClient()
            if self.elasticsearch.health_check():
                self.log_test("Elasticsearch Connection", "PASS",
                            "Successfully connected to Elasticsearch",
                            time.time() - start)
            else:
                self.log_test("Elasticsearch Connection", "FAIL",
                            "Health check failed")
        except Exception as e:
            self.log_test("Elasticsearch Connection", "FAIL", str(e))
        
        # Neo4j
        start = time.time()
        try:
            self.neo4j = Neo4jClient()
            if self.neo4j.health_check():
                self.log_test("Neo4j Connection", "PASS",
                            "Successfully connected to Neo4j",
                            time.time() - start)
            else:
                self.log_test("Neo4j Connection", "FAIL",
                            "Health check failed")
        except Exception as e:
            self.log_test("Neo4j Connection", "FAIL", str(e))
    
    def test_2_embeddings(self):
        """Test 2: Embedding Generation"""
        print("\n" + "=" * 80)
        print("TEST 2: Embedding Generation")
        print("=" * 80)
        
        start = time.time()
        try:
            self.embeddings = DualEmbeddingSystem()
            
            # Test general text
            test_text = "This is a test document for embedding generation."
            result = self.embeddings.embed(test_text, document_type="general")
            
            if result.embedding and len(result.embedding) == 1024:
                self.log_test("General Text Embedding", "PASS",
                            f"Generated {len(result.embedding)}-dim vector with {result.model}",
                            time.time() - start)
            else:
                self.log_test("General Text Embedding", "FAIL",
                            "Invalid embedding dimensions")
        except Exception as e:
            self.log_test("General Text Embedding", "FAIL", str(e))
        
        # Test financial text
        start = time.time()
        try:
            financial_text = "Q1 revenue was $10M, up 25% YoY. EBITDA margin improved to 30%."
            result = self.embeddings.embed(financial_text, document_type="financial")
            
            if result.embedding and len(result.embedding) == 1024:
                self.log_test("Financial Text Embedding", "PASS",
                            f"Generated {len(result.embedding)}-dim vector with {result.model}",
                            time.time() - start)
            else:
                self.log_test("Financial Text Embedding", "FAIL",
                            "Invalid embedding dimensions")
        except Exception as e:
            self.log_test("Financial Text Embedding", "FAIL", str(e))
    
    def test_3_postgres_storage(self):
        """Test 3: PostgreSQL Storage & Retrieval"""
        print("\n" + "=" * 80)
        print("TEST 3: PostgreSQL Storage & Retrieval")
        print("=" * 80)
        
        if not self.postgres or not self.embeddings:
            self.log_test("PostgreSQL Storage", "SKIP", "Prerequisites not met")
            return
        
        # Store embedding
        start = time.time()
        try:
            test_doc = "This is a test document for PostgreSQL storage."
            embedding_result = self.embeddings.embed(test_doc)
            
            doc_id = self.postgres.store_embedding(
                case_id="test_case_001",
                document_id="test_doc_001",
                chunk_id=0,
                content=test_doc,
                embedding=embedding_result.embedding,
                metadata={
                    "test": True,
                    "timestamp": time.time()
                }
            )
            
            self.log_test("PostgreSQL Store Embedding", "PASS",
                        f"Stored with ID: {doc_id}",
                        time.time() - start)
        except Exception as e:
            self.log_test("PostgreSQL Store Embedding", "FAIL", str(e))
            return
        
        # Semantic search
        start = time.time()
        try:
            query = "test document storage"
            query_embedding = self.embeddings.embed(query).embedding
            
            results = self.postgres.semantic_search(
                query_embedding=query_embedding,
                case_id="test_case_001",
                limit=5
            )
            
            if results and len(results) > 0:
                self.log_test("PostgreSQL Semantic Search", "PASS",
                            f"Found {len(results)} results, top similarity: {results[0].similarity:.3f}",
                            time.time() - start)
            else:
                self.log_test("PostgreSQL Semantic Search", "FAIL",
                            "No results found")
        except Exception as e:
            self.log_test("PostgreSQL Semantic Search", "FAIL", str(e))
    
    def test_4_qdrant_storage(self):
        """Test 4: Qdrant Storage & Retrieval"""
        print("\n" + "=" * 80)
        print("TEST 4: Qdrant Storage & Retrieval")
        print("=" * 80)
        
        if not self.qdrant or not self.embeddings:
            self.log_test("Qdrant Storage", "SKIP", "Prerequisites not met")
            return
        
        # Store embedding
        start = time.time()
        try:
            test_doc = "This is a test document for Qdrant vector storage."
            embedding_result = self.embeddings.embed(test_doc)
            
            point_id = self.qdrant.store_embedding(
                document_id="test_doc_qdrant_001",
                chunk_id=0,
                content=test_doc,
                embedding=embedding_result.embedding,
                metadata={
                    "case_id": "test_case_001",
                    "test": True
                }
            )
            
            self.log_test("Qdrant Store Embedding", "PASS",
                        f"Stored with ID: {point_id}",
                        time.time() - start)
        except Exception as e:
            self.log_test("Qdrant Store Embedding", "FAIL", str(e))
            return
        
        # Batch store
        start = time.time()
        try:
            batch_docs = [
                "Financial analysis of Q1 results.",
                "Legal review of contract terms.",
                "Risk assessment for the project."
            ]
            
            records = []
            for i, doc in enumerate(batch_docs):
                emb = self.embeddings.embed(doc).embedding
                records.append({
                    "document_id": f"test_batch_{i}",
                    "chunk_id": 0,
                    "content": doc,
                    "embedding": emb,
                    "metadata": {"batch": True, "index": i}
                })
            
            count = self.qdrant.batch_store_embeddings(records)
            self.log_test("Qdrant Batch Store", "PASS",
                        f"Stored {count} records",
                        time.time() - start)
        except Exception as e:
            self.log_test("Qdrant Batch Store", "FAIL", str(e))
        
        # Semantic search
        start = time.time()
        try:
            query = "financial analysis"
            query_embedding = self.embeddings.embed(query).embedding
            
            results = self.qdrant.semantic_search(
                query_embedding=query_embedding,
                limit=5
            )
            
            if results and len(results) > 0:
                self.log_test("Qdrant Semantic Search", "PASS",
                            f"Found {len(results)} results, top score: {results[0].score:.3f}",
                            time.time() - start)
            else:
                self.log_test("Qdrant Semantic Search", "FAIL",
                            "No results found")
        except Exception as e:
            self.log_test("Qdrant Semantic Search", "FAIL", str(e))
    
    def test_5_elasticsearch_storage(self):
        """Test 5: Elasticsearch Document Storage"""
        print("\n" + "=" * 80)
        print("TEST 5: Elasticsearch Document Storage")
        print("=" * 80)
        
        if not self.elasticsearch:
            self.log_test("Elasticsearch Storage", "SKIP", "Prerequisites not met")
            return
        
        # Store document
        start = time.time()
        try:
            doc_id = self.elasticsearch.store_document(
                case_id="test_case_001",
                document_id="test_es_doc_001",
                filename="test_document.txt",
                content="This is a comprehensive test document for Elasticsearch full-text search capabilities.",
                document_type="text",
                metadata={
                    "author": "Test System",
                    "category": "testing"
                }
            )
            
            self.log_test("Elasticsearch Store Document", "PASS",
                        f"Stored with ID: {doc_id}",
                        time.time() - start)
        except Exception as e:
            self.log_test("Elasticsearch Store Document", "FAIL", str(e))
            return
        
        # Wait for indexing
        time.sleep(2)
        
        # Full-text search
        start = time.time()
        try:
            results = self.elasticsearch.full_text_search(
                query="test document search",
                case_id="test_case_001"
            )
            
            if results and len(results) > 0:
                self.log_test("Elasticsearch Full-Text Search", "PASS",
                            f"Found {len(results)} documents",
                            time.time() - start)
            else:
                self.log_test("Elasticsearch Full-Text Search", "FAIL",
                            "No results found")
        except Exception as e:
            self.log_test("Elasticsearch Full-Text Search", "FAIL", str(e))
    
    def test_6_neo4j_graph(self):
        """Test 6: Neo4j Graph Operations"""
        print("\n" + "=" * 80)
        print("TEST 6: Neo4j Graph Operations")
        print("=" * 80)
        
        if not self.neo4j:
            self.log_test("Neo4j Graph", "SKIP", "Prerequisites not met")
            return
        
        # Create entities
        start = time.time()
        try:
            self.neo4j.create_entity(
                case_id="test_case_001",
                entity_id="company_a",
                entity_type="Company",
                properties={"name": "Company A", "industry": "Technology"}
            )
            
            self.neo4j.create_entity(
                case_id="test_case_001",
                entity_id="person_b",
                entity_type="Person",
                properties={"name": "John Doe", "role": "CEO"}
            )
            
            self.log_test("Neo4j Create Entities", "PASS",
                        "Created 2 entities",
                        time.time() - start)
        except Exception as e:
            self.log_test("Neo4j Create Entities", "FAIL", str(e))
            return
        
        # Create relationship
        start = time.time()
        try:
            self.neo4j.create_relationship(
                from_entity_id="person_b",
                to_entity_id="company_a",
                relationship_type="WORKS_FOR",
                properties={"since": "2020"}
            )
            
            self.log_test("Neo4j Create Relationship", "PASS",
                        "Created WORKS_FOR relationship",
                        time.time() - start)
        except Exception as e:
            self.log_test("Neo4j Create Relationship", "FAIL", str(e))
    
    def test_7_smart_router(self):
        """Test 7: Smart Database Router"""
        print("\n" + "=" * 80)
        print("TEST 7: Smart Database Router")
        print("=" * 80)
        
        start = time.time()
        try:
            self.router = SmartDatabaseRouter()
            status = self.router.system_status()
            
            available = sum(1 for db in status["databases"].values() if db["status"] == "available")
            total = len(status["databases"])
            
            self.log_test("Smart Router Initialization", "PASS",
                        f"{available}/{total} databases available",
                        time.time() - start)
        except Exception as e:
            self.log_test("Smart Router Initialization", "FAIL", str(e))
            return
        
        # Test routing logic
        start = time.time()
        try:
            # Small case -> PostgreSQL
            small_target = self.router.route_embedding_storage("small_case", vector_count=1000)
            if small_target == "postgres":
                self.log_test("Router Small Case Logic", "PASS",
                            f"Correctly routed to {small_target}")
            else:
                self.log_test("Router Small Case Logic", "FAIL",
                            f"Wrong target: {small_target}")
            
            # Large case -> Qdrant
            large_target = self.router.route_embedding_storage("large_case", vector_count=150000)
            if large_target == "qdrant":
                self.log_test("Router Large Case Logic", "PASS",
                            f"Correctly routed to {large_target}")
            else:
                self.log_test("Router Large Case Logic", "FAIL",
                            f"Wrong target: {large_target}")
        except Exception as e:
            self.log_test("Router Logic", "FAIL", str(e))
    
    def test_8_end_to_end(self):
        """Test 8: End-to-End Workflow"""
        print("\n" + "=" * 80)
        print("TEST 8: End-to-End Workflow with Persistence")
        print("=" * 80)
        
        if not all([self.router, self.embeddings]):
            self.log_test("E2E Workflow", "SKIP", "Prerequisites not met")
            return
        
        start = time.time()
        try:
            # 1. Generate embeddings
            documents = [
                "Financial report shows strong Q1 performance with 25% revenue growth.",
                "Legal team completed contract review, identified 3 areas of concern.",
                "Risk assessment indicates medium-level exposure in European markets."
            ]
            
            records = []
            for i, doc in enumerate(documents):
                emb = self.embeddings.embed(doc, document_type="general")
                records.append({
                    "document_id": f"e2e_doc_{i}",
                    "chunk_id": 0,
                    "content": doc,
                    "embedding": emb.embedding,
                    "metadata": {
                        "case_id": "e2e_test_case",
                        "index": i,
                        "model": emb.model
                    }
                })
            
            # 2. Store via router (will go to PostgreSQL for small set)
            db_used, count = self.router.store_embeddings("e2e_test_case", records)
            
            # 3. Store documents in Elasticsearch
            for i, doc in enumerate(documents):
                self.router.store_document(
                    case_id="e2e_test_case",
                    document_id=f"e2e_doc_{i}",
                    filename=f"document_{i}.txt",
                    content=doc,
                    document_type="text"
                )
            
            # 4. Semantic search
            query = "financial performance"
            query_emb = self.embeddings.embed(query).embedding
            search_results = self.router.semantic_search(
                case_id="e2e_test_case",
                query_embedding=query_emb,
                limit=3
            )
            
            duration = time.time() - start
            
            if search_results and len(search_results) > 0:
                self.log_test("E2E Workflow", "PASS",
                            f"Processed {len(documents)} docs, stored in {db_used}, found {len(search_results)} results",
                            duration)
            else:
                self.log_test("E2E Workflow", "FAIL",
                            "No search results")
        except Exception as e:
            self.log_test("E2E Workflow", "FAIL", str(e))
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print(f"\nTotal Tests:    {self.results['total']}")
        print(f"✅ Passed:      {self.results['passed']}")
        print(f"❌ Failed:      {self.results['failed']}")
        print(f"⏭️  Skipped:     {self.results['skipped']}")
        print()
        
        if self.results['failed'] == 0:
            print("🎉 ALL TESTS PASSED! Database integration is working correctly.")
        else:
            print("⚠️  Some tests failed. Please review the output above.")
        
        # Save results to file
        results_file = Path(__file__).parent.parent.parent / "test_results_database.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n📄 Detailed results saved to: {results_file}")
        print()


def main():
    """Run all tests"""
    tests = DatabaseIntegrationTests()
    
    # Run test suites
    tests.test_1_connectivity()
    tests.test_2_embeddings()
    tests.test_3_postgres_storage()
    tests.test_4_qdrant_storage()
    tests.test_5_elasticsearch_storage()
    tests.test_6_neo4j_graph()
    tests.test_7_smart_router()
    tests.test_8_end_to_end()
    
    # Print summary
    tests.print_summary()
    
    # Exit code
    sys.exit(0 if tests.results['failed'] == 0 else 1)


if __name__ == "__main__":
    main()
