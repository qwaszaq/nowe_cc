// Create document node
MERGE (d:Document {file_path: 'HOW_TO_TEACH_SYSTEM_PROFESSIONAL_ANALYSIS.md'})
SET d.title = '🎓 JAK NAUCZYĆ SYSTEM AUTOMATYCZNEJ ANALIZY RAPORTÓW CBA',
    d.document_type = 'analysis',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'analysis'})
MERGE (d)-[:IS_TYPE]->(dt);