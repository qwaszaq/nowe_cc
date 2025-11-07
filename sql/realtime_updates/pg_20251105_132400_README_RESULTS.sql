INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'README_RESULTS.md',
    'architecture',
    '📊 Results Storage - README',
    '# 📊 Results Storage - README

## 🎯 Quick Navigation

### **I''m working with...**

#### **🧪 Development / Testing (CBA reports, experiments)**
→ Read: `RESULTS_QUICK_START.md`  
→ CLI: `python case_cli',
    80,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();