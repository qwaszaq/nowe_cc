INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'HOW_TO_TEACH_SYSTEM_PROFESSIONAL_ANALYSIS.md',
    'analysis',
    '🎓 JAK NAUCZYĆ SYSTEM AUTOMATYCZNEJ ANALIZY RAPORTÓW CBA',
    '# 🎓 JAK NAUCZYĆ SYSTEM AUTOMATYCZNEJ ANALIZY RAPORTÓW CBA
## Implementation Guide: Teaching AI System Professional Analysis

**Data:** 2024-11-05  
**Cel:** Przekonwertować profesjonalną metodologię a',
    1764,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();