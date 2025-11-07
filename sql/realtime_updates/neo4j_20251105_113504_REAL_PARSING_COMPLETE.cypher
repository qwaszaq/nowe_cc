// Create document node
MERGE (d:Document {file_path: 'REAL_PARSING_COMPLETE.md'})
SET d.title = '✅ REAL PARSING - COMPLETE & WORKING!',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);