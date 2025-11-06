"""
Document Processing Module for Destiny

Handles downloading and parsing of financial documents (PDF, DOCX, TXT, XLSX, CSV, HTML)
for criminal investigation analysis.

Enhanced with intelligent multi-source extraction system:
- PDF, DOCX, TXT, XLSX, CSV, HTML support
- Automatic fallback strategies
- Quality assessment and validation
- Multi-language support (Polish, English, German)

Components:
- downloader.py: Download documents from URLs (Grupa Azoty, etc.)
- pdf_parser.py: Extract text, tables, structure from PDFs
- text_extractor.py: Common text extraction utilities
- extraction_manager.py: Intelligent multi-source extraction orchestrator
- intelligent_extractor.py: Quality metrics and assessment
- docx_handler.py: Microsoft Word document extraction
- txt_handler.py: Plain text extraction
- spreadsheet_handler.py: Excel/CSV extraction
- html_handler.py: HTML document extraction
"""

from .downloader import DocumentDownloader
from .text_extractor import extract_financial_numbers, extract_dates

# Intelligent extraction system (new)
from .extraction_manager import IntelligentExtractionManager
from .intelligent_extractor import (
    ExtractionResult,
    QualityMetrics,
    QualityThresholds,
    QualityAssessor,
    LanguageDetector,
    MultiLanguagePatterns,
    ExtractionMethod,
)

# Individual handlers
from .docx_handler import DOCXExtractionStrategy
from .txt_handler import TXTExtractionStrategy
from .spreadsheet_handler import SpreadsheetExtractionStrategy
from .html_handler import HTMLExtractionStrategy

__all__ = [
    # Legacy API
    'DocumentDownloader',
    'extract_financial_numbers',
    'extract_dates',

    # Intelligent Extraction System
    'IntelligentExtractionManager',
    'ExtractionResult',
    'QualityMetrics',
    'QualityThresholds',
    'QualityAssessor',
    'LanguageDetector',
    'MultiLanguagePatterns',
    'ExtractionMethod',

    # Individual handlers
    'DOCXExtractionStrategy',
    'TXTExtractionStrategy',
    'SpreadsheetExtractionStrategy',
    'HTMLExtractionStrategy',
]
