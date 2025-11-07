// Create document node
MERGE (d:Document {file_path: 'WYSZUKIWANIE_STATUS.md'})
SET d.title = '🔍 STATUS WYSZUKIWANIA - Co Mamy Zaimplementowane?',
    d.document_type = 'status_report',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'status_report'})
MERGE (d)-[:IS_TYPE]->(dt);