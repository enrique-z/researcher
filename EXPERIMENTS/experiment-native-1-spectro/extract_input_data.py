#!/usr/bin/env python3
"""
Extract and process input data for experiment-native-1-spectro
"""
import json
import os
from datetime import datetime

def extract_experiment_data():
    """Extract and format data from the input package"""
    
    # Load the input package
    with open('input/researcher_input_package_20250811_145003.json', 'r') as f:
        input_data = json.load(f)
    
    # Extract key components
    research_topic = input_data['topic']
    bibtex_content = input_data['bibtex_content']
    original_idea = input_data['original_idea']
    
    # Create formatted experiment configuration
    experiment_config = {
        "experiment_name": "experiment-native-1-spectro",
        "start_time": datetime.now().isoformat(),
        "research_focus": "Active Spectroscopy Framework for Stratospheric Aerosol Injection",
        "core_hypothesis": original_idea['Short Hypothesis'],
        "expected_duration_hours": 4.5,
        "target_papers": 5,
        "quality_target": 5.0,
        "experimental_protocols": [
            "E1. Active probing design and identifiability",
            "E2. Frequency response and nonlinear distortion", 
            "E3. Robust control synthesis",
            "E4. Early-warning via phase drift and harmonic growth",
            "E5. Cross-model robustness",
            "E6. Practicality bounds"
        ],
        "technical_methods": [
            "Information-optimal probe signal design (multi-sine, PRBS, chirp)",
            "Frequency-domain system identification using spectral regression",
            "Second-order Volterra kernel estimation for nonlinear characterization",
            "H-infinity and MPC controller synthesis",
            "Fisher information maximization under environmental constraints",
            "Early-warning indicator development via phase drift analysis"
        ]
    }
    
    # Save processed data
    with open('input/experiment_config.json', 'w') as f:
        json.dump(experiment_config, f, indent=2)
    
    # Save formatted research topic
    with open('input/research_topic_formatted.txt', 'w') as f:
        f.write(research_topic)
    
    # Save BibTeX references  
    with open('input/references.bib', 'w') as f:
        f.write(bibtex_content)
        
    # Save experimental requirements
    with open('input/experimental_requirements.txt', 'w') as f:
        f.write("EXPERIMENTAL PROTOCOL REQUIREMENTS:\n\n")
        for i, protocol in enumerate(experiment_config['experimental_protocols'], 1):
            f.write(f"{i}. {protocol}\n")
        
        f.write("\n\nTECHNICAL METHODOLOGY REQUIREMENTS:\n\n")
        for i, method in enumerate(experiment_config['technical_methods'], 1):
            f.write(f"{i}. {method}\n")
    
    return experiment_config, research_topic, bibtex_content

if __name__ == "__main__":
    config, topic, refs = extract_experiment_data()
    print("✅ Input data extracted successfully!")
    print(f"📋 Research Topic: {config['research_focus']}")
    print(f"📚 References: {len(refs.split('@')) - 1} papers")
    print(f"🎯 Target: {config['target_papers']} papers in {config['expected_duration_hours']} hours")
    print(f"📊 Quality Target: {config['quality_target']}/10")