INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'COMPREHENSIVE_STATUS_REPORT.md',
    'analysis',
    '📊 Comprehensive Status Report',
    '# 📊 Comprehensive Status Report
## Multi-Year PDF Analysis System - Grupa Azoty S.A.

**Date**: 2025-11-07  
**Session Summary**: Priority 1 & 2 Gap Fixes Complete  
**Overall Status**: ✅ **4 out of 5',
    273,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();