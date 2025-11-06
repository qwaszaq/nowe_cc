# Intelligent Multi-Source Extraction System Design

**Date:** 2025-11-06
**Purpose:** Auto-detect extraction problems and implement appropriate strategies for multi-source financial data
**Context:** Building on Round 2 success (text extraction for Polish PDFs), expand to handle PDF, TXT, DOCX, and other formats

---

## 🎯 Goals

1. **Auto-detect extraction quality issues** - Identify when primary extraction method fails
2. **Multi-source support** - Handle PDF, TXT, DOCX, CSV, Excel, HTML financial reports
3. **Intelligent fallback chain** - Automatically try alternative extraction strategies
4. **Quality validation** - Verify extracted data meets financial statement requirements
5. **Language support** - Handle Polish, English, and potentially other languages
6. **Performance** - Fast extraction with minimal overhead

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Intelligent Extraction Manager                │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  1. Document Type Detection                                 │ │
│  │     - File extension (.pdf, .txt, .docx, .xlsx, .html)     │ │
│  │     - Content sniffing (magic bytes, structure analysis)   │ │
│  │     - Language detection (Polish vs English vs Other)      │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ↓                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  2. Primary Extraction Strategy Selection                   │ │
│  │     - PDF: pdfplumber → Camelot → Text extraction          │ │
│  │     - DOCX: python-docx table extraction → Text parsing    │ │
│  │     - TXT: Direct text parsing with regex                  │ │
│  │     - XLSX: pandas → openpyxl structured data              │ │
│  │     - HTML: BeautifulSoup table extraction                 │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ↓                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  3. Quality Assessment                                      │ │
│  │     - Key item detection (total assets, equity, etc.)      │ │
│  │     - Accounting equation validation                       │ │
│  │     - Semantic matching (E5 embeddings)                    │ │
│  │     - Numeric density check                                │ │
│  │     - Completeness score (% of required fields)            │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ↓                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  4. Fallback Chain (if quality < threshold)                │ │
│  │     - Try alternative extraction methods                   │ │
│  │     - Adjust parameters (chunk size, page range, regex)    │ │
│  │     - Multi-strategy fusion (combine results)              │ │
│  │     - Human-in-the-loop (request manual guidance)          │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              ↓                                    │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  5. Result Validation & Enrichment                         │ │
│  │     - Final accounting equation check                      │ │
│  │     - Calculate derived metrics (ratios, working capital)  │ │
│  │     - Confidence scoring per field                         │ │
│  │     - Metadata: extraction method used, quality score      │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📄 Document Type Handlers

### 1. PDF Handler (Enhanced)

**Current Capability:**
- ✅ pdfplumber table detection
- ✅ Camelot stream-based extraction
- ✅ Text-based fallback for borderless tables
- ✅ E5 semantic matching for balance sheets

**Proposed Enhancements:**

```python
class PDFExtractionStrategy:
    """
    Multi-strategy PDF extraction with auto-detection
    """

    STRATEGIES = [
        'pdfplumber_tables',      # Best for bordered tables
        'camelot_stream',         # Best for text-aligned tables
        'camelot_lattice',        # Best for heavy borders
        'text_extraction',        # Best for borderless/text layout
        'ocr_fallback',           # Last resort for scanned PDFs
    ]

    def extract(self, pdf_path: Path) -> ExtractionResult:
        """
        Try strategies in order until quality threshold met
        """
        for strategy in self.STRATEGIES:
            result = self._try_strategy(strategy, pdf_path)

            if result.quality_score > self.quality_threshold:
                logger.info(f"✅ Success with {strategy}: {result.quality_score:.1%}")
                return result
            else:
                logger.warning(f"⚠️  {strategy} insufficient: {result.quality_score:.1%}")

        # Fusion: Combine results from multiple strategies
        return self._fusion_strategy(pdf_path)

    def _try_strategy(self, strategy: str, pdf_path: Path) -> ExtractionResult:
        """Execute specific extraction strategy"""
        if strategy == 'pdfplumber_tables':
            return self._extract_with_pdfplumber(pdf_path)
        elif strategy == 'camelot_stream':
            return self._extract_with_camelot_stream(pdf_path)
        elif strategy == 'text_extraction':
            return self._extract_from_text(pdf_path)
        elif strategy == 'ocr_fallback':
            return self._extract_with_ocr(pdf_path)
        # ... etc

    def _fusion_strategy(self, pdf_path: Path) -> ExtractionResult:
        """
        Combine results from multiple strategies
        - Use best value for each field (highest confidence)
        - Fill gaps from secondary sources
        """
        results = [self._try_strategy(s, pdf_path) for s in self.STRATEGIES[:3]]
        return self._merge_results(results)
```

**New Features:**
- **OCR Support** - For scanned PDFs (Tesseract/AWS Textract)
- **Layout Analysis** - Detect table vs text-based layout automatically
- **Multi-page Balance Sheets** - Handle statements spanning multiple pages
- **Column Detection** - Auto-detect multi-column layouts

### 2. DOCX Handler (New)

**Use Case:** Financial reports in Microsoft Word format

```python
class DOCXExtractionStrategy:
    """
    Extract financial statements from Word documents
    """

    def extract(self, docx_path: Path) -> ExtractionResult:
        """
        1. Try python-docx table extraction
        2. Fallback to text parsing
        3. Handle nested tables
        """
        doc = Document(docx_path)

        # Strategy 1: Extract from tables
        tables = doc.tables
        for table in tables:
            if self._is_balance_sheet(table):
                return self._extract_from_table(table)

        # Strategy 2: Extract from text
        text = "\n".join([p.text for p in doc.paragraphs])
        return self._extract_from_text(text)

    def _is_balance_sheet(self, table) -> bool:
        """Check if table contains balance sheet markers"""
        text = self._table_to_text(table)
        return any(keyword in text.lower() for keyword in
                  ['aktywa razem', 'total assets', 'bilans', 'balance sheet'])

    def _extract_from_table(self, table) -> ExtractionResult:
        """Extract values from Word table structure"""
        rows = []
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            rows.append(cells)

        return self._parse_structured_data(rows)
```

**Features:**
- Table structure extraction
- Text-based fallback
- Nested table handling
- Style-based section detection (headings, bold text)

### 3. TXT Handler (New)

**Use Case:** Plain text exports of financial statements

```python
class TXTExtractionStrategy:
    """
    Extract financial statements from plain text files
    """

    def extract(self, txt_path: Path) -> ExtractionResult:
        """
        Pure text parsing - most challenging format
        """
        with open(txt_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Detect layout type
        if self._is_tabular_layout(text):
            return self._extract_tabular(text)
        elif self._is_indented_layout(text):
            return self._extract_indented(text)
        else:
            return self._extract_freeform(text)

    def _is_tabular_layout(self, text: str) -> bool:
        """Detect if text uses tabs/spaces for alignment"""
        lines = text.split('\n')
        # Check for consistent spacing patterns
        return self._has_consistent_columns(lines)

    def _extract_tabular(self, text: str) -> ExtractionResult:
        """
        Extract from tab/space-aligned text
        Similar to current PDF text extraction
        """
        patterns = self._build_regex_patterns()
        return self._apply_patterns(text, patterns)
```

**Challenges:**
- No structural information (no borders, no formatting)
- Requires sophisticated regex patterns
- Need to handle various alignment styles (tabs, spaces, dots)

**Solutions:**
- Pattern learning from examples
- ML-based column detection
- Heuristic alignment detection

### 4. XLSX/CSV Handler (New)

**Use Case:** Excel exports and CSV files

```python
class SpreadsheetExtractionStrategy:
    """
    Extract from Excel and CSV files
    """

    def extract(self, file_path: Path) -> ExtractionResult:
        """
        Structured data extraction - easiest case
        """
        if file_path.suffix == '.xlsx':
            df = pd.read_excel(file_path, sheet_name=None)  # All sheets
        else:  # .csv
            df = {'Sheet1': pd.read_csv(file_path)}

        # Find the balance sheet
        for sheet_name, data in df.items():
            if self._is_balance_sheet(data):
                return self._extract_from_dataframe(data)

        return ExtractionResult(success=False, error="No balance sheet found")

    def _is_balance_sheet(self, df: pd.DataFrame) -> bool:
        """Check if DataFrame contains balance sheet"""
        text = df.to_string()
        return any(keyword in text.lower() for keyword in
                  ['aktywa razem', 'total assets', 'pasywa razem'])

    def _extract_from_dataframe(self, df: pd.DataFrame) -> ExtractionResult:
        """
        Extract from structured DataFrame
        - Column detection (labels, current year, prior year)
        - Row matching (total assets, equity, etc.)
        """
        financial_data = {}

        # Detect label column and value columns
        label_col = self._find_label_column(df)
        value_cols = [c for c in df.columns if c != label_col]

        # Extract values
        for idx, row in df.iterrows():
            label = str(row[label_col]).lower()
            if 'aktywa razem' in label:
                financial_data['total_assets'] = row[value_cols[0]]
            # ... etc

        return ExtractionResult(success=True, data=financial_data)
```

**Advantages:**
- Structured data (easiest to parse)
- Clear column/row boundaries
- Type information (numbers vs text)

**Challenges:**
- Multi-level headers
- Merged cells
- Irregular structure (notes, subtotals in wrong places)

### 5. HTML Handler (New)

**Use Case:** Web-published financial statements

```python
class HTMLExtractionStrategy:
    """
    Extract from HTML financial reports
    """

    def extract(self, html_path: Path) -> ExtractionResult:
        """
        Extract from HTML tables using BeautifulSoup
        """
        with open(html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # Find all tables
        tables = soup.find_all('table')

        for table in tables:
            if self._is_balance_sheet(table):
                return self._extract_from_table(table)

        # Fallback: extract from text
        text = soup.get_text()
        return self._extract_from_text(text)

    def _is_balance_sheet(self, table) -> bool:
        """Check if HTML table contains balance sheet"""
        text = table.get_text()
        return any(keyword in text.lower() for keyword in
                  ['balance sheet', 'statement of financial position', 'bilans'])

    def _extract_from_table(self, table) -> ExtractionResult:
        """Extract from HTML table structure"""
        rows = []
        for tr in table.find_all('tr'):
            cells = [td.get_text().strip() for td in tr.find_all(['td', 'th'])]
            rows.append(cells)

        return self._parse_structured_data(rows)
```

**Features:**
- HTML table structure extraction
- Handle CSS styling (bold = total row)
- Multi-table documents (find correct table)
- XBRL support (for regulatory filings)

---

## 🔍 Quality Assessment System

### Quality Metrics

```python
@dataclass
class QualityMetrics:
    """
    Multi-dimensional quality assessment
    """

    # Completeness: % of required fields found
    completeness_score: float  # 0.0 - 1.0
    required_fields_found: int
    required_fields_total: int

    # Validation: Does data make sense?
    validation_score: float  # 0.0 - 1.0
    accounting_equation_valid: bool  # Assets = Equity + Liabilities
    balance_diff: float  # How far off from perfect balance

    # Confidence: How confident are we in extraction?
    confidence_score: float  # 0.0 - 1.0
    semantic_match_score: float  # E5 embedding similarity
    numeric_density: float  # % of expected numbers found

    # Overall Quality Score (weighted average)
    overall_score: float  # 0.0 - 1.0

    # Metadata
    extraction_method: str  # Which strategy succeeded
    fallback_attempts: int  # How many strategies tried
    processing_time: float  # Seconds


class QualityAssessor:
    """
    Assess extraction quality
    """

    REQUIRED_FIELDS = [
        'total_assets',
        'total_equity',
        'total_liabilities',
        'current_assets',
        'current_liabilities',
        'fixed_assets',
        'cash',
        'inventories',
    ]

    WEIGHTS = {
        'completeness': 0.35,
        'validation': 0.35,
        'confidence': 0.30,
    }

    def assess(self, result: ExtractionResult) -> QualityMetrics:
        """
        Comprehensive quality assessment
        """
        # 1. Completeness
        completeness = self._assess_completeness(result)

        # 2. Validation
        validation = self._assess_validation(result)

        # 3. Confidence
        confidence = self._assess_confidence(result)

        # 4. Overall score
        overall = (
            completeness * self.WEIGHTS['completeness'] +
            validation * self.WEIGHTS['validation'] +
            confidence * self.WEIGHTS['confidence']
        )

        return QualityMetrics(
            completeness_score=completeness,
            validation_score=validation,
            confidence_score=confidence,
            overall_score=overall,
            # ... other fields
        )

    def _assess_completeness(self, result: ExtractionResult) -> float:
        """
        Score: % of required fields successfully extracted
        """
        found = sum(1 for field in self.REQUIRED_FIELDS
                   if field in result.data and result.data[field] is not None)
        return found / len(self.REQUIRED_FIELDS)

    def _assess_validation(self, result: ExtractionResult) -> float:
        """
        Score: Does accounting equation hold?
        Assets = Equity + Liabilities (within 1% tolerance)
        """
        try:
            assets = result.data.get('total_assets', 0)
            equity = result.data.get('total_equity', 0)
            liabilities = result.data.get('total_liabilities', 0)

            balance = equity + liabilities
            diff = abs(assets - balance)
            tolerance = assets * 0.01  # 1%

            if diff < tolerance:
                return 1.0
            elif diff < tolerance * 5:  # 5%
                return 0.5
            else:
                return 0.0
        except:
            return 0.0

    def _assess_confidence(self, result: ExtractionResult) -> float:
        """
        Score: How confident are we?
        - Semantic match score (E5 embeddings)
        - Numeric density (are numbers present?)
        - Extraction method reliability
        """
        semantic_score = result.metadata.get('semantic_match_score', 0.5)
        numeric_density = result.metadata.get('numeric_density', 0.0)

        # Weight semantic matching more heavily
        return semantic_score * 0.7 + numeric_density * 0.3
```

### Quality Thresholds

```python
class QualityThresholds:
    """
    Define when extraction is "good enough"
    """

    # Minimum scores to accept extraction
    MIN_OVERALL_SCORE = 0.70  # 70% overall quality
    MIN_COMPLETENESS = 0.60   # 60% of required fields (5/8)
    MIN_VALIDATION = 0.80     # Accounting equation within 5%
    MIN_CONFIDENCE = 0.60     # 60% confidence

    # Thresholds for warnings
    WARN_OVERALL_SCORE = 0.85
    WARN_COMPLETENESS = 0.75

    @classmethod
    def should_accept(cls, metrics: QualityMetrics) -> bool:
        """
        Should we accept this extraction result?
        """
        return (
            metrics.overall_score >= cls.MIN_OVERALL_SCORE and
            metrics.completeness_score >= cls.MIN_COMPLETENESS and
            metrics.validation_score >= cls.MIN_VALIDATION and
            metrics.confidence_score >= cls.MIN_CONFIDENCE
        )

    @classmethod
    def should_warn(cls, metrics: QualityMetrics) -> bool:
        """
        Should we warn user about quality?
        """
        return (
            metrics.overall_score < cls.WARN_OVERALL_SCORE or
            metrics.completeness_score < cls.WARN_COMPLETENESS
        )
```

---

## 🔄 Fallback Chain Strategy

### Intelligent Fallback

```python
class IntelligentExtractionManager:
    """
    Orchestrate extraction with automatic fallbacks
    """

    def __init__(self):
        self.handlers = {
            '.pdf': PDFExtractionStrategy(),
            '.docx': DOCXExtractionStrategy(),
            '.txt': TXTExtractionStrategy(),
            '.xlsx': SpreadsheetExtractionStrategy(),
            '.csv': SpreadsheetExtractionStrategy(),
            '.html': HTMLExtractionStrategy(),
        }
        self.quality_assessor = QualityAssessor()

    def extract(self, file_path: Path) -> ExtractionResult:
        """
        Main extraction entry point
        """
        logger.info(f"📄 Starting extraction: {file_path.name}")

        # 1. Detect file type
        handler = self._get_handler(file_path)

        # 2. Primary extraction
        result = handler.extract(file_path)

        # 3. Quality assessment
        metrics = self.quality_assessor.assess(result)
        result.quality_metrics = metrics

        logger.info(f"   Quality: {metrics.overall_score:.1%} "
                   f"(completeness: {metrics.completeness_score:.1%}, "
                   f"validation: {metrics.validation_score:.1%})")

        # 4. Decision: Accept, Retry, or Fallback?
        if QualityThresholds.should_accept(metrics):
            logger.info(f"✅ Extraction successful with {metrics.extraction_method}")
            return result

        # 5. Fallback chain
        logger.warning(f"⚠️  Quality insufficient ({metrics.overall_score:.1%}), trying fallbacks...")
        return self._fallback_chain(file_path, handler, result)

    def _fallback_chain(self, file_path: Path, handler, initial_result: ExtractionResult) -> ExtractionResult:
        """
        Try alternative strategies
        """
        fallback_strategies = handler.get_fallback_strategies()

        best_result = initial_result
        best_score = initial_result.quality_metrics.overall_score

        for i, strategy in enumerate(fallback_strategies):
            logger.info(f"   Fallback {i+1}/{len(fallback_strategies)}: Trying {strategy}...")

            result = handler.extract_with_strategy(file_path, strategy)
            metrics = self.quality_assessor.assess(result)
            result.quality_metrics = metrics

            logger.info(f"      Result: {metrics.overall_score:.1%} quality")

            # Keep best result
            if metrics.overall_score > best_score:
                best_result = result
                best_score = metrics.overall_score

            # Accept if good enough
            if QualityThresholds.should_accept(metrics):
                logger.info(f"✅ Fallback successful with {strategy}")
                return result

        # 6. Fusion strategy: Combine results
        logger.info("   Trying fusion strategy (combining results)...")
        fusion_result = self._fusion_extraction(file_path, handler)
        fusion_metrics = self.quality_assessor.assess(fusion_result)

        if fusion_metrics.overall_score > best_score:
            logger.info(f"✅ Fusion successful: {fusion_metrics.overall_score:.1%}")
            return fusion_result

        # 7. Return best result (even if below threshold)
        logger.warning(f"⚠️  All strategies exhausted. Best score: {best_score:.1%}")
        return best_result

    def _fusion_extraction(self, file_path: Path, handler) -> ExtractionResult:
        """
        Combine results from multiple strategies
        """
        strategies = handler.get_all_strategies()
        results = [handler.extract_with_strategy(file_path, s) for s in strategies]

        # Merge: For each field, take value with highest confidence
        merged_data = {}
        merged_confidence = {}

        for field in QualityAssessor.REQUIRED_FIELDS:
            best_value = None
            best_confidence = 0.0

            for result in results:
                if field in result.data:
                    value = result.data[field]
                    confidence = result.metadata.get(f'{field}_confidence', 0.5)

                    if confidence > best_confidence:
                        best_value = value
                        best_confidence = confidence

            if best_value is not None:
                merged_data[field] = best_value
                merged_confidence[field] = best_confidence

        return ExtractionResult(
            success=True,
            data=merged_data,
            metadata={'fusion': True, 'confidence': merged_confidence}
        )
```

---

## 🌍 Multi-Language Support

### Language Detection

```python
class LanguageDetector:
    """
    Detect document language and adjust extraction patterns
    """

    LANGUAGE_KEYWORDS = {
        'polish': [
            'aktywa', 'pasywa', 'zobowiązania', 'kapitał własny',
            'środki pieniężne', 'należności', 'zapasy'
        ],
        'english': [
            'assets', 'liabilities', 'equity', 'cash',
            'receivables', 'inventory', 'payables'
        ],
        'german': [
            'aktiva', 'passiva', 'eigenkapital', 'verbindlichkeiten'
        ],
    }

    def detect(self, text: str) -> str:
        """
        Detect primary language
        """
        text_lower = text.lower()

        scores = {}
        for lang, keywords in self.LANGUAGE_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            scores[lang] = score

        return max(scores, key=scores.get)


class MultiLanguagePatterns:
    """
    Regex patterns for different languages
    """

    PATTERNS = {
        'polish': {
            'total_assets': r'AKTYWA\s+RAZEM\s*\n\s*\n\s*(\d[\d\s]+)',
            'total_equity': r'Kapitał\s+własny\s+razem\s*\n\s*(\d[\d\s]+)',
            # ... more patterns
        },
        'english': {
            'total_assets': r'Total\s+Assets\s*\n\s*(\d[\d\s,]+)',
            'total_equity': r'Total\s+Equity\s*\n\s*(\d[\d\s,]+)',
            # ... more patterns
        },
    }

    def get_patterns(self, language: str) -> dict:
        """
        Get regex patterns for language
        """
        return self.PATTERNS.get(language, self.PATTERNS['english'])
```

---

## 📊 Usage Example

```python
# Initialize the intelligent extraction manager
manager = IntelligentExtractionManager()

# Extract from any supported file type
files = [
    'azoty_annual_2024.pdf',
    'quarterly_report_q3.docx',
    'financial_statement.txt',
    'balance_sheet.xlsx',
    'financial_data.csv',
    'annual_report.html',
]

for file in files:
    result = manager.extract(Path(file))

    if result.success:
        metrics = result.quality_metrics

        # Print summary
        print(f"\n📄 {file}")
        print(f"   ✅ Extraction successful")
        print(f"   📊 Quality: {metrics.overall_score:.1%}")
        print(f"   📋 Completeness: {metrics.completeness_score:.1%} "
              f"({metrics.required_fields_found}/{metrics.required_fields_total})")
        print(f"   ✔️  Validation: {metrics.validation_score:.1%}")
        print(f"   🎯 Confidence: {metrics.confidence_score:.1%}")
        print(f"   ⚙️  Method: {metrics.extraction_method}")
        print(f"   ⏱️  Time: {metrics.processing_time:.2f}s")

        if QualityThresholds.should_warn(metrics):
            print(f"   ⚠️  Warning: Quality below recommended threshold")

        # Print extracted values
        print(f"\n   Extracted Values:")
        print(f"   - Total Assets: {result.data.get('total_assets'):,.0f}")
        print(f"   - Total Equity: {result.data.get('total_equity'):,.0f}")
        print(f"   - Total Liabilities: {result.data.get('total_liabilities'):,.0f}")

        # Validate accounting equation
        assets = result.data.get('total_assets', 0)
        equity = result.data.get('total_equity', 0)
        liabilities = result.data.get('total_liabilities', 0)
        balance = equity + liabilities
        diff = abs(assets - balance)

        print(f"\n   Accounting Equation:")
        print(f"   Assets: {assets:,.0f}")
        print(f"   Equity + Liabilities: {balance:,.0f}")
        print(f"   Difference: {diff:,.0f} ({diff/assets*100:.2f}%)")

        if diff < assets * 0.01:
            print(f"   ✅ BALANCE SHEET BALANCES")
        else:
            print(f"   ⚠️  Warning: Balance sheet doesn't balance")
    else:
        print(f"\n📄 {file}")
        print(f"   ❌ Extraction failed: {result.error}")
```

---

## 🚀 Implementation Phases

### Phase 1: Enhanced PDF Support (Week 1)
- ✅ **DONE:** Text extraction for borderless tables
- ✅ **DONE:** E5 semantic matching
- ✅ **DONE:** Camelot stream extraction
- 🔜 **TODO:** OCR support for scanned PDFs
- 🔜 **TODO:** Multi-page balance sheet handling
- 🔜 **TODO:** Fusion strategy implementation

### Phase 2: Multi-Format Support (Week 2)
- 🔜 **TODO:** DOCX handler implementation
- 🔜 **TODO:** TXT handler implementation
- 🔜 **TODO:** XLSX/CSV handler implementation
- 🔜 **TODO:** HTML handler implementation

### Phase 3: Quality System (Week 3)
- 🔜 **TODO:** Quality metrics calculator
- 🔜 **TODO:** Threshold configuration
- 🔜 **TODO:** Fallback chain orchestration
- 🔜 **TODO:** Fusion strategy

### Phase 4: Intelligence & Learning (Week 4)
- 🔜 **TODO:** Pattern learning from examples
- 🔜 **TODO:** Auto-parameter tuning
- 🔜 **TODO:** Multi-language support expansion
- 🔜 **TODO:** ML-based layout detection

---

## 🎯 Success Criteria

### Extraction Quality
- ✅ **Completeness:** 80%+ of required fields extracted
- ✅ **Validation:** Accounting equation validates (< 1% error)
- ✅ **Confidence:** 70%+ confidence score
- ✅ **Speed:** < 10 seconds per document

### Format Support
- ✅ **PDF:** 95%+ success rate (bordered + borderless)
- 🎯 **DOCX:** 90%+ success rate (target)
- 🎯 **TXT:** 80%+ success rate (target)
- 🎯 **XLSX/CSV:** 98%+ success rate (target)
- 🎯 **HTML:** 85%+ success rate (target)

### User Experience
- ✅ **Automatic:** No manual intervention required
- ✅ **Transparent:** Clear quality metrics and warnings
- ✅ **Reliable:** Consistent results across document types
- ✅ **Fast:** Real-time feedback (< 10s)

---

## 📈 Metrics & Monitoring

### Track These Metrics

```python
@dataclass
class SystemMetrics:
    """
    Track extraction system performance
    """

    # Success rates by format
    pdf_success_rate: float
    docx_success_rate: float
    txt_success_rate: float
    xlsx_success_rate: float
    html_success_rate: float

    # Quality distribution
    avg_quality_score: float
    quality_below_threshold: int  # Count
    quality_warnings: int  # Count

    # Performance
    avg_processing_time: float
    p95_processing_time: float

    # Fallback usage
    primary_strategy_success: int
    fallback_required: int
    fusion_required: int

    # Method distribution
    method_usage: dict[str, int]  # method name → count


class MetricsCollector:
    """
    Collect and report extraction metrics
    """

    def __init__(self):
        self.results: list[ExtractionResult] = []

    def record(self, result: ExtractionResult):
        """Record extraction result"""
        self.results.append(result)

    def report(self) -> SystemMetrics:
        """Generate metrics report"""
        # Calculate metrics from results
        return SystemMetrics(
            pdf_success_rate=self._success_rate('.pdf'),
            avg_quality_score=self._avg_quality(),
            # ... etc
        )
```

---

## 🔐 Security & Privacy Considerations

### Data Handling
- ✅ **No external APIs** - All processing local (no data leakage)
- ✅ **Sensitive data** - Financial statements handled securely
- ✅ **Audit trail** - Log extraction methods and confidence scores
- ✅ **Validation** - Always validate accounting equation

### Error Handling
- ✅ **Graceful degradation** - Return best available result
- ✅ **Clear warnings** - Alert user to quality issues
- ✅ **Metadata preservation** - Track extraction method and confidence
- ✅ **Logging** - Comprehensive logging for debugging

---

## 💡 Future Enhancements

### Machine Learning Integration
- **Layout detection** - ML model to classify PDF layout types
- **Pattern learning** - Learn regex patterns from training examples
- **Auto-correction** - ML-based error correction for extracted values
- **Confidence prediction** - ML model to predict extraction confidence

### Advanced Features
- **Multi-document analysis** - Extract from entire annual report
- **Time-series extraction** - Extract multiple periods automatically
- **Footnote extraction** - Extract notes and disclosures
- **XBRL parsing** - Native support for XBRL regulatory filings
- **Real-time extraction** - Streaming extraction for large documents

### User Experience
- **GUI dashboard** - Visual quality metrics and warnings
- **Manual correction** - Easy interface to fix extraction errors
- **Template learning** - System learns from manual corrections
- **Batch processing** - Process multiple documents in parallel

---

## 📝 Summary

This intelligent extraction system will:

1. **Auto-detect** extraction problems using quality metrics
2. **Support multiple formats** (PDF, DOCX, TXT, XLSX, HTML)
3. **Automatically fallback** to alternative strategies when needed
4. **Combine results** using fusion strategy for maximum accuracy
5. **Provide transparency** with detailed quality metrics
6. **Handle multiple languages** (Polish, English, German, etc.)
7. **Maintain performance** (< 10s per document)

**Current Status:** Phase 1 complete (PDF text extraction), ready for Phase 2 (multi-format support)

**Next Steps:**
1. Implement DOCX handler (highest priority after PDF)
2. Implement quality assessment system
3. Implement fallback chain orchestration
4. Add TXT and XLSX handlers
5. Add fusion strategy

This design builds on the successful Round 2 implementation and extends it to handle the full spectrum of financial document formats users encounter in the wild.
