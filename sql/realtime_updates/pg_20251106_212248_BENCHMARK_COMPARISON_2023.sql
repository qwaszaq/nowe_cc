INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'BENCHMARK_COMPARISON_2023.md',
    'general_documentation',
    'Financial Extraction Quality Benchmark - Grupa Azoty 2023',
    '# Financial Extraction Quality Benchmark - Grupa Azoty 2023

**Test Date:** 2025-11-06
**Source Document:** Grupa Azoty Tarnów - Śródroczne skrócone skonsolidowane sprawozdanie finansowe (6-month repo',
    476,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();