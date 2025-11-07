# 🔄 PIPELINE ANALITYCZNY - PEŁNY OPIS PROCESU
## Jak działa system analizy dokumentów CBA

**Data:** 2024-11-05  
**System:** Autonomous Document Analysis System  
**Zakres:** Od skanowania folderu do profesjonalnej analizy 7-fazowej

---

## 📊 OVERVIEW - ARCHITEKTURA SYSTEMU

```
┌─────────────────────────────────────────────────────────────┐
│  USER INPUT: folder_path + case_id (optional)              │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: DOCUMENT DISCOVERY & CLASSIFICATION               │
│  ├─ DocumentScanner: skanuje folder                         │
│  ├─ IntelligentFileClassifier: klasyfikuje pliki          │
│  └─ AutomaticTaskGenerator: generuje zadania              │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: DOCUMENT STORAGE                                  │
│  ├─ UniversalDocumentParser: ekstrahuje tekst             │
│  ├─ DualEmbeddingSystem: generuje embeddings              │
│  └─ SmartDatabaseRouter: zapisuje do baz danych            │
│      ├─ PostgreSQL: dokumenty                             │
│      ├─ Elasticsearch: pełnotekstowe wyszukiwanie          │
│      ├─ Qdrant: wektory (embeddingi)                       │
│      └─ Neo4j: graf relacji                               │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: AUTONOMOUS AGENT EXECUTION                        │
│  ├─ Routing Logic: decyduje o typie analizy                │
│  │   ├─ Investigative? → Investigative Team lub           │
│  │   │                     Professional Analyzer          │
│  │   └─ Standard? → Basic Agents (Financial, Legal, etc.) │
│  │                                                   │
│  ├─ [IF INVESTIGATIVE] Professional Analyzer (7 faz)      │
│  │   ├─ Phase 1: Structure Analysis                      │
│  │   ├─ Phase 2: Quantitative Extraction                  │
│  │   ├─ Phase 3: Qualitative Analysis                     │
│  │   ├─ Phase 4: Temporal Trends                          │
│  │   ├─ Phase 5: Comparative Analysis                     │
│  │   ├─ Phase 6: Critical Assessment                      │
│  │   └─ Phase 7: Insight Synthesis                       │
│  │                                                   │
│  └─ [IF STANDARD] Basic Agents                           │
│      ├─ FinancialAnalystAgent                            │
│      ├─ LegalAnalystAgent                                 │
│      ├─ RiskAnalystAgent                                  │
│      ├─ DataScienceAgent                                  │
│      ├─ ArchitectAgent                                    │
│      └─ DocumentationAgent                               │
│          └─ LMStudioLLMClient + RAGCAGOrchestrator       │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: RESULT SYNTHESIS                                  │
│  ├─ Aggregacja wyników z wszystkich agentów                │
│  ├─ Generowanie raportu końcowego                          │
│  └─ Zapis do pliku JSON                                   │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
                    FINAL RESULTS
```

---

## 🔍 SZCZEGÓŁOWY PRZEPŁYW KROK PO KROKU

### 🚀 INICJALIZACJA SYSTEMU (`__init__`)

**Kiedy:** Przy starcie `AutonomousOrchestrator`

**Komponenty inicjalizowane:**

1. **Document Discovery System**
   ```
   self.task_generator = AutomaticTaskGenerator()
   ```
   - Zawiera: `DocumentScanner`, `IntelligentFileClassifier`
   - Cel: Skanowanie i klasyfikacja plików

2. **LLM Client (LMStudio)**
   ```
   self.llm = LMStudioLLMClient(
       base_url="http://192.168.200.226:1234/v1",
       model="openai/gpt-oss-20b"
   )
   ```
   - Cel: Lokalne LLM do analizy tekstu
   - Sprawdza połączenie: `health_check()`

3. **RAG + CAG Orchestrator**
   ```
   self.rag_cag = RAGCAGOrchestrator(
       context_window=44000,
       use_cag=True
   )
   ```
   - Cel: Optymalizacja kontekstu dla LLM
   - Cache Augmented Generation: używa cache zamiast pełnego kontekstu

4. **Data Infrastructure**
   ```
   self.embeddings = DualEmbeddingSystem()
   self.db_router = SmartDatabaseRouter()
   ```
   - Embeddings: generuje wektory dla dokumentów
   - Router: decyduje gdzie zapisać (PostgreSQL/Elasticsearch/Qdrant/Neo4j)

5. **Basic Agents Registry**
   ```
   self.agents = {
       'financial': FinancialAnalystAgent(),
       'legal': LegalAnalystAgent(),
       'risk': RiskAnalystAgent(),
       'data_science': DataScienceAgent(),
       'architect': ArchitectAgent(),
       'documentation': DocumentationAgent(),
   }
   ```
   - 6 podstawowych agentów specjalistycznych

6. **Investigative Team** (opcjonalnie)
   ```
   self.investigative_team = AnalyticalTeam()
   ```
   - 9 wyspecjalizowanych agentów investigacyjnych
   - Wymaga: `agents.analytical.analytical_team`

7. **Professional Analyzer** (NOWY!)
   ```
   self.professional_analyzer = ProfessionalAnalyzer(
       config=AnalysisConfig(
           enable_structure_analysis=True,
           enable_quantitative_extraction=True,
           enable_qualitative_analysis=True,
           enable_temporal_trends=True,
           enable_comparative_analysis=True,
           enable_critical_assessment=True,
           enable_synthesis=True,
       )
   )
   ```
   - 7-fazowy engine analizy profesjonalnej
   - Działa niezależnie od Investigative Team

**Wynik:** System gotowy do przetwarzania

---

### 📋 STEP 1: DOCUMENT DISCOVERY & CLASSIFICATION

**Metoda:** `process_folder()` → `task_generator.process_folder()`

**Proces:**

#### 1.1. Document Scanning (`DocumentScanner`)

```python
scanner = DocumentScanner()
files = scanner.scan_folder(folder_path)
```

**Co się dzieje:**
- Skanuje folder rekursywnie
- Zbiera wszystkie pliki (PDF, DOCX, TXT, MD, etc.)
- Dla każdego pliku:
  - Oblicza hash (identyfikator unikalny)
  - Sprawdza rozmiar
  - Określa typ mime

**Wynik:** Lista plików z metadanymi

#### 1.2. Intelligent Classification (`IntelligentFileClassifier`)

```python
classifier = IntelligentFileClassifier()
for file in files:
    category, confidence = classifier.classify_file(file)
```

**Co się dzieje:**

**Klasyfikacja bazuje na:**
- **Nazwie pliku:** Regex patterns (np. `.*cba.*`, `.*informacja.*`)
- **Rozszerzeniu:** `.pdf` → dokument
- **Słowach kluczowych:** Wyszukiwanie w nazwie pliku

**Kategorie:**
- `investigative` - dokumenty investigacyjne (CBA, śledztwa)
- `financial` - dokumenty finansowe
- `legal` - dokumenty prawne
- `technical` - dokumenty techniczne
- `general` - pozostałe

**Dla CBA:**
```
Keywords: ['cba', 'antykorupcyjn', 'śledztw', 'investigation']
→ Category: investigative
→ Confidence: 0.50-0.60
```

**Wynik:** Każdy plik ma kategorię i confidence score

#### 1.3. Task Generation (`AutomaticTaskGenerator`)

```python
tasks = generator.generate_tasks(files)
```

**Co się dzieje:**

**Dla każdej kategorii:**
1. Grupuje pliki według kategorii
2. Wybiera odpowiednich agentów:
   - `investigative` → `['investigative']` (specjalny marker)
   - `financial` → `['financial']`
   - `legal` → `['legal']`
   - etc.

3. Określa typ investigacji (jeśli investigative):
   - `comprehensive` - pełna analiza
   - `osint` - analiza OSINT
   - `financial` - analiza finansowa
   - `legal` - analiza prawna

4. Generuje zadania:
```python
task = {
    'task_id': 'task_001',
    'category': 'investigative',
    'priority': 91,  # wysoki priorytet
    'agents': ['investigative'],
    'files': [...],  # lista plików
    'file_count': 13,
    'investigation_type': 'comprehensive',
    'analyses': ['trend_analysis', 'quantitative_extraction', ...]
}
```

**Wynik:** Lista zadań do wykonania

---

### 💾 STEP 2: DOCUMENT STORAGE

**Metoda:** `_store_documents()`

**Proces:**

#### 2.1. Content Extraction (`UniversalDocumentParser`)

```python
parser = UniversalDocumentParser()
for file_info in files:
    parse_result = parser.parse(file_path)
    content = parse_result.text
```

**Co się dzieje:**

**Dla każdego pliku:**
- **PDF:** `pdftotext` (command-line) lub `PyPDF2` (fallback)
- **DOCX:** `python-docx`
- **TXT/MD:** bezpośrednie odczytanie
- **Tabele:** Ekstrakcja tabel z PDF (`PDFTableExtractor`)

**Wynik:** Tekst z każdego dokumentu

#### 2.2. Embedding Generation (`DualEmbeddingSystem`)

```python
embedding_result = self.embeddings.embed(
    content,
    document_type=file_info.get('category', 'general')
)
```

**Co się dzieje:**

**System dual embedding:**
- **Jina Embeddings:** Dla większości dokumentów
- **E5/IntFloat:** Dla dokumentów specjalistycznych

**Proces:**
1. Tekst dzielony na chunki (np. 500 znaków)
2. Dla każdego chunka:
   - Generowany embedding (wektor 768/1024 wymiarów)
   - Metadata (filename, category, chunk_id)

**Wynik:** Wektory dla każdego dokumentu

#### 2.3. Database Storage (`SmartDatabaseRouter`)

```python
# PostgreSQL: Dokumenty pełnotekstowe
doc_id = self.db_router.store_document(
    case_id=case_id,
    document_id=file_info['hash'],
    filename=file_info['filename'],
    content=content,
    document_type=file_info['type'],
    metadata={...}
)

# Qdrant: Embeddings
db_used, count = self.db_router.store_embeddings(
    case_id, 
    embedding_records
)
```

**Co się dzieje:**

**Smart Routing:**
- **PostgreSQL:** Dokumenty strukturalne, metadane
- **Elasticsearch:** Pełnotekstowe wyszukiwanie
- **Qdrant:** Wektory (embeddingi) dla similarity search
- **Neo4j:** Graf relacji między dokumentami

**Wynik:** Wszystkie dokumenty zapisane w bazach danych

---

### 🤖 STEP 3: AUTONOMOUS AGENT EXECUTION

**Metoda:** `_execute_tasks()`

**Proces:**

#### 3.1. Task Routing Logic

```python
for task in tasks:
    if 'investigative' in task['agents']:
        if self.investigative_enabled:
            # Investigative Team
            result = self._execute_investigative_task(...)
        elif self.professional_analyzer:
            # Professional Analyzer (7 faz)
            result = self._execute_professional_analysis_task(...)
    else:
        # Basic Agents
        result = self._execute_with_basic_agents(...)
```

**Routing Decision Tree:**

```
Task Category?
├─ investigative?
│   ├─ Investigative Team available? → Use Investigative Team
│   └─ Professional Analyzer available? → Use Professional Analyzer (7 faz)
│
└─ Other (financial, legal, etc.)?
    └─ Use Basic Agents (FinancialAnalystAgent, etc.)
```

---

### 🔍 PROFESSIONAL ANALYZER - 7 FAZ (DLA INVESTIGATIVE)

**Metoda:** `_execute_professional_analysis_task()`

**Proces:**

#### Dokument Preparation

```python
parser = UniversalDocumentParser()
documents = []
for file_info in file_paths:
    parse_result = parser.parse(file_path)
    year = extract_year_from_filename(filename)
    documents.append({
        'filename': filename,
        'text': parse_result.text,
        'year': year,
        'path': file_path,
    })
```

**Co się dzieje:**
- Parsuje wszystkie pliki PDF
- Ekstrahuje tekst
- Wyciąga rok z nazwy pliku (np. "Informacja_2021.pdf" → 2021)

**Wynik:** Lista dokumentów z tekstem i metadanymi

#### 🔬 Phase 1: Structure Analysis (`StructureExtractor`)

```python
results['phase1'] = self.structure_extractor.analyze(documents)
```

**Co się dzieje:**

1. **Extract Sections:**
   - Regex patterns dla nagłówków sekcji
   - Wzorce: `Rozdział`, `DZIAŁ`, `###`, etc.
   - Analiza pierwszych 10k znaków każdego dokumentu

2. **Identify Common Sections:**
   - Lista sekcji wspólnych dla wszystkich dokumentów
   - Częstotliwość występowania

3. **Analyze Evolution:**
   - Porównanie struktury między wczesnymi i późnymi dokumentami
   - Zmiany w czasie

**Wynik:**
```python
{
    'total_documents': 13,
    'structures': {
        2021: {
            'filename': 'Informacja_2021.pdf',
            'sections': ['Wprowadzenie', 'Działalność operacyjna', ...],
            'text_length': 111009,
            'section_count': 8
        },
        ...
    },
    'common_sections': ['Wprowadzenie', 'Działalność operacyjna', ...],
    'evolution': {
        'early_period': {'avg_sections': 6.5},
        'recent_period': {'avg_sections': 9.2},
        'evolution': 'increasing'
    }
}
```

---

#### 📊 Phase 2: Quantitative Extraction (`QuantitativeExtractor`)

```python
results['phase2'] = self.quantitative_extractor.extract(documents)
```

**Co się dzieje:**

1. **Pattern Matching:**
   - Regex patterns dla metryk:
     - `sprawy_operacyjne`: `r'spraw[^.]*operacyjn[^.]*[:\s]+(\d{1,4})'`
     - `zatrzymania`: `r'zatrzyman[^.]*[:\s]+(\d{1,4})'`
     - `skazania`: `r'skazan[^.]*[:\s]+(\d{1,4})'`
     - `budzet`: `r'budżet[^.]*[:\s]+(\d{1,3}(?:\s?\d{3})*)\s*(?:mln|milion|zł)'`
     - etc.

2. **Extract Values:**
   - Dla każdego dokumentu:
     - Szuka wszystkich wzorców w tekście
     - Wyciąga wartości liczbowe
     - Waliduje (czy to liczba)

3. **Aggregate by Year:**
   - Grupuje metryki według roku
   - Wybiera najbardziej prawdopodobną wartość (najczęstsza)

**Wynik:**
```python
{
    'metrics': {
        2021: {
            'sprawy_operacyjne': {
                'value': 1234,
                'confidence': 'extracted',
                'source': 'Informacja_2021.pdf',
                'matches_found': 3
            },
            'zatrzymania': {...},
            'skazania': {...},
            ...
        },
        2022: {...},
        ...
    },
    'total_years': 13,
    'extraction_summary': {
        'total_metrics_extracted': 45,
        'metrics_per_year': {2021: 5, 2022: 4, ...}
    }
}
```

---

#### 📝 Phase 3: Qualitative Analysis (`QualitativeAnalyzer`)

```python
results['phase3'] = self.qualitative_analyzer.analyze(documents)
```

**Co się dzieje:**

1. **Tone Analysis:**
   - Wzorce słów kluczowych:
     - `positive`: ['sukces', 'osiągnięci', 'efektywn', ...]
     - `challenge`: ['wyzwani', 'trudności', 'problem', ...]
     - `cooperation`: ['współprac', 'kooperacj', ...]
     - `innovation`: ['nowoczesn', 'innowacj', ...]
   - Liczy wystąpienia każdego tonu

2. **Theme Analysis:**
   - Wzorce tematów:
     - `korupcja`: ['korupcj', 'łapówk', ...]
     - `współpraca_międzynarodowa`: ['międzynarodow', 'europejsk', ...]
     - `technologia`: ['technolog', 'cyfrow', ...]
   - Liczy wystąpienia każdego tematu

3. **Evolution Analysis:**
   - Porównanie tonu/tematów między okresami
   - Zmiany w czasie

**Wynik:**
```python
{
    'narrative_analysis': {
        2021: {
            'tone': {
                'positive': 45,
                'challenge': 12,
                'cooperation': 33,
                'innovation': 8
            },
            'themes': {
                'korupcja': 47,
                'śledztwa': 95,
                'współpraca': 28,
                ...
            },
            'dominant_tone': 'positive',
            'dominant_theme': 'śledztwa'
        },
        ...
    },
    'evolution': {
        'early_period': {'positive': 30, 'challenge': 8, ...},
        'recent_period': {'positive': 45, 'challenge': 12, ...},
        'changes': {'positive': 50.0, 'challenge': 50.0, ...}
    }
}
```

---

#### 📈 Phase 4: Temporal Trends (`TemporalTrendAnalyzer`)

```python
results['phase4'] = self.trend_analyzer.analyze(results['phase2'])
```

**Co się dzieje:**

1. **Extract Time Series:**
   - Dla każdej metryki: wartości przez lata
   - Przykład: `sprawy_operacyjne`: [1234, 1345, 1456, ...]

2. **Calculate Trends:**
   - **Total Growth:** `(last - first) / first * 100`
   - **CAGR:** Compound Annual Growth Rate
   - **Linear Regression:** Trend direction (increasing/decreasing/stable)
   - **Correlation:** Siła trendu (R²)

3. **Find Inflection Points:**
   - Wykrywa punkty zwrotne (peaks, troughs)
   - Anomalie w danych

**Wynik:**
```python
{
    'trends': {
        'sprawy_operacyjne': {
            'years': [2021, 2022, 2023, 2024],
            'values': [1234, 1345, 1456, 1523],
            'first_value': 1234,
            'last_value': 1523,
            'total_growth': 23.4,
            'cagr': 7.2,
            'trend': 'increasing',
            'trend_strength': 0.89,
            'slope': 96.3,
            'inflection_points': [
                {'year': 2022, 'value': 1345, 'type': 'peak'}
            ]
        },
        ...
    },
    'summary': {
        'total_metrics': 5,
        'increasing': 3,
        'decreasing': 1,
        'stable': 1
    }
}
```

---

#### 🔍 Phase 5: Comparative Analysis (`ComparativeAnalyzer`)

```python
results['phase5'] = self.comparative_analyzer.analyze(results['phase2'])
```

**Co się dzieje:**

1. **Efficiency Metrics:**
   - **Success Rate:** `(skazania / sprawy_operacyjne) * 100`
   - **Cost per Case:** `budzet / sprawy_operacyjne`
   - **Cases per Employee:** `sprawy_operacyjne / funkcjonariusze`

2. **Period Comparison:**
   - Podział na okresy (early vs recent)
   - Średnie wartości dla każdego okresu
   - Zmiany procentowe

3. **Correlations:**
   - Analiza korelacji między metrykami
   - Zależności

**Wynik:**
```python
{
    'efficiency_metrics': {
        2021: {
            'success_rate': 45.2,
            'cost_per_case': 76923.45,
            'cases_per_employee': 12.3
        },
        ...
    },
    'periods': {
        'early': [2021, 2022, 2023],
        'recent': [2024, 2025],
        'comparison': {
            'sprawy_operacyjne': {
                'early_avg': 1350,
                'recent_avg': 1480,
                'change': 9.6
            },
            ...
        }
    }
}
```

---

#### ⚠️ Phase 6: Critical Assessment (`CriticalAssessor`)

```python
results['phase6'] = self.critical_assessor.assess(documents, results)
```

**Co się dzieje:**

1. **Data Completeness:**
   - Sprawdza brakujące lata
   - Procent kompletności danych dla każdego roku

2. **Consistency Checks:**
   - Logiczne niespójności:
     - `skazania > sprawy_operacyjne` → ERROR
     - `cost_per_case > threshold` → ANOMALY
   - Walidacja wartości

3. **Confidence Scoring:**
   - Ocena ogólnego confidence:
     - `avg_completeness * 0.7 + consistency_score * 0.3`

4. **Limitations:**
   - Lista ograniczeń analizy

**Wynik:**
```python
{
    'data_completeness': {
        2021: 0.85,
        2022: 0.92,
        ...
    },
    'consistency_issues': [
        {
            'year': 2023,
            'issue': 'Skazania (1500) > Sprawy (1200)',
            'type': 'logical_inconsistency',
            'severity': 'high'
        }
    ],
    'missing_years': [2009, 2016, 2018],
    'overall_confidence': 0.78,
    'limitations': [
        'Analysis based on text extraction only',
        'Tables may contain additional data',
        ...
    ]
}
```

---

#### 💡 Phase 7: Insight Synthesis (`SynthesisEngine`)

```python
results['phase7'] = self.synthesis_engine.synthesize(results)
```

**Co się dzieje:**

1. **Extract Key Findings:**
   - Z Phase 4 (trends): wszystkie trendy != 'stable'
   - Formatuje jako kluczowe odkrycia

2. **Efficiency Insights:**
   - Z Phase 5: średnie wartości efektywności
   - Interpretacja (wysoka/średnia/niska skuteczność)

3. **Recommendations:**
   - Z Phase 6: brakujące lata → rekomendacja pozyskania
   - Niespójności → rekomendacja weryfikacji

4. **Executive Summary:**
   - Synteza wszystkich wniosków w krótki tekst

**Wynik:**
```python
{
    'key_findings': [
        {
            'metric': 'Sprawy Operacyjne',
            'trend': 'increasing',
            'growth': 23.4,
            'cagr': 7.2,
            'significance': 'high'
        },
        ...
    ],
    'efficiency_insights': [
        {
            'metric': 'Average Success Rate',
            'value': 42.5,
            'interpretation': 'Średnia skuteczność'
        }
    ],
    'recommendations': [
        {
            'type': 'data_completeness',
            'priority': 'high',
            'text': 'Pozyskać brakujące raporty dla lat: 2009, 2016, 2018'
        },
        ...
    ],
    'executive_summary': 'Zidentyfikowano 3 kluczowe trendy. Analiza efektywności...'
}
```

---

### 🤖 BASIC AGENTS EXECUTION (DLA STANDARD TASKS)

**Metoda:** `_execute_tasks()` → basic agents loop

**Proces:**

```python
for agent_type in task['agents']:
    agent = self.agents.get(agent_type)
    
    # Parse documents
    task_docs = parse_documents(task['files'])
    
    # Build prompt with RAG+CAG
    prompt = context_mgr.create_optimized_prompt(
        case_id=case_id,
        agent_type=agent_type,
        new_content=hot_content
    )
    
    # LLM Analysis
    llm_response = self.llm.chat_completion([
        {"role": "user", "content": prompt}
    ])
    
    # Store result
    agent_results.append({
        'agent': agent_type,
        'output': llm_response.content,
        'tokens_used': llm_response.tokens_used,
        'confidence': 0.85
    })
```

**Co się dzieje:**

1. **Document Parsing:**
   - Ekstrahuje tekst z plików
   - Ogranicza do pierwszych 2000 znaków (context window)

2. **RAG + CAG Optimization:**
   - **RAG:** Retrieval Augmented Generation - pobiera podobne dokumenty z cache
   - **CAG:** Cache Augmented Generation - używa cache zamiast pełnego kontekstu
   - Optymalizuje prompt do rozmiaru context window

3. **LLM Analysis:**
   - Wysyła prompt do LMStudio
   - Otrzymuje analizę tekstową

4. **Result Formatting:**
   - Formatuje wynik jako output agenta

**Wynik:** Lista wyników od każdego agenta

---

### 📊 STEP 4: RESULT SYNTHESIS

**Metoda:** `_synthesize_results()`

**Proces:**

1. **Aggregate Results:**
   - Zbiera wszystkie wyniki z agentów
   - Grupuje według kategorii

2. **Extract Findings:**
   - Kluczowe odkrycia z każdego agenta
   - Confidence scores

3. **Generate Report:**
   - Tworzy JSON report:
     ```json
     {
         "case_id": "...",
         "folder": "...",
         "summary": {
             "total_files": 13,
             "total_tasks": 2,
             "successful_agents": 7
         },
         "findings": [...],
         "task_results": [...]
     }
     ```

4. **Save to File:**
   - Zapisuje do `reports/autonomous_{case_id}.json`

**Wynik:** Kompletny raport analizy

---

## 🔄 KOMPLETNY PRZEPŁYW - PRZYKŁAD DLA CBA

### Input:
```
folder_path: "testdocsLLM/"
case_id: "professional_analysis_20251105_143407"
```

### Step 1: Discovery
```
📂 Skanowanie folderu...
   Znaleziono 14 plików
   
📋 Klasyfikacja...
   Informacja_2021.pdf → investigative (confidence: 0.50)
   Informacja_2022.pdf → investigative (confidence: 0.50)
   ...
   
🎯 Generowanie zadań...
   Task 1: INVESTIGATIVE (13 plików)
   Task 2: TECHNICAL (1 plik)
```

### Step 2: Storage
```
💾 Zapisywanie dokumentów...
   Parsowanie PDF...
   Generowanie embeddings...
   Zapis do PostgreSQL...
   Zapis do Elasticsearch...
   Zapis do Qdrant...
   Zapis do Neo4j...
```

### Step 3: Execution
```
🤖 Task 1: INVESTIGATIVE
   📊 Routing to Professional Analyzer
   
   📋 Phase 1: Structure Analysis...
      Przeanalizowano 13 dokumentów
      Znaleziono 8 wspólnych sekcji
   
   📊 Phase 2: Quantitative Extraction...
      Wyekstrahowano metryki dla 13 lat
      Znaleziono 45 wartości metryk
   
   📝 Phase 3: Qualitative Analysis...
      Przeanalizowano ton i tematy
      Dominujący ton: positive
      Dominujący temat: śledztwa
   
   📈 Phase 4: Temporal Trends...
      Przeanalizowano 5 trendów
      Trendy: 3 increasing, 1 decreasing, 1 stable
   
   🔍 Phase 5: Comparative Analysis...
      Obliczono metryki efektywności
      Success rate: 42.5%
   
   ⚠️  Phase 6: Critical Assessment...
      Znaleziono 2 niespójności
      Confidence: 0.78
   
   💡 Phase 7: Insight Synthesis...
      3 kluczowe wnioski
      2 rekomendacje
   
   ✅ Professional Analysis complete (0.2s)
```

### Step 4: Synthesis
```
📊 Generowanie raportu...
   Zapisano: reports/autonomous_professional_analysis_20251105_143407.json
```

---

## 🔧 KOMPONENTY SYSTEMU - SZCZEGÓŁY

### 1. Document Parser (`UniversalDocumentParser`)
- **PDF:** `pdftotext` (command-line) lub `PyPDF2`
- **DOCX:** `python-docx`
- **TXT/MD:** bezpośrednie odczytanie
- **Tabele:** `PDFTableExtractor` (camelot, pdfplumber)

### 2. Embedding System (`DualEmbeddingSystem`)
- **Jina:** Dla większości dokumentów (768 dim)
- **E5/IntFloat:** Dla dokumentów specjalistycznych (1024 dim)

### 3. Database Router (`SmartDatabaseRouter`)
- **PostgreSQL:** Dokumenty strukturalne
- **Elasticsearch:** Pełnotekstowe wyszukiwanie
- **Qdrant:** Wektory (similarity search)
- **Neo4j:** Graf relacji

### 4. LLM Client (`LMStudioLLMClient`)
- **Base URL:** `http://192.168.200.226:1234/v1`
- **Model:** `openai/gpt-oss-20b`
- **Context Window:** 44000 tokens

### 5. RAG+CAG (`RAGCAGOrchestrator`)
- **RAG:** Retrieval podobnych dokumentów
- **CAG:** Cache zamiast pełnego kontekstu
- **Optymalizacja:** Redukcja użycia tokenów

---

## ⏱️ TIMELINE - CZAS WYKONANIA

Typowy czas dla 13 dokumentów CBA:

```
Inicjalizacja:         ~2-3s
Discovery:             ~0.5s
Storage:               ~5-10s
Professional Analysis: ~0.2-2s (7 faz)
Basic Agents:          ~10-30s per agent
Synthesis:             ~0.1s

TOTAL:                 ~25-50s
```

---

## 🎯 DECISION POINTS

**Routing Decisions:**

1. **Investigative vs Standard?**
   - Klasyfikacja: `investigative` keyword → Investigative
   - Inne → Standard

2. **Investigative Team vs Professional Analyzer?**
   - Investigative Team available? → Use Team
   - Professional Analyzer available? → Use Analyzer
   - None? → Fallback to basic agents

3. **Which Basic Agent?**
   - Category: `financial` → FinancialAnalystAgent
   - Category: `legal` → LegalAnalystAgent
   - etc.

---

**To jest kompletny pipeline analityczny!** 🎉

System działa automatycznie od skanowania folderu do profesjonalnej analizy 7-fazowej, wykorzystując wszystkie komponenty: parsery, embeddings, bazy danych, LLM, RAG+CAG, i Professional Analyzer.
