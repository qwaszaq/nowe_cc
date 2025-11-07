INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'PRECYZYJNY_PODZIAL.md',
    'general_documentation',
    '🔒 PRECYZYJNY PODZIAŁ: Investigation vs Development',
    '# 🔒 PRECYZYJNY PODZIAŁ: Investigation vs Development

**Data:** 5 Listopada 2024  
**Cel:** Absolutna separacja danych śledczych od rozwoju systemu

---

## 📋 INWENTARYZACJA - Co Mamy Obecnie

### **I',
    676,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();