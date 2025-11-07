"""
Case Manager - Centralized Results Storage
Manages the complete lifecycle of case results across all storage layers
"""

import json
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import hashlib


class CaseManager:
    """
    Manages case storage across file system and databases
    
    Features:
    - Creates case structure
    - Stores results in appropriate layers
    - Provides unified query interface
    - Handles archival and cleanup
    """
    
    def __init__(self, base_path: str = "cases"):
        """
        Initialize case manager
        
        Args:
            base_path: Base directory for cases (default: "cases")
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(exist_ok=True)
        
        # Create indexes
        self.index_file = self.base_path / "index.json"
        self._ensure_index()
    
    def _ensure_index(self):
        """Ensure index file exists"""
        if not self.index_file.exists():
            self._save_index({})
    
    def _load_index(self) -> Dict[str, Any]:
        """Load case index"""
        if self.index_file.exists():
            return json.loads(self.index_file.read_text())
        return {}
    
    def _save_index(self, index: Dict[str, Any]):
        """Save case index"""
        self.index_file.write_text(json.dumps(index, indent=2))
    
    def _update_index(self, case_id: str, metadata: Dict[str, Any]):
        """Update index with case metadata"""
        index = self._load_index()
        index[case_id] = {
            "case_id": case_id,
            "created_at": metadata.get("created_at", datetime.now().isoformat()),
            "status": metadata.get("status", "created"),
            "folder_path": metadata.get("folder_path", ""),
            "total_files": metadata.get("total_files", 0),
            "categories": metadata.get("categories", {}),
            "updated_at": datetime.now().isoformat()
        }
        self._save_index(index)
    
    def create_case(
        self,
        case_id: str,
        folder_path: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Path:
        """
        Create new case structure
        
        Args:
            case_id: Unique case identifier
            folder_path: Source folder path
            metadata: Optional case metadata
            
        Returns:
            Path to case directory
        """
        case_dir = self.base_path / case_id
        
        # Create directory structure
        structure = {
            "input": ["documents", "manifest.json", "checksums.txt"],
            "processing": ["extracted", "embeddings", "classifications", "tasks"],
            "results": ["agents", "visualizations"],
            "audit": [],
            "archives": []
        }
        
        for main_dir, subdirs in structure.items():
            main_path = case_dir / main_dir
            main_path.mkdir(parents=True, exist_ok=True)
            
            for subdir in subdirs:
                if subdir.endswith(".json") or subdir.endswith(".txt"):
                    # Create file
                    (main_path / subdir).touch()
                else:
                    # Create directory
                    (main_path / subdir).mkdir(exist_ok=True)
        
        # Create metadata
        full_metadata = {
            "case_id": case_id,
            "folder_path": folder_path,
            "created_at": datetime.now().isoformat(),
            "status": "created",
            **(metadata or {})
        }
        
        (case_dir / "metadata.json").write_text(
            json.dumps(full_metadata, indent=2)
        )
        
        # Update index
        self._update_index(case_id, full_metadata)
        
        print(f"✅ Created case structure: {case_dir}")
        return case_dir
    
    def save_agent_result(
        self,
        case_id: str,
        agent_name: str,
        result: Dict[str, Any]
    ):
        """
        Save agent execution result
        
        Args:
            case_id: Case identifier
            agent_name: Agent name
            result: Agent result dictionary
        """
        case_dir = self.base_path / case_id
        agent_file = case_dir / "results" / "agents" / f"{agent_name}_analysis.json"
        
        # Add timestamp
        result["saved_at"] = datetime.now().isoformat()
        
        agent_file.write_text(json.dumps(result, indent=2))
        print(f"  💾 Saved {agent_name} result: {agent_file.name}")
    
    def save_final_report(
        self,
        case_id: str,
        report: Dict[str, Any],
        formats: List[str] = ["json", "md", "html"]
    ):
        """
        Save final case report in multiple formats
        
        Args:
            case_id: Case identifier
            report: Report dictionary
            formats: Output formats (json, md, html)
        """
        case_dir = self.base_path / case_id
        results_dir = case_dir / "results"
        
        # JSON format (always)
        json_file = results_dir / "final_report.json"
        json_file.write_text(json.dumps(report, indent=2))
        print(f"  📄 Saved JSON report: {json_file.name}")
        
        # Markdown format
        if "md" in formats:
            md_file = results_dir / "final_report.md"
            md_content = self._generate_markdown_report(report)
            md_file.write_text(md_content)
            print(f"  📄 Saved Markdown report: {md_file.name}")
        
        # HTML format
        if "html" in formats:
            html_file = results_dir / "final_report.html"
            html_content = self._generate_html_report(report)
            html_file.write_text(html_content)
            print(f"  📄 Saved HTML report: {html_file.name}")
        
        # Update case status
        self._update_case_status(case_id, "complete")
    
    def _generate_markdown_report(self, report: Dict[str, Any]) -> str:
        """Generate Markdown report"""
        md = []
        md.append(f"# Case Analysis Report: {report['case_id']}\n")
        md.append(f"**Date:** {report.get('timestamp', 'N/A')}\n")
        md.append(f"**Folder:** `{report.get('folder', 'N/A')}`\n")
        md.append("\n---\n")
        
        # Summary
        summary = report.get('summary', {})
        md.append("## Summary\n")
        md.append(f"- **Total Files:** {summary.get('total_files', 0)}")
        md.append(f"- **Total Size:** {summary.get('total_size_mb', 0):.1f} MB")
        md.append(f"- **Tasks Executed:** {summary.get('total_tasks', 0)}")
        md.append(f"- **Successful Agents:** {summary.get('successful_agents', 0)}\n")
        
        # Files by type
        if 'files_by_type' in summary:
            md.append("### Files by Type\n")
            for file_type, count in summary['files_by_type'].items():
                md.append(f"- **{file_type}:** {count}")
            md.append("")
        
        # Findings
        if 'findings' in report and report['findings']:
            md.append("## Key Findings\n")
            for i, finding in enumerate(report['findings'], 1):
                md.append(f"### {i}. [{finding['agent'].upper()}] {finding['category']}\n")
                md.append(f"**Confidence:** {finding['confidence']:.1%}\n")
                md.append(f"{finding['output'][:500]}...\n")
        
        return "\n".join(md)
    
    def _generate_html_report(self, report: Dict[str, Any]) -> str:
        """Generate HTML report"""
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Case Report: {report['case_id']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #2c3e50; }}
        h2 {{ color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        .metadata {{ background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .finding {{ background: #fff; border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .agent {{ color: #3498db; font-weight: bold; }}
        .confidence {{ color: #27ae60; }}
    </style>
</head>
<body>
    <h1>Case Analysis Report</h1>
    <div class="metadata">
        <p><strong>Case ID:</strong> {report['case_id']}</p>
        <p><strong>Date:</strong> {report.get('timestamp', 'N/A')}</p>
        <p><strong>Folder:</strong> {report.get('folder', 'N/A')}</p>
    </div>
    
    <h2>Summary</h2>
    <ul>
        <li>Total Files: {report.get('summary', {}).get('total_files', 0)}</li>
        <li>Total Size: {report.get('summary', {}).get('total_size_mb', 0):.1f} MB</li>
        <li>Tasks: {report.get('summary', {}).get('total_tasks', 0)}</li>
        <li>Successful Agents: {report.get('summary', {}).get('successful_agents', 0)}</li>
    </ul>
    
    <h2>Findings</h2>
"""
        
        for i, finding in enumerate(report.get('findings', []), 1):
            html += f"""
    <div class="finding">
        <h3>{i}. <span class="agent">[{finding['agent'].upper()}]</span> {finding['category']}</h3>
        <p><span class="confidence">Confidence: {finding['confidence']:.1%}</span></p>
        <pre>{finding['output'][:1000]}...</pre>
    </div>
"""
        
        html += """
</body>
</html>
"""
        return html
    
    def _update_case_status(self, case_id: str, status: str):
        """Update case status"""
        case_dir = self.base_path / case_id
        metadata_file = case_dir / "metadata.json"
        
        if metadata_file.exists():
            metadata = json.loads(metadata_file.read_text())
            metadata["status"] = status
            metadata["updated_at"] = datetime.now().isoformat()
            metadata_file.write_text(json.dumps(metadata, indent=2))
            
            # Update index
            self._update_index(case_id, metadata)
    
    def get_case(self, case_id: str) -> Optional[Dict[str, Any]]:
        """
        Get case information
        
        Args:
            case_id: Case identifier
            
        Returns:
            Case metadata or None if not found
        """
        case_dir = self.base_path / case_id
        metadata_file = case_dir / "metadata.json"
        
        if metadata_file.exists():
            return json.loads(metadata_file.read_text())
        return None
    
    def list_cases(
        self,
        status: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        List all cases
        
        Args:
            status: Filter by status (optional)
            limit: Maximum results
            
        Returns:
            List of case metadata
        """
        index = self._load_index()
        cases = list(index.values())
        
        # Filter by status
        if status:
            cases = [c for c in cases if c.get('status') == status]
        
        # Sort by created_at (newest first)
        cases.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        return cases[:limit]
    
    def search_cases(self, query: str) -> List[Dict[str, Any]]:
        """
        Search cases by query (simple text search)
        
        Args:
            query: Search query
            
        Returns:
            Matching cases
        """
        query_lower = query.lower()
        results = []
        
        for case in self.list_cases(limit=1000):
            # Search in case_id, folder_path
            searchable = f"{case.get('case_id', '')} {case.get('folder_path', '')}".lower()
            if query_lower in searchable:
                results.append(case)
        
        return results
    
    def get_case_report(self, case_id: str, format: str = "json") -> Optional[str]:
        """
        Get case final report
        
        Args:
            case_id: Case identifier
            format: Report format (json, md, html)
            
        Returns:
            Report content or None
        """
        case_dir = self.base_path / case_id
        report_file = case_dir / "results" / f"final_report.{format}"
        
        if report_file.exists():
            return report_file.read_text()
        return None
    
    def archive_case(self, case_id: str) -> Path:
        """
        Archive a case (create timestamped snapshot)
        
        Args:
            case_id: Case identifier
            
        Returns:
            Path to archive
        """
        case_dir = self.base_path / case_id
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_dir = case_dir / "archives" / timestamp
        
        # Copy results to archive
        shutil.copytree(
            case_dir / "results",
            archive_dir / "results"
        )
        
        # Save snapshot metadata
        snapshot = {
            "case_id": case_id,
            "archived_at": datetime.now().isoformat(),
            "snapshot_dir": str(archive_dir.relative_to(self.base_path))
        }
        
        (archive_dir / "snapshot_metadata.json").write_text(
            json.dumps(snapshot, indent=2)
        )
        
        print(f"📦 Archived case: {archive_dir}")
        return archive_dir
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get overall statistics
        
        Returns:
            Statistics dictionary
        """
        cases = self.list_cases(limit=10000)
        
        stats = {
            "total_cases": len(cases),
            "by_status": {},
            "total_files": 0,
            "by_date": {}
        }
        
        for case in cases:
            # Count by status
            status = case.get('status', 'unknown')
            stats['by_status'][status] = stats['by_status'].get(status, 0) + 1
            
            # Total files
            stats['total_files'] += case.get('total_files', 0)
            
            # By date
            date = case.get('created_at', '')[:10]  # YYYY-MM-DD
            if date:
                stats['by_date'][date] = stats['by_date'].get(date, 0) + 1
        
        return stats


# Convenience functions
def create_case_structure(case_id: str, folder_path: str) -> Path:
    """Create new case structure"""
    manager = CaseManager()
    return manager.create_case(case_id, folder_path)


def save_case_results(case_id: str, report: Dict[str, Any]):
    """Save case results"""
    manager = CaseManager()
    manager.save_final_report(case_id, report)


def get_case_info(case_id: str) -> Optional[Dict[str, Any]]:
    """Get case information"""
    manager = CaseManager()
    return manager.get_case(case_id)


if __name__ == "__main__":
    # Example usage
    manager = CaseManager()
    
    print("📊 Case Manager Statistics:")
    stats = manager.get_statistics()
    print(f"  Total cases: {stats['total_cases']}")
    print(f"  Total files: {stats['total_files']}")
    print(f"  By status: {stats['by_status']}")
