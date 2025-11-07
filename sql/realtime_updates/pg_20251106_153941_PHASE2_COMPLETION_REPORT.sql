INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'PHASE2_COMPLETION_REPORT.md',
    'analysis',
    'Phase 2 Completion Report: Full Team Integration',
    '# Phase 2 Completion Report: Full Team Integration

**Date:** 2025-11-06
**System:** Destiny Multi-Agent Investigation Framework
**Phase:** Phase 2 - Full Analytical Team LLM Integration
**Status:** ✅',
    557,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();