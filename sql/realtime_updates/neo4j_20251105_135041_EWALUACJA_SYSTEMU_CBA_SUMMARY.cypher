// Create document node
MERGE (d:Document {file_path: 'reports/EWALUACJA_SYSTEMU_CBA_SUMMARY.md'})
SET d.title = '✅ EWALUACJA SYSTEMU ANALIZY CBA - RAPORT KOŃCOWY',
    d.document_type = 'status_report',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'status_report'})
MERGE (d)-[:IS_TYPE]->(dt);