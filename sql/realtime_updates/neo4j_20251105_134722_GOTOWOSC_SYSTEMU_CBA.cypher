// Create document node
MERGE (d:Document {file_path: 'reports/GOTOWOSC_SYSTEMU_CBA.md'})
SET d.title = '✅ INTEGRACJA ZAKOŃCZONA - SYSTEM GOTOWY DO PRACY Z RAPORTAMI CBA',
    d.document_type = 'general_documentation',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'general_documentation'})
MERGE (d)-[:IS_TYPE]->(dt);