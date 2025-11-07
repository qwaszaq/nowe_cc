INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'POROWNANIE_SYSTEM_VS_AI_ANALYSIS.md',
    'analysis',
    '🔬 PORÓWNANIE: SYSTEM LOKALNY VS ANALIZA AI',
    '# 🔬 PORÓWNANIE: SYSTEM LOKALNY VS ANALIZA AI
## Jak analiza automatyczna wypada na tle profesjonalnej analizy AI

**Data:** 2024-11-05  
**System:** Local Professional Analyzer (7 faz)  
**Porównanie ',
    573,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();