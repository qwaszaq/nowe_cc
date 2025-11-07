INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'CBA_COMPREHENSIVE_ANALYSIS_2024.md',
    'analysis',
    '🔍 CBA COMPREHENSIVE ANALYSIS 2024',
    '# 🔍 CBA COMPREHENSIVE ANALYSIS 2024
## Wieloaspektowa Analiza Investigative - Centralne Biuro Antykorupcyjne

**Data Analizy:** 2024-11-05  
**System:** Autonomous Investigative Integration  
**Case I',
    524,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();