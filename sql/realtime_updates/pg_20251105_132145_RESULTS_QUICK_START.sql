INSERT INTO documents (
    file_path, document_type, title, content_preview,
    line_count, created_at, indexed_at, source
) VALUES (
    'RESULTS_QUICK_START.md',
    'architecture',
    '🚀 Results Storage - Quick Start Guide',
    '# 🚀 Results Storage - Quick Start Guide

**Welcome!** This guide shows you how to use the new results storage system.

---

## 📋 What''s New?

### **Before:**
```
reports/
  ├── autonomous_case_001.jso',
    396,
    NOW(), NOW(), 'realtime_watcher'
)
ON CONFLICT (file_path) DO UPDATE SET
    document_type = EXCLUDED.document_type,
    title = EXCLUDED.title,
    indexed_at = NOW();