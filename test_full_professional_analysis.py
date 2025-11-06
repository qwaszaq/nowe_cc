#!/usr/bin/env python3
"""
Full Professional Analysis Test
Uruchamia pełną analizę CBA przez lokalny system i ocenia jakość
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from src.autonomous.autonomous_orchestrator import AutonomousOrchestrator


def run_full_analysis():
    """Uruchom pełną analizę CBA"""
    print("=" * 80)
    print("🚀 PEŁNA ANALIZA CBA - LOKALNY SYSTEM")
    print("=" * 80)
    print()
    
    # Sprawdź dostępność folderu
    test_folder = Path("testdocsLLM")
    if not test_folder.exists():
        print(f"❌ Folder {test_folder} nie istnieje!")
        return None
    
    cba_files = list(test_folder.glob("*CBA*.pdf")) + list(test_folder.glob("*cba*.pdf"))
    print(f"📂 Znaleziono {len(cba_files)} plików CBA")
    
    if len(cba_files) == 0:
        print("⚠️  Brak plików CBA w folderze")
        return None
    
    print("\n" + "=" * 80)
    print("INICJALIZACJA SYSTEMU")
    print("=" * 80)
    print()
    
    try:
        # Utwórz orchestrator
        orchestrator = AutonomousOrchestrator(enable_investigative=True)
        
        print("\n" + "=" * 80)
        print("URUCHAMIANIE ANALIZY")
        print("=" * 80)
        print()
        
        start_time = time.time()
        
        # Uruchom analizę
        results = orchestrator.process_folder(
            folder_path=str(test_folder.absolute()),
            case_id=f"professional_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        )
        
        duration = time.time() - start_time
        
        print("\n" + "=" * 80)
        print("ANALIZA ZAKOŃCZONA")
        print("=" * 80)
        print(f"⏱️  Czas wykonania: {duration:.1f}s ({duration/60:.1f} min)")
        print()
        
        return results, duration, orchestrator
        
    except Exception as e:
        print(f"\n❌ Błąd podczas analizy: {e}")
        import traceback
        traceback.print_exc()
        return None, 0, None


def analyze_quality(results, duration, orchestrator):
    """Przeanalizuj jakość wyników"""
    print("\n" + "=" * 80)
    print("📊 ANALIZA JAKOŚCI WYNIKÓW")
    print("=" * 80)
    print()
    
    if not results:
        print("❌ Brak wyników do analizy")
        return None
    
    quality_report = {
        'timestamp': datetime.now().isoformat(),
        'duration_seconds': duration,
        'summary': results.get('summary', {}),
        'professional_analysis': {},
        'quality_metrics': {},
        'issues': [],
        'recommendations': [],
    }
    
    # 1. Sprawdź czy Professional Analyzer został użyty
    professional_analysis_found = False
    professional_results = {}
    
    task_results = results.get('task_results', [])
    for task_result in task_results:
        agent_results = task_result.get('agent_results', [])
        for agent_result in agent_results:
            # Sprawdź w professional_analysis field
            if 'professional_analysis' in agent_result:
                prof_data = agent_result['professional_analysis']
                if isinstance(prof_data, dict):
                    professional_analysis_found = True
                    professional_results = prof_data
                    break
            
            # Sprawdź też w nazwie agenta i analysis_phase
            agent_name = agent_result.get('agent', '')
            if 'professional' in agent_name.lower():
                professional_analysis_found = True
                analysis_phase = agent_result.get('analysis_phase', '')
                if analysis_phase:
                    if analysis_phase not in professional_results:
                        professional_results[analysis_phase] = {}
                    professional_results[analysis_phase]['output'] = agent_result.get('output', '')
        
        # Sprawdź też w głównym task_result
        if 'professional_analysis' in task_result:
            prof_data = task_result['professional_analysis']
            if isinstance(prof_data, dict):
                professional_analysis_found = True
                professional_results = prof_data
                break
    
    quality_report['professional_analysis'] = {
        'was_used': professional_analysis_found,
        'phases_found': len(professional_results),
        'results': professional_results
    }
    
    print("1️⃣ PROFESSIONAL ANALYZER:")
    print(f"   {'✅ Użyty' if professional_analysis_found else '❌ Nie użyty'}")
    if professional_analysis_found:
        if isinstance(professional_results, dict):
            print(f"   Faz znalezionych: {len(professional_results)}")
            for phase in professional_results.keys():
                print(f"      - {phase}")
        else:
            print(f"   ⚠️  Professional results w nieoczekiwanym formacie: {type(professional_results)}")
            professional_results = {}  # Reset to empty dict
    
    # 2. Sprawdź jakość ekstrakcji danych
    print("\n2️⃣ EKSTRAKCJA DANYCH:")
    if professional_results:
        phase2 = professional_results.get('phase2', {})
        if isinstance(phase2, dict):
            metrics = phase2.get('metrics', {})
            if metrics:
                total_metrics = sum(len(m) for m in metrics.values())
                print(f"   ✅ Wyekstrahowano metryki dla {len(metrics)} lat")
                print(f"   📊 Łącznie {total_metrics} wartości metryk")
                quality_report['quality_metrics']['metrics_extracted'] = total_metrics
                quality_report['quality_metrics']['years_with_data'] = len(metrics)
            else:
                print("   ⚠️  Brak wyekstrahowanych metryk")
                quality_report['issues'].append("Brak wyekstrahowanych metryk w phase2")
        else:
            print("   ⚠️  Phase2 nie zawiera danych w oczekiwanym formacie")
            quality_report['issues'].append("Phase2 format issue")
    else:
        print("   ❌ Brak danych z Professional Analyzer")
        quality_report['issues'].append("Professional Analyzer nie został uruchomiony")
    
    # 3. Sprawdź analizę jakościową
    print("\n3️⃣ ANALIZA JAKOŚCIOWA:")
    if professional_results:
        phase3 = professional_results.get('phase3', {})
        if isinstance(phase3, dict):
            narrative = phase3.get('narrative_analysis', {})
            if narrative:
                print(f"   ✅ Przeanalizowano {len(narrative)} dokumentów")
                quality_report['quality_metrics']['qualitative_analysis'] = len(narrative)
            else:
                print("   ⚠️  Brak analizy jakościowej")
        else:
            print("   ⚠️  Phase3 nie zawiera danych")
    else:
        print("   ❌ Brak danych")
    
    # 4. Sprawdź trendy temporalne
    print("\n4️⃣ TRENDY TEMPORALNE:")
    if professional_results:
        phase4 = professional_results.get('phase4', {})
        if isinstance(phase4, dict):
            trends = phase4.get('trends', {})
            if trends:
                print(f"   ✅ Przeanalizowano {len(trends)} trendów")
                quality_report['quality_metrics']['trends_analyzed'] = len(trends)
                for metric_name, trend_data in list(trends.items())[:3]:
                    trend = trend_data.get('trend', 'unknown')
                    growth = trend_data.get('total_growth', 0)
                    print(f"      - {metric_name}: {trend} ({growth:.1f}%)")
            else:
                print("   ⚠️  Brak trendów")
        else:
            print("   ⚠️  Phase4 nie zawiera danych")
    else:
        print("   ❌ Brak danych")
    
    # 5. Sprawdź syntezę wniosków
    print("\n5️⃣ SYNTEZA WNIOSKÓW:")
    if professional_results:
        phase7 = professional_results.get('phase7', {})
        if isinstance(phase7, dict):
            findings = phase7.get('key_findings', [])
            recommendations = phase7.get('recommendations', [])
            if findings:
                print(f"   ✅ {len(findings)} kluczowych wniosków")
                quality_report['quality_metrics']['key_findings'] = len(findings)
            if recommendations:
                print(f"   ✅ {len(recommendations)} rekomendacji")
                quality_report['quality_metrics']['recommendations'] = len(recommendations)
        else:
            print("   ⚠️  Phase7 nie zawiera danych")
    else:
        print("   ❌ Brak danych")
    
    # 6. Ogólna ocena jakości
    print("\n6️⃣ OCENA OGÓLNA:")
    
    quality_score = 0
    max_score = 5
    
    if professional_analysis_found:
        quality_score += 1
        print("   ✅ Professional Analyzer uruchomiony")
    else:
        print("   ❌ Professional Analyzer nie uruchomiony")
        quality_report['issues'].append("Professional Analyzer nie został uruchomiony")
    
    if quality_report['quality_metrics'].get('metrics_extracted', 0) > 0:
        quality_score += 1
        print("   ✅ Dane ilościowe wyekstrahowane")
    else:
        print("   ❌ Brak danych ilościowych")
    
    if quality_report['quality_metrics'].get('trends_analyzed', 0) > 0:
        quality_score += 1
        print("   ✅ Trendy temporalne przeanalizowane")
    else:
        print("   ⚠️  Brak analizy trendów")
    
    if quality_report['quality_metrics'].get('key_findings', 0) > 0:
        quality_score += 1
        print("   ✅ Wnioski wygenerowane")
    else:
        print("   ⚠️  Brak wniosków")
    
    if len(quality_report['issues']) == 0:
        quality_score += 1
        print("   ✅ Brak krytycznych problemów")
    else:
        print(f"   ⚠️  Znaleziono {len(quality_report['issues'])} problemów")
    
    quality_percentage = (quality_score / max_score) * 100
    quality_report['quality_score'] = quality_score
    quality_report['quality_percentage'] = quality_percentage
    
    print(f"\n   📊 OCENA JAKOŚCI: {quality_score}/{max_score} ({quality_percentage:.0f}%)")
    
    # Rekomendacje
    print("\n7️⃣ REKOMENDACJE:")
    if not professional_analysis_found:
        quality_report['recommendations'].append("Sprawdź czy Professional Analyzer jest poprawnie zintegrowany")
    if quality_report['quality_metrics'].get('metrics_extracted', 0) == 0:
        quality_report['recommendations'].append("Poprawić ekstrakcję danych ilościowych")
    if quality_report['quality_metrics'].get('trends_analyzed', 0) == 0:
        quality_report['recommendations'].append("Sprawdzić analizę trendów temporalnych")
    
    for rec in quality_report['recommendations']:
        print(f"   - {rec}")
    
    # Zapisz raport jakości
    report_path = f"quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(quality_report, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n✅ Raport jakości zapisany: {report_path}")
    
    # Zapisz pełne wyniki
    results_path = f"full_analysis_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"✅ Pełne wyniki zapisane: {results_path}")
    
    return quality_report


def main():
    """Main execution"""
    print("\n" + "=" * 80)
    print("🔍 TEST PEŁNEJ ANALIZY I OCENY JAKOŚCI")
    print("=" * 80)
    print()
    
    # Uruchom analizę
    result = run_full_analysis()
    
    if result is None:
        print("\n❌ Nie udało się uruchomić analizy")
        return 1
    
    results, duration, orchestrator = result
    
    # Przeanalizuj jakość
    quality_report = analyze_quality(results, duration, orchestrator)
    
    print("\n" + "=" * 80)
    print("✅ TEST ZAKOŃCZONY")
    print("=" * 80)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
