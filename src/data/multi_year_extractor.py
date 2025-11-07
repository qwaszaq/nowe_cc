"""
Multi-year financial data extraction pipeline
Integrates with existing extraction system
"""

from pathlib import Path
from typing import Dict, List, Optional
import logging

# Import existing extraction system
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

# Direct import to avoid circular dependencies
import importlib.util

# Import intelligent extractor
extractor_path = Path(__file__).parent.parent / "document_processing" / "intelligent_extractor.py"
spec = importlib.util.spec_from_file_location("intelligent_extractor", extractor_path)
intelligent_extractor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(intelligent_extractor)
IntelligentExtractor = intelligent_extractor.IntelligentExtractor

from .multi_year_storage import MultiYearDataStore, save_extraction_result

logger = logging.getLogger(__name__)


class MultiYearExtractor:
    """
    Extract financial data from multiple years of reports and store in unified format
    """

    def __init__(self):
        self.extractor = IntelligentExtractor()
        self.storage = MultiYearDataStore()
        logger.info("MultiYearExtractor initialized")

    def extract_multi_year(
        self,
        company_name: str,
        industry: str,
        currency: str,
        pdf_paths: Dict[int, Path]
    ) -> Dict[str, Any]:
        """
        Extract from multiple PDFs and store as multi-year dataset

        Args:
            company_name: Company name (e.g., "Grupa Azoty S.A.")
            industry: Industry sector
            currency: Currency code
            pdf_paths: {
                2023: Path("report_2023.pdf"),
                2022: Path("report_2022.pdf"),
                2021: Path("report_2021.pdf"),
                ...
            }

        Returns:
            {
                'success': bool,
                'years_extracted': list,
                'years_failed': list,
                'data': multi-year dataset
            }
        """
        logger.info(f"=" * 80)
        logger.info(f"MULTI-YEAR EXTRACTION: {company_name}")
        logger.info(f"Years to extract: {sorted(pdf_paths.keys())}")
        logger.info(f"=" * 80)

        years_extracted = []
        years_failed = []
        all_data = {}

        for year in sorted(pdf_paths.keys()):
            pdf_path = pdf_paths[year]

            logger.info(f"\n--- Extracting {year} from {pdf_path.name} ---")

            try:
                # Extract
                result = self.extractor.extract(pdf_path)

                if result.success and result.data:
                    # Store this year's data
                    save_extraction_result(
                        company_name=company_name,
                        industry=industry,
                        currency=currency,
                        year=year,
                        extracted_data=result.data
                    )

                    all_data[year] = result.data
                    years_extracted.append(year)

                    logger.info(f"  ✅ {year}: {len(result.data)} metrics extracted")

                    if result.quality_metrics:
                        logger.info(f"     Quality: {result.quality_metrics.overall_score:.1%}")
                        logger.info(f"     Completeness: {result.quality_metrics.completeness_score:.1%}")

                else:
                    years_failed.append(year)
                    logger.warning(f"  ❌ {year}: Extraction failed - {result.error}")

            except Exception as e:
                years_failed.append(year)
                logger.error(f"  ❌ {year}: Exception - {e}", exc_info=True)

        logger.info(f"\n" + "=" * 80)
        logger.info(f"MULTI-YEAR EXTRACTION COMPLETE")
        logger.info(f"  Success: {len(years_extracted)} years")
        logger.info(f"  Failed: {len(years_failed)} years")
        logger.info(f"=" * 80)

        return {
            'success': len(years_extracted) > 0,
            'years_extracted': years_extracted,
            'years_failed': years_failed,
            'data': all_data
        }

    def load_for_analysis(self, company_name: str) -> Optional[Dict]:
        """
        Load multi-year data ready for intelligence analysis

        Args:
            company_name: Company name

        Returns:
            Data in format ready for LocalIntelligenceService
        """
        return self.storage.load_company_data(company_name)

    def get_available_years(self, company_name: str) -> List[int]:
        """
        Get years with extracted data for a company

        Args:
            company_name: Company name

        Returns:
            List of years (e.g., [2020, 2021, 2022, 2023, 2024])
        """
        return self.storage.get_years_available(company_name)


# Standalone function for easy usage
def extract_and_store_multi_year(
    company_name: str,
    industry: str,
    currency: str,
    pdf_directory: Path,
    filename_pattern: str = "*annual*.pdf"
) -> Dict:
    """
    Extract all annual reports from a directory

    Args:
        company_name: Company name
        industry: Industry sector
        currency: Currency code
        pdf_directory: Directory containing PDFs
        filename_pattern: Glob pattern for PDF files

    Returns:
        Extraction result dict
    """
    # Find all PDFs
    pdf_files = list(pdf_directory.glob(filename_pattern))

    if not pdf_files:
        logger.warning(f"No PDFs found in {pdf_directory} matching {filename_pattern}")
        return {'success': False, 'error': 'No PDFs found'}

    # Try to extract year from filename
    import re
    pdf_paths = {}

    for pdf_file in pdf_files:
        # Look for 4-digit year in filename
        year_match = re.search(r'(20\d{2})', pdf_file.name)

        if year_match:
            year = int(year_match.group(1))
            pdf_paths[year] = pdf_file
            logger.info(f"Found {year}: {pdf_file.name}")
        else:
            logger.warning(f"Could not extract year from filename: {pdf_file.name}")

    if not pdf_paths:
        return {'success': False, 'error': 'Could not determine years from filenames'}

    # Extract
    extractor = MultiYearExtractor()
    return extractor.extract_multi_year(
        company_name=company_name,
        industry=industry,
        currency=currency,
        pdf_paths=pdf_paths
    )
