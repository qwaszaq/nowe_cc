INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'FINAL_EXTRACTION_REPORT.md',
    'analysis',
    'Final Extraction Quality Report: Manual vs Automated Comparison',
    '# Final Extraction Quality Report: Manual vs Automated Comparison

**Date:** 2025-11-06
**Analyst:** Claude Code
**Test Subject:** Grupa Azoty Tarnów Annual Report 2024
**Objective:** Compare automate',
    632,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();