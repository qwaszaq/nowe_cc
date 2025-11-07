// Create document node
MERGE (d:Document {file_path: 'GRAF_RELACJI_STATUS.md'})
SET d.title = '🕸️ GRAF RELACJI - Status Implementacji',
    d.document_type = 'status_report',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'status_report'})
MERGE (d)-[:IS_TYPE]->(dt);