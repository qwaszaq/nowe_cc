// Create document node
MERGE (d:Document {file_path: 'PIPELINE_ANALITYCZNY_PELNY_OPIS.md'})
SET d.title = '🔄 PIPELINE ANALITYCZNY - PEŁNY OPIS PROCESU',
    d.document_type = 'team_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'team_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);