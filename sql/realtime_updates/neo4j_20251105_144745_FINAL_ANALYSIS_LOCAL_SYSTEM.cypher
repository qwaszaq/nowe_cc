// Create document node
MERGE (d:Document {file_path: 'FINAL_ANALYSIS_LOCAL_SYSTEM.md'})
SET d.title = '✅ ANALIZA WYNIKÓW LOKALNEGO SYSTEMU - KOŃCOWY RAPORT',
    d.document_type = 'analysis',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'analysis'})
MERGE (d)-[:IS_TYPE]->(dt);