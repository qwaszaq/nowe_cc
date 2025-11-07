"""
Phase 3: Qualitative Analysis
"""

import re
from typing import Dict, List, Any
from collections import defaultdict


class QualitativeAnalyzer:
    """Analyze qualitative aspects of documents"""
    
    def __init__(self):
        # Tone indicators
        self.tone_patterns = {
            'positive': [
                'sukces', 'osiągnięci', 'efektywn', 'poprawa', 
                'wzrost', 'rozwój', 'udan', 'pozytywn'
            ],
            'challenge': [
                'wyzwani', 'trudności', 'problem', 'ograniczen',
                'bariery', 'utrudnien', 'spadek'
            ],
            'cooperation': [
                'współprac', 'kooperacj', 'partnerstw', 'współdziałan',
                'koordynacj', 'wsparcie'
            ],
            'innovation': [
                'nowoczesn', 'innowacj', 'rozwój', 'modernizacj',
                'technolog', 'cyfrow', 'digitalizacj'
            ],
        }
        
        # Theme patterns
        self.theme_patterns = {
            'korupcja': ['korupcj', 'łapówk', 'przekup', 'antykorupcyjn'],
            'współpraca_międzynarodowa': ['międzynarodow', 'europejsk', 'unij', 'eu'],
            'szkolenia': ['szkoleni', 'kurs', 'edukacj', 'trening'],
            'technologia': ['technolog', 'cyfrow', 'system informatyczn', 'it'],
            'finansowanie': ['budżet', 'finansow', 'nakład', 'środki'],
        }
    
    def analyze(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform qualitative analysis"""
        
        narrative_analysis = {}
        
        for doc in documents:
            year = doc.get('year')
            text = doc.get('text', '')
            filename = doc.get('filename', '')
            
            if not text or len(text) < 100:
                continue
            
            text_lower = text.lower()
            
            # Analyze tone
            tone_scores = {}
            for tone, keywords in self.tone_patterns.items():
                score = sum(len(re.findall(kw, text_lower)) for kw in keywords)
                tone_scores[tone] = score
            
            # Analyze themes
            theme_scores = {}
            for theme, keywords in self.theme_patterns.items():
                score = sum(len(re.findall(kw, text_lower)) for kw in keywords)
                theme_scores[theme] = score
            
            # Determine dominant tone and theme
            dominant_tone = max(tone_scores.items(), key=lambda x: x[1])[0] if tone_scores else None
            dominant_theme = max(theme_scores.items(), key=lambda x: x[1])[0] if theme_scores else None
            
            key = year if year else filename
            
            narrative_analysis[key] = {
                'tone': tone_scores,
                'themes': theme_scores,
                'dominant_tone': dominant_tone,
                'dominant_theme': dominant_theme,
                'text_length': len(text),
            }
        
        # Cross-temporal analysis
        evolution = self._analyze_evolution(narrative_analysis)
        
        return {
            'narrative_analysis': narrative_analysis,
            'evolution': evolution,
        }
    
    def _analyze_evolution(self, narrative_analysis: Dict) -> Dict[str, Any]:
        """Analyze how tone and themes evolved"""
        if len(narrative_analysis) < 2:
            return {}
        
        # Filter only year-based keys
        year_analysis = {k: v for k, v in narrative_analysis.items() if isinstance(k, int)}
        
        if len(year_analysis) < 2:
            return {}
        
        years = sorted(year_analysis.keys())
        mid_point = len(years) // 2
        
        early_years = years[:mid_point]
        recent_years = years[mid_point:]
        
        # Average tone scores
        early_avg_tones = defaultdict(float)
        recent_avg_tones = defaultdict(float)
        
        for year in early_years:
            if year in year_analysis:
                for tone, score in year_analysis[year]['tone'].items():
                    early_avg_tones[tone] += score
        
        for year in recent_years:
            if year in year_analysis:
                for tone, score in year_analysis[year]['tone'].items():
                    recent_avg_tones[tone] += score
        
        # Normalize
        if early_years:
            early_avg_tones = {k: v / len(early_years) for k, v in early_avg_tones.items()}
        if recent_years:
            recent_avg_tones = {k: v / len(recent_years) for k, v in recent_avg_tones.items()}
        
        return {
            'early_period': dict(early_avg_tones),
            'recent_period': dict(recent_avg_tones),
            'changes': self._calculate_changes(early_avg_tones, recent_avg_tones),
        }
    
    def _calculate_changes(self, early: Dict, recent: Dict) -> Dict[str, float]:
        """Calculate changes between periods"""
        changes = {}
        all_keys = set(early.keys()) | set(recent.keys())
        
        for key in all_keys:
            early_val = early.get(key, 0)
            recent_val = recent.get(key, 0)
            if early_val > 0:
                change = ((recent_val - early_val) / early_val) * 100
            else:
                change = 100 if recent_val > 0 else 0
            changes[key] = change
        
        return changes
