// Create document node
MERGE (d:Document {file_path: 'INVESTIGATIVE_INTEGRATION_COMPLETE.md'})
SET d.title = '🎉 INVESTIGATIVE INTEGRATION - COMPLETE',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);