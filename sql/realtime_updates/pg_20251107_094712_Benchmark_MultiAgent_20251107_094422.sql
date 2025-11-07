INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'output/intelligence_reports/Benchmark_MultiAgent_20251107_094422.md',
    'team_documentation',
    'Untitled',
    '**COMPREHENSIVE INTELLIGENCE REPORT: Grupa Azoty S.A.**

═══════════════════════════════════════════════════════════════

## EXECUTIVE SUMMARY  

Overall Assessment Score: **38/100**  
Investment Reco',
    158,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();