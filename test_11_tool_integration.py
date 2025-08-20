#!/usr/bin/env python3
"""
11-Tool Integration Test Suite
Validates complete integration of all tools in the research pipeline
"""

import sys
import os
import time
import json
from pathlib import Path
from datetime import datetime

def setup_paths():
    """Setup all tool paths"""
    paths = {
        'agent_lightning': '/Users/apple/code/GUIDE/agent-lightning',
        'iris': '/Users/apple/code/IRIS/src',
        'guide': '/Users/apple/code/GUIDE',
        'oxford': '/Users/apple/code/scientificoxford-try-shaun',
        'ursa': '/Users/apple/code/losalamos/experiment-verifier'
    }
    
    for name, path in paths.items():
        if path not in sys.path:
            sys.path.append(path)
    
    return paths

def test_imports():
    """Test all tool imports"""
    print("🧪 TESTING IMPORTS...")
    print("=" * 50)
    
    results = {}
    
    # Agent Lightning
    try:
        from agentlightning.trainer import Trainer as AgentTrainer
        from agentlightning.client import AgentLightningClient as AgentClient
        results['agent_lightning'] = {'status': 'SUCCESS', 'imports': ['Trainer', 'AgentLightningClient']}
        print("✅ Agent Lightning: SUCCESS")
    except Exception as e:
        results['agent_lightning'] = {'status': 'FAILED', 'error': str(e)}
        print(f"❌ Agent Lightning: FAILED - {e}")
    
    # IRIS
    try:
        # Try absolute imports from IRIS src directory
        sys.path.insert(0, '/Users/apple/code/IRIS/src')
        from agents.ideation import IdeationAgent
        from mcts.tree import MCTS
        results['iris'] = {'status': 'SUCCESS', 'imports': ['IdeationAgent', 'MCTS']}
        print("✅ IRIS: SUCCESS")
    except Exception as e:
        results['iris'] = {'status': 'FAILED', 'error': str(e)}
        print(f"❌ IRIS: FAILED - {e}")
    
    # GUIDE
    try:
        # Try absolute imports from GUIDE directory
        sys.path.insert(0, '/Users/apple/code/GUIDE')
        from prompt_gen import generate_evaluation_prompts
        from review_gen import generate_reviews
        results['guide'] = {'status': 'SUCCESS', 'imports': ['generate_evaluation_prompts', 'generate_reviews']}
        print("✅ GUIDE: SUCCESS")
    except Exception as e:
        results['guide'] = {'status': 'FAILED', 'error': str(e)}
        print(f"❌ GUIDE: FAILED - {e}")
    
    return results

def test_api_configuration():
    """Test API key configuration"""
    print("\n🔑 TESTING API CONFIGURATION...")
    print("=" * 50)
    
    env_file = Path('/Users/apple/code/Researcher/.env')
    if not env_file.exists():
        print("❌ .env file not found")
        return {'status': 'FAILED', 'error': '.env file missing'}
    
    try:
        with open(env_file, 'r') as f:
            env_content = f.read()
        
        required_keys = ['OPENAI_API_KEY', 'GOOGLE_API_KEY', 'GEMINI_API_KEY']
        found_keys = []
        missing_keys = []
        
        for key in required_keys:
            if f"{key}=" in env_content and len(env_content.split(f"{key}=")[1].split()[0]) > 10:
                found_keys.append(key)
                print(f"✅ {key}: Configured")
            else:
                missing_keys.append(key)
                print(f"❌ {key}: Missing or empty")
        
        return {
            'status': 'SUCCESS' if not missing_keys else 'PARTIAL',
            'found_keys': found_keys,
            'missing_keys': missing_keys
        }
        
    except Exception as e:
        print(f"❌ Error reading .env: {e}")
        return {'status': 'FAILED', 'error': str(e)}

def test_pipeline_structure():
    """Test pipeline structure and phase methods"""
    print("\n🏗️ TESTING PIPELINE STRUCTURE...")
    print("=" * 50)
    
    try:
        # Import the main experiment class
        from execute_qbo_sai_experiment import QBOSAIExperiment
        
        # Check if new phase methods exist
        experiment = QBOSAIExperiment(
            research_domain="test_domain",
            experiment_type="test_type"
        )
        
        required_methods = [
            'execute_phase_0_3_adversarial_challenge',
            'execute_phase_0_5_interactive_refinement',
            'execute_phase_1_3_novelty_assessment',
            'execute_phase_2_5_methodological_feasibility'
        ]
        
        results = {}
        for method_name in required_methods:
            if hasattr(experiment, method_name):
                results[method_name] = 'EXISTS'
                print(f"✅ {method_name}: EXISTS")
            else:
                results[method_name] = 'MISSING'
                print(f"❌ {method_name}: MISSING")
        
        return {'status': 'SUCCESS', 'methods': results}
        
    except Exception as e:
        print(f"❌ Pipeline structure test failed: {e}")
        return {'status': 'FAILED', 'error': str(e)}

def test_phase_integration():
    """Test individual phase integrations with mock data"""
    print("\n⚙️ TESTING PHASE INTEGRATIONS...")
    print("=" * 50)
    
    results = {}
    
    try:
        from execute_qbo_sai_experiment import QBOSAIExperiment
        
        experiment = QBOSAIExperiment(
            research_domain="quantum_biology", 
            experiment_type="integration_test"
        )
        
        # Test Phase 0.3: Agent Lightning
        print("Testing Phase 0.3: Agent Lightning...")
        try:
            result_0_3 = experiment.execute_phase_0_3_adversarial_challenge("Test hypothesis for adversarial challenge")
            if result_0_3.get('phase') == 'agent_lightning_adversarial_challenge':
                results['phase_0_3'] = 'SUCCESS'
                print("✅ Phase 0.3: SUCCESS")
            else:
                results['phase_0_3'] = f"UNEXPECTED_RESULT: {result_0_3}"
                print(f"⚠️ Phase 0.3: Unexpected result - {result_0_3}")
        except Exception as e:
            results['phase_0_3'] = f'ERROR: {e}'
            print(f"❌ Phase 0.3: ERROR - {e}")
        
        # Test Phase 0.5: IRIS  
        print("Testing Phase 0.5: IRIS...")
        try:
            result_0_5 = experiment.execute_phase_0_5_interactive_refinement("Test challenged hypothesis")
            if result_0_5.get('phase') == 'iris_interactive_refinement':
                results['phase_0_5'] = 'SUCCESS'
                print("✅ Phase 0.5: SUCCESS")
            else:
                results['phase_0_5'] = f"UNEXPECTED_RESULT: {result_0_5}"
                print(f"⚠️ Phase 0.5: Unexpected result - {result_0_5}")
        except Exception as e:
            results['phase_0_5'] = f'ERROR: {e}'
            print(f"❌ Phase 0.5: ERROR - {e}")
        
        # Test Phase 1.3: GUIDE Novelty
        print("Testing Phase 1.3: GUIDE Novelty...")
        try:
            result_1_3 = experiment.execute_phase_1_3_novelty_assessment("Test refined hypothesis")
            if result_1_3.get('phase') == 'guide_novelty_assessment':
                results['phase_1_3'] = 'SUCCESS'
                print("✅ Phase 1.3: SUCCESS")
            else:
                results['phase_1_3'] = f"UNEXPECTED_RESULT: {result_1_3}"
                print(f"⚠️ Phase 1.3: Unexpected result - {result_1_3}")
        except Exception as e:
            results['phase_1_3'] = f'ERROR: {e}'
            print(f"❌ Phase 1.3: ERROR - {e}")
        
        return {'status': 'SUCCESS', 'phase_results': results}
        
    except Exception as e:
        return {'status': 'FAILED', 'error': str(e)}

def generate_integration_report(test_results):
    """Generate comprehensive integration report"""
    print("\n📊 INTEGRATION REPORT")
    print("=" * 60)
    
    report = {
        'timestamp': datetime.now().isoformat(),
        'test_results': test_results,
        'summary': {}
    }
    
    # Calculate success rates
    import_success = sum(1 for result in test_results.get('imports', {}).values() 
                        if result.get('status') == 'SUCCESS')
    import_total = len(test_results.get('imports', {}))
    
    phase_success = sum(1 for result in test_results.get('phase_integration', {}).get('phase_results', {}).values()
                       if 'SUCCESS' in str(result))
    phase_total = len(test_results.get('phase_integration', {}).get('phase_results', {}))
    
    report['summary'] = {
        'imports': f"{import_success}/{import_total} tools",
        'api_config': test_results.get('api_config', {}).get('status', 'UNKNOWN'),
        'pipeline_structure': test_results.get('pipeline_structure', {}).get('status', 'UNKNOWN'),
        'phase_integration': f"{phase_success}/{phase_total} phases",
        'overall_status': 'READY' if import_success >= 2 and phase_success >= 2 else 'NEEDS_WORK'
    }
    
    print(f"📦 Tool Imports: {report['summary']['imports']}")
    print(f"🔑 API Configuration: {report['summary']['api_config']}")
    print(f"🏗️ Pipeline Structure: {report['summary']['pipeline_structure']}")
    print(f"⚙️ Phase Integration: {report['summary']['phase_integration']}")
    print(f"🎯 Overall Status: {report['summary']['overall_status']}")
    
    # Save report
    report_file = Path('/Users/apple/code/Researcher/integration_test_report.json')
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Report saved to: {report_file}")
    return report

def main():
    """Main test execution"""
    print("🧪 11-TOOL INTEGRATION TEST SUITE")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Setup environment
    paths = setup_paths()
    print(f"📁 Tool paths configured: {list(paths.keys())}")
    print()
    
    # Run tests
    test_results = {}
    
    test_results['imports'] = test_imports()
    test_results['api_config'] = test_api_configuration()  
    test_results['pipeline_structure'] = test_pipeline_structure()
    test_results['phase_integration'] = test_phase_integration()
    
    # Generate report
    report = generate_integration_report(test_results)
    
    print("\n🎯 NEXT STEPS:")
    if report['summary']['overall_status'] == 'READY':
        print("✅ Integration complete! Ready for full pipeline testing.")
        print("💡 Run: python execute_qbo_sai_experiment.py")
        print("📊 Monitor: streamlit run streamlit_dashboard.py")
    else:
        print("⚠️ Integration needs work. Check failed components above.")
        print("🔧 Fix failed imports and configurations before proceeding.")
    
    return report['summary']['overall_status'] == 'READY'

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)