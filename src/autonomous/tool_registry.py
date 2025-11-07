"""
Tool Registry - Agents can discover and use tools autonomously
"""

from typing import Dict, List, Any, Callable, Optional
from dataclasses import dataclass
import inspect


@dataclass
class Tool:
    """Tool definition"""
    name: str
    description: str
    category: str
    input_types: List[str]
    output_type: str
    function: Callable
    examples: List[str]


class ToolRegistry:
    """
    Central registry of tools that agents can use
    Agents can discover tools based on their needs
    """
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register built-in tools"""
        
        # Text extraction tools
        self.register_tool(Tool(
            name="extract_text_from_pdf",
            description="Extract text content from PDF files",
            category="extraction",
            input_types=["pdf"],
            output_type="text",
            function=self._extract_pdf_text,
            examples=["Extract text from financial report PDF"]
        ))
        
        self.register_tool(Tool(
            name="extract_tables_from_excel",
            description="Extract tables and data from Excel spreadsheets",
            category="extraction",
            input_types=["excel", "xlsx", "xls"],
            output_type="structured_data",
            function=self._extract_excel_tables,
            examples=["Extract financial data from quarterly report Excel"]
        ))
        
        self.register_tool(Tool(
            name="read_text_file",
            description="Read plain text files",
            category="extraction",
            input_types=["txt", "md"],
            output_type="text",
            function=self._read_text_file,
            examples=["Read README.md", "Read contract.txt"]
        ))
        
        # Analysis tools
        self.register_tool(Tool(
            name="calculate_statistics",
            description="Calculate basic statistics from numerical data",
            category="analysis",
            input_types=["numbers", "structured_data"],
            output_type="statistics",
            function=self._calculate_statistics,
            examples=["Calculate mean, median, std of revenue data"]
        ))
        
        self.register_tool(Tool(
            name="extract_entities",
            description="Extract named entities (people, organizations, locations)",
            category="nlp",
            input_types=["text"],
            output_type="entities",
            function=self._extract_entities,
            examples=["Extract company names from contract"]
        ))
        
        self.register_tool(Tool(
            name="summarize_text",
            description="Generate summary of long text",
            category="nlp",
            input_types=["text"],
            output_type="text",
            function=self._summarize_text,
            examples=["Summarize 50-page report"]
        ))
        
        # Search tools
        self.register_tool(Tool(
            name="semantic_search",
            description="Search documents using semantic similarity",
            category="search",
            input_types=["text_query"],
            output_type="documents",
            function=self._semantic_search,
            examples=["Find documents about revenue growth"]
        ))
        
        self.register_tool(Tool(
            name="keyword_search",
            description="Search documents using keywords",
            category="search",
            input_types=["text_query"],
            output_type="documents",
            function=self._keyword_search,
            examples=["Find documents containing 'Q4 2023'"]
        ))
    
    def register_tool(self, tool: Tool):
        """Register a new tool"""
        self.tools[tool.name] = tool
    
    def find_tools(self, 
                   input_type: Optional[str] = None,
                   category: Optional[str] = None,
                   keyword: Optional[str] = None) -> List[Tool]:
        """
        Find tools matching criteria
        
        Args:
            input_type: Filter by input type (e.g., 'pdf', 'excel')
            category: Filter by category (e.g., 'extraction', 'analysis')
            keyword: Search in tool name/description
            
        Returns:
            List of matching tools
        """
        results = []
        
        for tool in self.tools.values():
            # Check input type
            if input_type and input_type not in tool.input_types:
                continue
            
            # Check category
            if category and tool.category != category:
                continue
            
            # Check keyword
            if keyword:
                keyword_lower = keyword.lower()
                if (keyword_lower not in tool.name.lower() and 
                    keyword_lower not in tool.description.lower()):
                    continue
            
            results.append(tool)
        
        return results
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """Get tool by name"""
        return self.tools.get(name)
    
    def suggest_tools(self, file_type: str, task_description: str) -> List[Tool]:
        """
        Suggest appropriate tools for a file type and task
        
        Args:
            file_type: Type of file (e.g., 'pdf', 'excel')
            task_description: What the agent wants to do
            
        Returns:
            Suggested tools
        """
        suggestions = []
        
        # Find tools that accept this file type
        for tool in self.tools.values():
            if file_type in tool.input_types:
                suggestions.append(tool)
        
        # If task mentions specific keywords, prioritize those tools
        task_lower = task_description.lower()
        keywords = {
            'extract': 'extraction',
            'analyze': 'analysis',
            'search': 'search',
            'summarize': 'nlp',
            'entities': 'nlp',
            'statistics': 'analysis'
        }
        
        for keyword, category in keywords.items():
            if keyword in task_lower:
                category_tools = [t for t in self.tools.values() if t.category == category]
                suggestions.extend(category_tools)
        
        # Remove duplicates, preserve order
        seen = set()
        unique_suggestions = []
        for tool in suggestions:
            if tool.name not in seen:
                seen.add(tool.name)
                unique_suggestions.append(tool)
        
        return unique_suggestions
    
    def list_all_tools(self) -> Dict[str, List[Tool]]:
        """List all tools grouped by category"""
        by_category = {}
        
        for tool in self.tools.values():
            if tool.category not in by_category:
                by_category[tool.category] = []
            by_category[tool.category].append(tool)
        
        return by_category
    
    # Tool implementations (these are placeholders)
    
    def _extract_pdf_text(self, pdf_path: str) -> str:
        """Extract text from PDF"""
        # Placeholder - would use PyPDF2 or pdfplumber
        return f"[PDF text extraction from {pdf_path}]"
    
    def _extract_excel_tables(self, excel_path: str) -> Dict[str, Any]:
        """Extract tables from Excel"""
        # Placeholder - would use openpyxl or pandas
        return {"tables": [], "sheets": []}
    
    def _read_text_file(self, text_path: str) -> str:
        """Read text file"""
        try:
            with open(text_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {e}"
    
    def _calculate_statistics(self, data: List[float]) -> Dict[str, float]:
        """Calculate basic statistics"""
        import statistics
        return {
            "mean": statistics.mean(data),
            "median": statistics.median(data),
            "stdev": statistics.stdev(data) if len(data) > 1 else 0
        }
    
    def _extract_entities(self, text: str) -> List[Dict[str, str]]:
        """Extract named entities"""
        # Placeholder - would use spaCy or similar
        return [{"entity": "Example Corp", "type": "ORG"}]
    
    def _summarize_text(self, text: str, max_length: int = 200) -> str:
        """Summarize text"""
        # Placeholder - would use LLM or extractive summarization
        return text[:max_length] + "..."
    
    def _semantic_search(self, query: str, case_id: str) -> List[Dict[str, Any]]:
        """Semantic search"""
        # Would use actual embedding search
        return []
    
    def _keyword_search(self, query: str, case_id: str) -> List[Dict[str, Any]]:
        """Keyword search"""
        # Would use Elasticsearch
        return []


# Global registry instance
_registry = ToolRegistry()

def get_tool_registry() -> ToolRegistry:
    """Get global tool registry"""
    return _registry
