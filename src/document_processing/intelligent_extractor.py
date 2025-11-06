"""
Intelligent Multi-Source Financial Data Extraction System

Auto-detects extraction problems and implements appropriate strategies.
Supports: PDF, DOCX, TXT, XLSX, CSV, HTML

Author: Destiny Team
Date: 2025-11-06
"""

import logging
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import time

logger = logging.getLogger(__name__)


class ExtractionMethod(Enum):
    """Extraction methods available"""
    PDFPLUMBER_TABLES = "pdfplumber_tables"
    CAMELOT_STREAM = "camelot_stream"
    CAMELOT_LATTICE = "camelot_lattice"
    PDF_TEXT = "pdf_text_extraction"
    PDF_OCR = "pdf_ocr"
    DOCX_TABLES = "docx_tables"
    DOCX_TEXT = "docx_text"
    TXT_TABULAR = "txt_tabular"
    TXT_INDENTED = "txt_indented"
    TXT_FREEFORM = "txt_freeform"
    XLSX_STRUCTURED = "xlsx_structured"
    CSV_STRUCTURED = "csv_structured"
    HTML_TABLES = "html_tables"
    HTML_TEXT = "html_text"
    FUSION = "fusion_strategy"


@dataclass
class QualityMetrics:
    """
    Multi-dimensional quality assessment for extraction
    """
    # Completeness: % of required fields found
    completeness_score: float = 0.0  # 0.0 - 1.0
    required_fields_found: int = 0
    required_fields_total: int = 8

    # Validation: Does data make sense?
    validation_score: float = 0.0  # 0.0 - 1.0
    accounting_equation_valid: bool = False
    balance_diff: float = 0.0
    balance_diff_percent: float = 0.0

    # Confidence: How confident are we?
    confidence_score: float = 0.0  # 0.0 - 1.0
    semantic_match_score: float = 0.0
    numeric_density: float = 0.0

    # Overall Quality Score (weighted average)
    overall_score: float = 0.0  # 0.0 - 1.0

    # Metadata
    extraction_method: str = "unknown"
    fallback_attempts: int = 0
    processing_time: float = 0.0
    warnings: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        return (
            f"Quality: {self.overall_score:.1%} "
            f"(completeness: {self.completeness_score:.1%}, "
            f"validation: {self.validation_score:.1%}, "
            f"confidence: {self.confidence_score:.1%})"
        )


@dataclass
class ExtractionResult:
    """
    Result of financial data extraction
    """
    success: bool
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    quality_metrics: Optional[QualityMetrics] = None
    error: Optional[str] = None
    warnings: List[str] = field(default_factory=list)

    def get_value(self, field: str, default: Any = None) -> Any:
        """Safely get a value from extracted data"""
        return self.data.get(field, default)


class QualityThresholds:
    """
    Define when extraction is "good enough"
    """
    # Minimum scores to accept extraction
    MIN_OVERALL_SCORE = 0.70  # 70% overall quality
    MIN_COMPLETENESS = 0.60   # 60% of required fields (5/8)
    MIN_VALIDATION = 0.80     # Accounting equation within 5%
    MIN_CONFIDENCE = 0.60     # 60% confidence

    # Thresholds for warnings
    WARN_OVERALL_SCORE = 0.85
    WARN_COMPLETENESS = 0.75

    # Quality score weights
    WEIGHT_COMPLETENESS = 0.35
    WEIGHT_VALIDATION = 0.35
    WEIGHT_CONFIDENCE = 0.30

    @classmethod
    def should_accept(cls, metrics: QualityMetrics) -> bool:
        """Should we accept this extraction result?"""
        return (
            metrics.overall_score >= cls.MIN_OVERALL_SCORE and
            metrics.completeness_score >= cls.MIN_COMPLETENESS and
            metrics.validation_score >= cls.MIN_VALIDATION and
            metrics.confidence_score >= cls.MIN_CONFIDENCE
        )

    @classmethod
    def should_warn(cls, metrics: QualityMetrics) -> bool:
        """Should we warn user about quality?"""
        return (
            metrics.overall_score < cls.WARN_OVERALL_SCORE or
            metrics.completeness_score < cls.WARN_COMPLETENESS
        )


class QualityAssessor:
    """
    Assess extraction quality with multiple metrics
    """

    REQUIRED_FIELDS = [
        'total_assets',
        'total_equity',
        'total_liabilities',
        'current_assets',
        'current_liabilities',
        'fixed_assets',
        'cash',
        'inventories',
    ]

    def assess(self, result: ExtractionResult) -> QualityMetrics:
        """
        Comprehensive quality assessment
        """
        start_time = time.time()

        # 1. Completeness
        completeness, fields_found = self._assess_completeness(result)

        # 2. Validation
        validation, eq_valid, balance_diff, balance_pct = self._assess_validation(result)

        # 3. Confidence
        confidence = self._assess_confidence(result)

        # 4. Overall score (weighted average)
        overall = (
            completeness * QualityThresholds.WEIGHT_COMPLETENESS +
            validation * QualityThresholds.WEIGHT_VALIDATION +
            confidence * QualityThresholds.WEIGHT_CONFIDENCE
        )

        # 5. Collect warnings
        warnings = []
        if completeness < 0.75:
            warnings.append(f"Low completeness: {completeness:.1%} (expected 75%+)")
        if not eq_valid:
            warnings.append(f"Accounting equation doesn't balance: {balance_pct:.2f}% difference")
        if confidence < 0.70:
            warnings.append(f"Low confidence: {confidence:.1%} (expected 70%+)")

        metrics = QualityMetrics(
            completeness_score=completeness,
            required_fields_found=fields_found,
            required_fields_total=len(self.REQUIRED_FIELDS),
            validation_score=validation,
            accounting_equation_valid=eq_valid,
            balance_diff=balance_diff,
            balance_diff_percent=balance_pct,
            confidence_score=confidence,
            overall_score=overall,
            extraction_method=result.metadata.get('extraction_method', 'unknown'),
            fallback_attempts=result.metadata.get('fallback_attempts', 0),
            processing_time=time.time() - start_time,
            warnings=warnings,
        )

        return metrics

    def _assess_completeness(self, result: ExtractionResult) -> Tuple[float, int]:
        """Score: % of required fields successfully extracted"""
        found = 0
        for field in self.REQUIRED_FIELDS:
            value = result.data.get(field)
            if value is not None and value != 0:
                found += 1

        completeness = found / len(self.REQUIRED_FIELDS)
        return completeness, found

    def _assess_validation(self, result: ExtractionResult) -> Tuple[float, bool, float, float]:
        """
        Score: Does accounting equation hold?
        Assets = Equity + Liabilities (within 1% tolerance)
        """
        try:
            assets = float(result.data.get('total_assets', 0))
            equity = float(result.data.get('total_equity', 0))
            liabilities = float(result.data.get('total_liabilities', 0))

            if assets == 0:
                return 0.0, False, 0.0, 0.0

            balance = equity + liabilities
            diff = abs(assets - balance)
            diff_pct = (diff / assets) * 100 if assets > 0 else 100.0
            tolerance = assets * 0.01  # 1%

            if diff < tolerance:
                return 1.0, True, diff, diff_pct
            elif diff < tolerance * 5:  # 5%
                return 0.5, False, diff, diff_pct
            else:
                return 0.0, False, diff, diff_pct
        except (ValueError, TypeError):
            return 0.0, False, 0.0, 0.0

    def _assess_confidence(self, result: ExtractionResult) -> float:
        """
        Score: How confident are we?
        - Semantic match score (E5 embeddings)
        - Numeric density (are numbers present?)
        """
        semantic_score = result.metadata.get('semantic_match_score', 0.5)
        numeric_density = result.metadata.get('numeric_density', 0.5)

        # Weight semantic matching more heavily
        return semantic_score * 0.7 + numeric_density * 0.3


class LanguageDetector:
    """
    Detect document language for pattern selection
    """

    LANGUAGE_KEYWORDS = {
        'polish': [
            'aktywa', 'pasywa', 'zobowiązania', 'kapitał własny',
            'środki pieniężne', 'należności', 'zapasy', 'razem'
        ],
        'english': [
            'assets', 'liabilities', 'equity', 'cash',
            'receivables', 'inventory', 'payables', 'total'
        ],
        'german': [
            'aktiva', 'passiva', 'eigenkapital', 'verbindlichkeiten',
            'zahlungsmittel', 'forderungen', 'vorräte'
        ],
    }

    def detect(self, text: str) -> str:
        """
        Detect primary language from text
        """
        text_lower = text.lower()

        scores = {}
        for lang, keywords in self.LANGUAGE_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            scores[lang] = score

        if not scores or max(scores.values()) == 0:
            return 'english'  # Default

        return max(scores, key=scores.get)


class MultiLanguagePatterns:
    """
    Regex patterns for different languages
    """

    PATTERNS = {
        'polish': {
            'total_assets': [
                r'AKTYWA\s+RAZEM\s*\n\s*\n\s*(\d[\d\s]+)',
                r'Suma\s+aktywów\s*\n\s*(\d[\d\s]+)',
            ],
            'total_equity': [
                r'Kapitał\s+własny\s+razem\s*\n\s*(\d[\d\s]+)',
                r'KAPITAŁ\s+WŁASNY\s+RAZEM\s*\n\s*\n\s*(\d[\d\s]+)',
            ],
            'total_liabilities': [
                r'Zobowiązania\s+razem\s*\n\s*(\d[\d\s]+)',
                r'ZOBOWIĄZANIA\s+RAZEM\s*\n\s*\n\s*(\d[\d\s]+)',
            ],
            'current_assets': [
                r'Aktywa\s+obrotowe\s+razem\s*\n\s*(\d[\d\s]+)',
            ],
            'current_liabilities': [
                r'Zobowiązania\s+krótkoterminowe\s+razem\s*\n\s*(\d[\d\s]+)',
            ],
            'fixed_assets': [
                r'Aktywa\s+trwałe\s+razem\s*\n\s*\d+\s*\n\s*(\d[\d\s]+)',
            ],
            'cash': [
                r'Środki\s+pieniężne\s+i\s+ich\s+ekwiwalenty\s*\n\s*\d*\s*\n\s*(\d[\d\s]+)',
            ],
            'inventories': [
                r'Zapasy\s*\n\s*\d*\s*\n\s*(\d[\d\s]+)',
            ],
        },
        'english': {
            'total_assets': [
                r'Total\s+Assets\s*\n\s*(\d[\d\s,]+)',
                r'TOTAL\s+ASSETS\s*\n\s*(\d[\d\s,]+)',
            ],
            'total_equity': [
                r'Total\s+Equity\s*\n\s*(\d[\d\s,]+)',
                r"Total\s+Shareholders'\s+Equity\s*\n\s*(\d[\d\s,]+)",
            ],
            'total_liabilities': [
                r'Total\s+Liabilities\s*\n\s*(\d[\d\s,]+)',
            ],
            'current_assets': [
                r'Total\s+Current\s+Assets\s*\n\s*(\d[\d\s,]+)',
            ],
            'current_liabilities': [
                r'Total\s+Current\s+Liabilities\s*\n\s*(\d[\d\s,]+)',
            ],
            'fixed_assets': [
                r'Total\s+Fixed\s+Assets\s*\n\s*(\d[\d\s,]+)',
                r'Property,?\s+Plant,?\s+and\s+Equipment\s*\n\s*(\d[\d\s,]+)',
            ],
            'cash': [
                r'Cash\s+and\s+Cash\s+Equivalents\s*\n\s*(\d[\d\s,]+)',
            ],
            'inventories': [
                r'Inventories\s*\n\s*(\d[\d\s,]+)',
            ],
        },
    }

    def get_patterns(self, language: str) -> Dict[str, List[str]]:
        """Get regex patterns for language"""
        return self.PATTERNS.get(language, self.PATTERNS['english'])

    @staticmethod
    def parse_number(value_str: str, language: str = 'polish') -> Optional[float]:
        """
        Parse number from string based on language format

        Polish: 23 744 452 (space as thousand separator)
        English: 23,744,452 (comma as thousand separator)
        """
        if not value_str:
            return None

        # Remove all whitespace and common separators
        cleaned = value_str.replace(' ', '').replace('\xa0', '').replace('\n', '').replace('\r', '')

        if language == 'polish':
            # Polish uses comma as decimal separator
            cleaned = cleaned.replace(',', '.')
        else:
            # English uses comma as thousand separator
            cleaned = cleaned.replace(',', '')

        try:
            return float(cleaned)
        except ValueError:
            return None


# Import this at the end to avoid circular imports
__all__ = [
    'ExtractionMethod',
    'QualityMetrics',
    'ExtractionResult',
    'QualityThresholds',
    'QualityAssessor',
    'LanguageDetector',
    'MultiLanguagePatterns',
]
