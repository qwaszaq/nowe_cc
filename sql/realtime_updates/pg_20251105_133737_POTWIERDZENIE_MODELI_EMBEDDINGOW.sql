INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/implementation/POTWIERDZENIE_MODELI_EMBEDDINGOW.md',
    'general_documentation',
    '✅ POTWIERDZENIE MODELI EMBEDDINGÓW W LMSTUDIO',
    '# ✅ POTWIERDZENIE MODELI EMBEDDINGÓW W LMSTUDIO

**Data weryfikacji:** 2024-11-05  
**Serwer:** http://192.168.200.226:1234/v1

---

## 📊 DOSTĘPNE MODELE EMBEDDINGÓW

### ✅ **1. JINA V4 TEXT RETRIEVAL',
    92,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();