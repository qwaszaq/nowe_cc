// Create document node
MERGE (d:Document {file_path: 'docs/auto-generated/2025-11-07/COMMIT_fb8cb6f_feature.md'})
SET d.title = 'Download 6 Azoty annual reports for multi-year analysis (2022-2024)',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);