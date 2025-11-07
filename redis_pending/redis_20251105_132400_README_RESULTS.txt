SET doc:README_RESULTS:title "📊 Results Storage - README"
SET doc:README_RESULTS:type "architecture"
SET doc:README_RESULTS:path "README_RESULTS.md"
SET doc:README_RESULTS:content "# 📊 Results Storage - README

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
python case_cli.py list"
EXPIRE doc:README_RESULTS:content 86400
SADD docs:all "README_RESULTS"
SADD docs:type:architecture "README_RESULTS"