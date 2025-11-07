"""
Autonomous Document Discovery System
Automatically scans folders and identifies files for processing
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import mimetypes
from datetime import datetime
import hashlib


class DocumentScanner:
    """Scans directories and identifies documents"""
    
    # Supported file types
    SUPPORTED_EXTENSIONS = {
        # Text documents
        '.txt': 'text',
        '.md': 'text',
        '.csv': 'tabular',
        
        # Office documents
        '.pdf': 'pdf',
        '.docx': 'word',
        '.doc': 'word',
        '.xlsx': 'excel',
        '.xls': 'excel',
        
        # Data formats
        '.json': 'json',
        '.xml': 'xml',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        
        # Images (for OCR)
        '.png': 'image',
        '.jpg': 'image',
        '.jpeg': 'image',
        '.tiff': 'image',
    }
    
    def __init__(self):
        self.discovered_files = []
        
    def scan_folder(self, folder_path: str, recursive: bool = True) -> List[Dict[str, Any]]:
        """
        Scan folder and discover all processable files
        
        Args:
            folder_path: Path to folder
            recursive: Scan subdirectories
            
        Returns:
            List of discovered files with metadata
        """
        folder = Path(folder_path)
        
        if not folder.exists():
            raise ValueError(f"Folder does not exist: {folder_path}")
        
        if not folder.is_dir():
            raise ValueError(f"Not a directory: {folder_path}")
        
        discovered = []
        
        # Scan files
        if recursive:
            files = folder.rglob('*')
        else:
            files = folder.glob('*')
        
        for file_path in files:
            if file_path.is_file():
                file_info = self._analyze_file(file_path)
                if file_info:
                    discovered.append(file_info)
        
        self.discovered_files = discovered
        return discovered
    
    def _analyze_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Analyze single file and extract metadata"""
        
        # Get extension
        ext = file_path.suffix.lower()
        
        # Check if supported
        if ext not in self.SUPPORTED_EXTENSIONS:
            return None
        
        # Get file stats
        stats = file_path.stat()
        
        # Calculate file hash
        file_hash = self._calculate_hash(file_path)
        
        return {
            'path': str(file_path.absolute()),
            'filename': file_path.name,
            'extension': ext,
            'type': self.SUPPORTED_EXTENSIONS[ext],
            'size_bytes': stats.st_size,
            'size_mb': round(stats.st_size / (1024 * 1024), 2),
            'modified': datetime.fromtimestamp(stats.st_mtime).isoformat(),
            'hash': file_hash,
            'mime_type': mimetypes.guess_type(str(file_path))[0],
        }
    
    def _calculate_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file"""
        sha256 = hashlib.sha256()
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        
        return sha256.hexdigest()[:16]  # First 16 chars
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of discovered files"""
        if not self.discovered_files:
            return {"total": 0, "by_type": {}}
        
        # Count by type
        by_type = {}
        total_size = 0
        
        for file in self.discovered_files:
            file_type = file['type']
            by_type[file_type] = by_type.get(file_type, 0) + 1
            total_size += file['size_bytes']
        
        return {
            'total': len(self.discovered_files),
            'by_type': by_type,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'files': self.discovered_files
        }


class IntelligentFileClassifier:
    """
    Classifies files and determines what to do with them
    """
    
    # Classification rules
    CLASSIFICATION_RULES = {
        'investigative': {
            'keywords': ['investigation', 'osint', 'intelligence', 'surveillance', 'fraud', 'corruption', 
                        'scandal', 'whistleblower', 'leak', 'evidence', 'witness', 'testimony',
                        'cba', 'prokuratura', '?ledztwo', 'post?powanie', 'sprawa', 'afera'],
            'patterns': ['case', 'suspect', 'allegation'],
            'extensions': ['.pdf', '.docx', '.txt'],
        },
        'financial': {
            'keywords': ['revenue', 'profit', 'balance', 'income', 'financial', 'quarterly', 'annual', 'earnings'],
            'patterns': ['Q[1-4]', '20[0-9]{2}', 'FY', 'YoY'],
            'extensions': ['.xlsx', '.csv'],
        },
        'legal': {
            'keywords': ['contract', 'agreement', 'terms', 'conditions', 'clause', 'legal', 'compliance', 'regulation'],
            'patterns': ['article', 'section', 'hereby'],
            'extensions': ['.pdf', '.docx'],
        },
        'technical': {
            'keywords': ['specification', 'architecture', 'design', 'technical', 'API', 'database', 'system'],
            'patterns': ['v[0-9]', 'version'],
            'extensions': ['.md', '.txt', '.pdf'],
        },
        'data': {
            'keywords': ['dataset', 'data', 'records', 'entries'],
            'patterns': [],
            'extensions': ['.csv', '.xlsx', '.json'],
        },
    }
    
    def classify_file(self, file_info: Dict[str, Any], sample_content: Optional[str] = None) -> Dict[str, Any]:
        """
        Classify file and determine category
        
        FIXED: Now parses file content for accurate classification!
        
        Args:
            file_info: File metadata from DocumentScanner
            sample_content: Optional sample of file content for analysis
            
        Returns:
            Classification result with category and confidence
        """
        filename_lower = file_info['filename'].lower()
        extension = file_info['extension']
        file_path = file_info.get('path', '')
        
        # FIXED: Parse file content if not provided!
        if not sample_content and file_path:
            try:
                from src.parsing.document_parsers import UniversalDocumentParser
                parser = UniversalDocumentParser()
                parse_result = parser.parse(file_path)
                if parse_result.success:
                    # Use first 1000 chars for classification
                    sample_content = parse_result.text[:1000]
            except Exception:
                pass  # Continue with filename-only classification
        
        scores = {}
        
        # Score each category
        for category, rules in self.CLASSIFICATION_RULES.items():
            score = 0
            
            # Check extension
            if extension in rules['extensions']:
                score += 2
            
            # Check keywords in filename (lower weight)
            for keyword in rules['keywords']:
                if keyword.lower() in filename_lower:
                    score += 1  # Reduced from 3
            
            # Check content if provided (MUCH HIGHER WEIGHT!)
            if sample_content:
                content_lower = sample_content.lower()
                
                # Investigative keywords (highest priority)
                if category == 'investigative':
                    investigative_keywords = ['investigation', 'osint', 'intelligence', 'fraud', 
                                             'corruption', 'scandal', 'cba', 'centralne biuro', 
                                             'antykorupcyjn', 'prokuratura', '?ledztw', 'post?powanie',
                                             'afera', 'podejrzany', '?wiadek', 'dow?d']
                    keyword_matches = sum(1 for k in investigative_keywords if k in content_lower)
                    if keyword_matches >= 3:
                        score += 20  # Very high for investigative content!
                
                # Regular keyword matching
                for keyword in rules['keywords']:
                    if keyword.lower() in content_lower:
                        score += 3  # Increased from 1
            
            scores[category] = score
        
        # Get best category
        if scores:
            best_category = max(scores, key=scores.get)
            confidence = min(scores[best_category] / 10.0, 1.0)  # Normalize to 0-1
        else:
            best_category = 'general'
            confidence = 0.5
        
        return {
            'category': best_category,
            'confidence': confidence,
            'all_scores': scores,
            'file_type': file_info['type'],
        }
    
    def suggest_analysis(self, classification: Dict[str, Any]) -> List[str]:
        """
        Suggest what type of analysis to perform
        
        Args:
            classification: Result from classify_file
            
        Returns:
            List of suggested analysis types
        """
        category = classification['category']
        file_type = classification['file_type']
        
        suggestions = []
        
        # Category-specific suggestions
        if category == 'investigative':
            suggestions.extend(['comprehensive_investigation', 'osint_analysis', 
                               'entity_extraction', 'timeline_reconstruction', 
                               'critical_review', 'source_verification'])
        elif category == 'financial':
            suggestions.extend(['financial_analysis', 'data_extraction', 'trend_analysis'])
        elif category == 'legal':
            suggestions.extend(['legal_review', 'entity_extraction', 'risk_assessment'])
        elif category == 'technical':
            suggestions.extend(['technical_review', 'architecture_analysis'])
        elif category == 'data':
            suggestions.extend(['data_analysis', 'statistical_analysis', 'data_quality'])
        else:
            suggestions.extend(['general_analysis', 'summarization'])
        
        # File type specific
        if file_type == 'excel':
            suggestions.append('spreadsheet_analysis')
        elif file_type == 'pdf':
            suggestions.append('document_extraction')
        
        return list(set(suggestions))  # Remove duplicates
    
    def determine_investigation_type(self, classification: Dict[str, Any], all_scores: Dict[str, int]) -> str:
        """
        Determine what type of investigation is needed
        
        Args:
            classification: Result from classify_file
            all_scores: All category scores
            
        Returns:
            Investigation type: 'comprehensive', 'osint', 'financial', 'legal', or 'none'
        """
        category = classification['category']
        
        # If it's investigative content, go comprehensive
        if category == 'investigative':
            return 'comprehensive'
        
        # Check if other categories suggest investigation
        investigative_score = all_scores.get('investigative', 0)
        
        # High financial + some investigative = financial investigation
        if all_scores.get('financial', 0) > 5 and investigative_score > 3:
            return 'financial'
        
        # High legal + some investigative = legal investigation
        if all_scores.get('legal', 0) > 5 and investigative_score > 3:
            return 'legal'
        
        # Pure investigative signals
        if investigative_score >= 5:
            return 'osint'
        
        return 'none'


class AutomaticTaskGenerator:
    """
    Automatically generates tasks for agents based on discovered files
    """
    
    def __init__(self):
        self.scanner = DocumentScanner()
        self.classifier = IntelligentFileClassifier()
    
    def process_folder(self, folder_path: str) -> Dict[str, Any]:
        """
        Process entire folder and generate tasks
        
        Args:
            folder_path: Path to folder with documents
            
        Returns:
            Complete analysis plan with tasks
        """
        print(f"?? Scanning folder: {folder_path}")
        
        # 1. Discover files
        files = self.scanner.scan_folder(folder_path)
        summary = self.scanner.get_summary()
        
        print(f"?? Found {summary['total']} files ({summary['total_size_mb']} MB)")
        for file_type, count in summary['by_type'].items():
            print(f"   - {file_type}: {count}")
        
        # 2. Classify each file
        print("\n?? Classifying files...")
        classified_files = []
        
        for file in files:
            # Try to read sample content
            sample_content = self._read_sample(file['path'])
            
            # Classify
            classification = self.classifier.classify_file(file, sample_content)
            
            # Suggest analysis
            suggestions = self.classifier.suggest_analysis(classification)
            
            # Determine investigation type
            investigation_type = self.classifier.determine_investigation_type(
                classification, 
                classification.get('all_scores', {})
            )
            
            classified_files.append({
                **file,
                'category': classification['category'],
                'confidence': classification['confidence'],
                'suggested_analyses': suggestions,
                'investigation_type': investigation_type
            })
            
            print(f"   {file['filename']}: {classification['category']} (confidence: {classification['confidence']:.2f})")
        
        # 3. Generate tasks
        print("\n?? Generating tasks...")
        tasks = self._generate_tasks(classified_files)
        
        print(f"   Generated {len(tasks)} tasks")
        
        return {
            'folder': folder_path,
            'summary': summary,
            'files': classified_files,
            'tasks': tasks,
            'timestamp': datetime.now().isoformat()
        }
    
    def _read_sample(self, file_path: str, max_chars: int = 1000) -> Optional[str]:
        """Read sample content from file"""
        try:
            # For now, only handle text files
            if file_path.endswith('.txt') or file_path.endswith('.md'):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read(max_chars)
        except:
            pass
        return None
    
    def _generate_tasks(self, classified_files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate agent tasks based on classified files"""
        tasks = []
        
        # Group files by category
        by_category = {}
        for file in classified_files:
            category = file['category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(file)
        
        # Generate tasks per category
        for category, files in by_category.items():
            # Check if any file requires investigation
            investigation_types = [f.get('investigation_type', 'none') for f in files]
            primary_investigation = max(set(investigation_types), key=investigation_types.count)
            
            # Determine which agents to use
            agents = self._select_agents(category, primary_investigation)
            
            # Create task
            task = {
                'task_id': f"{category}_{len(tasks)}",
                'category': category,
                'agents': agents,
                'files': [f['path'] for f in files],
                'file_count': len(files),
                'analyses': list(set([a for f in files for a in f['suggested_analyses']])),
                'priority': self._calculate_priority(files),
                'investigation_type': primary_investigation,
            }
            
            tasks.append(task)
        
        # Sort by priority
        tasks.sort(key=lambda x: x['priority'], reverse=True)
        
        return tasks
    
    def _select_agents(self, category: str, investigation_type: str = 'none') -> List[str]:
        """
        Select appropriate agents for category
        
        Args:
            category: Document category
            investigation_type: Investigation type if applicable
            
        Returns:
            List of agent names
        """
        # If investigative content, use investigative team
        if category == 'investigative' or investigation_type != 'none':
            return ['investigative']  # Special marker for investigative team
        
        # Standard agent mapping
        agent_mapping = {
            'financial': ['financial', 'data_science'],
            'legal': ['legal', 'risk'],
            'technical': ['architect', 'developer'],
            'data': ['data_science'],
            'general': ['documentation'],
        }
        
        return agent_mapping.get(category, ['documentation'])
    
    def _calculate_priority(self, files: List[Dict[str, Any]]) -> int:
        """Calculate task priority (0-100)"""
        # Base priority
        priority = 50
        
        # Higher priority for more files
        priority += min(len(files) * 5, 20)
        
        # Higher priority for larger files
        total_size = sum(f['size_mb'] for f in files)
        priority += min(int(total_size), 20)
        
        # Higher priority for high confidence classifications
        avg_confidence = sum(f['confidence'] for f in files) / len(files)
        priority += int(avg_confidence * 10)
        
        return min(priority, 100)


if __name__ == "__main__":
    # Demo
    import sys
    
    if len(sys.argv) > 1:
        folder = sys.argv[1]
    else:
        folder = "."
    
    generator = AutomaticTaskGenerator()
    result = generator.process_folder(folder)
    
    print("\n" + "=" * 80)
    print("ANALYSIS PLAN")
    print("=" * 80)
    
    for i, task in enumerate(result['tasks'], 1):
        print(f"\nTask {i}: {task['category'].upper()}")
        print(f"  Priority: {task['priority']}/100")
        print(f"  Agents: {', '.join(task['agents'])}")
        print(f"  Files: {task['file_count']}")
        print(f"  Analyses: {', '.join(task['analyses'])}")
