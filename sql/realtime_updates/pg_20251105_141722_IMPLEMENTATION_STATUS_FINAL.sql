INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'IMPLEMENTATION_STATUS_FINAL.md',
    'status_report',
    '📊 STATUS WDROŻENIA - RAPORT KOŃCOWY',
    '# 📊 STATUS WDROŻENIA - RAPORT KOŃCOWY
## Implementation Status Report

**Data:** 2024-11-05  
**Sesja:** Investigative System Integration & CBA Analysis  
**Status:** ✅ MAJOR MILESTONES COMPLETED

---',
    579,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();