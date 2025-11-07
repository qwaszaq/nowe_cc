"""
Phase 5: Comparative & Contextual Analysis
"""

from typing import Dict, List, Any
from collections import defaultdict


class ComparativeAnalyzer:
    """Perform comparative analysis"""
    
    def analyze(self, quantitative_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comparative analysis"""
        
        metrics = quantitative_data.get('metrics', {})
        if not metrics:
            return {}
        
        comparative = {
            'efficiency_metrics': {},
            'periods': {},
            'correlations': {},
        }
        
        # Calculate efficiency metrics
        for year in sorted(metrics.keys()):
            if not isinstance(year, int):
                continue
                
            year_data = metrics[year]
            
            efficiency = {}
            
            # Success rate
            if 'sprawy_operacyjne' in year_data and 'skazania' in year_data:
                sprawy = year_data['sprawy_operacyjne'].get('value')
                skazania = year_data['skazania'].get('value')
                if sprawy and skazania and sprawy > 0:
                    efficiency['success_rate'] = (skazania / sprawy) * 100
            
            # Budget efficiency
            if 'budzet' in year_data and 'sprawy_operacyjne' in year_data:
                budzet = year_data['budzet'].get('value')
                sprawy = year_data['sprawy_operacyjne'].get('value')
                if budzet and sprawy and sprawy > 0:
                    efficiency['cost_per_case'] = budzet / sprawy
            
            # Employee productivity
            if 'funkcjonariusze' in year_data and 'sprawy_operacyjne' in year_data:
                funkcjonariusze = year_data['funkcjonariusze'].get('value')
                sprawy = year_data['sprawy_operacyjne'].get('value')
                if funkcjonariusze and sprawy and funkcjonariusze > 0:
                    efficiency['cases_per_employee'] = sprawy / funkcjonariusze
            
            if efficiency:
                comparative['efficiency_metrics'][year] = efficiency
        
        # Periodization
        years = sorted([y for y in metrics.keys() if isinstance(y, int)])
        if len(years) >= 4:
            mid_point = len(years) // 2
            comparative['periods'] = {
                'early': years[:mid_point],
                'recent': years[mid_point:],
                'comparison': self._compare_periods(years[:mid_point], years[mid_point:], metrics),
            }
        
        # Calculate correlations
        comparative['correlations'] = self._calculate_correlations(metrics)
        
        return comparative
    
    def _compare_periods(self, early_years: List[int], recent_years: List[int], 
                        metrics: Dict[int, Dict]) -> Dict[str, Any]:
        """Compare early vs recent periods"""
        
        comparison = {}
        
        # Aggregate metrics for each period
        early_metrics = defaultdict(list)
        recent_metrics = defaultdict(list)
        
        for year in early_years:
            if year in metrics:
                for metric_name, metric_data in metrics[year].items():
                    value = metric_data.get('value')
                    if value is not None:
                        early_metrics[metric_name].append(value)
        
        for year in recent_years:
            if year in metrics:
                for metric_name, metric_data in metrics[year].items():
                    value = metric_data.get('value')
                    if value is not None:
                        recent_metrics[metric_name].append(value)
        
        # Calculate averages and changes
        for metric_name in set(early_metrics.keys()) | set(recent_metrics.keys()):
            early_avg = sum(early_metrics[metric_name]) / len(early_metrics[metric_name]) if early_metrics[metric_name] else 0
            recent_avg = sum(recent_metrics[metric_name]) / len(recent_metrics[metric_name]) if recent_metrics[metric_name] else 0
            
            if early_avg > 0:
                change = ((recent_avg - early_avg) / early_avg) * 100
            else:
                change = 100 if recent_avg > 0 else 0
            
            comparison[metric_name] = {
                'early_avg': early_avg,
                'recent_avg': recent_avg,
                'change': change,
            }
        
        return comparison
    
    def _calculate_correlations(self, metrics: Dict[int, Dict]) -> Dict[str, float]:
        """Calculate correlations between metrics"""
        # This would require more sophisticated analysis
        # For now, return placeholder
        return {}
