// Create document node
MERGE (d:Document {file_path: 'LMSTUDIO_INTEGRATION_COMPLETE.md'})
SET d.title = '🎉 LMStudio Integration - COMPLETE!',
    d.document_type = 'team_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'team_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);