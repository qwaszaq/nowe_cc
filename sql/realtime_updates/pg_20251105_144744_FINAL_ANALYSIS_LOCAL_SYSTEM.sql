INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'FINAL_ANALYSIS_LOCAL_SYSTEM.md',
    'analysis',
    '✅ ANALIZA WYNIKÓW LOKALNEGO SYSTEMU - KOŃCOWY RAPORT',
    '# ✅ ANALIZA WYNIKÓW LOKALNEGO SYSTEMU - KOŃCOWY RAPORT
## Ocena analizy przeprowadzonej przez system on-premise (całkowicie autonomicznie)

**Data:** 2024-11-05  
**System:** Local Professional Analyz',
    225,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();