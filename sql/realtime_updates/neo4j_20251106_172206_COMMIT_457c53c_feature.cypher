// Create document node
MERGE (d:Document {file_path: 'docs/auto-generated/2025-11-06/COMMIT_457c53c_feature.md'})
SET d.title = 'feat(round2): Implement text-based PDF extraction for Polish financial reports',
    d.document_type = 'team_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'team_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);