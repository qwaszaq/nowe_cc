"""
Real Document Parsers - Fast & Cheap but Fully Functional
Supports: PDF, Excel, Word, txt, JSON, XML, CSV
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import json
import csv


class ParseResult:
    """Result from document parsing"""
    def __init__(self, 
                 text: str = "",
                 tables: List[Dict] = None,
                 metadata: Dict = None,
                 success: bool = True,
                 error: str = None):
        self.text = text
        self.tables = tables or []
        self.metadata = metadata or {}
        self.success = success
        self.error = error
    
    def __repr__(self):
        return f"ParseResult(text_len={len(self.text)}, tables={len(self.tables)}, success={self.success})"


class TextParser:
    """Simple text file parser"""
    
    def parse(self, file_path: str) -> ParseResult:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            return ParseResult(
                text=content,
                metadata={
                    'lines': len(content.split('\n')),
                    'chars': len(content),
                    'encoding': 'utf-8'
                }
            )
        except Exception as e:
            return ParseResult(success=False, error=str(e))


class PDFParser:
    """PDF parser using PyPDF2"""
    
    def parse(self, file_path: str) -> ParseResult:
        try:
            # Try PyPDF2
            try:
                import PyPDF2
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    
                    metadata = {
                        'pages': len(reader.pages),
                        'parser': 'PyPDF2'
                    }
                    
                    if reader.metadata:
                        metadata.update({
                            'title': reader.metadata.get('/Title', ''),
                            'author': reader.metadata.get('/Author', ''),
                            'creator': reader.metadata.get('/Creator', '')
                        })
                    
                    return ParseResult(text=text, metadata=metadata)
            
            except ImportError:
                # Fallback: pdfplumber
                try:
                    import pdfplumber
                    with pdfplumber.open(file_path) as pdf:
                        text = ""
                        tables = []
                        
                        for page in pdf.pages:
                            text += page.extract_text() + "\n"
                            
                            # Extract tables
                            page_tables = page.extract_tables()
                            if page_tables:
                                tables.extend(page_tables)
                        
                        return ParseResult(
                            text=text,
                            tables=[{'data': t} for t in tables],
                            metadata={
                                'pages': len(pdf.pages),
                                'parser': 'pdfplumber'
                            }
                        )
                
                except ImportError:
                    # Last resort: basic text extraction
                    return ParseResult(
                        text=f"[PDF file: {Path(file_path).name}]\n[Install PyPDF2 or pdfplumber for full extraction]",
                        metadata={'parser': 'basic'},
                        success=False,
                        error="No PDF library available"
                    )
        
        except Exception as e:
            return ParseResult(success=False, error=str(e))


class ExcelParser:
    """Excel parser using pandas"""
    
    def parse(self, file_path: str) -> ParseResult:
        try:
            import pandas as pd
            
            # Read all sheets
            excel_file = pd.ExcelFile(file_path)
            
            text = f"Excel file with {len(excel_file.sheet_names)} sheets\n\n"
            tables = []
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                # Add sheet info to text
                text += f"Sheet: {sheet_name}\n"
                text += f"Rows: {len(df)}, Columns: {len(df.columns)}\n"
                text += f"Columns: {', '.join(df.columns)}\n\n"
                
                # Add preview
                text += df.head(5).to_string() + "\n\n"
                
                # Store table data
                tables.append({
                    'sheet': sheet_name,
                    'data': df.to_dict('records'),
                    'columns': list(df.columns),
                    'rows': len(df)
                })
            
            return ParseResult(
                text=text,
                tables=tables,
                metadata={
                    'sheets': len(excel_file.sheet_names),
                    'sheet_names': excel_file.sheet_names,
                    'parser': 'pandas'
                }
            )
        
        except ImportError:
            return ParseResult(
                text=f"[Excel file: {Path(file_path).name}]\n[Install pandas and openpyxl for extraction]",
                success=False,
                error="pandas not available"
            )
        except Exception as e:
            return ParseResult(success=False, error=str(e))


class WordParser:
    """Word document parser"""
    
    def parse(self, file_path: str) -> ParseResult:
        try:
            import docx
            
            doc = docx.Document(file_path)
            
            # Extract text from paragraphs
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            
            # Extract tables
            tables = []
            for table in doc.tables:
                table_data = []
                for row in table.rows:
                    row_data = [cell.text for cell in row.cells]
                    table_data.append(row_data)
                tables.append({'data': table_data})
            
            return ParseResult(
                text=text,
                tables=tables,
                metadata={
                    'paragraphs': len(doc.paragraphs),
                    'tables': len(doc.tables),
                    'parser': 'python-docx'
                }
            )
        
        except ImportError:
            return ParseResult(
                text=f"[Word file: {Path(file_path).name}]\n[Install python-docx for extraction]",
                success=False,
                error="python-docx not available"
            )
        except Exception as e:
            return ParseResult(success=False, error=str(e))


class CSVParser:
    """CSV parser"""
    
    def parse(self, file_path: str) -> ParseResult:
        try:
            import pandas as pd
            
            df = pd.read_csv(file_path)
            
            text = f"CSV file with {len(df)} rows and {len(df.columns)} columns\n\n"
            text += f"Columns: {', '.join(df.columns)}\n\n"
            text += df.head(10).to_string() + "\n"
            
            return ParseResult(
                text=text,
                tables=[{
                    'data': df.to_dict('records'),
                    'columns': list(df.columns),
                    'rows': len(df)
                }],
                metadata={
                    'rows': len(df),
                    'columns': len(df.columns),
                    'parser': 'pandas'
                }
            )
        
        except ImportError:
            # Fallback to standard csv
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
                    
                    text = f"CSV file with {len(rows)} rows\n\n"
                    for row in rows[:10]:
                        text += str(row) + "\n"
                    
                    return ParseResult(
                        text=text,
                        tables=[{'data': rows}],
                        metadata={'rows': len(rows), 'parser': 'csv'}
                    )
            except Exception as e:
                return ParseResult(success=False, error=str(e))
        
        except Exception as e:
            return ParseResult(success=False, error=str(e))


class JSONParser:
    """JSON parser"""
    
    def parse(self, file_path: str) -> ParseResult:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Pretty print JSON
            text = json.dumps(data, indent=2, ensure_ascii=False)
            
            return ParseResult(
                text=text,
                metadata={
                    'type': type(data).__name__,
                    'keys': list(data.keys()) if isinstance(data, dict) else None,
                    'items': len(data) if isinstance(data, (list, dict)) else None,
                    'parser': 'json'
                }
            )
        
        except Exception as e:
            return ParseResult(success=False, error=str(e))


class XMLParser:
    """XML parser"""
    
    def parse(self, file_path: str) -> ParseResult:
        try:
            import xml.etree.ElementTree as ET
            
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Convert XML to text representation
            text = self._xml_to_text(root)
            
            return ParseResult(
                text=text,
                metadata={
                    'root_tag': root.tag,
                    'children': len(list(root)),
                    'parser': 'ElementTree'
                }
            )
        
        except Exception as e:
            return ParseResult(success=False, error=str(e))
    
    def _xml_to_text(self, element, level=0) -> str:
        """Convert XML element to readable text"""
        indent = "  " * level
        text = f"{indent}<{element.tag}>"
        
        if element.text and element.text.strip():
            text += f" {element.text.strip()}"
        
        text += "\n"
        
        for child in element:
            text += self._xml_to_text(child, level + 1)
        
        return text


class UniversalDocumentParser:
    """
    Universal parser that automatically selects the right parser
    Fast & cheap but fully functional!
    """
    
    def __init__(self):
        self.parsers = {
            '.txt': TextParser(),
            '.md': TextParser(),
            '.pdf': PDFParser(),
            '.xlsx': ExcelParser(),
            '.xls': ExcelParser(),
            '.docx': WordParser(),
            '.doc': WordParser(),
            '.csv': CSVParser(),
            '.json': JSONParser(),
            '.xml': XMLParser(),
            '.yaml': TextParser(),  # Simple text for YAML
            '.yml': TextParser(),
        }
    
    def parse(self, file_path: str) -> ParseResult:
        """
        Parse any supported document type
        
        Args:
            file_path: Path to file
            
        Returns:
            ParseResult with extracted content
        """
        path = Path(file_path)
        ext = path.suffix.lower()
        
        # Get appropriate parser
        parser = self.parsers.get(ext)
        
        if not parser:
            return ParseResult(
                text=f"[Unsupported file type: {ext}]",
                success=False,
                error=f"No parser for {ext}"
            )
        
        # Parse
        try:
            result = parser.parse(file_path)
            result.metadata['file_name'] = path.name
            result.metadata['file_size'] = path.stat().st_size
            result.metadata['extension'] = ext
            return result
        
        except Exception as e:
            return ParseResult(
                success=False,
                error=f"Parse failed: {str(e)}"
            )
    
    def get_preview(self, file_path: str, max_chars: int = 500) -> str:
        """Get quick preview of file content"""
        result = self.parse(file_path)
        
        if result.success:
            preview = result.text[:max_chars]
            if len(result.text) > max_chars:
                preview += "..."
            return preview
        else:
            return f"[Error: {result.error}]"


# Quick test
if __name__ == "__main__":
    parser = UniversalDocumentParser()
    
    print("Universal Document Parser - Test")
    print("=" * 60)
    
    # Test with a text file (always available)
    import tempfile
    import os
    
    # Create test files
    test_dir = tempfile.mkdtemp()
    
    # Test txt
    txt_file = os.path.join(test_dir, "test.txt")
    with open(txt_file, 'w') as f:
        f.write("This is a test document.\nWith multiple lines.\nAnd some content.")
    
    result = parser.parse(txt_file)
    print(f"\nTXT: {result}")
    print(f"Content preview: {result.text[:100]}")
    
    # Test JSON
    json_file = os.path.join(test_dir, "test.json")
    with open(json_file, 'w') as f:
        json.dump({"name": "Test", "value": 123, "items": [1, 2, 3]}, f)
    
    result = parser.parse(json_file)
    print(f"\nJSON: {result}")
    print(f"Metadata: {result.metadata}")
    
    # Cleanup
    import shutil
    shutil.rmtree(test_dir)
    
    print("\n" + "=" * 60)
    print("✅ Parser ready to use!")
