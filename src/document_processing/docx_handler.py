"""
DOCX (Microsoft Word) Financial Document Handler

Extracts financial statements from Word documents using table structure
and text parsing fallback.

Author: Destiny Team
Date: 2025-11-06
"""

import logging
from pathlib import Path
from typing import List, Dict, Optional, TYPE_CHECKING
import re

try:
    from docx import Document
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
    # Define dummy types for type hints when library not available
    if not TYPE_CHECKING:
        Document = None  # type: ignore
        Table = None  # type: ignore
        Paragraph = None  # type: ignore

from .intelligent_extractor import (
    ExtractionResult,
    ExtractionMethod,
    LanguageDetector,
    MultiLanguagePatterns,
)

logger = logging.getLogger(__name__)


class DOCXExtractionStrategy:
    """
    Extract financial statements from Word documents
    """

    def __init__(self):
        self.language_detector = LanguageDetector()
        self.pattern_provider = MultiLanguagePatterns()

    def is_available(self) -> bool:
        """Check if python-docx is available"""
        return DOCX_AVAILABLE

    def extract(self, docx_path: Path) -> ExtractionResult:
        """
        Main extraction entry point

        1. Try table extraction (most structured)
        2. Fallback to text parsing
        """
        if not self.is_available():
            return ExtractionResult(
                success=False,
                error="python-docx not installed. Run: pip install python-docx"
            )

        try:
            logger.info(f"📄 Extracting from DOCX: {docx_path.name}")
            doc = Document(str(docx_path))

            # Detect language
            full_text = self._extract_full_text(doc)
            language = self.language_detector.detect(full_text)
            logger.info(f"   Detected language: {language}")

            # Strategy 1: Extract from tables
            result = self._extract_from_tables(doc, language)
            if result.success:
                result.metadata['extraction_method'] = ExtractionMethod.DOCX_TABLES.value
                logger.info(f"   ✅ Table extraction successful")
                return result

            # Strategy 2: Extract from text
            logger.info(f"   Table extraction failed, trying text parsing...")
            result = self._extract_from_text(full_text, language)
            if result.success:
                result.metadata['extraction_method'] = ExtractionMethod.DOCX_TEXT.value
                logger.info(f"   ✅ Text extraction successful")
                return result

            return ExtractionResult(
                success=False,
                error="Could not extract balance sheet from DOCX"
            )

        except Exception as e:
            logger.error(f"   ❌ DOCX extraction failed: {e}")
            return ExtractionResult(
                success=False,
                error=f"DOCX extraction error: {str(e)}"
            )

    def _extract_full_text(self, doc: Document) -> str:
        """Extract all text from document"""
        paragraphs = [p.text for p in doc.paragraphs]
        return "\n".join(paragraphs)

    def _extract_from_tables(self, doc: Document, language: str) -> ExtractionResult:
        """
        Extract from Word table structure
        """
        # Find tables that look like balance sheets
        for table in doc.tables:
            if self._is_balance_sheet(table):
                return self._extract_from_table(table, language)

        return ExtractionResult(success=False, error="No balance sheet table found")

    def _is_balance_sheet(self, table: Table) -> bool:
        """Check if table contains balance sheet markers"""
        text = self._table_to_text(table)
        text_lower = text.lower()

        balance_sheet_keywords = [
            'aktywa razem', 'total assets', 'bilans', 'balance sheet',
            'statement of financial position', 'sytuacji finansowej'
        ]

        return any(keyword in text_lower for keyword in balance_sheet_keywords)

    def _table_to_text(self, table: Table) -> str:
        """Convert table to text for analysis"""
        text = []
        for row in table.rows:
            row_text = " ".join(cell.text.strip() for cell in row.cells)
            text.append(row_text)
        return "\n".join(text)

    def _extract_from_table(self, table: Table, language: str) -> ExtractionResult:
        """
        Extract values from Word table structure

        Table format typically:
        Row 1: Headers (Item | Current Year | Prior Year)
        Row 2+: Line items with values
        """
        rows_data = []
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
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
                'extraction_method': ExtractionMethod.DOCX_TABLES.value,
                'table_rows': len(rows_data),
                'language': language,
            }
        )

    def _parse_table_rows(self, rows: List[List[str]], language: str) -> Dict[str, float]:
        """
        Parse table rows to extract financial values

        Looks for key line items:
        - Total Assets / Aktywa razem
        - Total Equity / Kapitał własny razem
        - Total Liabilities / Zobowiązania razem
        etc.
        """
        data = {}

        # Define search patterns for different languages
        if language == 'polish':
            search_terms = {
                'total_assets': ['aktywa razem', 'suma aktywów'],
                'total_equity': ['kapitał własny razem', 'kapitał własny ogółem'],
                'total_liabilities': ['zobowiązania razem', 'zobowiązania ogółem'],
                'current_assets': ['aktywa obrotowe razem', 'aktywa obrotowe ogółem'],
                'current_liabilities': ['zobowiązania krótkoterminowe razem'],
                'fixed_assets': ['aktywa trwałe razem', 'aktywa trwałe ogółem'],
                'cash': ['środki pieniężne', 'gotówka'],
                'inventories': ['zapasy'],
            }
        else:  # English
            search_terms = {
                'total_assets': ['total assets', 'assets total'],
                'total_equity': ['total equity', 'shareholders\' equity', 'stockholders\' equity'],
                'total_liabilities': ['total liabilities', 'liabilities total'],
                'current_assets': ['total current assets', 'current assets total'],
                'current_liabilities': ['total current liabilities', 'current liabilities total'],
                'fixed_assets': ['total fixed assets', 'property, plant and equipment', 'ppe'],
                'cash': ['cash and cash equivalents', 'cash'],
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
                    # Extract numeric value (usually in column 1 or 2)
                    for i in range(1, len(row)):
                        value = MultiLanguagePatterns.parse_number(row[i], language)
                        if value is not None and value != 0:
                            data[field] = value
                            logger.debug(f"      Found {field}: {value:,.0f}")
                            break

        return data

    def _extract_from_text(self, text: str, language: str) -> ExtractionResult:
        """
        Extract from plain text using regex patterns
        """
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
            return ExtractionResult(success=False, error="No financial data found in text")

        return ExtractionResult(
            success=True,
            data=data,
            metadata={
                'extraction_method': ExtractionMethod.DOCX_TEXT.value,
                'language': language,
            }
        )

    def get_fallback_strategies(self) -> List[str]:
        """Return list of fallback strategies"""
        return ['tables', 'text']

    def extract_with_strategy(self, docx_path: Path, strategy: str) -> ExtractionResult:
        """Extract using specific strategy"""
        doc = Document(str(docx_path))
        full_text = self._extract_full_text(doc)
        language = self.language_detector.detect(full_text)

        if strategy == 'tables':
            return self._extract_from_tables(doc, language)
        elif strategy == 'text':
            return self._extract_from_text(full_text, language)
        else:
            return ExtractionResult(success=False, error=f"Unknown strategy: {strategy}")


__all__ = ['DOCXExtractionStrategy']
