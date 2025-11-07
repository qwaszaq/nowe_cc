// Create document node
MERGE (d:Document {file_path: 'docs/auto-generated/2025-11-07/COMMIT_71fe32a_documentation.md'})
SET d.title = 'Add multi-year PDF analysis plan + Phase 1 enhanced prompts',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);