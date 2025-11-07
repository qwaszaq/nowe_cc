# 🧪 Instrukcje Testowania Systemu

## 📁 Folder Testowy: `testdocsLLM/`

Folder jest już przygotowany i dodany do `.gitignore`.

---

## 🚀 Jak Przetestować System

### Krok 1: Dodaj Pliki Testowe

Wrzuć swoje dokumenty do folderu `testdocsLLM/`:

```bash
# Przykład:
testdocsLLM/
  ├── raport_finansowy_Q4.pdf
  ├── bilans_2023.xlsx
  ├── umowa_serwisowa.txt
  └── specyfikacja_techniczna.md
```

**Obsługiwane formaty:**
- 📄 Dokumenty: `.pdf`, `.docx`, `.doc`, `.txt`, `.md`
- 📊 Dane: `.xlsx`, `.xls`, `.csv`
- 📋 Strukturalne: `.json`, `.xml`, `.yaml`
- 🖼️ Obrazy: `.png`, `.jpg`, `.jpeg`, `.tiff`

---

### Krok 2: Uruchom Test

#### **Podstawowy test:**
```bash
python destiny_auto.py testdocsLLM
```

#### **Z własnym Case ID:**
```bash
python destiny_auto.py testdocsLLM --case-id moj_test_001
```

#### **Z verbose mode:**
```bash
python destiny_auto.py testdocsLLM --verbose
```

---

### Krok 3: Zobacz Wyniki

System wygeneruje raport w:
```
reports/autonomous_case_YYYYMMDD_HHMMSS.json
```

**Zobacz raport:**
```bash
# Ostatni raport
ls -lt reports/ | head -2

# Wyświetl JSON
cat reports/autonomous_*.json | jq .

# Lub po prostu otwórz
open reports/
```

---

## 🧪 Testy Dostępne

### Test 1: Autonomous System (Podstawowy)
```bash
python test_autonomous_lmstudio.py
```

**Co testuje:**
- Połączenie z LMStudio
- Automatyczne klasyfikowanie plików
- Wybór agentów
- Generowanie zadań
- Faktyczne wywołania LLM
- Token usage i savings

**Oczekiwany output:**
```
✅ LMStudio connected
📁 Found 3 files
🤖 Processing with RAG+CAG...
✅ Complete (2.3s)
   Tokens used: 1,250
   Tokens saved by CAG: 450
🎉 SUCCESS! System is using REAL LMStudio!
```

---

### Test 2: RAG+CAG Optimization
```bash
python test_rag_cag_lmstudio.py
```

**Co testuje:**
- Prostę wywołanie LMStudio
- RAG+CAG optimization
- Token savings calculation
- Context window efficiency

**Oczekiwany output:**
```
✅ LMStudio is online
📊 WITHOUT CAG: 30,000 tokens wasted
📊 WITH CAG: 27,000 tokens saved
🚀 44k context → Feels like 71,000 tokens!
IMPROVEMENT: 90% more efficient!
```

---

### Test 3: Database Integration
```bash
python tests/integration/test_database_integration.py
```

**Co testuje:**
- Połączenia do wszystkich 5 baz danych
- Generowanie embeddings
- Storage i retrieval
- Semantic search
- Smart routing

---

## 📊 Przykładowe Scenariusze

### Scenariusz 1: Dokumenty Finansowe

**Pliki:**
```
testdocsLLM/
  ├── Q4_2023_Revenue.pdf
  ├── Balance_Sheet.xlsx
  └── Financial_Summary.txt
```

**Uruchom:**
```bash
python destiny_auto.py testdocsLLM --case-id financial_test
```

**System wykona:**
1. Sklasyfikuje jako "financial"
2. Wybierze agentów: `financial`, `data_science`
3. Przeprowadzi analizy: `financial_analysis`, `trend_analysis`, `data_extraction`
4. Użyje RAG+CAG dla optymalizacji
5. Wygeneruje raport z kluczowymi metrykami

---

### Scenariusz 2: Mix Dokumentów

**Pliki:**
```
testdocsLLM/
  ├── financial_report.pdf      (financial)
  ├── service_contract.pdf      (legal)
  ├── architecture_spec.md      (technical)
  └── market_data.csv           (data)
```

**Uruchom:**
```bash
python destiny_auto.py testdocsLLM --case-id mixed_test
```

**System wykona:**
1. Sklasyfikuje każdy plik osobno
2. Wygeneruje 4 oddzielne zadania
3. Użyje różnych agentów dla każdej kategorii
4. Przeprowadzi analizy równolegle (jeśli możliwe)
5. Zsyntetyzuje wyniki w jeden raport

---

### Scenariusz 3: Duży Zbiór Danych

**Pliki:**
```
testdocsLLM/
  ├── doc_001.txt
  ├── doc_002.txt
  ├── doc_003.txt
  ... (wiele plików)
  └── doc_100.txt
```

**Uruchom:**
```bash
python destiny_auto.py testdocsLLM --case-id large_batch_test
```

**System wykona:**
1. Przeanalizuje wszystkie pliki
2. Użyje RAG+CAG dla efektywności
3. Przetworzy w optymalnych batch'ach
4. Pokaże token savings (duże!)
5. Wygeneruje comprehensive report

---

## 🔍 Weryfikacja Rezultatów

### Sprawdź Status Połączenia

```bash
# Health check wszystkich komponentów
python health_check.py
```

**Powinieneś zobaczyć:**
```
✅ LMStudio: Connected
✅ PostgreSQL: Connected
✅ Embeddings: Available
✅ Configuration: Valid
```

---

### Sprawdź Logi

```bash
# Zobacz ostatnie logi
tail -50 logs/destiny.log

# Lub filtruj po LMStudio
grep "LMStudio" logs/destiny.log
```

---

### Sprawdź Bazy Danych

```bash
# PostgreSQL - zobacz zapisane embeddings
psql -h localhost -U destiny -d destiny_analytical -c "SELECT COUNT(*) FROM document_embeddings;"

# Qdrant - zobacz collections
curl http://localhost:6333/collections

# Elasticsearch - zobacz dokumenty
curl http://localhost:9200/destiny_documents/_count
```

---

## ⚠️ Troubleshooting

### Problem: LMStudio Not Connected

**Objawy:**
```
⚠️ LMStudio not responding (will use fallback)
```

**Rozwiązanie:**
1. Sprawdź czy LMStudio działa:
   ```bash
   curl http://192.168.200.226:1234/v1/models
   ```

2. Sprawdź czy model jest załadowany:
   ```bash
   # Powinien pokazać gpt-oss-20b
   ```

3. Sprawdź network:
   ```bash
   ping 192.168.200.226
   ```

---

### Problem: No Embeddings Generated

**Objawy:**
```
❌ Error generating embeddings
```

**Rozwiązanie:**
1. Test embedding models:
   ```bash
   python test_lmstudio_simple.py
   ```

2. Sprawdź czy modele są dostępne:
   - `text-embedding-multilingual-e5-large-instruct`
   - `jina-embeddings-v4-text-retrieval`

---

### Problem: Database Connection Failed

**Objawy:**
```
❌ PostgreSQL connection failed
```

**Rozwiązanie:**
1. Uruchom setup:
   ```bash
   ./scripts/init_all_databases.sh
   ```

2. Sprawdź status:
   ```bash
   docker-compose ps
   ```

---

## 📈 Metryki do Obserwacji

### 1. Token Usage
```
Tokens used: 1,250
Tokens saved by CAG: 450
Savings: 36%
```

### 2. Performance
```
Processing time: 2.3s
Effective window: 47,000 tokens (vs 44,000 physical)
```

### 3. Quality
```
Confidence: 94%
Findings: 5 key insights
```

---

## 💡 Tips

**Tip 1: Zacznij od małych testów**
```bash
# Najpierw 1-3 pliki
# Potem zwiększaj
```

**Tip 2: Użyj verbose mode do debugowania**
```bash
python destiny_auto.py testdocsLLM --verbose
```

**Tip 3: Sprawdź raporty po każdym teście**
```bash
cat reports/autonomous_*.json | jq '.findings'
```

**Tip 4: Monitoruj token usage**
```bash
# Zobacz czy CAG działa
grep "tokens_saved" reports/autonomous_*.json
```

---

## ✅ Checklist Przed Testem

```
PRE-TEST:
  [ ] LMStudio running (192.168.200.226:1234)
  [ ] Model loaded (gpt-oss-20b)
  [ ] Embedding models available
  [ ] Databases running (docker-compose ps)
  [ ] Test files in testdocsLLM/

DURING TEST:
  [ ] Zobacz "LMStudio connected"
  [ ] Zobacz "Processing with RAG+CAG"
  [ ] Zobacz token usage
  [ ] Zobacz CAG savings

POST-TEST:
  [ ] Sprawdź report JSON
  [ ] Sprawdź findings
  [ ] Sprawdź metryki
  [ ] Sprawdź czy pliki w DB
```

---

## 🎉 Sukces!

**Jeśli zobaczysz:**
```
✅ LMStudio connected
✅ Processing with RAG+CAG
✅ Tokens saved by CAG: XXX
✅ ANALYSIS COMPLETE
🎉 SUCCESS! System is using REAL LMStudio!
```

**TO ZNACZY ŻE WSZYSTKO DZIAŁA!** 🚀

---

**Powodzenia z testami!** 
Wrzuć swoje pliki do `testdocsLLM/` i daj znać jak poszło! 😊
