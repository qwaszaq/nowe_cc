"""
Professional Analyzer - 7-Phase Analysis Engine

Main orchestrator for professional document analysis following 7-phase methodology:
1. Structure Analysis
2. Quantitative Extraction
3. Qualitative Analysis
4. Temporal Trends
5. Comparative Analysis
6. Critical Assessment
7. Insight Synthesis
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from src.analysis.structure_extractor import StructureExtractor
from src.analysis.quantitative_extractor import QuantitativeExtractor
from src.analysis.qualitative_analyzer import QualitativeAnalyzer
from src.analysis.temporal_trend_analyzer import TemporalTrendAnalyzer
from src.analysis.comparative_analyzer import ComparativeAnalyzer
from src.analysis.critical_assessor import CriticalAssessor
from src.analysis.synthesis_engine import SynthesisEngine


@dataclass
class AnalysisConfig:
    """Configuration for professional analysis"""
    enable_structure_analysis: bool = True
    enable_quantitative_extraction: bool = True
    enable_qualitative_analysis: bool = True
    enable_temporal_trends: bool = True
    enable_comparative_analysis: bool = True
    enable_critical_assessment: bool = True
    enable_synthesis: bool = True


class ProfessionalAnalyzer:
    """
    Professional 7-Phase Analysis Engine
    
    Performs comprehensive analysis following professional methodology:
    1. Structure Analysis
    2. Quantitative Extraction
    3. Qualitative Analysis
    4. Temporal Trends
    5. Comparative Analysis
    6. Critical Assessment
    7. Insight Synthesis
    
    Can optionally use local LLM (LMStudio) for interpretation layer.
    """
    
    def __init__(self, config: Optional[AnalysisConfig] = None, llm_client: Optional[Any] = None):
        """
        Initialize Professional Analyzer
        
        Args:
            config: Analysis configuration
            llm_client: Optional local LLM client (LMStudioLLMClient) for interpretation
        """
        self.config = config or AnalysisConfig()
        self.llm_client = llm_client
        
        # Initialize extractors
        if self.config.enable_structure_analysis:
            self.structure_extractor = StructureExtractor()
        else:
            self.structure_extractor = None
            
        if self.config.enable_quantitative_extraction:
            self.quantitative_extractor = QuantitativeExtractor()
        else:
            self.quantitative_extractor = None
            
        if self.config.enable_qualitative_analysis:
            self.qualitative_analyzer = QualitativeAnalyzer()
        else:
            self.qualitative_analyzer = None
            
        if self.config.enable_temporal_trends:
            self.trend_analyzer = TemporalTrendAnalyzer()
        else:
            self.trend_analyzer = None
            
        if self.config.enable_comparative_analysis:
            self.comparative_analyzer = ComparativeAnalyzer()
        else:
            self.comparative_analyzer = None
            
        if self.config.enable_critical_assessment:
            self.critical_assessor = CriticalAssessor()
        else:
            self.critical_assessor = None
            
        if self.config.enable_synthesis:
            self.synthesis_engine = SynthesisEngine(llm_client=self.llm_client)
        else:
            self.synthesis_engine = None
    
    def analyze(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Perform complete 7-phase analysis
        
        Args:
            documents: List of document dicts with 'text', 'year', 'filename'
        
        Returns:
            Complete analysis results for all phases
        """
        results = {}
        
        # Phase 1: Structure Analysis
        if self.config.enable_structure_analysis and self.structure_extractor:
            print("   📋 Phase 1: Structure Analysis...")
            results['phase1'] = self.structure_extractor.analyze(documents)
        
        # Phase 2: Quantitative Extraction
        if self.config.enable_quantitative_extraction and self.quantitative_extractor:
            print("   📊 Phase 2: Quantitative Extraction...")
            results['phase2'] = self.quantitative_extractor.extract(documents)
        
        # Phase 3: Qualitative Analysis
        if self.config.enable_qualitative_analysis and self.qualitative_analyzer:
            print("   📝 Phase 3: Qualitative Analysis...")
            results['phase3'] = self.qualitative_analyzer.analyze(documents)
        
        # Phase 4: Temporal Trends
        if self.config.enable_temporal_trends and self.trend_analyzer and 'phase2' in results:
            print("   📈 Phase 4: Temporal Trends...")
            results['phase4'] = self.trend_analyzer.analyze(results['phase2'])
        
        # Phase 5: Comparative Analysis
        if self.config.enable_comparative_analysis and self.comparative_analyzer and 'phase2' in results:
            print("   🔍 Phase 5: Comparative Analysis...")
            results['phase5'] = self.comparative_analyzer.analyze(results['phase2'])
        
        # Phase 6: Critical Assessment
        if self.config.enable_critical_assessment and self.critical_assessor:
            print("   ⚠️  Phase 6: Critical Assessment...")
            results['phase6'] = self.critical_assessor.assess(documents, results)
        
        # Phase 7: Synthesis
        if self.config.enable_synthesis and self.synthesis_engine:
            print("   💡 Phase 7: Insight Synthesis...")
            results['phase7'] = self.synthesis_engine.synthesize(results)
        
        return results
