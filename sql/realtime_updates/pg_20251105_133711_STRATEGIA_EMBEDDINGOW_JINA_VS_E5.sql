INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'docs/implementation/STRATEGIA_EMBEDDINGOW_JINA_VS_E5.md',
    'architecture',
    '🎯 STRATEGIA WYBORU EMBEDDINGÓW: JINA vs E5/INTFLOAT',
    '# 🎯 STRATEGIA WYBORU EMBEDDINGÓW: JINA vs E5/INTFLOAT

**Data:** 2024-11-05  
**Wersja:** 1.0  
**Kontekst:** Analiza raportów CBA i dokumentów strukturalnych

---

## 📊 EXECUTIVE SUMMARY

Szczegółowa',
    512,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();