INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'output/intelligence_reports/Azoty_MultiAgent_20251106_222059.md',
    'team_documentation',
    'Multi-Agent Intelligence Report: Grupa Azoty S.A.',
    '# Multi-Agent Intelligence Report: Grupa Azoty S.A.

**Generated:** 2025-11-06T22:20:59.643381
**Model:** openai/gpt-oss-20b
**Agents:** 6
**Generation Time:** 80.32s
**RAG:** True

---

**COMPREHENSI',
    154,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();