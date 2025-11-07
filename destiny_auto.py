#!/usr/bin/env python3
"""
DESTINY AUTO - Autonomous Document Analysis System
Simple CLI: Just point to a folder and let the agents do their work!

Usage:
    python destiny_auto.py /path/to/folder
    python destiny_auto.py /path/to/folder --case-id my_case
"""

import sys
import argparse
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from src.autonomous.autonomous_orchestrator import AutonomousOrchestrator


def print_banner():
    """Print welcome banner"""
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   ████████▄     ▄████████    ▄████████     ███      ▄█  ███▄▄▄█ ║
║   ███   ▀███   ███    ███   ███    ███ ▀█████████▄ ███  ███▀▀▀██║
║   ███    ███   ███    █▀    ███    █▀     ▀███▀▀██ ███▌ ███   █║
║   ███    ███  ▄███▄▄▄       ███            ███   ▀ ███▌ ███    ║
║   ███    ███ ▀▀███▀▀▀     ▀███████████     ███     ███▌ ███    ║
║   ███    ███   ███    █▄           ███     ███     ███  ███    ║
║   ███   ▄███   ███    ███    ▄█    ███     ███     ███  ███    ║
║   ████████▀    ██████████  ▄████████▀     ▄████▀   █▀    ▀█    ║
║                                                                  ║
║               AUTONOMOUS DOCUMENT ANALYSIS SYSTEM                ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝

    Just point to a folder → Agents analyze everything automatically!
    
""")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="DESTINY AUTO - Autonomous Document Analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a folder
  python destiny_auto.py /data/documents
  
  # Analyze with custom case ID
  python destiny_auto.py /data/case_001 --case-id case_001
  
  # Get help
  python destiny_auto.py --help

The system will:
  1. 🔍 Scan and classify all files
  2. 🧠 Decide what analysis to perform
  3. 🤖 Execute analysis with appropriate agents
  4. 📊 Generate comprehensive report
        """
    )
    
    parser.add_argument(
        'folder',
        help='Path to folder containing documents to analyze'
    )
    
    parser.add_argument(
        '--case-id',
        help='Case ID (default: auto-generated)',
        default=None
    )
    
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output'
    )
    
    parser.add_argument(
        '--no-banner',
        action='store_true',
        help='Skip banner'
    )
    
    args = parser.parse_args()
    
    # Print banner
    if not args.no_banner:
        print_banner()
    
    # Validate folder
    folder_path = Path(args.folder)
    if not folder_path.exists():
        print(f"❌ Error: Folder does not exist: {args.folder}")
        sys.exit(1)
    
    if not folder_path.is_dir():
        print(f"❌ Error: Not a directory: {args.folder}")
        sys.exit(1)
    
    try:
        # Create orchestrator
        orchestrator = AutonomousOrchestrator()
        
        # Process folder
        results = orchestrator.process_folder(
            str(folder_path.absolute()),
            case_id=args.case_id
        )
        
        # Print results
        print("\n" + "╔" + "=" * 78 + "╗")
        print("║" + " " * 30 + "FINAL RESULTS" + " " * 35 + "║")
        print("╚" + "=" * 78 + "╝")
        
        print(f"\n📊 Case ID: {results['case_id']}")
        print(f"📁 Folder: {results['folder']}")
        print(f"📄 Files Processed: {results['summary']['total_files']}")
        print(f"🎯 Tasks Executed: {results['summary']['total_tasks']}")
        print(f"✅ Successful Agents: {results['summary']['successful_agents']}")
        
        if results['summary']['total_files'] > 0:
            print(f"\n📚 Files by Type:")
            for file_type, count in results['summary']['files_by_type'].items():
                print(f"   - {file_type}: {count}")
        
        if results['findings']:
            print(f"\n🔍 Key Findings:")
            for i, finding in enumerate(results['findings'][:10], 1):
                confidence_bar = "█" * int(finding['confidence'] * 10)
                print(f"\n   {i}. [{finding['agent'].upper()}] {finding['category']}")
                print(f"      Confidence: {confidence_bar} {finding['confidence']:.1%}")
                print(f"      {finding['output'][:200]}...")
        
        print("\n" + "=" * 80)
        print("✅ ANALYSIS COMPLETE")
        print("=" * 80)
        print()
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        sys.exit(130)
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
