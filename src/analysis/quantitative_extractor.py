"""
Phase 2: Quantitative Data Extraction
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False


class DataConfidence(Enum):
    """Confidence levels for extracted data"""
    VERIFIED = "verified"  # ✅ Verified from source
    EXTRACTED = "extracted"  # ✅ Extracted from document
    ESTIMATED = "estimated"  # ⚠️ Estimated by LLM
    MISSING = "missing"  # ❌ Missing data


@dataclass
class ExtractedMetric:
    """Represents a single extracted metric"""
    name: str
    value: Any
    year: Optional[int]
    confidence: DataConfidence
    source: str  # filename, page, table reference
    context: Optional[str] = None  # surrounding text


class QuantitativeExtractor:
    """Extract quantitative data from documents"""
    
    def __init__(self):
        # Sanity check thresholds (max reasonable values)
        self.sanity_limits = {
            'sprawy_operacyjne': 10000,
            'sprawy_zakończone': 10000,
            'sprawy_w_toku': 10000,
            'zatrzymania': 5000,
            'zarzuty': 5000,
            'skazania': 3000,
            'budzet': 500000000,  # 500 mln zł max
            'funkcjonariusze': 5000,
            'szkolenia': 10000,
            'odzyskane_srodki': 1000000000,  # 1 mld zł max
        }
        
        # Domain-specific patterns for CBA reports
        self.patterns = {
            'sprawy_operacyjne': [
                r'spraw[^.]*operacyjn[^.]*[:\s]+(\d{1,4})',
                r'(\d{1,4})\s+spraw[^.]*operacyjn',
                r'wszczęto\s+(\d{1,4})\s+spraw',
                r'liczba\s+spraw\s+operacyjnych[^.]*(\d{1,4})',
            ],
            'sprawy_zakończone': [
                r'zakończon[^.]*[:\s]+(\d{1,4})',
                r'(\d{1,4})\s+zakończon',
                r'zakończono\s+(\d{1,4})\s+spraw',
            ],
            'sprawy_w_toku': [
                r'w\s+toku[^.]*[:\s]+(\d{1,4})',
                r'(\d{1,4})\s+spraw[^.]*w\s+toku',
            ],
            'zatrzymania': [
                r'zatrzyman[^.]*[:\s]+(\d{1,4})',
                r'(\d{1,4})\s+zatrzymań',
                r'zatrzymano\s+(\d{1,4})\s+osób',
            ],
            'zarzuty': [
                r'zarzut[^.]*[:\s]+(\d{1,4})',
                r'(\d{1,4})\s+zarzut',
                r'postawiono\s+(\d{1,4})\s+zarzut',
            ],
            'skazania': [
                r'skazan[^.]*[:\s]+(\d{1,4})',
                r'(\d{1,4})\s+skazań',
                r'skazano\s+(\d{1,4})\s+osób',
            ],
            'budzet': [
                r'budżet[^.]*[:\s]+(\d{1,3}(?:\s?\d{3})*)\s*(?:mln|milion|zł)',
                r'(\d{1,3}(?:\s?\d{3})*)\s*(?:mln|milion)[^.]*budżet',
                r'budżet.*?(\d{1,3}(?:\s?\d{3})*)\s*(?:mln|milion)',
            ],
            'funkcjonariusze': [
                r'funkcjonariusz[^.]*[:\s]+(\d{1,4})',
                r'(\d{1,4})\s+funkcjonariusz',
                r'liczba\s+funkcjonariuszy[^.]*(\d{1,4})',
            ],
            'szkolenia': [
                r'szkoleni[^.]*[:\s]+(\d{1,4})',
                r'(\d{1,4})\s+szkoleń',
                r'przeprowadzono\s+(\d{1,4})\s+szkoleń',
            ],
            'odzyskane_srodki': [
                r'odzyskan[^.]*[:\s]+(\d{1,3}(?:\s?\d{3})*)\s*(?:mln|milion|zł)',
                r'(\d{1,3}(?:\s?\d{3})*)\s*(?:mln|milion)[^.]*odzyskan',
            ],
        }
    
    def extract(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract quantitative metrics from documents
        
        Returns:
            Dict with metrics per year
        """
        metrics_by_year = {}
        extraction_issues = []
        
        for doc in documents:
            year = doc.get('year')
            text = doc.get('text', '')
            filename = doc.get('filename', '')
            filepath = doc.get('filepath') or doc.get('path', '')
            
            if not text or len(text) < 100:
                continue
            
            year_metrics = {}
            
            # Try to extract from PDF tables if available
            table_data = {}
            if filepath and PDFPLUMBER_AVAILABLE:
                table_data = self._extract_from_pdf_tables(filepath)
            
            for metric_name, pattern_list in self.patterns.items():
                extracted_metrics = []
                
                # First try table extraction if available
                if metric_name in table_data:
                    for value in table_data[metric_name]:
                        if self._sanity_check_value(value, metric_name):
                            metric = ExtractedMetric(
                                name=metric_name,
                                value=value,
                                year=year,
                                confidence=DataConfidence.VERIFIED,  # Higher confidence from tables
                                source=f"{filename} (table)",
                            )
                            extracted_metrics.append(metric)
                
                # Then try regex patterns
                for pattern in pattern_list:
                    matches = re.findall(pattern, text, re.IGNORECASE)
                    
                    for match in matches[:5]:  # Take up to 5 matches
                        try:
                            value = self._parse_value(match, metric_name)
                            
                            if value is not None and self._sanity_check_value(value, metric_name):
                                metric = ExtractedMetric(
                                    name=metric_name,
                                    value=value,
                                    year=year,
                                    confidence=DataConfidence.EXTRACTED,
                                    source=f"{filename}",
                                )
                                extracted_metrics.append(metric)
                            elif value is not None:
                                # Value failed sanity check
                                extraction_issues.append({
                                    'year': year,
                                    'metric': metric_name,
                                    'value': value,
                                    'reason': f'Value exceeds sanity limit ({self.sanity_limits.get(metric_name, "N/A")})',
                                    'source': filename,
                                })
                        except:
                            continue
                
                # Choose best value (prioritize table extraction, then most frequent)
                if extracted_metrics:
                    # Prefer VERIFIED (from tables) over EXTRACTED (from regex)
                    verified_metrics = [m for m in extracted_metrics if m.confidence == DataConfidence.VERIFIED]
                    if verified_metrics:
                        values = [m.value for m in verified_metrics]
                        best_value = max(set(values), key=values.count)
                        confidence = DataConfidence.VERIFIED.value
                    else:
                        values = [m.value for m in extracted_metrics]
                        best_value = max(set(values), key=values.count)
                        confidence = DataConfidence.EXTRACTED.value
                    
                    year_metrics[metric_name] = {
                        'value': best_value,
                        'confidence': confidence,
                        'source': filename,
                        'matches_found': len(extracted_metrics),
                    }
            
            if year_metrics:
                if year:
                    metrics_by_year[year] = year_metrics
                else:
                    # Use filename as key if no year
                    metrics_by_year[filename] = year_metrics
        
        return {
            'metrics': metrics_by_year,
            'total_years': len(metrics_by_year),
            'extraction_summary': self._create_summary(metrics_by_year),
            'extraction_issues': extraction_issues,
        }
    
    def _parse_value(self, match: Any, metric_name: str) -> Optional[int]:
        """Parse extracted value to integer"""
        if isinstance(match, tuple):
            match = match[0]
        
        # Clean value
        value_str = str(match).replace(' ', '').replace(',', '').replace('.', '')
        
        try:
            value = int(value_str)
            
            # Handle budget (might be in millions)
            if metric_name == 'budzet' and value < 1000:
                value = value * 1000000
            
            return value
        except:
            return None
    
    def _sanity_check_value(self, value: Any, metric_name: str) -> bool:
        """Check if extracted value is within reasonable limits"""
        if not isinstance(value, (int, float)):
            return False
        
        limit = self.sanity_limits.get(metric_name)
        if limit is None:
            return True  # No limit defined, accept
        
        return value <= limit
    
    def _extract_from_pdf_tables(self, filepath: str) -> Dict[str, List[Any]]:
        """Extract data from PDF tables using pdfplumber"""
        if not PDFPLUMBER_AVAILABLE or not filepath:
            return {}
        
        table_data = {}
        
        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    tables = page.extract_tables()
                    
                    for table in tables:
                        if not table:
                            continue
                        
                        # Look for metric names in table headers
                        for row_idx, row in enumerate(table):
                            if not row:
                                continue
                            
                            # Check first column for metric names
                            first_cell = str(row[0]).lower() if row[0] else ""
                            
                            for metric_name in self.patterns.keys():
                                if any(keyword in first_cell for keyword in metric_name.split('_')):
                                    # Try to extract value from this row
                                    for cell in row[1:]:
                                        if cell:
                                            value = self._parse_value(cell, metric_name)
                                            if value and self._sanity_check_value(value, metric_name):
                                                if metric_name not in table_data:
                                                    table_data[metric_name] = []
                                                table_data[metric_name].append(value)
        except Exception as e:
            # Silently fail - table extraction is optional
            pass
        
        return table_data
    
    def _create_summary(self, metrics_by_year: Dict) -> Dict[str, Any]:
        """Create summary of extracted metrics"""
        summary = {
            'total_metrics_extracted': sum(len(m) for m in metrics_by_year.values()),
            'metrics_per_year': {year: len(metrics) for year, metrics in metrics_by_year.items()},
            'coverage': {
                'years_with_data': len(metrics_by_year),
                'metrics_found': list(set().union(*[m.keys() for m in metrics_by_year.values()])) if metrics_by_year else [],
            },
        }
        
        return summary
