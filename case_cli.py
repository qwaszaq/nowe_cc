#!/usr/bin/env python3
"""
Case Management CLI
Easy command-line interface for managing analysis results
"""

import sys
import argparse
from pathlib import Path
from tabulate import tabulate
import json

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from src.storage.case_manager import CaseManager


def cmd_list(args):
    """List all cases"""
    manager = CaseManager()
    cases = manager.list_cases(status=args.status, limit=args.limit)
    
    if not cases:
        print("No cases found.")
        return
    
    # Prepare table
    table_data = []
    for case in cases:
        table_data.append([
            case['case_id'],
            case.get('status', 'N/A'),
            case.get('total_files', 0),
            case.get('created_at', 'N/A')[:19]  # Trim microseconds
        ])
    
    headers = ['Case ID', 'Status', 'Files', 'Created At']
    print("\n📋 Cases:")
    print(tabulate(table_data, headers=headers, tablefmt='grid'))
    print(f"\nTotal: {len(cases)} cases")


def cmd_show(args):
    """Show case details"""
    manager = CaseManager()
    case = manager.get_case(args.case_id)
    
    if not case:
        print(f"❌ Case not found: {args.case_id}")
        return
    
    print(f"\n📊 Case Details: {args.case_id}")
    print("=" * 70)
    
    # Basic info
    print(f"Status:       {case.get('status', 'N/A')}")
    print(f"Created:      {case.get('created_at', 'N/A')}")
    print(f"Updated:      {case.get('updated_at', 'N/A')}")
    print(f"Folder:       {case.get('folder_path', 'N/A')}")
    print(f"Total Files:  {case.get('total_files', 0)}")
    
    # Categories
    if 'categories' in case:
        print("\nCategories:")
        for cat, count in case['categories'].items():
            print(f"  - {cat}: {count}")
    
    # Show report if exists
    if args.report:
        report = manager.get_case_report(args.case_id, format='json')
        if report:
            report_data = json.loads(report)
            if 'findings' in report_data:
                print(f"\nFindings: {len(report_data['findings'])}")
                for i, finding in enumerate(report_data['findings'][:5], 1):
                    print(f"  {i}. [{finding['agent']}] {finding['category']} (confidence: {finding['confidence']:.0%})")
                if len(report_data['findings']) > 5:
                    print(f"  ... and {len(report_data['findings']) - 5} more")


def cmd_search(args):
    """Search cases"""
    manager = CaseManager()
    results = manager.search_cases(args.query)
    
    if not results:
        print(f"No cases found matching: {args.query}")
        return
    
    print(f"\n🔍 Search results for: '{args.query}'")
    table_data = []
    for case in results:
        table_data.append([
            case['case_id'],
            case.get('status', 'N/A'),
            case.get('total_files', 0)
        ])
    
    headers = ['Case ID', 'Status', 'Files']
    print(tabulate(table_data, headers=headers, tablefmt='simple'))
    print(f"\nFound: {len(results)} cases")


def cmd_report(args):
    """Get case report"""
    manager = CaseManager()
    report = manager.get_case_report(args.case_id, format=args.format)
    
    if not report:
        print(f"❌ Report not found: {args.case_id} (format: {args.format})")
        return
    
    if args.output:
        Path(args.output).write_text(report)
        print(f"✅ Report saved to: {args.output}")
    else:
        print(report)


def cmd_archive(args):
    """Archive a case"""
    manager = CaseManager()
    
    if not args.yes:
        response = input(f"Archive case '{args.case_id}'? [y/N]: ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
    
    archive_path = manager.archive_case(args.case_id)
    print(f"✅ Case archived: {archive_path}")


def cmd_stats(args):
    """Show statistics"""
    manager = CaseManager()
    stats = manager.get_statistics()
    
    print("\n📊 Statistics")
    print("=" * 70)
    print(f"Total Cases:  {stats['total_cases']}")
    print(f"Total Files:  {stats['total_files']}")
    
    print("\nBy Status:")
    for status, count in stats['by_status'].items():
        print(f"  - {status}: {count}")
    
    if args.detailed and 'by_date' in stats:
        print("\nBy Date (last 10 days):")
        dates = sorted(stats['by_date'].items(), reverse=True)[:10]
        for date, count in dates:
            print(f"  - {date}: {count}")


def cmd_create(args):
    """Create new case structure"""
    manager = CaseManager()
    
    metadata = {}
    if args.metadata:
        try:
            metadata = json.loads(args.metadata)
        except:
            print(f"⚠️  Invalid JSON metadata, ignoring")
    
    case_dir = manager.create_case(
        case_id=args.case_id,
        folder_path=args.folder,
        metadata=metadata
    )
    
    print(f"✅ Case created: {case_dir}")
    print("\nNext steps:")
    print(f"  1. Copy documents to: {case_dir}/input/documents/")
    print(f"  2. Run analysis: python destiny_auto.py {args.folder} --case-id {args.case_id}")


def main():
    parser = argparse.ArgumentParser(
        description="Destiny Case Management CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all cases
  python case_cli.py list
  
  # Show case details
  python case_cli.py show cba_analysis_2024
  
  # Search cases
  python case_cli.py search "CBA"
  
  # Get report
  python case_cli.py report cba_analysis_2024 --format md -o report.md
  
  # Archive case
  python case_cli.py archive old_case_001 --yes
  
  # Show statistics
  python case_cli.py stats --detailed
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all cases')
    list_parser.add_argument('--status', help='Filter by status')
    list_parser.add_argument('--limit', type=int, default=100, help='Max results')
    list_parser.set_defaults(func=cmd_list)
    
    # Show command
    show_parser = subparsers.add_parser('show', help='Show case details')
    show_parser.add_argument('case_id', help='Case ID')
    show_parser.add_argument('--report', action='store_true', help='Show report summary')
    show_parser.set_defaults(func=cmd_show)
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search cases')
    search_parser.add_argument('query', help='Search query')
    search_parser.set_defaults(func=cmd_search)
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Get case report')
    report_parser.add_argument('case_id', help='Case ID')
    report_parser.add_argument('--format', choices=['json', 'md', 'html'], default='json', help='Report format')
    report_parser.add_argument('-o', '--output', help='Output file')
    report_parser.set_defaults(func=cmd_report)
    
    # Archive command
    archive_parser = subparsers.add_parser('archive', help='Archive a case')
    archive_parser.add_argument('case_id', help='Case ID')
    archive_parser.add_argument('--yes', action='store_true', help='Skip confirmation')
    archive_parser.set_defaults(func=cmd_archive)
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show statistics')
    stats_parser.add_argument('--detailed', action='store_true', help='Show detailed stats')
    stats_parser.set_defaults(func=cmd_stats)
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create new case')
    create_parser.add_argument('case_id', help='Case ID')
    create_parser.add_argument('folder', help='Source folder path')
    create_parser.add_argument('--metadata', help='JSON metadata')
    create_parser.set_defaults(func=cmd_create)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        args.func(args)
    except Exception as e:
        print(f"❌ Error: {e}")
        if '--debug' in sys.argv:
            raise
        sys.exit(1)


if __name__ == "__main__":
    main()
