// Create document node
MERGE (d:Document {file_path: 'COMPREHENSIVE_STATUS_REPORT.md'})
SET d.title = '📊 Comprehensive Status Report',
    d.document_type = 'analysis',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'analysis'})
MERGE (d)-[:IS_TYPE]->(dt);