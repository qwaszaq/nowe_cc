INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU.md',
    'general_documentation',
    '📊 ANALIZA WYNIKÓW LOKALNEGO SYSTEMU',
    '# 📊 ANALIZA WYNIKÓW LOKALNEGO SYSTEMU
## Ocena analizy przeprowadzonej przez system on-premise

**Data:** 2024-11-05  
**System:** Local Professional Analyzer (fully autonomous)  
**Case ID:** profess',
    281,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();