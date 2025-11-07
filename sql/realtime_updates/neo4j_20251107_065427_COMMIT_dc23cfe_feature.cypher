// Create document node
MERGE (d:Document {file_path: 'docs/auto-generated/2025-11-07/COMMIT_dc23cfe_feature.md'})
SET d.title = 'Complete multi-agent intelligence system with local/Claude comparison',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);