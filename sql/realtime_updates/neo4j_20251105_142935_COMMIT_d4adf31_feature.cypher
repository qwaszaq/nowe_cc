// Create document node
MERGE (d:Document {file_path: 'docs/auto-generated/2025-11-05/COMMIT_d4adf31_feature.md'})
SET d.title = 'Add professional CBA analysis and implementation guide',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);