"""
PDF Parser for Financial Documents

Extracts text, tables, and structure from PDF annual reports.
Uses multiple parsing libraries for best results:
- PyMuPDF (fitz) for fast text extraction
- pdfplumber for table detection (primary)
- Camelot for complex tables (fallback - better for Polish financial reports)
- pdfminer.six for layout analysis

Author: Destiny Team
Date: 2025-11-06
"""

import fitz  # PyMuPDF
import pdfplumber
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import re
import logging
from dataclasses import dataclass

# Try to import Camelot (fallback for complex tables)
try:
    import camelot
    CAMELOT_AVAILABLE = True
except ImportError:
    CAMELOT_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class PDFSection:
    """Represents a section of the PDF document"""
    title: str
    page_start: int
    page_end: Optional[int]
    level: int  # 1 = main section, 2 = subsection, etc.
    content: str = ""


@dataclass
class PDFTable:
    """Represents an extracted table"""
    page: int
    title: Optional[str]
    headers: List[str]
    rows: List[List[str]]
    bbox: Tuple[float, float, float, float]  # (x0, y0, x1, y1)


@dataclass
class PDFDocument:
    """Complete parsed PDF document"""
    filename: str
    num_pages: int
    metadata: Dict
    sections: List[PDFSection]
    tables: List[PDFTable]
    full_text: str
    financial_statements: Dict[str, PDFTable]  # 'balance_sheet', 'income_statement', 'cash_flow'


class PDFParser:
    """
    Parse PDF documents with focus on financial reports

    Features:
    - Text extraction (preserve layout)
    - Table detection and extraction
    - Section detection (TOC, headers)
    - Financial statement identification
    - Number extraction
    """

    def __init__(self):
        """Initialize PDF parser"""
        self.financial_keywords = {
            'balance_sheet': [
                'bilans', 'balance sheet', 'sytuacja finansowa',
                'statement of financial position', 'aktywa', 'pasywa'
            ],
            'income_statement': [
                'rachunek zysków i strat', 'income statement', 'profit and loss',
                'comprehensive income', 'wynik finansowy', 'przychody', 'koszty'
            ],
            'cash_flow': [
                'przepływy pieniężne', 'cash flow', 'statement of cash flows',
                'środki pieniężne'
            ]
        }

    def parse(self, pdf_path: str) -> PDFDocument:
        """
        Parse complete PDF document

        Args:
            pdf_path: Path to PDF file

        Returns:
            PDFDocument with all extracted information
        """
        pdf_path = Path(pdf_path)

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        logger.info(f"Parsing PDF: {pdf_path.name}")

        # Extract metadata
        metadata = self._extract_metadata(str(pdf_path))
        logger.info(f"  Pages: {metadata.get('num_pages', 'unknown')}")

        # Extract full text
        full_text = self._extract_text_pymupdf(str(pdf_path))
        logger.info(f"  Text length: {len(full_text)} chars")

        # Detect sections
        sections = self._detect_sections(str(pdf_path), full_text)
        logger.info(f"  Sections: {len(sections)}")

        # Extract tables (pdfplumber first, then Camelot fallback for complex tables)
        tables = self._extract_tables_pdfplumber(str(pdf_path))
        logger.info(f"  Tables (pdfplumber): {len(tables)}")

        # If no tables found or tables have poor quality (empty/low numeric density), try Camelot
        has_poor_tables = self._has_mostly_empty_tables(tables)

        if CAMELOT_AVAILABLE and (len(tables) == 0 or has_poor_tables):
            logger.info("  Trying Camelot fallback for complex tables...")

            # Get pages that likely have financial statements
            # Check which pdfplumber tables have poor quality
            poor_pages = set()
            if has_poor_tables:
                for table in tables:
                    # Check this specific table
                    total = len(table.rows) * len(table.headers) if table.headers else 0
                    if total == 0:
                        continue
                    numeric = sum(1 for row in table.rows for cell in row
                                if cell and any(c.isdigit() for c in str(cell)))
                    if numeric / total < 0.05:  # Less than 5% numeric
                        poor_pages.add(table.page + 1)  # Camelot uses 1-based indexing

            # If no specific poor pages, try common financial statement pages
            if not poor_pages:
                poor_pages = set(range(30, 51))  # Pages 30-50

            logger.info(f"  Targeting {len(poor_pages)} pages with Camelot")
            camelot_tables = self._extract_tables_camelot(str(pdf_path), list(poor_pages))

            # Replace pdfplumber tables from poor pages with Camelot results
            if camelot_tables:
                logger.info(f"  Camelot found {len(camelot_tables)} tables")
                # Remove pdfplumber tables from pages we're replacing
                tables = [t for t in tables if (t.page + 1) not in poor_pages]
                # Add Camelot tables
                tables.extend(camelot_tables)
                logger.info(f"  Final table count: {len(tables)} (hybrid pdfplumber + Camelot)")
            else:
                logger.info(f"  Camelot found no tables - keeping pdfplumber results")

        # Identify financial statements
        financial_statements = self._identify_financial_statements(tables, sections)
        logger.info(f"  Financial statements: {list(financial_statements.keys())}")

        # FALLBACK: If balance sheet not found or has no key line items, try text extraction
        if 'balance_sheet' not in financial_statements or not self._has_key_balance_sheet_items(financial_statements.get('balance_sheet')):
            logger.info("  Balance sheet not found in tables OR missing key items, trying text extraction...")
            text_bs = self._extract_balance_sheet_from_text(str(pdf_path))
            if text_bs:
                financial_statements['balance_sheet'] = text_bs
                logger.info(f"  ✅ Text extraction SUCCESS: {len(text_bs.rows)} line items")
            else:
                logger.warning("  ⚠️  Text extraction failed - no balance sheet available")

        return PDFDocument(
            filename=pdf_path.name,
            num_pages=metadata.get('num_pages', 0),
            metadata=metadata,
            sections=sections,
            tables=tables,
            full_text=full_text,
            financial_statements=financial_statements
        )

    def _extract_metadata(self, pdf_path: str) -> Dict:
        """Extract PDF metadata using PyMuPDF"""
        try:
            doc = fitz.open(pdf_path)
            metadata = {
                'num_pages': len(doc),
                'title': doc.metadata.get('title', ''),
                'author': doc.metadata.get('author', ''),
                'subject': doc.metadata.get('subject', ''),
                'creator': doc.metadata.get('creator', ''),
                'producer': doc.metadata.get('producer', ''),
                'creation_date': doc.metadata.get('creationDate', ''),
                'modification_date': doc.metadata.get('modDate', '')
            }
            doc.close()
            return metadata
        except Exception as e:
            logger.error(f"Failed to extract metadata: {e}")
            return {'num_pages': 0}

    def _extract_text_pymupdf(self, pdf_path: str) -> str:
        """
        Extract text using PyMuPDF (fast, good quality)

        Preserves layout and handles multi-column text.
        """
        try:
            doc = fitz.open(pdf_path)
            text_parts = []

            for page_num in range(len(doc)):
                page = doc[page_num]

                # Extract text with layout preservation
                text = page.get_text("text")

                # Add page separator
                text_parts.append(f"\n\n--- PAGE {page_num + 1} ---\n\n")
                text_parts.append(text)

            doc.close()

            return "".join(text_parts)

        except Exception as e:
            logger.error(f"Text extraction failed: {e}")
            return ""

    def _detect_sections(self, pdf_path: str, full_text: str) -> List[PDFSection]:
        """
        Detect document sections from text and formatting

        Uses heuristics:
        - All caps text (likely headers)
        - Font size changes (PyMuPDF)
        - Numbering patterns (1., 1.1, etc.)
        - Common section names
        """
        sections = []

        try:
            doc = fitz.open(pdf_path)

            # Common section patterns
            section_patterns = [
                r'^(\d+\.)\s+([A-ZĄĆĘŁŃÓŚŹŻ][A-ZĄĆĘŁŃÓŚŹŻ\s]{3,})$',  # "1. INTRODUCTION"
                r'^([IVX]+\.)\s+([A-ZĄĆĘŁŃÓŚŹŻ][A-ZĄĆĘŁŃÓŚŹŻ\s]{3,})$',  # "I. SECTION"
                r'^([A-ZĄĆĘŁŃÓŚŹŻ][A-ZĄĆĘŁŃÓŚŹŻ\s]{10,})$',  # All caps (min 10 chars)
            ]

            current_section = None

            for page_num in range(len(doc)):
                page = doc[page_num]

                # Get text with formatting
                blocks = page.get_text("dict")["blocks"]

                for block in blocks:
                    if block.get("type") == 0:  # Text block
                        for line in block.get("lines", []):
                            # Extract text from line
                            line_text = ""
                            max_font_size = 0

                            for span in line.get("spans", []):
                                line_text += span.get("text", "")
                                max_font_size = max(max_font_size, span.get("size", 0))

                            line_text = line_text.strip()

                            # Check if it's a section header
                            for pattern in section_patterns:
                                match = re.match(pattern, line_text)
                                if match:
                                    # Close previous section
                                    if current_section:
                                        current_section.page_end = page_num
                                        sections.append(current_section)

                                    # Start new section
                                    title = line_text
                                    level = 1 if max_font_size > 14 else 2

                                    current_section = PDFSection(
                                        title=title,
                                        page_start=page_num + 1,
                                        page_end=None,
                                        level=level
                                    )

                                    break

            # Close last section
            if current_section:
                current_section.page_end = len(doc)
                sections.append(current_section)

            doc.close()

        except Exception as e:
            logger.error(f"Section detection failed: {e}")

        return sections

    def _extract_tables_pdfplumber(self, pdf_path: str) -> List[PDFTable]:
        """
        Extract tables using pdfplumber (best table detection)

        Handles:
        - Tables with borders
        - Tables without borders (whitespace-separated)
        - Multi-page tables
        """
        tables = []

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    # Find tables on this page
                    page_tables = page.extract_tables()

                    for table_data in page_tables:
                        if not table_data or len(table_data) < 2:
                            continue

                        # First row is usually headers
                        headers = [str(cell).strip() if cell else "" for cell in table_data[0]]

                        # Remaining rows are data
                        rows = []
                        for row_data in table_data[1:]:
                            row = [str(cell).strip() if cell else "" for cell in row_data]
                            rows.append(row)

                        # Try to find table title (text above table)
                        title = self._find_table_title(page, page_tables.index(table_data))

                        # Get bounding box
                        bbox = (0, 0, 0, 0)  # pdfplumber doesn't provide easy bbox

                        table = PDFTable(
                            page=page_num + 1,
                            title=title,
                            headers=headers,
                            rows=rows,
                            bbox=bbox
                        )

                        tables.append(table)

        except Exception as e:
            logger.error(f"Table extraction failed: {e}")

        return tables

    def _find_table_title(self, page, table_index: int) -> Optional[str]:
        """
        Try to find title of table (text immediately above)

        This is heuristic - looks for text in proximity to table.
        """
        # TODO: Implement proximity-based title detection
        return None

    def _identify_financial_statements(self, tables: List[PDFTable],
                                      sections: List[PDFSection]) -> Dict[str, PDFTable]:
        """
        Identify which tables are financial statements

        Uses keywords and table structure to identify:
        - Balance sheet (Bilans)
        - Income statement (Rachunek zysków i strat)
        - Cash flow statement (Przepływy pieniężne)

        UPDATED: Now uses scoring to prefer main statements over detailed schedules
        """
        identified = {}

        # Define strong vs weak keywords (strong = main statement, weak = schedules/details)
        strong_keywords = {
            'balance_sheet': ['bilans', 'balance sheet', 'sytuacja finansowa',
                            'statement of financial position'],
            'income_statement': ['rachunek zysków i strat', 'income statement',
                               'profit and loss', 'comprehensive income'],
            'cash_flow': ['przepływy pieniężne', 'cash flow',
                         'statement of cash flows']
        }

        # Key line items that should appear in main statements (not detailed schedules)
        required_line_items = {
            'balance_sheet': ['suma aktywów', 'aktywa razem', 'kapitał własny',
                            'zobowiązania', 'total assets', 'equity'],
            'income_statement': ['przychody', 'koszty', 'wynik', 'zysk', 'strata',
                               'revenue', 'expenses', 'profit', 'loss'],
            'cash_flow': ['przepływy z działalności operacyjnej', 'inwestycyjnej',
                         'operating activities', 'investing activities']
        }

        for statement_type, keywords in self.financial_keywords.items():
            best_table = None
            best_score = 0

            # Score each table
            for table in tables:
                score = 0

                # Check table title
                title_text = (table.title or "").lower()
                headers_text = " ".join(table.headers).lower()

                # Combine all text from first 10 rows to check for line items
                row_text = ""
                for row in table.rows[:10]:
                    row_text += " ".join([str(cell) for cell in row if cell]).lower()

                # SCORING LOGIC:

                # 1. Strong keyword match (main statement name) = +10 points
                if statement_type in strong_keywords:
                    if any(kw in title_text or kw in headers_text
                          for kw in strong_keywords[statement_type]):
                        score += 10
                        logger.debug(f"  Page {table.page}: +10 (strong keyword match)")

                # 2. Weak keyword match (general terms like "aktywa") = +2 points
                if any(kw in title_text or kw in headers_text for kw in keywords):
                    score += 2
                    logger.debug(f"  Page {table.page}: +2 (keyword match)")

                # 3. Required line items present = +5 per item (max +15)
                if statement_type in required_line_items:
                    items_found = sum(1 for item in required_line_items[statement_type]
                                     if item in row_text or item in title_text)
                    if items_found > 0:
                        bonus = min(items_found * 5, 15)
                        score += bonus
                        logger.debug(f"  Page {table.page}: +{bonus} ({items_found} line items found)")

                # 4. Page number preference (earlier = better for main statements) = +(50 - page)/10
                # Page 30 = +2, Page 40 = +1, Page 50 = 0
                page_bonus = max(0, (50 - table.page) / 10)
                score += page_bonus
                logger.debug(f"  Page {table.page}: +{page_bonus:.1f} (page preference)")

                # 5. Table size (main statements typically have 20-50 rows) = +3 if in range
                if 20 <= len(table.rows) <= 50:
                    score += 3
                    logger.debug(f"  Page {table.page}: +3 (good size: {len(table.rows)} rows)")

                # 6. PENALTY: "zestawienie" (schedule/statement of changes) = -5 points
                if 'zestawienie' in title_text and 'zmian' in title_text:
                    score -= 5
                    logger.debug(f"  Page {table.page}: -5 (detailed schedule detected)")

                logger.info(f"  Table page {table.page}: score = {score:.1f}")

                # Track best match
                if score > best_score:
                    best_score = score
                    best_table = table

            # Select table with highest score (minimum score of 5 to avoid false positives)
            if best_table and best_score >= 5:
                identified[statement_type] = best_table
                logger.info(f"  ✅ {statement_type}: Page {best_table.page} (score: {best_score:.1f})")

            # Fallback: check section titles if no good table match
            if statement_type not in identified:
                for section in sections:
                    section_lower = section.title.lower()
                    if any(kw in section_lower for kw in keywords):
                        # Find tables in this section's page range
                        for table in tables:
                            if section.page_start <= table.page <= (section.page_end or section.page_start):
                                identified[statement_type] = table
                                logger.info(f"  ✅ {statement_type}: Page {table.page} (section match)")
                                break
                        break

        return identified

    def extract_financial_numbers(self, text: str) -> List[Dict]:
        """
        Extract financial numbers from text

        Returns list of:
        {
            'value': 1234567.89,
            'currency': 'PLN',
            'context': 'surrounding text',
            'unit': 'thousands' or 'millions'
        }
        """
        numbers = []

        # Pattern for financial numbers
        # Handles: "1 234,56", "1,234.56", "1234567"
        patterns = [
            r'([\d\s]+[\d,\.]+)\s*(tys|mln|thousand|million|PLN|EUR|USD|zł)',
            r'([\d\s]+[\d,\.]+)',
        ]

        for pattern in patterns:
            for match in re.finditer(pattern, text):
                value_str = match.group(1)
                unit = match.group(2) if len(match.groups()) > 1 else None

                # Clean and convert to float
                value_clean = value_str.replace(' ', '').replace(',', '.')

                try:
                    value = float(value_clean)

                    # Extract context (50 chars before and after)
                    start = max(0, match.start() - 50)
                    end = min(len(text), match.end() + 50)
                    context = text[start:end]

                    numbers.append({
                        'value': value,
                        'unit': unit,
                        'context': context,
                        'position': match.start()
                    })

                except ValueError:
                    continue

        return numbers

    def _has_mostly_empty_tables(self, tables: List[PDFTable]) -> bool:
        """
        Check if tables have mostly empty cells or low numeric density
        (signs of poor extraction)

        Returns True if any table has:
        - More than 50% empty cells, OR
        - Less than 5% numeric cells (for financial tables)
        """
        if not tables:
            return False

        for table in tables:
            total_cells = 0
            empty_cells = 0
            numeric_cells = 0

            for row in table.rows:
                for cell in row:
                    total_cells += 1
                    cell_str = str(cell).strip() if cell else ""

                    if not cell_str:
                        empty_cells += 1
                    elif any(char.isdigit() for char in cell_str):
                        numeric_cells += 1

            if total_cells == 0:
                continue

            empty_pct = empty_cells / total_cells
            numeric_pct = numeric_cells / total_cells

            # Poor extraction indicators:
            # 1. More than 50% empty cells
            # 2. Less than 5% numeric cells (financial tables should have numbers!)
            if empty_pct > 0.5 or numeric_pct < 0.05:
                logger.info(f"  Poor extraction detected: {empty_pct*100:.1f}% empty, {numeric_pct*100:.1f}% numeric")
                return True

        return False

    def _extract_tables_camelot(self, pdf_path: str, target_pages: List[int] = None) -> List[PDFTable]:
        """
        Extract tables using Camelot (fallback for complex Polish financial tables)

        Args:
            pdf_path: Path to PDF
            target_pages: Specific pages to parse (1-indexed), or None for intelligent detection

        Camelot is better for:
        - Complex table layouts
        - Tables with merged cells
        - Polish financial reports (like Grupa Azoty)

        Note: Camelot's 'all' pages can fail on some PDFs, so we parse specific pages
        """
        if not CAMELOT_AVAILABLE:
            return []

        tables = []

        try:
            # If no specific pages given, try to detect financial statement pages
            if target_pages is None:
                # Use pages that pdfplumber found tables on (likely to have tables)
                # For now, try common financial statement pages (30-50 for annual reports)
                target_pages = list(range(30, 51))  # Pages 30-50 (1-indexed)

            # Parse each page individually (more robust than 'all')
            for page_num in target_pages:
                try:
                    page_tables = camelot.read_pdf(
                        pdf_path,
                        pages=str(page_num),
                        flavor='stream'
                    )

                    # Process tables from this page
                    for table in page_tables:
                        df = table.df
                        actual_page = table.page - 1  # Camelot uses 1-based indexing

                        if df.empty or df.shape[0] < 2:
                            continue

                        # First row as headers
                        headers = [str(cell).strip() for cell in df.iloc[0]]

                        # Remaining rows as data
                        rows = []
                        for i in range(1, len(df)):
                            row = [str(cell).strip() for cell in df.iloc[i]]
                            rows.append(row)

                        # Try to find table title (from text near table)
                        title = None  # Can be enhanced later

                        tables.append(PDFTable(
                            page=actual_page,
                            title=title,
                            headers=headers,
                            rows=rows,
                            bbox=(0, 0, 0, 0)  # Camelot doesn't provide bbox easily
                        ))

                except Exception as page_error:
                    # Skip problematic pages (some pages cause Camelot errors)
                    logger.debug(f"Camelot failed on page {page_num}: {page_error}")
                    continue

            logger.info(f"Camelot extracted {len(tables)} tables from {len(target_pages)} pages")

        except Exception as e:
            logger.warning(f"Camelot extraction failed: {e}")

        return tables


# Test
    def _has_key_balance_sheet_items(self, table: Optional[PDFTable]) -> bool:
        """
        Check if table has key balance sheet line items (totals)

        Args:
            table: PDFTable to check

        Returns:
            True if table has balance sheet totals (AKTYWA RAZEM, PASYWA RAZEM, etc.)
        """
        if not table:
            return False

        # Combine all row text
        all_text = ""
        for row in table.rows:
            all_text += " ".join([str(cell).lower() for cell in row if cell]) + " "

        # Check for key totals that MUST be in a balance sheet
        required_items = [
            'aktywa razem',  # Total assets
            'kapitał własny razem',  # Total equity
        ]

        found = sum(1 for item in required_items if item in all_text)

        # Need at least 1 of the required items (some schedules have "aktywa" but not "aktywa razem")
        return found >= 1

    def _extract_balance_sheet_from_text(self, pdf_path: str) -> Optional[PDFTable]:
        """
        Extract balance sheet from text-based layout (fallback for non-table formats)

        Used for Polish financial reports that use spacing/tabs instead of table borders.
        Common in pages 5-6 of annual reports.

        Args:
            pdf_path: Path to PDF file

        Returns:
            PDFTable with balance sheet data, or None if not found
        """
        try:
            doc = fitz.open(pdf_path)

            # Try pages 4-7 (0-indexed) which typically contain balance sheets
            target_pages = [4, 5, 6]
            combined_text = ""

            for page_num in target_pages:
                if page_num < len(doc):
                    page = doc[page_num]
                    combined_text += f"\n--- PAGE {page_num + 1} ---\n"
                    combined_text += page.get_text()

            doc.close()

            # Check if this looks like a balance sheet
            if not any(keyword in combined_text.lower() for keyword in
                      ['aktywa razem', 'pasywa razem', 'sytuacji finansowej', 'bilans']):
                logger.info("  Text extraction: No balance sheet markers found")
                return None

            logger.info("  Text extraction: Found balance sheet markers, extracting values...")

            # Regex patterns for balance sheet line items
            # Format: "Line item name    Note    Value1    Value2"
            # Example: "AKTYWA RAZEM     23 744 452    24 296 520"

            # Patterns use format: "Label \n optional_empty_line \n value1 \n value2"
            # Numbers are on SEPARATE LINES after the label
            patterns = {
                # Assets - values on next non-empty lines
                'total_assets': r'AKTYWA\s+RAZEM\s*\n\s*\n\s*(\d[\d\s]+)\s*\n\s*(\d[\d\s]+)',
                'current_assets': r'Aktywa obrotowe razem\s*\n\s*(\d[\d\s]+)\s*\n\s*(\d[\d\s]+)',
                'fixed_assets': r'Aktywa trwałe razem\s*\n\s*\d+\s*\n\s*(\d[\d\s]+)\s*\n\s*(\d[\d\s]+)',
                'tangible_assets': r'Rzeczowe aktywa trwałe\s*\n\s*\d+\s*\n\s*(\d[\d\s]+)\s*\n\s*(\d[\d\s]+)',
                'cash': r'Środki pieniężne i ich ekwiwalenty\s*\n\s*\d*\s*\n\s*(\d[\d\s]+)\s*\n\s*(\d[\d\s]+)',
                'inventories': r'Zapasy\s*\n\s*\d*\s*\n\s*(\d[\d\s]+)\s*\n\s*(\d[\d\s]+)',
                'receivables': r'Należności z tytułu dostaw i usług oraz pozostałe\s*\n\s*\d*\s*\n\s*(\d[\d\s]+)\s*\n\s*(\d[\d\s]+)',

                # Equity & Liabilities
                'total_equity': r'Kapitał własny razem\s*\n\s*(\d[\d\s]+)\s*\n\s*(\d[\d\s]+)',
                'total_liabilities': r'Zobowiązania razem\s*\n\s*(\d[\d\s]+)\s*\n\s*(\d[\d\s]+)',
                'current_liabilities': r'Zobowiązania krótkoterminowe razem\s*\n\s*(\d[\d\s]+)\s*\n\s*(\d[\d\s]+)',
                'long_term_liabilities': r'Zobowiązania długoterminowe razem\s*\n\s*\d*\s*\n\s*(\d[\d\s]+)\s*\n\s*(\d[\d\s]+)',
                'short_term_debt': r'Zobowiązania z tytułu kredytów i pożyczek\s*\n\s*15\s*\n\s*(\d[\d\s]+)\s*\n\s*(\d[\d\s]+)',
                'payables': r'Zobowiązania z tytułu dostaw i usług oraz pozostałe\s*\n\s*\d*\s*\n\s*(\d[\d\s]+)\s*\n\s*(\d[\d\s]+)',
            }

            # Extract values
            extracted_data = {}
            for key, pattern in patterns.items():
                match = re.search(pattern, combined_text)
                if match:
                    # Get both columns (current period and previous period)
                    # Remove all whitespace including newlines
                    value1_str = match.group(1).replace(' ', '').replace('\xa0', '').replace('\n', '').replace('\r', '')
                    value2_str = match.group(2).replace(' ', '').replace('\xa0', '').replace('\n', '').replace('\r', '')

                    try:
                        value1 = float(value1_str)
                        value2 = float(value2_str)
                        extracted_data[key] = (value1, value2)
                        logger.debug(f"    {key}: {value1:,.0f} (current), {value2:,.0f} (previous)")
                    except ValueError:
                        logger.warning(f"    Failed to parse {key}: '{value1_str}', '{value2_str}'")

            if not extracted_data:
                logger.warning("  Text extraction: No values matched")
                return None

            # Build PDFTable structure from extracted data
            # Format: Row per line item, 2 columns (current + previous period)
            headers = ['Line Item', 'Na dzień 30.06.2024 (niebadane)', 'Na dzień 31.12.2023 (badane)']
            rows = []

            # Map keys to display names
            display_names = {
                'total_assets': 'AKTYWA RAZEM',
                'current_assets': 'Aktywa obrotowe razem',
                'fixed_assets': 'Aktywa trwałe razem',
                'tangible_assets': 'Rzeczowe aktywa trwałe',
                'cash': 'Środki pieniężne i ich ekwiwalenty',
                'inventories': 'Zapasy',
                'receivables': 'Należności z tytułu dostaw i usług',
                'total_equity': 'Kapitał własny razem',
                'total_liabilities': 'Zobowiązania razem',
                'current_liabilities': 'Zobowiązania krótkoterminowe razem',
                'long_term_liabilities': 'Zobowiązania długoterminowe razem',
                'short_term_debt': 'Zobowiązania z tytułu kredytów i pożyczek (krótkoterminowe)',
                'payables': 'Zobowiązania z tytułu dostaw i usług',
            }

            for key, (val1, val2) in extracted_data.items():
                label = display_names.get(key, key)
                rows.append([label, f"{val1:,.0f}".replace(',', ' '), f"{val2:,.0f}".replace(',', ' ')])

            logger.info(f"  ✅ Text extraction: Extracted {len(rows)} line items from balance sheet")

            # Create PDFTable
            return PDFTable(
                page=5,  # Balance sheet typically on pages 5-6
                title="Skonsolidowane sprawozdanie z sytuacji finansowej (text extraction)",
                headers=headers,
                rows=rows,
                bbox=(0, 0, 0, 0)  # No bbox for text extraction
            )

        except Exception as e:
            logger.error(f"Text extraction failed: {e}")
            return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    print("Testing PDF Parser...")
    print("=" * 80)

    # Check for sample PDF
    sample_dir = Path("data/documents/grupa_azoty_tarnow")

    if sample_dir.exists():
        pdf_files = list(sample_dir.glob("*.pdf"))

        if pdf_files:
            print(f"\nFound {len(pdf_files)} PDF files:")
            for pdf in pdf_files:
                print(f"  - {pdf.name}")

            # Parse first PDF
            parser = PDFParser()
            print(f"\nParsing: {pdf_files[0].name}")
            print("-" * 80)

            doc = parser.parse(str(pdf_files[0]))

            print(f"\nDocument: {doc.filename}")
            print(f"  Pages: {doc.num_pages}")
            print(f"  Sections: {len(doc.sections)}")
            print(f"  Tables: {len(doc.tables)}")

            if doc.sections:
                print("\nSections (first 5):")
                for section in doc.sections[:5]:
                    print(f"  {section.level}. {section.title} (pages {section.page_start}-{section.page_end})")

            if doc.tables:
                print(f"\nTables: {len(doc.tables)} found")
                for i, table in enumerate(doc.tables[:3], 1):
                    print(f"\n  Table {i} (page {table.page}):")
                    print(f"    Headers: {table.headers[:5]}...")
                    print(f"    Rows: {len(table.rows)}")

            if doc.financial_statements:
                print("\nIdentified Financial Statements:")
                for stmt_type, table in doc.financial_statements.items():
                    print(f"  ✅ {stmt_type}: page {table.page}, {len(table.rows)} rows")

        else:
            print("\n⚠️  No PDF files found in data/documents/grupa_azoty_tarnow/")
            print("   Run downloader.py first to download reports")

    else:
        print("\n⚠️  Directory not found: data/documents/grupa_azoty_tarnow/")
        print("   Run downloader.py first to download reports")
