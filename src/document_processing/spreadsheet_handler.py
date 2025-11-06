"""
XLSX/CSV (Spreadsheet) Financial Document Handler

Extracts financial statements from Excel and CSV files - the most structured format.

Author: Destiny Team
Date: 2025-11-06
"""

import logging
from pathlib import Path
from typing import List, Dict, Optional
import re

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False

from .intelligent_extractor import (
    ExtractionResult,
    ExtractionMethod,
    LanguageDetector,
    MultiLanguagePatterns,
)

logger = logging.getLogger(__name__)


class SpreadsheetExtractionStrategy:
    """
    Extract financial statements from Excel and CSV files
    """

    def __init__(self):
        self.language_detector = LanguageDetector()

    def is_available(self) -> bool:
        """Check if pandas is available"""
        return PANDAS_AVAILABLE

    def extract(self, file_path: Path) -> ExtractionResult:
        """
        Main extraction entry point

        XLSX: Try all sheets, find the one with balance sheet
        CSV: Single sheet extraction
        """
        if not self.is_available():
            return ExtractionResult(
                success=False,
                error="pandas not installed. Run: pip install pandas openpyxl"
            )

        try:
            logger.info(f"📄 Extracting from {file_path.suffix.upper()}: {file_path.name}")

            # Load file
            if file_path.suffix == '.xlsx':
                df_dict = pd.read_excel(str(file_path), sheet_name=None)  # All sheets
            elif file_path.suffix == '.csv':
                df_dict = {'Sheet1': pd.read_csv(str(file_path))}
            else:
                return ExtractionResult(
                    success=False,
                    error=f"Unsupported file type: {file_path.suffix}"
                )

            # Find the balance sheet
            for sheet_name, df in df_dict.items():
                logger.info(f"   Checking sheet: {sheet_name}")

                if self._is_balance_sheet(df):
                    logger.info(f"   ✅ Found balance sheet in: {sheet_name}")
                    return self._extract_from_dataframe(df, file_path.suffix)

            return ExtractionResult(
                success=False,
                error="No balance sheet found in any sheet"
            )

        except Exception as e:
            logger.error(f"   ❌ Spreadsheet extraction failed: {e}")
            return ExtractionResult(
                success=False,
                error=f"Spreadsheet extraction error: {str(e)}"
            )

    def _is_balance_sheet(self, df: pd.DataFrame) -> bool:
        """Check if DataFrame contains balance sheet"""
        text = df.to_string()
        text_lower = text.lower()

        balance_sheet_keywords = [
            'aktywa razem', 'total assets', 'pasywa razem', 'total liabilities',
            'balance sheet', 'statement of financial position', 'bilans'
        ]

        return any(keyword in text_lower for keyword in balance_sheet_keywords)

    def _extract_from_dataframe(self, df: pd.DataFrame, file_type: str) -> ExtractionResult:
        """
        Extract from structured DataFrame

        Expected structure:
        Column 0: Line item labels
        Column 1: Current year values
        Column 2: Prior year values (optional)
        """
        # Detect language
        text = df.to_string()
        language = self.language_detector.detect(text)
        logger.info(f"   Detected language: {language}")

        # Find label column and value columns
        label_col = self._find_label_column(df)
        if label_col is None:
            return ExtractionResult(
                success=False,
                error="Could not identify label column"
            )

        value_cols = [c for c in df.columns if c != label_col]
        if not value_cols:
            return ExtractionResult(
                success=False,
                error="Could not identify value columns"
            )

        logger.info(f"   Label column: {label_col}")
        logger.info(f"   Value columns: {value_cols}")

        # Extract values
        data = self._extract_values(df, label_col, value_cols[0], language)

        if not data:
            return ExtractionResult(
                success=False,
                error="Could not extract any financial values"
            )

        method = ExtractionMethod.XLSX_STRUCTURED if file_type == '.xlsx' else ExtractionMethod.CSV_STRUCTURED

        return ExtractionResult(
            success=True,
            data=data,
            metadata={
                'extraction_method': method.value,
                'language': language,
                'label_column': label_col,
                'value_column': value_cols[0],
                'rows': len(df),
            }
        )

    def _find_label_column(self, df: pd.DataFrame) -> Optional[str]:
        """
        Find the column containing line item labels

        Heuristic: Column with most text and financial keywords
        """
        max_score = 0
        best_col = None

        financial_keywords = [
            'assets', 'liabilities', 'equity', 'aktywa', 'zobowiązania',
            'kapitał', 'cash', 'środki', 'inventory', 'zapasy'
        ]

        for col in df.columns:
            # Convert to string and join all values
            text = ' '.join(df[col].astype(str)).lower()

            # Count financial keywords
            score = sum(1 for kw in financial_keywords if kw in text)

            if score > max_score:
                max_score = score
                best_col = col

        return best_col

    def _extract_values(self, df: pd.DataFrame, label_col: str, value_col: str, language: str) -> Dict[str, float]:
        """
        Extract financial values by matching labels
        """
        data = {}

        # Define search patterns
        if language == 'polish':
            search_terms = {
                'total_assets': ['aktywa razem', 'suma aktywów'],
                'total_equity': ['kapitał własny razem', 'kapitał własny ogółem'],
                'total_liabilities': ['zobowiązania razem', 'zobowiązania ogółem'],
                'current_assets': ['aktywa obrotowe razem'],
                'current_liabilities': ['zobowiązania krótkoterminowe razem'],
                'fixed_assets': ['aktywa trwałe razem'],
                'cash': ['środki pieniężne', 'gotówka'],
                'inventories': ['zapasy'],
            }
        else:  # English
            search_terms = {
                'total_assets': ['total assets', 'assets total'],
                'total_equity': ['total equity', 'shareholders equity', 'stockholders equity'],
                'total_liabilities': ['total liabilities', 'liabilities total'],
                'current_assets': ['total current assets', 'current assets total'],
                'current_liabilities': ['total current liabilities', 'current liabilities total'],
                'fixed_assets': ['total fixed assets', 'property plant equipment', 'ppe'],
                'cash': ['cash and cash equivalents', 'cash'],
                'inventories': ['inventories', 'inventory'],
            }

        # Search each row
        for idx, row in df.iterrows():
            try:
                label = str(row[label_col]).lower()

                # Try to match each field
                for field, terms in search_terms.items():
                    if any(term in label for term in terms):
                        value = self._parse_value(row[value_col], language)
                        if value is not None and value != 0:
                            data[field] = value
                            logger.debug(f"      Found {field}: {value:,.0f}")
                            break
            except Exception as e:
                continue

        return data

    def _parse_value(self, value, language: str) -> Optional[float]:
        """Parse numeric value from cell"""
        # If already numeric
        if isinstance(value, (int, float)):
            return float(value)

        # If string, parse it
        if isinstance(value, str):
            return MultiLanguagePatterns.parse_number(value, language)

        return None

    def get_fallback_strategies(self) -> List[str]:
        """Return list of fallback strategies"""
        return ['structured']  # Only one strategy for spreadsheets

    def extract_with_strategy(self, file_path: Path, strategy: str) -> ExtractionResult:
        """Extract using specific strategy (just calls main extract)"""
        return self.extract(file_path)


__all__ = ['SpreadsheetExtractionStrategy']
