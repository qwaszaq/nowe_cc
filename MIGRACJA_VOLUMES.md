# 🔄 MIGRACJA VOLUMES - Stare vs Nowe

**Data:** 5 Listopada 2024

---

## 🔍 SYTUACJA

### **Problem:**
Mieliśmy **DWA zestawy** Docker Compose:

1. **Stary:** `docker-compose.yml`
   - Volumes: `coursor-agents-destiny-folder_*`
   - Porty: 5432, 6333, 7474, 9200
   - **KONFLIKT z investigation containers!**
   - Status: Volumes utworzone, ale kontenery nigdy nie działały

2. **Nowy:** `docker-compose-dev.yml`
   - Volumes: `destiny_*`
   - Porty: 5434, 6335, 7475, 9201
   - **ZERO konfliktów!**
   - Status: Właśnie uruchomione

---

## 📦 VOLUMES - Co Mamy?

### **Stare Volumes (nie używane):**
```
coursor-agents-destiny-folder_postgres_data     (utworzony: 09:07:54)
coursor-agents-destiny-folder_qdrant_data       (utworzony: 09:07:54)
coursor-agents-destiny-folder_neo4j_data        (utworzony: 09:07:54)
coursor-agents-destiny-folder_elasticsearch_data (utworzony: 09:07:54)
```

**Status:** Sprawdzamy czy są tam jakieś dane...

### **Nowe Volumes (aktywne):**
```
destiny_postgres_data      (utworzony: 11:14:04) - AKTYWNY
destiny_qdrant_data        (utworzony: 11:14:04) - AKTYWNY
destiny_neo4j_data         (utworzony: 11:14:04) - AKTYWNY
destiny_elasticsearch_data (utworzony: 11:14:04) - AKTYWNY
```

**Status:** Czyste, świeże, działają!

---

## 📁 LOKALNE PLIKI (NIEZALEŻNE od volumes!)

**BARDZO WAŻNE:**
Twoje **lokalne pliki** są **BEZPIECZNE** i **NIEZALEŻNE** od Docker volumes!

```
testdocsLLM/         17MB  ✅ BEZPIECZNE (CBA reports)
analysis_reports/    68KB  ✅ BEZPIECZNE (raporty analizy)
batch_processed/     0B    ✅ BEZPIECZNE
batch_queue/         0B    ✅ BEZPIECZNE
helena_tasks/        ~MB   ✅ BEZPIECZNE
qdrant_pending/      ~MB   ✅ BEZPIECZNE
```

**Te pliki nie są w żadnym volume - są po prostu na dysku!**

---

## 🎯 DECYZJA - Co Dalej?

### **Opcja A: Migracja Danych (jeśli były)**

Jeśli w starych volumes były jakieś dane:

```bash
# 1. Stop nowych kontenerów
docker-compose -f docker-compose-dev.yml down

# 2. Migruj dane
docker run --rm \
  -v coursor-agents-destiny-folder_qdrant_data:/source \
  -v destiny_qdrant_data:/target \
  alpine sh -c "cp -a /source/. /target/"

# 3. Restart
docker-compose -f docker-compose-dev.yml up -d
```

### **Opcja B: Czysty Start (REKOMENDOWANE)**

Jeśli stare volumes są puste lub nieistotne:

```bash
# 1. Usuń stare volumes
docker volume rm coursor-agents-destiny-folder_postgres_data
docker volume rm coursor-agents-destiny-folder_qdrant_data
docker volume rm coursor-agents-destiny-folder_neo4j_data
docker volume rm coursor-agents-destiny-folder_elasticsearch_data

# 2. Nowe volumes już działają
docker-compose -f docker-compose-dev.yml ps

# 3. Załaduj dane z testdocsLLM
python3 profound_test.py
```

---

## ✅ CO JEST BEZPIECZNE?

```
✅ testdocsLLM/          - Twoje pliki PDF/Excel (17MB)
✅ analysis_reports/     - Raporty z analizy (68KB)
✅ helena_tasks/         - Zadania Helena
✅ qdrant_pending/       - Pending indexing
✅ Wszystkie skrypty Python
✅ Investigation data    - Całkowicie oddzielne!

❓ coursor-agents-destiny-folder_* volumes - sprawdzamy...
```

---

## 🚀 WORKFLOW PO MIGRACJI/CZYSZCZENIU

```bash
# 1. Development (nowe porty, czyste volumes)
export ENV_FILE=.env.development
docker-compose -f docker-compose-dev.yml up -d

# 2. Załaduj dane lokalne (testdocsLLM)
python3 profound_test.py

# 3. Dane zapisują się do nowych volumes
# destiny_qdrant_data, destiny_postgres_data, etc.

# 4. Investigation pozostaje nietknięte
curl http://localhost:6333/collections  # SMS data (143K vectors)
curl http://localhost:6335/collections  # Development data (fresh)
```

---

## 🎯 REKOMENDACJA

**CZYSTY START (Opcja B)** bo:

1. ✅ Stare kontenery NIGDY nie działały (konflikty portów)
2. ✅ Stare volumes prawdopodobnie puste
3. ✅ Lokalne pliki (testdocsLLM) są bezpieczne
4. ✅ Nowe volumes już działają poprawnie
5. ✅ Investigation data nietknięte

**Możemy bezpiecznie usunąć stare volumes i kontynuować z nowymi!**

---

## 📝 NASTĘPNE KROKI

Po sprawdzeniu zawartości starych volumes:

```bash
# Jeśli puste → usuń
docker volume rm coursor-agents-destiny-folder_postgres_data
docker volume rm coursor-agents-destiny-folder_qdrant_data
docker volume rm coursor-agents-destiny-folder_neo4j_data
docker volume rm coursor-agents-destiny-folder_elasticsearch_data

# Kontynuuj z nowymi
export ENV_FILE=.env.development
python3 profound_test.py
```
