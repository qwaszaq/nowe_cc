"""
Phase 1: Document Structure Analysis
"""

import re
from typing import Dict, List, Any
from collections import defaultdict


class StructureExtractor:
    """Extract and analyze document structure"""
    
    def __init__(self):
        # Common section patterns for CBA reports
        self.section_patterns = [
            r'(?:Rozdział|ROZDZIAŁ|Dział|DZIAŁ)\s+[IVX\d]+[\.\)]?\s+([A-ZĄĆĘŁŃÓŚŹŻ][^\.\n]{10,80})',
            r'^\s*([A-ZĄĆĘŁŃÓŚŹŻ][A-ZĄĆĘŁŃÓŚŹŻ\s]{5,50})\s*$',
            r'[0-9]+\.\s+([A-ZĄĆĘŁŃÓŚŹŻ][^\.\n]{10,80})',
            r'###\s+([A-ZĄĆĘŁŃÓŚŹŻ][^\n]{5,80})',  # Markdown headers
        ]
        
        # Common CBA sections (domain knowledge)
        self.known_sections = [
            'Wprowadzenie',
            'Działalność operacyjna',
            'Sprawy operacyjne',
            'Sprawy kontrolne',
            'Wyniki finansowe',
            'Budżet',
            'Kadra',
            'Funkcjonariusze',
            'Szkolenia',
            'Współpraca międzynarodowa',
            'Podsumowanie',
        ]
    
    def analyze(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze structure of all documents"""
        
        structures = {}
        all_sections = []
        
        for doc in documents:
            year = doc.get('year')
            text = doc.get('text', '')
            filename = doc.get('filename', '')
            
            if not text or len(text) < 100:
                continue
            
            # Extract sections
            sections = self._extract_sections(text)
            
            if year:
                structures[year] = {
                    'filename': filename,
                    'sections': sections,
                    'text_length': len(text),
                    'section_count': len(sections),
                }
                
                all_sections.extend(sections)
            elif filename:
                # Use filename as key if no year
                structures[filename] = {
                    'filename': filename,
                    'sections': sections,
                    'text_length': len(text),
                    'section_count': len(sections),
                }
                all_sections.extend(sections)
        
        # Identify common sections
        common_sections = self._identify_common_sections(all_sections)
        
        # Analyze structure evolution
        evolution = self._analyze_evolution(structures)
        
        return {
            'total_documents': len(structures),
            'structures': structures,
            'common_sections': common_sections,
            'evolution': evolution,
        }
    
    def _extract_sections(self, text: str, max_chars: int = 10000) -> List[str]:
        """Extract section headers from text"""
        sections = []
        text_sample = text[:max_chars]  # First 10k chars usually contain structure
        
        for pattern in self.section_patterns:
            matches = re.findall(pattern, text_sample, re.MULTILINE)
            sections.extend(matches)
        
        # Clean and deduplicate
        sections = [s.strip() for s in sections if len(s.strip()) > 5]
        sections = list(dict.fromkeys(sections))  # Remove duplicates, preserve order
        
        return sections[:20]  # Top 20 sections
    
    def _identify_common_sections(self, all_sections: List[str]) -> List[str]:
        """Identify sections common across documents"""
        section_counts = defaultdict(int)
        
        for section in all_sections:
            normalized = section.lower().strip()
            section_counts[normalized] += 1
        
        # Return most common (appearing in at least 2 documents)
        common = [
            section for section, count in sorted(section_counts.items(), key=lambda x: x[1], reverse=True)
            if count >= 2
        ]
        
        return common[:20]
    
    def _analyze_evolution(self, structures: Dict) -> Dict[str, Any]:
        """Analyze how structure evolved over time"""
        if len(structures) < 2:
            return {}
        
        # Filter only year-based keys
        year_structures = {k: v for k, v in structures.items() if isinstance(k, int)}
        
        if len(year_structures) < 2:
            return {}
        
        years = sorted(year_structures.keys())
        
        # Calculate average sections per period
        mid_point = len(years) // 2
        early_years = years[:mid_point]
        recent_years = years[mid_point:]
        
        early_avg_sections = sum(year_structures[y]['section_count'] for y in early_years) / len(early_years) if early_years else 0
        recent_avg_sections = sum(year_structures[y]['section_count'] for y in recent_years) / len(recent_years) if recent_years else 0
        
        return {
            'early_period': {
                'years': early_years,
                'avg_sections': early_avg_sections,
            },
            'recent_period': {
                'years': recent_years,
                'avg_sections': recent_avg_sections,
            },
            'evolution': 'increasing' if recent_avg_sections > early_avg_sections else 'decreasing',
        }
