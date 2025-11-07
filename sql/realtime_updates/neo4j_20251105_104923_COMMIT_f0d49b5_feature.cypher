// Create document node
MERGE (d:Document {file_path: 'docs/auto-generated/2025-11-05/COMMIT_f0d49b5_feature.md'})
SET d.title = 'Complete Week 1 Foundation - Hybrid Multi-Agent System',
    d.document_type = 'team_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'team_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);