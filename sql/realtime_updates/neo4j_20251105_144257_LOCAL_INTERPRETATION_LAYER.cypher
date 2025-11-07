// Create document node
MERGE (d:Document {file_path: 'LOCAL_INTERPRETATION_LAYER.md'})
SET d.title = '🏗️ ROZSZERZENIE SYSTEMU O LOKALNĄ INTERPRETACJĘ',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);