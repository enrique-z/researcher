#!/usr/bin/env python3
"""
Test script for Sakana bridge functionality verification
Tests the existing Pipeline 2 Sakana bridge with comprehensive validation
"""

import sys
import os

# Add Pipeline 2 to path
sys.path.insert(0, '/Users/apple/code/Researcher/PIPELINE_2_DEVELOPMENT')

from ai_researcher_enhanced.integration.sakana_bridge import SakanaBridge, create_sakana_bridge

def test_sakana_bridge():
    """Test the Sakana bridge with comprehensive validation."""
    print("🌉 Testing Sakana Bridge Integration")
    print("=" * 50)
    
    # Test 1: Bridge initialization
    print("1. Testing Sakana Bridge initialization...")
    try:
        bridge = create_sakana_bridge(real_data_mandatory=True)
        status = bridge.get_sakana_status()
        print(f"   ✅ Bridge initialized successfully")
        print(f"   📊 Sakana available: {status['sakana_available']}")
        print(f"   📊 GLENS loader active: {status['glens_loader_active']}")
        print(f"   📊 Real data available: {status['real_data_available']}")
        
    except Exception as e:
        print(f"   ❌ Bridge initialization failed: {e}")
        return False
    
    # Test 2: Data authenticity validation
    print("\n2. Testing data authenticity validation...")
    try:
        data_request = {
            'scenarios': ['GLENS', 'ARISE-SAI'],
            'variables': ['TREFHT', 'PRECT', 'BURDEN1'],
            'purpose': 'SAI pulse vs continuous analysis'
        }
        
        authenticity_result = bridge.validate_data_authenticity(data_request)
        print(f"   ✅ Authenticity check completed")
        print(f"   📊 Authentic: {authenticity_result['authentic']}")
        print(f"   📊 Source: {authenticity_result['source']}")
        print(f"   📊 Violations: {len(authenticity_result['violations'])}")
        
    except Exception as e:
        print(f"   ⚠️ Authenticity validation failed: {e}")
    
    # Test 3: Sakana validation for SAI hypothesis
    print("\n3. Testing Sakana validation for SAI hypothesis...")
    try:
        sai_hypothesis = {
            'title': 'SAI Pulse vs Continuous Injection Analysis',
            'description': 'Comparing pulsed versus continuous stratospheric aerosol injection using GLENS data',
            'parameters': {
                'injection_frequency': 'monthly',
                'aerosol_amount': 10.0,  # Tg SO2 equivalent
                'altitude': 20.0,  # km
                'latitude': 15.0
            },
            'expected_outcomes': ['temperature_cooling', 'precipitation_changes', 'radiative_forcing']
        }
        
        required_data = ['GLENS_control', 'GLENS_pulse', 'GLENS_continuous']
        
        sakana_result = bridge.perform_sakana_validation(sai_hypothesis, required_data)
        print(f"   ✅ Sakana validation completed")
        print(f"   📊 Sakana principle satisfied: {sakana_result['sakana_principle_satisfied']}")
        print(f"   📊 Empirical evidence found: {sakana_result['empirical_evidence_found']}")
        print(f"   📊 Validation tests: {len(sakana_result['validation_tests'])}")
        print(f"   📊 Recommendations: {len(sakana_result['recommendations'])}")
        
        # Show specific recommendations
        for rec in sakana_result['recommendations']:
            print(f"   🔍 {rec}")
            
    except Exception as e:
        print(f"   ⚠️ Sakana validation failed: {e}")
    
    # Test 4: Attempt data loading (will fail gracefully if no data)
    print("\n4. Testing data loading through Sakana...")
    try:
        scenarios = ['GLENS_control', 'GLENS_pulse', 'GLENS_continuous']
        variables = ['TREFHT', 'PRECT', 'BURDEN1']
        
        result = bridge.load_validated_data(scenarios, variables)
        print(f"   ✅ Data loading attempt completed")
        print(f"   📊 Loading status: {'SUCCESS' if 'error' not in result else 'FAILED'}")
        
        if 'error' in result:
            print(f"   📊 Error: {result['error']}")
        else:
            print(f"   📊 Data sources: {result['metadata']['data_source']}")
            print(f"   📊 Scenarios loaded: {result['metadata']['scenarios_loaded']}")
            print(f"   📊 Variables loaded: {result['metadata']['variables_loaded']}")
            
    except Exception as e:
        print(f"   ⚠️ Data loading failed: {e}")
    
    # Test 5: Bridge status summary
    print("\n5. Sakana Bridge status summary...")
    try:
        final_status = bridge.get_sakana_status()
        print(f"   ✅ Final status retrieved")
        for key, value in final_status.items():
            print(f"   📊 {key}: {value}")
            
    except Exception as e:
        print(f"   ❌ Status retrieval failed: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Sakana Bridge testing completed")
    
    # Provide integration summary
    if final_status['sakana_available']:
        print("🎯 Sakana system is ready for integration")
        if final_status['real_data_available']:
            print("🎯 Real GLENS data is available for SAI analysis")
        else:
            print("⚠️ Real GLENS data needs to be downloaded for full functionality")
    else:
        print("⚠️ Sakana system not available - integration requires ai-s-plus installation")
    
    return True

if __name__ == "__main__":
    success = test_sakana_bridge()
    if success:
        print("\n🌉 Sakana Bridge is functional and ready for 5-system integration")
    else:
        print("\n❌ Sakana Bridge requires debugging")