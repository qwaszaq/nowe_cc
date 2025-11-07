"""
Phase 4: Temporal Trend Analysis
"""

from typing import Dict, List, Any, Optional
try:
    from scipy import stats
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False


class TemporalTrendAnalyzer:
    """Analyze temporal trends in metrics"""
    
    def analyze(self, quantitative_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze trends in quantitative metrics"""
        
        metrics = quantitative_data.get('metrics', {})
        if not metrics:
            return {}
        
        trends = {}
        
        # For each metric, calculate trends
        metric_names = set()
        for year_data in metrics.values():
            metric_names.update(year_data.keys())
        
        for metric_name in metric_names:
            values = []
            years = []
            
            for year in sorted(metrics.keys()):
                if isinstance(year, int) and metric_name in metrics[year]:
                    value = metrics[year][metric_name].get('value')
                    if value is not None:
                        values.append(value)
                        years.append(year)
            
            if len(values) >= 2:
                trend_data = self._calculate_trend(years, values, metric_name)
                trends[metric_name] = trend_data
        
        return {
            'trends': trends,
            'summary': self._create_trend_summary(trends),
        }
    
    def _calculate_trend(self, years: List[int], values: List[float], metric_name: str) -> Dict[str, Any]:
        """Calculate trend for a metric"""
        
        # Basic statistics
        first_value = values[0]
        last_value = values[-1]
        total_growth = ((last_value - first_value) / first_value * 100) if first_value > 0 else 0
        
        # CAGR (Compound Annual Growth Rate)
        years_diff = years[-1] - years[0]
        if years_diff > 0 and first_value > 0:
            cagr = (((last_value / first_value) ** (1 / years_diff)) - 1) * 100
        else:
            cagr = 0
        
        # Linear regression for trend direction (used as secondary indicator)
        # PRIMARY indicator: total_growth (first to last value)
        # SECONDARY indicator: slope from regression (only if strong correlation)
        if len(years) >= 3 and SCIPY_AVAILABLE:
            try:
                slope, intercept, r_value, p_value, std_err = stats.linregress(years, values)
                trend_strength = abs(r_value)  # Correlation coefficient
            except:
                slope = (last_value - first_value) / years_diff if years_diff > 0 else 0
                trend_strength = 0
        else:
            slope = (last_value - first_value) / years_diff if years_diff > 0 else 0
            trend_strength = 0
        
        # Determine trend direction: Use total_growth as primary, slope as secondary
        # Only use slope if correlation is strong (r > 0.7) AND it agrees with total_growth
        growth_threshold = 5.0  # Minimum % change to be considered significant
        max_growth_threshold = 1000.0  # Maximum reasonable growth (sanity check)
        
        # Sanity check: flag unrealistic growth values
        is_unrealistic = abs(total_growth) > max_growth_threshold
        
        if abs(total_growth) < growth_threshold:
            trend_direction = 'stable'
        elif total_growth > 0:
            # Growth is positive - check if slope agrees (for validation)
            if trend_strength > 0.7 and slope < 0:
                # Inconsistency: positive growth but negative slope - trust growth
                trend_direction = 'increasing'
            else:
                trend_direction = 'increasing'
        else:
            # Growth is negative - check if slope agrees (for validation)
            if trend_strength > 0.7 and slope > 0:
                # Inconsistency: negative growth but positive slope - trust growth
                trend_direction = 'decreasing'
            else:
                trend_direction = 'decreasing'
        
        # Identify inflection points (if significant)
        inflection_points = self._find_inflection_points(years, values)
        
        return {
            'years': years,
            'values': values,
            'first_value': first_value,
            'last_value': last_value,
            'total_growth': total_growth,
            'cagr': cagr,
            'trend': trend_direction,
            'trend_strength': trend_strength,
            'slope': slope,
            'inflection_points': inflection_points,
            'is_unrealistic_growth': is_unrealistic,
            'growth_flag': 'unrealistic' if is_unrealistic else 'normal',
        }
    
    def _find_inflection_points(self, years: List[int], values: List[float]) -> List[Dict[str, Any]]:
        """Find inflection points in time series"""
        if len(values) < 3:
            return []
        
        inflection_points = []
        
        for i in range(1, len(values) - 1):
            prev_change = values[i] - values[i-1]
            next_change = values[i+1] - values[i]
            
            # Sign change indicates inflection
            if (prev_change > 0 and next_change < 0) or (prev_change < 0 and next_change > 0):
                inflection_points.append({
                    'year': years[i],
                    'value': values[i],
                    'type': 'peak' if prev_change > 0 else 'trough',
                })
        
        return inflection_points
    
    def _create_trend_summary(self, trends: Dict[str, Dict]) -> Dict[str, Any]:
        """Create summary of all trends"""
        increasing = [name for name, data in trends.items() if data['trend'] == 'increasing']
        decreasing = [name for name, data in trends.items() if data['trend'] == 'decreasing']
        stable = [name for name, data in trends.items() if data['trend'] == 'stable']
        
        return {
            'total_metrics': len(trends),
            'increasing': len(increasing),
            'decreasing': len(decreasing),
            'stable': len(stable),
            'metrics_increasing': increasing,
            'metrics_decreasing': decreasing,
        }
