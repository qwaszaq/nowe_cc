INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/auto-generated/2025-11-07/COMMIT_71fe32a_documentation.md',
    'general_documentation',
    'Add multi-year PDF analysis plan + Phase 1 enhanced prompts',
    '# Add multi-year PDF analysis plan + Phase 1 enhanced prompts

**Auto-Generated Documentation**

**Date:** 2025-11-07 07:10:31
**Commit:** `71fe32a`
**Type:** Documentation
**Author:** artur

---

## ',
    75,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();