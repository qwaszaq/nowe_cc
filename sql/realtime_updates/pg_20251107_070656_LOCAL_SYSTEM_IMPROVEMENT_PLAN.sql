INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'LOCAL_SYSTEM_IMPROVEMENT_PLAN.md',
    'architecture',
    'Local LLM System Improvement Plan',
    '# Local LLM System Improvement Plan

**Objective:** Maximize local LLM effectiveness to match Claude-level analysis quality
**Current Status:** Local system reaches correct conclusions but lacks sever',
    882,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();