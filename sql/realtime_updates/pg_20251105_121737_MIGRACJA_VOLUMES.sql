INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'MIGRACJA_VOLUMES.md',
    'general_documentation',
    '🔄 MIGRACJA VOLUMES - Stare vs Nowe',
    '# 🔄 MIGRACJA VOLUMES - Stare vs Nowe

**Data:** 5 Listopada 2024

---

## 🔍 SYTUACJA

### **Problem:**
Mieliśmy **DWA zestawy** Docker Compose:

1. **Stary:** `docker-compose.yml`
   - Volumes: `cours',
    172,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();