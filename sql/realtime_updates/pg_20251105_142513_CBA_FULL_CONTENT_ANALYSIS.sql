INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'CBA_FULL_CONTENT_ANALYSIS.md',
    'analysis',
    '🔍 CBA - PEŁNA ANALIZA TREŚCI DOKUMENTÓW',
    '# 🔍 CBA - PEŁNA ANALIZA TREŚCI DOKUMENTÓW
## Comprehensive Content Analysis (2008-2024)

**Data Analizy:** 2025-11-05 14:25:12  
**Analizowanych Dokumentów:** 13  
**Metoda:** Full PDF text extraction',
    618,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();