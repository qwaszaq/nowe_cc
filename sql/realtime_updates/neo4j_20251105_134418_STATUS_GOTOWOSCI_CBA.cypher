// Create document node
MERGE (d:Document {file_path: 'reports/STATUS_GOTOWOSCI_CBA.md'})
SET d.title = '✅ STATUS GOTOWOŚCI SYSTEMU DO PRACY Z RAPORTAMI CBA',
    d.document_type = 'status_report',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'status_report'})
MERGE (d)-[:IS_TYPE]->(dt);