"""
Qdrant vector store using E5 embeddings and BGE reranker
"""

import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    Filter, FieldCondition, MatchValue
)

# Import E5 embeddings and BGE reranker
import sys
import importlib.util

# Load E5 semantic matcher
semantic_matcher_path = Path(__file__).parent.parent / "document_processing" / "semantic_matcher.py"
spec = importlib.util.spec_from_file_location("semantic_matcher", semantic_matcher_path)
semantic_matcher_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(semantic_matcher_module)
E5SemanticMatcher = semantic_matcher_module.E5SemanticMatcher

from .document_loader import DocumentChunk

logger = logging.getLogger(__name__)


class QdrantVectorStore:
    """
    Qdrant-based vector store using E5 embeddings (1024 dims) and BGE reranker

    Storage structure:
        Collection: rag_documents
        Vector size: 1024 (E5)
        Distance: Cosine
        Payload: {company, year, content, metadata, chunk_index}
    """

    def __init__(
        self,
        collection_name: str = "rag_documents",
        qdrant_url: str = "http://localhost:6333",
        use_reranker: bool = True
    ):
        self.collection_name = collection_name
        self.qdrant_url = qdrant_url
        self.use_reranker = use_reranker

        # Initialize Qdrant client
        self.client = QdrantClient(url=qdrant_url)

        # Initialize E5 embeddings
        self.embedder = E5SemanticMatcher()

        # Initialize BGE reranker if enabled
        if use_reranker:
            try:
                from sentence_transformers import CrossEncoder
                self.reranker = CrossEncoder('BAAI/bge-reranker-base')
                logger.info("BGE reranker initialized")
            except Exception as e:
                logger.warning(f"Could not load BGE reranker: {e}. Continuing without reranking.")
                self.reranker = None
                self.use_reranker = False
        else:
            self.reranker = None

        # Create collection if it doesn't exist
        self._ensure_collection_exists()

        logger.info(f"QdrantVectorStore initialized: {qdrant_url}/{collection_name}")

    def _ensure_collection_exists(self):
        """
        Create collection if it doesn't exist
        """
        collections = self.client.get_collections().collections
        collection_names = [c.name for c in collections]

        if self.collection_name not in collection_names:
            logger.info(f"Creating collection: {self.collection_name}")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=1024,  # E5 embedding dimension
                    distance=Distance.COSINE
                )
            )
            logger.info(f"✓ Collection created: {self.collection_name}")
        else:
            logger.info(f"Collection already exists: {self.collection_name}")

    def ingest_documents(
        self,
        company: str,
        year: int,
        chunks: List[DocumentChunk],
        batch_size: int = 50
    ):
        """
        Ingest document chunks into Qdrant

        Args:
            company: Company name
            year: Year
            chunks: List of DocumentChunk objects
            batch_size: Batch size for embedding generation
        """
        if not chunks:
            logger.warning(f"No chunks to ingest for {company} ({year})")
            return

        logger.info(f"Ingesting {len(chunks)} chunks for {company} ({year})...")

        points = []

        # Generate embeddings and create points
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]

            for chunk in batch:
                # Generate embedding
                text = f"passage: {chunk.content}"
                emb = self.embedder.embed_text(text)

                if emb is None:
                    logger.warning(f"Failed to embed chunk {chunk.chunk_index}, skipping")
                    continue

                # Create point with section_type in payload
                point_id = f"{company.lower().replace(' ', '_')}_{year}_{chunk.chunk_index}"
                point = PointStruct(
                    id=hash(point_id) % (2**63),  # Convert to valid point ID
                    vector=emb.tolist(),
                    payload={
                        "company": company,
                        "year": year,
                        "content": chunk.content,
                        "metadata": chunk.metadata,
                        "chunk_index": chunk.chunk_index,
                        "section_type": chunk.section_type,  # ADD SECTION TYPE
                        "doc_id": point_id
                    }
                )
                points.append(point)

            if (i + batch_size) % 200 == 0:
                logger.info(f"  Processed {min(i + batch_size, len(chunks))}/{len(chunks)} chunks")

        # Upload to Qdrant in batches
        logger.info("  Uploading to Qdrant...")
        for i in range(0, len(points), 100):
            batch_points = points[i:i + 100]
            self.client.upsert(
                collection_name=self.collection_name,
                points=batch_points
            )

        logger.info(f"✅ Ingested {len(points)} chunks for {company} ({year})")

    def search(
        self,
        query: str,
        company: Optional[str] = None,
        year: Optional[int] = None,
        section_type: Optional[str] = None,
        top_k: int = 3,
        rerank_top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Semantic search for relevant chunks with optional reranking

        Args:
            query: Search query
            company: Filter by company (None = all companies)
            year: Filter by year (None = all years)
            section_type: Filter by section type (e.g., "risk_factors", "strategy")
            top_k: Number of final results to return
            rerank_top_k: Number of results to retrieve before reranking

        Returns:
            List of results with content, score, metadata
        """
        # Embed query
        query_emb = self.embedder.embed_text(f"query: {query}")

        if query_emb is None:
            logger.error("Query embedding failed")
            return []

        # Build filter
        filter_conditions = []
        if company:
            filter_conditions.append(
                FieldCondition(key="company", match=MatchValue(value=company))
            )
        if year:
            filter_conditions.append(
                FieldCondition(key="year", match=MatchValue(value=year))
            )
        if section_type:
            filter_conditions.append(
                FieldCondition(key="section_type", match=MatchValue(value=section_type))
            )

        query_filter = Filter(must=filter_conditions) if filter_conditions else None

        # Search Qdrant
        search_limit = rerank_top_k if self.use_reranker and self.reranker else top_k

        search_results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_emb.tolist(),
            query_filter=query_filter,
            limit=search_limit
        )

        if not search_results:
            logger.warning(f"No results found for query: {query}")
            return []

        # Convert to result format
        results = []
        for hit in search_results:
            results.append({
                "content": hit.payload["content"],
                "score": hit.score,
                "metadata": hit.payload["metadata"],
                "chunk_index": hit.payload["chunk_index"],
                "company": hit.payload["company"],
                "year": hit.payload["year"],
                "section_type": hit.payload.get("section_type", "unknown")
            })

        # Rerank if enabled
        if self.use_reranker and self.reranker and len(results) > top_k:
            logger.info(f"Reranking {len(results)} results with BGE...")

            # Prepare pairs for reranker
            pairs = [[query, result["content"]] for result in results]

            # Get reranking scores
            rerank_scores = self.reranker.predict(pairs)

            # Add rerank scores to results
            for result, rerank_score in zip(results, rerank_scores):
                result["rerank_score"] = float(rerank_score)
                # Keep original similarity score
                result["similarity_score"] = result["score"]
                # Use rerank score as primary score
                result["score"] = float(rerank_score)

            # Sort by rerank score
            results.sort(key=lambda x: x["rerank_score"], reverse=True)
            results = results[:top_k]

            logger.info(f"Reranked and selected top {len(results)} results")

        return results

    def delete_documents(self, company: str, year: int):
        """
        Delete all documents for a specific company and year

        Args:
            company: Company name
            year: Year
        """
        filter_conditions = [
            FieldCondition(key="company", match=MatchValue(value=company)),
            FieldCondition(key="year", match=MatchValue(value=year))
        ]

        self.client.delete(
            collection_name=self.collection_name,
            points_selector=Filter(must=filter_conditions)
        )

        logger.info(f"Deleted documents for {company} ({year})")

    def list_ingested_documents(self) -> List[Dict[str, Any]]:
        """
        List all ingested documents (unique company-year combinations)

        Returns:
            List of documents with metadata
        """
        # Scroll through all points and extract unique company-year combinations
        documents = {}

        offset = None
        while True:
            results, offset = self.client.scroll(
                collection_name=self.collection_name,
                limit=100,
                offset=offset
            )

            if not results:
                break

            for point in results:
                company = point.payload["company"]
                year = point.payload["year"]
                key = f"{company}_{year}"

                if key not in documents:
                    documents[key] = {
                        "company": company,
                        "year": year,
                        "num_chunks": 0
                    }

                documents[key]["num_chunks"] += 1

            if offset is None:
                break

        return list(documents.values())
