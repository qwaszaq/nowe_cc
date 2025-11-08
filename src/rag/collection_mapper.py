"""
Collection Mapper for RAG System
Maps analysis years to appropriate Qdrant collections
"""

from typing import List, Dict, Set
import logging

logger = logging.getLogger(__name__)


# Collection metadata registry
# Maps collections to their year coverage
COLLECTION_REGISTRY: Dict[str, Dict] = {
    "azoty_2019_2021_multi_year": {
        "years": [2019, 2020, 2021],
        "company": "Grupa Azoty",
        "description": "Pre-crisis period (2019-2021)",
        "documents": [
            "Financial Statements 2019, 2020, 2021",
            "Directors Reports 2019, 2020, 2021"
        ]
    },
    "rag_documents": {
        "years": [2022, 2023, 2024],
        "company": "Grupa Azoty",
        "description": "Crisis period (2022-2024)",
        "documents": [
            "Financial Statements 2022, 2023, 2024",
            "Directors Reports 2022, 2023, 2024"
        ]
    }
}


def get_collections_for_years(
    years: List[int],
    company: str = "Grupa Azoty"
) -> List[str]:
    """
    Map analysis years to appropriate Qdrant collections

    This is the smart collection selector that prevents querying
    wrong collections (e.g., querying 2019-2021 collection when
    analyzing 2022-2024 data).

    Args:
        years: List of years to analyze (e.g., [2022, 2023, 2024])
        company: Company name (default: "Grupa Azoty")

    Returns:
        List of collection names to query

    Examples:
        >>> get_collections_for_years([2022, 2023, 2024])
        ['rag_documents']

        >>> get_collections_for_years([2019, 2020, 2021])
        ['azoty_2019_2021_multi_year']

        >>> get_collections_for_years([2019, 2020, 2021, 2022, 2023, 2024])
        ['azoty_2019_2021_multi_year', 'rag_documents']
    """
    if not years:
        logger.warning("No years provided, defaulting to rag_documents")
        return ["rag_documents"]

    years_set = set(years)
    selected_collections = []

    # Find collections that have overlap with requested years
    for collection_name, metadata in COLLECTION_REGISTRY.items():
        collection_years = set(metadata["years"])

        # Check if there's any overlap
        if years_set & collection_years:  # Intersection
            selected_collections.append(collection_name)
            logger.info(
                f"Selected collection '{collection_name}' for years {sorted(years_set & collection_years)}"
            )

    # Fallback to default if no match
    if not selected_collections:
        logger.warning(
            f"No collections found for years {years}, defaulting to rag_documents"
        )
        selected_collections = ["rag_documents"]

    logger.info(
        f"Collection mapping for years {years}: {selected_collections}"
    )

    return selected_collections


def get_years_for_collection(collection_name: str) -> List[int]:
    """
    Get the years covered by a specific collection

    Args:
        collection_name: Name of the collection

    Returns:
        List of years covered by the collection

    Example:
        >>> get_years_for_collection("azoty_2019_2021_multi_year")
        [2019, 2020, 2021]
    """
    if collection_name in COLLECTION_REGISTRY:
        return COLLECTION_REGISTRY[collection_name]["years"]

    logger.warning(f"Collection '{collection_name}' not in registry")
    return []


def list_available_collections(company: str = "Grupa Azoty") -> List[Dict]:
    """
    List all available collections with their metadata

    Args:
        company: Filter by company (default: "Grupa Azoty")

    Returns:
        List of collection metadata

    Example:
        >>> collections = list_available_collections()
        >>> for coll in collections:
        >>>     print(f"{coll['name']}: {coll['years']}")
    """
    collections = []

    for name, metadata in COLLECTION_REGISTRY.items():
        if company.lower() in metadata["company"].lower():
            collections.append({
                "name": name,
                "years": metadata["years"],
                "description": metadata["description"],
                "documents": metadata["documents"]
            })

    return collections


def validate_year_coverage(years: List[int]) -> Dict[str, List[int]]:
    """
    Validate which years have RAG coverage

    Args:
        years: Years to validate

    Returns:
        Dictionary with 'covered' and 'missing' year lists

    Example:
        >>> validate_year_coverage([2019, 2020, 2025])
        {'covered': [2019, 2020], 'missing': [2025]}
    """
    all_covered_years = set()

    for metadata in COLLECTION_REGISTRY.values():
        all_covered_years.update(metadata["years"])

    years_set = set(years)
    covered = sorted(years_set & all_covered_years)
    missing = sorted(years_set - all_covered_years)

    return {
        "covered": covered,
        "missing": missing
    }


def get_collection_info(collection_name: str) -> Dict:
    """
    Get detailed information about a collection

    Args:
        collection_name: Name of the collection

    Returns:
        Collection metadata dictionary
    """
    if collection_name in COLLECTION_REGISTRY:
        return {
            "name": collection_name,
            **COLLECTION_REGISTRY[collection_name]
        }

    return {}


# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    print("=" * 80)
    print("COLLECTION MAPPER TEST")
    print("=" * 80)

    # Test 1: Pre-crisis years
    print("\n1. Analyzing pre-crisis years (2019-2021):")
    collections = get_collections_for_years([2019, 2020, 2021])
    print(f"   Collections: {collections}")
    print(f"   Expected: ['azoty_2019_2021_multi_year']")

    # Test 2: Crisis years
    print("\n2. Analyzing crisis years (2022-2024):")
    collections = get_collections_for_years([2022, 2023, 2024])
    print(f"   Collections: {collections}")
    print(f"   Expected: ['rag_documents']")

    # Test 3: Full 6-year span
    print("\n3. Analyzing full 6-year span (2019-2024):")
    collections = get_collections_for_years([2019, 2020, 2021, 2022, 2023, 2024])
    print(f"   Collections: {collections}")
    print(f"   Expected: ['azoty_2019_2021_multi_year', 'rag_documents']")

    # Test 4: Single year (2023)
    print("\n4. Analyzing single year (2023):")
    collections = get_collections_for_years([2023])
    print(f"   Collections: {collections}")
    print(f"   Expected: ['rag_documents']")

    # Test 5: Year coverage validation
    print("\n5. Validating year coverage (2019-2025):")
    coverage = validate_year_coverage([2019, 2020, 2021, 2022, 2023, 2024, 2025])
    print(f"   Covered: {coverage['covered']}")
    print(f"   Missing: {coverage['missing']}")

    # Test 6: List all collections
    print("\n6. Available collections:")
    for coll in list_available_collections():
        print(f"   {coll['name']}:")
        print(f"     Years: {coll['years']}")
        print(f"     Description: {coll['description']}")

    print("\n" + "=" * 80)
    print("✅ All tests complete")
    print("=" * 80)
