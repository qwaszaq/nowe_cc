// Create document node
MERGE (d:Document {file_path: 'INTELLIGENT_EXTRACTION_COMPLETE.md'})
SET d.title = 'Intelligent Multi-Source Extraction System - COMPLETE ✅',
    d.document_type = 'architecture',
    d.indexed_at = datetime(),
    d.source = 'realtime_watcher';

// Link to document type
MERGE (dt:DocumentType {name: 'architecture'})
MERGE (d)-[:IS_TYPE]->(dt);