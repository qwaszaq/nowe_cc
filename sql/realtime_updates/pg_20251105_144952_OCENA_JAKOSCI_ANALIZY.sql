INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'OCENA_JAKOSCI_ANALIZY.md',
    'general_documentation',
    '❌ OCENA JAKOŚCI ANALIZY - SZCZEGÓŁOWA WERYFIKACJA',
    '# ❌ OCENA JAKOŚCI ANALIZY - SZCZEGÓŁOWA WERYFIKACJA

## 📊 OCENA KOŃCOWA: 1/5 (BARDZO SŁABA)

**Znalezionych problemów:** 10

---

## 🔍 ZIDENTYFIKOWANE PROBLEMY

### 1. ❌ NIESPÓJNOŚCI TRENDÓW (2 błędy)',
    145,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();