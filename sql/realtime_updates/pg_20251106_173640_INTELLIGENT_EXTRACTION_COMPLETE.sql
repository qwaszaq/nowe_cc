INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'INTELLIGENT_EXTRACTION_COMPLETE.md',
    'architecture',
    'Intelligent Multi-Source Extraction System - COMPLETE ✅',
    '# Intelligent Multi-Source Extraction System - COMPLETE ✅

**Date:** 2025-11-06
**Status:** Fully Implemented & Tested
**Achievement:** Full-hog implementation of intelligent multi-source financial da',
    519,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();