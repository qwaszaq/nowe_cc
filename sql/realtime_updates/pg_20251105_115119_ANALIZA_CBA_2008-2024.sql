INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'ANALIZA_CBA_2008-2024.md',
    'protocol',
    'ANALIZA RAPORTÓW CBA 2008-2024',
    '# ANALIZA RAPORTÓW CBA 2008-2024

**Źródło:** Autonomous System Analysis  
**Data:** 5 Listopada 2024  
**Dokumenty:** 13 raportów CBA (912,156 znaków)  
**Agenci:** Legal, Risk, Architect

---

## 📄 ',
    245,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();