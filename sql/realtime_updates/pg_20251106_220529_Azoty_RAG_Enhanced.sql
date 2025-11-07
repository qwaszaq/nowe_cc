INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'output/intelligence_reports/Azoty_RAG_Enhanced.md',
    'general_documentation',
    'Comprehensive Intelligence Report: Grupa Azoty S.A.',
    '# Comprehensive Intelligence Report: Grupa Azoty S.A.

**Report Date:** 2025-11-06
**Industry:** Chemicals & Fertilizers
**Currency:** PLN (thousands)
**Analysis Period:** 2023
**Analysis Method:** Lo',
    333,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();