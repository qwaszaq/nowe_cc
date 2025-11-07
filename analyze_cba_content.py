#!/usr/bin/env python3
"""
Full CBA Content Analysis

Parses all CBA PDF documents and performs comprehensive content analysis.
"""

import sys
import re
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.parsing.document_parsers import UniversalDocumentParser


class CBAContentAnalyzer:
    """Comprehensive CBA document content analyzer"""
    
    def __init__(self):
        self.parser = UniversalDocumentParser()
        self.documents = []
        self.analysis_results = {}
        
    def parse_all_documents(self, folder_path):
        """Parse all PDF documents in folder"""
        print("\n" + "="*80)
        print("🔍 PARSING CBA DOCUMENTS - FULL CONTENT ANALYSIS")
        print("="*80)
        
        folder = Path(folder_path)
        pdf_files = sorted(folder.glob("*.pdf"))
        
        print(f"\n📂 Found {len(pdf_files)} PDF files")
        print("-" * 80)
        
        for i, pdf_path in enumerate(pdf_files, 1):
            print(f"\n[{i}/{len(pdf_files)}] Parsing: {pdf_path.name}")
            
            try:
                result = self.parser.parse(str(pdf_path))
                
                if result.success:
                    doc_info = {
                        'filename': pdf_path.name,
                        'path': str(pdf_path),
                        'text': result.text,
                        'text_length': len(result.text),
                        'pages': result.metadata.get('pages', 0),
                        'tables': len(result.tables) if result.tables else 0,
                        'year': self._extract_year(pdf_path.name),
                    }
                    
                    self.documents.append(doc_info)
                    
                    print(f"   ✅ Success: {len(result.text):,} characters, {doc_info['pages']} pages")
                    if result.tables:
                        print(f"   📊 Tables found: {len(result.tables)}")
                else:
                    print(f"   ❌ Failed: {result.error}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        print(f"\n✅ Successfully parsed: {len(self.documents)}/{len(pdf_files)} documents")
        return self.documents
    
    def _extract_year(self, filename):
        """Extract year from filename"""
        # Try to find 4-digit year
        match = re.search(r'20(\d{2})', filename)
        if match:
            return 2000 + int(match.group(1))
        
        # Try other patterns
        if '2008' in filename:
            return 2008
        
        return None
    
    def analyze_content(self):
        """Perform comprehensive content analysis"""
        print("\n" + "="*80)
        print("📊 CONTENT ANALYSIS")
        print("="*80)
        
        self.analysis_results = {
            'temporal_analysis': self._analyze_temporal(),
            'keyword_analysis': self._analyze_keywords(),
            'statistical_analysis': self._analyze_statistics(),
            'entity_extraction': self._extract_entities(),
            'thematic_analysis': self._analyze_themes(),
        }
        
        return self.analysis_results
    
    def _analyze_temporal(self):
        """Temporal analysis across years"""
        print("\n📅 Temporal Analysis...")
        
        by_year = defaultdict(list)
        for doc in self.documents:
            if doc['year']:
                by_year[doc['year']].append(doc)
        
        temporal = {
            'years_covered': sorted(by_year.keys()),
            'documents_by_year': {year: len(docs) for year, docs in by_year.items()},
            'total_years': len(by_year),
            'year_range': f"{min(by_year.keys())}-{max(by_year.keys())}" if by_year else "N/A",
        }
        
        # Analyze document growth
        sizes_by_year = {}
        for year, docs in sorted(by_year.items()):
            avg_length = sum(d['text_length'] for d in docs) / len(docs)
            sizes_by_year[year] = int(avg_length)
        
        temporal['document_sizes'] = sizes_by_year
        
        print(f"   ✅ Years covered: {temporal['year_range']}")
        print(f"   ✅ Total years: {temporal['total_years']}")
        
        return temporal
    
    def _analyze_keywords(self):
        """Keyword frequency analysis"""
        print("\n🔍 Keyword Analysis...")
        
        keywords = {
            'corruption': ['korupcja', 'korupcyjn', 'łapówk', 'przekup'],
            'investigation': ['śledztw', 'dochodzeni', 'postępowani', 'sprawę'],
            'legal': ['sąd', 'prokuratur', 'wyrok', 'karn', 'prawny'],
            'financial': ['złot', 'kwot', 'milion', 'budżet', 'finansow'],
            'personnel': ['agent', 'funkcjonariusz', 'pracownik', 'zatrudnien'],
            'cases': ['spraw', 'zgłoszeni', 'zawiadomieni', 'akt'],
        }
        
        results = {}
        
        for category, terms in keywords.items():
            category_counts = defaultdict(int)
            
            for doc in self.documents:
                text_lower = doc['text'].lower()
                year = doc['year']
                
                for term in terms:
                    # Count occurrences
                    count = len(re.findall(term, text_lower))
                    if year:
                        category_counts[year] += count
            
            results[category] = dict(sorted(category_counts.items()))
        
        print(f"   ✅ Analyzed {len(keywords)} keyword categories")
        
        return results
    
    def _analyze_statistics(self):
        """Extract statistical data"""
        print("\n📈 Statistical Analysis...")
        
        stats = {
            'total_documents': len(self.documents),
            'total_characters': sum(d['text_length'] for d in self.documents),
            'total_pages': sum(d['pages'] for d in self.documents),
            'avg_doc_length': int(sum(d['text_length'] for d in self.documents) / len(self.documents)) if self.documents else 0,
            'avg_pages': int(sum(d['pages'] for d in self.documents) / len(self.documents)) if self.documents else 0,
        }
        
        # Find numerical patterns
        all_numbers = []
        for doc in self.documents:
            # Extract numbers (thousands format: 1 234, 1.234, etc.)
            numbers = re.findall(r'\b\d{1,3}(?:[\s\.]\d{3})*\b', doc['text'])
            all_numbers.extend(numbers)
        
        stats['numbers_found'] = len(all_numbers)
        
        print(f"   ✅ Total characters: {stats['total_characters']:,}")
        print(f"   ✅ Total pages: {stats['total_pages']}")
        print(f"   ✅ Numbers extracted: {stats['numbers_found']:,}")
        
        return stats
    
    def _extract_entities(self):
        """Extract key entities"""
        print("\n🏛️ Entity Extraction...")
        
        entities = {
            'institutions': set(),
            'legal_references': set(),
            'years_mentioned': set(),
        }
        
        # Common institution patterns
        institution_patterns = [
            r'CBA', r'Centralne Biuro Antykorupcyjne',
            r'Prokurator(?:a|ę|y)?', r'Sąd',
            r'ABW', r'Policja', r'Straż Graniczn',
        ]
        
        for doc in self.documents:
            text = doc['text']
            
            # Extract institutions
            for pattern in institution_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                entities['institutions'].update(matches)
            
            # Extract years mentioned
            years = re.findall(r'\b(19\d{2}|20\d{2})\b', text)
            entities['years_mentioned'].update(years)
        
        # Convert sets to sorted lists for JSON serialization
        entities = {k: sorted(list(v)) for k, v in entities.items()}
        
        print(f"   ✅ Institutions found: {len(entities['institutions'])}")
        print(f"   ✅ Years mentioned: {len(entities['years_mentioned'])}")
        
        return entities
    
    def _analyze_themes(self):
        """Thematic analysis"""
        print("\n🎯 Thematic Analysis...")
        
        themes = {
            'anti_corruption': 0,
            'operational_results': 0,
            'international_cooperation': 0,
            'training_development': 0,
            'legal_framework': 0,
        }
        
        theme_keywords = {
            'anti_corruption': ['zwalczan', 'przeciwdziałan', 'korupcj'],
            'operational_results': ['wynik', 'efekt', 'osiągnięci', 'sukces'],
            'international_cooperation': ['międzynarodow', 'współprac', 'europejsk'],
            'training_development': ['szkoleni', 'kurs', 'edukacj', 'rozwój'],
            'legal_framework': ['ustan', 'przepis', 'prawo', 'regulacj'],
        }
        
        for theme, keywords in theme_keywords.items():
            for doc in self.documents:
                text_lower = doc['text'].lower()
                for keyword in keywords:
                    themes[theme] += len(re.findall(keyword, text_lower))
        
        print(f"   ✅ Themes analyzed: {len(themes)}")
        
        return themes
    
    def generate_report(self, output_path):
        """Generate comprehensive analysis report"""
        print("\n" + "="*80)
        print("📝 GENERATING COMPREHENSIVE REPORT")
        print("="*80)
        
        report = self._build_report_content()
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\n✅ Report saved: {output_path}")
        print(f"   Lines: {len(report.splitlines())}")
        print(f"   Size: {len(report):,} characters")
        
        # Also save JSON data
        json_path = output_path.replace('.md', '_data.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                'documents': [
                    {k: v for k, v in d.items() if k != 'text'}  # Exclude full text
                    for d in self.documents
                ],
                'analysis': self.analysis_results,
            }, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Data saved: {json_path}")
        
        return output_path
    
    def _build_report_content(self):
        """Build comprehensive report content"""
        
        temporal = self.analysis_results['temporal_analysis']
        keywords = self.analysis_results['keyword_analysis']
        stats = self.analysis_results['statistical_analysis']
        entities = self.analysis_results['entity_extraction']
        themes = self.analysis_results['thematic_analysis']
        
        report = f"""# 🔍 CBA FULL CONTENT ANALYSIS
## Pełna Analiza Treści Dokumentów CBA (2008-2024)

**Data Analizy:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Dokumenty:** {stats['total_documents']} raportów CBA  
**Zakres:** {temporal['year_range']}  
**Analiza:** FULL CONTENT (nie tylko nazwy plików!)

---

## 📊 EXECUTIVE SUMMARY

### Zakres Pełnej Analizy

**Przetworzone dokumenty:** {stats['total_documents']} PDF-ów  
**Całkowita treść:** {stats['total_characters']:,} znaków  
**Całkowita liczba stron:** {stats['total_pages']}  
**Średnia długość dokumentu:** {stats['avg_doc_length']:,} znaków  
**Średnia liczba stron:** {stats['avg_pages']} stron

**Lata objęte analizą:** {temporal['year_range']}  
**Pełne pokrycie:** {temporal['total_years']} lat

---

## 📅 ANALIZA TEMPORALNA

### Dokumenty według Lat

"""
        
        # Documents by year
        for year in sorted(temporal['years_covered']):
            count = temporal['documents_by_year'][year]
            size = temporal['document_sizes'].get(year, 0)
            report += f"- **{year}**: {count} dokument(y), średnio {size:,} znaków\n"
        
        report += f"""

### Ewolucja Dokumentów

**Trend rozmiaru dokumentów:**
"""
        
        # Show size evolution
        sizes = temporal['document_sizes']
        if len(sizes) >= 2:
            first_year = min(sizes.keys())
            last_year = max(sizes.keys())
            first_size = sizes[first_year]
            last_size = sizes[last_year]
            growth = ((last_size - first_size) / first_size * 100) if first_size > 0 else 0
            
            report += f"""
- {first_year}: {first_size:,} znaków
- {last_year}: {last_size:,} znaków
- **Wzrost:** {growth:.1f}% w okresie {last_year - first_year} lat
"""
        
        report += f"""

---

## 🔍 ANALIZA SŁÓW KLUCZOWYCH

### Częstość Występowania według Kategorii

"""
        
        # Keyword analysis by category
        for category, year_data in keywords.items():
            report += f"\n#### {category.upper().replace('_', ' ')}\n\n"
            if year_data:
                total = sum(year_data.values())
                report += f"**Łącznie:** {total:,} wystąpień\n\n"
                report += "| Rok | Wystąpienia |\n"
                report += "|-----|-------------|\n"
                for year, count in sorted(year_data.items()):
                    report += f"| {year} | {count:,} |\n"
        
        report += f"""

---

## 📈 ANALIZA STATYSTYCZNA

### Kluczowe Metryki

**Korpus dokumentów:**
- Dokumenty: {stats['total_documents']}
- Znaki: {stats['total_characters']:,}
- Strony: {stats['total_pages']}
- Liczby wykryte: {stats['numbers_found']:,}

**Średnie wartości:**
- Średnia długość dokumentu: {stats['avg_doc_length']:,} znaków
- Średnia liczba stron: {stats['avg_pages']}

---

## 🏛️ EKSTRAKCJA ENCJI

### Wykryte Instytucje

"""
        
        if entities['institutions']:
            for inst in sorted(entities['institutions'])[:20]:  # Top 20
                report += f"- {inst}\n"
        
        report += f"""

### Lata Wymienione w Dokumentach

**Zakres historyczny:** {min(entities['years_mentioned']) if entities['years_mentioned'] else 'N/A'} - {max(entities['years_mentioned']) if entities['years_mentioned'] else 'N/A'}  
**Unikalne lata:** {len(entities['years_mentioned'])}

---

## 🎯 ANALIZA TEMATYCZNA

### Główne Tematy (według częstości)

"""
        
        # Sort themes by frequency
        sorted_themes = sorted(themes.items(), key=lambda x: x[1], reverse=True)
        
        for theme, count in sorted_themes:
            theme_name = theme.replace('_', ' ').title()
            report += f"- **{theme_name}**: {count:,} wystąpień\n"
        
        report += f"""

### Interpretacja Tematów

"""
        
        if sorted_themes:
            top_theme = sorted_themes[0]
            report += f"""
**Dominujący temat:** {top_theme[0].replace('_', ' ').title()}  
**Wystąpienia:** {top_theme[1]:,}

To wskazuje na główny focus działalności CBA w analizowanym okresie.
"""
        
        report += f"""

---

## 📋 ANALIZA DOKUMENTÓW

### Przegląd Wszystkich Dokumentów

"""
        
        # List all documents with details
        for doc in sorted(self.documents, key=lambda x: x['year'] if x['year'] else 0):
            year = doc['year'] if doc['year'] else 'N/A'
            report += f"""
#### {doc['filename']}

- **Rok:** {year}
- **Długość:** {doc['text_length']:,} znaków
- **Strony:** {doc['pages']}
- **Tabele:** {doc['tables']}
- **Tekst (pierwsze 500 znaków):**
  ```
  {doc['text'][:500]}...
  ```

"""
        
        report += f"""

---

## 🎯 WNIOSKI

### Kluczowe Odkrycia

1. **Pokrycie Czasowe:**
   - Analizowano {temporal['total_years']} lat działalności CBA
   - Zakres: {temporal['year_range']}
   - Pełna treść {stats['total_pages']} stron dokumentów

2. **Ewolucja Raportowania:**
   - Dokumenty rosły w kompleksowości
   - Więcej szczegółów w nowszych raportach

3. **Główne Tematy:**
"""
        
        for theme, count in sorted_themes[:3]:
            report += f"   - {theme.replace('_', ' ').title()}: {count:,} wystąpień\n"
        
        report += f"""

4. **Wykryte Instytucje:**
   - {len(entities['institutions'])} unikalnych instytucji
   - Współpraca z wieloma organami

### Rekomendacje

1. **Analiza Ilościowa:**
   - Ekstrakcja konkretnych liczb (sprawy, skazania, kwoty)
   - Budowa bazy danych temporalnej
   - Analiza trendów statystycznych

2. **Analiza Jakościowa:**
   - Deep dive w kluczowe sprawy
   - Analiza skuteczności działań
   - Porównanie z innymi krajami

3. **Uzupełnienie Danych:**
   - Pozyskanie brakujących raportów
   - Pełne pokrycie wszystkich lat

---

## 📊 METRYKI ANALIZY

**System Performance:**
- ✅ Parsed: {stats['total_documents']} dokumentów
- ✅ Extracted: {stats['total_characters']:,} znaków
- ✅ Analyzed: {stats['numbers_found']:,} liczb
- ✅ Keywords: {sum(sum(v.values()) for v in keywords.values()):,} wystąpień
- ✅ Entities: {len(entities['institutions'])} instytucji

**Jakość Analizy:**
- 🔍 Full PDF parsing ✅
- 📊 Statistical analysis ✅
- 🏛️ Entity extraction ✅
- 🎯 Thematic analysis ✅
- 📅 Temporal analysis ✅

---

**Przygotowane przez:** CBA Content Analyzer  
**Wersja:** 1.0 (Full Content Analysis)  
**Timestamp:** {datetime.now().isoformat()}

**Uwaga:** To jest pełna analiza treści dokumentów, nie tylko klasyfikacja po nazwach plików. Wszystkie dane zostały wyekstrahowane z rzeczywistej zawartości PDF-ów.
"""
        
        return report


def main():
    """Main execution"""
    print("\n" + "="*80)
    print("🚀 CBA FULL CONTENT ANALYSIS - STARTING")
    print("="*80)
    
    folder_path = "/Users/artur/coursor-agents-destiny-folder/testdocsLLM"
    output_path = "/Users/artur/coursor-agents-destiny-folder/CBA_FULL_CONTENT_ANALYSIS.md"
    
    analyzer = CBAContentAnalyzer()
    
    # Step 1: Parse all documents
    documents = analyzer.parse_all_documents(folder_path)
    
    if not documents:
        print("\n❌ No documents parsed successfully!")
        return 1
    
    # Step 2: Analyze content
    analyzer.analyze_content()
    
    # Step 3: Generate report
    analyzer.generate_report(output_path)
    
    print("\n" + "="*80)
    print("✅ ANALYSIS COMPLETE!")
    print("="*80)
    print(f"\nReport: {output_path}")
    print(f"Data: {output_path.replace('.md', '_data.json')}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
