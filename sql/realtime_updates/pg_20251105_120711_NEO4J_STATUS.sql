INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'NEO4J_STATUS.md',
    'status_report',
    '🕸️ NEO4J STATUS - Weryfikacja',
    '# 🕸️ NEO4J STATUS - Weryfikacja

**Data:** 5 Listopada 2024

---

## ✅ NEO4J DZIAŁA!

```bash
# Kontener uruchomiony:
sms-neo4j    Up 15 hours    0.0.0.0:7474->7474/tcp

# HTTP endpoint odpowiada:
cur',
    148,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();