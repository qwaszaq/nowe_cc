// Create document node
MERGE (d:Document {file_path: 'docs/auto-generated/2025-11-06/COMMIT_3d81426_feature.md'})
SET d.title = 'feat(ai-extraction): Integrate E5 semantic matching + LLM validation for financial data extraction',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);