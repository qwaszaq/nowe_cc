// Create document node
MERGE (d:Document {file_path: 'FIXES_COMPLETE_SUCCESS.md'})
SET d.title = '🎉 FIXES COMPLETE - SYSTEM DZIAŁA!',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);