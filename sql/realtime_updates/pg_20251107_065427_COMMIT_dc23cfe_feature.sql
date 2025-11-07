INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/auto-generated/2025-11-07/COMMIT_dc23cfe_feature.md',
    'architecture',
    'Complete multi-agent intelligence system with local/Claude comparison',
    '# Complete multi-agent intelligence system with local/Claude comparison

**Auto-Generated Documentation**

**Date:** 2025-11-07 06:54:26
**Commit:** `dc23cfe`
**Type:** Feature
**Author:** artur

---
',
    1988,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();