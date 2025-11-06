"""
Semantic Matcher using E5 Embeddings for Financial Line Item Detection

Uses LM Studio's E5-large model to semantically match row labels to financial concepts.
This allows robust extraction even when exact text doesn't match expected patterns.

Author: Destiny Team
Date: 2025-11-06
"""

import logging
from typing import List, Dict, Tuple, Optional
import urllib.request
import urllib.error
import json
import numpy as np

logger = logging.getLogger(__name__)


class E5SemanticMatcher:
    """
    Semantic matching using E5 embeddings via LM Studio

    Maps row labels to financial concepts using vector similarity.
    """

    def __init__(
        self,
        base_url: str = "http://192.168.200.226:1234/v1",
        model: str = "text-embedding-multilingual-e5-large-instruct",
        similarity_threshold: float = 0.65
    ):
        """
        Initialize E5 semantic matcher

        Args:
            base_url: LM Studio API endpoint
            model: Embedding model name
            similarity_threshold: Minimum cosine similarity for match (0.0-1.0)
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.similarity_threshold = similarity_threshold

        # Financial concept queries (multi-language)
        self.financial_concepts = {
            'total_assets': [
                'query: Total Assets',
                'query: Aktywa razem',
                'query: Sum of all assets'
            ],
            'current_assets': [
                'query: Current Assets',
                'query: Aktywa obrotowe',
                'query: Short-term assets'
            ],
            'fixed_assets': [
                'query: Fixed Assets',
                'query: Aktywa trwałe',
                'query: Long-term assets'
            ],
            'total_equity': [
                'query: Total Equity',
                'query: Kapitał własny',
                'query: Shareholders equity'
            ],
            'total_liabilities': [
                'query: Total Liabilities',
                'query: Zobowiązania razem',
                'query: Sum of all liabilities'
            ],
            'current_liabilities': [
                'query: Current Liabilities',
                'query: Zobowiązania krótkoterminowe',
                'query: Short-term liabilities'
            ],
            'long_term_liabilities': [
                'query: Long-term Liabilities',
                'query: Zobowiązania długoterminowe',
                'query: Non-current liabilities'
            ],
            'cash': [
                'query: Cash and Cash Equivalents',
                'query: Środki pieniężne',
                'query: Cash'
            ],
            'inventories': [
                'query: Inventories',
                'query: Zapasy',
                'query: Stock'
            ],
            'revenue': [
                'query: Revenue',
                'query: Przychody',
                'query: Sales'
            ],
            'net_income': [
                'query: Net Income',
                'query: Zysk netto',
                'query: Net Profit'
            ]
        }

        # Cache embeddings to avoid re-computing
        self.concept_embeddings_cache = {}

    def embed_text(self, text: str) -> Optional[np.ndarray]:
        """
        Get embedding for text using E5 via LM Studio

        Args:
            text: Text to embed (use 'query: ' prefix for queries)

        Returns:
            Embedding vector or None if failed
        """
        try:
            url = f"{self.base_url}/embeddings"

            payload = {
                "model": self.model,
                "input": text
            }

            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )

            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))

                if 'data' in result and len(result['data']) > 0:
                    embedding = result['data'][0]['embedding']
                    return np.array(embedding)
                else:
                    logger.warning(f"No embedding returned for: {text[:50]}")
                    return None

        except Exception as e:
            logger.error(f"E5 embedding failed for '{text[:50]}': {e}")
            return None

    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(dot_product / (norm1 * norm2))

    def match_row_label(
        self,
        row_label: str,
        candidates: Optional[List[str]] = None
    ) -> Tuple[Optional[str], float]:
        """
        Match a row label to a financial concept using semantic similarity

        Args:
            row_label: Text from table row (e.g., "Aktywa razem")
            candidates: List of concept keys to search (None = all)

        Returns:
            (concept_key, confidence_score) or (None, 0.0) if no match
        """
        if not row_label or len(row_label.strip()) < 3:
            return None, 0.0

        # Embed the row label (use passage prefix for E5)
        row_text = f"passage: {row_label.strip()}"
        row_embedding = self.embed_text(row_text)

        if row_embedding is None:
            return None, 0.0

        # Check against all concepts (or subset if specified)
        concepts_to_check = candidates if candidates else list(self.financial_concepts.keys())

        best_match = None
        best_score = 0.0

        for concept_key in concepts_to_check:
            # Get embeddings for all query variations of this concept
            concept_queries = self.financial_concepts.get(concept_key, [])

            for query in concept_queries:
                # Use cache if available
                cache_key = f"{concept_key}_{query}"

                if cache_key in self.concept_embeddings_cache:
                    concept_embedding = self.concept_embeddings_cache[cache_key]
                else:
                    concept_embedding = self.embed_text(query)
                    if concept_embedding is not None:
                        self.concept_embeddings_cache[cache_key] = concept_embedding

                if concept_embedding is None:
                    continue

                # Calculate similarity
                similarity = self.cosine_similarity(row_embedding, concept_embedding)

                # Keep best match
                if similarity > best_score:
                    best_score = similarity
                    best_match = concept_key

        # Return match only if above threshold
        if best_score >= self.similarity_threshold:
            logger.info(f"✅ Matched '{row_label}' → {best_match} (confidence: {best_score:.3f})")
            return best_match, best_score
        else:
            logger.debug(f"❌ No match for '{row_label}' (best: {best_score:.3f})")
            return None, 0.0

    def match_table_rows(
        self,
        rows: List[Dict[str, str]]
    ) -> Dict[str, Tuple[str, float, int]]:
        """
        Match all rows in a table to financial concepts

        Args:
            rows: List of row dicts with 'label' and 'values' keys

        Returns:
            Dict mapping concept_key → (row_label, confidence, row_index)
        """
        matches = {}

        for i, row in enumerate(rows):
            row_label = row.get('label', '')

            if not row_label:
                continue

            concept, confidence = self.match_row_label(row_label)

            if concept:
                # Keep best match for each concept
                if concept not in matches or confidence > matches[concept][1]:
                    matches[concept] = (row_label, confidence, i)

        logger.info(f"📊 Matched {len(matches)} financial concepts from {len(rows)} rows")
        return matches

    def preload_concept_embeddings(self):
        """
        Pre-compute embeddings for all financial concepts

        Useful to do once at initialization for faster matching later.
        """
        logger.info("🔄 Pre-loading E5 embeddings for financial concepts...")

        total = 0
        for concept_key, queries in self.financial_concepts.items():
            for query in queries:
                cache_key = f"{concept_key}_{query}"

                if cache_key not in self.concept_embeddings_cache:
                    embedding = self.embed_text(query)

                    if embedding is not None:
                        self.concept_embeddings_cache[cache_key] = embedding
                        total += 1

        logger.info(f"✅ Pre-loaded {total} concept embeddings")


# Standalone test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Initialize matcher
    matcher = E5SemanticMatcher()

    # Preload embeddings
    matcher.preload_concept_embeddings()

    # Test with Polish financial terms
    test_labels = [
        "Aktywa razem",
        "Aktywa obrotowe razem",
        "Rzeczowe aktywa trwałe",
        "Kapitał własny razem",
        "Zobowiązania razem",
        "Zobowiązania krótkoterminowe razem",
        "Środki pieniężne i ich ekwiwalenty",
        "Zapasy",
        "Przychody netto ze sprzedaży",
    ]

    print("\n" + "=" * 80)
    print("TESTING E5 SEMANTIC MATCHING")
    print("=" * 80)

    for label in test_labels:
        concept, confidence = matcher.match_row_label(label)

        if concept:
            print(f"✅ '{label}' → {concept} ({confidence:.1%})")
        else:
            print(f"❌ '{label}' → NO MATCH")

    print("=" * 80)
