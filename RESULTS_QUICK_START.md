# 🚀 Results Storage - Quick Start Guide

**Welcome!** This guide shows you how to use the new results storage system.

---

## 📋 What's New?

### **Before:**
```
reports/
  ├── autonomous_case_001.json
  ├── autonomous_case_002.json
  └── ... (flat structure)
```

### **After:**
```
cases/
  ├── case_001/
  │   ├── metadata.json
  │   ├── input/
  │   ├── results/
  │   ├── audit/
  │   └── archives/
  ├── case_002/
  └── index.json (fast lookup)
```

**Benefits:**
- ✅ Organized by case
- ✅ Multiple report formats (JSON, MD, HTML)
- ✅ Complete audit trail
- ✅ Easy to search and query
- ✅ Scalable to 1000s of cases

---

## 🎯 Quick Start (5 minutes)

### **Step 1: Migrate Existing Results**

```bash
# One-time migration
python migrate_existing_results.py
```

This moves your existing `reports/autonomous_*.json` to the new `cases/` structure.

---

### **Step 2: Run New Analysis**

```bash
# Run autonomous analysis (automatically uses new structure)
python destiny_auto.py testdocsLLM/ --case-id my_new_case

# Results will be saved to:
# cases/my_new_case/results/
```

---

### **Step 3: Explore Results**

```bash
# List all cases
python case_cli.py list

# Show case details
python case_cli.py show my_new_case

# Get report in different formats
python case_cli.py report my_new_case --format md -o report.md
python case_cli.py report my_new_case --format html -o report.html

# Search cases
python case_cli.py search "CBA"

# Show statistics
python case_cli.py stats --detailed
```

---

## 📊 Common Tasks

### **View Latest Results**

```bash
# Show last 10 cases
python case_cli.py list --limit 10

# Show completed cases only
python case_cli.py list --status complete
```

### **Export Report**

```bash
# Get Markdown report
python case_cli.py report cba_analysis_2024 --format md -o ~/Desktop/report.md

# Get HTML report (viewable in browser)
python case_cli.py report cba_analysis_2024 --format html -o ~/Desktop/report.html
```

### **Find Specific Case**

```bash
# Search by name
python case_cli.py search "cba"

# Show full details with findings
python case_cli.py show cba_analysis_2024 --report
```

### **Archive Old Cases**

```bash
# Archive a case (creates timestamped snapshot)
python case_cli.py archive old_case_001 --yes
```

---

## 🎨 Report Formats

### **JSON Format** (machine-readable)
```json
{
  "case_id": "cba_analysis_2024",
  "timestamp": "2024-11-05T13:08:03",
  "summary": {...},
  "findings": [...]
}
```

### **Markdown Format** (human-readable)
```markdown
# Case Analysis Report: cba_analysis_2024

**Date:** 2024-11-05T13:08:03

## Summary
- Total Files: 14
- Total Size: 17.2 MB
...
```

### **HTML Format** (web view)
Beautiful formatted report you can open in your browser!

---

## 🗂️ Case Directory Structure

```
cases/cba_analysis_2024/
├── metadata.json              # Case info
├── input/                     # Original documents
│   ├── documents/
│   ├── manifest.json
│   └── checksums.txt
├── processing/                # Intermediate files
│   ├── extracted/
│   ├── embeddings/
│   ├── classifications/
│   └── tasks/
├── results/                   # 📊 FINAL OUTPUTS
│   ├── final_report.json     # Complete analysis
│   ├── final_report.md       # Markdown version
│   ├── final_report.html     # HTML version
│   ├── agents/               # Per-agent results
│   │   ├── legal_analysis.json
│   │   ├── financial_analysis.json
│   │   └── risk_assessment.json
│   └── visualizations/       # Charts (future)
├── audit/                     # Execution logs
│   ├── execution_log.json
│   ├── agent_traces.jsonl
│   └── performance_metrics.json
└── archives/                  # Historical snapshots
    └── 20241105_130803/
```

---

## 🔍 Advanced Queries

### **Python API**

```python
from src.storage.case_manager import CaseManager

manager = CaseManager()

# Get case info
case = manager.get_case("cba_analysis_2024")
print(f"Status: {case['status']}")

# List recent cases
recent = manager.list_cases(limit=10)
for case in recent:
    print(f"{case['case_id']}: {case['total_files']} files")

# Search
results = manager.search_cases("CBA")
print(f"Found {len(results)} matching cases")

# Get report
report = manager.get_case_report("cba_analysis_2024", format="json")
data = json.loads(report)
```

### **Direct File Access**

```python
from pathlib import Path
import json

# Access case directly
case_dir = Path("cases/cba_analysis_2024")

# Read report
report = json.loads(
    (case_dir / "results" / "final_report.json").read_text()
)

# Read agent result
legal_analysis = json.loads(
    (case_dir / "results" / "agents" / "legal_analysis.json").read_text()
)
```

---

## 📈 Database Integration (Future)

The system is designed to work with multiple databases:

- **PostgreSQL** - Structured data & fast queries
- **Qdrant** - Vector similarity search
- **Elasticsearch** - Full-text search
- **Neo4j** - Relationship graph
- **Redis** - Hot cache

Currently, only **file system** storage is active. Database integration coming in Phase 2!

---

## 🔄 Migration Notes

### **What Gets Migrated**

- ✅ All `reports/autonomous_*.json` files
- ✅ Case metadata extracted from reports
- ✅ Final reports in JSON/MD/HTML
- ✅ Individual agent results

### **What Stays**

- ✅ Original `reports/` files (not deleted)
- ✅ Can keep both old and new structure during transition

### **What's New**

- ✅ Organized case directories
- ✅ Multiple report formats
- ✅ Audit trail structure (ready for future use)

---

## 🎓 Tips & Best Practices

### **Case IDs**

Use descriptive case IDs:
```bash
# Good
--case-id cba_reports_2024
--case-id financial_audit_q4
--case-id due_diligence_companyX

# Avoid
--case-id case1
--case-id test
--case-id untitled
```

### **Regular Archival**

Archive completed cases monthly:
```bash
# Archive old cases
python case_cli.py archive old_case_001 --yes
python case_cli.py archive old_case_002 --yes
```

### **Quick Stats**

Check system health weekly:
```bash
python case_cli.py stats --detailed
```

---

## 🐛 Troubleshooting

### **"Case not found"**

```bash
# List all cases to find correct case_id
python case_cli.py list

# Search by partial name
python case_cli.py search "part_of_name"
```

### **"Report not found"**

Case might not be complete yet:
```bash
# Check case status
python case_cli.py show <case_id>

# Status should be "complete"
```

### **Migration Issues**

```bash
# Re-run migration (skips existing cases)
python migrate_existing_results.py

# Check what was migrated
python case_cli.py list
```

---

## 📚 Next Steps

1. **Migrate existing results** (one-time)
   ```bash
   python migrate_existing_results.py
   ```

2. **Explore your cases**
   ```bash
   python case_cli.py list
   python case_cli.py show <case_id>
   ```

3. **Run new analysis**
   ```bash
   python destiny_auto.py /path/to/documents --case-id my_case
   ```

4. **Export reports**
   ```bash
   python case_cli.py report my_case --format html -o report.html
   ```

---

## 💡 Quick Reference

```bash
# Most used commands
python case_cli.py list                    # Show all cases
python case_cli.py show <id>               # Case details
python case_cli.py search <query>          # Find cases
python case_cli.py report <id> -o out.md   # Export report
python case_cli.py stats                   # Statistics

# Run analysis with new structure
python destiny_auto.py /folder --case-id my_case

# Migrate old reports
python migrate_existing_results.py
```

---

## 🎉 You're Ready!

The new results storage system is designed to be:
- **Simple** - Easy to use, intuitive structure
- **Powerful** - Multiple formats, fast search
- **Scalable** - Handles 1000s of cases
- **Future-proof** - Ready for database integration

**Questions?** See `RESULTS_STORAGE_ARCHITECTURE.md` for technical details.
