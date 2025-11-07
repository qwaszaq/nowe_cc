// Create document node
MERGE (d:Document {file_path: 'docs/implementation/POTWIERDZENIE_MODELI_EMBEDDINGOW.md'})
SET d.title = '✅ POTWIERDZENIE MODELI EMBEDDINGÓW W LMSTUDIO',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);