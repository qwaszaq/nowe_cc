INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'SEPARACJA_DANYCH_DEVELOPMENT.md',
    'general_documentation',
    '🔒 SEPARACJA: Investigation Data vs Development System',
    '# 🔒 SEPARACJA: Investigation Data vs Development System

**Data:** 5 Listopada 2024  
**Critical Issue:** Musimy rozdzielić dane śledcze od rozwoju systemu!

---

## ⚠️ PROBLEM - Nie Możemy Mieszać!

',
    487,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();