INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'AUTONOMOUS_SYSTEM_GUIDE.md',
    'guide',
    '🤖 AUTONOMOUS SYSTEM - User Guide',
    '# 🤖 AUTONOMOUS SYSTEM - User Guide

## Koncepcja: "Wskaż i Zapomnij"

System działa **w pełni autonomicznie**:

```
TY: "Przeanalizuj folder /data/documents/"
    ↓
SYSTEM AUTOMATYCZNIE:
  1. 🔍 Skanuj',
    433,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();