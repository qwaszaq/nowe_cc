INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'reports/cba_analiza_merytoryczna_2024.md',
    'general_documentation',
    '📊 ANALIZA MERYTORYCZNA RAPORTÓW CBA 2008-2024',
    '# 📊 ANALIZA MERYTORYCZNA RAPORTÓW CBA 2008-2024

**Data analizy:** 2024-11-05
**Zakres:** 13 raportów rocznych CBA
**Model:** LMStudio (openai/gpt-oss-20b)

---

# CZĘŚĆ 1: EFEKTYWNOŚĆ I METRYKI W CZA',
    282,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();