INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'HOW_I_WOULD_ANALYZE_CBA_REPORTS.md',
    'analysis',
    '🔍 JAK ANALIZOWAŁBYM RAPORTY CBA',
    '# 🔍 JAK ANALIZOWAŁBYM RAPORTY CBA
## Professional Analysis Methodology

**Perspective:** AI Analyst with investigative capabilities  
**Document Type:** CBA Annual Reports (2008-2024)  
**Approach:** ',
    493,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();