"""
Autonomous Orchestrator
Fully autonomous system that processes folders without human intervention
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from typing import List, Dict, Any, Optional
import time
from datetime import datetime
from pathlib import Path

from src.autonomous.document_discovery import AutomaticTaskGenerator
from src.agents.base_agent import FinancialAnalystAgent, LegalAnalystAgent, RiskAnalystAgent
from src.agents.additional_agents import DataScienceAgent, ArchitectAgent, DocumentationAgent
from src.data.embedding_pipeline import DualEmbeddingSystem
from src.data.smart_router import SmartDatabaseRouter
from src.llm.lmstudio_client import LMStudioLLMClient
from src.memory.rag_cag_strategy import RAGCAGOrchestrator
from datetime import datetime

# Import investigative team
try:
    from agents.analytical.analytical_team import AnalyticalTeam
    INVESTIGATIVE_AVAILABLE = True
except ImportError:
    INVESTIGATIVE_AVAILABLE = False
    print("⚠️  Analytical team not available (will use basic agents only)")

# Import Professional Analyzer
try:
    from src.analysis.professional_analyzer import ProfessionalAnalyzer, AnalysisConfig
    PROFESSIONAL_ANALYSIS_AVAILABLE = True
except ImportError as e:
    PROFESSIONAL_ANALYSIS_AVAILABLE = False
    print(f"⚠️  Professional analysis not available: {e}")


class AutonomousOrchestrator:
    """
    Fully autonomous orchestration system
    User points to folder → System handles everything
    
    Now with INVESTIGATIVE CAPABILITIES:
    - Detects investigative content automatically
    - Routes to specialized analytical team when appropriate
    - Maintains basic agent support for standard tasks
    """
    
    def __init__(self, enable_investigative: bool = True):
        """
        Initialize autonomous system
        
        Args:
            enable_investigative: Enable investigative team (requires analytical agents)
        """
        print("🚀 Initializing Autonomous System...")
        
        # Discovery & classification
        self.task_generator = AutomaticTaskGenerator()
        
        # LLM Client - REAL LMSTUDIO CONNECTION
        print("   🔌 Connecting to LMStudio...")
        try:
            self.llm = LMStudioLLMClient(
                base_url="http://192.168.200.226:1234/v1",
                model="openai/gpt-oss-20b"
            )
            # Test connection
            if self.llm.health_check():
                print("   ✅ LMStudio connected")
            else:
                print("   ⚠️  LMStudio not responding (will use fallback)")
        except Exception as e:
            print(f"   ⚠️  LMStudio connection failed: {e}")
            self.llm = None
        
        # RAG + CAG Orchestrator
        print("   💾 Initializing RAG+CAG...")
        self.rag_cag = RAGCAGOrchestrator(
            context_window=44000,  # Local LLM context
            use_cag=True
        )
        print("   ✅ RAG+CAG ready")
        
        # Data infrastructure
        self.embeddings = DualEmbeddingSystem()
        self.db_router = SmartDatabaseRouter()
        
        # Basic agent registry
        self.agents = {
            'financial': FinancialAnalystAgent(),
            'legal': LegalAnalystAgent(),
            'risk': RiskAnalystAgent(),
            'data_science': DataScienceAgent(),
            'architect': ArchitectAgent(),
            'documentation': DocumentationAgent(),
        }
        
        # Initialize investigative team if available and enabled
        self.investigative_team = None
        self.investigative_enabled = enable_investigative and INVESTIGATIVE_AVAILABLE
        
        if self.investigative_enabled:
            try:
                print("   🔍 Initializing Investigative Team...")
                self.investigative_team = AnalyticalTeam()
                print("   ✅ Investigative team ready (9 specialized agents)")
            except Exception as e:
                print(f"   ⚠️  Could not initialize investigative team: {e}")
                self.investigative_enabled = False
        
        # Initialize Professional Analyzer (with LLM for interpretation)
        self.professional_analyzer = None
        if PROFESSIONAL_ANALYSIS_AVAILABLE:
            try:
                print("   📊 Initializing Professional Analyzer...")
                # Pass LLM client to Professional Analyzer for local interpretation
                llm_for_analysis = self.llm if self.llm else None
                self.professional_analyzer = ProfessionalAnalyzer(
                    config=AnalysisConfig(
                        enable_structure_analysis=True,
                        enable_quantitative_extraction=True,
                        enable_qualitative_analysis=True,
                        enable_temporal_trends=True,
                        enable_comparative_analysis=True,
                        enable_critical_assessment=True,
                        enable_synthesis=True,
                    ),
                    llm_client=llm_for_analysis  # Local LLM for interpretation
                )
                if llm_for_analysis:
                    print("   ✅ Professional Analyzer ready (7-phase analysis + LLM interpretation)")
                else:
                    print("   ✅ Professional Analyzer ready (7-phase analysis, no LLM)")
            except Exception as e:
                print(f"   ⚠️  Could not initialize professional analyzer: {e}")
                self.professional_analyzer = None
        
        print("✅ System initialized")
        print(f"   - {len(self.agents)} basic agents available")
        if self.investigative_enabled:
            print(f"   - 9 investigative agents available")
        print(f"   - LLM: {'LMStudio' if self.llm else 'Fallback mode'}")
        print(f"   - Database router ready")
        print(f"   - Embedding system ready")
        print(f"   - RAG+CAG optimization enabled")
        print()
    
    def process_folder(self, folder_path: str, case_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Main entry point: Process entire folder autonomously
        
        Args:
            folder_path: Path to folder with documents
            case_id: Optional case ID (auto-generated if not provided)
            
        Returns:
            Complete analysis results
        """
        start_time = time.time()
        
        # Generate case ID if not provided
        if not case_id:
            case_id = f"case_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print("╔" + "=" * 78 + "╗")
        print(f"║  AUTONOMOUS ANALYSIS: {case_id:<57}║")
        print("╚" + "=" * 78 + "╝")
        print()
        
        # Step 1: Discover & classify files
        print("📋 STEP 1: Document Discovery & Classification")
        print("-" * 80)
        discovery_result = self.task_generator.process_folder(folder_path)
        
        # Step 2: Store documents
        print("\n💾 STEP 2: Document Storage")
        print("-" * 80)
        stored_docs = self._store_documents(case_id, discovery_result)
        
        # Step 3: Execute tasks autonomously
        print("\n🤖 STEP 3: Autonomous Agent Execution")
        print("-" * 80)
        task_results = self._execute_tasks(case_id, discovery_result['tasks'], stored_docs)
        
        # Step 4: Synthesize results
        print("\n📊 STEP 4: Result Synthesis")
        print("-" * 80)
        final_results = self._synthesize_results(case_id, discovery_result, task_results)
        
        duration = time.time() - start_time
        
        print("\n" + "=" * 80)
        print(f"✅ ANALYSIS COMPLETE ({duration:.1f}s)")
        print("=" * 80)
        
        return final_results
    
    def _store_documents(self, case_id: str, discovery_result: Dict[str, Any]) -> Dict[str, Any]:
        """Store all discovered documents in databases"""
        
        files = discovery_result['files']
        print(f"Storing {len(files)} documents...")
        
        stored = {
            'embeddings': [],
            'documents': [],
            'errors': []
        }
        
        for file_info in files:
            try:
                # Read file content (for supported types)
                content = self._extract_content(file_info)
                
                if not content:
                    print(f"   ⏭️  {file_info['filename']}: Unsupported for text extraction")
                    continue
                
                # Generate embeddings
                embedding_result = self.embeddings.embed(
                    content,
                    document_type=file_info.get('category', 'general')
                )
                
                # Store in Elasticsearch (full document)
                doc_id = self.db_router.store_document(
                    case_id=case_id,
                    document_id=file_info['hash'],
                    filename=file_info['filename'],
                    content=content,
                    document_type=file_info['type'],
                    metadata={
                        'category': file_info['category'],
                        'confidence': file_info['confidence'],
                        'path': file_info['path']
                    }
                )
                
                stored['documents'].append(doc_id)
                
                # Store embeddings
                embedding_records = [{
                    'document_id': file_info['hash'],
                    'chunk_id': 0,
                    'content': content[:500],  # Store preview
                    'embedding': embedding_result.embedding,
                    'metadata': {
                        'filename': file_info['filename'],
                        'category': file_info['category']
                    }
                }]
                
                db_used, count = self.db_router.store_embeddings(case_id, embedding_records)
                stored['embeddings'].append({
                    'file': file_info['filename'],
                    'db': db_used,
                    'count': count
                })
                
                print(f"   ✅ {file_info['filename']}: Stored in {db_used}")
                
            except Exception as e:
                error_msg = f"Error storing {file_info['filename']}: {str(e)}"
                stored['errors'].append(error_msg)
                print(f"   ❌ {error_msg}")
        
        print(f"\n📊 Storage Summary:")
        print(f"   - Documents: {len(stored['documents'])}")
        print(f"   - Embeddings: {len(stored['embeddings'])}")
        print(f"   - Errors: {len(stored['errors'])}")
        
        return stored
    
    def _extract_content(self, file_info: Dict[str, Any]) -> Optional[str]:
        """Extract text content from file - REAL PARSING!"""
        file_path = file_info['path']
        
        try:
            # Use Universal Parser
            from src.parsing.document_parsers import UniversalDocumentParser
            parser = UniversalDocumentParser()
            
            result = parser.parse(file_path)
            
            if result.success:
                # Include tables in text if available
                full_content = result.text
                
                if result.tables:
                    full_content += f"\n\n[Extracted {len(result.tables)} tables]\n"
                    for i, table in enumerate(result.tables, 1):
                        full_content += f"\nTable {i}:\n"
                        if 'data' in table:
                            # Show table preview
                            full_content += str(table['data'][:5]) + "\n"
                
                return full_content
            else:
                print(f"   ⚠️  Parse failed for {file_info['filename']}: {result.error}")
                return f"[{file_info['filename']}]\n[Parse error: {result.error}]"
                
        except Exception as e:
            print(f"   ⚠️  Could not extract content from {file_path}: {e}")
            return f"[{file_info['filename']}]\n[Error: {str(e)}]"
    
    def _execute_tasks(self, case_id: str, tasks: List[Dict[str, Any]], stored_docs: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute all tasks autonomously"""
        
        results = []
        
        for i, task in enumerate(tasks, 1):
            print(f"\n📌 Task {i}/{len(tasks)}: {task['category'].upper()} (Priority: {task['priority']})")
            print(f"   Agents: {', '.join(task['agents'])}")
            print(f"   Files: {task['file_count']}")
            
            investigation_type = task.get('investigation_type', 'none')
            
            # Check if this requires investigative team OR professional analysis
            if 'investigative' in task['agents']:
                # If investigative team available, use it
                if self.investigative_enabled:
                    print(f"   🔍 Routing to Investigative Team (Type: {investigation_type})")
                    result = self._execute_investigative_task(case_id, task, investigation_type)
                    results.append(result)
                    continue
                # If investigative team NOT available but Professional Analyzer IS available
                elif self.professional_analyzer:
                    print(f"   📊 Routing to Professional Analyzer (Investigative content detected)")
                    result = self._execute_professional_analysis_task(case_id, task)
                    results.append(result)
                    continue
                else:
                    print(f"   ⚠️  Investigative task detected but no analyzer available")
                    # Fall through to basic agents
            
            # Execute with each agent
            agent_results = []
            
            for agent_type in task['agents']:
                agent = self.agents.get(agent_type)
                
                if not agent:
                    print(f"   ⚠️  Agent '{agent_type}' not available")
                    continue
                
                try:
                    # Prepare documents for this task
                    # FIXED: Parse files directly instead of relying on DB!
                    task_docs = []
                    extracted_metrics = {}  # NEW: Store extracted metrics per document
                    from src.parsing.document_parsers import UniversalDocumentParser
                    from src.parsing.pdf_table_extractor import PDFTableExtractor
                    parser = UniversalDocumentParser()
                    table_extractor = PDFTableExtractor()
                    
                    for file_info in task['files'][:5]:  # Limit to 5 docs for demo
                        # FIXED: Handle both dict and string formats
                        if isinstance(file_info, dict):
                            file_path = file_info.get('path', file_info.get('filename', ''))
                            filename = file_info.get('filename', Path(file_path).name if file_path else '')
                            category = file_info.get('category', 'unknown')
                        else:
                            # file_info is a string path
                            file_path = str(file_info)
                            filename = Path(file_path).name
                            category = 'unknown'
                        
                        if not file_path:
                            continue
                        
                        # Parse document DIRECTLY
                        parse_result = parser.parse(str(file_path))
                        if parse_result.success:
                            # NEW: Extract metrics from PDF if it's a PDF file
                            file_metrics = None
                            if str(file_path).lower().endswith('.pdf'):
                                try:
                                    print(f"   📊 Extracting metrics from {filename}...")
                                    file_metrics = table_extractor.extract_numeric_data(str(file_path), parse_result.text)
                                    # Extract year from filename for better organization
                                    year = None
                                    for y in range(2008, 2025):
                                        if str(y) in filename:
                                            year = y
                                            break
                                    if year and file_metrics:
                                        extracted_metrics[year] = file_metrics
                                        metrics_count = sum(1 for v in file_metrics.values() if v is not None and isinstance(v, (int, float)))
                                        if metrics_count > 0:
                                            print(f"      ✅ Extracted {metrics_count} metrics for year {year}")
                                    elif file_metrics:
                                        extracted_metrics[filename] = file_metrics
                                        metrics_count = sum(1 for v in file_metrics.values() if v is not None and isinstance(v, (int, float)))
                                        if metrics_count > 0:
                                            print(f"      ✅ Extracted {metrics_count} metrics")
                                except Exception as e:
                                    print(f"   ⚠️  Metrics extraction failed for {filename}: {e}")
                            
                            # Use first 2000 chars (fits in context window)
                            content_preview = parse_result.text[:2000]
                            task_docs.append({
                                'filename': filename,
                                'category': category,
                                'content': content_preview,
                                'full_length': len(parse_result.text),
                                'metrics': file_metrics  # NEW: Include metrics per document
                            })
                    
                    # Use RAG+CAG for optimized processing
                    # FIXED: Always use LMStudio when available!
                    if self.llm:
                        print(f"   🤖 {agent_type}: Processing with RAG+CAG...")
                        start = time.time()
                        
                        # Build optimized prompt using CAG
                        from src.memory.cache_augmented_generation import SmartContextManager
                        context_mgr = SmartContextManager(max_tokens=44000)
                        
                        # Prepare hot content with REAL document content!
                        hot_content = f"TASK: Analyze {task['category']} documents as {agent_type}\n\n"
                        hot_content += f"You are analyzing {len(task_docs)} documents.\n"
                        hot_content += f"Required analyses: {', '.join(task['analyses'])}\n\n"
                        
                        # NEW: Add extracted metrics if available
                        if extracted_metrics:
                            print(f"   📊 Including {len(extracted_metrics)} documents with extracted metrics")
                            hot_content += "=== EXTRACTED DATA FROM DOCUMENTS ===\n"
                            hot_content += "IMPORTANT: Use ONLY these verified numbers (marked with ✅). Do NOT generate new numbers!\n\n"
                            for key, metrics in extracted_metrics.items():
                                if metrics and any(v is not None for k, v in metrics.items() if k != 'sources'):
                                    hot_content += f"Data from {key}:\n"
                                    for metric_name, value in metrics.items():
                                        if metric_name != 'sources' and value is not None:
                                            hot_content += f"  - {metric_name}: {value} ✅\n"
                                    if metrics.get('sources'):
                                        hot_content += f"  Sources: {len(metrics['sources'])} data points extracted\n"
                                    hot_content += "\n"
                            hot_content += "=== END OF EXTRACTED DATA ===\n\n"
                            hot_content += "CRITICAL INSTRUCTIONS:\n"
                            hot_content += "- Analyze ONLY the extracted data above (marked with ✅)\n"
                            hot_content += "- If data is missing for a year, mark as '[BRAK DANYCH]' or '[SZACUNEK]'\n"
                            hot_content += "- Do NOT generate or invent numbers\n"
                            hot_content += "- Base all conclusions on the extracted data\n"
                            hot_content += "- Mark any estimates as '[SZACUNEK]' in your analysis\n"
                            hot_content += "- If you need to reference numbers not in extracted data, use '[SZACUNEK]'\n\n"
                        
                        # Add real document content!
                        for i, doc in enumerate(task_docs, 1):
                            hot_content += f"\n--- Document {i}: {doc['filename']} ---\n"
                            hot_content += f"Category: {doc['category']}\n"
                            hot_content += f"Content preview ({doc['full_length']} chars total):\n\n"
                            hot_content += doc['content']
                            hot_content += "\n\n"
                        
                        hot_content += "\n\nProvide a detailed analysis with:\n"
                        hot_content += "1. Key findings from the documents AND extracted data\n"
                        hot_content += "2. Important patterns or trends (based on extracted data)\n"
                        hot_content += "3. Specific insights relevant to your role\n"
                        hot_content += "4. Mark any estimates as '[SZACUNEK]' or '[BRAK DANYCH]'\n"
                        hot_content += "5. Confidence level and reasoning\n"
                        
                        # Build prompt with CAG
                        prompt_result = context_mgr.create_optimized_prompt(
                            case_id=case_id,
                            agent_type=agent_type,
                            new_content=hot_content
                        )
                        
                        # REAL LMStudio call
                        llm_response = self.llm.chat_completion([
                            {"role": "user", "content": prompt_result['prompt']}
                        ])
                        
                        duration = time.time() - start
                        
                        # FIXED: Use tokens_used instead of usage
                        total_tokens = llm_response.tokens_used.get('total', 0)
                        
                        agent_results.append({
                            'agent': agent_type,
                            'output': llm_response.content,
                            'duration': duration,
                            'tokens_used': total_tokens,
                            'tokens_saved': prompt_result.get('tokens_saved', 0),
                            'confidence': 0.85,  # Would be calculated from response
                            'extracted_metrics': extracted_metrics if extracted_metrics else {}  # NEW: Include metrics
                        })
                        
                        print(f"   ✅ {agent_type}: Complete ({duration:.1f}s)")
                        print(f"      Tokens used: {total_tokens}")
                        print(f"      Tokens saved by CAG: {prompt_result.get('tokens_saved', 0)}")
                    
                    else:
                        # Fallback: Use agent's built-in execute
                        print(f"   🤖 {agent_type}: Processing (fallback mode)...")
                        start = time.time()
                        
                        from src.agents.base_agent import Task as AgentTask
                        
                        agent_task = AgentTask(
                            task_id=f"{case_id}_{task['task_id']}_{agent_type}",
                            title=f"Analyze {task['category']} documents",
                            description=f"Analyze {task['file_count']} {task['category']} documents",
                            task_type='analysis',
                            data={
                                'case_id': case_id,
                                'files': task['files'], 
                                'analyses': task['analyses'],
                                'agent_type': agent_type,
                                'priority': task['priority']
                            },
                            created_at=datetime.now()
                        )
                        
                        result = agent.execute(agent_task)
                        duration = time.time() - start
                        
                        agent_results.append({
                            'agent': agent_type,
                            'result': result,
                            'duration': duration
                        })
                        
                        print(f"   ✅ {agent_type}: Complete ({duration:.1f}s, confidence: {result.confidence:.2f})")
                    
                except Exception as e:
                    print(f"   ❌ {agent_type}: Error - {str(e)}")
                    import traceback
                    traceback.print_exc()
                    agent_results.append({
                        'agent': agent_type,
                        'error': str(e)
                    })
            
            results.append({
                'task': task,
                'agent_results': agent_results
            })
        
        return results
    
    def _execute_investigative_task(
        self, 
        case_id: str, 
        task: Dict[str, Any], 
        investigation_type: str
    ) -> Dict[str, Any]:
        """
        Execute task using investigative team
        
        Args:
            case_id: Case identifier
            task: Task definition
            investigation_type: Type of investigation ('comprehensive', 'osint', 'financial', 'legal')
            
        Returns:
            Task result with investigative findings
        """
        try:
            # Extract subject from files
            file_paths = task['files'][:5]  # Limit to 5 for analysis
            subject = f"Case {case_id}"
            
            # If there's a clear subject, extract it
            # For now, use case_id, but could be enhanced
            
            print(f"   📋 Preparing investigation: {subject}")
            print(f"   📂 Analyzing {len(file_paths)} documents")
            
            # STEP 1: Professional Analysis (7 phases) - NEW!
            professional_results = None
            if self.professional_analyzer:
                try:
                    print(f"   🔍 Running Professional Analysis (7 phases)...")
                    from src.parsing.document_parsers import UniversalDocumentParser
                    parser = UniversalDocumentParser()
                    
                    documents = []
                    for file_info in file_paths:
                        if isinstance(file_info, dict):
                            file_path = file_info.get('path', file_info.get('filename', ''))
                            filename = file_info.get('filename', Path(file_path).name if file_path else '')
                        else:
                            file_path = str(file_info)
                            filename = Path(file_path).name
                        
                        if not file_path:
                            continue
                        
                        # Parse document
                        parse_result = parser.parse(str(file_path))
                        if parse_result.success:
                            # Extract year from filename
                            year = None
                            for y in range(2008, 2025):
                                if str(y) in filename:
                                    year = y
                                    break
                            
                            documents.append({
                                'filename': filename,
                                'text': parse_result.text,
                                'year': year,
                                'path': file_path,
                                'filepath': file_path,  # Also include as filepath for quantitative_extractor
                            })
                    
                    if documents:
                        professional_results = self.professional_analyzer.analyze(documents)
                        print(f"   ✅ Professional Analysis complete: {len(professional_results)} phases")
                except Exception as e:
                    print(f"   ⚠️  Professional Analysis failed: {e}")
                    import traceback
                    traceback.print_exc()
            
            # STEP 2: Investigative Team Analysis (if available)
            investigation_results = None
            if self.investigative_team:
                print(f"   🚀 Launching {investigation_type} investigation...")
                start_time = time.time()
                
                investigation_results = self.investigative_team.investigate(
                    subject=subject,
                    investigation_type=investigation_type,
                    priority="high"
                )
                
                duration = time.time() - start_time
                print(f"   ✅ Investigation complete ({duration:.1f}s)")
                print(f"   📊 {len(investigation_results)} analysis phases completed")
            
            # STEP 3: Combine results
            agent_results = []
            
            # Add professional analysis results
            if professional_results:
                for phase_key, phase_data in professional_results.items():
                    agent_results.append({
                        'agent': f'professional_{phase_key}',
                        'output': self._format_professional_output(phase_key, phase_data),
                        'duration': 0,  # Duration tracked per phase
                        'confidence': 0.85,
                        'analysis_phase': phase_key,
                        'professional_analysis': True
                    })
            
            # Add investigative team results
            if investigation_results:
                duration = duration if 'duration' in locals() else 0
                for phase_name, phase_result in investigation_results.items():
                    agent_results.append({
                        'agent': f'investigative_{phase_name}',
                        'output': self._format_investigation_output(phase_result),
                        'duration': duration / len(investigation_results) if investigation_results else 0,
                        'confidence': 0.9,
                        'investigation_phase': phase_name
                    })
            
            return {
                'task': task,
                'agent_results': agent_results,
                'investigation_type': investigation_type,
                'professional_analysis': professional_results  # Include full professional analysis
            }
            
        except Exception as e:
            print(f"   ❌ Investigation failed: {str(e)}")
            import traceback
            traceback.print_exc()
            
            return {
                'task': task,
                'agent_results': [{
                    'agent': 'investigative_error',
                    'error': str(e)
                }]
            }
    
    def _execute_professional_analysis_task(
        self,
        case_id: str,
        task: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute task using Professional Analyzer only
        
        Args:
            case_id: Case identifier
            task: Task definition
            
        Returns:
            Task result with professional analysis findings
        """
        if not self.professional_analyzer:
            return {
                'task': task,
                'agent_results': [{
                    'agent': 'professional_analysis_error',
                    'error': 'Professional Analyzer not available'
                }]
            }
        
        try:
            # Extract documents
            file_paths = task['files'][:10]  # Limit to 10 for analysis
            print(f"   📋 Preparing professional analysis: {len(file_paths)} documents")
            
            from src.parsing.document_parsers import UniversalDocumentParser
            parser = UniversalDocumentParser()
            
            documents = []
            for file_info in file_paths:
                if isinstance(file_info, dict):
                    file_path = file_info.get('path', file_info.get('filename', ''))
                    filename = file_info.get('filename', Path(file_path).name if file_path else '')
                else:
                    file_path = str(file_info)
                    filename = Path(file_path).name
                
                if not file_path:
                    continue
                
                # Parse document
                parse_result = parser.parse(str(file_path))
                if parse_result.success:
                    # Extract year from filename
                    year = None
                    for y in range(2008, 2025):
                        if str(y) in filename:
                            year = y
                            break
                    
                    documents.append({
                        'filename': filename,
                        'text': parse_result.text,
                        'year': year,
                        'path': file_path,
                        'filepath': file_path,  # Also include as filepath for quantitative_extractor
                    })
            
            if not documents:
                return {
                    'task': task,
                    'agent_results': [{
                        'agent': 'professional_analysis_error',
                        'error': 'No documents could be parsed'
                    }]
                }
            
            # Run Professional Analysis (7 phases)
            print(f"   🔍 Running Professional Analysis (7 phases)...")
            start_time = time.time()
            
            professional_results = self.professional_analyzer.analyze(documents)
            
            duration = time.time() - start_time
            print(f"   ✅ Professional Analysis complete ({duration:.1f}s)")
            print(f"   📊 {len(professional_results)} phases completed")
            
            # Convert professional results to agent_results format
            agent_results = []
            for phase_key, phase_data in professional_results.items():
                agent_results.append({
                    'agent': f'professional_{phase_key}',
                    'output': self._format_professional_output(phase_key, phase_data),
                    'duration': duration / len(professional_results) if professional_results else 0,
                    'confidence': 0.85,
                    'analysis_phase': phase_key,
                    'professional_analysis': True
                })
            
            return {
                'task': task,
                'agent_results': agent_results,
                'professional_analysis': professional_results,
                'analysis_type': 'professional_only'
            }
            
        except Exception as e:
            print(f"   ❌ Professional Analysis failed: {str(e)}")
            import traceback
            traceback.print_exc()
            
            return {
                'task': task,
                'agent_results': [{
                    'agent': 'professional_analysis_error',
                    'error': str(e)
                }]
            }
    
    def _format_investigation_output(self, task_result) -> str:
        """Format investigation output for synthesis"""
        if hasattr(task_result, 'output'):
            output = task_result.output
            if isinstance(output, dict):
                # Extract relevant information from dict
                return str(output)
            elif isinstance(output, str):
                return output
            else:
                return f"Investigation completed: {type(output).__name__}"
        else:
            return "Investigation phase completed"
    
    def _format_professional_output(self, phase_key: str, phase_data: Dict[str, Any]) -> str:
        """Format professional analysis output for synthesis"""
        import json
        
        # Create summary based on phase type
        if phase_key == 'phase1':
            return f"Structure Analysis: {phase_data.get('total_documents', 0)} documents analyzed"
        elif phase_key == 'phase2':
            metrics = phase_data.get('metrics', {})
            return f"Quantitative Extraction: {len(metrics)} years with metrics extracted"
        elif phase_key == 'phase3':
            narrative = phase_data.get('narrative_analysis', {})
            return f"Qualitative Analysis: {len(narrative)} documents analyzed"
        elif phase_key == 'phase4':
            trends = phase_data.get('trends', {})
            return f"Temporal Trends: {len(trends)} metrics analyzed"
        elif phase_key == 'phase5':
            efficiency = phase_data.get('efficiency_metrics', {})
            return f"Comparative Analysis: {len(efficiency)} efficiency metrics calculated"
        elif phase_key == 'phase6':
            assessment = phase_data
            issues = len(assessment.get('consistency_issues', []))
            return f"Critical Assessment: {issues} issues identified, confidence: {assessment.get('overall_confidence', 0):.2f}"
        elif phase_key == 'phase7':
            synthesis = phase_data
            findings = len(synthesis.get('key_findings', []))
            recommendations = len(synthesis.get('recommendations', []))
            return f"Insight Synthesis: {findings} key findings, {recommendations} recommendations"
        else:
            return f"Professional Analysis Phase: {phase_key} - {json.dumps(phase_data, indent=2)[:500]}"
    
    def _synthesize_results(self, case_id: str, discovery: Dict[str, Any], task_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Synthesize all results into final report"""
        
        print("Generating final report...")
        
        # Count successes
        total_tasks = len(task_results)
        successful_agents = sum(
            1 for tr in task_results
            for ar in tr['agent_results']
            if 'result' in ar
        )
        
        # Extract key findings
        findings = []
        for tr in task_results:
            for ar in tr['agent_results']:
                # FIXED: Handle different output formats properly
                output_text = ""
                confidence = 0.5
                
                if 'output' in ar:
                    # LMStudio path - output is string
                    output_text = ar['output']
                    confidence = ar.get('confidence', 0.85)
                    
                elif 'result' in ar:
                    # Fallback path - result is TaskResult object
                    result_obj = ar['result']
                    if hasattr(result_obj, 'output'):
                        output_val = result_obj.output
                        # Handle dict output
                        if isinstance(output_val, dict):
                            output_text = str(output_val)
                        elif isinstance(output_val, str):
                            output_text = output_val
                        else:
                            output_text = f"[Result: {type(output_val).__name__}]"
                        confidence = getattr(result_obj, 'confidence', 0.7)
                    else:
                        output_text = f"[{ar.get('agent', 'unknown')} completed]"
                        confidence = 0.6
                
                elif 'error' in ar:
                    # Error case
                    output_text = f"Error: {ar['error']}"
                    confidence = 0.0
                
                else:
                    # Unknown format
                    output_text = f"[{ar.get('agent', 'unknown')} processed in {ar.get('duration', 0):.1f}s]"
                    confidence = 0.5
                
                # Only add if we have meaningful output
                if output_text and len(output_text) > 10:
                    findings.append({
                        'agent': ar.get('agent', 'unknown'),
                        'category': tr['task']['category'],
                        'output': output_text,
                        'confidence': confidence
                    })
        
        # Extract metrics info from task results
        extracted_metrics_summary = {}
        for tr in task_results:
            for ar in tr['agent_results']:
                if 'extracted_metrics' in ar:
                    extracted_metrics_summary.update(ar['extracted_metrics'])
        
        report = {
            'case_id': case_id,
            'folder': discovery['folder'],
            'timestamp': datetime.now().isoformat(),
            
            'summary': {
                'total_files': discovery['summary']['total'],
                'files_by_type': discovery['summary']['by_type'],
                'total_size_mb': discovery['summary']['total_size_mb'],
                'total_tasks': total_tasks,
                'successful_agents': successful_agents,
                'extracted_metrics_count': len(extracted_metrics_summary),
            },
            
            'extracted_metrics': extracted_metrics_summary,  # NEW: Include extracted metrics
            
            'findings': findings,
            'task_results': task_results,
        }
        
        # Save report
        report_path = Path(f"reports/autonomous_{case_id}.json")
        report_path.parent.mkdir(exist_ok=True)
        
        import json
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\n📄 Report saved: {report_path}")
        
        return report


def main():
    """CLI entry point"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python autonomous_orchestrator.py <folder_path> [case_id]")
        print("\nExample:")
        print("  python autonomous_orchestrator.py /path/to/documents")
        print("  python autonomous_orchestrator.py /data/case_001 case_001")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    case_id = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Create orchestrator
    orchestrator = AutonomousOrchestrator()
    
    # Process folder
    results = orchestrator.process_folder(folder_path, case_id)
    
    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Case ID: {results['case_id']}")
    print(f"Files Processed: {results['summary']['total_files']}")
    print(f"Tasks Executed: {results['summary']['total_tasks']}")
    print(f"Successful Agents: {results['summary']['successful_agents']}")
    print(f"\nTop Findings:")
    for i, finding in enumerate(results['findings'][:5], 1):
        print(f"  {i}. [{finding['agent']}] {finding['category']}: {finding['output'][:100]}...")


if __name__ == "__main__":
    main()
