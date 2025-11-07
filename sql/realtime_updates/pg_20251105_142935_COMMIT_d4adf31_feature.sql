INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/auto-generated/2025-11-05/COMMIT_d4adf31_feature.md',
    'general_documentation',
    'Add professional CBA analysis and implementation guide',
    '# Add professional CBA analysis and implementation guide

**Auto-Generated Documentation**

**Date:** 2025-11-05 14:29:35
**Commit:** `d4adf31`
**Type:** Feature
**Author:** artur

---

## 📝 Commit Me',
    78,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();