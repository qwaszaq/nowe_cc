"""
Document loader for RAG system
Loads and chunks PDFs for embedding
"""

from pathlib import Path
from typing import List, Dict, Any
import logging
from dataclasses import dataclass
import re

logger = logging.getLogger(__name__)


@dataclass
class DocumentChunk:
    """Document chunk with metadata"""
    content: str
    metadata: Dict[str, Any]
    chunk_index: int
    section_type: str = "unknown"  # Detected section type


class DocumentLoader:
    """
    Load and chunk company documents for RAG

    Uses simple text splitting (no complex dependencies like langchain)
    """

    def __init__(
        self,
        chunk_size: int = 750,
        chunk_overlap: int = 100
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Section detection patterns (Polish and English)
        self.section_patterns = {
            "financial_statements": [
                r'(?i)(bilans|balance\s+sheet|sprawozdanie\s+z\s+sytuacji\s+finansowej)',
                r'(?i)(rachunek\s+zysków|income\s+statement|sprawozdanie\s+z\s+całkowitych\s+dochodów)',
                r'(?i)(cash\s+flow|przepływy\s+pieniężne)',
                r'(?i)(aktywa|pasywa|assets|liabilities|kapitał\s+własny|equity)'
            ],
            "management_discussion": [
                r'(?i)(zarząd|management|dyskusja\s+i\s+analiza|md&a)',
                r'(?i)(komentarz\s+zarządu|management.*discussion)',
                r'(?i)(sytuacja\s+finansowa|financial\s+position)',
                r'(?i)(wyniki\s+finansowe|financial\s+results)'
            ],
            "risk_factors": [
                r'(?i)(ryzyko|risk\s+factors?|czynniki\s+ryzyka)',
                r'(?i)(zagrożenia|threats|niepewność|uncertainty)',
                r'(?i)(ryzyko\s+kredytowe|credit\s+risk|ryzyko\s+rynkowe|market\s+risk)',
                r'(?i)(ryzyko\s+płynności|liquidity\s+risk)'
            ],
            "strategy": [
                r'(?i)(strategia|strategy|cele\s+strategiczne|strategic\s+objectives)',
                r'(?i)(plany\s+rozwoju|development\s+plans|wzrost|growth)',
                r'(?i)(inicjatywy|initiatives|projekty|projects)',
                r'(?i)(inwestycje|investments|nakłady|expenditures)'
            ],
            "operations": [
                r'(?i)(działalność\s+operacyjna|operations|produkcja|production)',
                r'(?i)(sprzedaż|sales|przychody|revenue)',
                r'(?i)(segment|dywizja|division)',
                r'(?i)(koszty\s+operacyjne|operating\s+costs)'
            ],
            "notes": [
                r'(?i)(nota\s+\d+|note\s+\d+|przypisy|notes)',
                r'(?i)(polityka\s+rachunkowości|accounting\s+policies)',
                r'(?i)(zasady\s+rachunkowości|accounting\s+principles)'
            ]
        }

        logger.info(f"DocumentLoader initialized: chunk_size={chunk_size}, overlap={chunk_overlap}")

    def load_annual_report(
        self,
        pdf_path: Path,
        company: str,
        year: int,
        document_type: str = "annual_report"
    ) -> List[DocumentChunk]:
        """
        Load and chunk annual report PDF

        Args:
            pdf_path: Path to PDF
            company: Company name
            year: Report year
            document_type: Type of document

        Returns:
            List of DocumentChunk objects
        """
        logger.info(f"Loading {document_type} for {company} ({year}): {pdf_path.name}")

        try:
            # Extract text using pdfplumber (you already have this)
            import pdfplumber

            all_text = []
            page_mapping = []  # Track which chunk came from which page

            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, start=1):
                    page_text = page.extract_text()

                    if not page_text:
                        continue

                    # Clean text
                    page_text = self._clean_text(page_text)
                    all_text.append(page_text)
                    page_mapping.append((page_num, len(page_text)))

            # Combine all text
            full_text = "\n\n".join(all_text)

            # Chunk the text
            chunks = self._chunk_text(full_text)

            # Create DocumentChunk objects with section detection
            document_chunks = []
            for chunk_idx, chunk_text in enumerate(chunks):
                # Determine which page this chunk is from (approximate)
                page_num = self._estimate_page_number(chunk_idx, len(chunks), len(page_mapping))

                # Detect section type
                section_type = self._detect_section_type(chunk_text)

                chunk = DocumentChunk(
                    content=chunk_text,
                    metadata={
                        "company": company,
                        "year": year,
                        "document_type": document_type,
                        "source_file": pdf_path.name,
                        "page": page_num,
                        "total_pages": len(page_mapping),
                        "chunk_size": len(chunk_text),
                        "section_type": section_type
                    },
                    chunk_index=chunk_idx,
                    section_type=section_type
                )
                document_chunks.append(chunk)

            # Log section distribution
            section_counts = {}
            for chunk in document_chunks:
                section_type = chunk.section_type
                section_counts[section_type] = section_counts.get(section_type, 0) + 1

            logger.info(f"Section distribution: {section_counts}")

            logger.info(f"Loaded {len(document_chunks)} chunks from {len(page_mapping)} pages")
            return document_chunks

        except Exception as e:
            logger.error(f"Failed to load document: {e}", exc_info=True)
            return []

    def load_multiple_reports(
        self,
        pdf_paths: Dict[int, Path],
        company: str
    ) -> List[DocumentChunk]:
        """
        Load multiple years of reports

        Args:
            pdf_paths: {2023: Path(...), 2022: Path(...), ...}
            company: Company name

        Returns:
            Combined list of all document chunks
        """
        all_chunks = []

        for year in sorted(pdf_paths.keys()):
            pdf_path = pdf_paths[year]
            logger.info(f"Loading {year} report...")

            chunks = self.load_annual_report(pdf_path, company, year)
            all_chunks.extend(chunks)

        logger.info(f"Loaded {len(all_chunks)} total chunks across {len(pdf_paths)} years")
        return all_chunks

    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        # Remove excessive whitespace
        text = " ".join(text.split())

        # Remove page numbers (common patterns)
        text = re.sub(r'\b\d+\s*/\s*\d+\b', '', text)
        text = re.sub(r'\bPage\s+\d+\b', '', text, flags=re.IGNORECASE)

        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    def _chunk_text(self, text: str) -> List[str]:
        """
        Chunk text with overlap using simple sentence-based splitting

        Args:
            text: Full text to chunk

        Returns:
            List of text chunks
        """
        # Split into sentences (simple approach)
        sentences = self._split_sentences(text)

        chunks = []
        current_chunk = []
        current_length = 0

        for sentence in sentences:
            sentence_length = len(sentence)

            # If adding this sentence exceeds chunk size, save current chunk
            if current_length + sentence_length > self.chunk_size and current_chunk:
                chunks.append(" ".join(current_chunk))

                # Overlap: keep last few sentences
                overlap_sentences = self._get_overlap_sentences(current_chunk)
                current_chunk = overlap_sentences
                current_length = sum(len(s) for s in current_chunk)

            current_chunk.append(sentence)
            current_length += sentence_length

        # Add final chunk
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def _split_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences (simple approach)

        Args:
            text: Text to split

        Returns:
            List of sentences
        """
        # Simple sentence splitting on . ! ?
        sentences = re.split(r'[.!?]+\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    def _get_overlap_sentences(self, sentences: List[str]) -> List[str]:
        """
        Get sentences for overlap based on chunk_overlap setting

        Args:
            sentences: List of sentences in current chunk

        Returns:
            Last N sentences that fit within overlap size
        """
        overlap_sentences = []
        overlap_length = 0

        # Take sentences from the end until we reach overlap size
        for sentence in reversed(sentences):
            sentence_length = len(sentence)

            if overlap_length + sentence_length > self.chunk_overlap:
                break

            overlap_sentences.insert(0, sentence)
            overlap_length += sentence_length

        return overlap_sentences

    def _estimate_page_number(
        self,
        chunk_index: int,
        total_chunks: int,
        total_pages: int
    ) -> int:
        """
        Estimate which page a chunk came from

        Args:
            chunk_index: Index of current chunk
            total_chunks: Total number of chunks
            total_pages: Total number of pages in document

        Returns:
            Estimated page number
        """
        # Simple linear estimation
        if total_chunks == 0:
            return 1

        estimated_page = int((chunk_index / total_chunks) * total_pages) + 1
        return min(estimated_page, total_pages)

    def _detect_section_type(self, text: str) -> str:
        """
        Detect section type based on content patterns

        Args:
            text: Chunk text

        Returns:
            Section type string
        """
        # Check each section type's patterns
        for section_type, patterns in self.section_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    return section_type

        # Default to unknown
        return "unknown"
