INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/auto-generated/2025-11-06/COMMIT_9c14593_feature.md',
    'architecture',
    'feat(intelligent-extraction): Complete multi-source extraction system',
    '# feat(intelligent-extraction): Complete multi-source extraction system

**Auto-Generated Documentation**

**Date:** 2025-11-06 17:37:24
**Commit:** `9c14593`
**Type:** Feature
**Author:** artur

---
',
    267,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();