INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'testdocsLLM/README.md',
    'general_documentation',
    'Test Documents for LLM Testing',
    '# Test Documents for LLM Testing

## Folder do testowania systemu

Wrzuć tutaj dokumenty testowe (PDF, Excel, txt, etc.) do przetestowania autonomicznego systemu.

## Jak używać:

```bash
# Po dodaniu',
    39,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();