# 🔒 SEPARACJA: Investigation Data vs Development System

**Data:** 5 Listopada 2024  
**Critical Issue:** Musimy rozdzielić dane śledcze od rozwoju systemu!

---

## ⚠️ PROBLEM - Nie Możemy Mieszać!

```
❌ ŹLE: Development system używa investigation databases
❌ ŹLE: Test data miesza się z production cases
❌ ŹLE: Jeden kontener dla wszystkiego
```

**Dlaczego to problem:**
- 🔐 Security: Investigation data jest wrażliwe
- 🧪 Testing: Nie możemy testować na production data
- 🗑️ Cleanup: Nie możemy usunąć test data bez ryzyka
- 📊 Analytics: Trudno oddzielić metrics
- 🐛 Debugging: Risk of corrupting real cases

---

## ✅ PRAWIDŁOWA ARCHITEKTURA

### **2 Osobne Środowiska:**

```
┌─────────────────────────────────────────────────────────┐
│  INVESTIGATION ENVIRONMENT (Production)                  │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  sms-postgres:5432        → SMS investigation data      │
│  sms-neo4j:7474          → SMS relationship graphs      │
│  sms-qdrant:6333         → SMS embeddings               │
│  hercules-elasticsearch  → OSINT documents              │
│  hercules-postgres:5433  → Hercules cases               │
│                                                          │
│  ✅ Zawiera: Real cases, sensitive data                  │
│  ✅ Access: Restricted, read-only dla dev               │
│  ✅ Backup: Critical                                     │
│  ❌ NIE używać do: Testing, experiments                  │
│                                                          │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  DEVELOPMENT ENVIRONMENT (Dev/Test)                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  destiny_postgres:5434   → Framework development        │
│  destiny_neo4j:7475      → Graph testing                │
│  destiny_qdrant:6335     → Embedding experiments        │
│  destiny_elasticsearch   → Document parsing tests       │
│                                                          │
│  ✅ Zawiera: Test data, CBA reports, experiments        │
│  ✅ Access: Full read/write                             │
│  ✅ Backup: Optional (can recreate)                     │
│  ✅ Używać do: Development, testing, prototyping        │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 IMPLEMENTACJA - Różne Porty

### **docker-compose-dev.yml** (Development)

```yaml
version: '3.8'

services:
  # Development PostgreSQL - CZYSTE dla testów
  postgres:
    image: ankane/pgvector:latest
    container_name: destiny_postgres
    environment:
      POSTGRES_DB: destiny_dev
      POSTGRES_USER: destiny
      POSTGRES_PASSWORD: destiny_dev_2024
    ports:
      - "5434:5432"  # ← INNY PORT!
    volumes:
      - destiny_postgres_data:/var/lib/postgresql/data
    networks:
      - destiny_dev_network

  # Development Qdrant - dla testów embeddings
  qdrant:
    image: qdrant/qdrant:latest
    container_name: destiny_qdrant
    ports:
      - "6335:6333"  # ← INNY PORT!
      - "6336:6334"
    volumes:
      - destiny_qdrant_data:/qdrant/storage
    networks:
      - destiny_dev_network

  # Development Neo4j - dla testów grafów
  neo4j:
    image: neo4j:5.13-community
    container_name: destiny_neo4j
    environment:
      NEO4J_AUTH: neo4j/destiny_dev_2024
    ports:
      - "7475:7474"  # ← INNY PORT!
      - "7688:7687"
    volumes:
      - destiny_neo4j_data:/data
    networks:
      - destiny_dev_network

  # Development Elasticsearch - dla testów dokumentów
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    container_name: destiny_elasticsearch
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9201:9200"  # ← INNY PORT!
    volumes:
      - destiny_elasticsearch_data:/usr/share/elasticsearch/data
    networks:
      - destiny_dev_network

networks:
  destiny_dev_network:
    name: destiny_dev_network

volumes:
  destiny_postgres_data:
  destiny_qdrant_data:
  destiny_neo4j_data:
  destiny_elasticsearch_data:
```

---

## 📋 .env Configuration

### **.env.investigation** (Production Cases)

```bash
# Investigation Environment - READ ONLY!
INVESTIGATION_MODE=true

# SMS Investigation
SMS_POSTGRES_HOST=localhost
SMS_POSTGRES_PORT=5432
SMS_QDRANT_URL=http://localhost:6333
SMS_NEO4J_URL=http://localhost:7474

# Hercules Investigation
HERCULES_POSTGRES_PORT=5433
HERCULES_ELASTICSEARCH_URL=http://localhost:9200

# Access
READ_ONLY=true  # ← IMPORTANT!
```

### **.env.development** (Framework Development)

```bash
# Development Environment - FULL ACCESS
DEVELOPMENT_MODE=true

# Destiny Development
POSTGRES_HOST=localhost
POSTGRES_PORT=5434  # ← Different!
POSTGRES_DB=destiny_dev
POSTGRES_USER=destiny
POSTGRES_PASSWORD=destiny_dev_2024

QDRANT_URL=http://localhost:6335  # ← Different!
NEO4J_URL=http://localhost:7475    # ← Different!
ELASTICSEARCH_URL=http://localhost:9201  # ← Different!

# Access
READ_ONLY=false  # Full access for dev
```

---

## 🎯 UŻYCIE

### **Development Work (Testing, CBA Reports, etc.):**

```bash
# Start development environment
docker-compose -f docker-compose-dev.yml up -d

# Use development config
export ENV_FILE=.env.development

# Run tests with development data
python3 profound_test.py  # → Uses port 6335, 7475, etc.

# Development is isolated!
# - No risk to investigation data
# - Can drop/recreate databases freely
# - Full experimentation
```

### **Investigation Work (Real Cases - SMS, OSINT):**

```bash
# Use investigation environment (already running)
export ENV_FILE=.env.investigation

# Query investigation data (READ-ONLY!)
python3 query_sms_cases.py  # → Uses port 6333, 7474, etc.

# READ ONLY mode prevents:
# - Accidental deletion
# - Test data pollution
# - Schema modifications
```

---

## 🔒 SECURITY & ISOLATION

### **Investigation Data Protection:**

```python
# src/data/investigation_client.py

class InvestigationDataAccess:
    """
    READ-ONLY access to investigation databases
    """
    
    def __init__(self):
        if os.getenv('INVESTIGATION_MODE') != 'true':
            raise PermissionError("Investigation mode not enabled")
        
        if os.getenv('READ_ONLY') != 'true':
            raise PermissionError("Investigation data is READ-ONLY")
        
        self.postgres = PostgresClient(
            port=5432,  # Investigation port
            read_only=True
        )
        
        self.qdrant = QdrantClient(
            url="http://localhost:6333",  # Investigation port
            read_only=True
        )
    
    def query_sms_cases(self, case_id: str):
        """Query SMS investigation data - READ ONLY"""
        return self.postgres.query(f"SELECT * FROM cases WHERE id = {case_id}")
    
    def write_operation(self):
        """Prevented!"""
        raise PermissionError("Cannot write to investigation database!")
```

### **Development Data Freedom:**

```python
# src/data/development_client.py

class DevelopmentDataAccess:
    """
    FULL access to development databases
    """
    
    def __init__(self):
        if os.getenv('DEVELOPMENT_MODE') != 'true':
            raise PermissionError("Development mode not enabled")
        
        self.postgres = PostgresClient(
            port=5434,  # Development port
            read_only=False  # Full access!
        )
        
        self.qdrant = QdrantClient(
            url="http://localhost:6335",  # Development port
            read_only=False
        )
    
    def test_cba_reports(self):
        """Full experimentation allowed"""
        # Can create, modify, delete freely
        self.postgres.execute("DROP TABLE IF EXISTS test_table")
        self.qdrant.delete_collection("test_collection")
        # No risk to investigation data!
```

---

## 📊 DATA SEPARATION MATRIX

| Aspect | Investigation Env | Development Env |
|--------|------------------|-----------------|
| **Ports** | 5432, 6333, 7474, 9200 | 5434, 6335, 7475, 9201 |
| **Data** | SMS, OSINT, Real cases | CBA reports, Test data |
| **Access** | READ-ONLY | FULL (R/W) |
| **Backup** | Critical (daily) | Optional |
| **Cleanup** | Never (archive only) | Anytime |
| **Networks** | sms_network, hercules_net | destiny_dev_network |
| **Volumes** | Persistent, backed up | Can be wiped |

---

## 🚀 MIGRATION STRATEGY

### **Phase 1: Setup Development Environment** (Now)

```bash
# 1. Create docker-compose-dev.yml (different ports)
# 2. Create .env.development
# 3. Start development containers
docker-compose -f docker-compose-dev.yml up -d

# 4. Initialize development databases
bash scripts/init_dev_databases.sh

# 5. Load test data (CBA reports)
python3 scripts/load_cba_reports.py --env development
```

### **Phase 2: Separate Code Access** (Next)

```python
# config.py
class Config:
    @classmethod
    def get_environment(cls):
        env = os.getenv('ENV', 'development')
        
        if env == 'investigation':
            return InvestigationConfig()  # Ports 5432, 6333, etc.
        elif env == 'development':
            return DevelopmentConfig()    # Ports 5434, 6335, etc.
        else:
            raise ValueError(f"Unknown environment: {env}")

class InvestigationConfig:
    POSTGRES_PORT = 5432
    QDRANT_PORT = 6333
    NEO4J_PORT = 7474
    READ_ONLY = True

class DevelopmentConfig:
    POSTGRES_PORT = 5434
    QDRANT_PORT = 6335
    NEO4J_PORT = 7475
    READ_ONLY = False
```

### **Phase 3: Access Control** (Future)

```python
# Enforce read-only for investigation
@require_environment('investigation')
@read_only
def query_sms_case(case_id):
    """Can only read investigation data"""
    pass

@require_environment('development')
def test_feature():
    """Full access in development"""
    pass
```

---

## 🎯 BENEFITS

### **Development Environment:**

```
✅ Safe experimentation (no risk to real cases)
✅ Can drop/recreate databases anytime
✅ Test CBA reports without fear
✅ Fast iterations
✅ No backup concerns
✅ Full access
```

### **Investigation Environment:**

```
✅ Data integrity protected
✅ No accidental modifications
✅ Clear separation of concerns
✅ Audit trail clear
✅ Backup strategy clear
✅ Compliance-ready
```

---

## 💡 USAGE EXAMPLES

### **Example 1: Testing Local Graph on CBA Reports**

```bash
# Use DEVELOPMENT environment
export ENV=development

# Start dev containers (different ports!)
docker-compose -f docker-compose-dev.yml up -d

# Test local graph with CBA reports
python3 test_local_graph.py

# Results stored in:
# - destiny_postgres:5434
# - destiny_qdrant:6335
# - destiny_neo4j:7475

# ✅ Investigation data untouched!
```

### **Example 2: Query SMS Investigation**

```bash
# Use INVESTIGATION environment
export ENV=investigation

# Query SMS data (READ-ONLY!)
python3 query_sms_investigation.py --case-id SMS-2024-001

# Reads from:
# - sms_postgres:5432
# - sms_qdrant:6333
# - sms_neo4j:7474

# ✅ Cannot modify investigation data!
```

### **Example 3: Hybrid - Learn from Investigations, Test in Dev**

```python
# Step 1: Query investigation patterns (READ-ONLY)
investigation_client = InvestigationDataAccess()
sms_patterns = investigation_client.query_patterns()

# Step 2: Test on development data (FULL ACCESS)
development_client = DevelopmentDataAccess()
development_client.test_patterns(sms_patterns, cba_reports)

# ✅ Best of both worlds!
```

---

## 🎯 BOTTOM LINE

```
╔════════════════════════════════════════════════════════╗
║                                                        ║
║  FUNDAMENTALNA SEPARACJA:                              ║
║                                                        ║
║  🔐 INVESTIGATION (5432, 6333, 7474, 9200)             ║
║     - SMS cases, OSINT, Hercules                       ║
║     - READ-ONLY access                                 ║
║     - Protected, backed up                             ║
║     - Existing containers (sms-*, hercules-*)          ║
║                                                        ║
║  🧪 DEVELOPMENT (5434, 6335, 7475, 9201)               ║
║     - CBA reports, tests, experiments                  ║
║     - FULL access (create/modify/delete)               ║
║     - Can wipe anytime                                 ║
║     - New containers (destiny_*)                       ║
║                                                        ║
║  NIE MIESZAMY! ❌                                      ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
```

**Action Plan:**
1. ✅ Create `docker-compose-dev.yml` (różne porty)
2. ✅ Create `.env.development` & `.env.investigation`
3. ✅ Start development containers
4. ✅ Update code to use environment-based config
5. ✅ Test separation

**Zgoda? Robię to teraz?** 🚀
