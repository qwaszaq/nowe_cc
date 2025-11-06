"""
TXT (Plain Text) Financial Document Handler

Extracts financial statements from plain text files using sophisticated
text parsing and pattern matching.

Author: Destiny Team
Date: 2025-11-06
"""

import logging
from pathlib import Path
from typing import List, Dict, Optional
import re

from .intelligent_extractor import (
    ExtractionResult,
    ExtractionMethod,
    LanguageDetector,
    MultiLanguagePatterns,
)

logger = logging.getLogger(__name__)


class TXTExtractionStrategy:
    """
    Extract financial statements from plain text files
    """

    def __init__(self):
        self.language_detector = LanguageDetector()
        self.pattern_provider = MultiLanguagePatterns()

    def extract(self, txt_path: Path) -> ExtractionResult:
        """
        Main extraction entry point

        1. Detect layout type (tabular, indented, freeform)
        2. Apply appropriate extraction strategy
        """
        try:
            logger.info(f"📄 Extracting from TXT: {txt_path.name}")

            with open(txt_path, 'r', encoding='utf-8') as f:
                text = f.read()

            # Detect language
            language = self.language_detector.detect(text)
            logger.info(f"   Detected language: {language}")

            # Detect layout type
            if self._is_tabular_layout(text):
                logger.info(f"   Layout: Tabular")
                result = self._extract_tabular(text, language)
                if result.success:
                    result.metadata['extraction_method'] = ExtractionMethod.TXT_TABULAR.value
                    return result

            if self._is_indented_layout(text):
                logger.info(f"   Layout: Indented")
                result = self._extract_indented(text, language)
                if result.success:
                    result.metadata['extraction_method'] = ExtractionMethod.TXT_INDENTED.value
                    return result

            # Fallback: freeform text
            logger.info(f"   Layout: Freeform")
            result = self._extract_freeform(text, language)
            if result.success:
                result.metadata['extraction_method'] = ExtractionMethod.TXT_FREEFORM.value
                return result

            return ExtractionResult(
                success=False,
                error="Could not extract balance sheet from TXT"
            )

        except Exception as e:
            logger.error(f"   ❌ TXT extraction failed: {e}")
            return ExtractionResult(
                success=False,
                error=f"TXT extraction error: {str(e)}"
            )

    def _is_tabular_layout(self, text: str) -> bool:
        """
        Detect if text uses tabs/spaces for column alignment

        Indicators:
        - Multiple consecutive spaces (≥ 3)
        - Tab characters
        - Consistent column positions
        """
        lines = text.split('\n')

        # Check for tabs
        tab_lines = sum(1 for line in lines if '\t' in line)
        if tab_lines > len(lines) * 0.1:  # 10%+ lines have tabs
            return True

        # Check for multiple consecutive spaces (column alignment)
        multi_space_lines = sum(1 for line in lines if '   ' in line)  # 3+ spaces
        if multi_space_lines > len(lines) * 0.2:  # 20%+ lines have multi-spaces
            return True

        return False

    def _is_indented_layout(self, text: str) -> bool:
        """
        Detect if text uses indentation to show hierarchy

        Indicators:
        - Lines starting with spaces
        - Hierarchical structure (parent-child relationships)
        """
        lines = text.split('\n')

        # Check for indented lines
        indented_lines = sum(1 for line in lines if line.startswith('  ') and line.strip())
        if indented_lines > len(lines) * 0.3:  # 30%+ lines are indented
            return True

        return False

    def _extract_tabular(self, text: str, language: str) -> ExtractionResult:
        """
        Extract from tab/space-aligned text

        Format example:
        ASSETS                           Current Year    Prior Year
        Current Assets                   6,272,971       7,031,404
        Total Assets                     23,744,452      24,296,520
        """
        data = {}
        patterns = self.pattern_provider.get_patterns(language)

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
            return ExtractionResult(success=False, error="No financial data found in tabular text")

        return ExtractionResult(
            success=True,
            data=data,
            metadata={'language': language}
        )

    def _extract_indented(self, text: str, language: str) -> ExtractionResult:
        """
        Extract from indented hierarchical text

        Format example:
          ASSETS
            Current Assets
              Cash                        847,447
              Inventories               2,067,660
            Total Current Assets        6,272,971
          TOTAL ASSETS                 23,744,452
        """
        data = {}
        patterns = self.pattern_provider.get_patterns(language)

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
            return ExtractionResult(success=False, error="No financial data found in indented text")

        return ExtractionResult(
            success=True,
            data=data,
            metadata={'language': language}
        )

    def _extract_freeform(self, text: str, language: str) -> ExtractionResult:
        """
        Extract from freeform text (least structured)

        Uses aggressive pattern matching to find financial values
        """
        data = {}
        patterns = self.pattern_provider.get_patterns(language)

        for field, pattern_list in patterns.items():
            for pattern in pattern_list:
                # Try with different regex flags
                for flags in [re.IGNORECASE | re.MULTILINE, re.IGNORECASE | re.DOTALL]:
                    match = re.search(pattern, text, flags)
                    if match:
                        value_str = match.group(1)
                        value = MultiLanguagePatterns.parse_number(value_str, language)
                        if value is not None:
                            data[field] = value
                            logger.debug(f"      Found {field}: {value:,.0f}")
                            break
                if field in data:
                    break

        if not data:
            return ExtractionResult(success=False, error="No financial data found in freeform text")

        return ExtractionResult(
            success=True,
            data=data,
            metadata={'language': language}
        )

    def get_fallback_strategies(self) -> List[str]:
        """Return list of fallback strategies"""
        return ['tabular', 'indented', 'freeform']

    def extract_with_strategy(self, txt_path: Path, strategy: str) -> ExtractionResult:
        """Extract using specific strategy"""
        with open(txt_path, 'r', encoding='utf-8') as f:
            text = f.read()

        language = self.language_detector.detect(text)

        if strategy == 'tabular':
            return self._extract_tabular(text, language)
        elif strategy == 'indented':
            return self._extract_indented(text, language)
        elif strategy == 'freeform':
            return self._extract_freeform(text, language)
        else:
            return ExtractionResult(success=False, error=f"Unknown strategy: {strategy}")


__all__ = ['TXTExtractionStrategy']
