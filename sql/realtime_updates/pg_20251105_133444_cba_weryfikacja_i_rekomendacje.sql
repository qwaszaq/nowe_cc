INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'reports/cba_weryfikacja_i_rekomendacje.md',
    'general_documentation',
    '🔍 WERYFIKACJA ANALIZY MERYTORYCZNEJ CBA - RAPORT KRYTYCZNY',
    '# 🔍 WERYFIKACJA ANALIZY MERYTORYCZNEJ CBA - RAPORT KRYTYCZNY

**Data weryfikacji:** 2024-11-05  
**Weryfikator:** Analiza rzeczywistych danych z PDF-ów  
**Porównanie:** Analiza LLM vs. Rzeczywiste da',
    412,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();