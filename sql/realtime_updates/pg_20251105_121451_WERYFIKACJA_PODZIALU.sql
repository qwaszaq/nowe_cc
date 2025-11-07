INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'WERYFIKACJA_PODZIALU.md',
    'general_documentation',
    '✅ WERYFIKACJA PODZIAŁU - Investigation vs Development',
    '# ✅ WERYFIKACJA PODZIAŁU - Investigation vs Development

**Data:** 5 Listopada 2024

---

## 📊 FINAL PORT ALLOCATION

### **INVESTIGATION Environment (Production - DO NOT MODIFY)**

```
Container Name',
    295,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();