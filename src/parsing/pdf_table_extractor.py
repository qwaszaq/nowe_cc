"""
PDF Table Extractor - Extract tables and structured data from PDFs
Part of CBA Analysis Improvement Plan
"""
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
import json

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

try:
    import camelot
    HAS_CAMELOT = True
except ImportError:
    HAS_CAMELOT = False

try:
    import tabula
    HAS_TABULA = True
except ImportError:
    HAS_TABULA = False


class PDFTableExtractor:
    """
    Extract tables and structured data from PDF files
    
    Uses multiple methods:
    1. PDFPlumber (best for text-based tables)
    2. Camelot (best for lattice/stream tables)
    3. Tabula (fallback)
    """
    
    def __init__(self):
        self.methods_available = {
            'pdfplumber': HAS_PDFPLUMBER,
            'camelot': HAS_CAMELOT,
            'tabula': HAS_TABULA
        }
        
        if not any(self.methods_available.values()):
            print("⚠️  Warning: No PDF table extraction libraries available!")
            print("   Install: pip install pdfplumber camelot-py tabula-py")
    
    def extract_tables(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Extract all tables from PDF
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of tables with metadata
        """
        tables = []
        pdf_path_obj = Path(pdf_path)
        
        if not pdf_path_obj.exists():
            return tables
        
        # Method 1: PDFPlumber (most reliable for text tables)
        if HAS_PDFPLUMBER:
            try:
                with pdfplumber.open(str(pdf_path_obj)) as pdf:
                    for page_num, page in enumerate(pdf.pages):
                        page_tables = page.extract_tables()
                        for table_idx, table in enumerate(page_tables):
                            if table and len(table) > 0:
                                tables.append({
                                    'method': 'pdfplumber',
                                    'page': page_num + 1,
                                    'table_index': table_idx,
                                    'data': table,
                                    'row_count': len(table),
                                    'col_count': len(table[0]) if table else 0
                                })
            except Exception as e:
                print(f"⚠️  PDFPlumber extraction failed: {e}")
        
        # Method 2: Camelot (for lattice/stream tables)
        if HAS_CAMELOT and len(tables) == 0:
            try:
                camelot_tables = camelot.read_pdf(str(pdf_path_obj), pages='all', flavor='lattice')
                for table in camelot_tables:
                    tables.append({
                        'method': 'camelot',
                        'page': table.page,
                        'data': table.df.to_dict('records'),
                        'accuracy': table.accuracy,
                        'row_count': len(table.df),
                        'col_count': len(table.df.columns)
                    })
            except Exception as e:
                print(f"⚠️  Camelot extraction failed: {e}")
        
        return tables
    
    def extract_numeric_data(self, pdf_path: str, text: Optional[str] = None) -> Dict[str, Any]:
        """
        Extract numeric metrics from PDF
        
        Args:
            pdf_path: Path to PDF file
            text: Optional pre-extracted text (to avoid re-extraction)
            
        Returns:
            Dict with extracted numeric data
        """
        metrics = {
            'sprawy_operacyjne': None,
            'sprawy_kontrolne': None,
            'sprawy_analityczne': None,
            'zatrzymane_osoby': None,
            'budzet': None,
            'pracownicy': None,
            'sources': []
        }
        
        # Extract text if not provided
        if not text:
            if HAS_PDFPLUMBER:
                try:
                    with pdfplumber.open(str(pdf_path)) as pdf:
                        text_parts = []
                        for page in pdf.pages:
                            text_parts.append(page.extract_text() or '')
                        text = '\n\n'.join(text_parts)
                except Exception as e:
                    print(f"⚠️  Text extraction failed: {e}")
                    return metrics
        
        if not text:
            return metrics
        
        # Extract tables for better data extraction
        tables = self.extract_tables(pdf_path)
        
        # Patterns for CBA reports
        patterns = {
            'sprawy_operacyjne': [
                r'spraw.*operacyjn[^.]*\s+(\d{1,4})',
                r'(\d{1,4})\s+spraw.*operacyjn',
                r'liczba\s+spraw.*operacyjn[^.]*\s+(\d{1,4})',
            ],
            'sprawy_kontrolne': [
                r'spraw.*kontroln[^.]*\s+(\d{1,4})',
                r'(\d{1,4})\s+spraw.*kontroln',
                r'postępowan.*kontroln[^.]*\s+(\d{1,4})',
            ],
            'budzet': [
                r'budżet[^.]*\s+(\d{1,3}(?:\s?\d{3})*)\s*(?:mln|milion|zł|PLN)',
                r'(\d{1,3}(?:\s?\d{3})*)\s*(?:mln|milion).*budżet',
            ],
            'pracownicy': [
                r'funkcjonariuszy[^.]*\s+(\d{1,4})',
                r'(\d{1,4})\s+funkcjonariuszy',
                r'pracowników[^.]*\s+(\d{1,4})',
            ]
        }
        
        text_lower = text.lower()
        
        # Extract from text patterns
        for key, pattern_list in patterns.items():
            for pattern in pattern_list:
                matches = re.findall(pattern, text_lower, re.IGNORECASE)
                if matches:
                    try:
                        num_str = str(matches[0]).replace(' ', '').replace(',', '.')
                        
                        if key == 'budzet':
                            # Handle millions
                            if 'mln' in text_lower or 'milion' in text_lower:
                                num = float(num_str) * 1000000
                            else:
                                num = float(num_str)
                        else:
                            num = int(num_str)
                        
                        # Only set if not already set or if this seems more reliable
                        if metrics[key] is None or (isinstance(num, int) and num < 10000):
                            metrics[key] = num
                            metrics['sources'].append({
                                'metric': key,
                                'value': num,
                                'method': 'text_pattern',
                                'pattern': pattern[:50]
                            })
                            break
                    except (ValueError, IndexError):
                        pass
        
        # Extract from tables
        for table in tables:
            table_data = table.get('data', [])
            if table_data:
                # Look for numeric patterns in table cells
                for row_idx, row in enumerate(table_data[:10]):  # First 10 rows
                    if isinstance(row, (list, tuple)):
                        for cell in row:
                            if isinstance(cell, str):
                                # Check if cell contains numbers
                                numbers = re.findall(r'\d{1,4}', cell)
                                if numbers:
                                    # Context-based extraction (simplified)
                                    cell_lower = cell.lower()
                                    if 'operacyjn' in cell_lower and metrics['sprawy_operacyjne'] is None:
                                        try:
                                            metrics['sprawy_operacyjne'] = int(numbers[0])
                                            metrics['sources'].append({
                                                'metric': 'sprawy_operacyjne',
                                                'value': int(numbers[0]),
                                                'method': 'table',
                                                'page': table.get('page', 0),
                                                'row': row_idx
                                            })
                                        except:
                                            pass
        
        return metrics
    
    def get_extraction_summary(self, pdf_path: str) -> Dict[str, Any]:
        """
        Get summary of extraction capabilities
        
        Returns:
            Summary dict
        """
        tables = self.extract_tables(pdf_path)
        metrics = self.extract_numeric_data(pdf_path)
        
        return {
            'file': str(pdf_path),
            'tables_found': len(tables),
            'methods_available': self.methods_available,
            'metrics_extracted': {k: v for k, v in metrics.items() if v is not None and k != 'sources'},
            'sources_count': len(metrics.get('sources', []))
        }


def test_extractor():
    """Test the table extractor"""
    print("🧪 Testing PDF Table Extractor...")
    print("=" * 80)
    
    extractor = PDFTableExtractor()
    
    print("\n📊 Available methods:")
    for method, available in extractor.methods_available.items():
        status = "✅" if available else "❌"
        print(f"   {status} {method}")
    
    # Test on CBA report
    test_pdf = Path("testdocsLLM/Informacja_2021.pdf")
    
    if test_pdf.exists():
        print(f"\n📄 Testing on: {test_pdf.name}")
        
        summary = extractor.get_extraction_summary(str(test_pdf))
        
        print(f"\n✅ Results:")
        print(f"   Tables found: {summary['tables_found']}")
        print(f"   Metrics extracted: {len(summary['metrics_extracted'])}")
        for metric, value in summary['metrics_extracted'].items():
            print(f"   - {metric}: {value}")
        
        if summary['tables_found'] > 0:
            tables = extractor.extract_tables(str(test_pdf))
            print(f"\n📊 First table preview:")
            if tables:
                first_table = tables[0]
                print(f"   Method: {first_table['method']}")
                print(f"   Page: {first_table['page']}")
                print(f"   Size: {first_table['row_count']} rows × {first_table['col_count']} cols")
    else:
        print(f"\n⚠️  Test PDF not found: {test_pdf}")
    
    print("\n✅ Test complete!")


if __name__ == "__main__":
    test_extractor()
