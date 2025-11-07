INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'GRAF_RELACJI_STATUS.md',
    'status_report',
    '🕸️ GRAF RELACJI - Status Implementacji',
    '# 🕸️ GRAF RELACJI - Status Implementacji

**Data:** 5 Listopada 2024  
**Pytanie:** Czy mamy lokalny graf relacji z heurystyką i semantyką?

---

## 📊 SZYBKA ODPOWIEDŹ

```
Neo4j (Full Graph DB):     ',
    633,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();