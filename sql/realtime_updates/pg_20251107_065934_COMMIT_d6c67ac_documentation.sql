INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/auto-generated/2025-11-07/COMMIT_d6c67ac_documentation.md',
    'general_documentation',
    'Add comprehensive system completion report',
    '# Add comprehensive system completion report

**Auto-Generated Documentation**

**Date:** 2025-11-07 06:59:33
**Commit:** `d6c67ac`
**Type:** Documentation
**Author:** artur

---

## 📝 Commit Message
',
    58,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();