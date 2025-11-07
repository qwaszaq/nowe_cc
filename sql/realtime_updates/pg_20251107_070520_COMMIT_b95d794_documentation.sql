INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/auto-generated/2025-11-07/COMMIT_b95d794_documentation.md',
    'general_documentation',
    'Add comprehensive local LLM improvement plan',
    '# Add comprehensive local LLM improvement plan

**Auto-Generated Documentation**

**Date:** 2025-11-07 07:05:19
**Commit:** `b95d794`
**Type:** Documentation
**Author:** artur

---

## 📝 Commit Messag',
    70,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();