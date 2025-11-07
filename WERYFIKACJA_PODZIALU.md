# ✅ WERYFIKACJA PODZIAŁU - Investigation vs Development

**Data:** 5 Listopada 2024

---

## 📊 FINAL PORT ALLOCATION

### **INVESTIGATION Environment (Production - DO NOT MODIFY)**

```
Container Name              Port(s)           Purpose                   Data
─────────────────────────────────────────────────────────────────────────────
sms-postgres                5432              SMS Cases DB              Production
sms-qdrant                  6333-6334         SMS Embeddings            96,100+ vectors
sms-neo4j                   7474, 7687        SMS Relationships         Production
hercules-postgres           5433              Hercules Cases            Production
hercules-elasticsearch      9200, 9300        OSINT Documents           Production
hercules-kibana             5601              OSINT Dashboard           Analytics
hercules-redis              6380              Hercules Cache            Production
hercules-minio              9000-9001         File Storage              Production
hercules-kafka              9092-9093, 29092  Message Queue             Production
```

**Total Collections in sms-qdrant:**
- sms_embeddings: 96,100 points
- sms_corpus_chunks: 10,957 points
- ragsms: 33,227 points
- sms_analysis_messages: 496 points
- destiny-team-framework-master: 462 points
- Others: ~1,500 points

**Total: ~143,000 vectors (PRODUCTION DATA!)**

---

### **DEVELOPMENT Environment (Framework - FULL ACCESS)**

```
Container Name              Port(s)           Purpose                   Data
─────────────────────────────────────────────────────────────────────────────
destiny-postgres            5434              Development DB            Test/CBA
destiny-qdrant              6335-6336         Development Vectors       Test data
destiny-neo4j               7475, 7688        Development Graph         Test data
destiny-elasticsearch       9201, 9301        Development Search        Test data
destiny-redis               6379              Development Cache         Test data
```

**Initial Data:** Empty (fresh start for development)

---

## ✅ VERIFICATION COMMANDS

### **Check Port Separation:**

```bash
# Investigation ports (existing)
curl -s http://localhost:6333/collections | jq '.result.collections | length'
# Should show: 14 collections

# Development ports (new)
curl -s http://localhost:6335/collections | jq '.result.collections | length'  
# Should show: 0 collections (empty)
```

### **Test Development Access:**

```bash
# Load development environment
export ENV_FILE=.env.development

# Test PostgreSQL
docker exec destiny-postgres psql -U destiny -d destiny_dev -c "SELECT version();"

# Test Qdrant
curl http://localhost:6335/health

# Test Neo4j
curl http://localhost:7475

# Test Elasticsearch
curl http://localhost:9201/_cluster/health
```

### **Test Investigation Access (READ-ONLY):**

```bash
# Load investigation environment  
export ENV_FILE=.env.investigation

# Query SMS data (READ-ONLY)
python3 -c "
from src.data.qdrant_client import QdrantVectorStore
q = QdrantVectorStore(url='http://localhost:6333')
print(f'SMS collections: {q.list_collections()}')
"

# ✅ Can read
# ❌ Cannot write (enforced in code)
```

---

## 🔒 SECURITY VERIFICATION

### **Test READ-ONLY Enforcement:**

```python
# test_read_only.py
from config import get_config
import os

# Test investigation (should enforce READ-ONLY)
os.environ['ENVIRONMENT'] = 'investigation'
os.environ['READ_ONLY'] = 'false'  # Try to bypass

try:
    config = get_config()  # Should raise PermissionError!
    print("❌ FAILED: Investigation not enforcing READ-ONLY!")
except PermissionError as e:
    print(f"✅ PASSED: {e}")

# Test development (should allow full access)
os.environ['ENVIRONMENT'] = 'development'
os.environ['READ_ONLY'] = 'false'

config = get_config()
print(f"✅ Development allows full access: {not config.read_only}")
```

---

## 📊 DATA INVENTORY

### **Investigation Data (Protected):**

| System | Container | Port | Data Volume | Status |
|--------|-----------|------|-------------|--------|
| SMS PostgreSQL | sms-postgres | 5432 | Unknown | 🔒 Protected |
| SMS Qdrant | sms-qdrant | 6333 | 143K vectors | 🔒 Protected |
| SMS Neo4j | sms-neo4j | 7474 | Unknown | 🔒 Protected |
| Hercules PostgreSQL | hercules-postgres | 5433 | Unknown | 🔒 Protected |
| Hercules Elasticsearch | hercules-elasticsearch | 9200 | Unknown | 🔒 Protected |

**Backup Status:** Should be backed up regularly (CRITICAL!)

---

### **Development Data (Experimental):**

| System | Container | Port | Data Volume | Status |
|--------|-----------|------|-------------|--------|
| Destiny PostgreSQL | destiny-postgres | 5434 | 0 MB (fresh) | ✅ Full Access |
| Destiny Qdrant | destiny-qdrant | 6335 | 0 vectors | ✅ Full Access |
| Destiny Neo4j | destiny-neo4j | 7475 | 0 nodes | ✅ Full Access |
| Destiny Elasticsearch | destiny-elasticsearch | 9201 | 0 docs | ✅ Full Access |

**Backup Status:** Optional (can recreate from CBA reports)

---

## 🎯 USAGE GUIDE

### **Development Work (Default):**

```bash
# 1. Use development environment
export ENV_FILE=.env.development

# 2. Verify ports
docker-compose -f docker-compose-dev.yml ps

# 3. Run tests with CBA reports
python3 profound_test.py

# 4. Experiment freely
python3 test_local_graph.py
python3 test_new_features.py

# ✅ Uses: 5434, 6335, 7475, 9201
# ✅ Investigation data: UNTOUCHED
# ✅ Can drop/recreate anytime
```

### **Investigation Query (When Needed):**

```bash
# 1. Use investigation environment
export ENV_FILE=.env.investigation

# 2. Query SMS patterns (READ-ONLY)
python3 scripts/query_sms_cases.py --case-id SMS-2024-001

# 3. Learn from investigation data
python3 scripts/analyze_sms_patterns.py

# ✅ Uses: 5432, 6333, 7474, 9200
# ✅ READ-ONLY enforced
# ❌ Cannot modify production data
```

---

## 🚀 WORKFLOW EXAMPLES

### **Example 1: Develop Local Graph on CBA Reports**

```bash
# Development environment
export ENV_FILE=.env.development

# Process CBA reports
python3 destiny_auto.py testdocsLLM

# Build local graph
python3 scripts/build_local_graph.py --input testdocsLLM --output analysis_reports/

# Test graph queries
python3 scripts/test_graph_queries.py

# ✅ All data goes to destiny-postgres:5434, destiny-qdrant:6335
# ✅ Investigation data completely isolated
```

### **Example 2: Learn from SMS, Test on Development**

```bash
# Step 1: Query SMS patterns (investigation environment)
export ENV_FILE=.env.investigation
python3 scripts/extract_sms_patterns.py > sms_patterns.json

# Step 2: Test patterns on development data
export ENV_FILE=.env.development
python3 scripts/test_patterns.py --patterns sms_patterns.json --data testdocsLLM

# ✅ Investigation data: READ only
# ✅ Development data: FULL access
```

---

## 🎯 VERIFICATION CHECKLIST

```bash
# ✅ Check 1: Port separation
docker ps | grep -E "postgres|qdrant|neo4j|elastic"
# Should show DIFFERENT ports for destiny-* vs sms-*/hercules-*

# ✅ Check 2: Investigation data intact
curl -s http://localhost:6333/collections | jq '.result.collections | length'
# Should still show 14 collections

# ✅ Check 3: Development environment clean
curl -s http://localhost:6335/collections | jq '.result.collections | length'
# Should show 0 (fresh start)

# ✅ Check 4: No port conflicts
docker-compose -f docker-compose-dev.yml ps
# Should show all containers "Up" or "healthy"

# ✅ Check 5: Config loads correctly
python3 -c "from config import get_config; import os; os.environ['ENVIRONMENT']='development'; c=get_config(); print(f'PostgreSQL port: {c.postgres.port}')"
# Should print: PostgreSQL port: 5434
```

---

## 🎯 BOTTOM LINE

```
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║  ✅ PODZIAŁ ZREALIZOWANY!                             ║
║                                                       ║
║  INVESTIGATION (Production):                          ║
║    Ports: 5432, 5433, 6333, 7474, 9200              ║
║    Data: 143K+ vectors, production cases             ║
║    Access: READ-ONLY from development                ║
║    Containers: sms-*, hercules-* (existing)          ║
║                                                       ║
║  DEVELOPMENT (Framework):                             ║
║    Ports: 5434, 6335, 7475, 9201                    ║
║    Data: Fresh, CBA reports, tests                   ║
║    Access: FULL read/write                           ║
║    Containers: destiny-* (new, running)              ║
║                                                       ║
║  ZERO CONFLICTS ✅                                    ║
║  ZERO RISK TO PRODUCTION DATA ✅                      ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
```

**Wszystko działa i jest bezpieczne!** 🔒🚀
