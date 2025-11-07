# Download 6 Azoty annual reports for multi-year analysis (2022-2024)

**Auto-Generated Documentation**

**Date:** 2025-11-07 07:15:34
**Commit:** `fb8cb6f`
**Type:** Feature
**Author:** artur

---

## 📝 Commit Message

**feat: Download 6 Azoty annual reports for multi-year analysis (2022-2024)**

Phase 1 Complete: Data Acquisition ✅

Downloaded 6 PDF files (21.6M total):
- 2022: Consolidated Financial Statements (2.4M) + Directors Report (3.0M)
- 2023: Consolidated Financial Statements (2.5M) + Directors Report (4.0M)
- 2024: Consolidated Financial Statements (3.4M) + Directors Report (6.3M)

Files:
- scripts/download_azoty_reports.sh (download automation)
- data/documents/grupa_azoty/*.pdf (6 annual reports)

Next: Phase 2 - Extract multi-year financial data from PDFs
- Balance Sheet (2022-2024)
- Income Statement (2022-2024)
- Cash Flow (2022-2024)
- Combine into multi-year dataset
- Ingest into RAG system

Purpose: Establish comprehensive baseline for single-agent vs multi-agent vs Claude comparison on full annual reports (not just limited 2023 balance sheet data)


## 📁 Files Changed

**Total:** 36 file(s)

### Shell Files (1)

- `scripts/download_azoty_reports.sh`


### Documentation Files (9)

- `docs/auto-generated/2025-11-07/COMMIT_71fe32a_documentation.md`
- `docs/auto-generated/2025-11-07/COMMIT_b95d794_documentation.md`
- `docs/auto-generated/2025-11-07/COMMIT_d6c67ac_documentation.md`
- `docs/auto-generated/2025-11-07/COMMIT_dc23cfe_feature.md`
- `helena_tasks/helena_task_20251107_070000_agent_code.md`
- `helena_tasks/helena_task_20251107_070000_database_schema.md`
- `helena_tasks/helena_task_20251107_070000_documentation.md`
- `helena_tasks/helena_task_20251107_070000_general_change.md`
- `helena_tasks/helena_task_20251107_070000_knowledge_graph.md`


### Configuration Files (11)

- `.change_tracking_state.json`
- `helena_tasks/processed/success_realtime_20251107_065426_COMMIT_dc23cfe_feature.json`
- `helena_tasks/processed/success_realtime_20251107_065933_COMMIT_d6c67ac_documentation.json`
- `helena_tasks/processed/success_realtime_20251107_070519_COMMIT_b95d794_documentation.json`
- `helena_tasks/processed/success_realtime_20251107_070655_LOCAL_SYSTEM_IMPROVEMENT_PLAN.json`
- `helena_tasks/processed/success_realtime_20251107_071031_COMMIT_71fe32a_documentation.json`
- `qdrant_pending/indexed/doc_20251107_065427_COMMIT_dc23cfe_feature.json`
- `qdrant_pending/indexed/doc_20251107_065934_COMMIT_d6c67ac_documentation.json`
- `qdrant_pending/indexed/doc_20251107_070520_COMMIT_b95d794_documentation.json`
- `qdrant_pending/indexed/doc_20251107_070656_LOCAL_SYSTEM_IMPROVEMENT_PLAN.json`
- `qdrant_pending/indexed/doc_20251107_071031_COMMIT_71fe32a_documentation.json`


### Other Files (15)

- `redis_pending/redis_20251107_065427_COMMIT_dc23cfe_feature.txt`
- `redis_pending/redis_20251107_065934_COMMIT_d6c67ac_documentation.txt`
- `redis_pending/redis_20251107_070520_COMMIT_b95d794_documentation.txt`
- `redis_pending/redis_20251107_070656_LOCAL_SYSTEM_IMPROVEMENT_PLAN.txt`
- `redis_pending/redis_20251107_071031_COMMIT_71fe32a_documentation.txt`
- `sql/realtime_updates/neo4j_20251107_065427_COMMIT_dc23cfe_feature.cypher`
- `sql/realtime_updates/neo4j_20251107_065934_COMMIT_d6c67ac_documentation.cypher`
- `sql/realtime_updates/neo4j_20251107_070520_COMMIT_b95d794_documentation.cypher`
- `sql/realtime_updates/neo4j_20251107_070656_LOCAL_SYSTEM_IMPROVEMENT_PLAN.cypher`
- `sql/realtime_updates/neo4j_20251107_071031_COMMIT_71fe32a_documentation.cypher`
- `sql/realtime_updates/pg_20251107_065427_COMMIT_dc23cfe_feature.sql`
- `sql/realtime_updates/pg_20251107_065934_COMMIT_d6c67ac_documentation.sql`
- `sql/realtime_updates/pg_20251107_070520_COMMIT_b95d794_documentation.sql`
- `sql/realtime_updates/pg_20251107_070656_LOCAL_SYSTEM_IMPROVEMENT_PLAN.sql`
- `sql/realtime_updates/pg_20251107_071031_COMMIT_71fe32a_documentation.sql`


## 📊 Statistics

```
fb8cb6f feat: Download 6 Azoty annual reports for multi-year analysis (2022-2024)
 .change_tracking_state.json                        |    4 +-
 .../2025-11-07/COMMIT_71fe32a_documentation.md     |   75 +
 .../2025-11-07/COMMIT_b95d794_documentation.md     |   70 +
 .../2025-11-07/COMMIT_d6c67ac_documentation.md     |   58 +
 .../2025-11-07/COMMIT_dc23cfe_feature.md           | 1988 ++++++++++++++++++++
 .../helena_task_20251107_070000_agent_code.md      |  199 ++
 .../helena_task_20251107_070000_database_schema.md |  202 ++
 .../helena_task_20251107_070000_documentation.md   |  200 ++
 .../helena_task_20251107_070000_general_change.md  |  201 ++
 .../helena_task_20251107_070000_knowledge_graph.md |  193 ++
 ...ime_20251107_065426_COMMIT_dc23cfe_feature.json |    9 +
 ...251107_065933_COMMIT_d6c67ac_documentation.json |    9 +
 ...251107_070519_COMMIT_b95d794_documentation.json |    9 +
 ...51107_070655_LOCAL_SYSTEM_IMPROVEMENT_PLAN.json |    9 +
 ...251107_071031_COMMIT_71fe32a_documentation.json |    9 +
 ...doc_20251107_065427_COMMIT_dc23cfe_feature.json |    8 +
 ...251107_065934_COMMIT_d6c67ac_documentation.json |    8 +
 ...251107_070520_COMMIT_b95d794_documentation.json |    8 +
 ...51107_070656_LOCAL_SYSTEM_IMPROVEMENT_PLAN.json |    8 +
 ...251107_071031_COMMIT_71fe32a_documentation.json |    8 +
 ...edis_20251107_065427_COMMIT_dc23cfe_feature.txt |   38 +
 ...0251107_065934_COMMIT_d6c67ac_documentation.txt |   52 +
 ...0251107_070520_COMMIT_b95d794_documentation.txt |   38 +
 ...251107_070656_LOCAL_SYSTEM_IMPROVEMENT_PLAN.txt |   25 +
 ...0251107_071031_COMMIT_71fe32a_documentation.txt |   35 +
 scripts/download_azoty_reports.sh                  |   68 +
 ...j_20251107_065427_COMMIT_dc23cfe_feature.cypher |   10 +
 ...1107_065934_COMMIT_d6c67ac_documentation.cypher |   10 +
 ...1107_070520_COMMIT_b95d794_documentation.cypher |   10 +
 ...107_070656_LOCAL_SYSTEM_IMPROVEMENT_PLAN.cypher |   10 +
 ...1107_071031_COMMIT_71fe32a_documentation.cypher |   10 +
 .../pg_20251107_065427_COMMIT_dc23cfe_feature.sql  |   25 +
 ...0251107_065934_COMMIT_d6c67ac_documentation.sql |   27 +
 ...0251107_070520_COMMIT_b95d794_documentation.sql |   26 +
 ...251107_070656_LOCAL_SYSTEM_IMPROVEMENT_PLAN.sql |   18 +
 ...0251107_071031_COMMIT_71fe32a_documentation.sql |   26 +
 36 files changed, 3701 insertions(+), 2 deletions(-)
```

## 🤖 Metadata

```json
{
  "commit_hash": "fb8cb6f484793acb17f19ce93f769bbed23a864c",
  "commit_type": "feature",
  "timestamp": 1762496134,
  "files_changed": [
    ".change_tracking_state.json",
    "docs/auto-generated/2025-11-07/COMMIT_71fe32a_documentation.md",
    "docs/auto-generated/2025-11-07/COMMIT_b95d794_documentation.md",
    "docs/auto-generated/2025-11-07/COMMIT_d6c67ac_documentation.md",
    "docs/auto-generated/2025-11-07/COMMIT_dc23cfe_feature.md",
    "helena_tasks/helena_task_20251107_070000_agent_code.md",
    "helena_tasks/helena_task_20251107_070000_database_schema.md",
    "helena_tasks/helena_task_20251107_070000_documentation.md",
    "helena_tasks/helena_task_20251107_070000_general_change.md",
    "helena_tasks/helena_task_20251107_070000_knowledge_graph.md",
    "helena_tasks/processed/success_realtime_20251107_065426_COMMIT_dc23cfe_feature.json",
    "helena_tasks/processed/success_realtime_20251107_065933_COMMIT_d6c67ac_documentation.json",
    "helena_tasks/processed/success_realtime_20251107_070519_COMMIT_b95d794_documentation.json",
    "helena_tasks/processed/success_realtime_20251107_070655_LOCAL_SYSTEM_IMPROVEMENT_PLAN.json",
    "helena_tasks/processed/success_realtime_20251107_071031_COMMIT_71fe32a_documentation.json",
    "qdrant_pending/indexed/doc_20251107_065427_COMMIT_dc23cfe_feature.json",
    "qdrant_pending/indexed/doc_20251107_065934_COMMIT_d6c67ac_documentation.json",
    "qdrant_pending/indexed/doc_20251107_070520_COMMIT_b95d794_documentation.json",
    "qdrant_pending/indexed/doc_20251107_070656_LOCAL_SYSTEM_IMPROVEMENT_PLAN.json",
    "qdrant_pending/indexed/doc_20251107_071031_COMMIT_71fe32a_documentation.json",
    "redis_pending/redis_20251107_065427_COMMIT_dc23cfe_feature.txt",
    "redis_pending/redis_20251107_065934_COMMIT_d6c67ac_documentation.txt",
    "redis_pending/redis_20251107_070520_COMMIT_b95d794_documentation.txt",
    "redis_pending/redis_20251107_070656_LOCAL_SYSTEM_IMPROVEMENT_PLAN.txt",
    "redis_pending/redis_20251107_071031_COMMIT_71fe32a_documentation.txt",
    "scripts/download_azoty_reports.sh",
    "sql/realtime_updates/neo4j_20251107_065427_COMMIT_dc23cfe_feature.cypher",
    "sql/realtime_updates/neo4j_20251107_065934_COMMIT_d6c67ac_documentation.cypher",
    "sql/realtime_updates/neo4j_20251107_070520_COMMIT_b95d794_documentation.cypher",
    "sql/realtime_updates/neo4j_20251107_070656_LOCAL_SYSTEM_IMPROVEMENT_PLAN.cypher",
    "sql/realtime_updates/neo4j_20251107_071031_COMMIT_71fe32a_documentation.cypher",
    "sql/realtime_updates/pg_20251107_065427_COMMIT_dc23cfe_feature.sql",
    "sql/realtime_updates/pg_20251107_065934_COMMIT_d6c67ac_documentation.sql",
    "sql/realtime_updates/pg_20251107_070520_COMMIT_b95d794_documentation.sql",
    "sql/realtime_updates/pg_20251107_070656_LOCAL_SYSTEM_IMPROVEMENT_PLAN.sql",
    "sql/realtime_updates/pg_20251107_071031_COMMIT_71fe32a_documentation.sql"
  ],
  "auto_generated": true
}
```

---
*This document was automatically generated from a git commit.*
*Helena will process this and add to all 4 databases (PostgreSQL, Neo4j, Qdrant, Redis).*