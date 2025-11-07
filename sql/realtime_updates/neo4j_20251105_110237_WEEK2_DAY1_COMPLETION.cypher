// Create document node
MERGE (d:Document {file_path: 'WEEK2_DAY1_COMPLETION.md'})
SET d.title = '🚀 WEEK 2 - DAY 1 COMPLETION REPORT',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);