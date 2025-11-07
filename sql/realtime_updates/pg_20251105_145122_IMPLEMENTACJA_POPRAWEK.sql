INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'IMPLEMENTACJA_POPRAWEK.md',
    'general_documentation',
    '✅ IMPLEMENTACJA POPRAWEK JAKOŚCI ANALIZY',
    '# ✅ IMPLEMENTACJA POPRAWEK JAKOŚCI ANALIZY

## 📋 Zaimplementowane Poprawki

### 1. ✅ Parsowanie Tabel PDF (pdfplumber)

**Lokalizacja:** `src/analysis/quantitative_extractor.py`

**Zmiany:**
- Dodano ',
    131,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();