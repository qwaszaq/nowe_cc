INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'MULTI_YEAR_PDF_COMPARISON.md',
    'general_documentation',
    'Multi-Year PDF Analysis - System Comparison',
    '# Multi-Year PDF Analysis - System Comparison
## Grupa Azoty S.A. Intelligence Reports (2022-2024)

**Date**: 2025-11-07 07:55:56

---

## Executive Summary

This report compares three intelligence sy',
    83,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();