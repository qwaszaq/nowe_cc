// Create document node
MERGE (d:Document {file_path: 'output/intelligence_reports/Azoty_MultiAgent_20251106_222059.md'})
SET d.title = 'Multi-Agent Intelligence Report: Grupa Azoty S.A.',
    d.document_type = 'team_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'team_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);