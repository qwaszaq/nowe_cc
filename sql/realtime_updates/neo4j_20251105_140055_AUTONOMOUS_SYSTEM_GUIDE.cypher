// Create document node
MERGE (d:Document {file_path: 'AUTONOMOUS_SYSTEM_GUIDE.md'})
SET d.title = '🤖 AUTONOMOUS SYSTEM - User Guide',
    d.document_type = 'guide',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'guide'})
MERGE (d)-[:IS_TYPE]->(dt);