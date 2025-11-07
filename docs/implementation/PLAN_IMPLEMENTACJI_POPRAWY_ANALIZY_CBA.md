# 🚀 PLAN IMPLEMENTACJI POPRAWY ANALIZY CBA

**Data:** 2024-11-05  
**Wersja:** 1.0  
**Status:** Gotowy do realizacji

---

## 📋 EXECUTIVE SUMMARY

Plan implementacji poprawy systemu analizy raportów CBA, eliminujący halucynacje LLM i zapewniający weryfikowalne dane liczbowe z dokumentów źródłowych.

**Główne cele:**
1. ✅ Ekstrakcja rzeczywistych danych z PDF-ów przed analizą LLM
2. ✅ Walidacja i oznaczanie niepewności danych
3. ✅ System cytowania źródeł
4. ✅ Optymalizacja wyboru embeddingów (Jina vs E5/IntFloat)

**Szacowany czas:** 3 tygodnie (przy pełnym zaangażowaniu)

---

## 🎯 FAZA 1: KRYTYCZNE NAPRAWY (Tydzień 1)

### **TASK 1.1: Ekstrakcja Tabel z PDF** 🔴 WYSOKI PRIORYTET

**Cel:** Wyekstrahować rzeczywiste dane liczbowe z PDF-ów przed analizą LLM

**Zadania:**
- [ ] Zainstalować `camelot-py` lub `tabula-py` dla ekstrakcji tabel
- [ ] Zainstalować `pdfplumber` dla zaawansowanej ekstrakcji
- [ ] Stworzyć moduł `src/parsing/pdf_table_extractor.py`
- [ ] Zintegrować z `UniversalFileExtractor`

**Szacowany czas:** 2-3 dni

**Implementacja:**
```python
# src/parsing/pdf_table_extractor.py

import camelot
import pdfplumber
from typing import List, Dict, Any

class PDFTableExtractor:
    """
    Extract tables and structured data from PDF files
    """
    
    def extract_tables(self, pdf_path: str) -> List[Dict[str, Any]]:
        """
        Extract all tables from PDF
        
        Returns:
            List of tables with metadata
        """
        tables = []
        
        # Method 1: Camelot (best for text-based tables)
        try:
            camelot_tables = camelot.read_pdf(pdf_path, pages='all')
            for table in camelot_tables:
                tables.append({
                    'method': 'camelot',
                    'page': table.page,
                    'data': table.df.to_dict('records'),
                    'accuracy': table.accuracy
                })
        except Exception as e:
            print(f"Camelot failed: {e}")
        
        # Method 2: PDFPlumber (fallback)
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    page_tables = page.extract_tables()
                    for table in page_tables:
                        tables.append({
                            'method': 'pdfplumber',
                            'page': page_num + 1,
                            'data': table
                        })
        except Exception as e:
            print(f"PDFPlumber failed: {e}")
        
        return tables
    
    def extract_numeric_data(self, pdf_path: str) -> Dict[str, Any]:
        """
        Extract numeric metrics from PDF
        
        Returns:
            Dict with extracted numeric data
        """
        # Extract text
        # Extract tables
        # Parse for key metrics (sprawy operacyjne, budżet, etc.)
        # Return structured data
        pass
```

**Zależności:**
```bash
pip install camelot-py[cv] tabula-py pdfplumber
```

**Testy:**
- Test na wszystkich 13 raportach CBA
- Weryfikacja jakości ekstrakcji
- Porównanie z ręczną ekstrakcją (próbka)

---

### **TASK 1.2: Pipeline Ekstrakcji → Walidacja → Analiza** 🔴 WYSOKI PRIORYTET

**Cel:** Stworzyć pipeline: PDF → Ekstrakcja → Walidacja → Analiza LLM

**Zadania:**
- [ ] Stworzyć moduł `src/parsing/data_extraction_pipeline.py`
- [ ] Integracja z `AutonomousOrchestrator`
- [ ] Struktura danych dla wyekstrahowanych metryk
- [ ] Walidacja danych (sprawdzenie spójności)

**Szacowany czas:** 2-3 dni

**Implementacja:**
```python
# src/parsing/data_extraction_pipeline.py

from typing import Dict, List, Any, Optional
from pathlib import Path
import json

class DataExtractionPipeline:
    """
    Complete pipeline for extracting and validating data from PDFs
    """
    
    def __init__(self):
        self.table_extractor = PDFTableExtractor()
        self.text_extractor = UniversalFileExtractor()
    
    def extract_case_data(self, pdf_paths: List[Path]) -> Dict[str, Any]:
        """
        Extract all data from PDFs for a case
        
        Returns:
            Structured data with extracted metrics
        """
        case_data = {
            'documents': [],
            'metrics': {},
            'tables': [],
            'extraction_metadata': {}
        }
        
        for pdf_path in pdf_paths:
            doc_data = self._extract_document_data(pdf_path)
            case_data['documents'].append(doc_data)
            
            # Aggregate metrics
            if doc_data.get('metrics'):
                self._merge_metrics(case_data['metrics'], doc_data['metrics'])
        
        return case_data
    
    def _extract_document_data(self, pdf_path: Path) -> Dict[str, Any]:
        """Extract data from single PDF"""
        # Extract text
        text, text_meta = self.text_extractor.extract_pdf(pdf_path)
        
        # Extract tables
        tables = self.table_extractor.extract_tables(str(pdf_path))
        
        # Extract numeric metrics
        metrics = self._extract_metrics(text, tables)
        
        return {
            'file': str(pdf_path),
            'text': text,
            'text_metadata': text_meta,
            'tables': tables,
            'metrics': metrics,
            'extraction_timestamp': datetime.now().isoformat()
        }
    
    def _extract_metrics(self, text: str, tables: List[Dict]) -> Dict[str, Any]:
        """Extract numeric metrics from text and tables"""
        metrics = {}
        
        # Patterns for CBA reports
        patterns = {
            'sprawy_operacyjne': r'spraw.*operacyjn[^.]*\s+(\d{1,4})',
            'budzet': r'budżet[^.]*\s+(\d{1,3}(?:\s?\d{3})*)\s*(?:mln|milion|zł)',
            # ... więcej wzorców
        }
        
        # Extract from text
        # Extract from tables
        # Cross-validate
        
        return metrics
    
    def validate_data(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate extracted data
        
        Returns:
            Validation report with confidence scores
        """
        validation = {
            'valid': True,
            'confidence': 1.0,
            'warnings': [],
            'errors': []
        }
        
        # Check data consistency
        # Check for missing critical data
        # Calculate confidence scores
        
        return validation
```

**Integracja z AutonomousOrchestrator:**
```python
# src/autonomous/autonomous_orchestrator.py

class AutonomousOrchestrator:
    def __init__(self):
        # ... existing code ...
        self.data_extractor = DataExtractionPipeline()  # NEW
    
    def process_case(self, folder_path: str, case_id: str):
        # STEP 1: Extract data BEFORE LLM analysis
        pdf_files = list(Path(folder_path).glob("*.pdf"))
        extracted_data = self.data_extractor.extract_case_data(pdf_files)
        
        # STEP 2: Validate extracted data
        validation = self.data_extractor.validate_data(extracted_data)
        
        # STEP 3: Store extracted data
        self._store_extracted_data(case_id, extracted_data)
        
        # STEP 4: LLM analyzes EXTRACTED data (not generates new)
        llm_prompt = self._build_llm_prompt(extracted_data)
        analysis = self.llm.analyze(llm_prompt)
        
        # STEP 5: Combine extracted data + LLM analysis
        final_report = self._combine_results(extracted_data, analysis)
        
        return final_report
```

---

### **TASK 1.3: Oznaczanie Szacunków i Niepewności** 🟡 ŚREDNI PRIORYTET

**Cel:** Oznaczyć wszystkie szacunki i brak danych w analizie

**Zadania:**
- [ ] Rozszerzyć format raportu o pole `data_confidence`
- [ ] Stworzyć helper do oznaczania niepewności
- [ ] Zaktualizować template raportu HTML/MD

**Szacowany czas:** 1 dzień

**Implementacja:**
```python
# src/analysis/data_confidence.py

from enum import Enum

class DataConfidence(Enum):
    VERIFIED = "verified"  # ✅ Zweryfikowane z PDF
    EXTRACTED = "extracted"  # ✅ Wyekstrahowane z dokumentu
    ESTIMATED = "estimated"  # ⚠️ Szacunek LLM
    MISSING = "missing"  # ❌ Brak danych

class DataMarker:
    """Mark data with confidence levels"""
    
    @staticmethod
    def mark_value(value: Any, confidence: DataConfidence, source: str = None) -> Dict:
        return {
            'value': value,
            'confidence': confidence.value,
            'source': source,
            'icon': DataMarker._get_icon(confidence)
        }
    
    @staticmethod
    def _get_icon(confidence: DataConfidence) -> str:
        icons = {
            DataConfidence.VERIFIED: "✅",
            DataConfidence.EXTRACTED: "✅",
            DataConfidence.ESTIMATED: "⚠️",
            DataConfidence.MISSING: "❌"
        }
        return icons[confidence]
```

---

### **TASK 1.4: Zmiana Promptu LLM** 🔴 WYSOKI PRIORYTET

**Cel:** LLM analizuje tylko wyekstrahowane dane, nie generuje nowe

**Zadania:**
- [ ] Zaktualizować prompt w `destiny_auto.py`
- [ ] Dodać instrukcje: "Nie generuj nowych liczb"
- [ ] Przekazywać wyekstrahowane dane do LLM

**Szacowany czas:** 0.5 dnia

**Nowy prompt:**
```python
PROMPT_TEMPLATE = """
Przeanalizuj następujące ZWERYFIKOWANE dane z raportów CBA:

{extracted_data}

WAŻNE:
- Nie generuj nowych liczb ani danych
- Analizuj TYLKO podane wyekstrahowane dane
- Jeśli brakuje danych dla jakiegoś roku, oznacz jako "BRAK DANYCH"
- Wszystkie wnioski powinny bazować na podanych danych

Zadania:
1. Przeanalizuj trendy w podanych danych
2. Zidentyfikuj kluczowe zmiany w czasie
3. Sformułuj wnioski strategiczne
4. Wskaż obszary wymagające uwagi
"""
```

---

## 🎯 FAZA 2: ULEPSZENIA (Tydzień 2)

### **TASK 2.1: System Cytowania Źródeł** 🟡 ŚREDNI PRIORYTET

**Cel:** Każda liczba w analizie ma źródło (plik, strona, tabela)

**Zadania:**
- [ ] Rozszerzyć strukturę danych o źródła
- [ ] Generator cytowań dla raportów
- [ ] Zintegrować z systemem raportowania

**Szacowany czas:** 2 dni

**Implementacja:**
```python
# src/analysis/source_citation.py

class SourceCitation:
    """Generate source citations for extracted data"""
    
    def cite(self, value: Any, source: Dict[str, Any]) -> str:
        """
        Generate citation string
        
        Format: "[PDF 2021, str. 15, tabela 2]"
        """
        parts = []
        
        if source.get('file'):
            year = self._extract_year(source['file'])
            parts.append(f"PDF {year}")
        
        if source.get('page'):
            parts.append(f"str. {source['page']}")
        
        if source.get('table'):
            parts.append(f"tabela {source['table']}")
        
        citation = ", ".join(parts)
        return f"[{citation}]"
```

---

### **TASK 2.2: OCR dla Skanowanych Dokumentów** 🟡 ŚREDNI PRIORYTET

**Cel:** Obsługa skanowanych PDF-ów (obrazy tekstu)

**Zadania:**
- [ ] Integracja Tesseract OCR
- [ ] Wykrywanie skanowanych dokumentów
- [ ] Fallback na OCR gdy brak tekstu

**Szacowany czas:** 2 dni

**Implementacja:**
```python
# src/parsing/pdf_ocr.py

import pytesseract
from pdf2image import convert_from_path

class PDFOCR:
    """OCR for scanned PDFs"""
    
    def extract_text_ocr(self, pdf_path: str) -> str:
        """Extract text using OCR"""
        images = convert_from_path(pdf_path)
        text_parts = []
        
        for image in images:
            text = pytesseract.image_to_string(image, lang='pol+eng')
            text_parts.append(text)
        
        return '\n\n'.join(text_parts)
```

---

### **TASK 2.3: Weryfikacja Danych** 🟡 ŚREDNI PRIORYTET

**Cel:** Automatyczna weryfikacja spójności danych

**Zadania:**
- [ ] Weryfikacja spójności między latami
- [ ] Wykrywanie anomalii w danych
- [ ] Raporty walidacji

**Szacowany czas:** 1-2 dni

---

## 🎯 FAZA 3: DŁUGOTERMINOWE (Tydzień 3+)

### **TASK 3.1: System Wersjonowania Danych** 🟢 NISKI PRIORYTET

**Cel:** Śledzenie zmian w wyekstrahowanych danych

**Szacowany czas:** 2 dni

---

### **TASK 3.2: Dashboard Weryfikacji** 🟢 NISKI PRIORYTET

**Cel:** Wizualny interfejs do weryfikacji danych

**Szacowany czas:** 3-5 dni

---

## 📊 METRYKI SUKCESU

| Metryka | Cel | Pomiar |
|---------|-----|--------|
| **Precyzja ekstrakcji** | >90% | Porównanie z ręczną ekstrakcją |
| **Pokrycie danych** | >80% | % lat z wyekstrahowanymi danymi |
| **Weryfikowalność** | 100% | Wszystkie liczby mają źródło |
| **Redukcja halucynacji** | 100% | Zero wymyślonych liczb |

---

## 🛠️ NARZĘDZIA I ZALEŻNOŚCI

### **Nowe biblioteki:**
```bash
pip install camelot-py[cv] tabula-py pdfplumber pytesseract pdf2image
```

### **Systemowe zależności:**
```bash
# macOS
brew install tesseract poppler

# Ubuntu/Debian
sudo apt-get install tesseract-ocr poppler-utils
```

---

## 📅 HARMONOGRAM

| Tydzień | Zadania | Status |
|---------|---------|--------|
| **Tydzień 1** | Task 1.1-1.4 (Krytyczne naprawy) | 🔴 |
| **Tydzień 2** | Task 2.1-2.3 (Ulepszenia) | 🟡 |
| **Tydzień 3+** | Task 3.1-3.2 (Długoterminowe) | 🟢 |

---

## ✅ CHECKLIST REALIZACJI

### **Faza 1:**
- [ ] Ekstrakcja tabel z PDF działa
- [ ] Pipeline ekstrakcji → walidacja → analiza działa
- [ ] Szacunki są oznaczone
- [ ] LLM nie generuje nowych liczb

### **Faza 2:**
- [ ] System cytowania działa
- [ ] OCR działa dla skanowanych PDF-ów
- [ ] Weryfikacja danych działa

### **Faza 3:**
- [ ] Wersjonowanie danych działa
- [ ] Dashboard weryfikacji działa

---

## 🚀 QUICK START

```bash
# 1. Zainstaluj zależności
pip install camelot-py[cv] tabula-py pdfplumber

# 2. Zainstaluj systemowe zależności (macOS)
brew install tesseract poppler

# 3. Przetestuj ekstrakcję
python -m src.parsing.pdf_table_extractor testdocsLLM/Informacja_2021.pdf

# 4. Uruchom pełny pipeline
python destiny_auto.py testdocsLLM/ --case-id cba_test_v2
```

---

**Autor:** System Architecture  
**Data utworzenia:** 2024-11-05  
**Ostatnia aktualizacja:** 2024-11-05
