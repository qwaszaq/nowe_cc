INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'reports/EWALUACJA_SYSTEMU_CBA_SUMMARY.md',
    'status_report',
    '✅ EWALUACJA SYSTEMU ANALIZY CBA - RAPORT KOŃCOWY',
    '# ✅ EWALUACJA SYSTEMU ANALIZY CBA - RAPORT KOŃCOWY

**Data:** 2024-11-05  
**Test:** Pełna analiza 13 raportów CBA  
**Status:** ✅ **SUKCES**

---

## 🎯 PODSUMOWANIE WYKONAWCZE

### ✅ **GŁÓWNE OSIĄGNI',
    124,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();