INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'FULL_HOG_FINAL_STATUS.md',
    'status_report',
    '🚀 FULL HOG - FINAL STATUS',
    '# 🚀 FULL HOG - FINAL STATUS

**Date:** November 5, 2024  
**Branch:** `feature/week2-database-async-integration`  
**Status:** 🎉 **COMPLETE & OPERATIONAL**

---

## ✅ CO DOKŁADNIE ZOSTAŁO ZROBIONE

##',
    483,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();