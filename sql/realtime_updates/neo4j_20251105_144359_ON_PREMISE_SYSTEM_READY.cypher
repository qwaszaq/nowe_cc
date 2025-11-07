// Create document node
MERGE (d:Document {file_path: 'ON_PREMISE_SYSTEM_READY.md'})
SET d.title = '✅ SYSTEM ON-PREMISE - GOTOWY DO DEPLOYMENT',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);