// Create document node
MERGE (d:Document {file_path: 'reports/cba_analiza_merytoryczna_2024.md'})
SET d.title = '📊 ANALIZA MERYTORYCZNA RAPORTÓW CBA 2008-2024',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);