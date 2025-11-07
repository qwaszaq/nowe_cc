// Create document node
MERGE (d:Document {file_path: 'HOW_I_WOULD_ANALYZE_CBA_REPORTS.md'})
SET d.title = '🔍 JAK ANALIZOWAŁBYM RAPORTY CBA',
    d.document_type = 'analysis',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'analysis'})
MERGE (d)-[:IS_TYPE]->(dt);