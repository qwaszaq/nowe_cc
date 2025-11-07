// Create document node
MERGE (d:Document {file_path: 'ANALIZA_CBA_2008-2024.md'})
SET d.title = 'ANALIZA RAPORTÓW CBA 2008-2024',
    d.document_type = 'protocol',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'protocol'})
MERGE (d)-[:IS_TYPE]->(dt);