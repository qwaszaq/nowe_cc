INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'LOCAL_INTERPRETATION_LAYER.md',
    'general_documentation',
    '🏗️ ROZSZERZENIE SYSTEMU O LOKALNĄ INTERPRETACJĘ',
    '# 🏗️ ROZSZERZENIE SYSTEMU O LOKALNĄ INTERPRETACJĘ
## On-Premise Professional Analyzer z warstwą interpretacyjną

**Data:** 2024-11-05  
**Cel:** System w pełni on-premise z lokalną interpretacją przez',
    239,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();