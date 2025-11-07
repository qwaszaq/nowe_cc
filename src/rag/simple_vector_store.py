"""
Simple file-based vector store using NumPy + JSON
No Qdrant/ChromaDB - just local files
"""

import numpy as np
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

# Import E5 embeddings (reuse existing)
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


class SimpleVectorStore:
    """
    File-based vector store using E5 embeddings stored as NumPy arrays

    Storage structure:
        data/rag_storage/
        ├── grupa_azoty_sa_2023_embeddings.npy  # NumPy array of embeddings
        ├── grupa_azoty_sa_2023_metadata.json   # Chunk metadata
        ├── grupa_azoty_sa_2022_embeddings.npy
        ├── grupa_azoty_sa_2022_metadata.json
        └── ...
    """

    def __init__(self, storage_dir: str = "data/rag_storage"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Initialize E5 embeddings
        self.embedder = E5SemanticMatcher()

        logger.info(f"SimpleVectorStore initialized: {self.storage_dir}")

    def ingest_documents(
        self,
        company: str,
        year: int,
        chunks: List[DocumentChunk],
        batch_size: int = 50
    ):
        """
        Ingest document chunks into vector store

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

        # Create document ID
        doc_id = self._create_doc_id(company, year)

        # Generate embeddings
        logger.info("  Generating embeddings...")
        embeddings = []

        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            batch_texts = [f"passage: {chunk.content}" for chunk in batch]

            for text in batch_texts:
                emb = self.embedder.embed_text(text)
                if emb is not None:
                    embeddings.append(emb)
                else:
                    # Fallback: zero embedding
                    embeddings.append(np.zeros(1024))  # E5 embedding dimension

            if (i + batch_size) % 200 == 0:
                logger.info(f"    Processed {min(i + batch_size, len(chunks))}/{len(chunks)} chunks")

        embeddings_array = np.array(embeddings)

        # Save embeddings (NumPy binary format)
        emb_path = self.storage_dir / f"{doc_id}_embeddings.npy"
        np.save(emb_path, embeddings_array)
        logger.info(f"  ✓ Saved embeddings: {emb_path} ({embeddings_array.shape})")

        # Save metadata (JSON)
        metadata = {
            "company": company,
            "year": year,
            "num_chunks": len(chunks),
            "chunks": [
                {
                    "content": chunk.content,
                    "metadata": chunk.metadata,
                    "chunk_index": chunk.chunk_index
                }
                for chunk in chunks
            ]
        }

        metadata_path = self.storage_dir / f"{doc_id}_metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        logger.info(f"  ✓ Saved metadata: {metadata_path}")
        logger.info(f"✅ Ingested {len(chunks)} chunks for {company} ({year})")

    def search(
        self,
        query: str,
        company: Optional[str] = None,
        year: Optional[int] = None,
        top_k: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Semantic search for relevant chunks

        Args:
            query: Search query
            company: Filter by company (None = all companies)
            year: Filter by year (None = all years)
            top_k: Number of results to return

        Returns:
            List of results with content, score, metadata
        """
        # Embed query
        query_emb = self.embedder.embed_text(f"query: {query}")

        if query_emb is None:
            logger.error("Query embedding failed")
            return []

        # Find relevant documents
        docs_to_search = self._get_relevant_documents(company, year)

        if not docs_to_search:
            logger.warning(f"No documents found for company={company}, year={year}")
            return []

        all_results = []

        # Search each document
        for doc_id in docs_to_search:
            emb_path = self.storage_dir / f"{doc_id}_embeddings.npy"
            metadata_path = self.storage_dir / f"{doc_id}_metadata.json"

            if not emb_path.exists() or not metadata_path.exists():
                continue

            # Load embeddings
            doc_embeddings = np.load(emb_path)

            # Load metadata
            with open(metadata_path, 'r', encoding='utf-8') as f:
                doc_metadata = json.load(f)

            # Calculate similarities
            similarities = self._cosine_similarity_batch(query_emb, doc_embeddings)

            # Get top results from this document
            top_indices = np.argsort(similarities)[::-1][:top_k]

            for idx in top_indices:
                chunk_data = doc_metadata['chunks'][idx]
                all_results.append({
                    "content": chunk_data['content'],
                    "score": float(similarities[idx]),
                    "metadata": chunk_data['metadata'],
                    "chunk_index": chunk_data['chunk_index']
                })

        # Sort all results by score and return top_k
        all_results.sort(key=lambda x: x['score'], reverse=True)
        return all_results[:top_k]

    def _create_doc_id(self, company: str, year: int) -> str:
        """
        Create document ID from company and year

        Args:
            company: Company name
            year: Year

        Returns:
            doc_id (e.g., "grupa_azoty_sa_2023")
        """
        safe_company = company.lower().replace(" ", "_").replace(".", "").replace(",", "")
        return f"{safe_company}_{year}"

    def _get_relevant_documents(
        self,
        company: Optional[str],
        year: Optional[int]
    ) -> List[str]:
        """
        Get document IDs matching filters

        Args:
            company: Company filter
            year: Year filter

        Returns:
            List of document IDs
        """
        # List all embedding files
        all_emb_files = list(self.storage_dir.glob("*_embeddings.npy"))

        doc_ids = []

        for emb_file in all_emb_files:
            doc_id = emb_file.stem.replace("_embeddings", "")

            # Apply filters
            if company:
                safe_company = company.lower().replace(" ", "_").replace(".", "").replace(",", "")
                if not doc_id.startswith(safe_company):
                    continue

            if year:
                if not doc_id.endswith(f"_{year}"):
                    continue

            doc_ids.append(doc_id)

        return doc_ids

    def _cosine_similarity_batch(
        self,
        query_emb: np.ndarray,
        doc_embeddings: np.ndarray
    ) -> np.ndarray:
        """
        Calculate cosine similarity between query and all document embeddings

        Args:
            query_emb: Query embedding (1D array)
            doc_embeddings: Document embeddings (2D array: N x dim)

        Returns:
            Similarity scores (1D array: N)
        """
        # Normalize query
        query_norm = query_emb / (np.linalg.norm(query_emb) + 1e-10)

        # Normalize documents
        doc_norms = np.linalg.norm(doc_embeddings, axis=1, keepdims=True) + 1e-10
        doc_embeddings_norm = doc_embeddings / doc_norms

        # Dot product = cosine similarity (after normalization)
        similarities = np.dot(doc_embeddings_norm, query_norm)

        return similarities

    def list_ingested_documents(self) -> List[Dict[str, Any]]:
        """
        List all ingested documents

        Returns:
            List of documents with metadata
        """
        documents = []

        metadata_files = list(self.storage_dir.glob("*_metadata.json"))

        for metadata_file in sorted(metadata_files):
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)

                documents.append({
                    "company": metadata['company'],
                    "year": metadata['year'],
                    "num_chunks": metadata['num_chunks'],
                    "doc_id": metadata_file.stem.replace("_metadata", "")
                })
            except Exception as e:
                logger.error(f"Error reading {metadata_file}: {e}")

        return documents
