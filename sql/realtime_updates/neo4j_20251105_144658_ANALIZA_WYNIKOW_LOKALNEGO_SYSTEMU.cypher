// Create document node
MERGE (d:Document {file_path: 'ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU.md'})
SET d.title = '📊 ANALIZA WYNIKÓW LOKALNEGO SYSTEMU',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);