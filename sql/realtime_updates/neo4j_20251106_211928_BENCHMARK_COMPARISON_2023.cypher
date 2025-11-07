// Create document node
MERGE (d:Document {file_path: 'BENCHMARK_COMPARISON_2023.md'})
SET d.title = 'Financial Extraction Quality Benchmark - Grupa Azoty 2023',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);