INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'WNIOSKI_ARTUR.md',
    'team_documentation',
    '🎯 PROFOUND TEST - WNIOSKI DLA ARTURA',
    '# 🎯 PROFOUND TEST - WNIOSKI DLA ARTURA

## TL;DR

```
✅ PARSING: DZIAŁA IDEALNIE (912k chars, 13 PDFów)
✅ WORKFLOW: DZIAŁA AUTONOMICZNIE  
✅ LMSTUDIO: POŁĄCZONY I GOTOWY
❌ ANALYSIS: NIE DZIAŁA (3 bugi',
    455,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();