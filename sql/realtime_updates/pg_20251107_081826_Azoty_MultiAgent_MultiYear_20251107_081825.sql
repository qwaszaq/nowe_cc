INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'output/intelligence_reports/Azoty_MultiAgent_MultiYear_20251107_081825.md',
    'team_documentation',
    'Untitled',
    '**COMPREHENSIVE INTELLIGENCE REPORT: Grupa Azoty S.A.**

═══════════════════════════════════════════════════════════════  

## EXECUTIVE SUMMARY  

Grupa Azoty is Poland’s largest fertilizer producer ',
    149,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();