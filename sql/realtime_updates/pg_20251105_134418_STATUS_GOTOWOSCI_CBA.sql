INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'reports/STATUS_GOTOWOSCI_CBA.md',
    'status_report',
    '✅ STATUS GOTOWOŚCI SYSTEMU DO PRACY Z RAPORTAMI CBA',
    '# ✅ STATUS GOTOWOŚCI SYSTEMU DO PRACY Z RAPORTAMI CBA

**Data:** 2024-11-05  
**Status:** ⚠️ **Częściowo gotowy** - podstawy działają, integracja wymaga ukończenia

---

## 🎯 CO DZIAŁA ✅

### **1. Eks',
    145,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();