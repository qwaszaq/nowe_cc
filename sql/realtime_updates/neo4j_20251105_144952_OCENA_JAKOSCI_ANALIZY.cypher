// Create document node
MERGE (d:Document {file_path: 'OCENA_JAKOSCI_ANALIZY.md'})
SET d.title = '❌ OCENA JAKOŚCI ANALIZY - SZCZEGÓŁOWA WERYFIKACJA',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);