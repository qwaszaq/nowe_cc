"""
Phase 7: Insight Synthesis
"""

from typing import Dict, List, Any, Optional
from collections import defaultdict


class SynthesisEngine:
    """Synthesize insights from all analysis phases"""
    
    def __init__(self, llm_client: Optional[Any] = None):
        """
        Initialize Synthesis Engine
        
        Args:
            llm_client: Optional LLM client for local interpretation (LMStudioLLMClient)
        """
        self.llm_client = llm_client
        self.use_llm_interpretation = llm_client is not None
    
    def synthesize(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize insights from all phases"""
        
        synthesis = {
            'key_findings': [],
            'trends': [],
            'efficiency_insights': [],
            'recommendations': [],
            'executive_summary': '',
        }
        
        # Extract key findings from trends
        trends = analysis_results.get('phase4', {}).get('trends', {})
        for metric_name, trend_data in trends.items():
            if trend_data.get('trend') != 'stable':
                synthesis['key_findings'].append({
                    'metric': metric_name.replace('_', ' ').title(),
                    'trend': trend_data['trend'],
                    'growth': trend_data.get('total_growth', 0),
                    'cagr': trend_data.get('cagr', 0),
                    'significance': 'high' if abs(trend_data.get('total_growth', 0)) > 20 else 'medium',
                })
        
        # Efficiency insights
        comparative = analysis_results.get('phase5', {})
        efficiency = comparative.get('efficiency_metrics', {})
        if efficiency:
            success_rates = [e.get('success_rate', 0) for e in efficiency.values() if e.get('success_rate')]
            if success_rates:
                avg_success_rate = sum(success_rates) / len(success_rates)
                synthesis['efficiency_insights'].append({
                    'metric': 'Average Success Rate',
                    'value': avg_success_rate,
                    'interpretation': self._interpret_success_rate(avg_success_rate),
                })
        
        # Recommendations
        assessment = analysis_results.get('phase6', {})
        if assessment.get('missing_years'):
            synthesis['recommendations'].append({
                'type': 'data_completeness',
                'priority': 'high',
                'text': f"Pozyskać brakujące raporty dla lat: {', '.join(map(str, assessment['missing_years']))}",
            })
        
        if assessment.get('consistency_issues'):
            synthesis['recommendations'].append({
                'type': 'data_quality',
                'priority': 'medium',
                'text': f"Zweryfikować {len(assessment['consistency_issues'])} znalezionych niespójności w danych",
            })
        
        # Generate executive summary
        synthesis['executive_summary'] = self._generate_executive_summary(synthesis)
        
        # Add LLM interpretation if available
        if self.use_llm_interpretation:
            synthesis['llm_interpretation'] = self._generate_llm_interpretation(
                analysis_results, synthesis
            )
        
        return synthesis
    
    def _generate_llm_interpretation(
        self, 
        analysis_results: Dict[str, Any], 
        synthesis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate LLM-based interpretation using local LLM"""
        
        if not self.llm_client:
            return {}
        
        try:
            # Build context from analysis results
            context = self._build_interpretation_context(analysis_results, synthesis)
            
            # Create prompt for LLM
            prompt = self._build_interpretation_prompt(context)
            
            # Get LLM interpretation
            messages = [
                {
                    "role": "system",
                    "content": "Jesteś profesjonalnym analitykiem raportów instytucjonalnych. Analizujesz dane wyekstrahowane przez system automatyczny i dostarczasz głębokiej interpretacji strategicznej."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            response = self.llm_client.chat_completion(messages, temperature=0.7, max_tokens=2000)
            
            if response.success:
                # Parse LLM response
                interpretation = self._parse_llm_response(response.content)
                return interpretation
            else:
                return {'error': response.error}
                
        except Exception as e:
            return {'error': str(e)}
    
    def _build_interpretation_context(
        self, 
        analysis_results: Dict[str, Any], 
        synthesis: Dict[str, Any]
    ) -> str:
        """Build context string for LLM interpretation"""
        
        context_parts = []
        
        # Phase 2: Quantitative data
        phase2 = analysis_results.get('phase2', {})
        metrics = phase2.get('metrics', {})
        if metrics:
            context_parts.append("=== WYEKSTRAHOWANE DANE LICZBOWE ===\n")
            for year in sorted([y for y in metrics.keys() if isinstance(y, int)])[:5]:
                year_metrics = metrics[year]
                context_parts.append(f"\nRok {year}:")
                for metric_name, metric_data in list(year_metrics.items())[:5]:
                    value = metric_data.get('value')
                    if value is not None:
                        context_parts.append(f"  - {metric_name}: {value}")
        
        # Phase 4: Trends
        phase4 = analysis_results.get('phase4', {})
        trends = phase4.get('trends', {})
        if trends:
            context_parts.append("\n=== TRENDY TEMPORALNE ===\n")
            for metric_name, trend_data in list(trends.items())[:5]:
                trend = trend_data.get('trend', 'unknown')
                growth = trend_data.get('total_growth', 0)
                cagr = trend_data.get('cagr', 0)
                context_parts.append(
                    f"{metric_name}: {trend} (growth: {growth:.1f}%, CAGR: {cagr:.2f}%)"
                )
        
        # Phase 5: Efficiency
        phase5 = analysis_results.get('phase5', {})
        efficiency = phase5.get('efficiency_metrics', {})
        if efficiency:
            context_parts.append("\n=== METRYKI EFEKTYWNOŚCI ===\n")
            for year in sorted([y for y in efficiency.keys() if isinstance(y, int)])[:3]:
                eff_data = efficiency[year]
                success_rate = eff_data.get('success_rate')
                cost_per_case = eff_data.get('cost_per_case')
                if success_rate:
                    context_parts.append(f"{year}: Success Rate: {success_rate:.1f}%")
                if cost_per_case:
                    context_parts.append(f"{year}: Cost per Case: {cost_per_case:,.0f} zł")
        
        # Phase 6: Assessment
        phase6 = analysis_results.get('phase6', {})
        issues = phase6.get('consistency_issues', [])
        if issues:
            context_parts.append("\n=== ZNALEZIONE PROBLEMY ===\n")
            for issue in issues[:3]:
                context_parts.append(f"- {issue.get('issue', 'N/A')}")
        
        return "\n".join(context_parts)
    
    def _build_interpretation_prompt(self, context: str) -> str:
        """Build prompt for LLM interpretation"""
        
        return f"""Przeanalizuj następujące ZWERYFIKOWANE dane z automatycznej analizy raportów CBA:

{context}

ZADANIA:

1. INTERPRETACJA TRENDÓW:
   - Co oznaczają te trendy dla działalności CBA?
   - Jakie są prawdopodobne przyczyny tych zmian?
   - Czy trendy są pozytywne czy negatywne?

2. ANALIZA EFEKTYWNOŚCI:
   - Jak oceniasz efektywność CBA na podstawie metryk?
   - Czy Success Rate jest dobry?
   - Czy Cost per Case jest uzasadniony?

3. WNIOSKI STRATEGICZNE:
   - Jakie są główne wnioski z analizy?
   - Co to oznacza dla strategii CBA?
   - Jakie są obszary wymagające uwagi?

4. REKOMENDACJE:
   - Rekomendacje operacyjne (co zrobić w krótkim terminie)
   - Rekomendacje strategiczne (co zmienić długoterminowo)
   - Priorytety działania

WAŻNE:
- Analizuj TYLKO podane dane (nie generuj nowych liczb)
- Jeśli brakuje danych, oznacz jako "[BRAK DANYCH]"
- Bądź krytyczny - kwestionuj dane jeśli są niespójne
- Formułuj wnioski oparte na dowodach

Format odpowiedzi:
- Interpretacja Trendów (2-3 akapity)
- Analiza Efektywności (1-2 akapity)
- Wnioski Strategiczne (2-3 akapity)
- Rekomendacje (lista z priorytetami)
"""
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into structured format"""
        
        # Simple parsing - extract sections
        interpretation = {
            'trend_interpretation': '',
            'efficiency_analysis': '',
            'strategic_insights': '',
            'recommendations': [],
            'full_text': response
        }
        
        # Try to extract sections (simple regex-based)
        import re
        
        sections = {
            'trend_interpretation': r'(?:INTERPRETACJA TRENDÓW|Trend|Trendy).*?(?=\n\n|\n[A-Z]|$)',
            'efficiency_analysis': r'(?:ANALIZA EFEKTYWNOŚCI|Efektywność).*?(?=\n\n|\n[A-Z]|$)',
            'strategic_insights': r'(?:WNIOSKI STRATEGICZNE|Wnioski).*?(?=\n\n|\n[A-Z]|$)',
            'recommendations': r'(?:REKOMENDACJE|Rekomendacje).*?(?=\n\n|\n[A-Z]|$)',
        }
        
        for key, pattern in sections.items():
            match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
            if match:
                if key == 'recommendations':
                    # Extract bullet points
                    recs = re.findall(r'[-•]\s*(.+?)(?=\n|$)', match.group(0))
                    interpretation['recommendations'] = recs
                else:
                    interpretation[key] = match.group(0).strip()
        
        return interpretation
    
    def _interpret_success_rate(self, rate: float) -> str:
        """Interpret success rate"""
        if rate >= 50:
            return "Bardzo wysoka skuteczność"
        elif rate >= 30:
            return "Wysoka skuteczność"
        elif rate >= 15:
            return "Średnia skuteczność"
        else:
            return "Niska skuteczność"
    
    def _generate_executive_summary(self, synthesis: Dict[str, Any]) -> str:
        """Generate executive summary"""
        summary_parts = []
        
        # Key findings
        if synthesis['key_findings']:
            summary_parts.append(f"Zidentyfikowano {len(synthesis['key_findings'])} kluczowych trendów.")
        
        # Efficiency
        if synthesis['efficiency_insights']:
            summary_parts.append("Analiza efektywności ujawniła kluczowe metryki wydajności.")
        
        # Recommendations
        if synthesis['recommendations']:
            summary_parts.append(f"Sformułowano {len(synthesis['recommendations'])} rekomendacji.")
        
        return " ".join(summary_parts) if summary_parts else "Analiza przeprowadzona zgodnie z metodologią 7 faz."
