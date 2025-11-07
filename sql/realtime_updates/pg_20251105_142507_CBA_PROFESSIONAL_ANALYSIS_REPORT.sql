INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'CBA_PROFESSIONAL_ANALYSIS_REPORT.md',
    'analysis',
    '🔍 PROFESJONALNA ANALIZA RAPORTÓW CBA',
    '# 🔍 PROFESJONALNA ANALIZA RAPORTÓW CBA
## Comprehensive Multi-Dimensional Analysis (2008-2024)

**Data Analizy:** 2025-11-05 14:25:06  
**Metodologia:** 7-Phase Professional Analysis  
**Dokumenty:** ',
    120,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();