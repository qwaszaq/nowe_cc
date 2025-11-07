// Create document node
MERGE (d:Document {file_path: 'docs/auto-generated/2025-11-07/COMMIT_b95d794_documentation.md'})
SET d.title = 'Add comprehensive local LLM improvement plan',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);