INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'reports/EWALUACJA_SYSTEMU_CBA.md',
    'general_documentation',
    '📊 EWALUACJA SYSTEMU ANALIZY CBA - RAPORT KOŃCOWY',
    '# 📊 EWALUACJA SYSTEMU ANALIZY CBA - RAPORT KOŃCOWY

**Data ewaluacji:** 2024-11-05  
**Porównanie:** System stary (z halucynacjami) vs System nowy (z ekstrakcją)

---

## 🎯 EXECUTIVE SUMMARY

### ✅ **',
    403,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();