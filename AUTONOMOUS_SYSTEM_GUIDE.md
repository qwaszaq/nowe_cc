# 🤖 AUTONOMOUS SYSTEM - User Guide

## Koncepcja: "Wskaż i Zapomnij"

System działa **w pełni autonomicznie**:

```
TY: "Przeanalizuj folder /data/documents/"
    ↓
SYSTEM AUTOMATYCZNIE:
  1. 🔍 Skanuje i klasyfikuje pliki
  2. 🧠 Decyduje jakie analizy przeprowadzić
  3. 🛠️ Wybiera odpowiednie narzędzia
  4. 🤖 Wykonuje pracę agentami
  5. 📊 Generuje raport
```

---

## 🚀 Quick Start

### Podstawowe użycie:

```bash
# Wskaż folder - system zrobi resztę
python destiny_auto.py /path/to/your/documents
```

### Z własnym ID:

```bash
python destiny_auto.py /data/case_001 --case-id case_001
```

### Przykład z verbose:

```bash
python destiny_auto.py ~/Documents/financial_reports --verbose
```

---

## 📋 Co system robi automatycznie?

### 1. **Document Discovery** (Wykrywanie dokumentów)

System automatycznie:
- ✅ Skanuje folder i podfoldery
- ✅ Identyfikuje typy plików (PDF, Excel, txt, etc.)
- ✅ Oblicza metadane (rozmiar, hash, data modyfikacji)
- ✅ Grupuje pliki według typu

**Obsługiwane formaty:**
```
📄 Dokumenty:     .pdf, .docx, .doc, .txt, .md
📊 Dane:          .xlsx, .xls, .csv
📋 Strukturalne:  .json, .xml, .yaml
🖼️  Obrazy:       .png, .jpg, .jpeg, .tiff (OCR)
```

---

### 2. **Intelligent Classification** (Inteligentna klasyfikacja)

System analizuje zawartość i automatycznie określa kategorię:

```python
Categories:
  🔍 investigative - Dochodzenia, OSINT, sprawy korupcyjne, śledztwa
  💰 financial     - Raporty finansowe, bilanse, wyniki
  ⚖️  legal        - Kontrakty, umowy, regulacje
  🏗️  technical    - Specyfikacje, architektury, dokumentacja
  📊 data          - Zbiory danych, statystyki
  📝 general       - Ogólne dokumenty
```

**NOWOŚĆ: Automatyczna detekcja treści investigative!**

System wykrywa dokumenty investigative na podstawie słów kluczowych:
- 🇬🇧 English: investigation, osint, intelligence, fraud, corruption, scandal, witness, evidence
- 🇵🇱 Polski: cba, prokuratura, śledztwo, postępowanie, afera, świadek, dowód

**Przykład:**
```
Plik: "Q4_2023_Financial_Report.pdf"
→ System: "To jest financial document (confidence: 0.95)"
→ Sugerowane analizy: financial_analysis, trend_analysis
```

---

### 3. **Automatic Task Generation** (Automatyczne zadania)

System generuje zadania na podstawie:
- Typu dokumentów
- Kategorii
- Zawartości
- Priorytetów

**Przykład:**
```
Wykryte:
  - 3 pliki financial
  - 2 pliki legal
  - 5 plików data

Wygenerowane zadania:
  1. [Priority: 85] Financial Analysis (3 files)
     Agents: financial, data_science
     
  2. [Priority: 75] Legal Review (2 files)
     Agents: legal, risk
     
  3. [Priority: 70] Data Analysis (5 files)
     Agents: data_science
```

---

### 4. **Agent Orchestration** (Orkiestracja agentów)

System automatycznie:
- ✅ Wybiera odpowiednich agentów
- ✅ Przekazuje im kontekst
- ✅ Wykonuje analizy równolegle (gdy możliwe)
- ✅ Zbiera wyniki
- ✅ **NOWOŚĆ:** Routuje do investigative team gdy wykryje treści śledcze!

**Dostępni agenci - BASIC TEAM (6 agentów):**
```
💰 financial      - Analiza finansowa
⚖️  legal         - Przegląd prawny
⚠️  risk          - Ocena ryzyka
📊 data_science   - Analiza danych
🏗️  architect     - Przegląd techniczny
📝 documentation  - Dokumentacja
```

**NOWOŚĆ: INVESTIGATIVE TEAM (9 specjalistycznych agentów):**
```
🎯 Viktor Kovalenko    - Investigation Director (Orchestrator)
🔍 Elena Volkov        - OSINT Specialist
💰 Marcus Chen         - Financial Analyst
⚖️  Adrian Kowalski    - Legal Analyst
📊 Maya Patel          - Data Analyst
📈 Sofia Martinez      - Market Research Specialist
🎭 Damian Rousseau     - Devil's Advocate (Critical Review)
📝 Lucas Rivera        - Report Synthesizer
🔧 Alex Morgan         - Technical Liaison
```

**Typy investigacji:**
- `comprehensive` - Pełne dochodzenie (wszystkie fazy, wszyscy agenci)
- `osint` - Wywiad open-source (Elena)
- `financial` - Analiza finansowa (Marcus)
- `legal` - Analiza prawna (Adrian)

---

### 5. **Tool Selection** (Wybór narzędzi)

Agenci automatycznie wybierają narzędzia:

```python
Plik: report.pdf
→ Agent używa: extract_text_from_pdf

Plik: data.xlsx
→ Agent używa: extract_tables_from_excel

Zadanie: "find financial documents"
→ Agent używa: semantic_search
```

**Dostępne kategorie narzędzi:**
- 📄 `extraction` - Ekstrakcja tekstu/danych
- 🔍 `search` - Wyszukiwanie
- 📊 `analysis` - Analiza statystyczna
- 🧠 `nlp` - Przetwarzanie języka

---

## 🎯 Przykładowe Scenariusze

### Scenariusz 1: Analiza Finansowa

```bash
# Masz folder z raportami finansowymi
python destiny_auto.py ~/Finance/Q4_2023

# System automatycznie:
# 1. Wykryje PDFy i Excele
# 2. Sklasyfikuje jako "financial"
# 3. Użyje agentów: financial + data_science
# 4. Wygeneruje analizę trendów i kluczowych metryk
```

### Scenariusz 2: Due Diligence

```bash
# Masz mix dokumentów do przeglądu
python destiny_auto.py ~/Cases/CompanyX_DD --case-id companyX

# System automatycznie:
# 1. Sklasyfikuje dokumenty (financial/legal/technical)
# 2. Użyje odpowiednich agentów dla każdej kategorii
# 3. Wygeneruje kompleksowy raport due diligence
```

### Scenariusz 3: Analiza Danych

```bash
# Masz folder z CSV i Excel
python destiny_auto.py ~/Data/market_research

# System automatycznie:
# 1. Wykryje pliki tabelaryczne
# 2. Użyje data_science agent
# 3. Przeprowadzi analizę statystyczną
# 4. Wygeneruje wnioski i wizualizacje
```

### 🆕 Scenariusz 4: Investigative Analysis

```bash
# Masz dokumenty śledcze (raporty CBA, prokuratura, etc.)
python destiny_auto.py ~/Cases/Investigation_2024 --case-id fraud_case_001

# System automatycznie:
# 1. WYKRYJE treści investigative (keywords: investigation, fraud, CBA, śledztwo)
# 2. PRZEŁĄCZY na Investigative Team (9 specjalistów)
# 3. URUCHOMI comprehensive investigation:
#    - Elena: OSINT gathering
#    - Marcus: Financial forensics
#    - Adrian: Legal analysis
#    - Maya: Data correlation
#    - Sofia: Market context
#    - Damian: Critical review
#    - Lucas: Final report synthesis
# 4. WYGENERUJE profesjonalny raport śledczy
```

### 🆕 Scenariusz 5: OSINT Only

```bash
# Chcesz tylko OSINT bez pełnego dochodzenia
# System wykryje treści investigative i użyje tylko Eleny
python destiny_auto.py ~/OSINT/target_research

# Wykryje: słowa kluczowe OSINT, intelligence
# Routing: investigative_type = 'osint'
# Agent: Elena Volkov (OSINT Specialist)
```

---

## 📊 Raport końcowy

System generuje raport w formacie JSON:

```json
{
  "case_id": "case_20241105_103000",
  "folder": "/path/to/documents",
  "summary": {
    "total_files": 15,
    "files_by_type": {
      "pdf": 5,
      "excel": 3,
      "text": 7
    },
    "total_tasks": 3,
    "successful_agents": 8
  },
  "findings": [
    {
      "agent": "financial",
      "category": "financial",
      "output": "Q4 revenue increased 25% YoY...",
      "confidence": 0.95
    }
  ]
}
```

**Lokalizacja:** `reports/autonomous_{case_id}.json`

---

## 🔍 INVESTIGATIVE INTEGRATION - Jak to działa?

### Automatyczna Detekcja

System używa **inteligentnego scoringu** do wykrywania treści investigative:

```python
# 1. SKANOWANIE ZAWARTOŚCI
Parser → Ekstrakcja tekstu z PDF/DOCX
↓
Content Analysis (pierwsze 1000 znaków)

# 2. SCORING
Investigative Keywords:
  🇬🇧 investigation, osint, intelligence, fraud, corruption, scandal
  🇵🇱 cba, prokuratura, śledztwo, postępowanie, afera
  
Każde dopasowanie: +3 punkty
3+ dopasowania: +20 punktów BONUS
  
# 3. KLASYFIKACJA
Score >= 5: investigative category
Score >= 3 + financial: financial investigation
Score >= 3 + legal: legal investigation
```

### Automatyczny Routing

```python
# 1. BASIC AGENTS (domyślnie)
financial documents → financial + data_science agents
legal documents → legal + risk agents
technical documents → architect + developer agents

# 2. INVESTIGATIVE TEAM (automatycznie gdy wykryje)
investigative content → AnalyticalTeam.investigate()
  ↓
  investigation_type determination:
    - 'comprehensive' → All 7 phases (Viktor → Elena → Marcus → Adrian → Maya → Damian → Lucas)
    - 'osint' → Elena only (OSINT gathering)
    - 'financial' → Marcus only (Financial forensics)
    - 'legal' → Adrian only (Legal research)
```

### Workflow Integracji

```
┌─────────────────────────────────────────────────────────────┐
│  User: python destiny_auto.py /investigation_docs          │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
         ┌──────────────────────┐
         │ DocumentScanner      │
         │ (scan all files)     │
         └──────────┬───────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │ IntelligentClassifier│
         │ (parse + analyze)    │
         └──────────┬───────────┘
                    │
                    ▼
         ┌──────────────────────┐
         │ DECISION POINT       │
         │ Is investigative?    │
         └──────────┬───────────┘
                    │
       ┌────────────┴────────────┐
       │                         │
       ▼                         ▼
   ❌ NO                      ✅ YES
   │                            │
   ▼                            ▼
┌────────────┐         ┌─────────────────┐
│Basic Agents│         │Investigative    │
│(6 agents)  │         │Team (9 agents)  │
└────────────┘         └─────────────────┘
   │                            │
   └────────────┬───────────────┘
                │
                ▼
    ┌───────────────────────┐
    │ Final Report          │
    │ (JSON + Summary)      │
    └───────────────────────┘
```

### Przykład: Auto-Detection w Akcji

```bash
# Folder zawiera:
# - fraud_report_2024.pdf (zawiera: "investigation", "fraud", "corruption")
# - witness_testimony.docx (zawiera: "witness", "evidence", "testimony")
# - CBA_raport.pdf (zawiera: "CBA", "prokuratura", "śledztwo")

python destiny_auto.py /cases/fraud_2024

OUTPUT:
🔍 Scanning folder: /cases/fraud_2024
📄 Found 3 files (2.5 MB)

🧠 Classifying files...
   fraud_report_2024.pdf: investigative (confidence: 1.00)
   witness_testimony.docx: investigative (confidence: 0.95)
   CBA_raport.pdf: investigative (confidence: 1.00)

📋 Generating tasks...
   Generated 1 tasks

📌 Task 1/1: INVESTIGATIVE (Priority: 85)
   Agents: investigative
   Files: 3
   🔍 Routing to Investigative Team (Type: comprehensive)
   
   📋 Preparing investigation: Case fraud_2024
   📂 Analyzing 3 documents
   🚀 Launching comprehensive investigation...
   
🔍 LAUNCHING INVESTIGATION: Case fraud_2024
   Type: comprehensive
   Priority: high
============================================================

🔄 Executing task: Plan investigation: Case fraud_2024
   Agent: Viktor Kovalenko
✅ Task completed: Plan investigation...

🔄 Executing task: OSINT investigation: Case fraud_2024
   Agent: Elena Volkov
✅ Task completed: OSINT investigation...

🔄 Executing task: Financial analysis: Case fraud_2024
   Agent: Marcus Chen
✅ Task completed: Financial analysis...

... (more phases)

✅ Investigation complete (125.3s)
📊 7 analysis phases completed

✅ ANALYSIS COMPLETE (130.5s)
```

---

## 🔧 Architektura Systemu

```
┌─────────────────────────────────────────────────────────┐
│                    destiny_auto.py                      │
│                     (User CLI)                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│          AutonomousOrchestrator                         │
│  - Główny kontroler                                     │
│  - Koordynuje cały proces                               │
└────┬─────────────┬──────────────┬──────────────────────┘
     │             │              │
     ▼             ▼              ▼
┌──────────┐  ┌─────────┐  ┌──────────────┐
│Document  │  │File     │  │Task          │
│Scanner   │  │Classifier│  │Generator     │
└──────────┘  └─────────┘  └──────────────┘
     │             │              │
     └─────────────┴──────────────┘
                   │
                   ▼
          ┌────────────────┐
          │  Agent Pool    │
          │  - Financial   │
          │  - Legal       │
          │  - Data Sci    │
          │  - etc.        │
          └────────┬───────┘
                   │
                   ▼
          ┌────────────────┐
          │  Tool Registry │
          │  - Extraction  │
          │  - Analysis    │
          │  - Search      │
          └────────┬───────┘
                   │
                   ▼
          ┌────────────────┐
          │  Databases     │
          │  - PostgreSQL  │
          │  - Qdrant      │
          │  - Elastic     │
          │  - Neo4j       │
          └────────────────┘
```

---

## ⚙️ Konfiguracja

System używa tych samych ustawień z `.env`:

```bash
# LMStudio (lokalny LLM)
LMSTUDIO_BASE_URL=http://192.168.200.226:1234/v1
LMSTUDIO_LLM_MODEL=openai/gpt-oss-20b

# Bazy danych
POSTGRES_HOST=localhost
QDRANT_HOST=localhost
ELASTICSEARCH_HOST=localhost
NEO4J_HOST=localhost

# Claude nadzór (opcjonalny)
ANTHROPIC_API_KEY=your_key
ENABLE_CLAUDE_SUPERVISION=false
```

---

## 🎓 Zaawansowane

### Programmatic API

```python
from src.autonomous.autonomous_orchestrator import AutonomousOrchestrator

# Stwórz orchestrator
orchestrator = AutonomousOrchestrator()

# Przetwórz folder
results = orchestrator.process_folder(
    "/path/to/folder",
    case_id="my_case"
)

# Wyniki
print(f"Processed {results['summary']['total_files']} files")
for finding in results['findings']:
    print(f"{finding['agent']}: {finding['output']}")
```

### Custom Tools

```python
from src.autonomous.tool_registry import get_tool_registry, Tool

registry = get_tool_registry()

# Dodaj własne narzędzie
registry.register_tool(Tool(
    name="custom_analyzer",
    description="My custom analysis",
    category="analysis",
    input_types=["text"],
    output_type="analysis",
    function=my_function,
    examples=["Analyze sentiment"]
))
```

---

## 🚀 Next Steps

1. **Uruchom pierwszy test:**
   ```bash
   python destiny_auto.py ./demo_documents
   ```

2. **Sprawdź raport:**
   ```bash
   cat reports/autonomous_*.json | jq .
   ```

3. **Rozbuduj system:**
   - Dodaj własne narzędzia
   - Stwórz własnych agentów
   - Dodaj nowe typy klasyfikacji

---

## 💡 Tips & Tricks

**Tip 1: Organizuj pliki**
```
case_001/
  ├── financial/
  ├── legal/
  └── technical/
```
System automatycznie wykryje strukturę.

**Tip 2: Nazwy plików**
Używaj opisowych nazw - system je analizuje:
- ✅ `Q4_2023_Revenue_Report.pdf`
- ❌ `document.pdf`

**Tip 3: Batch processing**
```bash
# Przetwarzaj wiele przypadków
for case in cases/*/; do
    python destiny_auto.py "$case"
done
```

---

## ❓ FAQ

**Q: Czy muszę ręcznie wybierać agentów?**  
A: NIE! System automatycznie wybiera najlepszych agentów dla każdego typu dokumentu.

**Q: Co jeśli mam mieszane typy dokumentów?**  
A: System sklasyfikuje każdy plik osobno i użyje odpowiednich agentów.

**Q: Czy mogę dodać własne typy plików?**  
A: TAK! Rozbuduj `DocumentScanner.SUPPORTED_EXTENSIONS`.

**Q: Czy działa offline?**  
A: TAK! (z lokalnym LMStudio, bez Claude supervision)

---

## 🎉 Bottom Line

```
PRZED:
  1. Przeczytaj dokumenty
  2. Zdecyduj co zrobić
  3. Wybierz agentów
  4. Uruchom analizę
  5. Zbierz wyniki
  
TERAZ:
  python destiny_auto.py /folder
  
  DONE! ✅
```

**System robi wszystko za Ciebie! 🚀**
