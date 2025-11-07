// Create document node
MERGE (d:Document {file_path: 'CBA_COMPREHENSIVE_ANALYSIS_2024.md'})
SET d.title = '🔍 CBA COMPREHENSIVE ANALYSIS 2024',
    d.document_type = 'analysis',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'analysis'})
MERGE (d)-[:IS_TYPE]->(dt);