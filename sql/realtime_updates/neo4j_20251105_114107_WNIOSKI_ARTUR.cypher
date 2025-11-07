// Create document node
MERGE (d:Document {file_path: 'WNIOSKI_ARTUR.md'})
SET d.title = '🎯 PROFOUND TEST - WNIOSKI DLA ARTURA',
    d.document_type = 'team_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'team_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);