#!/usr/bin/env python3
"""
Save Grupa Azoty 2023 data to multi-year storage
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data.multi_year_storage import save_extraction_result, MultiYearDataStore


def save_azoty_2023():
    """
    Save the verified Azoty 2023 data to JSON storage
    """
    print("=" * 80)
    print("SAVING GRUPA AZOTY 2023 DATA TO MULTI-YEAR STORAGE")
    print("=" * 80)
    print()

    # Data from LOCAL_EXTRACTION_RESULTS_2023.md (100% accurate)
    azoty_2023_data = {
        "Total Assets": 26019865,
        "Current Assets": 7904016,
        "Fixed Assets": 18115849,  # Derived
        "Total Equity": 8795144,
        "Total Liabilities": 17224721,
        "Current Liabilities": 11330491,
        "Long-term Liabilities": 5894230,  # Derived
        "Cash & Equivalents": 1405681,
        "Inventories": 2605887
    }

    print(f"Company: Grupa Azoty S.A.")
    print(f"Year: 2023")
    print(f"Metrics: {len(azoty_2023_data)}")
    print()

    # Save
    save_extraction_result(
        company_name="Grupa Azoty S.A.",
        industry="Chemicals & Fertilizers",
        currency="PLN",
        year=2023,
        extracted_data=azoty_2023_data
    )

    print("✅ Data saved successfully")
    print()

    # Verify
    store = MultiYearDataStore()
    loaded = store.load_company_data("Grupa Azoty S.A.")

    if loaded:
        print("Verification:")
        print(f"  Company: {loaded['company_name']}")
        print(f"  Industry: {loaded['industry']}")
        print(f"  Currency: {loaded['currency']}")
        print(f"  Years available: {store.get_years_available('Grupa Azoty S.A.')}")
        print(f"  Metrics in balance_sheet: {len(loaded['balance_sheet'])}")
        print()
        print("✅ Data verified and ready for multi-year analysis")
    else:
        print("❌ Verification failed")

    print()
    print("=" * 80)
    print(f"Stored at: data/companies/grupa_azoty_sa.json")
    print("=" * 80)


if __name__ == "__main__":
    save_azoty_2023()
