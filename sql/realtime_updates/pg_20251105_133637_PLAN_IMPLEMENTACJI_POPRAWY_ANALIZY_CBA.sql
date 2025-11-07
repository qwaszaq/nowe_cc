INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/implementation/PLAN_IMPLEMENTACJI_POPRAWY_ANALIZY_CBA.md',
    'architecture',
    '🚀 PLAN IMPLEMENTACJI POPRAWY ANALIZY CBA',
    '# 🚀 PLAN IMPLEMENTACJI POPRAWY ANALIZY CBA

**Data:** 2024-11-05  
**Wersja:** 1.0  
**Status:** Gotowy do realizacji

---

## 📋 EXECUTIVE SUMMARY

Plan implementacji poprawy systemu analizy raportów ',
    528,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();