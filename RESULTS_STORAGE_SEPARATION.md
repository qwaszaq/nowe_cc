# 🔀 Results Storage - Investigation vs Development

**CRITICAL:** System ma DWA całkowicie oddzielne środowiska!

---

## 📊 Podział Środowisk

### **🔬 INVESTIGATION (Production)**
```
Purpose:  Real investigation data analysis
Data:     SMS messages (143K vectors), OSINT data
Access:   READ-ONLY ⚠️
Databases: sms-*, hercules-*
```

### **🧪 DEVELOPMENT (Testing)**
```
Purpose:  Framework development, testing
Data:     CBA reports, test documents
Access:   FULL (read/write/delete)
Databases: destiny-*
```

---

## 🗺️ Mapa Kompletna

```
┌─────────────────────────────────────────────────────────────────┐
│                     DESTINY SYSTEM                              │
└─────────────────────────────────────────────────────────────────┘
           │                            │
           ▼                            ▼
┌──────────────────────┐    ┌──────────────────────┐
│   INVESTIGATION      │    │   DEVELOPMENT        │
│   (Production)       │    │   (Testing)          │
└──────────────────────┘    └──────────────────────┘
           │                            │
           ▼                            ▼
┌──────────────────────┐    ┌──────────────────────┐
│  READ-ONLY QUERIES   │    │  AUTONOMOUS ANALYSIS │
│  - SMS analysis      │    │  - CBA reports       │
│  - OSINT research    │    │  - Testing           │
│  - Pattern learning  │    │  - Development       │
└──────────────────────┘    └──────────────────────┘
           │                            │
           ▼                            ▼
┌──────────────────────┐    ┌──────────────────────┐
│  DATABASES           │    │  DATABASES           │
│  • sms-postgres      │    │  • destiny-postgres  │
│    (port 5432)       │    │    (port 5435)       │
│  • sms-qdrant        │    │  • destiny-qdrant    │
│    (port 6333)       │    │    (port 6335)       │
│  • sms-neo4j         │    │  • destiny-neo4j     │
│    (port 7474)       │    │    (port 7475)       │
│  • hercules-*        │    │  • destiny-*         │
└──────────────────────┘    └──────────────────────┘
           │                            │
           ▼                            ▼
┌──────────────────────┐    ┌──────────────────────┐
│  RESULTS STORAGE     │    │  RESULTS STORAGE     │
│  investigations/     │    │  cases/              │
│  (existing)          │    │  (NEW!)              │
└──────────────────────┘    └──────────────────────┘
```

---

## 🗂️ Struktura Katalogów

### **INVESTIGATION Results** (Existing)

```
investigations/
├── external/              # External OSINT data
│   ├── grupa_azoty_reports/
│   ├── court_cases/
│   └── public_records/
├── sms_analysis/          # SMS investigation results
│   ├── queries/
│   ├── patterns/
│   └── reports/
└── hercules_data/         # OSINT analysis
    ├── scrapes/
    ├── enriched/
    └── insights/
```

**Charakterystyka:**
- ✅ Read-only analysis results
- ✅ Real production data insights
- ✅ Already existing structure
- ⚠️ **NEVER** modify source databases

### **DEVELOPMENT Results** (NEW System)

```
cases/                     # NEW: Autonomous analysis results
├── {case_id}/
│   ├── metadata.json
│   ├── input/
│   ├── processing/
│   ├── results/
│   │   ├── final_report.json
│   │   ├── final_report.md
│   │   ├── final_report.html
│   │   └── agents/
│   ├── audit/
│   └── archives/
└── index.json

reports/                   # LEGACY: Flat reports (keep for compatibility)
└── autonomous_*.json
```

**Charakterystyka:**
- ✅ Full read/write access
- ✅ Test data (CBA reports, samples)
- ✅ Framework development
- ✅ Can experiment freely

---

## 🎯 Co Gdzie Przechowywać?

### **INVESTIGATION Results → `investigations/`**

**Use for:**
```bash
# Query results from SMS/OSINT databases
# Pattern discovery
# Research insights
# Real investigation findings
```

**Examples:**
```
investigations/sms_analysis/
├── query_results/
│   └── suspicious_patterns_2024.json
├── network_analysis/
│   └── entity_connections.json
└── reports/
    └── weekly_insights_2024-11.md
```

**Access:**
```python
# Read-only queries
from investigation_client import InvestigationDB

db = InvestigationDB(read_only=True)
results = db.query("SELECT * FROM sms_messages WHERE ...")
results.save_to("investigations/sms_analysis/query_results/")
```

---

### **DEVELOPMENT Results → `cases/`**

**Use for:**
```bash
# Autonomous system analysis
# CBA reports processing
# Framework testing
# Agent performance evaluation
```

**Examples:**
```
cases/
├── cba_analysis_2024/
│   └── results/
│       ├── final_report.json
│       └── agents/
│           ├── legal_analysis.json
│           └── risk_assessment.json
├── test_batch_001/
└── performance_benchmark/
```

**Access:**
```python
# Full access
from src.storage.case_manager import CaseManager

manager = CaseManager()
case_dir = manager.create_case("my_test_case", "/data")
# ... run analysis ...
manager.save_final_report("my_test_case", results)
```

---

## 🔐 Access Control Matrix

| Environment | Read | Write | Delete | Schema Changes | Data Source |
|-------------|------|-------|--------|----------------|-------------|
| **Investigation** | ✅ | ❌ | ❌ | ❌ | SMS, OSINT (real) |
| **Development** | ✅ | ✅ | ✅ | ✅ | CBA, tests (synthetic) |

---

## 🚀 Usage Examples

### **Scenario 1: Investigation Analysis**

```bash
# ❌ WRONG (would use development DBs)
python destiny_auto.py /investigation_data --case-id sms_analysis

# ✅ CORRECT (use investigation tools)
python query_investigation.py --query "suspicious_patterns" \
    --output investigations/sms_analysis/query_001.json
```

### **Scenario 2: Development Testing**

```bash
# ✅ CORRECT (uses development DBs)
python destiny_auto.py testdocsLLM/ --case-id cba_test_2024

# Results → cases/cba_test_2024/
```

### **Scenario 3: Learning from Investigation**

```python
# Read investigation results (read-only)
investigation_results = load_investigation_data("investigations/sms_analysis/")

# Train/test on development
manager = CaseManager()
case_dir = manager.create_case("learning_test", "/test_data")
# ... run analysis with learned patterns ...
```

---

## 📦 Migracja i Nowy Design

### **Co zaprojektowałem dzisiaj:**

System zarządzania wynikami dla **DEVELOPMENT**:
- `cases/` - structured case storage
- `case_cli.py` - command-line interface
- `CaseManager` - Python API
- Multiple report formats (JSON/MD/HTML)

### **Co już istnieje:**

Investigation results structure:
- `investigations/` - read-only analysis results
- Existing query tools
- OSINT data management

### **Co NIE zmieniamy:**

✅ `investigations/` - pozostaje jak jest  
✅ Investigation databases - READ-ONLY  
✅ Existing tools - działają dalej

---

## 🎨 Complete Picture

```
PROJECT ROOT
│
├── 🔬 INVESTIGATION (Production)
│   ├── .env.investigation          # Config
│   ├── investigations/             # Results
│   │   ├── sms_analysis/
│   │   ├── external/
│   │   └── hercules_data/
│   ├── Docker:
│   │   ├── sms-postgres (5432)    # READ-ONLY
│   │   ├── sms-qdrant (6333)      # READ-ONLY
│   │   ├── sms-neo4j (7474)       # READ-ONLY
│   │   └── hercules-* (various)   # READ-ONLY
│   └── Tools:
│       ├── query_investigation.py
│       └── investigation_client.py
│
└── 🧪 DEVELOPMENT (Testing)
    ├── .env.development            # Config
    ├── .env (main, points to dev)  # Active
    ├── cases/                      # Results (NEW!)
    │   ├── {case_id}/
    │   └── index.json
    ├── reports/                    # Legacy
    ├── Docker:
    │   ├── destiny-postgres (5435) # FULL ACCESS
    │   ├── destiny-qdrant (6335)   # FULL ACCESS
    │   ├── destiny-neo4j (7475)    # FULL ACCESS
    │   └── destiny-* (various)     # FULL ACCESS
    └── Tools:
        ├── destiny_auto.py         # Autonomous system
        ├── case_cli.py             # Case management
        └── src/storage/            # Storage API
```

---

## 🔄 Workflow Separation

### **Investigation Workflow:**

```
1. Query investigation DBs (read-only)
   ↓
2. Analyze patterns
   ↓
3. Save insights to investigations/
   ↓
4. Use findings for development learning
```

### **Development Workflow:**

```
1. Run autonomous analysis on test data
   ↓
2. Store results in cases/
   ↓
3. Evaluate performance
   ↓
4. Iterate and improve
   ↓
5. (Optional) Apply to investigation queries
```

---

## 💡 Key Takeaways

| Aspect | Investigation | Development |
|--------|--------------|-------------|
| **Purpose** | Real data analysis | Testing & development |
| **Data** | SMS (143K), OSINT | CBA reports, tests |
| **Access** | READ-ONLY ⚠️ | FULL ✅ |
| **Results** | `investigations/` | `cases/` (NEW) |
| **Databases** | sms-*, hercules-* | destiny-* |
| **Ports** | 5432, 6333, 7474 | 5435, 6335, 7475 |
| **Risk** | HIGH (production) | LOW (test data) |

---

## 🎯 Action Items

### **For Investigation:**
- ✅ Keep existing `investigations/` structure
- ✅ Continue using read-only queries
- ✅ No changes needed!

### **For Development:**
- ✅ Use new `cases/` structure (designed today)
- ✅ Migrate old `reports/` to `cases/` (optional)
- ✅ Use `case_cli.py` for management
- ✅ Run autonomous analysis freely

---

## 🚦 Decision Guide

**Ask yourself:**

**"Am I working with real SMS/OSINT data?"**
- YES → Use investigation tools, save to `investigations/`
- NO → Use autonomous system, save to `cases/`

**"Can I modify the database?"**
- NO → It's investigation, read-only queries
- YES → It's development, full access

**"Is this production data?"**
- YES → Investigation environment
- NO → Development environment

---

## 🎉 Summary

**Zaprojektowany dzisiaj system (`cases/`, `case_cli.py`, `CaseManager`):**
- ✅ Dla **DEVELOPMENT** (testing, CBA reports, framework dev)
- ✅ Używa **destiny-*** databases (ports 5435, 6335, 7475...)
- ✅ **FULL ACCESS** (read/write/delete)
- ✅ Bezpieczne do eksperymentów

**Istniejący system (`investigations/`):**
- ✅ Dla **INVESTIGATION** (real SMS/OSINT data)
- ✅ Używa **sms-***, **hercules-*** databases
- ✅ **READ-ONLY** (no modifications!)
- ⚠️ Production data - ostrożnie!

**OBA systemy działają równolegle, zero konfliktów!** 🎊
