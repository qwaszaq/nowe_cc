"""
Document Processing Module for Destiny

Handles downloading and parsing of financial documents (PDF, XLSX, DOC, TXT)
for criminal investigation analysis.

Components:
- downloader.py: Download documents from URLs (Grupa Azoty, etc.)
- pdf_parser.py: Extract text, tables, structure from PDFs
- xlsx_parser.py: Parse Excel financial statements
- doc_parser.py: Parse Word documents
- text_extractor.py: Common text extraction utilities
"""

from .downloader import DocumentDownloader
from .text_extractor import extract_financial_numbers, extract_dates

# PDF parser requires PyMuPDF (import separately if needed)
# from .pdf_parser import PDFParser

__all__ = [
    'DocumentDownloader',
    'extract_financial_numbers',
    'extract_dates'
]
