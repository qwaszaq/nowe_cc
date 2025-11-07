INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'RAG_SYSTEM_SUMMARY.md',
    'status_report',
    'RAG System Implementation Summary',
    '# RAG System Implementation Summary

**Date:** 2025-11-06
**Status:** ✅ **COMPLETE - Priority 3 (Week 4-5)**
**System:** Qdrant + E5 Embeddings + BGE Reranker + Intelligent Section Detection

---

## ',
    465,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();