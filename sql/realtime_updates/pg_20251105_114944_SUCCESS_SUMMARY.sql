INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'SUCCESS_SUMMARY.md',
    'status_report',
    '🎉 SUKCES - SYSTEM NAPRAWIONY I DZIAŁA!',
    '# 🎉 SUKCES - SYSTEM NAPRAWIONY I DZIAŁA!

## TL;DR

```
PRZED: 0% quality, pusty output, LMStudio nie używany
PO:    100% quality, 20k chars analysis, LMStudio aktywny!

Czas naprawy: 2 godziny
Fixes:',
    201,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();