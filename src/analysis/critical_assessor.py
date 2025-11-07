"""
Phase 6: Critical Assessment
"""

from typing import Dict, List, Any
from collections import defaultdict


class CriticalAssessor:
    """Perform critical assessment of data and analysis"""
    
    def assess(self, documents: List[Dict[str, Any]], analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Perform critical assessment"""
        
        assessment = {
            'data_completeness': {},
            'consistency_issues': [],
            'methodology_changes': [],
            'missing_years': [],
            'confidence_scores': {},
            'limitations': [],
        }
        
        # Check data completeness
        quantitative_data = analysis_results.get('phase2', {})
        metrics = quantitative_data.get('metrics', {})
        
        # Find all years mentioned in documents
        document_years = set()
        for doc in documents:
            year = doc.get('year')
            if year:
                document_years.add(year)
        
        # Expected years (if we know the range)
        if document_years:
            min_year = min(document_years)
            max_year = max(document_years)
            all_years = set(range(min_year, max_year + 1))
            missing_years = sorted(all_years - document_years)
            assessment['missing_years'] = missing_years
        
        # Check completeness per year
        for year in sorted(metrics.keys()):
            if isinstance(year, int):
                year_data = metrics[year]
                completeness = len([k for k in year_data.keys() if year_data[k].get('value') is not None]) / len(year_data) if year_data else 0
                assessment['data_completeness'][year] = completeness
        
        # Check consistency
        for year in sorted(metrics.keys()):
            if not isinstance(year, int):
                continue
                
            year_data = metrics[year]
            
            # Logical consistency checks
            if 'sprawy_operacyjne' in year_data and 'skazania' in year_data:
                sprawy = year_data['sprawy_operacyjne'].get('value')
                skazania = year_data['skazania'].get('value')
                
                if sprawy and skazania and skazania > sprawy:
                    assessment['consistency_issues'].append({
                        'year': year,
                        'issue': f'Skazania ({skazania}) > Sprawy ({sprawy})',
                        'type': 'logical_inconsistency',
                        'severity': 'high',
                    })
            
            if 'budzet' in year_data and 'sprawy_operacyjne' in year_data:
                budzet = year_data['budzet'].get('value')
                sprawy = year_data['sprawy_operacyjne'].get('value')
                
                if budzet and sprawy:
                    cost_per_case = budzet / sprawy
                    if cost_per_case > 10000000:  # > 10M per case seems unreasonable
                        assessment['consistency_issues'].append({
                            'year': year,
                            'issue': f'Cost per case ({cost_per_case:,.0f} zł) seems very high',
                            'type': 'anomaly',
                            'severity': 'medium',
                        })
        
        # Check for trend inconsistencies (from phase4)
        trend_data = analysis_results.get('phase4', {})
        trends = trend_data.get('trends', {})
        
        for metric_name, trend_info in trends.items():
            trend_direction = trend_info.get('trend', '')
            total_growth = trend_info.get('total_growth', 0)
            is_unrealistic = trend_info.get('is_unrealistic_growth', False)
            
            # Detect inconsistency: trend direction vs growth
            if trend_direction == 'increasing' and total_growth < 0:
                assessment['consistency_issues'].append({
                    'year': None,
                    'metric': metric_name,
                    'issue': f'Trend marked as "increasing" but growth is negative ({total_growth:.1f}%)',
                    'type': 'trend_inconsistency',
                    'severity': 'high',
                })
            elif trend_direction == 'decreasing' and total_growth > 0:
                assessment['consistency_issues'].append({
                    'year': None,
                    'metric': metric_name,
                    'issue': f'Trend marked as "decreasing" but growth is positive ({total_growth:.1f}%)',
                    'type': 'trend_inconsistency',
                    'severity': 'high',
                })
            
            # Flag unrealistic growth values
            if is_unrealistic:
                assessment['consistency_issues'].append({
                    'year': None,
                    'metric': metric_name,
                    'issue': f'Unrealistic growth value ({total_growth:.1f}%) - likely extraction error',
                    'type': 'unrealistic_value',
                    'severity': 'high',
                })
        
        # Identify limitations
        assessment['limitations'] = [
            'Analysis based on text extraction only (tables may contain additional data)',
            'Regex-based extraction may miss context',
            'No OCR for scanned documents',
            'No manual verification of extracted values',
            'Limited cross-validation between sources',
        ]
        
        # Calculate overall confidence
        if metrics:
            year_metrics = {k: v for k, v in metrics.items() if isinstance(k, int)}
            if year_metrics and assessment['data_completeness']:
                avg_completeness = sum(assessment['data_completeness'].values()) / len(assessment['data_completeness'])
                consistency_score = 1.0 - (len(assessment['consistency_issues']) / len(year_metrics) * 0.5)
                overall_confidence = (avg_completeness * 0.7 + consistency_score * 0.3)
                
                assessment['overall_confidence'] = overall_confidence
        
        return assessment
