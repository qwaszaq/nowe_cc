# Complete multi-agent intelligence system with local/Claude comparison

**Auto-Generated Documentation**

**Date:** 2025-11-07 06:54:26
**Commit:** `dc23cfe`
**Type:** Feature
**Author:** artur

---

## 📝 Commit Message

**feat: Complete multi-agent intelligence system with local/Claude comparison**

🎯 Major Features Implemented:

1. Multi-Agent Intelligence System (Priority 4)
   - 6 specialized agents: Financial, Risk, Industry, Strategy, Market, Synthesis
   - Sequential orchestration with context passing
   - RAG integration with section-filtered queries
   - Generation time: 80.32s for comprehensive analysis

2. RAG System Enhancement (Priority 3)
   - Qdrant vector store with BGE reranker
   - Section detection (6 types) for intelligent retrieval
   - E5 embeddings (1024 dimensions)
   - Chunk size: 750 chars, overlap: 100 chars

3. Multi-Year Data Pipeline (Priority 2)
   - JSON-based storage for company financial data
   - Support for balance sheet, income statement, cash flow
   - Financial ratio calculation
   - Data formatting for intelligence analysis

4. Comprehensive Analysis & Comparison
   - Local Single-Agent analysis (26.57s, 2 perspectives)
   - Local Multi-Agent analysis (80.32s, 6 perspectives)
   - Claude-powered analysis (comprehensive credit analysis)
   - Three-way comparison identifying weak spots in local LLMs

📊 Key Findings:

- Local LLMs (both single and multi-agent) recommended HOLD
- Claude identified distressed credit dynamics and recommended SELL
- Critical weak spots identified:
  * Severity calibration failure
  * Missing credit analysis framework
  * Lack of causal reasoning
  * Status quo anchoring
  * Generic risk factors
  * Missing feedback loop identification

🔬 Test Results:

- Grupa Azoty S.A. analyzed as test case
- Local system: 48/100 score, HOLD recommendation
- Claude system: 42/100 score, SELL recommendation (correct)
- Recommendation divergence reveals fundamental analytical gaps

📁 New Files:

Intelligence System:
- src/intelligence/services/multi_agent_intelligence_service.py
- src/intelligence/prompts/industry_context_prompts.py
- src/intelligence/prompts/strategic_evaluation_prompts.py
- src/intelligence/prompts/market_intelligence_prompts.py
- src/intelligence/prompts/synthesis_prompts.py

RAG System:
- src/rag/qdrant_vector_store.py
- src/rag/document_loader.py (enhanced with section detection)

Data Management:
- src/data/multi_year_storage.py
- data/companies/grupa_azoty_sa.json

Testing & Scripts:
- scripts/test_multi_agent_azoty.py
- scripts/test_rag_enhanced_report.py
- scripts/ingest_azoty_to_rag.py
- scripts/generate_claude_analysis.py

Documentation:
- MULTI_AGENT_SYSTEM_COMPLETE.md
- THREE_WAY_COMPARISON_LOCAL_VS_CLAUDE.md
- SINGLE_VS_MULTI_AGENT_COMPARISON.md
- COMPARISON_SUMMARY.md
- RAG_SYSTEM_SUMMARY.md
- RAG_INTEGRATION_COMPLETE.md
- INTELLIGENCE_SYSTEM_ROADMAP.md

Reports:
- output/intelligence_reports/Azoty_MultiAgent_20251106_222059.md
- output/intelligence_reports/Azoty_Claude_Analysis_20251106.md
- output/intelligence_reports/Azoty_Intelligence_Local_20251106_214207.md

✅ All Priorities Complete:
- Priority 1: Single-Agent Intelligence ✅
- Priority 2: Multi-Year Data Pipeline ✅
- Priority 3: RAG Integration ✅
- Priority 4: Multi-Agent Intelligence ✅

🚀 Generated with Claude Code (https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>


## 📁 Files Changed

**Total:** 611 file(s)

### Python Files (61)

- `analyze_cba_content.py`
- `analyze_cba_pdfs.py`
- `case_cli.py`
- `destiny_auto.py`
- `migrate_existing_results.py`
- `profound_test.py`
- `scripts/generate_claude_analysis.py`
- `scripts/ingest_azoty_to_rag.py`
- `scripts/reingest_with_sections.py`
- `scripts/save_azoty_data.py`
- `scripts/test_intelligence_azoty.py`
- `scripts/test_multi_agent_azoty.py`
- `scripts/test_rag_enhanced_report.py`
- `scripts/test_rag_queries.py`
- `src/analysis/__init__.py`
- `src/analysis/comparative_analyzer.py`
- `src/analysis/critical_assessor.py`
- `src/analysis/professional_analyzer.py`
- `src/analysis/qualitative_analyzer.py`
- `src/analysis/quantitative_extractor.py`
- `src/analysis/structure_extractor.py`
- `src/analysis/synthesis_engine.py`
- `src/analysis/temporal_trend_analyzer.py`
- `src/autonomous/autonomous_orchestrator.py`
- `src/autonomous/document_discovery.py`
- `src/autonomous/tool_registry.py`
- `src/data/__init__.py`
- `src/data/embedding_pipeline.py`
- `src/data/multi_year_extractor.py`
- `src/data/multi_year_storage.py`
- `src/data/qdrant_client.py`
- `src/data/smart_router.py`
- `src/intelligence/__init__.py`
- `src/intelligence/formatters/__init__.py`
- `src/intelligence/formatters/data_formatter.py`
- `src/intelligence/prompts/__init__.py`
- `src/intelligence/prompts/industry_context_prompts.py`
- `src/intelligence/prompts/local_llm_prompts.py`
- `src/intelligence/prompts/market_intelligence_prompts.py`
- `src/intelligence/prompts/strategic_evaluation_prompts.py`
- `src/intelligence/prompts/synthesis_prompts.py`
- `src/intelligence/services/__init__.py`
- `src/intelligence/services/local_intelligence_service.py`
- `src/intelligence/services/multi_agent_intelligence_service.py`
- `src/llm/__init__.py`
- `src/llm/agent_prompts.py`
- `src/llm/local_client.py`
- `src/memory/cache_augmented_generation.py`
- `src/memory/rag_cag_strategy.py`
- `src/parsing/document_parsers.py`
- `src/parsing/pdf_table_extractor.py`
- `src/rag/__init__.py`
- `src/rag/document_loader.py`
- `src/rag/qdrant_vector_store.py`
- `src/rag/rag_service.py`
- `src/rag/simple_vector_store.py`
- `src/storage/case_manager.py`
- `test_2023_benchmark.py`
- `test_azoty_2023_extraction.py`
- `test_simple_extraction_2023.py`
- `tests/integration/test_database_integration.py`


### Shell Files (3)

- `START_DEVELOPMENT.sh`
- `scripts/init_all_databases.sh`
- `scripts/init_postgres.sh`


### Documentation Files (93)

- `.claude/commands/ai-project-evaluator.md`
- `ANALIZA_JAKOSCI_PROFESSIONAL_ANALYZER.md`
- `ANALIZA_KRYTYCZNA_SYSTEMU_INVESTIGATIVE_QUALITY.md`
- `ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU.md`
- `ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU_PELNY.md`
- `AUTONOMOUS_SYSTEM_GUIDE.md`
- `BENCHMARK_COMPARISON_2023.md`
- `CBA_COMPREHENSIVE_ANALYSIS_2024.md`
- `CBA_FULL_CONTENT_ANALYSIS.md`
- `COMPARISON_SUMMARY.md`
- `FINAL_ANALYSIS_LOCAL_SYSTEM.md`
- `FIXES_COMPLETE_SUCCESS.md`
- `FULL_HOG_FINAL_STATUS.md`
- `GRAF_RELACJI_STATUS.md`
- `HOW_I_WOULD_ANALYZE_CBA_REPORTS.md`
- `IMPLEMENTACJA_POPRAWEK.md`
- `IMPLEMENTATION_STATUS.md`
- `IMPLEMENTATION_STATUS_FINAL.md`
- `INTELLIGENCE_SYSTEM_ROADMAP.md`
- `INVESTIGATIVE_INTEGRATION_COMPLETE.md`
- `ISTNIEJACE_KONTENERY_ANALIZA.md`
- `LMSTUDIO_INTEGRATION_COMPLETE.md`
- `LOCAL_INTERPRETATION_LAYER.md`
- `MIGRACJA_VOLUMES.md`
- `MULTI_AGENT_ARCHITECTURE.md`
- `MULTI_AGENT_SYSTEM_COMPLETE.md`
- `MVP_AI_SPECIALIST_AGENT_DESIGN.md`
- `NEO4J_STATUS.md`
- `OCENA_JAKOSCI_ANALIZY.md`
- `ON_PREMISE_SYSTEM_READY.md`
- `PELNA_ANALIZA_PROJEKTU_WSZYSTKIE_KOMPONENTY.md`
- `PHASE1_COMPLETION_REPORT.md`
- `PIPELINE_ANALITYCZNY_PELNY_OPIS.md`
- `POROWNANIE_SYSTEM_VS_AI_ANALYSIS.md`
- `PRACTICAL_INTELLIGENCE_ROADMAP.md`
- `PRECYZYJNY_PODZIAL.md`
- `PROFOUND_TEST_CONCLUSIONS.md`
- `RAG_INTEGRATION_COMPLETE.md`
- `RAG_SYSTEM_SUMMARY.md`
- `README_RESULTS.md`
- `REAL_PARSING_COMPLETE.md`
- `RESULTS_QUICK_START.md`
- `RESULTS_STORAGE_ARCHITECTURE.md`
- `RESULTS_STORAGE_SEPARATION.md`
- `RESULTS_SUMMARY.md`
- `SEPARACJA_DANYCH_DEVELOPMENT.md`
- `SINGLE_VS_MULTI_AGENT_COMPARISON.md`
- `SUCCESS_SUMMARY.md`
- `TEST_INSTRUCTIONS.md`
- `THREE_WAY_COMPARISON_LOCAL_VS_CLAUDE.md`
- `WEEK2_DAY1_COMPLETION.md`
- `WERYFIKACJA_PODZIALU.md`
- `WNIOSKI_ARTUR.md`
- `WYSZUKIWANIE_STATUS.md`
- `analysis_rounds/round_1/README.md`
- `analysis_rounds/round_1/alex_document_processing.md`
- `analysis_rounds/round_1/marcus_financial_analysis.md`
- `analysis_rounds/round_1/workflow_alex_marcus.md`
- `docs/architecture/RAG_CAG_STRATEGY.md`
- `docs/auto-generated/2025-11-05/COMMIT_d4adf31_feature.md`
- `docs/auto-generated/2025-11-05/COMMIT_f0d49b5_feature.md`
- `docs/auto-generated/2025-11-06/COMMIT_3d81426_feature.md`
- `docs/auto-generated/2025-11-06/COMMIT_457c53c_feature.md`
- `docs/auto-generated/2025-11-06/COMMIT_9c14593_feature.md`
- `docs/implementation/PLAN_IMPLEMENTACJI_POPRAWY_ANALIZY_CBA.md`
- `docs/implementation/POTWIERDZENIE_MODELI_EMBEDDINGOW.md`
- `docs/implementation/STRATEGIA_EMBEDDINGOW_JINA_VS_E5.md`
- `docs/status/MORNING_BRIEF_20251105.md`
- `docs/status/MORNING_BRIEF_20251106.md`
- `helena_tasks/helena_task_20251105_110000_agent_code.md`
- `helena_tasks/helena_task_20251105_110000_configuration.md`
- `helena_tasks/helena_task_20251105_110000_database_schema.md`
- `helena_tasks/helena_task_20251105_110000_documentation.md`
- `helena_tasks/helena_task_20251105_110000_general_change.md`
- `helena_tasks/helena_task_20251105_110000_knowledge_graph.md`
- `helena_tasks/helena_task_20251105_130000_general_change.md`
- `helena_tasks/helena_task_20251105_140000_general_change.md`
- `helena_tasks/helena_task_20251105_150000_documentation.md`
- `helena_tasks/helena_task_20251105_150000_general_change.md`
- `helena_tasks/helena_task_20251106_210000_documentation.md`
- `helena_tasks/helena_task_20251106_210000_general_change.md`
- `output/intelligence_reports/Azoty_Baseline_NoRAG.md`
- `output/intelligence_reports/Azoty_Claude_Analysis_20251106.md`
- `output/intelligence_reports/Azoty_Intelligence_Local_20251106_214207.md`
- `output/intelligence_reports/Azoty_MultiAgent_20251106_222059.md`
- `output/intelligence_reports/Azoty_RAG_Enhanced.md`
- `reports/EWALUACJA_SYSTEMU_CBA.md`
- `reports/EWALUACJA_SYSTEMU_CBA_SUMMARY.md`
- `reports/GOTOWOSC_SYSTEMU_CBA.md`
- `reports/IMPLEMENTACJA_I_TESTY_RAPORT.md`
- `reports/STATUS_GOTOWOSCI_CBA.md`
- `reports/cba_analiza_merytoryczna_2024.md`
- `reports/cba_weryfikacja_i_rekomendacje.md`


### Configuration Files (208)

- `.cache/prompts/architect_domain.json`
- `.cache/prompts/architect_system.json`
- `.cache/prompts/cba_analysis_2024_context.json`
- `.cache/prompts/cba_full_test_v2_context.json`
- `.cache/prompts/cba_test_integration_context.json`
- `.cache/prompts/data_science_domain.json`
- `.cache/prompts/data_science_system.json`
- `.cache/prompts/financial_domain.json`
- `.cache/prompts/financial_system.json`
- `.cache/prompts/legal_domain.json`
- `.cache/prompts/legal_system.json`
- `.cache/prompts/professional_analysis_20251105_143407_context.json`
- `.cache/prompts/professional_analysis_20251105_143445_context.json`
- `.cache/prompts/professional_analysis_20251105_143753_context.json`
- `.cache/prompts/professional_analysis_20251105_144305_context.json`
- `.cache/prompts/professional_analysis_20251105_144547_context.json`
- `.cache/prompts/profound_test_cba_reports_context.json`
- `.cache/prompts/risk_domain.json`
- `.cache/prompts/risk_system.json`
- `.cache/prompts/test_lmstudio_001_context.json`
- `.change_tracking_state.json`
- `CBA_FULL_CONTENT_ANALYSIS_data.json`
- `CBA_PROFESSIONAL_ANALYSIS_FINAL_results.json`
- `CBA_PROFESSIONAL_ANALYSIS_REPORT_full_data.json`
- `LOCAL_EXTRACTION_RESULTS_2023.json`
- `data/companies/grupa_azoty_sa.json`
- `docker-compose-dev.yml`
- `full_analysis_results_20251105_143433.json`
- `full_analysis_results_20251105_143824.json`
- `full_analysis_results_20251105_144346.json`
- `full_analysis_results_20251105_144624.json`
- `helena_tasks/processed/success_realtime_20251105_104923_COMMIT_f0d49b5_feature.json`
- `helena_tasks/processed/success_realtime_20251105_105739_AUTONOMOUS_SYSTEM_GUIDE.json`
- `helena_tasks/processed/success_realtime_20251105_110102_RAG_CAG_STRATEGY.json`
- `helena_tasks/processed/success_realtime_20251105_110237_WEEK2_DAY1_COMPLETION.json`
- `helena_tasks/processed/success_realtime_20251105_111232_LMSTUDIO_INTEGRATION_COMPLETE.json`
- `helena_tasks/processed/success_realtime_20251105_111355_FULL_HOG_FINAL_STATUS.json`
- `helena_tasks/processed/success_realtime_20251105_111541_README.json`
- `helena_tasks/processed/success_realtime_20251105_113504_REAL_PARSING_COMPLETE.json`
- `helena_tasks/processed/success_realtime_20251105_114107_WNIOSKI_ARTUR.json`
- `helena_tasks/processed/success_realtime_20251105_114855_FIXES_COMPLETE_SUCCESS.json`
- `helena_tasks/processed/success_realtime_20251105_114943_SUCCESS_SUMMARY.json`
- `helena_tasks/processed/success_realtime_20251105_115119_ANALIZA_CBA_2008-2024.json`
- `helena_tasks/processed/success_realtime_20251105_115422_README.json`
- `helena_tasks/processed/success_realtime_20251105_115928_WYSZUKIWANIE_STATUS.json`
- `helena_tasks/processed/success_realtime_20251105_120115_GRAF_RELACJI_STATUS.json`
- `helena_tasks/processed/success_realtime_20251105_120711_NEO4J_STATUS.json`
- `helena_tasks/processed/success_realtime_20251105_121013_ISTNIEJACE_KONTENERY_ANALIZA.json`
- `helena_tasks/processed/success_realtime_20251105_121125_SEPARACJA_DANYCH_DEVELOPMENT.json`
- `helena_tasks/processed/success_realtime_20251105_121305_PRECYZYJNY_PODZIAL.json`
- `helena_tasks/processed/success_realtime_20251105_121450_WERYFIKACJA_PODZIALU.json`
- `helena_tasks/processed/success_realtime_20251105_121736_MIGRACJA_VOLUMES.json`
- `helena_tasks/processed/success_realtime_20251105_131838_RESULTS_STORAGE_ARCHITECTURE.json`
- `helena_tasks/processed/success_realtime_20251105_132144_RESULTS_QUICK_START.json`
- `helena_tasks/processed/success_realtime_20251105_132326_RESULTS_STORAGE_SEPARATION.json`
- `helena_tasks/processed/success_realtime_20251105_132400_README_RESULTS.json`
- `helena_tasks/processed/success_realtime_20251105_132451_RESULTS_SUMMARY.json`
- `helena_tasks/processed/success_realtime_20251105_133123_cba_analiza_merytoryczna_2024.json`
- `helena_tasks/processed/success_realtime_20251105_133443_cba_weryfikacja_i_rekomendacje.json`
- `helena_tasks/processed/success_realtime_20251105_133637_PLAN_IMPLEMENTACJI_POPRAWY_ANALIZY_CBA.json`
- `helena_tasks/processed/success_realtime_20251105_133710_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.json`
- `helena_tasks/processed/success_realtime_20251105_133725_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.json`
- `helena_tasks/processed/success_realtime_20251105_133727_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.json`
- `helena_tasks/processed/success_realtime_20251105_133730_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.json`
- `helena_tasks/processed/success_realtime_20251105_133737_POTWIERDZENIE_MODELI_EMBEDDINGOW.json`
- `helena_tasks/processed/success_realtime_20251105_134418_STATUS_GOTOWOSCI_CBA.json`
- `helena_tasks/processed/success_realtime_20251105_134721_GOTOWOSC_SYSTEMU_CBA.json`
- `helena_tasks/processed/success_realtime_20251105_135015_EWALUACJA_SYSTEMU_CBA.json`
- `helena_tasks/processed/success_realtime_20251105_135041_EWALUACJA_SYSTEMU_CBA_SUMMARY.json`
- `helena_tasks/processed/success_realtime_20251105_140043_AUTONOMOUS_SYSTEM_GUIDE.json`
- `helena_tasks/processed/success_realtime_20251105_140054_AUTONOMOUS_SYSTEM_GUIDE.json`
- `helena_tasks/processed/success_realtime_20251105_140110_AUTONOMOUS_SYSTEM_GUIDE.json`
- `helena_tasks/processed/success_realtime_20251105_140140_AUTONOMOUS_SYSTEM_GUIDE.json`
- `helena_tasks/processed/success_realtime_20251105_140240_INVESTIGATIVE_INTEGRATION_COMPLETE.json`
- `helena_tasks/processed/success_realtime_20251105_140650_CBA_COMPREHENSIVE_ANALYSIS_2024.json`
- `helena_tasks/processed/success_realtime_20251105_141209_CBA_FULL_CONTENT_ANALYSIS.json`
- `helena_tasks/processed/success_realtime_20251105_141722_IMPLEMENTATION_STATUS_FINAL.json`
- `helena_tasks/processed/success_realtime_20251105_142247_HOW_I_WOULD_ANALYZE_CBA_REPORTS.json`
- `helena_tasks/processed/success_realtime_20251105_142507_CBA_PROFESSIONAL_ANALYSIS_REPORT.json`
- `helena_tasks/processed/success_realtime_20251105_142512_CBA_FULL_CONTENT_ANALYSIS.json`
- `helena_tasks/processed/success_realtime_20251105_142544_CBA_PROFESSIONAL_ANALYSIS_REPORT.json`
- `helena_tasks/processed/success_realtime_20251105_142726_HOW_TO_TEACH_SYSTEM_PROFESSIONAL_ANALYSIS.json`
- `helena_tasks/processed/success_realtime_20251105_142757_CBA_PROFESSIONAL_ANALYSIS_FINAL.json`
- `helena_tasks/processed/success_realtime_20251105_142935_COMMIT_d4adf31_feature.json`
- `helena_tasks/processed/success_realtime_20251105_143557_PIPELINE_ANALITYCZNY_PELNY_OPIS.json`
- `helena_tasks/processed/success_realtime_20251105_143844_ANALIZA_JAKOSCI_PROFESSIONAL_ANALYZER.json`
- `helena_tasks/processed/success_realtime_20251105_144019_POROWNANIE_SYSTEM_VS_AI_ANALYSIS.json`
- `helena_tasks/processed/success_realtime_20251105_144257_LOCAL_INTERPRETATION_LAYER.json`
- `helena_tasks/processed/success_realtime_20251105_144359_ON_PREMISE_SYSTEM_READY.json`
- `helena_tasks/processed/success_realtime_20251105_144657_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU.json`
- `helena_tasks/processed/success_realtime_20251105_144728_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU_PELNY.json`
- `helena_tasks/processed/success_realtime_20251105_144744_FINAL_ANALYSIS_LOCAL_SYSTEM.json`
- `helena_tasks/processed/success_realtime_20251105_144952_OCENA_JAKOSCI_ANALIZY.json`
- `helena_tasks/processed/success_realtime_20251105_145122_IMPLEMENTACJA_POPRAWEK.json`
- `helena_tasks/processed/success_realtime_20251106_153940_PHASE2_COMPLETION_REPORT.json`
- `helena_tasks/processed/success_realtime_20251106_170529_FINAL_EXTRACTION_REPORT.json`
- `helena_tasks/processed/success_realtime_20251106_172205_COMMIT_457c53c_feature.json`
- `helena_tasks/processed/success_realtime_20251106_173640_INTELLIGENT_EXTRACTION_COMPLETE.json`
- `helena_tasks/processed/success_realtime_20251106_173724_COMMIT_9c14593_feature.json`
- `helena_tasks/processed/success_realtime_20251106_210140_COMMIT_3d81426_feature.json`
- `helena_tasks/processed/success_realtime_20251106_211911_BENCHMARK_COMPARISON_2023.json`
- `helena_tasks/processed/success_realtime_20251106_211927_BENCHMARK_COMPARISON_2023.json`
- `helena_tasks/processed/success_realtime_20251106_212247_BENCHMARK_COMPARISON_2023.json`
- `helena_tasks/processed/success_realtime_20251106_212256_BENCHMARK_COMPARISON_2023.json`
- `helena_tasks/processed/success_realtime_20251106_214207_Azoty_Intelligence_Local_20251106_214207.json`
- `helena_tasks/processed/success_realtime_20251106_220127_RAG_SYSTEM_SUMMARY.json`
- `helena_tasks/processed/success_realtime_20251106_220301_Azoty_Baseline_NoRAG.json`
- `helena_tasks/processed/success_realtime_20251106_220341_Azoty_RAG_Enhanced.json`
- `helena_tasks/processed/success_realtime_20251106_220529_Azoty_RAG_Enhanced.json`
- `helena_tasks/processed/success_realtime_20251106_222059_Azoty_MultiAgent_20251106_222059.json`
- `qdrant_pending/indexed/doc_20251105_104923_COMMIT_f0d49b5_feature.json`
- `qdrant_pending/indexed/doc_20251105_105739_AUTONOMOUS_SYSTEM_GUIDE.json`
- `qdrant_pending/indexed/doc_20251105_110102_RAG_CAG_STRATEGY.json`
- `qdrant_pending/indexed/doc_20251105_110237_WEEK2_DAY1_COMPLETION.json`
- `qdrant_pending/indexed/doc_20251105_111232_LMSTUDIO_INTEGRATION_COMPLETE.json`
- `qdrant_pending/indexed/doc_20251105_111355_FULL_HOG_FINAL_STATUS.json`
- `qdrant_pending/indexed/doc_20251105_111541_README.json`
- `qdrant_pending/indexed/doc_20251105_113504_REAL_PARSING_COMPLETE.json`
- `qdrant_pending/indexed/doc_20251105_114107_WNIOSKI_ARTUR.json`
- `qdrant_pending/indexed/doc_20251105_114856_FIXES_COMPLETE_SUCCESS.json`
- `qdrant_pending/indexed/doc_20251105_114944_SUCCESS_SUMMARY.json`
- `qdrant_pending/indexed/doc_20251105_115119_ANALIZA_CBA_2008-2024.json`
- `qdrant_pending/indexed/doc_20251105_115423_README.json`
- `qdrant_pending/indexed/doc_20251105_115929_WYSZUKIWANIE_STATUS.json`
- `qdrant_pending/indexed/doc_20251105_120115_GRAF_RELACJI_STATUS.json`
- `qdrant_pending/indexed/doc_20251105_120711_NEO4J_STATUS.json`
- `qdrant_pending/indexed/doc_20251105_121014_ISTNIEJACE_KONTENERY_ANALIZA.json`
- `qdrant_pending/indexed/doc_20251105_121125_SEPARACJA_DANYCH_DEVELOPMENT.json`
- `qdrant_pending/indexed/doc_20251105_121306_PRECYZYJNY_PODZIAL.json`
- `qdrant_pending/indexed/doc_20251105_121451_WERYFIKACJA_PODZIALU.json`
- `qdrant_pending/indexed/doc_20251105_121737_MIGRACJA_VOLUMES.json`
- `qdrant_pending/indexed/doc_20251105_131839_RESULTS_STORAGE_ARCHITECTURE.json`
- `qdrant_pending/indexed/doc_20251105_132145_RESULTS_QUICK_START.json`
- `qdrant_pending/indexed/doc_20251105_132326_RESULTS_STORAGE_SEPARATION.json`
- `qdrant_pending/indexed/doc_20251105_132400_README_RESULTS.json`
- `qdrant_pending/indexed/doc_20251105_132452_RESULTS_SUMMARY.json`
- `qdrant_pending/indexed/doc_20251105_133124_cba_analiza_merytoryczna_2024.json`
- `qdrant_pending/indexed/doc_20251105_133444_cba_weryfikacja_i_rekomendacje.json`
- `qdrant_pending/indexed/doc_20251105_133637_PLAN_IMPLEMENTACJI_POPRAWY_ANALIZY_CBA.json`
- `qdrant_pending/indexed/doc_20251105_133711_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.json`
- `qdrant_pending/indexed/doc_20251105_133725_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.json`
- `qdrant_pending/indexed/doc_20251105_133728_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.json`
- `qdrant_pending/indexed/doc_20251105_133731_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.json`
- `qdrant_pending/indexed/doc_20251105_133737_POTWIERDZENIE_MODELI_EMBEDDINGOW.json`
- `qdrant_pending/indexed/doc_20251105_134418_STATUS_GOTOWOSCI_CBA.json`
- `qdrant_pending/indexed/doc_20251105_134722_GOTOWOSC_SYSTEMU_CBA.json`
- `qdrant_pending/indexed/doc_20251105_135015_EWALUACJA_SYSTEMU_CBA.json`
- `qdrant_pending/indexed/doc_20251105_135041_EWALUACJA_SYSTEMU_CBA_SUMMARY.json`
- `qdrant_pending/indexed/doc_20251105_140043_AUTONOMOUS_SYSTEM_GUIDE.json`
- `qdrant_pending/indexed/doc_20251105_140055_AUTONOMOUS_SYSTEM_GUIDE.json`
- `qdrant_pending/indexed/doc_20251105_140110_AUTONOMOUS_SYSTEM_GUIDE.json`
- `qdrant_pending/indexed/doc_20251105_140140_AUTONOMOUS_SYSTEM_GUIDE.json`
- `qdrant_pending/indexed/doc_20251105_140241_INVESTIGATIVE_INTEGRATION_COMPLETE.json`
- `qdrant_pending/indexed/doc_20251105_140651_CBA_COMPREHENSIVE_ANALYSIS_2024.json`
- `qdrant_pending/indexed/doc_20251105_141210_CBA_FULL_CONTENT_ANALYSIS.json`
- `qdrant_pending/indexed/doc_20251105_141722_IMPLEMENTATION_STATUS_FINAL.json`
- `qdrant_pending/indexed/doc_20251105_142248_HOW_I_WOULD_ANALYZE_CBA_REPORTS.json`
- `qdrant_pending/indexed/doc_20251105_142507_CBA_PROFESSIONAL_ANALYSIS_REPORT.json`
- `qdrant_pending/indexed/doc_20251105_142513_CBA_FULL_CONTENT_ANALYSIS.json`
- `qdrant_pending/indexed/doc_20251105_142545_CBA_PROFESSIONAL_ANALYSIS_REPORT.json`
- `qdrant_pending/indexed/doc_20251105_142726_HOW_TO_TEACH_SYSTEM_PROFESSIONAL_ANALYSIS.json`
- `qdrant_pending/indexed/doc_20251105_142758_CBA_PROFESSIONAL_ANALYSIS_FINAL.json`
- `qdrant_pending/indexed/doc_20251105_142935_COMMIT_d4adf31_feature.json`
- `qdrant_pending/indexed/doc_20251105_143558_PIPELINE_ANALITYCZNY_PELNY_OPIS.json`
- `qdrant_pending/indexed/doc_20251105_143845_ANALIZA_JAKOSCI_PROFESSIONAL_ANALYZER.json`
- `qdrant_pending/indexed/doc_20251105_144020_POROWNANIE_SYSTEM_VS_AI_ANALYSIS.json`
- `qdrant_pending/indexed/doc_20251105_144257_LOCAL_INTERPRETATION_LAYER.json`
- `qdrant_pending/indexed/doc_20251105_144359_ON_PREMISE_SYSTEM_READY.json`
- `qdrant_pending/indexed/doc_20251105_144658_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU.json`
- `qdrant_pending/indexed/doc_20251105_144728_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU_PELNY.json`
- `qdrant_pending/indexed/doc_20251105_144745_FINAL_ANALYSIS_LOCAL_SYSTEM.json`
- `qdrant_pending/indexed/doc_20251105_144952_OCENA_JAKOSCI_ANALIZY.json`
- `qdrant_pending/indexed/doc_20251105_145122_IMPLEMENTACJA_POPRAWEK.json`
- `qdrant_pending/indexed/doc_20251106_153941_PHASE2_COMPLETION_REPORT.json`
- `qdrant_pending/indexed/doc_20251106_170530_FINAL_EXTRACTION_REPORT.json`
- `qdrant_pending/indexed/doc_20251106_172206_COMMIT_457c53c_feature.json`
- `qdrant_pending/indexed/doc_20251106_173640_INTELLIGENT_EXTRACTION_COMPLETE.json`
- `qdrant_pending/indexed/doc_20251106_173724_COMMIT_9c14593_feature.json`
- `qdrant_pending/indexed/doc_20251106_210141_COMMIT_3d81426_feature.json`
- `qdrant_pending/indexed/doc_20251106_211912_BENCHMARK_COMPARISON_2023.json`
- `qdrant_pending/indexed/doc_20251106_211928_BENCHMARK_COMPARISON_2023.json`
- `qdrant_pending/indexed/doc_20251106_212248_BENCHMARK_COMPARISON_2023.json`
- `qdrant_pending/indexed/doc_20251106_212256_BENCHMARK_COMPARISON_2023.json`
- `qdrant_pending/indexed/doc_20251106_214208_Azoty_Intelligence_Local_20251106_214207.json`
- `qdrant_pending/indexed/doc_20251106_220128_RAG_SYSTEM_SUMMARY.json`
- `qdrant_pending/indexed/doc_20251106_220302_Azoty_Baseline_NoRAG.json`
- `qdrant_pending/indexed/doc_20251106_220342_Azoty_RAG_Enhanced.json`
- `qdrant_pending/indexed/doc_20251106_220529_Azoty_RAG_Enhanced.json`
- `qdrant_pending/indexed/doc_20251106_222100_Azoty_MultiAgent_20251106_222059.json`
- `quality_report_20251105_143433.json`
- `quality_report_20251105_143824.json`
- `quality_report_20251105_144346.json`
- `quality_report_20251105_144624.json`
- `reports/autonomous_cba_analysis_2024.json`
- `reports/autonomous_cba_full_test_v2.json`
- `reports/autonomous_cba_test_integration.json`
- `reports/autonomous_professional_analysis_20251105_143407.json`
- `reports/autonomous_professional_analysis_20251105_143445.json`
- `reports/autonomous_professional_analysis_20251105_143753.json`
- `reports/autonomous_professional_analysis_20251105_144305.json`
- `reports/autonomous_professional_analysis_20251105_144547.json`
- `reports/autonomous_profound_test_cba_reports.json`
- `reports/autonomous_real_parsing_test.json`
- `reports/autonomous_test_lmstudio_001.json`
- `reports/cba_extraction_results.json`
- `reports/cba_real_data_extracted.json`
- `reports/cba_verification_extraction.json`
- `test_workflow_results.json`


### Other Files (246)

- `.env`
- `.env.development`
- `.env.investigation`
- `.gitignore`
- `cba_content_analysis_log.txt`
- `cba_detection_results.txt`
- `cba_full_analysis_log.txt`
- `redis_pending/redis_20251105_104923_COMMIT_f0d49b5_feature.txt`
- `redis_pending/redis_20251105_105739_AUTONOMOUS_SYSTEM_GUIDE.txt`
- `redis_pending/redis_20251105_110103_RAG_CAG_STRATEGY.txt`
- `redis_pending/redis_20251105_110237_WEEK2_DAY1_COMPLETION.txt`
- `redis_pending/redis_20251105_111232_LMSTUDIO_INTEGRATION_COMPLETE.txt`
- `redis_pending/redis_20251105_111355_FULL_HOG_FINAL_STATUS.txt`
- `redis_pending/redis_20251105_111541_README.txt`
- `redis_pending/redis_20251105_113504_REAL_PARSING_COMPLETE.txt`
- `redis_pending/redis_20251105_114107_WNIOSKI_ARTUR.txt`
- `redis_pending/redis_20251105_114856_FIXES_COMPLETE_SUCCESS.txt`
- `redis_pending/redis_20251105_114944_SUCCESS_SUMMARY.txt`
- `redis_pending/redis_20251105_115119_ANALIZA_CBA_2008-2024.txt`
- `redis_pending/redis_20251105_115423_README.txt`
- `redis_pending/redis_20251105_115929_WYSZUKIWANIE_STATUS.txt`
- `redis_pending/redis_20251105_120115_GRAF_RELACJI_STATUS.txt`
- `redis_pending/redis_20251105_120711_NEO4J_STATUS.txt`
- `redis_pending/redis_20251105_121014_ISTNIEJACE_KONTENERY_ANALIZA.txt`
- `redis_pending/redis_20251105_121125_SEPARACJA_DANYCH_DEVELOPMENT.txt`
- `redis_pending/redis_20251105_121306_PRECYZYJNY_PODZIAL.txt`
- `redis_pending/redis_20251105_121451_WERYFIKACJA_PODZIALU.txt`
- `redis_pending/redis_20251105_121737_MIGRACJA_VOLUMES.txt`
- `redis_pending/redis_20251105_131839_RESULTS_STORAGE_ARCHITECTURE.txt`
- `redis_pending/redis_20251105_132145_RESULTS_QUICK_START.txt`
- `redis_pending/redis_20251105_132326_RESULTS_STORAGE_SEPARATION.txt`
- `redis_pending/redis_20251105_132400_README_RESULTS.txt`
- `redis_pending/redis_20251105_132452_RESULTS_SUMMARY.txt`
- `redis_pending/redis_20251105_133124_cba_analiza_merytoryczna_2024.txt`
- `redis_pending/redis_20251105_133444_cba_weryfikacja_i_rekomendacje.txt`
- `redis_pending/redis_20251105_133637_PLAN_IMPLEMENTACJI_POPRAWY_ANALIZY_CBA.txt`
- `redis_pending/redis_20251105_133711_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.txt`
- `redis_pending/redis_20251105_133725_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.txt`
- `redis_pending/redis_20251105_133728_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.txt`
- `redis_pending/redis_20251105_133731_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.txt`
- `redis_pending/redis_20251105_133737_POTWIERDZENIE_MODELI_EMBEDDINGOW.txt`
- `redis_pending/redis_20251105_134418_STATUS_GOTOWOSCI_CBA.txt`
- `redis_pending/redis_20251105_134722_GOTOWOSC_SYSTEMU_CBA.txt`
- `redis_pending/redis_20251105_135015_EWALUACJA_SYSTEMU_CBA.txt`
- `redis_pending/redis_20251105_135041_EWALUACJA_SYSTEMU_CBA_SUMMARY.txt`
- `redis_pending/redis_20251105_140043_AUTONOMOUS_SYSTEM_GUIDE.txt`
- `redis_pending/redis_20251105_140055_AUTONOMOUS_SYSTEM_GUIDE.txt`
- `redis_pending/redis_20251105_140110_AUTONOMOUS_SYSTEM_GUIDE.txt`
- `redis_pending/redis_20251105_140140_AUTONOMOUS_SYSTEM_GUIDE.txt`
- `redis_pending/redis_20251105_140241_INVESTIGATIVE_INTEGRATION_COMPLETE.txt`
- `redis_pending/redis_20251105_140651_CBA_COMPREHENSIVE_ANALYSIS_2024.txt`
- `redis_pending/redis_20251105_141210_CBA_FULL_CONTENT_ANALYSIS.txt`
- `redis_pending/redis_20251105_141722_IMPLEMENTATION_STATUS_FINAL.txt`
- `redis_pending/redis_20251105_142248_HOW_I_WOULD_ANALYZE_CBA_REPORTS.txt`
- `redis_pending/redis_20251105_142507_CBA_PROFESSIONAL_ANALYSIS_REPORT.txt`
- `redis_pending/redis_20251105_142513_CBA_FULL_CONTENT_ANALYSIS.txt`
- `redis_pending/redis_20251105_142545_CBA_PROFESSIONAL_ANALYSIS_REPORT.txt`
- `redis_pending/redis_20251105_142726_HOW_TO_TEACH_SYSTEM_PROFESSIONAL_ANALYSIS.txt`
- `redis_pending/redis_20251105_142758_CBA_PROFESSIONAL_ANALYSIS_FINAL.txt`
- `redis_pending/redis_20251105_142935_COMMIT_d4adf31_feature.txt`
- `redis_pending/redis_20251105_143558_PIPELINE_ANALITYCZNY_PELNY_OPIS.txt`
- `redis_pending/redis_20251105_143845_ANALIZA_JAKOSCI_PROFESSIONAL_ANALYZER.txt`
- `redis_pending/redis_20251105_144020_POROWNANIE_SYSTEM_VS_AI_ANALYSIS.txt`
- `redis_pending/redis_20251105_144258_LOCAL_INTERPRETATION_LAYER.txt`
- `redis_pending/redis_20251105_144359_ON_PREMISE_SYSTEM_READY.txt`
- `redis_pending/redis_20251105_144658_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU.txt`
- `redis_pending/redis_20251105_144728_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU_PELNY.txt`
- `redis_pending/redis_20251105_144745_FINAL_ANALYSIS_LOCAL_SYSTEM.txt`
- `redis_pending/redis_20251105_144952_OCENA_JAKOSCI_ANALIZY.txt`
- `redis_pending/redis_20251105_145122_IMPLEMENTACJA_POPRAWEK.txt`
- `redis_pending/redis_20251106_153941_PHASE2_COMPLETION_REPORT.txt`
- `redis_pending/redis_20251106_170530_FINAL_EXTRACTION_REPORT.txt`
- `redis_pending/redis_20251106_172206_COMMIT_457c53c_feature.txt`
- `redis_pending/redis_20251106_173641_INTELLIGENT_EXTRACTION_COMPLETE.txt`
- `redis_pending/redis_20251106_173724_COMMIT_9c14593_feature.txt`
- `redis_pending/redis_20251106_210141_COMMIT_3d81426_feature.txt`
- `redis_pending/redis_20251106_211912_BENCHMARK_COMPARISON_2023.txt`
- `redis_pending/redis_20251106_211928_BENCHMARK_COMPARISON_2023.txt`
- `redis_pending/redis_20251106_212248_BENCHMARK_COMPARISON_2023.txt`
- `redis_pending/redis_20251106_212256_BENCHMARK_COMPARISON_2023.txt`
- `redis_pending/redis_20251106_214208_Azoty_Intelligence_Local_20251106_214207.txt`
- `redis_pending/redis_20251106_220128_RAG_SYSTEM_SUMMARY.txt`
- `redis_pending/redis_20251106_220302_Azoty_Baseline_NoRAG.txt`
- `redis_pending/redis_20251106_220342_Azoty_RAG_Enhanced.txt`
- `redis_pending/redis_20251106_220530_Azoty_RAG_Enhanced.txt`
- `redis_pending/redis_20251106_222100_Azoty_MultiAgent_20251106_222059.txt`
- `reports/cba_analiza_merytoryczna_2024.html`
- `reports/cba_analysis_2024.html`
- `sql/realtime_updates/neo4j_20251105_104923_COMMIT_f0d49b5_feature.cypher`
- `sql/realtime_updates/neo4j_20251105_105739_AUTONOMOUS_SYSTEM_GUIDE.cypher`
- `sql/realtime_updates/neo4j_20251105_110102_RAG_CAG_STRATEGY.cypher`
- `sql/realtime_updates/neo4j_20251105_110237_WEEK2_DAY1_COMPLETION.cypher`
- `sql/realtime_updates/neo4j_20251105_111232_LMSTUDIO_INTEGRATION_COMPLETE.cypher`
- `sql/realtime_updates/neo4j_20251105_111355_FULL_HOG_FINAL_STATUS.cypher`
- `sql/realtime_updates/neo4j_20251105_111541_README.cypher`
- `sql/realtime_updates/neo4j_20251105_113504_REAL_PARSING_COMPLETE.cypher`
- `sql/realtime_updates/neo4j_20251105_114107_WNIOSKI_ARTUR.cypher`
- `sql/realtime_updates/neo4j_20251105_114856_FIXES_COMPLETE_SUCCESS.cypher`
- `sql/realtime_updates/neo4j_20251105_114944_SUCCESS_SUMMARY.cypher`
- `sql/realtime_updates/neo4j_20251105_115119_ANALIZA_CBA_2008-2024.cypher`
- `sql/realtime_updates/neo4j_20251105_115423_README.cypher`
- `sql/realtime_updates/neo4j_20251105_115929_WYSZUKIWANIE_STATUS.cypher`
- `sql/realtime_updates/neo4j_20251105_120115_GRAF_RELACJI_STATUS.cypher`
- `sql/realtime_updates/neo4j_20251105_120711_NEO4J_STATUS.cypher`
- `sql/realtime_updates/neo4j_20251105_121014_ISTNIEJACE_KONTENERY_ANALIZA.cypher`
- `sql/realtime_updates/neo4j_20251105_121125_SEPARACJA_DANYCH_DEVELOPMENT.cypher`
- `sql/realtime_updates/neo4j_20251105_121306_PRECYZYJNY_PODZIAL.cypher`
- `sql/realtime_updates/neo4j_20251105_121451_WERYFIKACJA_PODZIALU.cypher`
- `sql/realtime_updates/neo4j_20251105_121737_MIGRACJA_VOLUMES.cypher`
- `sql/realtime_updates/neo4j_20251105_131839_RESULTS_STORAGE_ARCHITECTURE.cypher`
- `sql/realtime_updates/neo4j_20251105_132145_RESULTS_QUICK_START.cypher`
- `sql/realtime_updates/neo4j_20251105_132326_RESULTS_STORAGE_SEPARATION.cypher`
- `sql/realtime_updates/neo4j_20251105_132400_README_RESULTS.cypher`
- `sql/realtime_updates/neo4j_20251105_132452_RESULTS_SUMMARY.cypher`
- `sql/realtime_updates/neo4j_20251105_133124_cba_analiza_merytoryczna_2024.cypher`
- `sql/realtime_updates/neo4j_20251105_133444_cba_weryfikacja_i_rekomendacje.cypher`
- `sql/realtime_updates/neo4j_20251105_133637_PLAN_IMPLEMENTACJI_POPRAWY_ANALIZY_CBA.cypher`
- `sql/realtime_updates/neo4j_20251105_133711_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.cypher`
- `sql/realtime_updates/neo4j_20251105_133725_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.cypher`
- `sql/realtime_updates/neo4j_20251105_133728_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.cypher`
- `sql/realtime_updates/neo4j_20251105_133731_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.cypher`
- `sql/realtime_updates/neo4j_20251105_133737_POTWIERDZENIE_MODELI_EMBEDDINGOW.cypher`
- `sql/realtime_updates/neo4j_20251105_134418_STATUS_GOTOWOSCI_CBA.cypher`
- `sql/realtime_updates/neo4j_20251105_134722_GOTOWOSC_SYSTEMU_CBA.cypher`
- `sql/realtime_updates/neo4j_20251105_135015_EWALUACJA_SYSTEMU_CBA.cypher`
- `sql/realtime_updates/neo4j_20251105_135041_EWALUACJA_SYSTEMU_CBA_SUMMARY.cypher`
- `sql/realtime_updates/neo4j_20251105_140043_AUTONOMOUS_SYSTEM_GUIDE.cypher`
- `sql/realtime_updates/neo4j_20251105_140055_AUTONOMOUS_SYSTEM_GUIDE.cypher`
- `sql/realtime_updates/neo4j_20251105_140110_AUTONOMOUS_SYSTEM_GUIDE.cypher`
- `sql/realtime_updates/neo4j_20251105_140140_AUTONOMOUS_SYSTEM_GUIDE.cypher`
- `sql/realtime_updates/neo4j_20251105_140241_INVESTIGATIVE_INTEGRATION_COMPLETE.cypher`
- `sql/realtime_updates/neo4j_20251105_140651_CBA_COMPREHENSIVE_ANALYSIS_2024.cypher`
- `sql/realtime_updates/neo4j_20251105_141210_CBA_FULL_CONTENT_ANALYSIS.cypher`
- `sql/realtime_updates/neo4j_20251105_141722_IMPLEMENTATION_STATUS_FINAL.cypher`
- `sql/realtime_updates/neo4j_20251105_142248_HOW_I_WOULD_ANALYZE_CBA_REPORTS.cypher`
- `sql/realtime_updates/neo4j_20251105_142507_CBA_PROFESSIONAL_ANALYSIS_REPORT.cypher`
- `sql/realtime_updates/neo4j_20251105_142513_CBA_FULL_CONTENT_ANALYSIS.cypher`
- `sql/realtime_updates/neo4j_20251105_142545_CBA_PROFESSIONAL_ANALYSIS_REPORT.cypher`
- `sql/realtime_updates/neo4j_20251105_142726_HOW_TO_TEACH_SYSTEM_PROFESSIONAL_ANALYSIS.cypher`
- `sql/realtime_updates/neo4j_20251105_142758_CBA_PROFESSIONAL_ANALYSIS_FINAL.cypher`
- `sql/realtime_updates/neo4j_20251105_142935_COMMIT_d4adf31_feature.cypher`
- `sql/realtime_updates/neo4j_20251105_143558_PIPELINE_ANALITYCZNY_PELNY_OPIS.cypher`
- `sql/realtime_updates/neo4j_20251105_143845_ANALIZA_JAKOSCI_PROFESSIONAL_ANALYZER.cypher`
- `sql/realtime_updates/neo4j_20251105_144020_POROWNANIE_SYSTEM_VS_AI_ANALYSIS.cypher`
- `sql/realtime_updates/neo4j_20251105_144257_LOCAL_INTERPRETATION_LAYER.cypher`
- `sql/realtime_updates/neo4j_20251105_144359_ON_PREMISE_SYSTEM_READY.cypher`
- `sql/realtime_updates/neo4j_20251105_144658_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU.cypher`
- `sql/realtime_updates/neo4j_20251105_144728_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU_PELNY.cypher`
- `sql/realtime_updates/neo4j_20251105_144745_FINAL_ANALYSIS_LOCAL_SYSTEM.cypher`
- `sql/realtime_updates/neo4j_20251105_144952_OCENA_JAKOSCI_ANALIZY.cypher`
- `sql/realtime_updates/neo4j_20251105_145122_IMPLEMENTACJA_POPRAWEK.cypher`
- `sql/realtime_updates/neo4j_20251106_153941_PHASE2_COMPLETION_REPORT.cypher`
- `sql/realtime_updates/neo4j_20251106_170530_FINAL_EXTRACTION_REPORT.cypher`
- `sql/realtime_updates/neo4j_20251106_172206_COMMIT_457c53c_feature.cypher`
- `sql/realtime_updates/neo4j_20251106_173640_INTELLIGENT_EXTRACTION_COMPLETE.cypher`
- `sql/realtime_updates/neo4j_20251106_173724_COMMIT_9c14593_feature.cypher`
- `sql/realtime_updates/neo4j_20251106_210141_COMMIT_3d81426_feature.cypher`
- `sql/realtime_updates/neo4j_20251106_211912_BENCHMARK_COMPARISON_2023.cypher`
- `sql/realtime_updates/neo4j_20251106_211928_BENCHMARK_COMPARISON_2023.cypher`
- `sql/realtime_updates/neo4j_20251106_212248_BENCHMARK_COMPARISON_2023.cypher`
- `sql/realtime_updates/neo4j_20251106_212256_BENCHMARK_COMPARISON_2023.cypher`
- `sql/realtime_updates/neo4j_20251106_214208_Azoty_Intelligence_Local_20251106_214207.cypher`
- `sql/realtime_updates/neo4j_20251106_220128_RAG_SYSTEM_SUMMARY.cypher`
- `sql/realtime_updates/neo4j_20251106_220302_Azoty_Baseline_NoRAG.cypher`
- `sql/realtime_updates/neo4j_20251106_220342_Azoty_RAG_Enhanced.cypher`
- `sql/realtime_updates/neo4j_20251106_220529_Azoty_RAG_Enhanced.cypher`
- `sql/realtime_updates/neo4j_20251106_222100_Azoty_MultiAgent_20251106_222059.cypher`
- `sql/realtime_updates/pg_20251105_104923_COMMIT_f0d49b5_feature.sql`
- `sql/realtime_updates/pg_20251105_105739_AUTONOMOUS_SYSTEM_GUIDE.sql`
- `sql/realtime_updates/pg_20251105_110102_RAG_CAG_STRATEGY.sql`
- `sql/realtime_updates/pg_20251105_110237_WEEK2_DAY1_COMPLETION.sql`
- `sql/realtime_updates/pg_20251105_111232_LMSTUDIO_INTEGRATION_COMPLETE.sql`
- `sql/realtime_updates/pg_20251105_111355_FULL_HOG_FINAL_STATUS.sql`
- `sql/realtime_updates/pg_20251105_111541_README.sql`
- `sql/realtime_updates/pg_20251105_113504_REAL_PARSING_COMPLETE.sql`
- `sql/realtime_updates/pg_20251105_114107_WNIOSKI_ARTUR.sql`
- `sql/realtime_updates/pg_20251105_114856_FIXES_COMPLETE_SUCCESS.sql`
- `sql/realtime_updates/pg_20251105_114944_SUCCESS_SUMMARY.sql`
- `sql/realtime_updates/pg_20251105_115119_ANALIZA_CBA_2008-2024.sql`
- `sql/realtime_updates/pg_20251105_115423_README.sql`
- `sql/realtime_updates/pg_20251105_115929_WYSZUKIWANIE_STATUS.sql`
- `sql/realtime_updates/pg_20251105_120115_GRAF_RELACJI_STATUS.sql`
- `sql/realtime_updates/pg_20251105_120711_NEO4J_STATUS.sql`
- `sql/realtime_updates/pg_20251105_121014_ISTNIEJACE_KONTENERY_ANALIZA.sql`
- `sql/realtime_updates/pg_20251105_121125_SEPARACJA_DANYCH_DEVELOPMENT.sql`
- `sql/realtime_updates/pg_20251105_121306_PRECYZYJNY_PODZIAL.sql`
- `sql/realtime_updates/pg_20251105_121451_WERYFIKACJA_PODZIALU.sql`
- `sql/realtime_updates/pg_20251105_121737_MIGRACJA_VOLUMES.sql`
- `sql/realtime_updates/pg_20251105_131839_RESULTS_STORAGE_ARCHITECTURE.sql`
- `sql/realtime_updates/pg_20251105_132145_RESULTS_QUICK_START.sql`
- `sql/realtime_updates/pg_20251105_132326_RESULTS_STORAGE_SEPARATION.sql`
- `sql/realtime_updates/pg_20251105_132400_README_RESULTS.sql`
- `sql/realtime_updates/pg_20251105_132452_RESULTS_SUMMARY.sql`
- `sql/realtime_updates/pg_20251105_133124_cba_analiza_merytoryczna_2024.sql`
- `sql/realtime_updates/pg_20251105_133444_cba_weryfikacja_i_rekomendacje.sql`
- `sql/realtime_updates/pg_20251105_133637_PLAN_IMPLEMENTACJI_POPRAWY_ANALIZY_CBA.sql`
- `sql/realtime_updates/pg_20251105_133711_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.sql`
- `sql/realtime_updates/pg_20251105_133725_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.sql`
- `sql/realtime_updates/pg_20251105_133728_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.sql`
- `sql/realtime_updates/pg_20251105_133730_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.sql`
- `sql/realtime_updates/pg_20251105_133737_POTWIERDZENIE_MODELI_EMBEDDINGOW.sql`
- `sql/realtime_updates/pg_20251105_134418_STATUS_GOTOWOSCI_CBA.sql`
- `sql/realtime_updates/pg_20251105_134722_GOTOWOSC_SYSTEMU_CBA.sql`
- `sql/realtime_updates/pg_20251105_135015_EWALUACJA_SYSTEMU_CBA.sql`
- `sql/realtime_updates/pg_20251105_135041_EWALUACJA_SYSTEMU_CBA_SUMMARY.sql`
- `sql/realtime_updates/pg_20251105_140043_AUTONOMOUS_SYSTEM_GUIDE.sql`
- `sql/realtime_updates/pg_20251105_140055_AUTONOMOUS_SYSTEM_GUIDE.sql`
- `sql/realtime_updates/pg_20251105_140110_AUTONOMOUS_SYSTEM_GUIDE.sql`
- `sql/realtime_updates/pg_20251105_140140_AUTONOMOUS_SYSTEM_GUIDE.sql`
- `sql/realtime_updates/pg_20251105_140241_INVESTIGATIVE_INTEGRATION_COMPLETE.sql`
- `sql/realtime_updates/pg_20251105_140651_CBA_COMPREHENSIVE_ANALYSIS_2024.sql`
- `sql/realtime_updates/pg_20251105_141210_CBA_FULL_CONTENT_ANALYSIS.sql`
- `sql/realtime_updates/pg_20251105_141722_IMPLEMENTATION_STATUS_FINAL.sql`
- `sql/realtime_updates/pg_20251105_142248_HOW_I_WOULD_ANALYZE_CBA_REPORTS.sql`
- `sql/realtime_updates/pg_20251105_142507_CBA_PROFESSIONAL_ANALYSIS_REPORT.sql`
- `sql/realtime_updates/pg_20251105_142513_CBA_FULL_CONTENT_ANALYSIS.sql`
- `sql/realtime_updates/pg_20251105_142545_CBA_PROFESSIONAL_ANALYSIS_REPORT.sql`
- `sql/realtime_updates/pg_20251105_142726_HOW_TO_TEACH_SYSTEM_PROFESSIONAL_ANALYSIS.sql`
- `sql/realtime_updates/pg_20251105_142758_CBA_PROFESSIONAL_ANALYSIS_FINAL.sql`
- `sql/realtime_updates/pg_20251105_142935_COMMIT_d4adf31_feature.sql`
- `sql/realtime_updates/pg_20251105_143558_PIPELINE_ANALITYCZNY_PELNY_OPIS.sql`
- `sql/realtime_updates/pg_20251105_143845_ANALIZA_JAKOSCI_PROFESSIONAL_ANALYZER.sql`
- `sql/realtime_updates/pg_20251105_144020_POROWNANIE_SYSTEM_VS_AI_ANALYSIS.sql`
- `sql/realtime_updates/pg_20251105_144257_LOCAL_INTERPRETATION_LAYER.sql`
- `sql/realtime_updates/pg_20251105_144359_ON_PREMISE_SYSTEM_READY.sql`
- `sql/realtime_updates/pg_20251105_144658_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU.sql`
- `sql/realtime_updates/pg_20251105_144728_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU_PELNY.sql`
- `sql/realtime_updates/pg_20251105_144744_FINAL_ANALYSIS_LOCAL_SYSTEM.sql`
- `sql/realtime_updates/pg_20251105_144952_OCENA_JAKOSCI_ANALIZY.sql`
- `sql/realtime_updates/pg_20251105_145122_IMPLEMENTACJA_POPRAWEK.sql`
- `sql/realtime_updates/pg_20251106_153941_PHASE2_COMPLETION_REPORT.sql`
- `sql/realtime_updates/pg_20251106_170530_FINAL_EXTRACTION_REPORT.sql`
- `sql/realtime_updates/pg_20251106_172206_COMMIT_457c53c_feature.sql`
- `sql/realtime_updates/pg_20251106_173640_INTELLIGENT_EXTRACTION_COMPLETE.sql`
- `sql/realtime_updates/pg_20251106_173724_COMMIT_9c14593_feature.sql`
- `sql/realtime_updates/pg_20251106_210141_COMMIT_3d81426_feature.sql`
- `sql/realtime_updates/pg_20251106_211912_BENCHMARK_COMPARISON_2023.sql`
- `sql/realtime_updates/pg_20251106_211928_BENCHMARK_COMPARISON_2023.sql`
- `sql/realtime_updates/pg_20251106_212248_BENCHMARK_COMPARISON_2023.sql`
- `sql/realtime_updates/pg_20251106_212256_BENCHMARK_COMPARISON_2023.sql`
- `sql/realtime_updates/pg_20251106_214208_Azoty_Intelligence_Local_20251106_214207.sql`
- `sql/realtime_updates/pg_20251106_220128_RAG_SYSTEM_SUMMARY.sql`
- `sql/realtime_updates/pg_20251106_220302_Azoty_Baseline_NoRAG.sql`
- `sql/realtime_updates/pg_20251106_220342_Azoty_RAG_Enhanced.sql`
- `sql/realtime_updates/pg_20251106_220529_Azoty_RAG_Enhanced.sql`
- `sql/realtime_updates/pg_20251106_222100_Azoty_MultiAgent_20251106_222059.sql`


## 📊 Statistics

```
dc23cfe feat: Complete multi-agent intelligence system with local/Claude comparison
 .cache/prompts/architect_domain.json               |    1 +
 .cache/prompts/architect_system.json               |    1 +
 .cache/prompts/cba_analysis_2024_context.json      |    1 +
 .cache/prompts/cba_full_test_v2_context.json       |    1 +
 .cache/prompts/cba_test_integration_context.json   |    1 +
 .cache/prompts/data_science_domain.json            |    1 +
 .cache/prompts/data_science_system.json            |    1 +
 .cache/prompts/financial_domain.json               |    1 +
 .cache/prompts/financial_system.json               |    1 +
 .cache/prompts/legal_domain.json                   |    1 +
 .cache/prompts/legal_system.json                   |    1 +
 ...fessional_analysis_20251105_143407_context.json |    1 +
 ...fessional_analysis_20251105_143445_context.json |    1 +
 ...fessional_analysis_20251105_143753_context.json |    1 +
 ...fessional_analysis_20251105_144305_context.json |    1 +
 ...fessional_analysis_20251105_144547_context.json |    1 +
 .../prompts/profound_test_cba_reports_context.json |    1 +
 .cache/prompts/risk_domain.json                    |    1 +
 .cache/prompts/risk_system.json                    |    1 +
 .cache/prompts/test_lmstudio_001_context.json      |    1 +
 .change_tracking_state.json                        |    4 +-
 .claude/commands/ai-project-evaluator.md           |   57 +
 .env                                               |   82 +
 .env.development                                   |   64 +
 .env.investigation                                 |   76 +
 .gitignore                                         |    7 +
 ANALIZA_JAKOSCI_PROFESSIONAL_ANALYZER.md           |  273 ++
 ANALIZA_KRYTYCZNA_SYSTEMU_INVESTIGATIVE_QUALITY.md | 1119 ++++++
 ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU.md               |  280 ++
 ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU_PELNY.md         |  295 ++
 AUTONOMOUS_SYSTEM_GUIDE.md                         |  631 ++++
 BENCHMARK_COMPARISON_2023.md                       |  475 +++
 CBA_COMPREHENSIVE_ANALYSIS_2024.md                 |  523 +++
 CBA_FULL_CONTENT_ANALYSIS.md                       |  617 ++++
 CBA_FULL_CONTENT_ANALYSIS_data.json                | 3867 ++++++++++++++++++++
 CBA_PROFESSIONAL_ANALYSIS_FINAL_results.json       |   41 +
 CBA_PROFESSIONAL_ANALYSIS_REPORT_full_data.json    |   50 +
 COMPARISON_SUMMARY.md                              |  444 +++
 FINAL_ANALYSIS_LOCAL_SYSTEM.md                     |  224 ++
 FIXES_COMPLETE_SUCCESS.md                          |  482 +++
 FULL_HOG_FINAL_STATUS.md                           |  482 +++
 GRAF_RELACJI_STATUS.md                             |  632 ++++
 HOW_I_WOULD_ANALYZE_CBA_REPORTS.md                 |  492 +++
 IMPLEMENTACJA_POPRAWEK.md                          |  130 +
 IMPLEMENTATION_STATUS.md                           |  424 +++
 IMPLEMENTATION_STATUS_FINAL.md                     |  578 +++
 INTELLIGENCE_SYSTEM_ROADMAP.md                     | 2686 ++++++++++++++
 INVESTIGATIVE_INTEGRATION_COMPLETE.md              |  354 ++
 ISTNIEJACE_KONTENERY_ANALIZA.md                    |  336 ++
 LMSTUDIO_INTEGRATION_COMPLETE.md                   |  453 +++
 LOCAL_EXTRACTION_RESULTS_2023.json                 |   23 +
 LOCAL_INTERPRETATION_LAYER.md                      |  238 ++
 MIGRACJA_VOLUMES.md                                |  171 +
 MULTI_AGENT_ARCHITECTURE.md                        |  441 +++
 MULTI_AGENT_SYSTEM_COMPLETE.md                     |  645 ++++
 MVP_AI_SPECIALIST_AGENT_DESIGN.md                  | 1143 ++++++
 NEO4J_STATUS.md                                    |  147 +
 OCENA_JAKOSCI_ANALIZY.md                           |  144 +
 ON_PREMISE_SYSTEM_READY.md                         |  244 ++
 PELNA_ANALIZA_PROJEKTU_WSZYSTKIE_KOMPONENTY.md     | 1080 ++++++
 PHASE1_COMPLETION_REPORT.md                        |  341 ++
 PIPELINE_ANALITYCZNY_PELNY_OPIS.md                 | 1013 +++++
 POROWNANIE_SYSTEM_VS_AI_ANALYSIS.md                |  572 +++
 PRACTICAL_INTELLIGENCE_ROADMAP.md                  | 1539 ++++++++
 PRECYZYJNY_PODZIAL.md                              |  675 ++++
 PROFOUND_TEST_CONCLUSIONS.md                       |  597 +++
 RAG_INTEGRATION_COMPLETE.md                        |  383 ++
 RAG_SYSTEM_SUMMARY.md                              |  464 +++
 README_RESULTS.md                                  |   79 +
 REAL_PARSING_COMPLETE.md                           |  267 ++
 RESULTS_QUICK_START.md                             |  395 ++
 RESULTS_STORAGE_ARCHITECTURE.md                    |  583 +++
 RESULTS_STORAGE_SEPARATION.md                      |  397 ++
 RESULTS_SUMMARY.md                                 |  341 ++
 SEPARACJA_DANYCH_DEVELOPMENT.md                    |  486 +++
 SINGLE_VS_MULTI_AGENT_COMPARISON.md                |  747 ++++
 START_DEVELOPMENT.sh                               |   62 +
 SUCCESS_SUMMARY.md                                 |  200 +
 TEST_INSTRUCTIONS.md                               |  415 +++
 THREE_WAY_COMPARISON_LOCAL_VS_CLAUDE.md            |  687 ++++
 WEEK2_DAY1_COMPLETION.md                           |  562 +++
 WERYFIKACJA_PODZIALU.md                            |  294 ++
 WNIOSKI_ARTUR.md                                   |  454 +++
 WYSZUKIWANIE_STATUS.md                             |  537 +++
 analysis_rounds/round_1/README.md                  |  393 ++
 .../round_1/alex_document_processing.md            |  288 ++
 .../round_1/marcus_financial_analysis.md           |  160 +
 analysis_rounds/round_1/workflow_alex_marcus.md    |  346 ++
 analyze_cba_content.py                             |  580 +++
 analyze_cba_pdfs.py                                |  615 ++++
 case_cli.py                                        |  265 ++
 cba_content_analysis_log.txt                       |   88 +
 cba_detection_results.txt                          |  207 ++
 cba_full_analysis_log.txt                          |   54 +
 data/companies/grupa_azoty_sa.json                 |   18 +
 destiny_auto.py                                    |  162 +
 docker-compose-dev.yml                             |  183 +
 docs/architecture/RAG_CAG_STRATEGY.md              |  437 +++
 .../2025-11-05/COMMIT_d4adf31_feature.md           |   78 +
 .../2025-11-05/COMMIT_f0d49b5_feature.md           |  938 +++++
 .../2025-11-06/COMMIT_3d81426_feature.md           |  142 +
 .../2025-11-06/COMMIT_457c53c_feature.md           |  269 ++
 .../2025-11-06/COMMIT_9c14593_feature.md           |  267 ++
 .../PLAN_IMPLEMENTACJI_POPRAWY_ANALIZY_CBA.md      |  527 +++
 .../POTWIERDZENIE_MODELI_EMBEDDINGOW.md            |   91 +
 .../STRATEGIA_EMBEDDINGOW_JINA_VS_E5.md            |  514 +++
 docs/status/MORNING_BRIEF_20251105.md              |  159 +
 docs/status/MORNING_BRIEF_20251106.md              |  156 +
 full_analysis_results_20251105_143433.json         |   95 +
 full_analysis_results_20251105_143824.json         | 1707 +++++++++
 full_analysis_results_20251105_144346.json         | 1714 +++++++++
 full_analysis_results_20251105_144624.json         | 1714 +++++++++
 .../helena_task_20251105_110000_agent_code.md      |  204 ++
 .../helena_task_20251105_110000_configuration.md   |  207 ++
 .../helena_task_20251105_110000_database_schema.md |  203 +
 .../helena_task_20251105_110000_documentation.md   |  202 +
 .../helena_task_20251105_110000_general_change.md  |  203 +
 .../helena_task_20251105_110000_knowledge_graph.md |  193 +
 .../helena_task_20251105_130000_general_change.md  |  200 +
 .../helena_task_20251105_140000_general_change.md  |  200 +
 .../helena_task_20251105_150000_documentation.md   |  202 +
 .../helena_task_20251105_150000_general_change.md  |  203 +
 .../helena_task_20251106_210000_documentation.md   |  200 +
 .../helena_task_20251106_210000_general_change.md  |  211 ++
 ...ime_20251105_104923_COMMIT_f0d49b5_feature.json |    9 +
 ...me_20251105_105739_AUTONOMOUS_SYSTEM_GUIDE.json |    9 +
 ..._realtime_20251105_110102_RAG_CAG_STRATEGY.json |    9 +
 ...time_20251105_110237_WEEK2_DAY1_COMPLETION.json |    9 +
 ...51105_111232_LMSTUDIO_INTEGRATION_COMPLETE.json |    9 +
 ...time_20251105_111355_FULL_HOG_FINAL_STATUS.json |    9 +
 .../success_realtime_20251105_111541_README.json   |    9 +
 ...time_20251105_113504_REAL_PARSING_COMPLETE.json |    9 +
 ...ess_realtime_20251105_114107_WNIOSKI_ARTUR.json |    9 +
 ...ime_20251105_114855_FIXES_COMPLETE_SUCCESS.json |    9 +
 ...s_realtime_20251105_114943_SUCCESS_SUMMARY.json |    9 +
 ...time_20251105_115119_ANALIZA_CBA_2008-2024.json |    9 +
 .../success_realtime_20251105_115422_README.json   |    9 +
 ...altime_20251105_115928_WYSZUKIWANIE_STATUS.json |    9 +
 ...altime_20251105_120115_GRAF_RELACJI_STATUS.json |    9 +
 ...cess_realtime_20251105_120711_NEO4J_STATUS.json |    9 +
 ...251105_121013_ISTNIEJACE_KONTENERY_ANALIZA.json |    9 +
 ...251105_121125_SEPARACJA_DANYCH_DEVELOPMENT.json |    9 +
 ...ealtime_20251105_121305_PRECYZYJNY_PODZIAL.json |    9 +
 ...ltime_20251105_121450_WERYFIKACJA_PODZIALU.json |    9 +
 ..._realtime_20251105_121736_MIGRACJA_VOLUMES.json |    9 +
 ...251105_131838_RESULTS_STORAGE_ARCHITECTURE.json |    9 +
 ...altime_20251105_132144_RESULTS_QUICK_START.json |    9 +
 ...20251105_132326_RESULTS_STORAGE_SEPARATION.json |    9 +
 ...ss_realtime_20251105_132400_README_RESULTS.json |    9 +
 ...s_realtime_20251105_132451_RESULTS_SUMMARY.json |    9 +
 ...51105_133123_cba_analiza_merytoryczna_2024.json |    9 +
 ...1105_133443_cba_weryfikacja_i_rekomendacje.json |    9 +
 ...637_PLAN_IMPLEMENTACJI_POPRAWY_ANALIZY_CBA.json |    9 +
 ...05_133710_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.json |    9 +
 ...05_133725_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.json |    9 +
 ...05_133727_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.json |    9 +
 ...05_133730_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.json |    9 +
 ...05_133737_POTWIERDZENIE_MODELI_EMBEDDINGOW.json |    9 +
 ...ltime_20251105_134418_STATUS_GOTOWOSCI_CBA.json |    9 +
 ...ltime_20251105_134721_GOTOWOSC_SYSTEMU_CBA.json |    9 +
 ...time_20251105_135015_EWALUACJA_SYSTEMU_CBA.json |    9 +
 ...51105_135041_EWALUACJA_SYSTEMU_CBA_SUMMARY.json |    9 +
 ...me_20251105_140043_AUTONOMOUS_SYSTEM_GUIDE.json |    9 +
 ...me_20251105_140054_AUTONOMOUS_SYSTEM_GUIDE.json |    9 +
 ...me_20251105_140110_AUTONOMOUS_SYSTEM_GUIDE.json |    9 +
 ...me_20251105_140140_AUTONOMOUS_SYSTEM_GUIDE.json |    9 +
 ..._140240_INVESTIGATIVE_INTEGRATION_COMPLETE.json |    9 +
 ...105_140650_CBA_COMPREHENSIVE_ANALYSIS_2024.json |    9 +
 ..._20251105_141209_CBA_FULL_CONTENT_ANALYSIS.json |    9 +
 ...0251105_141722_IMPLEMENTATION_STATUS_FINAL.json |    9 +
 ...105_142247_HOW_I_WOULD_ANALYZE_CBA_REPORTS.json |    9 +
 ...05_142507_CBA_PROFESSIONAL_ANALYSIS_REPORT.json |    9 +
 ..._20251105_142512_CBA_FULL_CONTENT_ANALYSIS.json |    9 +
 ...05_142544_CBA_PROFESSIONAL_ANALYSIS_REPORT.json |    9 +
 ..._HOW_TO_TEACH_SYSTEM_PROFESSIONAL_ANALYSIS.json |    9 +
 ...105_142757_CBA_PROFESSIONAL_ANALYSIS_FINAL.json |    9 +
 ...ime_20251105_142935_COMMIT_d4adf31_feature.json |    9 +
 ...105_143557_PIPELINE_ANALITYCZNY_PELNY_OPIS.json |    9 +
 ...3844_ANALIZA_JAKOSCI_PROFESSIONAL_ANALYZER.json |    9 +
 ...05_144019_POROWNANIE_SYSTEM_VS_AI_ANALYSIS.json |    9 +
 ...20251105_144257_LOCAL_INTERPRETATION_LAYER.json |    9 +
 ...me_20251105_144359_ON_PREMISE_SYSTEM_READY.json |    9 +
 ...5_144657_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU.json |    9 +
 ...28_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU_PELNY.json |    9 +
 ...0251105_144744_FINAL_ANALYSIS_LOCAL_SYSTEM.json |    9 +
 ...time_20251105_144952_OCENA_JAKOSCI_ANALIZY.json |    9 +
 ...ime_20251105_145122_IMPLEMENTACJA_POPRAWEK.json |    9 +
 ...e_20251106_153940_PHASE2_COMPLETION_REPORT.json |    9 +
 ...me_20251106_170529_FINAL_EXTRACTION_REPORT.json |    9 +
 ...ime_20251106_172205_COMMIT_457c53c_feature.json |    9 +
 ...106_173640_INTELLIGENT_EXTRACTION_COMPLETE.json |    9 +
 ...ime_20251106_173724_COMMIT_9c14593_feature.json |    9 +
 ...ime_20251106_210140_COMMIT_3d81426_feature.json |    9 +
 ..._20251106_211911_BENCHMARK_COMPARISON_2023.json |    9 +
 ..._20251106_211927_BENCHMARK_COMPARISON_2023.json |    9 +
 ..._20251106_212247_BENCHMARK_COMPARISON_2023.json |    9 +
 ..._20251106_212256_BENCHMARK_COMPARISON_2023.json |    9 +
 ...7_Azoty_Intelligence_Local_20251106_214207.json |    9 +
 ...ealtime_20251106_220127_RAG_SYSTEM_SUMMARY.json |    9 +
 ...ltime_20251106_220301_Azoty_Baseline_NoRAG.json |    9 +
 ...ealtime_20251106_220341_Azoty_RAG_Enhanced.json |    9 +
 ...ealtime_20251106_220529_Azoty_RAG_Enhanced.json |    9 +
 ...06_222059_Azoty_MultiAgent_20251106_222059.json |    9 +
 migrate_existing_results.py                        |  121 +
 .../intelligence_reports/Azoty_Baseline_NoRAG.md   |  317 ++
 .../Azoty_Claude_Analysis_20251106.md              |  407 ++
 .../Azoty_Intelligence_Local_20251106_214207.md    |  314 ++
 .../Azoty_MultiAgent_20251106_222059.md            |  154 +
 output/intelligence_reports/Azoty_RAG_Enhanced.md  |  332 ++
 profound_test.py                                   |  398 ++
 ...doc_20251105_104923_COMMIT_f0d49b5_feature.json |    8 +
 ...oc_20251105_105739_AUTONOMOUS_SYSTEM_GUIDE.json |    8 +
 .../doc_20251105_110102_RAG_CAG_STRATEGY.json      |    8 +
 .../doc_20251105_110237_WEEK2_DAY1_COMPLETION.json |    8 +
 ...51105_111232_LMSTUDIO_INTEGRATION_COMPLETE.json |    8 +
 .../doc_20251105_111355_FULL_HOG_FINAL_STATUS.json |    8 +
 .../indexed/doc_20251105_111541_README.json        |    8 +
 .../doc_20251105_113504_REAL_PARSING_COMPLETE.json |    8 +
 .../indexed/doc_20251105_114107_WNIOSKI_ARTUR.json |    8 +
 ...doc_20251105_114856_FIXES_COMPLETE_SUCCESS.json |    8 +
 .../doc_20251105_114944_SUCCESS_SUMMARY.json       |    8 +
 .../doc_20251105_115119_ANALIZA_CBA_2008-2024.json |    8 +
 .../indexed/doc_20251105_115423_README.json        |    8 +
 .../doc_20251105_115929_WYSZUKIWANIE_STATUS.json   |    8 +
 .../doc_20251105_120115_GRAF_RELACJI_STATUS.json   |    8 +
 .../indexed/doc_20251105_120711_NEO4J_STATUS.json  |    8 +
 ...251105_121014_ISTNIEJACE_KONTENERY_ANALIZA.json |    8 +
 ...251105_121125_SEPARACJA_DANYCH_DEVELOPMENT.json |    8 +
 .../doc_20251105_121306_PRECYZYJNY_PODZIAL.json    |    8 +
 .../doc_20251105_121451_WERYFIKACJA_PODZIALU.json  |    8 +
 .../doc_20251105_121737_MIGRACJA_VOLUMES.json      |    8 +
 ...251105_131839_RESULTS_STORAGE_ARCHITECTURE.json |    8 +
 .../doc_20251105_132145_RESULTS_QUICK_START.json   |    8 +
 ...20251105_132326_RESULTS_STORAGE_SEPARATION.json |    8 +
 .../doc_20251105_132400_README_RESULTS.json        |    8 +
 .../doc_20251105_132452_RESULTS_SUMMARY.json       |    8 +
 ...51105_133124_cba_analiza_merytoryczna_2024.json |    8 +
 ...1105_133444_cba_weryfikacja_i_rekomendacje.json |    8 +
 ...637_PLAN_IMPLEMENTACJI_POPRAWY_ANALIZY_CBA.json |    8 +
 ...05_133711_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.json |    8 +
 ...05_133725_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.json |    8 +
 ...05_133728_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.json |    8 +
 ...05_133731_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.json |    8 +
 ...05_133737_POTWIERDZENIE_MODELI_EMBEDDINGOW.json |    8 +
 .../doc_20251105_134418_STATUS_GOTOWOSCI_CBA.json  |    8 +
 .../doc_20251105_134722_GOTOWOSC_SYSTEMU_CBA.json  |    8 +
 .../doc_20251105_135015_EWALUACJA_SYSTEMU_CBA.json |    8 +
 ...51105_135041_EWALUACJA_SYSTEMU_CBA_SUMMARY.json |    8 +
 ...oc_20251105_140043_AUTONOMOUS_SYSTEM_GUIDE.json |    8 +
 ...oc_20251105_140055_AUTONOMOUS_SYSTEM_GUIDE.json |    8 +
 ...oc_20251105_140110_AUTONOMOUS_SYSTEM_GUIDE.json |    8 +
 ...oc_20251105_140140_AUTONOMOUS_SYSTEM_GUIDE.json |    8 +
 ..._140241_INVESTIGATIVE_INTEGRATION_COMPLETE.json |    8 +
 ...105_140651_CBA_COMPREHENSIVE_ANALYSIS_2024.json |    8 +
 ..._20251105_141210_CBA_FULL_CONTENT_ANALYSIS.json |    8 +
 ...0251105_141722_IMPLEMENTATION_STATUS_FINAL.json |    8 +
 ...105_142248_HOW_I_WOULD_ANALYZE_CBA_REPORTS.json |    8 +
 ...05_142507_CBA_PROFESSIONAL_ANALYSIS_REPORT.json |    8 +
 ..._20251105_142513_CBA_FULL_CONTENT_ANALYSIS.json |    8 +
 ...05_142545_CBA_PROFESSIONAL_ANALYSIS_REPORT.json |    8 +
 ..._HOW_TO_TEACH_SYSTEM_PROFESSIONAL_ANALYSIS.json |    8 +
 ...105_142758_CBA_PROFESSIONAL_ANALYSIS_FINAL.json |    8 +
 ...doc_20251105_142935_COMMIT_d4adf31_feature.json |    8 +
 ...105_143558_PIPELINE_ANALITYCZNY_PELNY_OPIS.json |    8 +
 ...3845_ANALIZA_JAKOSCI_PROFESSIONAL_ANALYZER.json |    8 +
 ...05_144020_POROWNANIE_SYSTEM_VS_AI_ANALYSIS.json |    8 +
 ...20251105_144257_LOCAL_INTERPRETATION_LAYER.json |    8 +
 ...oc_20251105_144359_ON_PREMISE_SYSTEM_READY.json |    8 +
 ...5_144658_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU.json |    8 +
 ...28_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU_PELNY.json |    8 +
 ...0251105_144745_FINAL_ANALYSIS_LOCAL_SYSTEM.json |    8 +
 .../doc_20251105_144952_OCENA_JAKOSCI_ANALIZY.json |    8 +
 ...doc_20251105_145122_IMPLEMENTACJA_POPRAWEK.json |    8 +
 ...c_20251106_153941_PHASE2_COMPLETION_REPORT.json |    8 +
 ...oc_20251106_170530_FINAL_EXTRACTION_REPORT.json |    8 +
 ...doc_20251106_172206_COMMIT_457c53c_feature.json |    8 +
 ...106_173640_INTELLIGENT_EXTRACTION_COMPLETE.json |    8 +
 ...doc_20251106_173724_COMMIT_9c14593_feature.json |    8 +
 ...doc_20251106_210141_COMMIT_3d81426_feature.json |    8 +
 ..._20251106_211912_BENCHMARK_COMPARISON_2023.json |    8 +
 ..._20251106_211928_BENCHMARK_COMPARISON_2023.json |    8 +
 ..._20251106_212248_BENCHMARK_COMPARISON_2023.json |    8 +
 ..._20251106_212256_BENCHMARK_COMPARISON_2023.json |    8 +
 ...8_Azoty_Intelligence_Local_20251106_214207.json |    8 +
 .../doc_20251106_220128_RAG_SYSTEM_SUMMARY.json    |    8 +
 .../doc_20251106_220302_Azoty_Baseline_NoRAG.json  |    8 +
 .../doc_20251106_220342_Azoty_RAG_Enhanced.json    |    8 +
 .../doc_20251106_220529_Azoty_RAG_Enhanced.json    |    8 +
 ...06_222100_Azoty_MultiAgent_20251106_222059.json |    8 +
 quality_report_20251105_143433.json                |   32 +
 quality_report_20251105_143824.json                | 1543 ++++++++
 quality_report_20251105_144346.json                | 1550 ++++++++
 quality_report_20251105_144624.json                | 1550 ++++++++
 ...edis_20251105_104923_COMMIT_f0d49b5_feature.txt |   36 +
 ...dis_20251105_105739_AUTONOMOUS_SYSTEM_GUIDE.txt |   59 +
 .../redis_20251105_110103_RAG_CAG_STRATEGY.txt     |   40 +
 ...redis_20251105_110237_WEEK2_DAY1_COMPLETION.txt |   54 +
 ...251105_111232_LMSTUDIO_INTEGRATION_COMPLETE.txt |   58 +
 ...redis_20251105_111355_FULL_HOG_FINAL_STATUS.txt |   37 +
 redis_pending/redis_20251105_111541_README.txt     |   45 +
 ...redis_20251105_113504_REAL_PARSING_COMPLETE.txt |   65 +
 .../redis_20251105_114107_WNIOSKI_ARTUR.txt        |   62 +
 ...edis_20251105_114856_FIXES_COMPLETE_SUCCESS.txt |   45 +
 .../redis_20251105_114944_SUCCESS_SUMMARY.txt      |   62 +
 ...redis_20251105_115119_ANALIZA_CBA_2008-2024.txt |   40 +
 redis_pending/redis_20251105_115423_README.txt     |   51 +
 .../redis_20251105_115929_WYSZUKIWANIE_STATUS.txt  |   54 +
 .../redis_20251105_120115_GRAF_RELACJI_STATUS.txt  |   50 +
 .../redis_20251105_120711_NEO4J_STATUS.txt         |   63 +
 ...0251105_121014_ISTNIEJACE_KONTENERY_ANALIZA.txt |   41 +
 ...0251105_121125_SEPARACJA_DANYCH_DEVELOPMENT.txt |   41 +
 .../redis_20251105_121306_PRECYZYJNY_PODZIAL.txt   |   35 +
 .../redis_20251105_121451_WERYFIKACJA_PODZIALU.txt |   27 +
 .../redis_20251105_121737_MIGRACJA_VOLUMES.txt     |   46 +
 ...0251105_131839_RESULTS_STORAGE_ARCHITECTURE.txt |   37 +
 .../redis_20251105_132145_RESULTS_QUICK_START.txt  |   62 +
 ..._20251105_132326_RESULTS_STORAGE_SEPARATION.txt |   44 +
 .../redis_20251105_132400_README_RESULTS.txt       |   43 +
 .../redis_20251105_132452_RESULTS_SUMMARY.txt      |   43 +
 ...251105_133124_cba_analiza_merytoryczna_2024.txt |   31 +
 ...51105_133444_cba_weryfikacja_i_rekomendacje.txt |   28 +
 ...3637_PLAN_IMPLEMENTACJI_POPRAWY_ANALIZY_CBA.txt |   39 +
 ...105_133711_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.txt |   42 +
 ...105_133725_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.txt |   42 +
 ...105_133728_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.txt |   42 +
 ...105_133731_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.txt |   42 +
 ...105_133737_POTWIERDZENIE_MODELI_EMBEDDINGOW.txt |   58 +
 .../redis_20251105_134418_STATUS_GOTOWOSCI_CBA.txt |   46 +
 .../redis_20251105_134722_GOTOWOSC_SYSTEMU_CBA.txt |   45 +
 ...redis_20251105_135015_EWALUACJA_SYSTEMU_CBA.txt |   37 +
 ...251105_135041_EWALUACJA_SYSTEMU_CBA_SUMMARY.txt |   50 +
 ...dis_20251105_140043_AUTONOMOUS_SYSTEM_GUIDE.txt |   59 +
 ...dis_20251105_140055_AUTONOMOUS_SYSTEM_GUIDE.txt |   59 +
 ...dis_20251105_140110_AUTONOMOUS_SYSTEM_GUIDE.txt |   59 +
 ...dis_20251105_140140_AUTONOMOUS_SYSTEM_GUIDE.txt |   59 +
 ...5_140241_INVESTIGATIVE_INTEGRATION_COMPLETE.txt |   41 +
 ...1105_140651_CBA_COMPREHENSIVE_ANALYSIS_2024.txt |   41 +
 ...s_20251105_141210_CBA_FULL_CONTENT_ANALYSIS.txt |   54 +
 ...20251105_141722_IMPLEMENTATION_STATUS_FINAL.txt |   37 +
 ...1105_142248_HOW_I_WOULD_ANALYZE_CBA_REPORTS.txt |   44 +
 ...105_142507_CBA_PROFESSIONAL_ANALYSIS_REPORT.txt |   64 +
 ...s_20251105_142513_CBA_FULL_CONTENT_ANALYSIS.txt |   54 +
 ...105_142545_CBA_PROFESSIONAL_ANALYSIS_REPORT.txt |   43 +
 ...6_HOW_TO_TEACH_SYSTEM_PROFESSIONAL_ANALYSIS.txt |   47 +
 ...1105_142758_CBA_PROFESSIONAL_ANALYSIS_FINAL.txt |   64 +
 ...edis_20251105_142935_COMMIT_d4adf31_feature.txt |   47 +
 ...1105_143558_PIPELINE_ANALITYCZNY_PELNY_OPIS.txt |   32 +
 ...43845_ANALIZA_JAKOSCI_PROFESSIONAL_ANALYZER.txt |   41 +
 ...105_144020_POROWNANIE_SYSTEM_VS_AI_ANALYSIS.txt |   29 +
 ..._20251105_144258_LOCAL_INTERPRETATION_LAYER.txt |   34 +
 ...dis_20251105_144359_ON_PREMISE_SYSTEM_READY.txt |   38 +
 ...05_144658_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU.txt |   43 +
 ...728_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU_PELNY.txt |   43 +
 ...20251105_144745_FINAL_ANALYSIS_LOCAL_SYSTEM.txt |   42 +
 ...redis_20251105_144952_OCENA_JAKOSCI_ANALIZY.txt |   42 +
 ...edis_20251105_145122_IMPLEMENTACJA_POPRAWEK.txt |   44 +
 ...is_20251106_153941_PHASE2_COMPLETION_REPORT.txt |   40 +
 ...dis_20251106_170530_FINAL_EXTRACTION_REPORT.txt |   37 +
 ...edis_20251106_172206_COMMIT_457c53c_feature.txt |   35 +
 ...1106_173641_INTELLIGENT_EXTRACTION_COMPLETE.txt |   30 +
 ...edis_20251106_173724_COMMIT_9c14593_feature.txt |   40 +
 ...edis_20251106_210141_COMMIT_3d81426_feature.txt |   35 +
 ...s_20251106_211912_BENCHMARK_COMPARISON_2023.txt |   28 +
 ...s_20251106_211928_BENCHMARK_COMPARISON_2023.txt |   28 +
 ...s_20251106_212248_BENCHMARK_COMPARISON_2023.txt |   28 +
 ...s_20251106_212256_BENCHMARK_COMPARISON_2023.txt |   28 +
 ...08_Azoty_Intelligence_Local_20251106_214207.txt |   34 +
 .../redis_20251106_220128_RAG_SYSTEM_SUMMARY.txt   |   39 +
 .../redis_20251106_220302_Azoty_Baseline_NoRAG.txt |   30 +
 .../redis_20251106_220342_Azoty_RAG_Enhanced.txt   |   34 +
 .../redis_20251106_220530_Azoty_RAG_Enhanced.txt   |   34 +
 ...106_222100_Azoty_MultiAgent_20251106_222059.txt |   29 +
 reports/EWALUACJA_SYSTEMU_CBA.md                   |  402 ++
 reports/EWALUACJA_SYSTEMU_CBA_SUMMARY.md           |  123 +
 reports/GOTOWOSC_SYSTEMU_CBA.md                    |  227 ++
 reports/IMPLEMENTACJA_I_TESTY_RAPORT.md            |  266 ++
 reports/STATUS_GOTOWOSCI_CBA.md                    |  144 +
 reports/autonomous_cba_analysis_2024.json          |  117 +
 reports/autonomous_cba_full_test_v2.json           |  563 +++
 reports/autonomous_cba_test_integration.json       |  209 ++
 ...mous_professional_analysis_20251105_143407.json |   95 +
 ...mous_professional_analysis_20251105_143445.json | 1707 +++++++++
 ...mous_professional_analysis_20251105_143753.json | 1707 +++++++++
 ...mous_professional_analysis_20251105_144305.json | 1714 +++++++++
 ...mous_professional_analysis_20251105_144547.json | 1714 +++++++++
 reports/autonomous_profound_test_cba_reports.json  |  117 +
 reports/autonomous_real_parsing_test.json          |  168 +
 reports/autonomous_test_lmstudio_001.json          |  153 +
 reports/cba_analiza_merytoryczna_2024.html         |  436 +++
 reports/cba_analiza_merytoryczna_2024.md           |  281 ++
 reports/cba_analysis_2024.html                     |  299 ++
 reports/cba_extraction_results.json                |   34 +
 reports/cba_real_data_extracted.json               |  203 +
 reports/cba_verification_extraction.json           |   57 +
 reports/cba_weryfikacja_i_rekomendacje.md          |  411 +++
 scripts/generate_claude_analysis.py                |  189 +
 scripts/ingest_azoty_to_rag.py                     |   55 +
 scripts/init_all_databases.sh                      |  172 +
 scripts/init_postgres.sh                           |  204 ++
 scripts/reingest_with_sections.py                  |   47 +
 scripts/save_azoty_data.py                         |   75 +
 scripts/test_intelligence_azoty.py                 |  131 +
 scripts/test_multi_agent_azoty.py                  |  157 +
 scripts/test_rag_enhanced_report.py                |  144 +
 scripts/test_rag_queries.py                        |   66 +
 ...j_20251105_104923_COMMIT_f0d49b5_feature.cypher |   10 +
 ..._20251105_105739_AUTONOMOUS_SYSTEM_GUIDE.cypher |   10 +
 .../neo4j_20251105_110102_RAG_CAG_STRATEGY.cypher  |   10 +
 ...4j_20251105_110237_WEEK2_DAY1_COMPLETION.cypher |   10 +
 ...105_111232_LMSTUDIO_INTEGRATION_COMPLETE.cypher |   10 +
 ...4j_20251105_111355_FULL_HOG_FINAL_STATUS.cypher |   10 +
 .../neo4j_20251105_111541_README.cypher            |   10 +
 ...4j_20251105_113504_REAL_PARSING_COMPLETE.cypher |   10 +
 .../neo4j_20251105_114107_WNIOSKI_ARTUR.cypher     |   10 +
 ...j_20251105_114856_FIXES_COMPLETE_SUCCESS.cypher |   10 +
 .../neo4j_20251105_114944_SUCCESS_SUMMARY.cypher   |   10 +
 ...4j_20251105_115119_ANALIZA_CBA_2008-2024.cypher |   10 +
 .../neo4j_20251105_115423_README.cypher            |   10 +
 ...eo4j_20251105_115929_WYSZUKIWANIE_STATUS.cypher |   10 +
 ...eo4j_20251105_120115_GRAF_RELACJI_STATUS.cypher |   10 +
 .../neo4j_20251105_120711_NEO4J_STATUS.cypher      |   10 +
 ...1105_121014_ISTNIEJACE_KONTENERY_ANALIZA.cypher |   10 +
 ...1105_121125_SEPARACJA_DANYCH_DEVELOPMENT.cypher |   10 +
 ...neo4j_20251105_121306_PRECYZYJNY_PODZIAL.cypher |   10 +
 ...o4j_20251105_121451_WERYFIKACJA_PODZIALU.cypher |   10 +
 .../neo4j_20251105_121737_MIGRACJA_VOLUMES.cypher  |   10 +
 ...1105_131839_RESULTS_STORAGE_ARCHITECTURE.cypher |   10 +
 ...eo4j_20251105_132145_RESULTS_QUICK_START.cypher |   10 +
 ...251105_132326_RESULTS_STORAGE_SEPARATION.cypher |   10 +
 .../neo4j_20251105_132400_README_RESULTS.cypher    |   10 +
 .../neo4j_20251105_132452_RESULTS_SUMMARY.cypher   |   10 +
 ...105_133124_cba_analiza_merytoryczna_2024.cypher |   10 +
 ...05_133444_cba_weryfikacja_i_rekomendacje.cypher |   10 +
 ...7_PLAN_IMPLEMENTACJI_POPRAWY_ANALIZY_CBA.cypher |   10 +
 ..._133711_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.cypher |   10 +
 ..._133725_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.cypher |   10 +
 ..._133728_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.cypher |   10 +
 ..._133731_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.cypher |   10 +
 ..._133737_POTWIERDZENIE_MODELI_EMBEDDINGOW.cypher |   10 +
 ...o4j_20251105_134418_STATUS_GOTOWOSCI_CBA.cypher |   10 +
 ...o4j_20251105_134722_GOTOWOSC_SYSTEMU_CBA.cypher |   10 +
 ...4j_20251105_135015_EWALUACJA_SYSTEMU_CBA.cypher |   10 +
 ...105_135041_EWALUACJA_SYSTEMU_CBA_SUMMARY.cypher |   10 +
 ..._20251105_140043_AUTONOMOUS_SYSTEM_GUIDE.cypher |   10 +
 ..._20251105_140055_AUTONOMOUS_SYSTEM_GUIDE.cypher |   10 +
 ..._20251105_140110_AUTONOMOUS_SYSTEM_GUIDE.cypher |   10 +
 ..._20251105_140140_AUTONOMOUS_SYSTEM_GUIDE.cypher |   10 +
 ...40241_INVESTIGATIVE_INTEGRATION_COMPLETE.cypher |   10 +
 ...5_140651_CBA_COMPREHENSIVE_ANALYSIS_2024.cypher |   10 +
 ...0251105_141210_CBA_FULL_CONTENT_ANALYSIS.cypher |   10 +
 ...51105_141722_IMPLEMENTATION_STATUS_FINAL.cypher |   10 +
 ...5_142248_HOW_I_WOULD_ANALYZE_CBA_REPORTS.cypher |   10 +
 ..._142507_CBA_PROFESSIONAL_ANALYSIS_REPORT.cypher |   10 +
 ...0251105_142513_CBA_FULL_CONTENT_ANALYSIS.cypher |   10 +
 ..._142545_CBA_PROFESSIONAL_ANALYSIS_REPORT.cypher |   10 +
 ...OW_TO_TEACH_SYSTEM_PROFESSIONAL_ANALYSIS.cypher |   10 +
 ...5_142758_CBA_PROFESSIONAL_ANALYSIS_FINAL.cypher |   10 +
 ...j_20251105_142935_COMMIT_d4adf31_feature.cypher |   10 +
 ...5_143558_PIPELINE_ANALITYCZNY_PELNY_OPIS.cypher |   10 +
 ...45_ANALIZA_JAKOSCI_PROFESSIONAL_ANALYZER.cypher |   10 +
 ..._144020_POROWNANIE_SYSTEM_VS_AI_ANALYSIS.cypher |   10 +
 ...251105_144257_LOCAL_INTERPRETATION_LAYER.cypher |   10 +
 ..._20251105_144359_ON_PREMISE_SYSTEM_READY.cypher |   10 +
 ...144658_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU.cypher |   10 +
 ..._ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU_PELNY.cypher |   10 +
 ...51105_144745_FINAL_ANALYSIS_LOCAL_SYSTEM.cypher |   10 +
 ...4j_20251105_144952_OCENA_JAKOSCI_ANALIZY.cypher |   10 +
 ...j_20251105_145122_IMPLEMENTACJA_POPRAWEK.cypher |   10 +
 ...20251106_153941_PHASE2_COMPLETION_REPORT.cypher |   10 +
 ..._20251106_170530_FINAL_EXTRACTION_REPORT.cypher |   10 +
 ...j_20251106_172206_COMMIT_457c53c_feature.cypher |   10 +
 ...6_173640_INTELLIGENT_EXTRACTION_COMPLETE.cypher |   10 +
 ...j_20251106_173724_COMMIT_9c14593_feature.cypher |   10 +
 ...j_20251106_210141_COMMIT_3d81426_feature.cypher |   10 +
 ...0251106_211912_BENCHMARK_COMPARISON_2023.cypher |   10 +
 ...0251106_211928_BENCHMARK_COMPARISON_2023.cypher |   10 +
 ...0251106_212248_BENCHMARK_COMPARISON_2023.cypher |   10 +
 ...0251106_212256_BENCHMARK_COMPARISON_2023.cypher |   10 +
 ...Azoty_Intelligence_Local_20251106_214207.cypher |   10 +
 ...neo4j_20251106_220128_RAG_SYSTEM_SUMMARY.cypher |   10 +
 ...o4j_20251106_220302_Azoty_Baseline_NoRAG.cypher |   10 +
 ...neo4j_20251106_220342_Azoty_RAG_Enhanced.cypher |   10 +
 ...neo4j_20251106_220529_Azoty_RAG_Enhanced.cypher |   10 +
 ..._222100_Azoty_MultiAgent_20251106_222059.cypher |   10 +
 .../pg_20251105_104923_COMMIT_f0d49b5_feature.sql  |   26 +
 .../pg_20251105_105739_AUTONOMOUS_SYSTEM_GUIDE.sql |   25 +
 .../pg_20251105_110102_RAG_CAG_STRATEGY.sql        |   23 +
 .../pg_20251105_110237_WEEK2_DAY1_COMPLETION.sql   |   25 +
 ...251105_111232_LMSTUDIO_INTEGRATION_COMPLETE.sql |   26 +
 .../pg_20251105_111355_FULL_HOG_FINAL_STATUS.sql   |   25 +
 sql/realtime_updates/pg_20251105_111541_README.sql |   24 +
 .../pg_20251105_113504_REAL_PARSING_COMPLETE.sql   |   26 +
 .../pg_20251105_114107_WNIOSKI_ARTUR.sql           |   23 +
 .../pg_20251105_114856_FIXES_COMPLETE_SUCCESS.sql  |   28 +
 .../pg_20251105_114944_SUCCESS_SUMMARY.sql         |   24 +
 .../pg_20251105_115119_ANALIZA_CBA_2008-2024.sql   |   24 +
 sql/realtime_updates/pg_20251105_115423_README.sql |   28 +
 .../pg_20251105_115929_WYSZUKIWANIE_STATUS.sql     |   26 +
 .../pg_20251105_120115_GRAF_RELACJI_STATUS.sql     |   25 +
 .../pg_20251105_120711_NEO4J_STATUS.sql            |   28 +
 ...0251105_121014_ISTNIEJACE_KONTENERY_ANALIZA.sql |   25 +
 ...0251105_121125_SEPARACJA_DANYCH_DEVELOPMENT.sql |   24 +
 .../pg_20251105_121306_PRECYZYJNY_PODZIAL.sql      |   24 +
 .../pg_20251105_121451_WERYFIKACJA_PODZIALU.sql    |   26 +
 .../pg_20251105_121737_MIGRACJA_VOLUMES.sql        |   27 +
 ...0251105_131839_RESULTS_STORAGE_ARCHITECTURE.sql |   25 +
 .../pg_20251105_132145_RESULTS_QUICK_START.sql     |   26 +
 ..._20251105_132326_RESULTS_STORAGE_SEPARATION.sql |   25 +
 .../pg_20251105_132400_README_RESULTS.sql          |   23 +
 .../pg_20251105_132452_RESULTS_SUMMARY.sql         |   25 +
 ...251105_133124_cba_analiza_merytoryczna_2024.sql |   23 +
 ...51105_133444_cba_weryfikacja_i_rekomendacje.sql |   19 +
 ...3637_PLAN_IMPLEMENTACJI_POPRAWY_ANALIZY_CBA.sql |   25 +
 ...105_133711_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.sql |   25 +
 ...105_133725_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.sql |   25 +
 ...105_133728_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.sql |   25 +
 ...105_133730_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.sql |   25 +
 ...105_133737_POTWIERDZENIE_MODELI_EMBEDDINGOW.sql |   24 +
 .../pg_20251105_134418_STATUS_GOTOWOSCI_CBA.sql    |   24 +
 .../pg_20251105_134722_GOTOWOSC_SYSTEMU_CBA.sql    |   26 +
 .../pg_20251105_135015_EWALUACJA_SYSTEMU_CBA.sql   |   24 +
 ...251105_135041_EWALUACJA_SYSTEMU_CBA_SUMMARY.sql |   25 +
 .../pg_20251105_140043_AUTONOMOUS_SYSTEM_GUIDE.sql |   25 +
 .../pg_20251105_140055_AUTONOMOUS_SYSTEM_GUIDE.sql |   25 +
 .../pg_20251105_140110_AUTONOMOUS_SYSTEM_GUIDE.sql |   25 +
 .../pg_20251105_140140_AUTONOMOUS_SYSTEM_GUIDE.sql |   25 +
 ...5_140241_INVESTIGATIVE_INTEGRATION_COMPLETE.sql |   26 +
 ...1105_140651_CBA_COMPREHENSIVE_ANALYSIS_2024.sql |   20 +
 ...g_20251105_141210_CBA_FULL_CONTENT_ANALYSIS.sql |   20 +
 ...20251105_141722_IMPLEMENTATION_STATUS_FINAL.sql |   22 +
 ...1105_142248_HOW_I_WOULD_ANALYZE_CBA_REPORTS.sql |   20 +
 ...105_142507_CBA_PROFESSIONAL_ANALYSIS_REPORT.sql |   20 +
 ...g_20251105_142513_CBA_FULL_CONTENT_ANALYSIS.sql |   20 +
 ...105_142545_CBA_PROFESSIONAL_ANALYSIS_REPORT.sql |   20 +
 ...6_HOW_TO_TEACH_SYSTEM_PROFESSIONAL_ANALYSIS.sql |   19 +
 ...1105_142758_CBA_PROFESSIONAL_ANALYSIS_FINAL.sql |   20 +
 .../pg_20251105_142935_COMMIT_d4adf31_feature.sql  |   26 +
 ...1105_143558_PIPELINE_ANALITYCZNY_PELNY_OPIS.sql |   20 +
 ...43845_ANALIZA_JAKOSCI_PROFESSIONAL_ANALYZER.sql |   20 +
 ...105_144020_POROWNANIE_SYSTEM_VS_AI_ANALYSIS.sql |   20 +
 ..._20251105_144257_LOCAL_INTERPRETATION_LAYER.sql |   19 +
 .../pg_20251105_144359_ON_PREMISE_SYSTEM_READY.sql |   20 +
 ...05_144658_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU.sql |   20 +
 ...728_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU_PELNY.sql |   19 +
 ...20251105_144744_FINAL_ANALYSIS_LOCAL_SYSTEM.sql |   19 +
 .../pg_20251105_144952_OCENA_JAKOSCI_ANALIZY.sql   |   25 +
 .../pg_20251105_145122_IMPLEMENTACJA_POPRAWEK.sql  |   24 +
 ...pg_20251106_153941_PHASE2_COMPLETION_REPORT.sql |   20 +
 .../pg_20251106_170530_FINAL_EXTRACTION_REPORT.sql |   20 +
 .../pg_20251106_172206_COMMIT_457c53c_feature.sql  |   22 +
 ...1106_173640_INTELLIGENT_EXTRACTION_COMPLETE.sql |   19 +
 .../pg_20251106_173724_COMMIT_9c14593_feature.sql  |   25 +
 .../pg_20251106_210141_COMMIT_3d81426_feature.sql  |   21 +
 ...g_20251106_211912_BENCHMARK_COMPARISON_2023.sql |   18 +
 ...g_20251106_211928_BENCHMARK_COMPARISON_2023.sql |   18 +
 ...g_20251106_212248_BENCHMARK_COMPARISON_2023.sql |   18 +
 ...g_20251106_212256_BENCHMARK_COMPARISON_2023.sql |   18 +
 ...08_Azoty_Intelligence_Local_20251106_214207.sql |   21 +
 .../pg_20251106_220128_RAG_SYSTEM_SUMMARY.sql      |   23 +
 .../pg_20251106_220302_Azoty_Baseline_NoRAG.sql    |   21 +
 .../pg_20251106_220342_Azoty_RAG_Enhanced.sql      |   21 +
 .../pg_20251106_220529_Azoty_RAG_Enhanced.sql      |   21 +
 ...106_222100_Azoty_MultiAgent_20251106_222059.sql |   25 +
 src/analysis/__init__.py                           |   15 +
 src/analysis/comparative_analyzer.py               |  119 +
 src/analysis/critical_assessor.py                  |  140 +
 src/analysis/professional_analyzer.py              |  149 +
 src/analysis/qualitative_analyzer.py               |  149 +
 src/analysis/quantitative_extractor.py             |  293 ++
 src/analysis/structure_extractor.py                |  148 +
 src/analysis/synthesis_engine.py                   |  288 ++
 src/analysis/temporal_trend_analyzer.py            |  156 +
 src/autonomous/autonomous_orchestrator.py          |  977 +++++
 src/autonomous/document_discovery.py               |  523 +++
 src/autonomous/tool_registry.py                    |  273 ++
 src/data/__init__.py                               |    3 +
 src/data/embedding_pipeline.py                     |   68 +-
 src/data/multi_year_extractor.py                   |  204 ++
 src/data/multi_year_storage.py                     |  303 ++
 src/data/qdrant_client.py                          |    3 +-
 src/data/smart_router.py                           |   28 +-
 src/intelligence/__init__.py                       |    3 +
 src/intelligence/formatters/__init__.py            |    3 +
 src/intelligence/formatters/data_formatter.py      |  179 +
 src/intelligence/prompts/__init__.py               |    3 +
 .../prompts/industry_context_prompts.py            |  204 ++
 src/intelligence/prompts/local_llm_prompts.py      |  396 ++
 .../prompts/market_intelligence_prompts.py         |  269 ++
 .../prompts/strategic_evaluation_prompts.py        |  259 ++
 src/intelligence/prompts/synthesis_prompts.py      |  314 ++
 src/intelligence/services/__init__.py              |    3 +
 .../services/local_intelligence_service.py         |  592 +++
 .../services/multi_agent_intelligence_service.py   |  502 +++
 src/llm/__init__.py                                |   33 +
 src/llm/agent_prompts.py                           |  515 +++
 src/llm/local_client.py                            |  281 ++
 src/memory/cache_augmented_generation.py           |  541 +++
 src/memory/rag_cag_strategy.py                     |  368 ++
 src/parsing/document_parsers.py                    |  437 +++
 src/parsing/pdf_table_extractor.py                 |  287 ++
 src/rag/__init__.py                                |    4 +
 src/rag/document_loader.py                         |  326 ++
 src/rag/qdrant_vector_store.py                     |  322 ++
 src/rag/rag_service.py                             |  262 ++
 src/rag/simple_vector_store.py                     |  295 ++
 src/storage/case_manager.py                        |  463 +++
 test_2023_benchmark.py                             |  236 ++
 test_azoty_2023_extraction.py                      |  154 +
 test_simple_extraction_2023.py                     |  209 ++
 test_workflow_results.json                         |   22 +
 tests/integration/test_database_integration.py     |  585 +++
 611 files changed, 85542 insertions(+), 8 deletions(-)
```

## 🤖 Metadata

```json
{
  "commit_hash": "dc23cfe16826526e334f0a77d1e72f2784b5a503",
  "commit_type": "feature",
  "timestamp": 1762494866,
  "files_changed": [
    ".cache/prompts/architect_domain.json",
    ".cache/prompts/architect_system.json",
    ".cache/prompts/cba_analysis_2024_context.json",
    ".cache/prompts/cba_full_test_v2_context.json",
    ".cache/prompts/cba_test_integration_context.json",
    ".cache/prompts/data_science_domain.json",
    ".cache/prompts/data_science_system.json",
    ".cache/prompts/financial_domain.json",
    ".cache/prompts/financial_system.json",
    ".cache/prompts/legal_domain.json",
    ".cache/prompts/legal_system.json",
    ".cache/prompts/professional_analysis_20251105_143407_context.json",
    ".cache/prompts/professional_analysis_20251105_143445_context.json",
    ".cache/prompts/professional_analysis_20251105_143753_context.json",
    ".cache/prompts/professional_analysis_20251105_144305_context.json",
    ".cache/prompts/professional_analysis_20251105_144547_context.json",
    ".cache/prompts/profound_test_cba_reports_context.json",
    ".cache/prompts/risk_domain.json",
    ".cache/prompts/risk_system.json",
    ".cache/prompts/test_lmstudio_001_context.json",
    ".change_tracking_state.json",
    ".claude/commands/ai-project-evaluator.md",
    ".env",
    ".env.development",
    ".env.investigation",
    ".gitignore",
    "ANALIZA_JAKOSCI_PROFESSIONAL_ANALYZER.md",
    "ANALIZA_KRYTYCZNA_SYSTEMU_INVESTIGATIVE_QUALITY.md",
    "ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU.md",
    "ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU_PELNY.md",
    "AUTONOMOUS_SYSTEM_GUIDE.md",
    "BENCHMARK_COMPARISON_2023.md",
    "CBA_COMPREHENSIVE_ANALYSIS_2024.md",
    "CBA_FULL_CONTENT_ANALYSIS.md",
    "CBA_FULL_CONTENT_ANALYSIS_data.json",
    "CBA_PROFESSIONAL_ANALYSIS_FINAL_results.json",
    "CBA_PROFESSIONAL_ANALYSIS_REPORT_full_data.json",
    "COMPARISON_SUMMARY.md",
    "FINAL_ANALYSIS_LOCAL_SYSTEM.md",
    "FIXES_COMPLETE_SUCCESS.md",
    "FULL_HOG_FINAL_STATUS.md",
    "GRAF_RELACJI_STATUS.md",
    "HOW_I_WOULD_ANALYZE_CBA_REPORTS.md",
    "IMPLEMENTACJA_POPRAWEK.md",
    "IMPLEMENTATION_STATUS.md",
    "IMPLEMENTATION_STATUS_FINAL.md",
    "INTELLIGENCE_SYSTEM_ROADMAP.md",
    "INVESTIGATIVE_INTEGRATION_COMPLETE.md",
    "ISTNIEJACE_KONTENERY_ANALIZA.md",
    "LMSTUDIO_INTEGRATION_COMPLETE.md",
    "LOCAL_EXTRACTION_RESULTS_2023.json",
    "LOCAL_INTERPRETATION_LAYER.md",
    "MIGRACJA_VOLUMES.md",
    "MULTI_AGENT_ARCHITECTURE.md",
    "MULTI_AGENT_SYSTEM_COMPLETE.md",
    "MVP_AI_SPECIALIST_AGENT_DESIGN.md",
    "NEO4J_STATUS.md",
    "OCENA_JAKOSCI_ANALIZY.md",
    "ON_PREMISE_SYSTEM_READY.md",
    "PELNA_ANALIZA_PROJEKTU_WSZYSTKIE_KOMPONENTY.md",
    "PHASE1_COMPLETION_REPORT.md",
    "PIPELINE_ANALITYCZNY_PELNY_OPIS.md",
    "POROWNANIE_SYSTEM_VS_AI_ANALYSIS.md",
    "PRACTICAL_INTELLIGENCE_ROADMAP.md",
    "PRECYZYJNY_PODZIAL.md",
    "PROFOUND_TEST_CONCLUSIONS.md",
    "RAG_INTEGRATION_COMPLETE.md",
    "RAG_SYSTEM_SUMMARY.md",
    "README_RESULTS.md",
    "REAL_PARSING_COMPLETE.md",
    "RESULTS_QUICK_START.md",
    "RESULTS_STORAGE_ARCHITECTURE.md",
    "RESULTS_STORAGE_SEPARATION.md",
    "RESULTS_SUMMARY.md",
    "SEPARACJA_DANYCH_DEVELOPMENT.md",
    "SINGLE_VS_MULTI_AGENT_COMPARISON.md",
    "START_DEVELOPMENT.sh",
    "SUCCESS_SUMMARY.md",
    "TEST_INSTRUCTIONS.md",
    "THREE_WAY_COMPARISON_LOCAL_VS_CLAUDE.md",
    "WEEK2_DAY1_COMPLETION.md",
    "WERYFIKACJA_PODZIALU.md",
    "WNIOSKI_ARTUR.md",
    "WYSZUKIWANIE_STATUS.md",
    "analysis_rounds/round_1/README.md",
    "analysis_rounds/round_1/alex_document_processing.md",
    "analysis_rounds/round_1/marcus_financial_analysis.md",
    "analysis_rounds/round_1/workflow_alex_marcus.md",
    "analyze_cba_content.py",
    "analyze_cba_pdfs.py",
    "case_cli.py",
    "cba_content_analysis_log.txt",
    "cba_detection_results.txt",
    "cba_full_analysis_log.txt",
    "data/companies/grupa_azoty_sa.json",
    "destiny_auto.py",
    "docker-compose-dev.yml",
    "docs/architecture/RAG_CAG_STRATEGY.md",
    "docs/auto-generated/2025-11-05/COMMIT_d4adf31_feature.md",
    "docs/auto-generated/2025-11-05/COMMIT_f0d49b5_feature.md",
    "docs/auto-generated/2025-11-06/COMMIT_3d81426_feature.md",
    "docs/auto-generated/2025-11-06/COMMIT_457c53c_feature.md",
    "docs/auto-generated/2025-11-06/COMMIT_9c14593_feature.md",
    "docs/implementation/PLAN_IMPLEMENTACJI_POPRAWY_ANALIZY_CBA.md",
    "docs/implementation/POTWIERDZENIE_MODELI_EMBEDDINGOW.md",
    "docs/implementation/STRATEGIA_EMBEDDINGOW_JINA_VS_E5.md",
    "docs/status/MORNING_BRIEF_20251105.md",
    "docs/status/MORNING_BRIEF_20251106.md",
    "full_analysis_results_20251105_143433.json",
    "full_analysis_results_20251105_143824.json",
    "full_analysis_results_20251105_144346.json",
    "full_analysis_results_20251105_144624.json",
    "helena_tasks/helena_task_20251105_110000_agent_code.md",
    "helena_tasks/helena_task_20251105_110000_configuration.md",
    "helena_tasks/helena_task_20251105_110000_database_schema.md",
    "helena_tasks/helena_task_20251105_110000_documentation.md",
    "helena_tasks/helena_task_20251105_110000_general_change.md",
    "helena_tasks/helena_task_20251105_110000_knowledge_graph.md",
    "helena_tasks/helena_task_20251105_130000_general_change.md",
    "helena_tasks/helena_task_20251105_140000_general_change.md",
    "helena_tasks/helena_task_20251105_150000_documentation.md",
    "helena_tasks/helena_task_20251105_150000_general_change.md",
    "helena_tasks/helena_task_20251106_210000_documentation.md",
    "helena_tasks/helena_task_20251106_210000_general_change.md",
    "helena_tasks/processed/success_realtime_20251105_104923_COMMIT_f0d49b5_feature.json",
    "helena_tasks/processed/success_realtime_20251105_105739_AUTONOMOUS_SYSTEM_GUIDE.json",
    "helena_tasks/processed/success_realtime_20251105_110102_RAG_CAG_STRATEGY.json",
    "helena_tasks/processed/success_realtime_20251105_110237_WEEK2_DAY1_COMPLETION.json",
    "helena_tasks/processed/success_realtime_20251105_111232_LMSTUDIO_INTEGRATION_COMPLETE.json",
    "helena_tasks/processed/success_realtime_20251105_111355_FULL_HOG_FINAL_STATUS.json",
    "helena_tasks/processed/success_realtime_20251105_111541_README.json",
    "helena_tasks/processed/success_realtime_20251105_113504_REAL_PARSING_COMPLETE.json",
    "helena_tasks/processed/success_realtime_20251105_114107_WNIOSKI_ARTUR.json",
    "helena_tasks/processed/success_realtime_20251105_114855_FIXES_COMPLETE_SUCCESS.json",
    "helena_tasks/processed/success_realtime_20251105_114943_SUCCESS_SUMMARY.json",
    "helena_tasks/processed/success_realtime_20251105_115119_ANALIZA_CBA_2008-2024.json",
    "helena_tasks/processed/success_realtime_20251105_115422_README.json",
    "helena_tasks/processed/success_realtime_20251105_115928_WYSZUKIWANIE_STATUS.json",
    "helena_tasks/processed/success_realtime_20251105_120115_GRAF_RELACJI_STATUS.json",
    "helena_tasks/processed/success_realtime_20251105_120711_NEO4J_STATUS.json",
    "helena_tasks/processed/success_realtime_20251105_121013_ISTNIEJACE_KONTENERY_ANALIZA.json",
    "helena_tasks/processed/success_realtime_20251105_121125_SEPARACJA_DANYCH_DEVELOPMENT.json",
    "helena_tasks/processed/success_realtime_20251105_121305_PRECYZYJNY_PODZIAL.json",
    "helena_tasks/processed/success_realtime_20251105_121450_WERYFIKACJA_PODZIALU.json",
    "helena_tasks/processed/success_realtime_20251105_121736_MIGRACJA_VOLUMES.json",
    "helena_tasks/processed/success_realtime_20251105_131838_RESULTS_STORAGE_ARCHITECTURE.json",
    "helena_tasks/processed/success_realtime_20251105_132144_RESULTS_QUICK_START.json",
    "helena_tasks/processed/success_realtime_20251105_132326_RESULTS_STORAGE_SEPARATION.json",
    "helena_tasks/processed/success_realtime_20251105_132400_README_RESULTS.json",
    "helena_tasks/processed/success_realtime_20251105_132451_RESULTS_SUMMARY.json",
    "helena_tasks/processed/success_realtime_20251105_133123_cba_analiza_merytoryczna_2024.json",
    "helena_tasks/processed/success_realtime_20251105_133443_cba_weryfikacja_i_rekomendacje.json",
    "helena_tasks/processed/success_realtime_20251105_133637_PLAN_IMPLEMENTACJI_POPRAWY_ANALIZY_CBA.json",
    "helena_tasks/processed/success_realtime_20251105_133710_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.json",
    "helena_tasks/processed/success_realtime_20251105_133725_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.json",
    "helena_tasks/processed/success_realtime_20251105_133727_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.json",
    "helena_tasks/processed/success_realtime_20251105_133730_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.json",
    "helena_tasks/processed/success_realtime_20251105_133737_POTWIERDZENIE_MODELI_EMBEDDINGOW.json",
    "helena_tasks/processed/success_realtime_20251105_134418_STATUS_GOTOWOSCI_CBA.json",
    "helena_tasks/processed/success_realtime_20251105_134721_GOTOWOSC_SYSTEMU_CBA.json",
    "helena_tasks/processed/success_realtime_20251105_135015_EWALUACJA_SYSTEMU_CBA.json",
    "helena_tasks/processed/success_realtime_20251105_135041_EWALUACJA_SYSTEMU_CBA_SUMMARY.json",
    "helena_tasks/processed/success_realtime_20251105_140043_AUTONOMOUS_SYSTEM_GUIDE.json",
    "helena_tasks/processed/success_realtime_20251105_140054_AUTONOMOUS_SYSTEM_GUIDE.json",
    "helena_tasks/processed/success_realtime_20251105_140110_AUTONOMOUS_SYSTEM_GUIDE.json",
    "helena_tasks/processed/success_realtime_20251105_140140_AUTONOMOUS_SYSTEM_GUIDE.json",
    "helena_tasks/processed/success_realtime_20251105_140240_INVESTIGATIVE_INTEGRATION_COMPLETE.json",
    "helena_tasks/processed/success_realtime_20251105_140650_CBA_COMPREHENSIVE_ANALYSIS_2024.json",
    "helena_tasks/processed/success_realtime_20251105_141209_CBA_FULL_CONTENT_ANALYSIS.json",
    "helena_tasks/processed/success_realtime_20251105_141722_IMPLEMENTATION_STATUS_FINAL.json",
    "helena_tasks/processed/success_realtime_20251105_142247_HOW_I_WOULD_ANALYZE_CBA_REPORTS.json",
    "helena_tasks/processed/success_realtime_20251105_142507_CBA_PROFESSIONAL_ANALYSIS_REPORT.json",
    "helena_tasks/processed/success_realtime_20251105_142512_CBA_FULL_CONTENT_ANALYSIS.json",
    "helena_tasks/processed/success_realtime_20251105_142544_CBA_PROFESSIONAL_ANALYSIS_REPORT.json",
    "helena_tasks/processed/success_realtime_20251105_142726_HOW_TO_TEACH_SYSTEM_PROFESSIONAL_ANALYSIS.json",
    "helena_tasks/processed/success_realtime_20251105_142757_CBA_PROFESSIONAL_ANALYSIS_FINAL.json",
    "helena_tasks/processed/success_realtime_20251105_142935_COMMIT_d4adf31_feature.json",
    "helena_tasks/processed/success_realtime_20251105_143557_PIPELINE_ANALITYCZNY_PELNY_OPIS.json",
    "helena_tasks/processed/success_realtime_20251105_143844_ANALIZA_JAKOSCI_PROFESSIONAL_ANALYZER.json",
    "helena_tasks/processed/success_realtime_20251105_144019_POROWNANIE_SYSTEM_VS_AI_ANALYSIS.json",
    "helena_tasks/processed/success_realtime_20251105_144257_LOCAL_INTERPRETATION_LAYER.json",
    "helena_tasks/processed/success_realtime_20251105_144359_ON_PREMISE_SYSTEM_READY.json",
    "helena_tasks/processed/success_realtime_20251105_144657_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU.json",
    "helena_tasks/processed/success_realtime_20251105_144728_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU_PELNY.json",
    "helena_tasks/processed/success_realtime_20251105_144744_FINAL_ANALYSIS_LOCAL_SYSTEM.json",
    "helena_tasks/processed/success_realtime_20251105_144952_OCENA_JAKOSCI_ANALIZY.json",
    "helena_tasks/processed/success_realtime_20251105_145122_IMPLEMENTACJA_POPRAWEK.json",
    "helena_tasks/processed/success_realtime_20251106_153940_PHASE2_COMPLETION_REPORT.json",
    "helena_tasks/processed/success_realtime_20251106_170529_FINAL_EXTRACTION_REPORT.json",
    "helena_tasks/processed/success_realtime_20251106_172205_COMMIT_457c53c_feature.json",
    "helena_tasks/processed/success_realtime_20251106_173640_INTELLIGENT_EXTRACTION_COMPLETE.json",
    "helena_tasks/processed/success_realtime_20251106_173724_COMMIT_9c14593_feature.json",
    "helena_tasks/processed/success_realtime_20251106_210140_COMMIT_3d81426_feature.json",
    "helena_tasks/processed/success_realtime_20251106_211911_BENCHMARK_COMPARISON_2023.json",
    "helena_tasks/processed/success_realtime_20251106_211927_BENCHMARK_COMPARISON_2023.json",
    "helena_tasks/processed/success_realtime_20251106_212247_BENCHMARK_COMPARISON_2023.json",
    "helena_tasks/processed/success_realtime_20251106_212256_BENCHMARK_COMPARISON_2023.json",
    "helena_tasks/processed/success_realtime_20251106_214207_Azoty_Intelligence_Local_20251106_214207.json",
    "helena_tasks/processed/success_realtime_20251106_220127_RAG_SYSTEM_SUMMARY.json",
    "helena_tasks/processed/success_realtime_20251106_220301_Azoty_Baseline_NoRAG.json",
    "helena_tasks/processed/success_realtime_20251106_220341_Azoty_RAG_Enhanced.json",
    "helena_tasks/processed/success_realtime_20251106_220529_Azoty_RAG_Enhanced.json",
    "helena_tasks/processed/success_realtime_20251106_222059_Azoty_MultiAgent_20251106_222059.json",
    "migrate_existing_results.py",
    "output/intelligence_reports/Azoty_Baseline_NoRAG.md",
    "output/intelligence_reports/Azoty_Claude_Analysis_20251106.md",
    "output/intelligence_reports/Azoty_Intelligence_Local_20251106_214207.md",
    "output/intelligence_reports/Azoty_MultiAgent_20251106_222059.md",
    "output/intelligence_reports/Azoty_RAG_Enhanced.md",
    "profound_test.py",
    "qdrant_pending/indexed/doc_20251105_104923_COMMIT_f0d49b5_feature.json",
    "qdrant_pending/indexed/doc_20251105_105739_AUTONOMOUS_SYSTEM_GUIDE.json",
    "qdrant_pending/indexed/doc_20251105_110102_RAG_CAG_STRATEGY.json",
    "qdrant_pending/indexed/doc_20251105_110237_WEEK2_DAY1_COMPLETION.json",
    "qdrant_pending/indexed/doc_20251105_111232_LMSTUDIO_INTEGRATION_COMPLETE.json",
    "qdrant_pending/indexed/doc_20251105_111355_FULL_HOG_FINAL_STATUS.json",
    "qdrant_pending/indexed/doc_20251105_111541_README.json",
    "qdrant_pending/indexed/doc_20251105_113504_REAL_PARSING_COMPLETE.json",
    "qdrant_pending/indexed/doc_20251105_114107_WNIOSKI_ARTUR.json",
    "qdrant_pending/indexed/doc_20251105_114856_FIXES_COMPLETE_SUCCESS.json",
    "qdrant_pending/indexed/doc_20251105_114944_SUCCESS_SUMMARY.json",
    "qdrant_pending/indexed/doc_20251105_115119_ANALIZA_CBA_2008-2024.json",
    "qdrant_pending/indexed/doc_20251105_115423_README.json",
    "qdrant_pending/indexed/doc_20251105_115929_WYSZUKIWANIE_STATUS.json",
    "qdrant_pending/indexed/doc_20251105_120115_GRAF_RELACJI_STATUS.json",
    "qdrant_pending/indexed/doc_20251105_120711_NEO4J_STATUS.json",
    "qdrant_pending/indexed/doc_20251105_121014_ISTNIEJACE_KONTENERY_ANALIZA.json",
    "qdrant_pending/indexed/doc_20251105_121125_SEPARACJA_DANYCH_DEVELOPMENT.json",
    "qdrant_pending/indexed/doc_20251105_121306_PRECYZYJNY_PODZIAL.json",
    "qdrant_pending/indexed/doc_20251105_121451_WERYFIKACJA_PODZIALU.json",
    "qdrant_pending/indexed/doc_20251105_121737_MIGRACJA_VOLUMES.json",
    "qdrant_pending/indexed/doc_20251105_131839_RESULTS_STORAGE_ARCHITECTURE.json",
    "qdrant_pending/indexed/doc_20251105_132145_RESULTS_QUICK_START.json",
    "qdrant_pending/indexed/doc_20251105_132326_RESULTS_STORAGE_SEPARATION.json",
    "qdrant_pending/indexed/doc_20251105_132400_README_RESULTS.json",
    "qdrant_pending/indexed/doc_20251105_132452_RESULTS_SUMMARY.json",
    "qdrant_pending/indexed/doc_20251105_133124_cba_analiza_merytoryczna_2024.json",
    "qdrant_pending/indexed/doc_20251105_133444_cba_weryfikacja_i_rekomendacje.json",
    "qdrant_pending/indexed/doc_20251105_133637_PLAN_IMPLEMENTACJI_POPRAWY_ANALIZY_CBA.json",
    "qdrant_pending/indexed/doc_20251105_133711_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.json",
    "qdrant_pending/indexed/doc_20251105_133725_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.json",
    "qdrant_pending/indexed/doc_20251105_133728_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.json",
    "qdrant_pending/indexed/doc_20251105_133731_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.json",
    "qdrant_pending/indexed/doc_20251105_133737_POTWIERDZENIE_MODELI_EMBEDDINGOW.json",
    "qdrant_pending/indexed/doc_20251105_134418_STATUS_GOTOWOSCI_CBA.json",
    "qdrant_pending/indexed/doc_20251105_134722_GOTOWOSC_SYSTEMU_CBA.json",
    "qdrant_pending/indexed/doc_20251105_135015_EWALUACJA_SYSTEMU_CBA.json",
    "qdrant_pending/indexed/doc_20251105_135041_EWALUACJA_SYSTEMU_CBA_SUMMARY.json",
    "qdrant_pending/indexed/doc_20251105_140043_AUTONOMOUS_SYSTEM_GUIDE.json",
    "qdrant_pending/indexed/doc_20251105_140055_AUTONOMOUS_SYSTEM_GUIDE.json",
    "qdrant_pending/indexed/doc_20251105_140110_AUTONOMOUS_SYSTEM_GUIDE.json",
    "qdrant_pending/indexed/doc_20251105_140140_AUTONOMOUS_SYSTEM_GUIDE.json",
    "qdrant_pending/indexed/doc_20251105_140241_INVESTIGATIVE_INTEGRATION_COMPLETE.json",
    "qdrant_pending/indexed/doc_20251105_140651_CBA_COMPREHENSIVE_ANALYSIS_2024.json",
    "qdrant_pending/indexed/doc_20251105_141210_CBA_FULL_CONTENT_ANALYSIS.json",
    "qdrant_pending/indexed/doc_20251105_141722_IMPLEMENTATION_STATUS_FINAL.json",
    "qdrant_pending/indexed/doc_20251105_142248_HOW_I_WOULD_ANALYZE_CBA_REPORTS.json",
    "qdrant_pending/indexed/doc_20251105_142507_CBA_PROFESSIONAL_ANALYSIS_REPORT.json",
    "qdrant_pending/indexed/doc_20251105_142513_CBA_FULL_CONTENT_ANALYSIS.json",
    "qdrant_pending/indexed/doc_20251105_142545_CBA_PROFESSIONAL_ANALYSIS_REPORT.json",
    "qdrant_pending/indexed/doc_20251105_142726_HOW_TO_TEACH_SYSTEM_PROFESSIONAL_ANALYSIS.json",
    "qdrant_pending/indexed/doc_20251105_142758_CBA_PROFESSIONAL_ANALYSIS_FINAL.json",
    "qdrant_pending/indexed/doc_20251105_142935_COMMIT_d4adf31_feature.json",
    "qdrant_pending/indexed/doc_20251105_143558_PIPELINE_ANALITYCZNY_PELNY_OPIS.json",
    "qdrant_pending/indexed/doc_20251105_143845_ANALIZA_JAKOSCI_PROFESSIONAL_ANALYZER.json",
    "qdrant_pending/indexed/doc_20251105_144020_POROWNANIE_SYSTEM_VS_AI_ANALYSIS.json",
    "qdrant_pending/indexed/doc_20251105_144257_LOCAL_INTERPRETATION_LAYER.json",
    "qdrant_pending/indexed/doc_20251105_144359_ON_PREMISE_SYSTEM_READY.json",
    "qdrant_pending/indexed/doc_20251105_144658_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU.json",
    "qdrant_pending/indexed/doc_20251105_144728_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU_PELNY.json",
    "qdrant_pending/indexed/doc_20251105_144745_FINAL_ANALYSIS_LOCAL_SYSTEM.json",
    "qdrant_pending/indexed/doc_20251105_144952_OCENA_JAKOSCI_ANALIZY.json",
    "qdrant_pending/indexed/doc_20251105_145122_IMPLEMENTACJA_POPRAWEK.json",
    "qdrant_pending/indexed/doc_20251106_153941_PHASE2_COMPLETION_REPORT.json",
    "qdrant_pending/indexed/doc_20251106_170530_FINAL_EXTRACTION_REPORT.json",
    "qdrant_pending/indexed/doc_20251106_172206_COMMIT_457c53c_feature.json",
    "qdrant_pending/indexed/doc_20251106_173640_INTELLIGENT_EXTRACTION_COMPLETE.json",
    "qdrant_pending/indexed/doc_20251106_173724_COMMIT_9c14593_feature.json",
    "qdrant_pending/indexed/doc_20251106_210141_COMMIT_3d81426_feature.json",
    "qdrant_pending/indexed/doc_20251106_211912_BENCHMARK_COMPARISON_2023.json",
    "qdrant_pending/indexed/doc_20251106_211928_BENCHMARK_COMPARISON_2023.json",
    "qdrant_pending/indexed/doc_20251106_212248_BENCHMARK_COMPARISON_2023.json",
    "qdrant_pending/indexed/doc_20251106_212256_BENCHMARK_COMPARISON_2023.json",
    "qdrant_pending/indexed/doc_20251106_214208_Azoty_Intelligence_Local_20251106_214207.json",
    "qdrant_pending/indexed/doc_20251106_220128_RAG_SYSTEM_SUMMARY.json",
    "qdrant_pending/indexed/doc_20251106_220302_Azoty_Baseline_NoRAG.json",
    "qdrant_pending/indexed/doc_20251106_220342_Azoty_RAG_Enhanced.json",
    "qdrant_pending/indexed/doc_20251106_220529_Azoty_RAG_Enhanced.json",
    "qdrant_pending/indexed/doc_20251106_222100_Azoty_MultiAgent_20251106_222059.json",
    "quality_report_20251105_143433.json",
    "quality_report_20251105_143824.json",
    "quality_report_20251105_144346.json",
    "quality_report_20251105_144624.json",
    "redis_pending/redis_20251105_104923_COMMIT_f0d49b5_feature.txt",
    "redis_pending/redis_20251105_105739_AUTONOMOUS_SYSTEM_GUIDE.txt",
    "redis_pending/redis_20251105_110103_RAG_CAG_STRATEGY.txt",
    "redis_pending/redis_20251105_110237_WEEK2_DAY1_COMPLETION.txt",
    "redis_pending/redis_20251105_111232_LMSTUDIO_INTEGRATION_COMPLETE.txt",
    "redis_pending/redis_20251105_111355_FULL_HOG_FINAL_STATUS.txt",
    "redis_pending/redis_20251105_111541_README.txt",
    "redis_pending/redis_20251105_113504_REAL_PARSING_COMPLETE.txt",
    "redis_pending/redis_20251105_114107_WNIOSKI_ARTUR.txt",
    "redis_pending/redis_20251105_114856_FIXES_COMPLETE_SUCCESS.txt",
    "redis_pending/redis_20251105_114944_SUCCESS_SUMMARY.txt",
    "redis_pending/redis_20251105_115119_ANALIZA_CBA_2008-2024.txt",
    "redis_pending/redis_20251105_115423_README.txt",
    "redis_pending/redis_20251105_115929_WYSZUKIWANIE_STATUS.txt",
    "redis_pending/redis_20251105_120115_GRAF_RELACJI_STATUS.txt",
    "redis_pending/redis_20251105_120711_NEO4J_STATUS.txt",
    "redis_pending/redis_20251105_121014_ISTNIEJACE_KONTENERY_ANALIZA.txt",
    "redis_pending/redis_20251105_121125_SEPARACJA_DANYCH_DEVELOPMENT.txt",
    "redis_pending/redis_20251105_121306_PRECYZYJNY_PODZIAL.txt",
    "redis_pending/redis_20251105_121451_WERYFIKACJA_PODZIALU.txt",
    "redis_pending/redis_20251105_121737_MIGRACJA_VOLUMES.txt",
    "redis_pending/redis_20251105_131839_RESULTS_STORAGE_ARCHITECTURE.txt",
    "redis_pending/redis_20251105_132145_RESULTS_QUICK_START.txt",
    "redis_pending/redis_20251105_132326_RESULTS_STORAGE_SEPARATION.txt",
    "redis_pending/redis_20251105_132400_README_RESULTS.txt",
    "redis_pending/redis_20251105_132452_RESULTS_SUMMARY.txt",
    "redis_pending/redis_20251105_133124_cba_analiza_merytoryczna_2024.txt",
    "redis_pending/redis_20251105_133444_cba_weryfikacja_i_rekomendacje.txt",
    "redis_pending/redis_20251105_133637_PLAN_IMPLEMENTACJI_POPRAWY_ANALIZY_CBA.txt",
    "redis_pending/redis_20251105_133711_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.txt",
    "redis_pending/redis_20251105_133725_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.txt",
    "redis_pending/redis_20251105_133728_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.txt",
    "redis_pending/redis_20251105_133731_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.txt",
    "redis_pending/redis_20251105_133737_POTWIERDZENIE_MODELI_EMBEDDINGOW.txt",
    "redis_pending/redis_20251105_134418_STATUS_GOTOWOSCI_CBA.txt",
    "redis_pending/redis_20251105_134722_GOTOWOSC_SYSTEMU_CBA.txt",
    "redis_pending/redis_20251105_135015_EWALUACJA_SYSTEMU_CBA.txt",
    "redis_pending/redis_20251105_135041_EWALUACJA_SYSTEMU_CBA_SUMMARY.txt",
    "redis_pending/redis_20251105_140043_AUTONOMOUS_SYSTEM_GUIDE.txt",
    "redis_pending/redis_20251105_140055_AUTONOMOUS_SYSTEM_GUIDE.txt",
    "redis_pending/redis_20251105_140110_AUTONOMOUS_SYSTEM_GUIDE.txt",
    "redis_pending/redis_20251105_140140_AUTONOMOUS_SYSTEM_GUIDE.txt",
    "redis_pending/redis_20251105_140241_INVESTIGATIVE_INTEGRATION_COMPLETE.txt",
    "redis_pending/redis_20251105_140651_CBA_COMPREHENSIVE_ANALYSIS_2024.txt",
    "redis_pending/redis_20251105_141210_CBA_FULL_CONTENT_ANALYSIS.txt",
    "redis_pending/redis_20251105_141722_IMPLEMENTATION_STATUS_FINAL.txt",
    "redis_pending/redis_20251105_142248_HOW_I_WOULD_ANALYZE_CBA_REPORTS.txt",
    "redis_pending/redis_20251105_142507_CBA_PROFESSIONAL_ANALYSIS_REPORT.txt",
    "redis_pending/redis_20251105_142513_CBA_FULL_CONTENT_ANALYSIS.txt",
    "redis_pending/redis_20251105_142545_CBA_PROFESSIONAL_ANALYSIS_REPORT.txt",
    "redis_pending/redis_20251105_142726_HOW_TO_TEACH_SYSTEM_PROFESSIONAL_ANALYSIS.txt",
    "redis_pending/redis_20251105_142758_CBA_PROFESSIONAL_ANALYSIS_FINAL.txt",
    "redis_pending/redis_20251105_142935_COMMIT_d4adf31_feature.txt",
    "redis_pending/redis_20251105_143558_PIPELINE_ANALITYCZNY_PELNY_OPIS.txt",
    "redis_pending/redis_20251105_143845_ANALIZA_JAKOSCI_PROFESSIONAL_ANALYZER.txt",
    "redis_pending/redis_20251105_144020_POROWNANIE_SYSTEM_VS_AI_ANALYSIS.txt",
    "redis_pending/redis_20251105_144258_LOCAL_INTERPRETATION_LAYER.txt",
    "redis_pending/redis_20251105_144359_ON_PREMISE_SYSTEM_READY.txt",
    "redis_pending/redis_20251105_144658_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU.txt",
    "redis_pending/redis_20251105_144728_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU_PELNY.txt",
    "redis_pending/redis_20251105_144745_FINAL_ANALYSIS_LOCAL_SYSTEM.txt",
    "redis_pending/redis_20251105_144952_OCENA_JAKOSCI_ANALIZY.txt",
    "redis_pending/redis_20251105_145122_IMPLEMENTACJA_POPRAWEK.txt",
    "redis_pending/redis_20251106_153941_PHASE2_COMPLETION_REPORT.txt",
    "redis_pending/redis_20251106_170530_FINAL_EXTRACTION_REPORT.txt",
    "redis_pending/redis_20251106_172206_COMMIT_457c53c_feature.txt",
    "redis_pending/redis_20251106_173641_INTELLIGENT_EXTRACTION_COMPLETE.txt",
    "redis_pending/redis_20251106_173724_COMMIT_9c14593_feature.txt",
    "redis_pending/redis_20251106_210141_COMMIT_3d81426_feature.txt",
    "redis_pending/redis_20251106_211912_BENCHMARK_COMPARISON_2023.txt",
    "redis_pending/redis_20251106_211928_BENCHMARK_COMPARISON_2023.txt",
    "redis_pending/redis_20251106_212248_BENCHMARK_COMPARISON_2023.txt",
    "redis_pending/redis_20251106_212256_BENCHMARK_COMPARISON_2023.txt",
    "redis_pending/redis_20251106_214208_Azoty_Intelligence_Local_20251106_214207.txt",
    "redis_pending/redis_20251106_220128_RAG_SYSTEM_SUMMARY.txt",
    "redis_pending/redis_20251106_220302_Azoty_Baseline_NoRAG.txt",
    "redis_pending/redis_20251106_220342_Azoty_RAG_Enhanced.txt",
    "redis_pending/redis_20251106_220530_Azoty_RAG_Enhanced.txt",
    "redis_pending/redis_20251106_222100_Azoty_MultiAgent_20251106_222059.txt",
    "reports/EWALUACJA_SYSTEMU_CBA.md",
    "reports/EWALUACJA_SYSTEMU_CBA_SUMMARY.md",
    "reports/GOTOWOSC_SYSTEMU_CBA.md",
    "reports/IMPLEMENTACJA_I_TESTY_RAPORT.md",
    "reports/STATUS_GOTOWOSCI_CBA.md",
    "reports/autonomous_cba_analysis_2024.json",
    "reports/autonomous_cba_full_test_v2.json",
    "reports/autonomous_cba_test_integration.json",
    "reports/autonomous_professional_analysis_20251105_143407.json",
    "reports/autonomous_professional_analysis_20251105_143445.json",
    "reports/autonomous_professional_analysis_20251105_143753.json",
    "reports/autonomous_professional_analysis_20251105_144305.json",
    "reports/autonomous_professional_analysis_20251105_144547.json",
    "reports/autonomous_profound_test_cba_reports.json",
    "reports/autonomous_real_parsing_test.json",
    "reports/autonomous_test_lmstudio_001.json",
    "reports/cba_analiza_merytoryczna_2024.html",
    "reports/cba_analiza_merytoryczna_2024.md",
    "reports/cba_analysis_2024.html",
    "reports/cba_extraction_results.json",
    "reports/cba_real_data_extracted.json",
    "reports/cba_verification_extraction.json",
    "reports/cba_weryfikacja_i_rekomendacje.md",
    "scripts/generate_claude_analysis.py",
    "scripts/ingest_azoty_to_rag.py",
    "scripts/init_all_databases.sh",
    "scripts/init_postgres.sh",
    "scripts/reingest_with_sections.py",
    "scripts/save_azoty_data.py",
    "scripts/test_intelligence_azoty.py",
    "scripts/test_multi_agent_azoty.py",
    "scripts/test_rag_enhanced_report.py",
    "scripts/test_rag_queries.py",
    "sql/realtime_updates/neo4j_20251105_104923_COMMIT_f0d49b5_feature.cypher",
    "sql/realtime_updates/neo4j_20251105_105739_AUTONOMOUS_SYSTEM_GUIDE.cypher",
    "sql/realtime_updates/neo4j_20251105_110102_RAG_CAG_STRATEGY.cypher",
    "sql/realtime_updates/neo4j_20251105_110237_WEEK2_DAY1_COMPLETION.cypher",
    "sql/realtime_updates/neo4j_20251105_111232_LMSTUDIO_INTEGRATION_COMPLETE.cypher",
    "sql/realtime_updates/neo4j_20251105_111355_FULL_HOG_FINAL_STATUS.cypher",
    "sql/realtime_updates/neo4j_20251105_111541_README.cypher",
    "sql/realtime_updates/neo4j_20251105_113504_REAL_PARSING_COMPLETE.cypher",
    "sql/realtime_updates/neo4j_20251105_114107_WNIOSKI_ARTUR.cypher",
    "sql/realtime_updates/neo4j_20251105_114856_FIXES_COMPLETE_SUCCESS.cypher",
    "sql/realtime_updates/neo4j_20251105_114944_SUCCESS_SUMMARY.cypher",
    "sql/realtime_updates/neo4j_20251105_115119_ANALIZA_CBA_2008-2024.cypher",
    "sql/realtime_updates/neo4j_20251105_115423_README.cypher",
    "sql/realtime_updates/neo4j_20251105_115929_WYSZUKIWANIE_STATUS.cypher",
    "sql/realtime_updates/neo4j_20251105_120115_GRAF_RELACJI_STATUS.cypher",
    "sql/realtime_updates/neo4j_20251105_120711_NEO4J_STATUS.cypher",
    "sql/realtime_updates/neo4j_20251105_121014_ISTNIEJACE_KONTENERY_ANALIZA.cypher",
    "sql/realtime_updates/neo4j_20251105_121125_SEPARACJA_DANYCH_DEVELOPMENT.cypher",
    "sql/realtime_updates/neo4j_20251105_121306_PRECYZYJNY_PODZIAL.cypher",
    "sql/realtime_updates/neo4j_20251105_121451_WERYFIKACJA_PODZIALU.cypher",
    "sql/realtime_updates/neo4j_20251105_121737_MIGRACJA_VOLUMES.cypher",
    "sql/realtime_updates/neo4j_20251105_131839_RESULTS_STORAGE_ARCHITECTURE.cypher",
    "sql/realtime_updates/neo4j_20251105_132145_RESULTS_QUICK_START.cypher",
    "sql/realtime_updates/neo4j_20251105_132326_RESULTS_STORAGE_SEPARATION.cypher",
    "sql/realtime_updates/neo4j_20251105_132400_README_RESULTS.cypher",
    "sql/realtime_updates/neo4j_20251105_132452_RESULTS_SUMMARY.cypher",
    "sql/realtime_updates/neo4j_20251105_133124_cba_analiza_merytoryczna_2024.cypher",
    "sql/realtime_updates/neo4j_20251105_133444_cba_weryfikacja_i_rekomendacje.cypher",
    "sql/realtime_updates/neo4j_20251105_133637_PLAN_IMPLEMENTACJI_POPRAWY_ANALIZY_CBA.cypher",
    "sql/realtime_updates/neo4j_20251105_133711_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.cypher",
    "sql/realtime_updates/neo4j_20251105_133725_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.cypher",
    "sql/realtime_updates/neo4j_20251105_133728_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.cypher",
    "sql/realtime_updates/neo4j_20251105_133731_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.cypher",
    "sql/realtime_updates/neo4j_20251105_133737_POTWIERDZENIE_MODELI_EMBEDDINGOW.cypher",
    "sql/realtime_updates/neo4j_20251105_134418_STATUS_GOTOWOSCI_CBA.cypher",
    "sql/realtime_updates/neo4j_20251105_134722_GOTOWOSC_SYSTEMU_CBA.cypher",
    "sql/realtime_updates/neo4j_20251105_135015_EWALUACJA_SYSTEMU_CBA.cypher",
    "sql/realtime_updates/neo4j_20251105_135041_EWALUACJA_SYSTEMU_CBA_SUMMARY.cypher",
    "sql/realtime_updates/neo4j_20251105_140043_AUTONOMOUS_SYSTEM_GUIDE.cypher",
    "sql/realtime_updates/neo4j_20251105_140055_AUTONOMOUS_SYSTEM_GUIDE.cypher",
    "sql/realtime_updates/neo4j_20251105_140110_AUTONOMOUS_SYSTEM_GUIDE.cypher",
    "sql/realtime_updates/neo4j_20251105_140140_AUTONOMOUS_SYSTEM_GUIDE.cypher",
    "sql/realtime_updates/neo4j_20251105_140241_INVESTIGATIVE_INTEGRATION_COMPLETE.cypher",
    "sql/realtime_updates/neo4j_20251105_140651_CBA_COMPREHENSIVE_ANALYSIS_2024.cypher",
    "sql/realtime_updates/neo4j_20251105_141210_CBA_FULL_CONTENT_ANALYSIS.cypher",
    "sql/realtime_updates/neo4j_20251105_141722_IMPLEMENTATION_STATUS_FINAL.cypher",
    "sql/realtime_updates/neo4j_20251105_142248_HOW_I_WOULD_ANALYZE_CBA_REPORTS.cypher",
    "sql/realtime_updates/neo4j_20251105_142507_CBA_PROFESSIONAL_ANALYSIS_REPORT.cypher",
    "sql/realtime_updates/neo4j_20251105_142513_CBA_FULL_CONTENT_ANALYSIS.cypher",
    "sql/realtime_updates/neo4j_20251105_142545_CBA_PROFESSIONAL_ANALYSIS_REPORT.cypher",
    "sql/realtime_updates/neo4j_20251105_142726_HOW_TO_TEACH_SYSTEM_PROFESSIONAL_ANALYSIS.cypher",
    "sql/realtime_updates/neo4j_20251105_142758_CBA_PROFESSIONAL_ANALYSIS_FINAL.cypher",
    "sql/realtime_updates/neo4j_20251105_142935_COMMIT_d4adf31_feature.cypher",
    "sql/realtime_updates/neo4j_20251105_143558_PIPELINE_ANALITYCZNY_PELNY_OPIS.cypher",
    "sql/realtime_updates/neo4j_20251105_143845_ANALIZA_JAKOSCI_PROFESSIONAL_ANALYZER.cypher",
    "sql/realtime_updates/neo4j_20251105_144020_POROWNANIE_SYSTEM_VS_AI_ANALYSIS.cypher",
    "sql/realtime_updates/neo4j_20251105_144257_LOCAL_INTERPRETATION_LAYER.cypher",
    "sql/realtime_updates/neo4j_20251105_144359_ON_PREMISE_SYSTEM_READY.cypher",
    "sql/realtime_updates/neo4j_20251105_144658_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU.cypher",
    "sql/realtime_updates/neo4j_20251105_144728_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU_PELNY.cypher",
    "sql/realtime_updates/neo4j_20251105_144745_FINAL_ANALYSIS_LOCAL_SYSTEM.cypher",
    "sql/realtime_updates/neo4j_20251105_144952_OCENA_JAKOSCI_ANALIZY.cypher",
    "sql/realtime_updates/neo4j_20251105_145122_IMPLEMENTACJA_POPRAWEK.cypher",
    "sql/realtime_updates/neo4j_20251106_153941_PHASE2_COMPLETION_REPORT.cypher",
    "sql/realtime_updates/neo4j_20251106_170530_FINAL_EXTRACTION_REPORT.cypher",
    "sql/realtime_updates/neo4j_20251106_172206_COMMIT_457c53c_feature.cypher",
    "sql/realtime_updates/neo4j_20251106_173640_INTELLIGENT_EXTRACTION_COMPLETE.cypher",
    "sql/realtime_updates/neo4j_20251106_173724_COMMIT_9c14593_feature.cypher",
    "sql/realtime_updates/neo4j_20251106_210141_COMMIT_3d81426_feature.cypher",
    "sql/realtime_updates/neo4j_20251106_211912_BENCHMARK_COMPARISON_2023.cypher",
    "sql/realtime_updates/neo4j_20251106_211928_BENCHMARK_COMPARISON_2023.cypher",
    "sql/realtime_updates/neo4j_20251106_212248_BENCHMARK_COMPARISON_2023.cypher",
    "sql/realtime_updates/neo4j_20251106_212256_BENCHMARK_COMPARISON_2023.cypher",
    "sql/realtime_updates/neo4j_20251106_214208_Azoty_Intelligence_Local_20251106_214207.cypher",
    "sql/realtime_updates/neo4j_20251106_220128_RAG_SYSTEM_SUMMARY.cypher",
    "sql/realtime_updates/neo4j_20251106_220302_Azoty_Baseline_NoRAG.cypher",
    "sql/realtime_updates/neo4j_20251106_220342_Azoty_RAG_Enhanced.cypher",
    "sql/realtime_updates/neo4j_20251106_220529_Azoty_RAG_Enhanced.cypher",
    "sql/realtime_updates/neo4j_20251106_222100_Azoty_MultiAgent_20251106_222059.cypher",
    "sql/realtime_updates/pg_20251105_104923_COMMIT_f0d49b5_feature.sql",
    "sql/realtime_updates/pg_20251105_105739_AUTONOMOUS_SYSTEM_GUIDE.sql",
    "sql/realtime_updates/pg_20251105_110102_RAG_CAG_STRATEGY.sql",
    "sql/realtime_updates/pg_20251105_110237_WEEK2_DAY1_COMPLETION.sql",
    "sql/realtime_updates/pg_20251105_111232_LMSTUDIO_INTEGRATION_COMPLETE.sql",
    "sql/realtime_updates/pg_20251105_111355_FULL_HOG_FINAL_STATUS.sql",
    "sql/realtime_updates/pg_20251105_111541_README.sql",
    "sql/realtime_updates/pg_20251105_113504_REAL_PARSING_COMPLETE.sql",
    "sql/realtime_updates/pg_20251105_114107_WNIOSKI_ARTUR.sql",
    "sql/realtime_updates/pg_20251105_114856_FIXES_COMPLETE_SUCCESS.sql",
    "sql/realtime_updates/pg_20251105_114944_SUCCESS_SUMMARY.sql",
    "sql/realtime_updates/pg_20251105_115119_ANALIZA_CBA_2008-2024.sql",
    "sql/realtime_updates/pg_20251105_115423_README.sql",
    "sql/realtime_updates/pg_20251105_115929_WYSZUKIWANIE_STATUS.sql",
    "sql/realtime_updates/pg_20251105_120115_GRAF_RELACJI_STATUS.sql",
    "sql/realtime_updates/pg_20251105_120711_NEO4J_STATUS.sql",
    "sql/realtime_updates/pg_20251105_121014_ISTNIEJACE_KONTENERY_ANALIZA.sql",
    "sql/realtime_updates/pg_20251105_121125_SEPARACJA_DANYCH_DEVELOPMENT.sql",
    "sql/realtime_updates/pg_20251105_121306_PRECYZYJNY_PODZIAL.sql",
    "sql/realtime_updates/pg_20251105_121451_WERYFIKACJA_PODZIALU.sql",
    "sql/realtime_updates/pg_20251105_121737_MIGRACJA_VOLUMES.sql",
    "sql/realtime_updates/pg_20251105_131839_RESULTS_STORAGE_ARCHITECTURE.sql",
    "sql/realtime_updates/pg_20251105_132145_RESULTS_QUICK_START.sql",
    "sql/realtime_updates/pg_20251105_132326_RESULTS_STORAGE_SEPARATION.sql",
    "sql/realtime_updates/pg_20251105_132400_README_RESULTS.sql",
    "sql/realtime_updates/pg_20251105_132452_RESULTS_SUMMARY.sql",
    "sql/realtime_updates/pg_20251105_133124_cba_analiza_merytoryczna_2024.sql",
    "sql/realtime_updates/pg_20251105_133444_cba_weryfikacja_i_rekomendacje.sql",
    "sql/realtime_updates/pg_20251105_133637_PLAN_IMPLEMENTACJI_POPRAWY_ANALIZY_CBA.sql",
    "sql/realtime_updates/pg_20251105_133711_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.sql",
    "sql/realtime_updates/pg_20251105_133725_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.sql",
    "sql/realtime_updates/pg_20251105_133728_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.sql",
    "sql/realtime_updates/pg_20251105_133730_STRATEGIA_EMBEDDINGOW_JINA_VS_E5.sql",
    "sql/realtime_updates/pg_20251105_133737_POTWIERDZENIE_MODELI_EMBEDDINGOW.sql",
    "sql/realtime_updates/pg_20251105_134418_STATUS_GOTOWOSCI_CBA.sql",
    "sql/realtime_updates/pg_20251105_134722_GOTOWOSC_SYSTEMU_CBA.sql",
    "sql/realtime_updates/pg_20251105_135015_EWALUACJA_SYSTEMU_CBA.sql",
    "sql/realtime_updates/pg_20251105_135041_EWALUACJA_SYSTEMU_CBA_SUMMARY.sql",
    "sql/realtime_updates/pg_20251105_140043_AUTONOMOUS_SYSTEM_GUIDE.sql",
    "sql/realtime_updates/pg_20251105_140055_AUTONOMOUS_SYSTEM_GUIDE.sql",
    "sql/realtime_updates/pg_20251105_140110_AUTONOMOUS_SYSTEM_GUIDE.sql",
    "sql/realtime_updates/pg_20251105_140140_AUTONOMOUS_SYSTEM_GUIDE.sql",
    "sql/realtime_updates/pg_20251105_140241_INVESTIGATIVE_INTEGRATION_COMPLETE.sql",
    "sql/realtime_updates/pg_20251105_140651_CBA_COMPREHENSIVE_ANALYSIS_2024.sql",
    "sql/realtime_updates/pg_20251105_141210_CBA_FULL_CONTENT_ANALYSIS.sql",
    "sql/realtime_updates/pg_20251105_141722_IMPLEMENTATION_STATUS_FINAL.sql",
    "sql/realtime_updates/pg_20251105_142248_HOW_I_WOULD_ANALYZE_CBA_REPORTS.sql",
    "sql/realtime_updates/pg_20251105_142507_CBA_PROFESSIONAL_ANALYSIS_REPORT.sql",
    "sql/realtime_updates/pg_20251105_142513_CBA_FULL_CONTENT_ANALYSIS.sql",
    "sql/realtime_updates/pg_20251105_142545_CBA_PROFESSIONAL_ANALYSIS_REPORT.sql",
    "sql/realtime_updates/pg_20251105_142726_HOW_TO_TEACH_SYSTEM_PROFESSIONAL_ANALYSIS.sql",
    "sql/realtime_updates/pg_20251105_142758_CBA_PROFESSIONAL_ANALYSIS_FINAL.sql",
    "sql/realtime_updates/pg_20251105_142935_COMMIT_d4adf31_feature.sql",
    "sql/realtime_updates/pg_20251105_143558_PIPELINE_ANALITYCZNY_PELNY_OPIS.sql",
    "sql/realtime_updates/pg_20251105_143845_ANALIZA_JAKOSCI_PROFESSIONAL_ANALYZER.sql",
    "sql/realtime_updates/pg_20251105_144020_POROWNANIE_SYSTEM_VS_AI_ANALYSIS.sql",
    "sql/realtime_updates/pg_20251105_144257_LOCAL_INTERPRETATION_LAYER.sql",
    "sql/realtime_updates/pg_20251105_144359_ON_PREMISE_SYSTEM_READY.sql",
    "sql/realtime_updates/pg_20251105_144658_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU.sql",
    "sql/realtime_updates/pg_20251105_144728_ANALIZA_WYNIKOW_LOKALNEGO_SYSTEMU_PELNY.sql",
    "sql/realtime_updates/pg_20251105_144744_FINAL_ANALYSIS_LOCAL_SYSTEM.sql",
    "sql/realtime_updates/pg_20251105_144952_OCENA_JAKOSCI_ANALIZY.sql",
    "sql/realtime_updates/pg_20251105_145122_IMPLEMENTACJA_POPRAWEK.sql",
    "sql/realtime_updates/pg_20251106_153941_PHASE2_COMPLETION_REPORT.sql",
    "sql/realtime_updates/pg_20251106_170530_FINAL_EXTRACTION_REPORT.sql",
    "sql/realtime_updates/pg_20251106_172206_COMMIT_457c53c_feature.sql",
    "sql/realtime_updates/pg_20251106_173640_INTELLIGENT_EXTRACTION_COMPLETE.sql",
    "sql/realtime_updates/pg_20251106_173724_COMMIT_9c14593_feature.sql",
    "sql/realtime_updates/pg_20251106_210141_COMMIT_3d81426_feature.sql",
    "sql/realtime_updates/pg_20251106_211912_BENCHMARK_COMPARISON_2023.sql",
    "sql/realtime_updates/pg_20251106_211928_BENCHMARK_COMPARISON_2023.sql",
    "sql/realtime_updates/pg_20251106_212248_BENCHMARK_COMPARISON_2023.sql",
    "sql/realtime_updates/pg_20251106_212256_BENCHMARK_COMPARISON_2023.sql",
    "sql/realtime_updates/pg_20251106_214208_Azoty_Intelligence_Local_20251106_214207.sql",
    "sql/realtime_updates/pg_20251106_220128_RAG_SYSTEM_SUMMARY.sql",
    "sql/realtime_updates/pg_20251106_220302_Azoty_Baseline_NoRAG.sql",
    "sql/realtime_updates/pg_20251106_220342_Azoty_RAG_Enhanced.sql",
    "sql/realtime_updates/pg_20251106_220529_Azoty_RAG_Enhanced.sql",
    "sql/realtime_updates/pg_20251106_222100_Azoty_MultiAgent_20251106_222059.sql",
    "src/analysis/__init__.py",
    "src/analysis/comparative_analyzer.py",
    "src/analysis/critical_assessor.py",
    "src/analysis/professional_analyzer.py",
    "src/analysis/qualitative_analyzer.py",
    "src/analysis/quantitative_extractor.py",
    "src/analysis/structure_extractor.py",
    "src/analysis/synthesis_engine.py",
    "src/analysis/temporal_trend_analyzer.py",
    "src/autonomous/autonomous_orchestrator.py",
    "src/autonomous/document_discovery.py",
    "src/autonomous/tool_registry.py",
    "src/data/__init__.py",
    "src/data/embedding_pipeline.py",
    "src/data/multi_year_extractor.py",
    "src/data/multi_year_storage.py",
    "src/data/qdrant_client.py",
    "src/data/smart_router.py",
    "src/intelligence/__init__.py",
    "src/intelligence/formatters/__init__.py",
    "src/intelligence/formatters/data_formatter.py",
    "src/intelligence/prompts/__init__.py",
    "src/intelligence/prompts/industry_context_prompts.py",
    "src/intelligence/prompts/local_llm_prompts.py",
    "src/intelligence/prompts/market_intelligence_prompts.py",
    "src/intelligence/prompts/strategic_evaluation_prompts.py",
    "src/intelligence/prompts/synthesis_prompts.py",
    "src/intelligence/services/__init__.py",
    "src/intelligence/services/local_intelligence_service.py",
    "src/intelligence/services/multi_agent_intelligence_service.py",
    "src/llm/__init__.py",
    "src/llm/agent_prompts.py",
    "src/llm/local_client.py",
    "src/memory/cache_augmented_generation.py",
    "src/memory/rag_cag_strategy.py",
    "src/parsing/document_parsers.py",
    "src/parsing/pdf_table_extractor.py",
    "src/rag/__init__.py",
    "src/rag/document_loader.py",
    "src/rag/qdrant_vector_store.py",
    "src/rag/rag_service.py",
    "src/rag/simple_vector_store.py",
    "src/storage/case_manager.py",
    "test_2023_benchmark.py",
    "test_azoty_2023_extraction.py",
    "test_simple_extraction_2023.py",
    "test_workflow_results.json",
    "tests/integration/test_database_integration.py"
  ],
  "auto_generated": true
}
```

---
*This document was automatically generated from a git commit.*
*Helena will process this and add to all 4 databases (PostgreSQL, Neo4j, Qdrant, Redis).*