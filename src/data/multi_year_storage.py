"""
Simple JSON-based storage for multi-year financial data
No database needed - just JSON files
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class MultiYearDataStore:
    """
    Store multi-year financial data in JSON files

    File structure:
        data/companies/
        ├── grupa_azoty_sa.json
        ├── orlen_sa.json
        └── ...

    JSON format:
        {
            "company_name": "Grupa Azoty S.A.",
            "industry": "Chemicals & Fertilizers",
            "currency": "PLN",
            "data": {
                "2023": {
                    "Total Assets": 26019865,
                    "Current Assets": 7904016,
                    ...
                },
                "2022": {...},
                "2021": {...}
            }
        }
    """

    def __init__(self, storage_dir: str = "data/companies"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"MultiYearDataStore initialized: {self.storage_dir}")

    def save_company_data(
        self,
        company_name: str,
        industry: str,
        currency: str,
        years_data: Dict[int, Dict[str, float]]
    ):
        """
        Save multi-year data for a company

        Args:
            company_name: Company name (e.g., "Grupa Azoty S.A.")
            industry: Industry sector
            currency: Currency code (e.g., "PLN")
            years_data: {
                2023: {'Total Assets': 26019865, 'Current Assets': 7904016, ...},
                2022: {'Total Assets': 25000000, ...},
                ...
            }
        """
        # Sanitize company name for filename
        safe_name = self._sanitize_filename(company_name)
        filepath = self.storage_dir / f"{safe_name}.json"

        # Load existing if present
        if filepath.exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                existing = json.load(f)
        else:
            existing = {
                "company_name": company_name,
                "industry": industry,
                "currency": currency,
                "data": {}
            }

        # Merge new data
        for year, data in years_data.items():
            existing["data"][str(year)] = data

        # Save
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(existing, f, indent=2, ensure_ascii=False)

        logger.info(f"Saved data for {company_name}: {len(years_data)} years to {filepath}")

    def load_company_data(
        self,
        company_name: str
    ) -> Optional[Dict]:
        """
        Load multi-year data for a company

        Args:
            company_name: Company name

        Returns:
            {
                "company_name": "Grupa Azoty S.A.",
                "industry": "Chemicals & Fertilizers",
                "currency": "PLN",
                "balance_sheet": {
                    "Total Assets": {2023: 26019865, 2022: 25000000, ...},
                    "Current Assets": {2023: 7904016, 2022: 8000000, ...},
                    ...
                },
                "income_statement": {...},
                "cash_flow": {...}
            }
        """
        safe_name = self._sanitize_filename(company_name)
        filepath = self.storage_dir / f"{safe_name}.json"

        if not filepath.exists():
            logger.warning(f"No data found for {company_name} at {filepath}")
            return None

        with open(filepath, 'r', encoding='utf-8') as f:
            stored = json.load(f)

        # Convert to intelligence service format
        result = {
            "company_name": stored["company_name"],
            "industry": stored.get("industry", "Unknown"),
            "currency": stored.get("currency", "PLN"),
            "balance_sheet": {},
            "income_statement": {},
            "cash_flow": {}
        }

        # Transform year-first to metric-first format
        # From: {2023: {Total Assets: 26019865}, 2022: {...}}
        # To: {Total Assets: {2023: 26019865, 2022: ...}}
        all_metrics = set()
        for year_data in stored["data"].values():
            all_metrics.update(year_data.keys())

        for metric in all_metrics:
            # Determine which statement this metric belongs to
            category = self._categorize_metric(metric)

            if category not in result:
                result[category] = {}

            result[category][metric] = {}

            for year_str, year_data in stored["data"].items():
                if metric in year_data:
                    result[category][metric][int(year_str)] = year_data[metric]

        logger.info(f"Loaded {company_name}: {len(stored['data'])} years, {len(all_metrics)} metrics")
        return result

    def list_companies(self) -> List[str]:
        """
        List all companies with stored data

        Returns:
            List of company names
        """
        companies = []
        for json_file in self.storage_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    companies.append(data["company_name"])
            except Exception as e:
                logger.error(f"Error reading {json_file}: {e}")

        return sorted(companies)

    def get_years_available(self, company_name: str) -> List[int]:
        """
        Get list of years with data for a company

        Args:
            company_name: Company name

        Returns:
            Sorted list of years (e.g., [2020, 2021, 2022, 2023, 2024])
        """
        safe_name = self._sanitize_filename(company_name)
        filepath = self.storage_dir / f"{safe_name}.json"

        if not filepath.exists():
            return []

        with open(filepath, 'r', encoding='utf-8') as f:
            stored = json.load(f)

        years = [int(year) for year in stored["data"].keys()]
        return sorted(years)

    def _sanitize_filename(self, company_name: str) -> str:
        """
        Convert company name to safe filename

        Args:
            company_name: "Grupa Azoty S.A." or "PKN ORLEN S.A."

        Returns:
            "grupa_azoty_sa" or "pkn_orlen_sa"
        """
        # Remove special characters, convert to lowercase
        safe = company_name.lower()
        safe = safe.replace(".", "")
        safe = safe.replace(",", "")
        safe = safe.replace(" ", "_")
        safe = safe.replace("-", "_")
        safe = safe.replace("__", "_")
        return safe.strip("_")

    def _categorize_metric(self, metric: str) -> str:
        """
        Categorize a metric into balance_sheet, income_statement, or cash_flow

        Args:
            metric: Metric name (e.g., "Total Assets", "Revenue", "Operating Cash Flow")

        Returns:
            "balance_sheet", "income_statement", or "cash_flow"
        """
        metric_lower = metric.lower()

        # Balance sheet keywords
        balance_sheet_keywords = [
            'assets', 'liabilities', 'equity', 'capital', 'reserves',
            'inventories', 'receivables', 'payables', 'cash', 'debt'
        ]

        # Income statement keywords
        income_keywords = [
            'revenue', 'sales', 'income', 'profit', 'loss', 'margin',
            'ebitda', 'ebit', 'expense', 'cost', 'earnings', 'eps'
        ]

        # Cash flow keywords
        cash_flow_keywords = [
            'cash flow', 'operating cash', 'investing cash', 'financing cash',
            'free cash flow', 'capex', 'dividends paid'
        ]

        # Check keywords
        for keyword in cash_flow_keywords:
            if keyword in metric_lower:
                return 'cash_flow'

        for keyword in income_keywords:
            if keyword in metric_lower:
                return 'income_statement'

        for keyword in balance_sheet_keywords:
            if keyword in metric_lower:
                return 'balance_sheet'

        # Default to balance sheet
        return 'balance_sheet'


# Helper functions for easy usage
def save_extraction_result(
    company_name: str,
    industry: str,
    currency: str,
    year: int,
    extracted_data: Dict[str, float]
):
    """
    Save extracted financial data for a single year

    Args:
        company_name: Company name
        industry: Industry sector
        currency: Currency code
        year: Year
        extracted_data: Dict of metric → value
    """
    store = MultiYearDataStore()
    store.save_company_data(
        company_name=company_name,
        industry=industry,
        currency=currency,
        years_data={year: extracted_data}
    )


def load_for_intelligence_report(company_name: str) -> Optional[Dict]:
    """
    Load company data in format ready for intelligence report generation

    Args:
        company_name: Company name

    Returns:
        Dict ready for LocalIntelligenceService.generate_intelligence_report()
    """
    store = MultiYearDataStore()
    return store.load_company_data(company_name)
