INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'ON_PREMISE_SYSTEM_READY.md',
    'architecture',
    '✅ SYSTEM ON-PREMISE - GOTOWY DO DEPLOYMENT',
    '# ✅ SYSTEM ON-PREMISE - GOTOWY DO DEPLOYMENT
## Pełna autonomia z lokalną interpretacją

**Data:** 2024-11-05  
**Status:** ✅ Gotowy na production (on-premise)  
**Architektura:** Fully autonomous, pr',
    245,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();