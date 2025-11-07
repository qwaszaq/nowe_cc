# Multi-Year PDF Analysis Plan
## Comprehensive Baseline Testing Before Phase 1 Implementation

**Objective:** Test all three systems (Single-Agent, Multi-Agent, Claude) on 3 years of actual Azoty annual reports to establish comprehensive baseline for improvement planning.

**Rationale:** Current comparison uses only limited 2023 balance sheet data. Testing on full annual reports (2022, 2023, 2024) will reveal:
- How systems handle multi-year trends
- RAG quality with real document sections
- Ability to extract management guidance
- Handling of complete financial statements (not just balance sheet)
- Narrative analysis capability (MD&A, risk factors, strategy)

---

## Phase 1: Data Acquisition

### Task 1.1: Download Azoty Annual Reports

**Target Reports:**
1. Grupa Azoty S.A. Annual Report 2022 (fiscal year ending Dec 31, 2022)
2. Grupa Azoty S.A. Annual Report 2023 (fiscal year ending Dec 31, 2023)
3. Grupa Azoty S.A. Annual Report 2024 (fiscal year ending Dec 31, 2024, or latest available)

**Sources:**
- Primary: Grupa Azoty investor relations website (https://grupaazoty.com/en/relacje-inwestorskie)
- Alternative: Polish securities regulator (KNF) - https://www.knf.gov.pl
- Alternative: Warsaw Stock Exchange (WSE) filings

**Download Locations:**
```
data/documents/grupa_azoty/
├── Grupa_Azoty_Annual_Report_2022.pdf
├── Grupa_Azoty_Annual_Report_2023.pdf
└── Grupa_Azoty_Annual_Report_2024.pdf (or H1 2024 if annual not yet available)
```

**Deliverable:** 3 PDF annual reports

---

## Phase 2: Data Extraction & Preparation

### Task 2.1: Extract Multi-Year Financial Data

**Objective:** Extract complete financial statements from all 3 reports

**Data to Extract:**
- Balance Sheet (all line items, 3 years)
- Income Statement (all line items, 3 years)
- Cash Flow Statement (all line items, 3 years)
- Key ratios (calculated from extracted data)

**Method:**
```bash
# Use existing extraction system
python3 src/document_processing/intelligent_extractor.py \
  --pdf data/documents/grupa_azoty/Grupa_Azoty_Annual_Report_2022.pdf \
  --output data/companies/grupa_azoty_2022.json

python3 src/document_processing/intelligent_extractor.py \
  --pdf data/documents/grupa_azoty/Grupa_Azoty_Annual_Report_2023.pdf \
  --output data/companies/grupa_azoty_2023.json

python3 src/document_processing/intelligent_extractor.py \
  --pdf data/documents/grupa_azoty/Grupa_Azoty_Annual_Report_2024.pdf \
  --output data/companies/grupa_azoty_2024.json
```

**Validation:**
- Verify accounting equation (Assets = Liabilities + Equity)
- Check year-over-year trend consistency
- Validate currency (PLN thousands)

**Deliverable:** 3 JSON files with complete financial data

---

### Task 2.2: Combine Multi-Year Dataset

**Objective:** Create unified dataset with 3-year trends

**File:** `data/companies/grupa_azoty_multi_year.json`

**Structure:**
```json
{
  "company_name": "Grupa Azoty S.A.",
  "industry": "Chemicals & Fertilizers",
  "currency": "PLN",
  "unit": "thousands",
  "balance_sheet": {
    "Total Assets": {2022: X, 2023: Y, 2024: Z},
    "Current Assets": {2022: X, 2023: Y, 2024: Z},
    ...
  },
  "income_statement": {
    "Revenue": {2022: X, 2023: Y, 2024: Z},
    "EBIT": {2022: X, 2023: Y, 2024: Z},
    ...
  },
  "cash_flow": {
    "Operating Cash Flow": {2022: X, 2023: Y, 2024: Z},
    ...
  }
}
```

**Deliverable:** Unified multi-year JSON dataset

---

### Task 2.3: Ingest PDFs into RAG System

**Objective:** Load all 3 annual reports into Qdrant for RAG queries

**Method:**
```python
# scripts/ingest_azoty_multi_year.py

from src.rag.document_loader import DocumentLoader
from src.rag.qdrant_vector_store import QdrantVectorStore

def ingest_all_reports():
    """Ingest 3 years of Azoty reports into Qdrant"""

    loader = DocumentLoader(chunk_size=750, chunk_overlap=100)
    vector_store = QdrantVectorStore(
        collection_name="azoty_multi_year",
        url="http://localhost:6333"
    )

    # Load each year
    reports = {
        2022: "data/documents/grupa_azoty/Grupa_Azoty_Annual_Report_2022.pdf",
        2023: "data/documents/grupa_azoty/Grupa_Azoty_Annual_Report_2023.pdf",
        2024: "data/documents/grupa_azoty/Grupa_Azoty_Annual_Report_2024.pdf"
    }

    all_docs = []
    for year, pdf_path in reports.items():
        print(f"Loading {year} report...")
        docs = loader.load_annual_report(
            pdf_path=Path(pdf_path),
            company="Grupa Azoty S.A.",
            year=year
        )
        all_docs.extend(docs)
        print(f"  Loaded {len(docs)} chunks from {year}")

    print(f"\nTotal chunks: {len(all_docs)}")

    # Ingest into Qdrant
    vector_store.ingest_documents(all_docs)

    print("✅ RAG ingestion complete")

    # Test retrieval
    print("\nTesting retrieval...")
    results = vector_store.search(
        query="Why did profitability decline from 2022 to 2023?",
        company="Grupa Azoty S.A.",
        top_k=5
    )

    for i, result in enumerate(results, 1):
        print(f"\nResult {i} (score: {result['score']:.3f}):")
        print(f"Year: {result['metadata']['year']}")
        print(f"Page: {result['metadata']['page']}")
        print(f"Content: {result['content'][:150]}...")

if __name__ == "__main__":
    ingest_all_reports()
```

**Deliverable:** Qdrant collection with 3 years of documents

---

## Phase 3: Analysis Generation

### Task 3.1: Generate Single-Agent Analysis

**Objective:** Generate single-agent intelligence report using multi-year data

**Command:**
```bash
python3 scripts/test_intelligence_multi_year.py --system single-agent
```

**Expected Output:**
- File: `output/intelligence_reports/Azoty_SingleAgent_MultiYear_[timestamp].md`
- Generation time: ~30-40 seconds
- Report length: 20,000-25,000 characters
- Perspectives: 2 (Financial Health + Risk Assessment)

**Analysis Coverage:**
- 3-year financial trend analysis
- Year-over-year changes (2022→2023→2024)
- Trend identification (improving/stable/deteriorating)
- Basic investment thesis (Bull/Bear/Base)

**Deliverable:** Single-agent multi-year report

---

### Task 3.2: Generate Multi-Agent Analysis

**Objective:** Generate 6-agent intelligence report with RAG

**Command:**
```bash
python3 scripts/test_intelligence_multi_year.py --system multi-agent --use-rag
```

**Expected Output:**
- File: `output/intelligence_reports/Azoty_MultiAgent_MultiYear_[timestamp].md`
- Generation time: ~90-120 seconds (longer with 3 years of data)
- Report length: 12,000-15,000 characters
- Perspectives: 6 (Financial + Risk + Industry + Strategy + Market + Synthesis)

**Analysis Coverage:**
- 3-year trends across all dimensions
- RAG-grounded analysis (cites specific report sections and page numbers)
- Industry context (competitive position, market trends)
- Strategic assessment (management guidance, initiatives)
- Market intelligence (catalysts, recent developments)
- Cross-perspective synthesis (converging signals, conflicts, blind spots)

**Deliverable:** Multi-agent multi-year report

---

### Task 3.3: Generate Claude Benchmark Analysis

**Objective:** Generate Claude analysis as quality benchmark

**Method:**
```bash
python3 scripts/generate_claude_multi_year.py
```

**Process:**
1. Load multi-year data
2. Prepare comprehensive prompt with 3 years of financials
3. Generate prompt file for manual Claude submission
4. Submit to Claude (claude.ai or API)
5. Save Claude's response

**Expected Output:**
- File: `output/intelligence_reports/Azoty_Claude_MultiYear_[timestamp].md`
- Report length: 18,000-22,000 characters
- Perspectives: 6 (comprehensive)

**Analysis Coverage:**
- Multi-year trend analysis with severity calibration
- Framework selection (credit vs equity based on 3-year trajectory)
- Causal reasoning (feedback loops, cascading effects)
- Probability-weighted scenarios (Bull/Base/Bear with percentages)
- Decision triggers (upgrade/downgrade conditions)

**Deliverable:** Claude multi-year benchmark report

---

## Phase 4: Comparative Analysis

### Task 4.1: Three-Way Comparison

**Objective:** Compare all three systems on multi-year PDF analysis

**Comparison Dimensions:**

1. **Data Extraction Quality**
   - Completeness (% of financial data extracted from PDFs)
   - Accuracy (verification against source PDFs)
   - Trend consistency (year-over-year changes make sense)

2. **Analysis Depth**
   - Coverage of analysis dimensions (financial, risk, industry, strategy, market)
   - Multi-year trend analysis (vs single-year snapshot)
   - Causal reasoning (identifies why metrics changed)

3. **RAG Quality**
   - Source citations (page numbers, section references)
   - Relevance (retrieved context matches query)
   - Integration (RAG context woven into analysis effectively)

4. **Severity Calibration**
   - Framework selection (credit vs equity appropriate for company state)
   - Severity language (critical vs weak for same condition)
   - Probability calibration (realistic bull/base/bear percentages)

5. **Narrative Analysis**
   - Management guidance extraction
   - Risk factor identification
   - Strategic initiative tracking
   - Industry context understanding

6. **Recommendation Quality**
   - Consistency with analysis (recommendation follows from findings)
   - Decision triggers (specific, measurable)
   - Probability weighting (realistic scenario probabilities)

**Comparison Document:**
```
MULTI_YEAR_PDF_COMPARISON.md

Structure:
1. Executive Summary (key findings)
2. Data Extraction Comparison
3. Analysis Depth Comparison
4. RAG Quality Comparison
5. Severity Calibration Comparison
6. Narrative Analysis Comparison
7. Recommendation Quality Comparison
8. Gap Analysis (what local systems are missing)
9. Improvement Priorities (what to fix first)
```

**Deliverable:** Comprehensive comparison report

---

### Task 4.2: Gap Analysis & Improvement Priorities

**Objective:** Identify specific gaps and prioritize improvements

**Gap Categories:**

1. **Prompt Engineering Gaps**
   - Severity calibration failures
   - Framework selection errors
   - Missing chain-of-thought reasoning
   - Vague probability estimates

2. **RAG System Gaps**
   - Retrieval quality issues
   - Section filtering effectiveness
   - Reranking performance
   - Context integration

3. **Data Extraction Gaps**
   - Missing financial statement items
   - Incomplete multi-year coverage
   - Ratio calculation errors

4. **Architectural Gaps**
   - Multi-agent coordination issues
   - Context passing effectiveness
   - Synthesis quality

**Prioritization Framework:**

| Gap | Impact | Effort | Priority |
|-----|--------|--------|----------|
| Severity calibration | High | Low | 1 |
| Framework selection | High | Low | 1 |
| RAG retrieval quality | High | Medium | 2 |
| Chain-of-thought | Medium | Low | 3 |
| Probability calibration | Medium | Low | 3 |
| Data extraction completeness | Medium | High | 4 |

**Deliverable:** Prioritized improvement roadmap

---

## Phase 5: Implementation Plan

### Task 5.1: Create Targeted Improvement Plan

**Based on gap analysis, create specific improvements for:**

**High-Priority (Week 1):**
1. Severity calibration prompts (add explicit scales)
2. Framework decision tree (credit vs equity)
3. Few-shot examples (calibrated severity)

**Medium-Priority (Week 2):**
4. RAG query optimization (better retrieval)
5. Chain-of-thought templates
6. Probability quantification mandates

**Lower-Priority (Week 3-4):**
7. Self-critique loop
8. Multi-year trend analysis enhancement
9. Narrative extraction improvement

**Deliverable:** Updated LOCAL_SYSTEM_IMPROVEMENT_PLAN.md with multi-year PDF findings

---

## Implementation Timeline

### Week 0: Data Acquisition & Preparation (3-5 days)
- Day 1: Download 3 annual reports
- Day 2: Extract financial data from each PDF
- Day 3: Combine into multi-year dataset
- Day 4: Ingest PDFs into RAG system
- Day 5: Validate data quality

**Checkpoint:** All 3 PDFs downloaded, extracted, validated, ingested into RAG

### Week 1: Analysis Generation (3-5 days)
- Day 1: Generate single-agent multi-year report
- Day 2: Generate multi-agent multi-year report
- Day 3: Generate Claude multi-year benchmark
- Day 4: Initial comparison review
- Day 5: Detailed gap analysis

**Checkpoint:** 3 comprehensive reports generated, initial gaps identified

### Week 2: Comparative Analysis & Planning (3-5 days)
- Day 1-2: Complete three-way comparison document
- Day 3: Gap analysis and prioritization
- Day 4: Create targeted improvement plan
- Day 5: Review and finalize roadmap

**Checkpoint:** MULTI_YEAR_PDF_COMPARISON.md complete, improvement priorities clear

### Week 3-4: Begin Improvements
- Implement high-priority improvements from gap analysis
- Test on multi-year dataset
- Measure improvement vs baseline

---

## Success Criteria

### Data Extraction
- ✅ All 3 annual reports downloaded
- ✅ Complete financial statements extracted (balance sheet, income statement, cash flow)
- ✅ Accounting equation validated for all years
- ✅ Multi-year trends consistent
- ✅ PDFs ingested into RAG system

### Analysis Generation
- ✅ Single-agent report generated successfully
- ✅ Multi-agent report generated with RAG
- ✅ Claude benchmark generated
- ✅ All reports analyze 3-year trends (not just 2023)

### Comparison Quality
- ✅ Comprehensive comparison across 6 dimensions
- ✅ Specific gaps identified with examples
- ✅ Improvement priorities ranked (impact × effort)
- ✅ Targeted improvement plan created

### Quality Baseline
- ✅ Quantitative metrics captured (generation time, report length, coverage %)
- ✅ Qualitative assessment documented (severity calibration, framework selection, etc.)
- ✅ Clear baseline established for measuring future improvements

---

## Key Questions to Answer

Through this multi-year PDF analysis, we will answer:

1. **Data Extraction:**
   - How complete is our PDF extraction? (% of financial data captured)
   - How accurate are multi-year trends? (verification against source PDFs)

2. **RAG Quality:**
   - Does RAG improve analysis depth with full PDFs? (vs limited 2023 data)
   - Are source citations accurate? (page numbers, section references)
   - Does section filtering work? (financial_statements, management_discussion, etc.)

3. **Analysis Quality:**
   - Do systems identify multi-year trends? (2022→2023→2024 trajectory)
   - Do systems explain why metrics changed? (causal reasoning)
   - Do systems extract management guidance? (from MD&A sections)

4. **System Comparison:**
   - How does single-agent compare to multi-agent on comprehensive PDFs?
   - How do local systems compare to Claude on multi-year analysis?
   - What are the TOP 3 gaps to fix first?

5. **Improvement Direction:**
   - Is the problem data extraction or analysis quality?
   - Is the problem RAG retrieval or prompt engineering?
   - Should we focus on single-agent improvements or multi-agent architecture?

---

## Deliverables Checklist

### Data
- [ ] Grupa Azoty Annual Report 2022.pdf
- [ ] Grupa Azoty Annual Report 2023.pdf
- [ ] Grupa Azoty Annual Report 2024.pdf
- [ ] grupa_azoty_2022.json (extracted data)
- [ ] grupa_azoty_2023.json (extracted data)
- [ ] grupa_azoty_2024.json (extracted data)
- [ ] grupa_azoty_multi_year.json (combined dataset)
- [ ] Qdrant collection "azoty_multi_year" (RAG)

### Reports
- [ ] Azoty_SingleAgent_MultiYear_[timestamp].md
- [ ] Azoty_MultiAgent_MultiYear_[timestamp].md
- [ ] Azoty_Claude_MultiYear_[timestamp].md

### Analysis Documents
- [ ] MULTI_YEAR_PDF_COMPARISON.md (comprehensive comparison)
- [ ] MULTI_YEAR_GAP_ANALYSIS.md (specific gaps and priorities)
- [ ] LOCAL_SYSTEM_IMPROVEMENT_PLAN.md (updated with multi-year findings)

### Scripts
- [ ] scripts/ingest_azoty_multi_year.py
- [ ] scripts/test_intelligence_multi_year.py
- [ ] scripts/generate_claude_multi_year.py
- [ ] scripts/compare_multi_year_systems.py

---

## Risk Mitigation

**Risk:** Annual reports not available in English
**Mitigation:** Use Polish reports, extract financials (universal), note language limitation for narrative analysis

**Risk:** 2024 annual report not yet published
**Mitigation:** Use H1 2024 report or Q3 2024 report as substitute, note data limitation

**Risk:** PDF extraction quality poor for complex layouts
**Mitigation:** Manual verification of extracted data against source PDFs, flag extraction confidence scores

**Risk:** RAG retrieval low quality with full documents
**Mitigation:** Test section filtering, adjust chunk size if needed, measure retrieval precision

**Risk:** Multi-year analysis too slow (>5 minutes)
**Mitigation:** Profile performance, optimize if needed, document performance vs quality trade-off

---

**Status:** Plan Complete - Ready to Execute
**Next Step:** Task 1.1 - Download 3 Azoty annual reports
**Timeline:** 2-3 weeks total (acquisition + analysis + comparison)
**Objective:** Establish comprehensive baseline before implementing improvements
**Maintainer:** Artur
**Last Updated:** 2025-11-07
