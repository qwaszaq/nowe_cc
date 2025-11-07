// Create document node
MERGE (d:Document {file_path: 'FINAL_EXTRACTION_REPORT.md'})
SET d.title = 'Final Extraction Quality Report: Manual vs Automated Comparison',
    d.document_type = 'analysis',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'analysis'})
MERGE (d)-[:IS_TYPE]->(dt);