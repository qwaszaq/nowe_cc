"""
Document Downloader for Financial Reports

Downloads annual reports and other documents from company websites.
Focus: Grupa Azoty Tarnów (https://tarnow.grupaazoty.com/relacje-inwestorskie/raporty-okresowe)

Author: Destiny Team
Date: 2025-11-06
"""

import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class DocumentDownloader:
    """
    Download financial documents from company websites

    Features:
    - Scrape investor relations pages for PDF links
    - Download PDFs with progress tracking
    - Organize by company, year, report type
    - Resume interrupted downloads
    - Rate limiting to be polite
    """

    def __init__(self, download_dir: str = "data/documents"):
        """
        Initialize downloader

        Args:
            download_dir: Base directory for downloaded documents
        """
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)

        # HTTP session with headers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

        # Rate limiting
        self.last_request_time = 0
        self.min_delay = 1.0  # seconds between requests

    def _rate_limit(self):
        """Enforce rate limiting between requests"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_delay:
            time.sleep(self.min_delay - elapsed)
        self.last_request_time = time.time()

    def scrape_grupa_azoty_reports(self, url: str = "https://tarnow.grupaazoty.com/relacje-inwestorskie/raporty-okresowe") -> List[Dict]:
        """
        Scrape Grupa Azoty Tarnów investor relations page for PDF links

        Args:
            url: Investor relations URL

        Returns:
            List of document metadata dicts:
            {
                'title': 'Raport roczny 2023',
                'url': 'https://...',
                'filename': 'grupa_azoty_raport_2023.pdf',
                'year': 2023,
                'type': 'annual'
            }
        """
        logger.info(f"Scraping Grupa Azoty reports from {url}")

        self._rate_limit()

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all PDF links
            documents = []

            # Look for links containing "raport" (report) and ending in .pdf
            for link in soup.find_all('a', href=True):
                href = link['href']
                text = link.get_text(strip=True)

                # Check if it's a PDF
                if not (href.lower().endswith('.pdf') or '.pdf' in href.lower()):
                    continue

                # Check if it's a report
                if not any(keyword in text.lower() or keyword in href.lower()
                          for keyword in ['raport', 'sprawozdanie', 'report', 'annual']):
                    continue

                # Make absolute URL
                full_url = urljoin(url, href)

                # Extract year from text or filename
                year = self._extract_year(text + " " + href)

                # Determine report type
                report_type = self._classify_report_type(text + " " + href)

                # Generate filename
                filename = self._generate_filename("grupa_azoty_tarnow", report_type, year)

                documents.append({
                    'title': text,
                    'url': full_url,
                    'filename': filename,
                    'year': year,
                    'type': report_type,
                    'scraped_at': datetime.now().isoformat()
                })

            logger.info(f"Found {len(documents)} documents")
            return documents

        except requests.RequestException as e:
            logger.error(f"Failed to scrape {url}: {e}")
            return []

    def _extract_year(self, text: str) -> Optional[int]:
        """Extract 4-digit year from text"""
        import re
        match = re.search(r'\b(20\d{2})\b', text)
        return int(match.group(1)) if match else None

    def _classify_report_type(self, text: str) -> str:
        """
        Classify report type from title/filename

        Returns: 'annual', 'quarterly', 'monthly', 'other'
        """
        text_lower = text.lower()

        if any(word in text_lower for word in ['roczny', 'annual', 'roczne']):
            return 'annual'
        elif any(word in text_lower for word in ['kwartalny', 'quarterly', 'kwartalne', 'q1', 'q2', 'q3', 'q4']):
            return 'quarterly'
        elif any(word in text_lower for word in ['miesięczny', 'monthly']):
            return 'monthly'
        else:
            return 'other'

    def _generate_filename(self, company: str, report_type: str, year: Optional[int]) -> str:
        """Generate standardized filename"""
        company_slug = company.lower().replace(' ', '_')
        year_str = f"_{year}" if year else ""
        return f"{company_slug}_{report_type}{year_str}.pdf"

    def download_document(self, doc_metadata: Dict, company_dir: Optional[str] = None) -> Optional[str]:
        """
        Download a single document

        Args:
            doc_metadata: Document metadata from scrape_*_reports()
            company_dir: Subdirectory for company (default: extracted from metadata)

        Returns:
            Path to downloaded file, or None if failed
        """
        url = doc_metadata['url']
        filename = doc_metadata['filename']

        # Create company subdirectory
        if not company_dir:
            company_dir = "grupa_azoty_tarnow"

        save_dir = self.download_dir / company_dir
        save_dir.mkdir(parents=True, exist_ok=True)

        save_path = save_dir / filename

        # Check if already downloaded
        if save_path.exists():
            logger.info(f"Already downloaded: {filename}")
            return str(save_path)

        logger.info(f"Downloading {filename} from {url}")

        self._rate_limit()

        try:
            response = self.session.get(url, timeout=60, stream=True)
            response.raise_for_status()

            # Get file size
            total_size = int(response.headers.get('content-length', 0))

            # Download with progress
            downloaded = 0
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        # Log progress every 1MB
                        if downloaded % (1024 * 1024) < 8192 and total_size > 0:
                            percent = (downloaded / total_size) * 100
                            logger.info(f"  Progress: {percent:.1f}% ({downloaded / 1024 / 1024:.1f}MB)")

            logger.info(f"✅ Downloaded: {save_path}")
            return str(save_path)

        except Exception as e:
            logger.error(f"❌ Failed to download {url}: {e}")

            # Clean up partial download
            if save_path.exists():
                save_path.unlink()

            return None

    def download_all_reports(self, company: str = "grupa_azoty_tarnow",
                            filter_year: Optional[int] = None,
                            filter_type: Optional[str] = None) -> List[str]:
        """
        Download all reports from a company

        Args:
            company: Company identifier
            filter_year: Only download reports from this year
            filter_type: Only download reports of this type (annual, quarterly, etc.)

        Returns:
            List of paths to downloaded files
        """
        # Currently only supports Grupa Azoty Tarnów
        if company != "grupa_azoty_tarnow":
            raise ValueError(f"Unsupported company: {company}")

        # Scrape documents
        documents = self.scrape_grupa_azoty_reports()

        # Apply filters
        if filter_year:
            documents = [d for d in documents if d['year'] == filter_year]
            logger.info(f"Filtered to year {filter_year}: {len(documents)} documents")

        if filter_type:
            documents = [d for d in documents if d['type'] == filter_type]
            logger.info(f"Filtered to type '{filter_type}': {len(documents)} documents")

        # Download all
        downloaded_paths = []

        for i, doc in enumerate(documents, 1):
            logger.info(f"\n[{i}/{len(documents)}] {doc['title']}")

            path = self.download_document(doc, company_dir=company)

            if path:
                downloaded_paths.append(path)

        logger.info(f"\n✅ Downloaded {len(downloaded_paths)} / {len(documents)} documents")

        return downloaded_paths


# Test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    print("Testing Document Downloader...")
    print("=" * 80)

    downloader = DocumentDownloader()

    # Scrape Grupa Azoty reports
    print("\n1. Scraping Grupa Azoty Tarnów reports...")
    documents = downloader.scrape_grupa_azoty_reports()

    print(f"\nFound {len(documents)} documents:")
    for doc in documents[:5]:  # Show first 5
        print(f"  - {doc['year']} | {doc['type']:10s} | {doc['title'][:60]}")

    if len(documents) > 5:
        print(f"  ... and {len(documents) - 5} more")

    # Download annual reports only
    if documents:
        print("\n2. Downloading annual reports...")

        choice = input("\nDownload all annual reports? (y/n): ").lower()

        if choice == 'y':
            paths = downloader.download_all_reports(
                company="grupa_azoty_tarnow",
                filter_type="annual"
            )

            print(f"\n✅ Downloaded to: {downloader.download_dir / 'grupa_azoty_tarnow'}")
            print(f"   Files: {len(paths)}")
