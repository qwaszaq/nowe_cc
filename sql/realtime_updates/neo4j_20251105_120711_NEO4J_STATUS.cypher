// Create document node
MERGE (d:Document {file_path: 'NEO4J_STATUS.md'})
SET d.title = '🕸️ NEO4J STATUS - Weryfikacja',
    d.document_type = 'status_report',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'status_report'})
MERGE (d)-[:IS_TYPE]->(dt);