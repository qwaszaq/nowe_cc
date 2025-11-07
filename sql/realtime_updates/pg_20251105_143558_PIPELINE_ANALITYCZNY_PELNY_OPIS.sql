INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'PIPELINE_ANALITYCZNY_PELNY_OPIS.md',
    'team_documentation',
    '🔄 PIPELINE ANALITYCZNY - PEŁNY OPIS PROCESU',
    '# 🔄 PIPELINE ANALITYCZNY - PEŁNY OPIS PROCESU
## Jak działa system analizy dokumentów CBA

**Data:** 2024-11-05  
**System:** Autonomous Document Analysis System  
**Zakres:** Od skanowania folderu do',
    1014,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();