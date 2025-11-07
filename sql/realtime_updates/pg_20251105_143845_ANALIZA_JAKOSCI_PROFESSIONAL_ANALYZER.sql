INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'ANALIZA_JAKOSCI_PROFESSIONAL_ANALYZER.md',
    'general_documentation',
    '📊 ANALIZA JAKOŚCI PROFESSIONAL ANALYZER',
    '# 📊 ANALIZA JAKOŚCI PROFESSIONAL ANALYZER
## Szczegółowy raport z testu pełnej analizy CBA

**Data testu:** 2024-11-05  
**Case ID:** professional_analysis_20251105_143753  
**Czas wykonania:** 30.6s ',
    274,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();