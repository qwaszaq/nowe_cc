#!/usr/bin/env python3
"""
Migrate Existing Results to New Structure
One-time script to move legacy reports to new case structure
"""

import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from src.storage.case_manager import CaseManager


def migrate_legacy_reports():
    """Migrate reports from reports/ to new cases/ structure"""
    
    manager = CaseManager()
    reports_dir = Path("reports")
    
    if not reports_dir.exists():
        print("❌ No reports/ directory found")
        return
    
    # Find all autonomous reports
    legacy_reports = list(reports_dir.glob("autonomous_*.json"))
    
    if not legacy_reports:
        print("ℹ️  No legacy reports found")
        return
    
    print(f"\n🔄 Found {len(legacy_reports)} legacy reports to migrate")
    print("=" * 70)
    
    migrated = 0
    skipped = 0
    failed = 0
    
    for report_file in legacy_reports:
        try:
            # Load report
            report = json.loads(report_file.read_text())
            case_id = report.get('case_id')
            
            if not case_id:
                print(f"⚠️  Skipping {report_file.name}: no case_id")
                skipped += 1
                continue
            
            # Check if already migrated
            if manager.get_case(case_id):
                print(f"⏭️  Skipping {case_id}: already exists")
                skipped += 1
                continue
            
            print(f"\n📦 Migrating: {case_id}")
            
            # Create case structure
            metadata = {
                "migrated_from": str(report_file),
                "migrated_at": datetime.now().isoformat(),
                "total_files": report.get('summary', {}).get('total_files', 0),
                "categories": report.get('summary', {}).get('files_by_type', {})
            }
            
            case_dir = manager.create_case(
                case_id=case_id,
                folder_path=report.get('folder', 'unknown'),
                metadata=metadata
            )
            
            # Save report
            manager.save_final_report(case_id, report, formats=['json', 'md', 'html'])
            
            # Save individual agent results
            if 'findings' in report:
                for finding in report['findings']:
                    agent_name = finding.get('agent', 'unknown')
                    manager.save_agent_result(case_id, agent_name, finding)
            
            print(f"  ✅ Migrated to: {case_dir}")
            migrated += 1
            
        except Exception as e:
            print(f"  ❌ Failed: {e}")
            failed += 1
            continue
    
    # Summary
    print("\n" + "=" * 70)
    print("Migration Summary:")
    print(f"  ✅ Migrated: {migrated}")
    print(f"  ⏭️  Skipped:  {skipped}")
    print(f"  ❌ Failed:   {failed}")
    print(f"  📊 Total:    {len(legacy_reports)}")
    
    if migrated > 0:
        print("\n💡 Tip: You can now use:")
        print("   python case_cli.py list")
        print("   python case_cli.py show <case_id>")


def main():
    print("=" * 70)
    print("MIGRATE LEGACY REPORTS TO NEW STRUCTURE")
    print("=" * 70)
    
    response = input("\nThis will migrate reports/ to cases/ structure. Continue? [y/N]: ")
    if response.lower() != 'y':
        print("Cancelled.")
        return
    
    migrate_legacy_reports()
    
    print("\n✅ Migration complete!")


if __name__ == "__main__":
    main()
