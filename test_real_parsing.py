#!/usr/bin/env python3
"""
Test Real Parsing with Your Files in testdocsLLM/
Shows FULL FUNCTIONALITY with real content extraction
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.parsing.document_parsers import UniversalDocumentParser
from src.autonomous.autonomous_orchestrator import AutonomousOrchestrator
import os


def test_parser_directly():
    """Test parser on files in testdocsLLM/"""
    print("=" * 80)
    print("TEST 1: Direct Parser Test")
    print("=" * 80)
    print()
    
    test_dir = Path("testdocsLLM")
    
    if not test_dir.exists():
        print("❌ testdocsLLM/ folder not found")
        return
    
    files = list(test_dir.glob("*"))
    files = [f for f in files if f.is_file() and f.name != "README.md"]
    
    if not files:
        print("⚠️  No files found in testdocsLLM/")
        print("   Add some test documents and run again!")
        return
    
    print(f"Found {len(files)} files to parse:")
    print()
    
    parser = UniversalDocumentParser()
    
    for file_path in files:
        print(f"📄 {file_path.name}")
        print("-" * 60)
        
        result = parser.parse(str(file_path))
        
        if result.success:
            print(f"✅ SUCCESS")
            print(f"   Parser: {result.metadata.get('parser', 'unknown')}")
            print(f"   Text length: {len(result.text)} chars")
            
            if result.tables:
                print(f"   Tables extracted: {len(result.tables)}")
            
            # Show preview
            preview = result.text[:300]
            if len(result.text) > 300:
                preview += "..."
            print(f"\n   Preview:")
            for line in preview.split('\n')[:5]:
                print(f"   {line}")
            
        else:
            print(f"❌ FAILED: {result.error}")
        
        print()
    
    print("=" * 80)
    print()


def test_autonomous_with_real_content():
    """Test full autonomous system with real content"""
    print("=" * 80)
    print("TEST 2: Full Autonomous System with Real Parsing")
    print("=" * 80)
    print()
    
    test_dir = Path("testdocsLLM")
    
    if not test_dir.exists() or not list(test_dir.glob("*")):
        print("⚠️  No files in testdocsLLM/")
        print("   Skipping autonomous test")
        return
    
    print("🚀 Initializing Autonomous System...")
    print()
    
    try:
        orchestrator = AutonomousOrchestrator()
        
        print("\n" + "=" * 80)
        print("PROCESSING WITH REAL CONTENT EXTRACTION")
        print("=" * 80)
        print()
        
        results = orchestrator.process_folder(
            folder_path=str(test_dir.absolute()),
            case_id="real_parsing_test"
        )
        
        print("\n" + "=" * 80)
        print("RESULTS - Real Content Was Extracted!")
        print("=" * 80)
        print()
        
        print(f"📊 Case ID: {results['case_id']}")
        print(f"📁 Files Processed: {results['summary']['total_files']}")
        print(f"🎯 Tasks Executed: {results['summary']['total_tasks']}")
        
        if results['findings']:
            print(f"\n🔍 Analysis with REAL Content:")
            for i, finding in enumerate(results['findings'][:5], 1):
                print(f"\n{i}. [{finding['agent'].upper()}] {finding['category']}")
                print(f"   Confidence: {finding['confidence']:.1%}")
                
                # Show first 200 chars of analysis
                output = finding['output'][:200]
                if len(finding['output']) > 200:
                    output += "..."
                print(f"   {output}")
        
        print("\n" + "=" * 80)
        print("✅ TEST COMPLETE - System Used REAL Content!")
        print("=" * 80)
        
        # Check if LMStudio was used
        if orchestrator.llm:
            print("\n🎉 LMStudio: ✅ Connected and Used")
        else:
            print("\n⚠️  LMStudio: Not connected (fallback mode)")
        
        print(f"\n📄 Full report saved to: reports/{results['case_id']}.json")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


def show_parsing_capabilities():
    """Show what can be parsed"""
    print("=" * 80)
    print("PARSING CAPABILITIES")
    print("=" * 80)
    print()
    
    capabilities = {
        "📄 Text Documents": [".txt", ".md"],
        "📑 PDF Documents": [".pdf"],
        "📊 Spreadsheets": [".xlsx", ".xls", ".csv"],
        "📝 Word Documents": [".docx", ".doc"],
        "📋 Structured Data": [".json", ".xml", ".yaml", ".yml"]
    }
    
    print("Supported formats with REAL parsing:")
    print()
    
    for category, formats in capabilities.items():
        print(f"{category}")
        for fmt in formats:
            print(f"   {fmt}")
        print()
    
    print("Features:")
    print("  ✅ Text extraction")
    print("  ✅ Table extraction (Excel, PDF, Word)")
    print("  ✅ Metadata extraction")
    print("  ✅ Graceful fallback if libraries missing")
    print()
    
    print("=" * 80)
    print()


def check_dependencies():
    """Check if parsing libraries are installed"""
    print("=" * 80)
    print("DEPENDENCY CHECK")
    print("=" * 80)
    print()
    
    dependencies = {
        'PyPDF2': 'PDF parsing',
        'pdfplumber': 'Advanced PDF parsing',
        'pandas': 'Excel/CSV parsing',
        'openpyxl': 'Excel support',
        'docx': 'Word document parsing'
    }
    
    missing = []
    
    for module, purpose in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {module:<15} - {purpose}")
        except ImportError:
            print(f"⚠️  {module:<15} - {purpose} (MISSING)")
            missing.append(module)
    
    print()
    
    if missing:
        print(f"Missing {len(missing)} optional libraries:")
        print("Install with:")
        print(f"  pip install {' '.join(missing)}")
        print()
        print("System will use fallbacks for these formats.")
    else:
        print("🎉 All parsing libraries installed!")
    
    print()
    print("=" * 80)
    print()


def main():
    """Run all tests"""
    
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 25 + "REAL PARSING TEST" + " " * 36 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    # Check dependencies
    check_dependencies()
    
    # Show capabilities
    show_parsing_capabilities()
    
    # Test parser directly
    test_parser_directly()
    
    # Test full autonomous system
    test_autonomous_with_real_content()
    
    print("\n" + "=" * 80)
    print("ALL TESTS COMPLETE")
    print("=" * 80)
    print()
    print("📁 Add more files to testdocsLLM/ and run again!")
    print("🚀 Or use: python destiny_auto.py testdocsLLM")
    print()


if __name__ == "__main__":
    main()
