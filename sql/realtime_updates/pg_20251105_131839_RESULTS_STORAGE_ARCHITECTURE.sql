INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'RESULTS_STORAGE_ARCHITECTURE.md',
    'architecture',
    '🗂️ Results Storage Architecture - Design Document',
    '# 🗂️ Results Storage Architecture - Design Document

**Date:** November 5, 2024  
**System:** Destiny Autonomous Analysis  
**Author:** Architecture Team

---

## 🎯 Design Goals

1. **Discoverable** -',
    584,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();