INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/architecture/RAG_CAG_STRATEGY.md',
    'architecture',
    '🚀 RAG + CAG Strategy - Context Window Revolution',
    '# 🚀 RAG + CAG Strategy - Context Window Revolution

## Problem: 44k vs 200k Context Window

```
LOCAL LLM:    44,000 tokens  😰
CLAUDE:      200,000 tokens  🎉

Challenge: 100 documents, 455 processing ',
    438,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();