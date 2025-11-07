# 📊 Results Storage - README

## 🎯 Quick Navigation

### **I'm working with...**

#### **🧪 Development / Testing (CBA reports, experiments)**
→ Read: `RESULTS_QUICK_START.md`  
→ CLI: `python case_cli.py --help`  
→ Use: `cases/` directory

#### **🔬 Investigation (SMS/OSINT, real data)**
→ Use: existing `investigations/` directory  
→ Tools: investigation query tools  
→ **READ-ONLY** access

#### **❓ Not sure which environment?**
→ Read: `RESULTS_STORAGE_SEPARATION.md`

---

## 📚 Documentation

| Document | Purpose | Audience |
|----------|---------|----------|
| **RESULTS_STORAGE_SEPARATION.md** | Environment guide (Investigation vs Development) | Everyone - START HERE |
| **RESULTS_QUICK_START.md** | Quick start for development results | Developers |
| **RESULTS_STORAGE_ARCHITECTURE.md** | Technical architecture (development) | Architects |
| **case_cli.py --help** | Command-line reference | Users |

---

## 🚀 Quick Commands

```bash
# Development environment
python case_cli.py list                    # List all cases
python case_cli.py show <case_id>          # Show case details
python destiny_auto.py /folder --case-id my_case  # Run analysis

# Investigation environment
# (use existing investigation tools)
```

---

## 🔀 Key Differences

| Aspect | Development | Investigation |
|--------|------------|---------------|
| **Data** | CBA reports, tests | SMS, OSINT (real) |
| **Access** | Full (read/write) | Read-only |
| **Storage** | `cases/` | `investigations/` |
| **DBs** | destiny-* | sms-*, hercules-* |
| **Risk** | Low (test data) | High (production) |

---

## 💡 Examples

### Development (Test Data)
```bash
# Analyze CBA reports
python destiny_auto.py testdocsLLM/ --case-id cba_test

# Results saved to: cases/cba_test/
```

### Investigation (Real Data)
```bash
# Query SMS database (read-only)
python query_investigation.py --query "pattern_analysis"

# Results saved to: investigations/sms_analysis/
```

---

**Start here:** `RESULTS_STORAGE_SEPARATION.md`
