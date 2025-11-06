"""
Text Extraction Utilities

Common utilities for extracting structured information from text.

Author: Destiny Team
Date: 2025-11-06
"""

import re
from typing import List, Dict, Optional
from datetime import datetime


def extract_financial_numbers(text: str) -> List[Dict]:
    """
    Extract financial numbers with context

    Handles various formats:
    - 1 234,56 PLN (Polish format)
    - 1,234.56 USD (English format)
    - 1234567 (no formatting)
    - Numbers with units (tys., mln., thousands, millions)

    Returns:
        List of dicts with 'value', 'unit', 'currency', 'context'
    """
    results = []

    # Pattern for numbers with currency/unit
    patterns = [
        # Polish format: "1 234,56 mln PLN"
        r'([\d\s]+,\d{2})\s+(tys\.|mln\.|mld\.)?\s*(PLN|EUR|USD|zł)',

        # English format: "1,234.56 million USD"
        r'([\d,]+\.\d{2})\s+(thousand|million|billion)?\s*(PLN|EUR|USD)',

        # Simple: "1234567 PLN"
        r'(\d{4,})\s*(PLN|EUR|USD|zł)',
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            value_str = match.group(1)
            unit = match.group(2) if len(match.groups()) >= 2 else None
            currency = match.group(3) if len(match.groups()) >= 3 else None

            # Normalize value
            normalized = normalize_financial_number(value_str)

            if normalized is not None:
                # Extract context (80 chars before and after)
                start = max(0, match.start() - 80)
                end = min(len(text), match.end() + 80)
                context = text[start:end].strip()

                results.append({
                    'value': normalized,
                    'unit': unit,
                    'currency': currency,
                    'context': context,
                    'raw': match.group(0)
                })

    return results


def normalize_financial_number(value_str: str) -> Optional[float]:
    """
    Normalize various number formats to float

    Examples:
        "1 234,56" → 1234.56
        "1,234.56" → 1234.56
        "1234567" → 1234567.0
    """
    try:
        # Remove spaces
        cleaned = value_str.replace(' ', '').replace('\xa0', '')

        # Detect format
        if ',' in cleaned and '.' in cleaned:
            # Both comma and dot - determine which is decimal separator
            last_comma = cleaned.rfind(',')
            last_dot = cleaned.rfind('.')

            if last_comma > last_dot:
                # Comma is decimal separator (European): "1.234,56"
                cleaned = cleaned.replace('.', '').replace(',', '.')
            else:
                # Dot is decimal separator (US): "1,234.56"
                cleaned = cleaned.replace(',', '')

        elif ',' in cleaned:
            # Only comma - could be thousands or decimal
            # If 2 digits after comma, it's decimal
            if re.search(r',\d{2}$', cleaned):
                cleaned = cleaned.replace(',', '.')
            else:
                cleaned = cleaned.replace(',', '')

        # Convert to float
        return float(cleaned)

    except (ValueError, AttributeError):
        return None


def extract_dates(text: str) -> List[Dict]:
    """
    Extract dates from text

    Handles formats:
    - 2024-12-31
    - 31.12.2024
    - December 31, 2024
    - 31 grudnia 2024 (Polish)
    """
    results = []

    patterns = [
        # ISO format: 2024-12-31
        (r'\b(\d{4})-(\d{2})-(\d{2})\b', '%Y-%m-%d'),

        # European: 31.12.2024
        (r'\b(\d{1,2})\.(\d{1,2})\.(\d{4})\b', '%d.%m.%Y'),

        # US: 12/31/2024
        (r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b', '%m/%d/%Y'),
    ]

    for pattern, fmt in patterns:
        for match in re.finditer(pattern, text):
            date_str = match.group(0)

            try:
                date_obj = datetime.strptime(date_str, fmt)

                # Extract context
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].strip()

                results.append({
                    'date': date_obj,
                    'date_str': date_str,
                    'context': context
                })

            except ValueError:
                continue

    return results


def extract_percentages(text: str) -> List[Dict]:
    """
    Extract percentages from text

    Examples:
    - 15.5%
    - 15,5%
    - 15.5 percent
    """
    results = []

    patterns = [
        r'(\d+[,\.]\d+)\s*%',  # 15.5%
        r'(\d+)\s*%',           # 15%
        r'(\d+[,\.]\d+)\s+proc',  # 15.5 procent (Polish)
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            value_str = match.group(1)

            # Normalize
            normalized = normalize_financial_number(value_str)

            if normalized is not None:
                # Extract context
                start = max(0, match.start() - 60)
                end = min(len(text), match.end() + 60)
                context = text[start:end].strip()

                results.append({
                    'value': normalized,
                    'context': context,
                    'raw': match.group(0)
                })

    return results


def extract_company_names(text: str) -> List[str]:
    """
    Extract potential company names

    Looks for:
    - Names in all caps (GRUPA AZOTY)
    - Names with S.A., Sp. z o.o., Inc., Corp, etc.
    """
    companies = []

    patterns = [
        r'\b([A-ZĄĆĘŁŃÓŚŹŻ]{2,}(?:\s+[A-ZĄĆĘŁŃÓŚŹŻ]{2,})+)\s+S\.?A\.?',  # GRUPA AZOTY S.A.
        r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\s+Inc\.?',  # TechCorp Inc.
        r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\s+Corp\.?',  # TechCorp Corp.
        r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\s+Ltd\.?',  # TechCorp Ltd.
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, text):
            company = match.group(1).strip()
            if company and company not in companies:
                companies.append(company)

    return companies


def extract_section_by_keyword(text: str, keyword: str, max_lines: int = 50) -> Optional[str]:
    """
    Extract section of text around a keyword

    Useful for finding specific sections like "Revenue", "Balance Sheet", etc.

    Args:
        text: Full document text
        keyword: Keyword to search for (case insensitive)
        max_lines: Maximum lines to extract after keyword

    Returns:
        Extracted section text, or None if not found
    """
    lines = text.split('\n')

    for i, line in enumerate(lines):
        if keyword.lower() in line.lower():
            # Found keyword, extract this line + next N lines
            start = i
            end = min(i + max_lines, len(lines))

            section = '\n'.join(lines[start:end])
            return section

    return None


# Test
if __name__ == "__main__":
    print("Testing Text Extraction Utilities...")
    print("=" * 80)

    # Test financial number extraction
    test_text = """
    Przychody ze sprzedaży wyniosły 1 234,56 mln PLN w roku 2023.
    Operating revenue was 2,345.67 thousand USD.
    Total assets: 5678901 PLN.
    Zysk netto: 456,78 tys. EUR.
    """

    print("\n1. Financial Numbers:")
    numbers = extract_financial_numbers(test_text)
    for num in numbers:
        print(f"  {num['value']:>12.2f} {num['unit'] or '':<10s} {num['currency'] or '':<5s} | {num['context'][:50]}...")

    # Test percentage extraction
    test_percentages = """
    Marża operacyjna wzrosła do 15,5% w Q3 2024.
    Revenue growth was 23.4 percent year-over-year.
    """

    print("\n2. Percentages:")
    percentages = extract_percentages(test_percentages)
    for pct in percentages:
        print(f"  {pct['value']:>6.2f}% | {pct['context'][:60]}...")

    # Test company name extraction
    test_companies = """
    GRUPA AZOTY S.A. jest największym producentem.
    TechCorp Inc. announced merger with DataSystems Corp.
    """

    print("\n3. Company Names:")
    companies = extract_company_names(test_companies)
    for company in companies:
        print(f"  - {company}")

    # Test date extraction
    test_dates = """
    Report date: 2024-12-31
    Na dzień 31.12.2023 aktywa wyniosły...
    Filed on 12/31/2024.
    """

    print("\n4. Dates:")
    dates = extract_dates(test_dates)
    for date_info in dates:
        print(f"  {date_info['date'].strftime('%Y-%m-%d')} | {date_info['context'][:50]}...")

    print("\n✅ All tests complete")
