"""
Intelligent Extraction Manager

Orchestrates multi-source financial data extraction with automatic
fallbacks and quality assessment.

Author: Destiny Team
Date: 2025-11-06
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional
import time

from .intelligent_extractor import (
    ExtractionResult,
    QualityMetrics,
    QualityThresholds,
    QualityAssessor,
)
from .pdf_parser import PDFParser
from .docx_handler import DOCXExtractionStrategy
from .txt_handler import TXTExtractionStrategy
from .spreadsheet_handler import SpreadsheetExtractionStrategy
from .html_handler import HTMLExtractionStrategy

logger = logging.getLogger(__name__)


class IntelligentExtractionManager:
    """
    Orchestrate extraction with automatic fallbacks and quality validation
    """

    def __init__(self):
        # Initialize all handlers
        self.pdf_handler = PDFParser()
        self.docx_handler = DOCXExtractionStrategy()
        self.txt_handler = TXTExtractionStrategy()
        self.spreadsheet_handler = SpreadsheetExtractionStrategy()
        self.html_handler = HTMLExtractionStrategy()

        self.quality_assessor = QualityAssessor()

        # Handler mapping by file extension
        self.handlers = {
            '.pdf': self.pdf_handler,
            '.docx': self.docx_handler,
            '.txt': self.txt_handler,
            '.xlsx': self.spreadsheet_handler,
            '.csv': self.spreadsheet_handler,
            '.html': self.html_handler,
            '.htm': self.html_handler,
        }

    def extract(self, file_path: Path, enable_fallback: bool = True) -> ExtractionResult:
        """
        Main extraction entry point

        Args:
            file_path: Path to financial document
            enable_fallback: Whether to try fallback strategies on failure

        Returns:
            ExtractionResult with quality metrics
        """
        start_time = time.time()

        logger.info("=" * 80)
        logger.info(f"📄 INTELLIGENT EXTRACTION: {file_path.name}")
        logger.info("=" * 80)

        # Validate file exists
        if not isinstance(file_path, Path):
            file_path = Path(file_path)

        if not file_path.exists():
            return ExtractionResult(
                success=False,
                error=f"File not found: {file_path}"
            )

        # Get handler for file type
        handler = self._get_handler(file_path)
        if handler is None:
            return ExtractionResult(
                success=False,
                error=f"Unsupported file type: {file_path.suffix}"
            )

        # Primary extraction
        result = self._extract_with_handler(handler, file_path)

        # Assess quality
        metrics = self.quality_assessor.assess(result)
        result.quality_metrics = metrics
        metrics.processing_time = time.time() - start_time

        logger.info(f"\n📊 Quality Assessment:")
        logger.info(f"   Overall: {metrics.overall_score:.1%}")
        logger.info(f"   Completeness: {metrics.completeness_score:.1%} "
                   f"({metrics.required_fields_found}/{metrics.required_fields_total})")
        logger.info(f"   Validation: {metrics.validation_score:.1%}")
        logger.info(f"   Confidence: {metrics.confidence_score:.1%}")

        # Decision: Accept, Retry, or Fallback?
        if QualityThresholds.should_accept(metrics):
            logger.info(f"\n✅ EXTRACTION SUCCESSFUL")
            logger.info(f"   Method: {metrics.extraction_method}")
            logger.info(f"   Time: {metrics.processing_time:.2f}s")
            self._print_warnings(metrics)
            return result

        # Fallback chain
        if enable_fallback and file_path.suffix == '.pdf':
            logger.warning(f"\n⚠️  Quality insufficient ({metrics.overall_score:.1%}), trying fallbacks...")
            fallback_result = self._fallback_chain(file_path, handler, result)

            if fallback_result.quality_metrics.overall_score > metrics.overall_score:
                logger.info(f"\n✅ FALLBACK SUCCESSFUL")
                logger.info(f"   Method: {fallback_result.quality_metrics.extraction_method}")
                logger.info(f"   Quality improved: {metrics.overall_score:.1%} → {fallback_result.quality_metrics.overall_score:.1%}")
                return fallback_result

        # Return best result (even if below threshold)
        logger.warning(f"\n⚠️  All strategies exhausted. Best quality: {metrics.overall_score:.1%}")
        self._print_warnings(metrics)
        return result

    def _get_handler(self, file_path: Path):
        """Get appropriate handler for file type"""
        return self.handlers.get(file_path.suffix.lower())

    def _extract_with_handler(self, handler, file_path: Path) -> ExtractionResult:
        """Extract using specific handler"""
        try:
            if isinstance(handler, PDFParser):
                # PDFParser has different interface (returns Document)
                doc = handler.parse(str(file_path))
                return self._convert_pdf_document_to_result(doc)
            else:
                # Other handlers return ExtractionResult directly
                return handler.extract(file_path)
        except Exception as e:
            logger.error(f"   ❌ Extraction error: {e}")
            return ExtractionResult(
                success=False,
                error=f"Extraction error: {str(e)}"
            )

    def _convert_pdf_document_to_result(self, doc) -> ExtractionResult:
        """
        Convert PDFDocument to ExtractionResult

        Extract financial statement data from PDFDocument.financial_statements
        """
        if not doc or 'balance_sheet' not in doc.financial_statements:
            return ExtractionResult(
                success=False,
                error="No balance sheet found in PDF"
            )

        bs = doc.financial_statements['balance_sheet']
        data = {}

        # Extract values from balance sheet rows
        def find_value(label_search):
            """Find value by label substring"""
            for row in bs.rows:
                if not row or len(row) < 2:
                    continue
                label = str(row[0]).lower()
                if label_search.lower() in label:
                    value_str = str(row[1]).replace(' ', '').replace(',', '').replace('\xa0', '')
                    try:
                        return float(value_str)
                    except:
                        pass
            return None

        # Extract key values
        data['total_assets'] = find_value('aktywa razem')
        data['current_assets'] = find_value('aktywa obrotowe razem')
        data['fixed_assets'] = find_value('aktywa trwałe razem')
        data['total_equity'] = find_value('kapitał własny razem')
        data['total_liabilities'] = find_value('zobowiązania razem')
        data['current_liabilities'] = find_value('zobowiązania krótkoterminowe')
        data['cash'] = find_value('środki pieniężne')
        data['inventories'] = find_value('zapasy')

        # Remove None values
        data = {k: v for k, v in data.items() if v is not None}

        return ExtractionResult(
            success=True if data else False,
            data=data,
            metadata={
                'extraction_method': 'pdf_text_extraction',
                'page': bs.page,
                'rows': len(bs.rows),
            }
        )

    def _fallback_chain(self, file_path: Path, handler, initial_result: ExtractionResult) -> ExtractionResult:
        """
        Try alternative strategies for PDF files
        """
        # For PDFs, the PDFParser already has internal fallback (pdfplumber → Camelot → text)
        # Here we could try fusion or other advanced strategies

        # For now, return initial result
        # TODO: Implement fusion strategy
        return initial_result

    def _print_warnings(self, metrics: QualityMetrics):
        """Print quality warnings"""
        if QualityThresholds.should_warn(metrics):
            logger.warning(f"\n⚠️  QUALITY WARNINGS:")
            for warning in metrics.warnings:
                logger.warning(f"   - {warning}")

    def batch_extract(self, file_paths: list) -> Dict[str, ExtractionResult]:
        """
        Extract from multiple files

        Args:
            file_paths: List of file paths

        Returns:
            Dict mapping file_path → ExtractionResult
        """
        results = {}

        logger.info("=" * 80)
        logger.info(f"📦 BATCH EXTRACTION: {len(file_paths)} files")
        logger.info("=" * 80)

        for file_path in file_paths:
            if not isinstance(file_path, Path):
                file_path = Path(file_path)

            result = self.extract(file_path)
            results[str(file_path)] = result

        # Print summary
        logger.info("\n" + "=" * 80)
        logger.info("📊 BATCH EXTRACTION SUMMARY")
        logger.info("=" * 80)

        success_count = sum(1 for r in results.values() if r.success)
        total_count = len(results)

        logger.info(f"\nSuccess Rate: {success_count}/{total_count} ({success_count/total_count*100:.0f}%)")
        logger.info(f"\nResults by file:")

        for file_path, result in results.items():
            if result.success:
                metrics = result.quality_metrics
                logger.info(f"✅ {Path(file_path).name}")
                logger.info(f"   Quality: {metrics.overall_score:.1%}, "
                           f"Completeness: {metrics.completeness_score:.1%}, "
                           f"Method: {metrics.extraction_method}")
            else:
                logger.info(f"❌ {Path(file_path).name}")
                logger.info(f"   Error: {result.error}")

        return results


__all__ = ['IntelligentExtractionManager']
