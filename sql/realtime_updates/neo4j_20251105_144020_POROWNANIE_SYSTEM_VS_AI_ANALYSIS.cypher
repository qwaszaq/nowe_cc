// Create document node
MERGE (d:Document {file_path: 'POROWNANIE_SYSTEM_VS_AI_ANALYSIS.md'})
SET d.title = '🔬 PORÓWNANIE: SYSTEM LOKALNY VS ANALIZA AI',
    d.document_type = 'analysis',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'analysis'})
MERGE (d)-[:IS_TYPE]->(dt);