// Create document node
MERGE (d:Document {file_path: 'docs/implementation/STRATEGIA_EMBEDDINGOW_JINA_VS_E5.md'})
SET d.title = '🎯 STRATEGIA WYBORU EMBEDDINGÓW: JINA vs E5/INTFLOAT',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);