// Create document node
MERGE (d:Document {file_path: 'docs/auto-generated/2025-11-06/COMMIT_9c14593_feature.md'})
SET d.title = 'feat(intelligent-extraction): Complete multi-source extraction system',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);