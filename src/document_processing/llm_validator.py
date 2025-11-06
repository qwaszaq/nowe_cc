"""
LLM Validator for Financial Data Extraction

Uses local LLM (via LM Studio) to validate extracted values and provide
additional parsing for complex cases.

Author: Destiny Team
Date: 2025-11-06
"""

import logging
from typing import Dict, List, Optional, Any
import urllib.request
import urllib.error
import json
import re

logger = logging.getLogger(__name__)


class LLMFinancialValidator:
    """
    Use local LLM to validate and enhance financial data extraction
    """

    def __init__(
        self,
        base_url: str = "http://192.168.200.226:1234/v1",
        model: str = "openai/gpt-oss-20b",
        temperature: float = 0.1,  # Low temp for consistent validation
        timeout: int = 30
    ):
        """
        Initialize LLM validator

        Args:
            base_url: LM Studio API endpoint
            model: LLM model to use
            temperature: Sampling temperature (low for validation)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.temperature = temperature
        self.timeout = timeout

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 500
    ) -> Optional[str]:
        """
        Call LLM for chat completion

        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Maximum tokens in response

        Returns:
            Response text or None if failed
        """
        try:
            url = f"{self.base_url}/chat/completions"

            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": max_tokens
            }

            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )

            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                result = json.loads(response.read().decode('utf-8'))

                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content']
                else:
                    logger.warning("No completion returned from LLM")
                    return None

        except Exception as e:
            logger.error(f"LLM completion failed: {e}")
            return None

    def validate_accounting_equation(
        self,
        total_assets: float,
        total_equity: float,
        total_liabilities: float
    ) -> Dict[str, Any]:
        """
        Validate accounting equation: Assets = Equity + Liabilities

        Uses LLM to assess if small differences are acceptable.

        Args:
            total_assets: Total assets value
            total_equity: Total equity value
            total_liabilities: Total liabilities value

        Returns:
            Validation result dict
        """
        difference = total_assets - (total_equity + total_liabilities)
        diff_percent = abs(difference / total_assets * 100) if total_assets != 0 else 0

        # Simple validation (no LLM needed if perfect)
        if difference == 0:
            return {
                'valid': True,
                'difference': 0,
                'difference_percent': 0.0,
                'explanation': 'Perfect balance',
                'llm_used': False
            }

        # Small difference - use LLM to assess
        if diff_percent < 5:  # Less than 5% difference
            messages = [
                {
                    "role": "system",
                    "content": "You are a financial auditor validating balance sheet data."
                },
                {
                    "role": "user",
                    "content": f"""Validate this accounting equation:

Total Assets: {total_assets:,.0f}
Total Equity: {total_equity:,.0f}
Total Liabilities: {total_liabilities:,.0f}

Equity + Liabilities = {total_equity + total_liabilities:,.0f}
Difference: {difference:,.0f} ({diff_percent:.2f}%)

Is this difference acceptable? Answer with just YES or NO and a brief reason."""
                }
            ]

            llm_response = self.chat_completion(messages, max_tokens=100)

            if llm_response:
                is_valid = 'YES' in llm_response.upper() or 'ACCEPTABLE' in llm_response.upper()
                return {
                    'valid': is_valid,
                    'difference': difference,
                    'difference_percent': diff_percent,
                    'explanation': llm_response.strip(),
                    'llm_used': True
                }

        # Significant difference or LLM failed
        return {
            'valid': False,
            'difference': difference,
            'difference_percent': diff_percent,
            'explanation': f'Difference too large: {diff_percent:.2f}%',
            'llm_used': False
        }

    def extract_value_from_text(
        self,
        text: str,
        field_name: str,
        context: Optional[str] = None
    ) -> Optional[float]:
        """
        Use LLM to extract a specific financial value from text

        Useful when regex patterns fail.

        Args:
            text: Text containing the value
            field_name: Name of the field to extract (e.g., "Total Assets")
            context: Optional context about the document

        Returns:
            Extracted value or None if failed
        """
        messages = [
            {
                "role": "system",
                "content": "You are a financial data extraction specialist. Extract exact numeric values from financial documents."
            },
            {
                "role": "user",
                "content": f"""Extract the value for "{field_name}" from this text:

{text[:1000]}

Return ONLY the numeric value (no currency, no commas, just the number).
If the value is in thousands, return the actual thousands value.
If not found, return "NOT FOUND"."""
            }
        ]

        if context:
            messages[1]['content'] += f"\n\nContext: {context}"

        llm_response = self.chat_completion(messages, max_tokens=50)

        if llm_response:
            # Try to parse number from response
            llm_response = llm_response.strip()

            if 'NOT FOUND' in llm_response.upper():
                return None

            # Extract first number found
            numbers = re.findall(r'[-+]?\d+(?:\.\d+)?', llm_response.replace(',', ''))

            if numbers:
                try:
                    return float(numbers[0])
                except ValueError:
                    pass

        return None

    def validate_financial_ratios(
        self,
        data: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Use LLM to assess if financial ratios are reasonable

        Args:
            data: Dict of extracted financial values

        Returns:
            Validation result with LLM assessment
        """
        # Calculate key ratios
        ratios_text = []

        if 'current_assets' in data and 'current_liabilities' in data and data['current_liabilities'] != 0:
            current_ratio = data['current_assets'] / data['current_liabilities']
            ratios_text.append(f"Current Ratio: {current_ratio:.2f}")

        if 'total_liabilities' in data and 'total_equity' in data and data['total_equity'] != 0:
            debt_to_equity = data['total_liabilities'] / data['total_equity']
            ratios_text.append(f"Debt-to-Equity: {debt_to_equity:.2f}")

        if not ratios_text:
            return {'valid': True, 'warnings': [], 'llm_used': False}

        messages = [
            {
                "role": "system",
                "content": "You are a financial analyst evaluating company health."
            },
            {
                "role": "user",
                "content": f"""Assess these financial ratios for a Polish chemical manufacturing company:

{chr(10).join(ratios_text)}

Are these ratios reasonable? Identify any red flags.
Answer in 2-3 sentences."""
            }
        ]

        llm_response = self.chat_completion(messages, max_tokens=200)

        warnings = []
        if llm_response:
            # Check for warning keywords
            warning_keywords = ['concern', 'risk', 'warning', 'problem', 'low', 'high', 'distress']
            if any(kw in llm_response.lower() for kw in warning_keywords):
                warnings.append(llm_response.strip())

        return {
            'valid': True,
            'warnings': warnings,
            'llm_assessment': llm_response.strip() if llm_response else None,
            'llm_used': True
        }

    def cross_validate_values(
        self,
        extracted_values: Dict[str, float],
        text_chunks: List[str]
    ) -> Dict[str, Any]:
        """
        Use LLM to cross-validate extracted values against source text

        Args:
            extracted_values: Dict of field → value
            text_chunks: List of text chunks from the document

        Returns:
            Validation result with confidence scores
        """
        # Build validation prompt
        values_text = "\n".join([f"{k}: {v:,.0f}" for k, v in extracted_values.items()])

        # Use first 2000 chars of text chunks
        context = "\n".join(text_chunks)[:2000]

        messages = [
            {
                "role": "system",
                "content": "You are validating extracted financial data against source text."
            },
            {
                "role": "user",
                "content": f"""Extracted values:
{values_text}

Source text:
{context}

Are these values consistent with the source text? Rate confidence 0-100%.
Answer format: "Confidence: XX% - Brief explanation" """
            }
        ]

        llm_response = self.chat_completion(messages, max_tokens=150)

        if llm_response:
            # Try to extract confidence percentage
            confidence_match = re.search(r'(\d+)%', llm_response)

            if confidence_match:
                confidence = int(confidence_match.group(1))
                return {
                    'confidence': confidence,
                    'explanation': llm_response.strip(),
                    'llm_used': True
                }

        return {
            'confidence': 50,  # Default middle ground
            'explanation': 'LLM validation failed',
            'llm_used': False
        }


# Standalone test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    validator = LLMFinancialValidator()

    print("\n" + "=" * 80)
    print("TESTING LLM FINANCIAL VALIDATOR")
    print("=" * 80)

    # Test 1: Validate accounting equation
    print("\n1. Testing Accounting Equation Validation:")
    result = validator.validate_accounting_equation(
        total_assets=26_019_865,
        total_equity=8_795_144,
        total_liabilities=17_224_721
    )
    print(f"   Valid: {result['valid']}")
    print(f"   Difference: {result['difference']:,.0f}")
    print(f"   Explanation: {result['explanation']}")

    # Test 2: Validate financial ratios
    print("\n2. Testing Financial Ratios Assessment:")
    data = {
        'current_assets': 7_904_016,
        'current_liabilities': 11_330_491,
        'total_liabilities': 17_224_721,
        'total_equity': 8_795_144
    }
    result = validator.validate_financial_ratios(data)
    print(f"   Valid: {result['valid']}")
    print(f"   Warnings: {len(result['warnings'])}")
    if result.get('llm_assessment'):
        print(f"   Assessment: {result['llm_assessment']}")

    print("=" * 80)
