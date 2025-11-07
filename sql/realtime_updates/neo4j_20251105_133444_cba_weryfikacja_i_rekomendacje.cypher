// Create document node
MERGE (d:Document {file_path: 'reports/cba_weryfikacja_i_rekomendacje.md'})
SET d.title = '🔍 WERYFIKACJA ANALIZY MERYTORYCZNEJ CBA - RAPORT KRYTYCZNY',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);