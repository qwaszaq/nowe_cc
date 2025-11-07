# 🗂️ Results Storage Architecture - Design Document

**Date:** November 5, 2024  
**System:** Destiny Autonomous Analysis  
**Author:** Architecture Team

---

## 🎯 Design Goals

1. **Discoverable** - Easy to find results by case_id, date, agent, category
2. **Scalable** - Handle 1000s of analyses without performance degradation
3. **Multi-Layer** - Different storage for different needs (files, DB, search, graph)
4. **Auditable** - Complete trace from input → processing → output
5. **Queryable** - Fast search across historical analyses
6. **Archivable** - Clear retention policies and backup strategy

---

## 📁 File System Structure

```
destiny-project/
│
├── cases/                          # 🎯 PRIMARY: All case data
│   ├── {case_id}/                  # One folder per case
│   │   ├── metadata.json           # Case metadata
│   │   ├── input/                  # Original documents
│   │   │   ├── documents/
│   │   │   ├── manifest.json      # List of all input files
│   │   │   └── checksums.txt      # MD5/SHA256 hashes
│   │   ├── processing/             # Intermediate artifacts
│   │   │   ├── extracted/         # Extracted text, tables
│   │   │   ├── embeddings/        # Vector embeddings (backup)
│   │   │   ├── classifications/   # File classifications
│   │   │   └── tasks/             # Generated task definitions
│   │   ├── results/                # 📊 FINAL OUTPUTS
│   │   │   ├── final_report.json  # Complete analysis
│   │   │   ├── final_report.md    # Human-readable
│   │   │   ├── final_report.html  # Web view
│   │   │   ├── agents/            # Per-agent results
│   │   │   │   ├── legal_analysis.json
│   │   │   │   ├── financial_analysis.json
│   │   │   │   └── risk_assessment.json
│   │   │   └── visualizations/    # Charts, graphs
│   │   │       ├── timeline.png
│   │   │       ├── network.png
│   │   │       └── metrics.png
│   │   ├── audit/                  # Audit trail
│   │   │   ├── execution_log.json
│   │   │   ├── agent_traces.jsonl  # JSONL for streaming
│   │   │   └── performance_metrics.json
│   │   └── archives/               # Historical versions
│   │       └── {timestamp}/        # Snapshots
│   │
│   └── index.json                  # Case index (fast lookup)
│
├── reports/                        # 📋 LEGACY: Flat reports (keep for compatibility)
│   ├── autonomous_{case_id}.json
│   └── autonomous_{case_id}.html
│
├── analytics/                      # 📊 Cross-case analytics
│   ├── monthly/
│   │   └── 2024-11/
│   │       ├── summary.json
│   │       ├── agent_performance.json
│   │       └── token_usage.json
│   ├── trends/                     # Trend analysis
│   └── benchmarks/                 # Performance benchmarks
│
└── exports/                        # 📤 Export formats
    ├── csv/                        # Tabular exports
    ├── excel/                      # Excel workbooks
    └── api/                        # API-ready JSON
```

---

## 🗄️ Database Storage Strategy

### **Layer 1: PostgreSQL** (Structured Data & Search)

```sql
-- Cases table
CREATE TABLE cases (
    case_id VARCHAR(255) PRIMARY KEY,
    folder_path TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(50), -- pending, processing, complete, failed
    total_files INT,
    total_size_mb FLOAT,
    classification JSONB, -- {legal: 13, technical: 1}
    metadata JSONB
);

-- Documents table
CREATE TABLE documents (
    document_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id VARCHAR(255) REFERENCES cases(case_id),
    file_path TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_type VARCHAR(50),
    file_size_bytes BIGINT,
    file_hash VARCHAR(64), -- SHA256
    category VARCHAR(100),
    classification_confidence FLOAT,
    created_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB
);

-- Agent executions table
CREATE TABLE agent_executions (
    execution_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id VARCHAR(255) REFERENCES cases(case_id),
    agent_name VARCHAR(100),
    agent_category VARCHAR(100),
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    duration_seconds FLOAT,
    tokens_used INT,
    tokens_saved INT, -- CAG savings
    confidence FLOAT,
    status VARCHAR(50), -- success, failed, timeout
    output_summary TEXT, -- First 500 chars
    output_full TEXT, -- Full output
    metadata JSONB
);

-- Findings table (searchable key insights)
CREATE TABLE findings (
    finding_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    case_id VARCHAR(255) REFERENCES cases(case_id),
    execution_id UUID REFERENCES agent_executions(execution_id),
    agent_name VARCHAR(100),
    category VARCHAR(100),
    finding_type VARCHAR(100), -- risk, opportunity, issue, insight
    severity VARCHAR(50), -- critical, high, medium, low, info
    title TEXT,
    description TEXT,
    evidence TEXT,
    confidence FLOAT,
    created_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB
);

-- Indexes for fast queries
CREATE INDEX idx_cases_created ON cases(created_at DESC);
CREATE INDEX idx_documents_case ON documents(case_id);
CREATE INDEX idx_documents_category ON documents(category);
CREATE INDEX idx_executions_case ON agent_executions(case_id);
CREATE INDEX idx_executions_agent ON agent_executions(agent_name);
CREATE INDEX idx_findings_case ON findings(case_id);
CREATE INDEX idx_findings_type ON findings(finding_type, severity);

-- Full-text search
CREATE INDEX idx_findings_search ON findings USING GIN(to_tsvector('english', title || ' ' || description));
```

### **Layer 2: Qdrant** (Vector Search)

```python
# Collections structure
collections = {
    "case_documents": {
        "vectors": {
            "size": 1024,
            "distance": "Cosine"
        },
        "payload_schema": {
            "case_id": "keyword",
            "document_id": "keyword",
            "file_name": "text",
            "category": "keyword",
            "chunk_id": "integer",
            "content": "text",
            "metadata": "json"
        }
    },
    
    "case_findings": {
        "vectors": {
            "size": 1024,
            "distance": "Cosine"
        },
        "payload_schema": {
            "case_id": "keyword",
            "agent_name": "keyword",
            "finding_type": "keyword",
            "title": "text",
            "description": "text"
        }
    },
    
    "case_summaries": {
        "vectors": {
            "size": 1024,
            "distance": "Cosine"
        },
        "payload_schema": {
            "case_id": "keyword",
            "summary": "text",
            "categories": "keyword[]",
            "agents_used": "keyword[]",
            "key_insights": "text"
        }
    }
}
```

### **Layer 3: Elasticsearch** (Full-Text Search & Analytics)

```json
{
  "cases_index": {
    "mappings": {
      "properties": {
        "case_id": {"type": "keyword"},
        "folder_path": {"type": "text"},
        "created_at": {"type": "date"},
        "status": {"type": "keyword"},
        "documents": {
          "type": "nested",
          "properties": {
            "file_name": {"type": "text"},
            "category": {"type": "keyword"},
            "content": {"type": "text", "analyzer": "english"}
          }
        },
        "findings": {
          "type": "nested",
          "properties": {
            "agent": {"type": "keyword"},
            "title": {"type": "text"},
            "description": {"type": "text"},
            "severity": {"type": "keyword"}
          }
        }
      }
    }
  }
}
```

### **Layer 4: Neo4j** (Relationships & Graph)

```cypher
// Case node
CREATE (c:Case {
    case_id: 'cba_analysis_2024',
    created_at: datetime(),
    status: 'complete'
})

// Document nodes
CREATE (d:Document {
    document_id: uuid(),
    file_name: 'Informacja_2021.pdf',
    category: 'legal'
})

// Agent execution nodes
CREATE (e:Execution {
    execution_id: uuid(),
    agent_name: 'legal',
    duration: 13.1,
    tokens_used: 4164
})

// Finding nodes
CREATE (f:Finding {
    finding_id: uuid(),
    title: 'Data confidentiality risk',
    severity: 'high'
})

// Relationships
CREATE (c)-[:CONTAINS]->(d)
CREATE (c)-[:ANALYZED_BY]->(e)
CREATE (e)-[:PRODUCED]->(f)
CREATE (d)-[:MENTIONED_IN]->(f)
CREATE (f)-[:RELATES_TO]->(d)
```

### **Layer 5: Redis** (Hot Cache & Real-time)

```python
# Redis keys structure
keys = {
    # Current processing
    f"case:{case_id}:status": "processing",
    f"case:{case_id}:progress": "45%",
    f"case:{case_id}:current_agent": "legal",
    
    # Recent results (TTL: 24h)
    f"recent:cases": ["case_001", "case_002", ...],
    f"recent:findings:{case_id}": [...],
    
    # Metrics (rolling window)
    f"metrics:daily:{date}:cases": 15,
    f"metrics:daily:{date}:tokens": 125000,
    
    # Cache (TTL: 1h)
    f"cache:case:{case_id}:summary": {...},
    f"cache:agent:legal:last_result": {...}
}
```

---

## 🔄 Result Storage Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  AUTONOMOUS ANALYSIS EXECUTION                              │
└───────────────┬─────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────┐
│  1. CREATE CASE STRUCTURE                                   │
│  - Generate case_id                                         │
│  - Create cases/{case_id}/ folders                          │
│  - Copy input files to cases/{case_id}/input/              │
│  - Create metadata.json                                     │
└───────────────┬─────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────┐
│  2. STORE IN DATABASES (parallel)                           │
│  ├─ PostgreSQL: case + documents records                    │
│  ├─ Qdrant: document vectors                                │
│  ├─ Elasticsearch: full-text indexes                        │
│  ├─ Neo4j: case + document nodes                            │
│  └─ Redis: case:status = "processing"                       │
└───────────────┬─────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────┐
│  3. SAVE PROCESSING ARTIFACTS                               │
│  - cases/{case_id}/processing/extracted/                    │
│  - cases/{case_id}/processing/classifications/              │
│  - Update PostgreSQL: agent_executions (start)              │
└───────────────┬─────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────┐
│  4. STORE AGENT RESULTS (per agent)                         │
│  - cases/{case_id}/results/agents/{agent}.json              │
│  - PostgreSQL: agent_executions (complete)                  │
│  - PostgreSQL: findings table                               │
│  - Qdrant: finding vectors                                  │
│  - Neo4j: execution + finding nodes                         │
│  - Redis: update progress                                   │
└───────────────┬─────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────┐
│  5. GENERATE FINAL REPORT                                   │
│  - cases/{case_id}/results/final_report.json                │
│  - cases/{case_id}/results/final_report.md                  │
│  - cases/{case_id}/results/final_report.html                │
│  - reports/autonomous_{case_id}.json (legacy)               │
└───────────────┬─────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────┐
│  6. UPDATE ALL DATABASES (final)                            │
│  - PostgreSQL: cases.status = "complete"                    │
│  - Elasticsearch: index complete case                       │
│  - Qdrant: store case summary vector                        │
│  - Neo4j: complete relationships                            │
│  - Redis: cache summary (TTL: 24h)                          │
└───────────────┬─────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────────┐
│  7. AUDIT & ANALYTICS                                       │
│  - cases/{case_id}/audit/execution_log.json                 │
│  - Update analytics/monthly/ aggregates                     │
│  - Trigger backup if needed                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Query Patterns & Use Cases

### **Use Case 1: Find case by ID**
```python
# File system
case_dir = Path(f"cases/{case_id}")
report = json.load(case_dir / "results" / "final_report.json")

# PostgreSQL (fastest for exact match)
result = db.execute(
    "SELECT * FROM cases WHERE case_id = %s",
    (case_id,)
).fetchone()
```

### **Use Case 2: Search across all findings**
```python
# Elasticsearch (best for full-text)
results = es.search(index="cases_index", body={
    "query": {
        "nested": {
            "path": "findings",
            "query": {
                "match": {"findings.description": "corruption risk"}
            }
        }
    }
})

# PostgreSQL (with full-text search)
results = db.execute("""
    SELECT * FROM findings
    WHERE to_tsvector('english', description)
        @@ to_tsquery('english', 'corruption & risk')
    ORDER BY confidence DESC
    LIMIT 10
""").fetchall()
```

### **Use Case 3: Find similar cases**
```python
# Qdrant (semantic similarity)
similar_cases = qdrant_client.search(
    collection_name="case_summaries",
    query_vector=embedding_of_new_case,
    limit=10
)
```

### **Use Case 4: Analyze agent performance**
```python
# PostgreSQL (analytics)
stats = db.execute("""
    SELECT 
        agent_name,
        COUNT(*) as executions,
        AVG(duration_seconds) as avg_duration,
        AVG(tokens_used) as avg_tokens,
        SUM(tokens_saved) as total_saved
    FROM agent_executions
    WHERE completed_at > NOW() - INTERVAL '30 days'
    GROUP BY agent_name
    ORDER BY executions DESC
""").fetchall()
```

### **Use Case 5: Graph analysis - Connected entities**
```cypher
// Neo4j - Find related documents through findings
MATCH (d1:Document)-[:MENTIONED_IN]->(f:Finding)
      <-[:MENTIONED_IN]-(d2:Document)
WHERE d1.case_id = 'cba_analysis_2024'
  AND d1 <> d2
RETURN d1.file_name, f.title, d2.file_name, COUNT(*) as connections
ORDER BY connections DESC
LIMIT 10
```

---

## 🔒 Security & Access Control

### **File System Permissions**
```bash
cases/
├── {case_id}/
│   ├── input/          # Read-only after ingestion
│   ├── processing/     # System write, user read
│   ├── results/        # System write, user read
│   └── audit/          # Append-only, immutable
```

### **Database Access Levels**

| Role | PostgreSQL | Qdrant | Elasticsearch | Neo4j | Redis |
|------|-----------|--------|---------------|-------|-------|
| **System** | FULL | FULL | FULL | FULL | FULL |
| **Analyst** | SELECT only | Search only | Search only | Read only | Read only |
| **Admin** | FULL | FULL | FULL | FULL | FULL |
| **API** | SELECT cases/findings | Search only | Search only | Read only | Read only |

---

## 📅 Retention & Archival

### **Retention Policy**

| Data Type | Hot Storage | Warm Storage | Cold Storage | Deletion |
|-----------|-------------|--------------|--------------|----------|
| **Active cases** | PostgreSQL + Files | - | - | Never |
| **Recent results (30d)** | All layers | - | - | - |
| **Older results (30-90d)** | PostgreSQL + Qdrant | Files compressed | - | - |
| **Historical (90d-1y)** | PostgreSQL only | S3/Archive | Qdrant/ES cleaned | - |
| **Ancient (1y+)** | Metadata only | - | Full archive | Optional |

### **Backup Strategy**

```bash
# Daily backups
├── PostgreSQL: pg_dump → S3 (encrypted)
├── Files: rsync cases/ → backup-server/
├── Qdrant: snapshot → S3
├── Elasticsearch: snapshot → S3
└── Neo4j: backup → S3

# Weekly backups
└── Full system snapshot (all layers)

# Monthly archives
└── Compressed cold storage (long-term retention)
```

---

## 🎯 Implementation Priority

### **Phase 1: Core Structure** (Week 1)
- [ ] Create `cases/` directory structure
- [ ] Update `AutonomousOrchestrator` to use new structure
- [ ] PostgreSQL schema implementation
- [ ] Basic file storage workflow

### **Phase 2: Multi-Database Integration** (Week 2)
- [ ] Qdrant integration (vectors)
- [ ] Elasticsearch integration (search)
- [ ] Neo4j integration (graph)
- [ ] Redis caching layer

### **Phase 3: Query & Analytics** (Week 3)
- [ ] Search API implementation
- [ ] Analytics dashboard
- [ ] Performance monitoring
- [ ] Cross-case analysis tools

### **Phase 4: Operations** (Week 4)
- [ ] Backup automation
- [ ] Retention policies
- [ ] Monitoring & alerting
- [ ] Documentation & training

---

## 📈 Success Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| **Query Speed** | <100ms for case lookup | PostgreSQL query time |
| **Search Accuracy** | >90% relevance | User feedback on search results |
| **Storage Efficiency** | <50MB per case avg | Disk usage monitoring |
| **Backup Reliability** | 100% success rate | Backup verification tests |
| **Data Availability** | 99.9% uptime | Database health checks |

---

## 🎉 Benefits of This Architecture

1. ✅ **Clear Organization** - Everything for a case in one place
2. ✅ **Fast Queries** - Multiple indexes for different query patterns
3. ✅ **Scalable** - Each layer handles what it does best
4. ✅ **Auditable** - Complete execution trace
5. ✅ **Flexible** - Easy to add new storage layers or query types
6. ✅ **Resilient** - Multiple backup strategies
7. ✅ **Developer-Friendly** - Intuitive structure, easy to navigate

---

## 🚀 Next Steps

1. **Review this design** with the team
2. **Create implementation tickets** for each phase
3. **Set up development environment** with new structure
4. **Migrate existing reports** to new structure (one-time)
5. **Update documentation** and examples

---

**Questions? See:** `docs/architecture/storage-architecture.md`  
**Implementation:** `src/storage/` (to be created)
