// Create document node
MERGE (d:Document {file_path: 'docs/implementation/PLAN_IMPLEMENTACJI_POPRAWY_ANALIZY_CBA.md'})
SET d.title = '🚀 PLAN IMPLEMENTACJI POPRAWY ANALIZY CBA',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);