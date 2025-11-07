INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'WYSZUKIWANIE_STATUS.md',
    'status_report',
    '🔍 STATUS WYSZUKIWANIA - Co Mamy Zaimplementowane?',
    '# 🔍 STATUS WYSZUKIWANIA - Co Mamy Zaimplementowane?

**Data:** 5 Listopada 2024  
**Status:** Częściowo zaimplementowane

---

## 📊 PODSUMOWANIE

```
✅ SEMANTYCZNE:     Zaimplementowane (80%)
⚠️  HEUR',
    538,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();