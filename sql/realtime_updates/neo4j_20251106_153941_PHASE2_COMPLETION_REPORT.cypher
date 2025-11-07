// Create document node
MERGE (d:Document {file_path: 'PHASE2_COMPLETION_REPORT.md'})
SET d.title = 'Phase 2 Completion Report: Full Team Integration',
    d.document_type = 'analysis',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'analysis'})
MERGE (d)-[:IS_TYPE]->(dt);