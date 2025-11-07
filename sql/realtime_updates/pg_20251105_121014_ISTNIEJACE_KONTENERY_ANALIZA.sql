INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'ISTNIEJACE_KONTENERY_ANALIZA.md',
    'general_documentation',
    '🔍 ISTNIEJĄCE KONTENERY - Analiza',
    '# 🔍 ISTNIEJĄCE KONTENERY - Analiza

**Data:** 5 Listopada 2024  
**Problem:** Mamy już działające kontenery z danymi!

---

## ✅ CO MAMY URUCHOMIONE

```
┌────────────────────────┬─────────────────┬──',
    337,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();