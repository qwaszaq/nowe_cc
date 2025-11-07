// Create document node
MERGE (d:Document {file_path: 'CBA_FULL_CONTENT_ANALYSIS.md'})
SET d.title = '🔍 CBA - PEŁNA ANALIZA TREŚCI DOKUMENTÓW',
    d.document_type = 'analysis',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'analysis'})
MERGE (d)-[:IS_TYPE]->(dt);