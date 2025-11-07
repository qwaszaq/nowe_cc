INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'CBA_PROFESSIONAL_ANALYSIS_FINAL.md',
    'analysis',
    '🔍 PROFESJONALNA ANALIZA RAPORTÓW CBA - FINAL',
    '# 🔍 PROFESJONALNA ANALIZA RAPORTÓW CBA - FINAL
## Comprehensive Multi-Dimensional Analysis (2008-2024)

**Data Analizy:** 2025-11-05 14:27:57  
**Metodologia:** 7-Phase Professional Analysis  
**Dokum',
    105,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();