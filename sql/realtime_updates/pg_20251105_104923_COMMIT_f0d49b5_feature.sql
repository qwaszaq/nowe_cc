INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/auto-generated/2025-11-05/COMMIT_f0d49b5_feature.md',
    'team_documentation',
    'Complete Week 1 Foundation - Hybrid Multi-Agent System',
    '# Complete Week 1 Foundation - Hybrid Multi-Agent System

**Auto-Generated Documentation**

**Date:** 2025-11-05 10:49:23
**Commit:** `f0d49b5`
**Type:** Feature
**Author:** artur

---

## 📝 Commit Me',
    938,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();