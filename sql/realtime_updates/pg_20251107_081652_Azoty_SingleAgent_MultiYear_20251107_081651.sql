INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'output/intelligence_reports/Azoty_SingleAgent_MultiYear_20251107_081651.md',
    'team_documentation',
    'Comprehensive Intelligence Report: Grupa Azoty S.A.',
    '# Comprehensive Intelligence Report: Grupa Azoty S.A.

**Report Date:** 2025-11-07
**Industry:** Chemicals & Fertilizers
**Currency:** PLN (thousands)
**Analysis Period:** 2022, 2023, 2024
**Analysis ',
    324,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();