// Create document node
MERGE (d:Document {file_path: 'output/intelligence_reports/Azoty_RAG_Enhanced.md'})
SET d.title = 'Comprehensive Intelligence Report: Grupa Azoty S.A.',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);