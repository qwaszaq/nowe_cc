# Add multi-year PDF analysis plan + Phase 1 enhanced prompts

**Auto-Generated Documentation**

**Date:** 2025-11-07 07:10:31
**Commit:** `71fe32a`
**Type:** Documentation
**Author:** artur

---

## 📝 Commit Message

**docs: Add multi-year PDF analysis plan + Phase 1 enhanced prompts**

MULTI_YEAR_PDF_ANALYSIS_PLAN.md:
- Comprehensive baseline testing before Phase 1 implementation
- Download 3 years of Azoty annual reports (2022, 2023, 2024)
- Test all 3 systems (Single-Agent, Multi-Agent, Claude) on full PDFs
- Compare data extraction, RAG quality, severity calibration, narrative analysis
- Gap analysis → prioritized improvement roadmap
- Timeline: 2-3 weeks (acquisition + analysis + comparison)

local_llm_prompts_v2.py (Phase 1 Enhanced Prompts - ready for testing):
- Framework decision tree (credit vs equity analysis)
- Explicit severity calibration scales (0-100 with thresholds)
- Few-shot examples with correct calibration
- Chain-of-thought reasoning templates
- Mandatory probability quantification
- Target: 75% → 80% quality match with Claude

Strategy: Establish comprehensive baseline first, then implement targeted improvements based on actual gaps identified from multi-year PDF analysis


## 📁 Files Changed

**Total:** 2 file(s)

### Python Files (1)

- `src/intelligence/prompts/local_llm_prompts_v2.py`


### Documentation Files (1)

- `MULTI_YEAR_PDF_ANALYSIS_PLAN.md`


## 📊 Statistics

```
71fe32a docs: Add multi-year PDF analysis plan + Phase 1 enhanced prompts
 MULTI_YEAR_PDF_ANALYSIS_PLAN.md                  |  539 +++++++++++
 src/intelligence/prompts/local_llm_prompts_v2.py | 1033 ++++++++++++++++++++++
 2 files changed, 1572 insertions(+)
```

## 🤖 Metadata

```json
{
  "commit_hash": "71fe32ad484a3c7cb65ed6e0a0cc772cbe187cbc",
  "commit_type": "documentation",
  "timestamp": 1762495831,
  "files_changed": [
    "MULTI_YEAR_PDF_ANALYSIS_PLAN.md",
    "src/intelligence/prompts/local_llm_prompts_v2.py"
  ],
  "auto_generated": true
}
```

---
*This document was automatically generated from a git commit.*
*Helena will process this and add to all 4 databases (PostgreSQL, Neo4j, Qdrant, Redis).*