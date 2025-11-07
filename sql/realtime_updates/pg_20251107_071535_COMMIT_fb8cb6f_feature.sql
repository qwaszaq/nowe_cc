INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/auto-generated/2025-11-07/COMMIT_fb8cb6f_feature.md',
    'general_documentation',
    'Download 6 Azoty annual reports for multi-year analysis (2022-2024)',
    '# Download 6 Azoty annual reports for multi-year analysis (2022-2024)

**Auto-Generated Documentation**

**Date:** 2025-11-07 07:15:34
**Commit:** `fb8cb6f`
**Type:** Feature
**Author:** artur

---

#',
    187,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();