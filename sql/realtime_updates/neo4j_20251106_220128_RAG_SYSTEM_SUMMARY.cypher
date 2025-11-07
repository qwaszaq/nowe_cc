// Create document node
MERGE (d:Document {file_path: 'RAG_SYSTEM_SUMMARY.md'})
SET d.title = 'RAG System Implementation Summary',
    d.document_type = 'status_report',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'status_report'})
MERGE (d)-[:IS_TYPE]->(dt);