INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/auto-generated/2025-11-06/COMMIT_3d81426_feature.md',
    'general_documentation',
    'feat(ai-extraction): Integrate E5 semantic matching + LLM validation for financial data extraction',
    '# feat(ai-extraction): Integrate E5 semantic matching + LLM validation for financial data extraction

**Auto-Generated Documentation**

**Date:** 2025-11-06 21:01:40
**Commit:** `3d81426`
**Type:** Fe',
    142,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();