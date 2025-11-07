INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'RESULTS_STORAGE_SEPARATION.md',
    'general_documentation',
    '🔀 Results Storage - Investigation vs Development',
    '# 🔀 Results Storage - Investigation vs Development

**CRITICAL:** System ma DWA całkowicie oddzielne środowiska!

---

## 📊 Podział Środowisk

### **🔬 INVESTIGATION (Production)**
```
Purpose:  Real i',
    398,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();