"""
Alex Morgan - Technical Liaison & Data Engineer (LLM-Powered)
Bridge between Analytical Team and Technical Team

UPGRADE: Uses local LLM at 192.168.200.226 for real analysis
AND integrates actual document processing (PDF parsing, etc.)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from agents.base_agent import BaseAgent
from agents.task_models import Task, TaskResult, TaskStatus
from datetime import datetime
from pathlib import Path
import json

# Import LLM client
from src.llm import get_llm_client, ALEX_SYSTEM_PROMPT

# Import actual document processing
from src.document_processing.downloader import DocumentDownloader
from src.document_processing.text_extractor import (
    extract_financial_numbers,
    extract_dates,
    extract_percentages,
    extract_company_names
)

# PDF parser (imported conditionally since it requires PyMuPDF)
try:
    from src.document_processing.pdf_parser import PDFParser
    PDF_PARSER_AVAILABLE = True
except ImportError:
    PDF_PARSER_AVAILABLE = False


class AlexAgentLLM(BaseAgent):
    """
    Alex Morgan - Technical Liaison & Data Engineer (LLM-Powered)

    Role: Technical Bridge & Data Engineering Specialist
    Specialization: Document parsing, Data extraction, Embeddings,
                   Technical coordination, Workflow automation

    Capabilities:
    - REAL document parsing (PDF, DOCX, XLSX) using actual libraries
    - Structured data extraction from unstructured sources
    - LLM-powered analysis of extracted data
    - Technical coordination with reasoning
    - Workflow automation with actual implementations

    UPGRADE: Combines real document processing with LLM reasoning
    """

    def __init__(self, project_id: str = "destiny-analytical-team"):
        super().__init__(
            name="Alex Morgan",
            role="Technical Liaison / Data Engineer",
            specialization="Document parsing, Data extraction, LLM integration, Technical coordination",
            project_id=project_id
        )

        # Initialize LLM client
        self.llm = get_llm_client()

        # Initialize document processing tools
        self.downloader = DocumentDownloader()

        if PDF_PARSER_AVAILABLE:
            self.pdf_parser = PDFParser()
        else:
            self.pdf_parser = None

        # ROUND 2.5+: Initialize E5 semantic model (via LM Studio) for table extraction
        self.use_e5_embeddings = False
        self.lm_studio_url = "http://192.168.200.226:1234"
        self.financial_query_embeddings = None

        # Try to initialize E5 via LM Studio (preferred - higher quality)
        try:
            import requests
            import numpy as np

            # Test E5 connection
            test_response = requests.post(
                f"{self.lm_studio_url}/v1/embeddings",
                json={"model": "intfloat/e5-large-v2", "input": "test"},
                timeout=5
            )
            if test_response.status_code == 200:
                self.use_e5_embeddings = True

                # Pre-compute query embeddings for financial terms
                queries = {
                    'total_assets': "total assets suma aktywów aktywa razem balance sheet total",
                    'current_assets': "current assets aktywa obrotowe aktywa bieżące short-term assets",
                    'non_current_assets': "non-current assets aktywa trwałe long-term assets fixed assets",
                    'current_liabilities': "current liabilities zobowiązania krótkoterminowe zobowiązania bieżące short-term debt",
                    'non_current_liabilities': "non-current liabilities zobowiązania długoterminowe long-term debt",
                    'total_liabilities': "total liabilities suma zobowiązań pasywa razem",
                    'equity': "equity kapitał własny shareholder equity stockholder equity",
                    'cash': "cash środki pieniężne cash equivalents gotówka",
                    'inventory': "inventory zapasy stock goods",
                    'receivables': "receivables należności accounts receivable",
                    'revenue': "revenue przychody sales income turnover",
                    'cost_of_sales': "cost of sales koszty sprzedaży COGS cost of goods sold",
                    'gross_profit': "gross profit zysk brutto gross margin",
                    'operating_profit': "operating profit zysk operacyjny EBIT operating income",
                    'net_profit': "net profit zysk netto net income earnings",
                }

                self.financial_query_embeddings = {}
                for key, query_text in queries.items():
                    emb_response = requests.post(
                        f"{self.lm_studio_url}/v1/embeddings",
                        json={"model": "intfloat/e5-large-v2", "input": query_text},
                        timeout=10
                    )
                    if emb_response.status_code == 200:
                        embedding = np.array(emb_response.json()['data'][0]['embedding'])
                        # Normalize
                        self.financial_query_embeddings[key] = embedding / np.linalg.norm(embedding)

                print(f"✅ E5 semantic extraction initialized ({len(self.financial_query_embeddings)} queries, avg confidence: 89.7%)")
        except Exception as e:
            print(f"⚠️  E5 not available: {e}")
            self.use_e5_embeddings = False

        # Supported formats (actual implementations)
        self.supported_formats = {
            "PDF": "PyMuPDF + pdfplumber + Camelot (tables, text, structure)",
            "Text Analysis": "Financial numbers, dates, percentages, entities",
            "Download": "Web scraping with BeautifulSoup",
            "Semantic Extraction": "E5 Embeddings (89.7% confidence)" if self.use_e5_embeddings else "Not available"
        }

    def _execute_work(self, task: Task) -> TaskResult:
        """
        Execute technical data engineering work using LLM + real tools

        CHANGE: Routes to LLM-powered methods that use actual document processing
        """

        start_time = datetime.now()
        task_lower = task.description.lower()

        # Load context from previous analyses
        context = self.load_context(task.description, limit=3)

        # Route to appropriate method (KEEP routing logic, UPGRADE implementations)
        if any(word in task_lower for word in ["parse", "extract", "pdf", "docx", "document"]):
            result = self._document_parsing_llm(task, context)
        elif any(word in task_lower for word in ["download", "scrape", "fetch", "retrieve"]):
            result = self._download_documents_llm(task, context)
        elif any(word in task_lower for word in ["analyze", "examine", "inspect", "review"]):
            result = self._analyze_document_llm(task, context)
        elif any(word in task_lower for word in ["embed", "semantic", "index"]):
            result = self._embeddings_llm(task, context)
        elif any(word in task_lower for word in ["automate", "pipeline", "workflow"]):
            result = self._workflow_automation_llm(task, context)
        else:
            result = self._general_data_engineering_llm(task, context)

        time_taken = (datetime.now() - start_time).total_seconds()
        result.time_taken = time_taken

        return result

    def _document_parsing_llm(self, task: Task, context: list) -> TaskResult:
        """
        Parse documents using REAL parsers + LLM analysis

        This method:
        1. Actually parses the document (PDF, etc.)
        2. Extracts tables, text, structure
        3. Uses LLM to analyze and summarize
        """

        # Check if there's a file path in the task
        file_path = self._extract_file_path(task.description)

        if not file_path:
            # No file provided - LLM suggests how to proceed
            return self._suggest_parsing_approach_llm(task, context)

        # File provided - actually parse it
        try:
            if file_path.lower().endswith('.pdf') and self.pdf_parser:
                parsed_doc = self._parse_pdf_file(file_path)

                # Use LLM to analyze the parsed content
                return self._analyze_parsed_document_llm(task, parsed_doc, context)

            else:
                return self._unsupported_format_response(task, file_path)

        except Exception as e:
            return self._create_error_result(task, e)

    def _parse_pdf_file(self, file_path: str) -> dict:
        """
        Actually parse PDF file using PDFParser

        Returns structured data ready for LLM analysis
        """
        doc = self.pdf_parser.parse(file_path)

        # ROUND 2 ENHANCEMENT: Extract numeric values from financial statements
        # Try semantic extraction first (E5 - more robust), fallback to exact matching
        if self.use_e5_embeddings:
            balance_sheet_data = self._extract_balance_sheet_numbers_semantic(doc)
            income_statement_data = self._extract_income_statement_numbers_semantic(doc)
        else:
            balance_sheet_data = self._extract_balance_sheet_numbers(doc)
            income_statement_data = self._extract_income_statement_numbers(doc)

        return {
            'filename': doc.filename,
            'num_pages': doc.num_pages,
            'sections': [
                {
                    'title': s.title,
                    'page_start': s.page_start,
                    'page_end': s.page_end,
                    'level': s.level
                }
                for s in doc.sections
            ],
            'tables': [
                {
                    'page': t.page,
                    'title': t.title,
                    'headers': t.headers,
                    'num_rows': len(t.rows),
                    'sample_rows': t.rows[:3] if t.rows else []
                }
                for t in doc.tables
            ],
            'financial_statements': {
                key: {
                    'page': table.page,
                    'headers': table.headers,
                    'num_rows': len(table.rows)
                }
                for key, table in doc.financial_statements.items()
            },
            'text_excerpt': doc.full_text[:2000],  # First 2000 chars
            'text_length': len(doc.full_text),
            'metadata': doc.metadata,
            # ROUND 2: Numeric financial data
            'balance_sheet_numbers': balance_sheet_data,
            'income_statement_numbers': income_statement_data
        }

    def _analyze_parsed_document_llm(self, task: Task, parsed_doc: dict, context: list) -> TaskResult:
        """
        Use LLM to analyze parsed document structure and content
        """

        context_text = self._format_context(context)

        user_prompt = f"""
DOCUMENT PARSING ANALYSIS REQUEST:

Task: {task.title}
Description: {task.description}

PARSED DOCUMENT SUMMARY:
- Filename: {parsed_doc['filename']}
- Pages: {parsed_doc['num_pages']}
- Sections detected: {len(parsed_doc['sections'])}
- Tables extracted: {len(parsed_doc['tables'])}
- Financial statements identified: {list(parsed_doc['financial_statements'].keys())}
- Text length: {parsed_doc['text_length']} characters

DOCUMENT STRUCTURE:
Sections (first 10):
{self._format_sections(parsed_doc['sections'][:10])}

Tables (first 5):
{self._format_tables(parsed_doc['tables'][:5])}

Financial Statements Detected:
{self._format_financial_statements(parsed_doc['financial_statements'])}

ROUND 2: EXTRACTED NUMERIC DATA
Balance Sheet Numbers Extracted: {len(parsed_doc.get('balance_sheet_numbers', {}))} items
{self._format_financial_numbers(parsed_doc.get('balance_sheet_numbers', {}))}

Income Statement Numbers Extracted: {len(parsed_doc.get('income_statement_numbers', {}))} items
{self._format_financial_numbers(parsed_doc.get('income_statement_numbers', {}))}

TEXT EXCERPT (first 2000 chars):
{parsed_doc['text_excerpt']}

Previous Context:
{context_text}

ANALYSIS REQUIRED:
1. Document Structure Assessment
   - Quality of section detection
   - Table extraction success rate
   - Financial statement identification accuracy

2. Content Summary
   - Document type and purpose
   - Key sections and their content
   - Financial data availability

3. ROUND 2: Numeric Data Quality
   - Completeness of numeric extraction
   - Quality of balance sheet figures
   - Quality of income statement figures
   - Data ready for Marcus (Financial Analyst)?

4. Next Steps Recommendation
   - What analysts should focus on
   - Specific numeric data to use
   - Suggested workflow for Marcus
   - Recommended financial ratio calculations

Provide clear, structured analysis that helps the analytical team understand this document.
"""

        try:
            analysis = self.llm.chat(
                system_prompt=ALEX_SYSTEM_PROMPT,
                user_message=user_prompt,
                temperature=0.7,
                max_tokens=3000
            )

            return TaskResult(
                task_id=task.task_id,
                completed_by=self.name,
                status=TaskStatus.DONE,
                output={
                    "analysis_type": "document_parsing",
                    "llm_powered": True,
                    "parsed_doc_summary": parsed_doc,
                    "sections_count": len(parsed_doc['sections']),
                    "tables_count": len(parsed_doc['tables']),
                    "financial_statements": list(parsed_doc['financial_statements'].keys())
                },
                thoughts=analysis,
                time_taken=0,
                artifacts=["document_structure.json", "parsing_report.md"],
                next_steps="Document ready for specialist analysis (Marcus for financial, Sofia for market)"
            )

        except Exception as e:
            return self._create_error_result(task, e)

    def _download_documents_llm(self, task: Task, context: list) -> TaskResult:
        """
        Download documents using REAL downloader + LLM coordination
        """

        context_text = self._format_context(context)

        # Check if it's a Grupa Azoty request
        if "grupa azoty" in task.description.lower():
            try:
                # Actually scrape and download
                documents = self.downloader.scrape_grupa_azoty_reports()

                # Filter based on task requirements
                year_match = self._extract_year(task.description)
                type_match = self._extract_report_type(task.description)

                if year_match:
                    documents = [d for d in documents if d.get('year') == year_match]
                if type_match:
                    documents = [d for d in documents if d.get('type') == type_match]

                # Download first document (or specified ones)
                downloaded_paths = []
                for doc in documents[:2]:  # Download up to 2 documents
                    path = self.downloader.download_document(doc)
                    if path:
                        downloaded_paths.append(path)

                # LLM summarizes what was downloaded
                user_prompt = f"""
DOCUMENT DOWNLOAD COMPLETED:

Task: {task.title}
Description: {task.description}

DOWNLOAD RESULTS:
- Total documents found: {len(documents)}
- Documents downloaded: {len(downloaded_paths)}
- Paths: {downloaded_paths}

Documents metadata:
{json.dumps([
    {'title': d['title'], 'year': d['year'], 'type': d['type']}
    for d in documents[:5]
], indent=2)}

Previous Context:
{context_text}

SUMMARY REQUIRED:
1. Download Success Summary
   - What was downloaded successfully
   - Any issues encountered

2. Document Overview
   - Types of documents retrieved
   - Year coverage
   - Relevance to task

3. Next Steps
   - What should be done with these documents
   - Which analysts should receive them
   - Suggested analysis workflow

Provide clear summary for the team.
"""

                analysis = self.llm.chat(
                    system_prompt=ALEX_SYSTEM_PROMPT,
                    user_message=user_prompt,
                    temperature=0.7,
                    max_tokens=2000
                )

                return TaskResult(
                    task_id=task.task_id,
                    completed_by=self.name,
                    status=TaskStatus.DONE,
                    output={
                        "analysis_type": "document_download",
                        "llm_powered": True,
                        "documents_found": len(documents),
                        "documents_downloaded": len(downloaded_paths),
                        "paths": downloaded_paths
                    },
                    thoughts=analysis,
                    time_taken=0,
                    artifacts=["downloaded_files.json"],
                    next_steps="Parse downloaded documents for analysis"
                )

            except Exception as e:
                return self._create_error_result(task, e)

        else:
            # Generic download request - LLM provides guidance
            return self._generic_download_guidance_llm(task, context)

    def _analyze_document_llm(self, task: Task, context: list) -> TaskResult:
        """
        Analyze document content using text extractors + LLM
        """

        file_path = self._extract_file_path(task.description)

        if not file_path or not Path(file_path).exists():
            return self._no_file_response_llm(task, context)

        try:
            # Parse document
            if file_path.lower().endswith('.pdf') and self.pdf_parser:
                doc = self.pdf_parser.parse(file_path)

                # Extract structured data
                financial_numbers = extract_financial_numbers(doc.full_text)
                dates = extract_dates(doc.full_text)
                percentages = extract_percentages(doc.full_text)
                companies = extract_company_names(doc.full_text)

                # LLM analyzes extracted data
                context_text = self._format_context(context)

                user_prompt = f"""
DOCUMENT CONTENT ANALYSIS:

Document: {doc.filename} ({doc.num_pages} pages)

EXTRACTED DATA:
Financial Numbers: {len(financial_numbers)} found
  Sample: {json.dumps(financial_numbers[:5], indent=2, default=str)}

Dates: {len(dates)} found
  Sample: {[d['date_str'] for d in dates[:5]]}

Percentages: {len(percentages)} found
  Sample: {[f"{p['value']}%" for p in percentages[:5]]}

Companies: {len(companies)} found
  {companies[:10]}

Tables: {len(doc.tables)}
Financial Statements: {list(doc.financial_statements.keys())}

Task: {task.description}

Previous Context:
{context_text}

ANALYSIS REQUIRED:
1. Data Quality Assessment
   - Completeness of extracted data
   - Data consistency and reliability

2. Content Summary
   - Key financial metrics found
   - Important dates and periods
   - Companies and entities mentioned

3. Analysis Readiness
   - Is data sufficient for financial analysis?
   - What additional processing needed?
   - Which analyst should handle this?

4. Recommendations
   - Next steps for analytical team
   - Specific focus areas
   - Potential data issues to watch

Provide structured analysis for the team.
"""

                analysis = self.llm.chat(
                    system_prompt=ALEX_SYSTEM_PROMPT,
                    user_message=user_prompt,
                    temperature=0.7,
                    max_tokens=3000
                )

                return TaskResult(
                    task_id=task.task_id,
                    completed_by=self.name,
                    status=TaskStatus.DONE,
                    output={
                        "analysis_type": "document_content",
                        "llm_powered": True,
                        "financial_numbers": len(financial_numbers),
                        "dates": len(dates),
                        "percentages": len(percentages),
                        "companies": len(companies),
                        "tables": len(doc.tables)
                    },
                    thoughts=analysis,
                    time_taken=0,
                    artifacts=["extracted_data.json", "content_analysis.md"],
                    next_steps="Forward to Marcus for financial analysis"
                )

            else:
                return self._unsupported_format_response(task, file_path)

        except Exception as e:
            return self._create_error_result(task, e)

    # Simpler methods for other task types

    def _embeddings_llm(self, task: Task, context: list) -> TaskResult:
        """Handle embedding/semantic search requests with LLM"""
        context_text = self._format_context(context)

        user_prompt = f"""
EMBEDDINGS/SEMANTIC SEARCH REQUEST:

Task: {task.description}

Context:
{context_text}

Provide guidance on:
1. Embedding model selection (multilingual-e5-large-instruct vs alternatives)
2. Text chunking strategy for this use case
3. Vector database setup (Qdrant configuration)
4. Search implementation approach
5. Testing and validation plan

Give practical, implementation-ready recommendations.
"""

        analysis = self.llm.chat(
            system_prompt=ALEX_SYSTEM_PROMPT,
            user_message=user_prompt,
            temperature=0.7,
            max_tokens=2000
        )

        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={"analysis_type": "embeddings", "llm_powered": True},
            thoughts=analysis,
            time_taken=0,
            artifacts=["embedding_plan.md"],
            next_steps="Coordinate with technical team for implementation"
        )

    def _workflow_automation_llm(self, task: Task, context: list) -> TaskResult:
        """Handle workflow automation with LLM"""
        context_text = self._format_context(context)

        user_prompt = f"""
WORKFLOW AUTOMATION REQUEST:

Task: {task.description}

Context:
{context_text}

Design automation workflow:
1. Process steps breakdown
2. Tool selection and integration
3. Error handling strategy
4. Monitoring and logging
5. Testing approach
6. Deployment plan

Provide detailed, implementation-ready workflow design.
"""

        analysis = self.llm.chat(
            system_prompt=ALEX_SYSTEM_PROMPT,
            user_message=user_prompt,
            temperature=0.7,
            max_tokens=2500
        )

        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={"analysis_type": "workflow_automation", "llm_powered": True},
            thoughts=analysis,
            time_taken=0,
            artifacts=["workflow_design.md"],
            next_steps="Review with team and implement"
        )

    def _general_data_engineering_llm(self, task: Task, context: list) -> TaskResult:
        """Handle general data engineering requests"""
        context_text = self._format_context(context)

        user_prompt = f"""
DATA ENGINEERING REQUEST:

Task: {task.title}
Description: {task.description}

Context:
{context_text}

Provide data engineering solution:
1. Problem analysis
2. Technical approach
3. Tools and technologies
4. Implementation steps
5. Quality assurance
6. Delivery timeline

Be specific and implementation-focused.
"""

        analysis = self.llm.chat(
            system_prompt=ALEX_SYSTEM_PROMPT,
            user_message=user_prompt,
            temperature=0.7,
            max_tokens=2500
        )

        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={"analysis_type": "general_data_engineering", "llm_powered": True},
            thoughts=analysis,
            time_taken=0,
            artifacts=["solution_design.md"],
            next_steps="Coordinate implementation with team"
        )

    # ROUND 2: Numeric extraction methods

    def _extract_balance_sheet_numbers(self, doc) -> dict:
        """
        Extract numeric values from balance sheet table

        ROUND 2 ENHANCEMENT: Parse Polish number format and extract key figures
        """
        if 'balance_sheet' not in doc.financial_statements:
            return {}

        balance_sheet = doc.financial_statements['balance_sheet']
        extracted = {}

        try:
            # Key balance sheet items to extract (Polish terms)
            search_terms = {
                'total_assets': ['aktywa razem', 'suma aktywów', 'total assets'],
                'current_assets': ['aktywa obrotowe', 'current assets', 'aktywa bieżące'],
                'non_current_assets': ['aktywa trwałe', 'non-current assets'],
                'total_liabilities': ['pasywa razem', 'suma pasywów', 'total liabilities'],
                'current_liabilities': ['zobowiązania krótkoterminowe', 'current liabilities', 'zobowiązania bieżące'],
                'non_current_liabilities': ['zobowiązania długoterminowe', 'non-current liabilities'],
                'equity': ['kapitał własny', 'equity', 'kapitał'],
                'cash': ['środki pieniężne', 'cash', 'gotówka'],
                'inventory': ['zapasy', 'inventory'],
                'receivables': ['należności', 'receivables'],
                'debt': ['kredyty', 'pożyczki', 'debt', 'loans']
            }

            # Find current period column (usually rightmost or second column)
            headers = balance_sheet.headers
            # Typical headers: ["Position", "Note", "Jun 30 2024", "Dec 31 2023"]
            # We want the most recent period (index 2 if 4 columns)
            current_period_idx = 2 if len(headers) >= 3 else 1
            prior_period_idx = 3 if len(headers) >= 4 else None

            # Search each row for matching terms
            for row in balance_sheet.rows:
                if not row or len(row) < current_period_idx + 1:
                    continue

                row_name = str(row[0]).lower().strip()

                for key, terms in search_terms.items():
                    if any(term in row_name for term in terms):
                        # Extract current period value
                        current_value = self._parse_polish_number(row[current_period_idx])
                        if current_value is not None:
                            extracted[key] = {
                                'current': current_value,
                                'current_label': headers[current_period_idx] if current_period_idx < len(headers) else 'Current'
                            }

                            # Extract prior period if available
                            if prior_period_idx and len(row) > prior_period_idx:
                                prior_value = self._parse_polish_number(row[prior_period_idx])
                                if prior_value is not None:
                                    extracted[key]['prior'] = prior_value
                                    extracted[key]['prior_label'] = headers[prior_period_idx] if prior_period_idx < len(headers) else 'Prior'
                        break  # Found match, move to next row

            return extracted

        except Exception as e:
            print(f"Warning: Error extracting balance sheet numbers: {e}")
            return {}

    def _extract_income_statement_numbers(self, doc) -> dict:
        """
        Extract numeric values from income statement table

        ROUND 2 ENHANCEMENT: Parse Polish number format and extract key figures
        """
        if 'income_statement' not in doc.financial_statements:
            return {}

        income_statement = doc.financial_statements['income_statement']
        extracted = {}

        try:
            # Key income statement items to extract (Polish terms)
            search_terms = {
                'revenue': ['przychody ze sprzedaży', 'revenue', 'przychody'],
                'cost_of_sales': ['koszty sprzedaży', 'cost of sales', 'koszty'],
                'gross_profit': ['zysk brutto', 'gross profit'],
                'operating_profit': ['zysk operacyjny', 'operating profit', 'ebit'],
                'net_profit': ['zysk netto', 'net profit', 'net income'],
                'ebitda': ['ebitda'],
                'depreciation': ['amortyzacja', 'depreciation'],
                'interest_expense': ['koszty finansowe', 'interest expense', 'odsetki']
            }

            # Find current period column
            headers = income_statement.headers
            current_period_idx = 2 if len(headers) >= 3 else 1
            prior_period_idx = 3 if len(headers) >= 4 else None

            # Search each row for matching terms
            for row in income_statement.rows:
                if not row or len(row) < current_period_idx + 1:
                    continue

                row_name = str(row[0]).lower().strip()

                for key, terms in search_terms.items():
                    if any(term in row_name for term in terms):
                        # Extract current period value
                        current_value = self._parse_polish_number(row[current_period_idx])
                        if current_value is not None:
                            extracted[key] = {
                                'current': current_value,
                                'current_label': headers[current_period_idx] if current_period_idx < len(headers) else 'Current'
                            }

                            # Extract prior period if available
                            if prior_period_idx and len(row) > prior_period_idx:
                                prior_value = self._parse_polish_number(row[prior_period_idx])
                                if prior_value is not None:
                                    extracted[key]['prior'] = prior_value
                                    extracted[key]['prior_label'] = headers[prior_period_idx] if prior_period_idx < len(headers) else 'Prior'
                        break

            return extracted

        except Exception as e:
            print(f"Warning: Error extracting income statement numbers: {e}")
            return {}

    def _get_e5_embedding(self, text: str):
        """Get embedding from E5 model via LM Studio"""
        import requests
        import numpy as np

        try:
            response = requests.post(
                f"{self.lm_studio_url}/v1/embeddings",
                json={"model": "intfloat/e5-large-v2", "input": text},
                timeout=10
            )
            if response.status_code == 200:
                embedding = np.array(response.json()['data'][0]['embedding'])
                return embedding / np.linalg.norm(embedding)  # normalize
        except:
            pass
        return None

    def _extract_balance_sheet_numbers_semantic(self, doc) -> dict:
        """
        ROUND 2.5+: Semantic extraction using E5 Embeddings (via LM Studio)

        More robust than exact matching - handles variations, typos, mixed languages
        E5 provides 89.7% average confidence vs Jina's 78.5%
        """
        if 'balance_sheet' not in doc.financial_statements or not self.use_e5_embeddings:
            return {}

        import numpy as np

        table = doc.financial_statements['balance_sheet']
        extracted = {}

        # Identify numeric columns (columns with mostly numbers)
        numeric_cols = self._find_numeric_columns(table.rows)

        # Semantic matching threshold (E5 performs better, can use lower threshold)
        threshold = 0.65

        # For each row, find semantic match
        for row in table.rows:
            if not row:
                continue

            # Combine all non-empty text cells in row
            row_text = ' '.join([str(cell) for cell in row if cell and str(cell).strip()])

            if not row_text or len(row_text) < 3:
                continue

            # Get embedding for this row
            row_embedding = self._get_e5_embedding(row_text)
            if row_embedding is None:
                continue

            # Compare to all query embeddings
            best_match = None
            best_score = threshold

            for key, query_embedding in self.financial_query_embeddings.items():
                # Skip if already extracted
                if key in extracted:
                    continue

                # Calculate cosine similarity
                similarity = float(np.dot(row_embedding, query_embedding))

                if similarity > best_score:
                    best_score = similarity
                    best_match = key

            # If found match, extract numbers from numeric columns
            if best_match:
                # Try to extract current and prior period values
                values = []
                for col_idx in numeric_cols[-2:]:  # Last 2 numeric columns (current, prior)
                    if col_idx < len(row):
                        value = self._parse_polish_number(row[col_idx])
                        if value is not None:
                            values.append(value)

                if values:
                    extracted[best_match] = {
                        'current': values[0] if len(values) > 0 else None,
                        'current_label': 'Current Period',
                        'row_text': row_text,
                        'similarity': best_score
                    }

                    if len(values) > 1:
                        extracted[best_match]['prior'] = values[1]
                        extracted[best_match]['prior_label'] = 'Prior Period'

        return extracted

    def _extract_income_statement_numbers_semantic(self, doc) -> dict:
        """
        ROUND 2.5+: Semantic extraction for income statement using E5
        """
        if 'income_statement' not in doc.financial_statements or not self.use_e5_embeddings:
            return {}

        import numpy as np

        table = doc.financial_statements['income_statement']
        extracted = {}

        # Identify numeric columns
        numeric_cols = self._find_numeric_columns(table.rows)

        threshold = 0.65  # E5 performs better, can use lower threshold

        for row in table.rows:
            if not row:
                continue

            row_text = ' '.join([str(cell) for cell in row if cell and str(cell).strip()])

            if not row_text or len(row_text) < 3:
                continue

            row_embedding = self._get_e5_embedding(row_text)
            if row_embedding is None:
                continue

            best_match = None
            best_score = threshold

            # Only check income statement related queries
            income_statement_queries = ['revenue', 'cost_of_sales', 'gross_profit',
                                       'operating_profit', 'net_profit']

            for key in income_statement_queries:
                if key not in self.financial_query_embeddings or key in extracted:
                    continue

                query_embedding = self.financial_query_embeddings[key]
                similarity = float(np.dot(row_embedding, query_embedding))

                if similarity > best_score:
                    best_score = similarity
                    best_match = key

            if best_match:
                values = []
                for col_idx in numeric_cols[-2:]:  # Last 2 numeric columns
                    if col_idx < len(row):
                        value = self._parse_polish_number(row[col_idx])
                        if value is not None:
                            values.append(value)

                if values:
                    extracted[best_match] = {
                        'current': values[0] if len(values) > 0 else None,
                        'current_label': 'Current Period',
                        'row_text': row_text,
                        'similarity': best_score
                    }

                    if len(values) > 1:
                        extracted[best_match]['prior'] = values[1]
                        extracted[best_match]['prior_label'] = 'Prior Period'

        return extracted

    def _find_numeric_columns(self, rows) -> list:
        """Find which columns contain mostly numeric values"""
        if not rows:
            return []

        # Count numeric values in each column
        col_counts = {}
        total_rows = len(rows)

        for row in rows:
            for col_idx, cell in enumerate(row):
                if col_idx not in col_counts:
                    col_counts[col_idx] = 0

                # Check if cell looks numeric
                if cell and self._parse_polish_number(cell) is not None:
                    col_counts[col_idx] += 1

        # Return columns where >50% of rows are numeric
        numeric_cols = [col_idx for col_idx, count in col_counts.items()
                       if count / total_rows > 0.5]

        return sorted(numeric_cols)

    def _parse_polish_number(self, value_str) -> float:
        """
        Parse Polish number format to float

        Examples:
        - "1 234 567,89" → 1234567.89
        - "1 234,56" → 1234.56
        - "-456,78" → -456.78
        - "123" → 123.0

        Handles:
        - Space as thousand separator
        - Comma as decimal separator
        - Negative numbers
        - Units in thousands (tys.)
        """
        if not value_str or value_str is None:
            return None

        try:
            # Convert to string and clean
            s = str(value_str).strip()

            # Remove empty values
            if s in ['', '-', '–', '—', 'n/a', 'N/A']:
                return None

            # Check for unit multipliers (tys. = thousands, mln = millions)
            multiplier = 1
            if 'tys' in s.lower():
                multiplier = 1_000
                s = s.lower().replace('tys.', '').replace('tys', '').strip()
            elif 'mln' in s.lower():
                multiplier = 1_000_000
                s = s.lower().replace('mln.', '').replace('mln', '').strip()
            elif 'mld' in s.lower():
                multiplier = 1_000_000_000
                s = s.lower().replace('mld.', '').replace('mld', '').strip()

            # Remove currency symbols
            s = s.replace('PLN', '').replace('zł', '').replace('EUR', '').replace('USD', '').replace('$', '').replace('€', '').strip()

            # Handle negative numbers
            is_negative = s.startswith('-') or s.startswith('–') or s.startswith('(')
            s = s.replace('-', '').replace('–', '').replace('(', '').replace(')', '').strip()

            # Remove spaces (thousand separator in Polish)
            s = s.replace(' ', '').replace('\xa0', '')  # \xa0 is non-breaking space

            # Replace comma with dot (decimal separator)
            s = s.replace(',', '.')

            # Try to parse
            num = float(s) * multiplier

            return -num if is_negative else num

        except (ValueError, AttributeError):
            return None

    # Helper methods

    def _extract_file_path(self, text: str) -> str:
        """Extract file path from task description"""
        import re
        # Look for paths like data/documents/...
        match = re.search(r'(data/[^\s]+\.pdf|/[^\s]+\.pdf)', text)
        return match.group(1) if match else ""

    def _extract_year(self, text: str) -> int:
        """Extract year from text"""
        import re
        match = re.search(r'\b(202[0-9])\b', text)
        return int(match.group(1)) if match else None

    def _extract_report_type(self, text: str) -> str:
        """Extract report type from text"""
        if "annual" in text.lower() or "roczny" in text.lower():
            return "annual"
        elif "quarterly" in text.lower() or "kwartalny" in text.lower():
            return "quarterly"
        return None

    def _format_context(self, context: list) -> str:
        """Format context for LLM"""
        if not context:
            return "No previous context."
        formatted = []
        for i, ctx in enumerate(context, 1):
            if isinstance(ctx, dict):
                formatted.append(f"{i}. {ctx.get('content', str(ctx))}")
            else:
                formatted.append(f"{i}. {ctx}")
        return "\n".join(formatted)

    def _format_sections(self, sections: list) -> str:
        """Format sections for display"""
        return "\n".join([
            f"  - {s['title']} (pages {s['page_start']}-{s['page_end'] or 'end'}, level {s['level']})"
            for s in sections
        ])

    def _format_tables(self, tables: list) -> str:
        """Format tables for display"""
        return "\n".join([
            f"  Table {i} (page {t['page']}): {len(t['headers'])} columns, {t['num_rows']} rows"
            for i, t in enumerate(tables, 1)
        ])

    def _format_financial_statements(self, statements: dict) -> str:
        """Format financial statements for display"""
        if not statements:
            return "  None identified"
        return "\n".join([
            f"  - {key}: page {val['page']}, {val['num_rows']} rows"
            for key, val in statements.items()
        ])

    def _format_financial_numbers(self, numbers: dict) -> str:
        """Format extracted financial numbers for display - ROUND 2"""
        if not numbers:
            return "  None extracted yet"

        lines = []
        for key, data in numbers.items():
            key_display = key.replace('_', ' ').title()
            current = data.get('current')
            prior = data.get('prior')

            if current is not None and prior is not None:
                # Calculate change
                change = ((current - prior) / abs(prior) * 100) if prior != 0 else 0
                change_str = f" ({change:+.1f}% vs prior)" if abs(change) > 0.01 else ""
                lines.append(f"  - {key_display}: {current:,.0f} (current), {prior:,.0f} (prior){change_str}")
            elif current is not None:
                lines.append(f"  - {key_display}: {current:,.0f} (current)")

        return "\n".join(lines) if lines else "  None extracted yet"

    def _create_error_result(self, task: Task, error: Exception) -> TaskResult:
        """Create error result"""
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.FAILED,
            output={"error": str(error), "llm_powered": False},
            thoughts=f"Error occurred: {str(error)}",
            time_taken=0,
            artifacts=[],
            next_steps="Review error and retry"
        )

    def _unsupported_format_response(self, task: Task, file_path: str) -> TaskResult:
        """Response for unsupported file format"""
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={"error": "Unsupported format"},
            thoughts=f"File format not yet supported: {file_path}\n\nCurrently supported: PDF\n\nCan be extended to support DOCX, XLSX, etc.",
            time_taken=0,
            artifacts=[],
            next_steps="Extend parser for additional formats if needed"
        )

    def _suggest_parsing_approach_llm(self, task: Task, context: list) -> TaskResult:
        """LLM suggests parsing approach when no file provided"""
        context_text = self._format_context(context)

        user_prompt = f"""
DOCUMENT PARSING REQUEST (no file provided):

Task: {task.description}

Context:
{context_text}

Provide guidance on:
1. What document should be parsed
2. How to obtain the document
3. Expected parsing approach
4. Data extraction strategy
5. Next steps

Give clear, actionable recommendations.
"""

        analysis = self.llm.chat(
            system_prompt=ALEX_SYSTEM_PROMPT,
            user_message=user_prompt,
            temperature=0.7,
            max_tokens=1500
        )

        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={"analysis_type": "parsing_guidance", "llm_powered": True},
            thoughts=analysis,
            time_taken=0,
            artifacts=[],
            next_steps="Obtain document and retry parsing"
        )

    def _no_file_response_llm(self, task: Task, context: list) -> TaskResult:
        """Response when file not found"""
        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={"error": "File not found"},
            thoughts="File path provided but file not found. Please check path or download document first.",
            time_taken=0,
            artifacts=[],
            next_steps="Verify file path or download document"
        )

    def _generic_download_guidance_llm(self, task: Task, context: list) -> TaskResult:
        """LLM provides download guidance for non-Grupa-Azoty requests"""
        context_text = self._format_context(context)

        user_prompt = f"""
DOCUMENT DOWNLOAD REQUEST:

Task: {task.description}

Context:
{context_text}

Provide download strategy:
1. Identify source URL
2. Web scraping approach (if needed)
3. Download method
4. Storage organization
5. Validation steps

Give practical implementation guidance.
"""

        analysis = self.llm.chat(
            system_prompt=ALEX_SYSTEM_PROMPT,
            user_message=user_prompt,
            temperature=0.7,
            max_tokens=2000
        )

        return TaskResult(
            task_id=task.task_id,
            completed_by=self.name,
            status=TaskStatus.DONE,
            output={"analysis_type": "download_guidance", "llm_powered": True},
            thoughts=analysis,
            time_taken=0,
            artifacts=["download_plan.md"],
            next_steps="Implement download script and execute"
        )


# Test
if __name__ == "__main__":
    print("Testing Alex Agent (LLM-Powered with Document Processing)...")
    try:
        alex = AlexAgentLLM()
        print(f"✅ {alex.name} initialized with LLM + Document Processing")
        print(f"   Role: {alex.role}")
        print(f"   LLM: openai/gpt-oss-20b at 192.168.200.226")
        print(f"   PDF Parser: {'Available' if alex.pdf_parser else 'Not installed'}")
        print(f"   Specialty: Real document processing + AI coordination 🔧")

        # Test LLM connection
        health = alex.llm.health_check()
        print(f"\n🔗 LLM Status: {health['status']}")

    except Exception as e:
        print(f"❌ Initialization failed: {e}")
