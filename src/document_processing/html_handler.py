"""
HTML Financial Document Handler

Extracts financial statements from HTML web pages using BeautifulSoup.

Author: Destiny Team
Date: 2025-11-06
"""

import logging
from pathlib import Path
from typing import List, Dict, Optional
import re

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

from .intelligent_extractor import (
    ExtractionResult,
    ExtractionMethod,
    LanguageDetector,
    MultiLanguagePatterns,
)

logger = logging.getLogger(__name__)


class HTMLExtractionStrategy:
    """
    Extract financial statements from HTML files
    """

    def __init__(self):
        self.language_detector = LanguageDetector()
        self.pattern_provider = MultiLanguagePatterns()

    def is_available(self) -> bool:
        """Check if BeautifulSoup is available"""
        return BS4_AVAILABLE

    def extract(self, html_path: Path) -> ExtractionResult:
        """
        Main extraction entry point

        1. Try table extraction
        2. Fallback to text parsing
        """
        if not self.is_available():
            return ExtractionResult(
                success=False,
                error="beautifulsoup4 not installed. Run: pip install beautifulsoup4"
            )

        try:
            logger.info(f"📄 Extracting from HTML: {html_path.name}")

            with open(html_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')

            # Detect language
            text = soup.get_text()
            language = self.language_detector.detect(text)
            logger.info(f"   Detected language: {language}")

            # Strategy 1: Extract from tables
            tables = soup.find_all('table')
            logger.info(f"   Found {len(tables)} tables")

            for i, table in enumerate(tables):
                if self._is_balance_sheet(table):
                    logger.info(f"   ✅ Found balance sheet in table {i+1}")
                    result = self._extract_from_table(table, language)
                    if result.success:
                        result.metadata['extraction_method'] = ExtractionMethod.HTML_TABLES.value
                        return result

            # Strategy 2: Extract from text
            logger.info(f"   Table extraction failed, trying text parsing...")
            result = self._extract_from_text(text, language)
            if result.success:
                result.metadata['extraction_method'] = ExtractionMethod.HTML_TEXT.value
                logger.info(f"   ✅ Text extraction successful")
                return result

            return ExtractionResult(
                success=False,
                error="Could not extract balance sheet from HTML"
            )

        except Exception as e:
            logger.error(f"   ❌ HTML extraction failed: {e}")
            return ExtractionResult(
                success=False,
                error=f"HTML extraction error: {str(e)}"
            )

    def _is_balance_sheet(self, table) -> bool:
        """Check if HTML table contains balance sheet"""
        text = table.get_text()
        text_lower = text.lower()

        balance_sheet_keywords = [
            'balance sheet', 'statement of financial position',
            'aktywa razem', 'total assets', 'bilans'
        ]

        return any(keyword in text_lower for keyword in balance_sheet_keywords)

    def _extract_from_table(self, table, language: str) -> ExtractionResult:
        """
        Extract from HTML table structure
        """
        rows_data = []
        for tr in table.find_all('tr'):
            cells = [td.get_text().strip() for td in tr.find_all(['td', 'th'])]
            if cells:
                rows_data.append(cells)

        if not rows_data:
            return ExtractionResult(success=False, error="Empty table")

        # Extract financial data
        data = self._parse_table_rows(rows_data, language)

        if not data:
            return ExtractionResult(success=False, error="Could not parse table data")

        return ExtractionResult(
            success=True,
            data=data,
            metadata={
                'extraction_method': ExtractionMethod.HTML_TABLES.value,
                'table_rows': len(rows_data),
                'language': language,
            }
        )

    def _parse_table_rows(self, rows: List[List[str]], language: str) -> Dict[str, float]:
        """Parse table rows to extract financial values"""
        data = {}

        # Define search patterns
        if language == 'polish':
            search_terms = {
                'total_assets': ['aktywa razem', 'suma aktywów'],
                'total_equity': ['kapitał własny razem'],
                'total_liabilities': ['zobowiązania razem'],
                'current_assets': ['aktywa obrotowe razem'],
                'current_liabilities': ['zobowiązania krótkoterminowe razem'],
                'fixed_assets': ['aktywa trwałe razem'],
                'cash': ['środki pieniężne'],
                'inventories': ['zapasy'],
            }
        else:  # English
            search_terms = {
                'total_assets': ['total assets', 'assets total'],
                'total_equity': ['total equity', 'shareholders\' equity'],
                'total_liabilities': ['total liabilities'],
                'current_assets': ['total current assets'],
                'current_liabilities': ['total current liabilities'],
                'fixed_assets': ['total fixed assets', 'property, plant and equipment'],
                'cash': ['cash and cash equivalents'],
                'inventories': ['inventories', 'inventory'],
            }

        # Search each row
        for row in rows:
            if not row or len(row) < 2:
                continue

            label = row[0].lower()

            # Try to match each field
            for field, terms in search_terms.items():
                if any(term in label for term in terms):
                    # Extract numeric value
                    for i in range(1, len(row)):
                        value = MultiLanguagePatterns.parse_number(row[i], language)
                        if value is not None and value != 0:
                            data[field] = value
                            logger.debug(f"      Found {field}: {value:,.0f}")
                            break

        return data

    def _extract_from_text(self, text: str, language: str) -> ExtractionResult:
        """Extract from plain text using regex patterns"""
        patterns = self.pattern_provider.get_patterns(language)
        data = {}

        for field, pattern_list in patterns.items():
            for pattern in pattern_list:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    value_str = match.group(1)
                    value = MultiLanguagePatterns.parse_number(value_str, language)
                    if value is not None:
                        data[field] = value
                        logger.debug(f"      Found {field}: {value:,.0f}")
                        break

        if not data:
            return ExtractionResult(success=False, error="No financial data found in HTML text")

        return ExtractionResult(
            success=True,
            data=data,
            metadata={'language': language}
        )

    def get_fallback_strategies(self) -> List[str]:
        """Return list of fallback strategies"""
        return ['tables', 'text']

    def extract_with_strategy(self, html_path: Path, strategy: str) -> ExtractionResult:
        """Extract using specific strategy"""
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        text = soup.get_text()
        language = self.language_detector.detect(text)

        if strategy == 'tables':
            tables = soup.find_all('table')
            for table in tables:
                if self._is_balance_sheet(table):
                    return self._extract_from_table(table, language)
            return ExtractionResult(success=False, error="No balance sheet table found")

        elif strategy == 'text':
            return self._extract_from_text(text, language)
        else:
            return ExtractionResult(success=False, error=f"Unknown strategy: {strategy}")


__all__ = ['HTMLExtractionStrategy']
