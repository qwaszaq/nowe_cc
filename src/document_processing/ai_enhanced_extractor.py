"""
AI-Enhanced Financial Data Extractor

Combines E5 semantic matching + Local LLM validation for superior extraction quality.

This is the "premium" version that uses AI throughout the extraction pipeline.

Author: Destiny Team
Date: 2025-11-06
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
import time

from .pdf_parser import PDFParser
from .semantic_matcher import E5SemanticMatcher
from .llm_validator import LLMFinancialValidator
from .intelligent_extractor import ExtractionResult, QualityMetrics

logger = logging.getLogger(__name__)


class AIEnhancedExtractor:
    """
    AI-powered financial data extraction using E5 + LLM

    Pipeline:
    1. Extract tables from PDF (pdfplumber/Camelot)
    2. Use E5 to semantically match row labels to concepts
    3. Extract numeric values from matched rows
    4. Use LLM to validate and cross-check
    5. Return results with high confidence scores
    """

    def __init__(self):
        self.pdf_parser = PDFParser()
        self.semantic_matcher = E5SemanticMatcher()
        self.llm_validator = LLMFinancialValidator()

        # Preload E5 embeddings for speed
        logger.info("🔄 Initializing AI-Enhanced Extractor...")
        self.semantic_matcher.preload_concept_embeddings()
        logger.info("✅ AI-Enhanced Extractor ready")

    def extract(self, pdf_path: Path) -> ExtractionResult:
        """
        Extract financial data using E5 + LLM

        Args:
            pdf_path: Path to PDF file

        Returns:
            ExtractionResult with AI-enhanced quality metrics
        """
        start_time = time.time()

        logger.info("=" * 80)
        logger.info(f"🤖 AI-ENHANCED EXTRACTION: {pdf_path.name}")
        logger.info("=" * 80)

        # Step 1: Parse PDF
        logger.info("📄 Step 1: Parsing PDF...")
        try:
            doc = self.pdf_parser.parse(str(pdf_path))
        except Exception as e:
            logger.error(f"PDF parsing failed: {e}")
            return ExtractionResult(
                success=False,
                error=f"PDF parsing failed: {e}"
            )

        # Step 2: Find balance sheet tables
        logger.info("🔍 Step 2: Identifying balance sheet tables...")
        balance_sheet_tables = self._find_balance_sheet_tables(doc)

        if not balance_sheet_tables:
            logger.warning("No balance sheet tables found")
            return ExtractionResult(
                success=False,
                error="No balance sheet tables detected"
            )

        logger.info(f"Found {len(balance_sheet_tables)} potential balance sheet tables")

        # Step 3: Extract rows from best table
        logger.info("📊 Step 3: Extracting table rows...")
        best_table = balance_sheet_tables[0]  # Use highest scoring table
        rows = self._extract_rows_from_table(best_table)

        if not rows:
            logger.warning("No rows extracted from table")
            return ExtractionResult(
                success=False,
                error="Failed to extract rows from balance sheet"
            )

        logger.info(f"Extracted {len(rows)} rows")

        # Step 4: Use E5 to match rows to financial concepts
        logger.info("🧠 Step 4: Semantic matching with E5...")
        matches = self.semantic_matcher.match_table_rows(rows)

        if not matches:
            logger.warning("No semantic matches found")
            return ExtractionResult(
                success=False,
                error="E5 semantic matching found no financial concepts"
            )

        logger.info(f"Matched {len(matches)} financial concepts")

        # Step 5: Extract values from matched rows
        logger.info("💰 Step 5: Extracting numeric values...")
        extracted_data = self._extract_values_from_matches(matches, rows)

        logger.info(f"Extracted {len(extracted_data)} values")
        for key, value in extracted_data.items():
            logger.info(f"  {key}: {value:,.0f}")

        # Step 6: LLM validation
        logger.info("✅ Step 6: LLM validation...")
        validation_result = self._llm_validate(extracted_data, doc.full_text)

        # Step 7: Calculate quality metrics
        logger.info("📈 Step 7: Quality assessment...")
        quality_metrics = self._calculate_quality_metrics(
            extracted_data,
            matches,
            validation_result,
            time.time() - start_time
        )

        logger.info(f"\n{quality_metrics}")

        # Build result
        result = ExtractionResult(
            success=True,
            data=extracted_data,
            quality_metrics=quality_metrics,
            metadata={
                'extraction_method': 'ai_enhanced_e5_llm',
                'num_tables_analyzed': len(balance_sheet_tables),
                'num_rows_processed': len(rows),
                'num_e5_matches': len(matches),
                'llm_validation': validation_result
            }
        )

        logger.info("=" * 80)
        logger.info("✅ AI-ENHANCED EXTRACTION COMPLETE")
        logger.info("=" * 80)

        return result

    def _find_balance_sheet_tables(self, doc) -> List:
        """Find tables that look like balance sheets"""
        candidates = []

        for table in doc.tables:
            # Check if table has balance sheet keywords nearby
            score = 0

            if table.title:
                title_lower = table.title.lower()
                if any(kw in title_lower for kw in ['bilans', 'balance sheet', 'sytuacja finansowa']):
                    score += 10

            # Check row labels
            for row in table.rows[:10]:  # Check first 10 rows
                if row and len(row) > 0:
                    label = str(row[0]).lower()
                    if 'aktywa' in label or 'assets' in label:
                        score += 5
                    if 'pasywa' in label or 'liabilities' in label or 'equity' in label:
                        score += 5

            # Check numeric density
            total_cells = len(table.rows) * len(table.headers) if table.headers else 0
            if total_cells > 0:
                numeric_cells = sum(
                    1 for row in table.rows for cell in row
                    if cell and any(c.isdigit() for c in str(cell))
                )
                numeric_density = numeric_cells / total_cells
                score += numeric_density * 10

            if score > 5:
                candidates.append((score, table))

        # Sort by score descending
        candidates.sort(key=lambda x: x[0], reverse=True)

        return [table for score, table in candidates]

    def _extract_rows_from_table(self, table) -> List[Dict[str, Any]]:
        """Extract rows with labels and values from table"""
        rows = []

        for row_data in table.rows:
            if not row_data or len(row_data) < 2:
                continue

            # First column is usually the label
            label = str(row_data[0]).strip()

            # Rest are values
            values = []
            for cell in row_data[1:]:
                if cell and str(cell).strip():
                    values.append(str(cell).strip())

            if label and values:
                rows.append({
                    'label': label,
                    'values': values,
                    'raw_row': row_data
                })

        return rows

    def _extract_values_from_matches(
        self,
        matches: Dict[str, tuple],
        rows: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Extract numeric values from matched rows"""
        extracted = {}

        for concept_key, (row_label, confidence, row_index) in matches.items():
            # Get the row
            if row_index >= len(rows):
                continue

            row = rows[row_index]

            # Try to extract number from values
            for value_str in row['values']:
                number = self._parse_polish_number(value_str)

                if number is not None:
                    extracted[concept_key] = number
                    break

        return extracted

    def _parse_polish_number(self, value_str: str) -> Optional[float]:
        """Parse Polish number format (space separators, parentheses for negatives)"""
        import re

        # Remove non-numeric except digits, spaces, commas, periods, parentheses, minus
        value_str = re.sub(r'[^\d\s,.()\-]', '', value_str)

        # Check for parentheses (negative)
        is_negative = '(' in value_str and ')' in value_str

        # Remove parentheses
        value_str = value_str.replace('(', '').replace(')', '')

        # Remove spaces (thousand separators in Polish)
        value_str = value_str.replace(' ', '')

        # Replace comma with period for decimal (Polish uses comma)
        # But be careful: "1,234" might be 1234 or 1.234
        # We'll assume thousands use spaces, so comma is decimal
        value_str = value_str.replace(',', '.')

        # Try to convert
        try:
            number = float(value_str)
            return -number if is_negative else number
        except ValueError:
            return None

    def _llm_validate(
        self,
        extracted_data: Dict[str, float],
        full_text: str
    ) -> Dict[str, Any]:
        """Use LLM to validate extracted values"""
        validation = {
            'accounting_equation': None,
            'financial_ratios': None,
            'cross_validation': None
        }

        # Validate accounting equation if we have the values
        if all(k in extracted_data for k in ['total_assets', 'total_equity', 'total_liabilities']):
            validation['accounting_equation'] = self.llm_validator.validate_accounting_equation(
                extracted_data['total_assets'],
                extracted_data['total_equity'],
                extracted_data['total_liabilities']
            )

        # Validate financial ratios
        validation['financial_ratios'] = self.llm_validator.validate_financial_ratios(
            extracted_data
        )

        # Cross-validate against text (use first 3000 chars)
        text_chunks = [full_text[:3000]]
        validation['cross_validation'] = self.llm_validator.cross_validate_values(
            extracted_data,
            text_chunks
        )

        return validation

    def _calculate_quality_metrics(
        self,
        extracted_data: Dict[str, float],
        matches: Dict[str, tuple],
        validation_result: Dict[str, Any],
        processing_time: float
    ) -> QualityMetrics:
        """Calculate quality metrics for AI-enhanced extraction"""
        metrics = QualityMetrics()

        # Completeness
        required_fields = ['total_assets', 'current_assets', 'fixed_assets', 'total_equity',
                          'total_liabilities', 'current_liabilities', 'cash', 'inventories']
        fields_found = sum(1 for f in required_fields if f in extracted_data)
        metrics.required_fields_found = fields_found
        metrics.required_fields_total = len(required_fields)
        metrics.completeness_score = fields_found / len(required_fields)

        # Validation (accounting equation)
        if validation_result.get('accounting_equation'):
            acct_eq = validation_result['accounting_equation']
            metrics.accounting_equation_valid = acct_eq.get('valid', False)
            metrics.balance_diff = acct_eq.get('difference', 0)

            if metrics.accounting_equation_valid:
                metrics.validation_score = 1.0
            else:
                # Score based on % difference
                diff_pct = abs(acct_eq.get('difference_percent', 100))
                metrics.validation_score = max(0, 1.0 - (diff_pct / 100))

        # Confidence (from E5 semantic matching)
        if matches:
            confidences = [conf for _, conf, _ in matches.values()]
            avg_confidence = sum(confidences) / len(confidences)
            metrics.semantic_match_score = avg_confidence

            # Use cross-validation confidence if available
            cross_val = validation_result.get('cross_validation', {})
            if cross_val.get('llm_used'):
                llm_confidence = cross_val.get('confidence', 50) / 100.0
                # Combine E5 and LLM confidence
                metrics.confidence_score = (avg_confidence + llm_confidence) / 2
            else:
                metrics.confidence_score = avg_confidence

        # Overall score (weighted average)
        metrics.overall_score = (
            metrics.completeness_score * 0.35 +
            metrics.validation_score * 0.35 +
            metrics.confidence_score * 0.30
        )

        # Metadata
        metrics.extraction_method = 'ai_enhanced_e5_llm'
        metrics.processing_time = processing_time

        # Warnings
        if metrics.confidence_score < 0.70:
            metrics.warnings.append(f"Low confidence: {metrics.confidence_score:.1%} (expected 70%+)")

        if metrics.overall_score < 0.85:
            metrics.warnings.append(f"Quality below target: {metrics.overall_score:.1%} (target 85%+)")

        if validation_result.get('financial_ratios', {}).get('warnings'):
            for warning in validation_result['financial_ratios']['warnings']:
                metrics.warnings.append(f"LLM warning: {warning[:100]}")

        return metrics


# Test function
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    extractor = AIEnhancedExtractor()

    pdf_path = Path("data/documents/grupa_azoty_tarnow/grupa_azoty_tarnow_annual_2023.pdf")

    if pdf_path.exists():
        result = extractor.extract(pdf_path)

        print("\n" + "=" * 80)
        print("EXTRACTION RESULTS")
        print("=" * 80)

        if result.success:
            print("\n✅ SUCCESS")
            print(f"\nExtracted {len(result.data)} values:")
            for key, value in result.data.items():
                print(f"  {key:30s}: {value:>20,.2f}")

            if result.quality_metrics:
                print(f"\nQuality: {result.quality_metrics.overall_score:.1%}")
        else:
            print(f"\n❌ FAILED: {result.error}")
    else:
        print(f"PDF not found: {pdf_path}")
