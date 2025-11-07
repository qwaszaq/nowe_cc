// Create document node
MERGE (d:Document {file_path: 'RESULTS_STORAGE_ARCHITECTURE.md'})
SET d.title = '🗂️ Results Storage Architecture - Design Document',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);