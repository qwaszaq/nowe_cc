INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/auto-generated/2025-11-06/COMMIT_457c53c_feature.md',
    'team_documentation',
    'feat(round2): Implement text-based PDF extraction for Polish financial reports',
    '# feat(round2): Implement text-based PDF extraction for Polish financial reports

**Auto-Generated Documentation**

**Date:** 2025-11-06 17:22:05
**Commit:** `457c53c`
**Type:** Feature
**Author:** ar',
    269,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();