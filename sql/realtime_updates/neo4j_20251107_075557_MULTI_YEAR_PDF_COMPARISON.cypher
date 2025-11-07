// Create document node
MERGE (d:Document {file_path: 'MULTI_YEAR_PDF_COMPARISON.md'})
SET d.title = 'Multi-Year PDF Analysis - System Comparison',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);