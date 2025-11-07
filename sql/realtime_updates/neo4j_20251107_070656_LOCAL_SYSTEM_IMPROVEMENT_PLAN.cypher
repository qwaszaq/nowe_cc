// Create document node
MERGE (d:Document {file_path: 'LOCAL_SYSTEM_IMPROVEMENT_PLAN.md'})
SET d.title = 'Local LLM System Improvement Plan',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);