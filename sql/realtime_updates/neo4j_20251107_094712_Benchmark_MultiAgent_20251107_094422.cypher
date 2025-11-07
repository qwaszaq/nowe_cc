// Create document node
MERGE (d:Document {file_path: 'output/intelligence_reports/Benchmark_MultiAgent_20251107_094422.md'})
SET d.title = 'Untitled',
    d.document_type = 'team_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'team_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);