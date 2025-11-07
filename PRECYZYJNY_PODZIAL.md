# 🔒 PRECYZYJNY PODZIAŁ: Investigation vs Development

**Data:** 5 Listopada 2024  
**Cel:** Absolutna separacja danych śledczych od rozwoju systemu

---

## 📋 INWENTARYZACJA - Co Mamy Obecnie

### **INVESTIGATION ENVIRONMENT (Production Cases)**

```
┌──────────────────────────┬──────────┬────────────────────┐
│ Container                │ Ports    │ Purpose            │
├──────────────────────────┼──────────┼────────────────────┤
│ sms-postgres             │ 5432     │ SMS investigations │
│ sms-neo4j                │ 7474     │ SMS graph          │
│ sms-qdrant               │ 6333     │ SMS embeddings     │
│ hercules-postgres        │ 5433     │ Hercules cases     │
│ hercules-elasticsearch   │ 9200     │ OSINT documents    │
│ hercules-kibana          │ 5601     │ OSINT analytics    │
└──────────────────────────┴──────────┴────────────────────┘
```

**Zawartość (Investigation Data):**
- SMS investigation cases
- OSINT reports & documents
- Hercules analytical data
- Real-world sensitive information
- Production relationships
- Historical investigation data

**Charakterystyka:**
- 🔐 CRITICAL - Cannot be lost
- 🔒 SENSITIVE - Privacy concerns
- 📊 PRODUCTION - Real cases
- ⚠️ READ-ONLY dla development
- 💾 BACKUP required daily

---

### **DESTINY CONTAINERS (Framework - Currently Broken)**

```
┌──────────────────────────┬──────────┬────────────────────┐
│ Container                │ Status   │ Problem            │
├──────────────────────────┼──────────┼────────────────────┤
│ destiny_postgres         │ Created  │ Port conflict      │
│ destiny_neo4j            │ Created  │ Port conflict      │
│ destiny_qdrant           │ N/A      │ Not created        │
│ destiny_elasticsearch    │ N/A      │ Not created        │
└──────────────────────────┴──────────┴────────────────────┘
```

**Problem:** Cannot start due to port conflicts with investigation containers!

---

## 🎯 DOCELOWA ARCHITEKTURA

### **Diagram Separacji:**

```
┌─────────────────────────────────────────────────────────────┐
│                    HOST MACHINE                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │  INVESTIGATION NETWORK (sms_network, hercules_net) │     │
│  │                                                     │     │
│  │  sms-postgres:5432        [SMS cases]             │     │
│  │  sms-neo4j:7474          [SMS relationships]      │     │
│  │  sms-qdrant:6333         [SMS embeddings]         │     │
│  │  hercules-postgres:5433  [Hercules cases]         │     │
│  │  hercules-elasticsearch  [OSINT docs]             │     │
│  │                                                     │     │
│  │  Access: READ-ONLY from development                │     │
│  │  Backup: Daily, critical                           │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │  DEVELOPMENT NETWORK (destiny_dev_network)         │     │
│  │                                                     │     │
│  │  destiny-postgres:5434   [Framework tests]        │     │
│  │  destiny-neo4j:7475      [Graph experiments]      │     │
│  │  destiny-qdrant:6335     [Embedding tests]        │     │
│  │  destiny-elasticsearch   [Doc parsing tests]      │     │
│  │                                                     │     │
│  │  Access: FULL read/write                           │     │
│  │  Backup: Optional (can recreate)                   │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 MAPOWANIE PORTÓW

### **Investigation Ports (EXISTING - DO NOT CHANGE):**

```
5432  → sms-postgres          (SMS investigation DB)
5433  → hercules-postgres     (Hercules cases)
6333  → sms-qdrant            (SMS embeddings)
7474  → sms-neo4j HTTP        (SMS graph browser)
7687  → sms-neo4j Bolt        (SMS graph queries)
9200  → hercules-elasticsearch (OSINT full-text search)
9300  → hercules-elasticsearch (cluster)
5601  → hercules-kibana       (OSINT dashboard)
```

**ZABRONIONE:** Modyfikacja tych portów!

---

### **Development Ports (NEW - Destiny Framework):**

```
5434  → destiny-postgres       (Development DB)
6335  → destiny-qdrant HTTP    (Development vectors)
6336  → destiny-qdrant gRPC    (Development vectors API)
7475  → destiny-neo4j HTTP     (Development graph browser)
7688  → destiny-neo4j Bolt     (Development graph queries)
9201  → destiny-elasticsearch  (Development search)
9301  → destiny-elasticsearch  (cluster)
6379  → destiny-redis          (Development cache)
```

**NOWE:** Różne porty = zero konfliktów!

---

## 🔧 IMPLEMENTACJA

### **1. docker-compose-dev.yml** (NEW FILE)

```yaml
# Destiny Development Environment
# Separate ports to avoid conflicts with investigation containers
# Data: CBA reports, framework tests, experiments
# Access: Full read/write

version: '3.8'

services:
  # Development PostgreSQL with pgvector
  postgres:
    image: ankane/pgvector:latest
    container_name: destiny-postgres
    environment:
      POSTGRES_DB: destiny_dev
      POSTGRES_USER: destiny
      POSTGRES_PASSWORD: destiny_dev_2024
      POSTGRES_HOST_AUTH_METHOD: trust
    ports:
      - "5434:5432"  # Different from investigation (5432)
    volumes:
      - destiny_postgres_data:/var/lib/postgresql/data
      - ./sql/init:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U destiny"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - destiny_dev_network
    restart: unless-stopped

  # Development Qdrant
  qdrant:
    image: qdrant/qdrant:latest
    container_name: destiny-qdrant
    ports:
      - "6335:6333"  # Different from investigation (6333)
      - "6336:6334"
    volumes:
      - destiny_qdrant_data:/qdrant/storage
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:6333/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5
    networks:
      - destiny_dev_network
    restart: unless-stopped

  # Development Neo4j
  neo4j:
    image: neo4j:5.13-community
    container_name: destiny-neo4j
    environment:
      NEO4J_AUTH: neo4j/destiny_dev_2024
      NEO4J_PLUGINS: '["apoc"]'
      NEO4J_dbms_memory_heap_max__size: 1G
    ports:
      - "7475:7474"  # Different from investigation (7474)
      - "7688:7687"  # Different from investigation (7687)
    volumes:
      - destiny_neo4j_data:/data
      - destiny_neo4j_logs:/logs
    healthcheck:
      test: ["CMD-SHELL", "cypher-shell -u neo4j -p destiny_dev_2024 'RETURN 1'"]
      interval: 30s
      timeout: 10s
      retries: 5
    networks:
      - destiny_dev_network
    restart: unless-stopped

  # Development Elasticsearch
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    container_name: destiny-elasticsearch
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9201:9200"  # Different from investigation (9200)
      - "9301:9300"
    volumes:
      - destiny_elasticsearch_data:/usr/share/elasticsearch/data
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5
    networks:
      - destiny_dev_network
    restart: unless-stopped

  # Development Redis (optional)
  redis:
    image: redis:7-alpine
    container_name: destiny-redis
    ports:
      - "6379:6379"
    volumes:
      - destiny_redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - destiny_dev_network
    restart: unless-stopped

networks:
  destiny_dev_network:
    name: destiny_dev_network
    driver: bridge

volumes:
  destiny_postgres_data:
    name: destiny_postgres_data
  destiny_qdrant_data:
    name: destiny_qdrant_data
  destiny_neo4j_data:
    name: destiny_neo4j_data
  destiny_neo4j_logs:
    name: destiny_neo4j_logs
  destiny_elasticsearch_data:
    name: destiny_elasticsearch_data
  destiny_redis_data:
    name: destiny_redis_data
```

---

### **2. .env.investigation** (READ-ONLY Access)

```bash
# ============================================
# INVESTIGATION ENVIRONMENT
# Purpose: Query existing investigation data
# Access: READ-ONLY
# Use for: Learning patterns, analysis
# ============================================

ENVIRONMENT=investigation
READ_ONLY=true

# SMS Investigation (DO NOT MODIFY!)
SMS_POSTGRES_HOST=localhost
SMS_POSTGRES_PORT=5432
SMS_POSTGRES_DB=sms  # Check actual name
SMS_POSTGRES_USER=postgres
SMS_POSTGRES_PASSWORD=<check_password>

SMS_QDRANT_URL=http://localhost:6333
SMS_NEO4J_URL=http://localhost:7474
SMS_NEO4J_USER=neo4j
SMS_NEO4J_PASSWORD=<check_password>

# Hercules Investigation (DO NOT MODIFY!)
HERCULES_POSTGRES_HOST=localhost
HERCULES_POSTGRES_PORT=5433
HERCULES_POSTGRES_DB=hercules  # Check actual name
HERCULES_POSTGRES_USER=postgres
HERCULES_POSTGRES_PASSWORD=<check_password>

HERCULES_ELASTICSEARCH_URL=http://localhost:9200
HERCULES_ELASTICSEARCH_USER=elastic
HERCULES_ELASTICSEARCH_PASSWORD=<check_password>

HERCULES_KIBANA_URL=http://localhost:5601

# IMPORTANT: READ-ONLY mode
# - Cannot create/modify/delete
# - Query only
# - Used for learning investigation patterns
ALLOW_WRITE=false
ALLOW_DELETE=false
ALLOW_SCHEMA_CHANGES=false
```

---

### **3. .env.development** (FULL Access)

```bash
# ============================================
# DEVELOPMENT ENVIRONMENT
# Purpose: Framework development and testing
# Access: FULL read/write
# Use for: CBA reports, experiments, testing
# ============================================

ENVIRONMENT=development
READ_ONLY=false

# Destiny Development (FULL ACCESS!)
POSTGRES_HOST=localhost
POSTGRES_PORT=5434  # ← Different!
POSTGRES_DB=destiny_dev
POSTGRES_USER=destiny
POSTGRES_PASSWORD=destiny_dev_2024

QDRANT_URL=http://localhost:6335  # ← Different!
QDRANT_API_KEY=  # None for development

NEO4J_URL=http://localhost:7475  # ← Different!
NEO4J_USER=neo4j
NEO4J_PASSWORD=destiny_dev_2024

ELASTICSEARCH_URL=http://localhost:9201  # ← Different!
ELASTICSEARCH_USER=  # None for development
ELASTICSEARCH_PASSWORD=

REDIS_URL=redis://localhost:6379

# FULL ACCESS mode
# - Can create/modify/delete
# - Can drop databases
# - Can experiment freely
ALLOW_WRITE=true
ALLOW_DELETE=true
ALLOW_SCHEMA_CHANGES=true

# LMStudio (shared between environments)
LMSTUDIO_URL=http://192.168.200.226:1234/v1
LMSTUDIO_MODEL=openai/gpt-oss-20b
```

---

### **4. config.py** (Environment-Aware)

```python
"""
Environment-aware configuration
Separates investigation data from development
"""

import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class DatabaseConfig:
    host: str
    port: int
    database: str
    user: str
    password: str
    read_only: bool = False

@dataclass
class VectorStoreConfig:
    url: str
    api_key: Optional[str] = None
    read_only: bool = False

@dataclass
class GraphDBConfig:
    url: str
    user: str
    password: str
    read_only: bool = False

class EnvironmentConfig:
    """Base class for environment configuration"""
    
    def __init__(self):
        self.environment = os.getenv('ENVIRONMENT', 'development')
        self.read_only = os.getenv('READ_ONLY', 'false').lower() == 'true'
    
    def validate(self):
        """Validate configuration"""
        raise NotImplementedError


class InvestigationConfig(EnvironmentConfig):
    """
    Configuration for investigation environment
    READ-ONLY access to SMS, Hercules, OSINT data
    """
    
    def __init__(self):
        super().__init__()
        
        # ENFORCE read-only for investigation
        if not self.read_only:
            raise PermissionError(
                "Investigation environment MUST be read-only! "
                "Set READ_ONLY=true in .env.investigation"
            )
        
        # SMS Investigation
        self.sms_postgres = DatabaseConfig(
            host=os.getenv('SMS_POSTGRES_HOST', 'localhost'),
            port=int(os.getenv('SMS_POSTGRES_PORT', '5432')),
            database=os.getenv('SMS_POSTGRES_DB', 'sms'),
            user=os.getenv('SMS_POSTGRES_USER', 'postgres'),
            password=os.getenv('SMS_POSTGRES_PASSWORD', ''),
            read_only=True  # ENFORCED!
        )
        
        self.sms_qdrant = VectorStoreConfig(
            url=os.getenv('SMS_QDRANT_URL', 'http://localhost:6333'),
            read_only=True  # ENFORCED!
        )
        
        self.sms_neo4j = GraphDBConfig(
            url=os.getenv('SMS_NEO4J_URL', 'http://localhost:7474'),
            user=os.getenv('SMS_NEO4J_USER', 'neo4j'),
            password=os.getenv('SMS_NEO4J_PASSWORD', ''),
            read_only=True  # ENFORCED!
        )
        
        # Hercules Investigation
        self.hercules_postgres = DatabaseConfig(
            host=os.getenv('HERCULES_POSTGRES_HOST', 'localhost'),
            port=int(os.getenv('HERCULES_POSTGRES_PORT', '5433')),
            database=os.getenv('HERCULES_POSTGRES_DB', 'hercules'),
            user=os.getenv('HERCULES_POSTGRES_USER', 'postgres'),
            password=os.getenv('HERCULES_POSTGRES_PASSWORD', ''),
            read_only=True  # ENFORCED!
        )
        
        self.hercules_elasticsearch = {
            'url': os.getenv('HERCULES_ELASTICSEARCH_URL', 'http://localhost:9200'),
            'user': os.getenv('HERCULES_ELASTICSEARCH_USER', 'elastic'),
            'password': os.getenv('HERCULES_ELASTICSEARCH_PASSWORD', ''),
            'read_only': True  # ENFORCED!
        }
    
    def validate(self):
        """Validate investigation config"""
        # Ensure all read_only flags are True
        assert self.sms_postgres.read_only, "SMS PostgreSQL must be read-only"
        assert self.sms_qdrant.read_only, "SMS Qdrant must be read-only"
        assert self.sms_neo4j.read_only, "SMS Neo4j must be read-only"
        assert self.hercules_postgres.read_only, "Hercules PostgreSQL must be read-only"
        
        print("✅ Investigation config validated (READ-ONLY enforced)")


class DevelopmentConfig(EnvironmentConfig):
    """
    Configuration for development environment
    FULL access to Destiny framework databases
    """
    
    def __init__(self):
        super().__init__()
        
        # Destiny Development (FULL ACCESS)
        self.postgres = DatabaseConfig(
            host=os.getenv('POSTGRES_HOST', 'localhost'),
            port=int(os.getenv('POSTGRES_PORT', '5434')),  # Different port!
            database=os.getenv('POSTGRES_DB', 'destiny_dev'),
            user=os.getenv('POSTGRES_USER', 'destiny'),
            password=os.getenv('POSTGRES_PASSWORD', 'destiny_dev_2024'),
            read_only=False  # FULL ACCESS!
        )
        
        self.qdrant = VectorStoreConfig(
            url=os.getenv('QDRANT_URL', 'http://localhost:6335'),  # Different port!
            api_key=os.getenv('QDRANT_API_KEY'),
            read_only=False  # FULL ACCESS!
        )
        
        self.neo4j = GraphDBConfig(
            url=os.getenv('NEO4J_URL', 'http://localhost:7475'),  # Different port!
            user=os.getenv('NEO4J_USER', 'neo4j'),
            password=os.getenv('NEO4J_PASSWORD', 'destiny_dev_2024'),
            read_only=False  # FULL ACCESS!
        )
        
        self.elasticsearch = {
            'url': os.getenv('ELASTICSEARCH_URL', 'http://localhost:9201'),  # Different port!
            'read_only': False  # FULL ACCESS!
        }
        
        self.redis = {
            'url': os.getenv('REDIS_URL', 'redis://localhost:6379')
        }
        
        # LMStudio (shared)
        self.lmstudio = {
            'url': os.getenv('LMSTUDIO_URL', 'http://192.168.200.226:1234/v1'),
            'model': os.getenv('LMSTUDIO_MODEL', 'openai/gpt-oss-20b')
        }
    
    def validate(self):
        """Validate development config"""
        # Ensure we're NOT using investigation ports
        assert self.postgres.port != 5432, "Cannot use investigation PostgreSQL port!"
        assert '6333' not in self.qdrant.url, "Cannot use investigation Qdrant port!"
        assert '7474' not in self.neo4j.url, "Cannot use investigation Neo4j port!"
        assert '9200' not in self.elasticsearch['url'], "Cannot use investigation Elasticsearch port!"
        
        print("✅ Development config validated (separate ports)")


def get_config() -> EnvironmentConfig:
    """
    Get configuration based on ENVIRONMENT variable
    
    Returns:
        InvestigationConfig or DevelopmentConfig
    """
    env = os.getenv('ENVIRONMENT', 'development').lower()
    
    if env == 'investigation':
        config = InvestigationConfig()
    elif env == 'development':
        config = DevelopmentConfig()
    else:
        raise ValueError(f"Unknown environment: {env}. Use 'investigation' or 'development'")
    
    config.validate()
    return config


# Usage:
if __name__ == "__main__":
    # Load appropriate .env file first
    from dotenv import load_dotenv
    
    env_file = os.getenv('ENV_FILE', '.env.development')
    load_dotenv(env_file)
    
    config = get_config()
    print(f"Loaded {config.environment} configuration")
    print(f"Read-only mode: {config.read_only}")
```

---

## 🚀 STARTUP PROCEDURE

### **Development Work (Default):**

```bash
# 1. Start development containers
docker-compose -f docker-compose-dev.yml up -d

# 2. Wait for health checks
docker-compose -f docker-compose-dev.yml ps

# 3. Initialize development databases
export ENV_FILE=.env.development
python3 scripts/init_dev_databases.sh

# 4. Load test data (CBA reports)
python3 scripts/load_test_data.py

# 5. Run tests
python3 profound_test.py

# ✅ Uses ports 5434, 6335, 7475, 9201
# ✅ Investigation data untouched!
```

### **Investigation Query (When Needed):**

```bash
# 1. Investigation containers already running
# (sms-*, hercules-*)

# 2. Use investigation config
export ENV_FILE=.env.investigation

# 3. Query investigation data (READ-ONLY)
python3 scripts/query_sms_patterns.py

# ✅ Uses ports 5432, 6333, 7474, 9200
# ✅ READ-ONLY enforced in code
# ✅ Cannot modify investigation data
```

---

## 🎯 VERIFICATION CHECKLIST

```bash
# Check port separation
docker ps --format "{{.Names}}: {{.Ports}}" | grep -E "postgres|qdrant|neo4j|elastic"

# Expected:
# sms-postgres: 5432          ← Investigation
# destiny-postgres: 5434       ← Development
# sms-qdrant: 6333            ← Investigation
# destiny-qdrant: 6335         ← Development
# sms-neo4j: 7474             ← Investigation
# destiny-neo4j: 7475          ← Development
# hercules-elasticsearch: 9200 ← Investigation
# destiny-elasticsearch: 9201  ← Development
```

---

## 📊 DATA FLOW MATRIX

| Data Type | Investigation Env | Development Env |
|-----------|------------------|-----------------|
| **SMS Cases** | ✅ Source (5432, 6333, 7474) | ❌ Not accessible |
| **Hercules OSINT** | ✅ Source (5433, 9200) | ❌ Not accessible |
| **CBA Reports** | ❌ Not relevant | ✅ Primary data (5434, 6335) |
| **Test Data** | ❌ NEVER | ✅ Primary data |
| **Framework Code** | ❌ Read-only queries | ✅ Full development |

---

## 🎯 BOTTOM LINE

```
╔═══════════════════════════════════════════════════╗
║                                                   ║
║  PRECYZYJNY PODZIAŁ:                              ║
║                                                   ║
║  🔐 INVESTIGATION (Existing)                      ║
║     Ports: 5432, 5433, 6333, 7474, 9200          ║
║     Data: SMS, Hercules, OSINT                    ║
║     Access: READ-ONLY from dev                    ║
║     Containers: sms-*, hercules-*                 ║
║     DO NOT MODIFY!                                ║
║                                                   ║
║  🧪 DEVELOPMENT (New)                             ║
║     Ports: 5434, 6335, 7475, 9201                ║
║     Data: CBA reports, tests                      ║
║     Access: FULL read/write                       ║
║     Containers: destiny-*                         ║
║     Safe to experiment!                           ║
║                                                   ║
║  ZERO CONFLICTS! ✅                               ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
```

**Ready to implement? Tworzę pliki teraz!** 🚀
