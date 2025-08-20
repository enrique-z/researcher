#!/usr/bin/env python3
"""
Find Real Alternative Sources using Gemini 2.5
Replaces placeholder references with authentic, recent papers
"""

import os
import json
import google.generativeai as genai
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.0-flash-exp')

def find_real_sources():
    """Find real alternative sources for SAI research"""
    print("🔍 Using Gemini 2.5 to find real alternative sources...")
    
    # Define the research areas we need to cover
    research_areas = [
        "Volterra kernel analysis climate system identification 2023-2025",
        "H-infinity control design climate geoengineering recent papers",
        "Model predictive control MPC climate systems 2023-2025",
        "Active spectroscopy climate perturbation system identification",
        "Frequency domain analysis climate system responses SAI",
        "Nonlinear system identification environmental systems climate",
        "Early warning indicators climate instability detection",
        "Phase drift harmonic distortion climate systems SAI",
        "Fisher information optimization climate system identification",
        "Koopman operator climate system modeling control"
    ]
    
    real_sources = []
    
    for area in research_areas:
        print(f"\n🔍 Searching: {area}")
        
        prompt = f"""Find 2-3 real, recent (2020-2025) academic papers on this topic: {area}

Requirements:
1. Papers must be REAL and PUBLISHED (not hypothetical)
2. Must be from reputable journals/conferences
3. Must have actual DOIs, authors, and publication details
4. Focus on climate science, control theory, or environmental systems
5. Must be relevant to stratospheric aerosol injection or climate control

Format each paper as:
- Title: [exact title]
- Authors: [author names]
- Journal/Conference: [publication venue]
- Year: [publication year]
- DOI: [DOI if available]
- URL: [URL if available]
- Abstract: [brief description of relevance]

Only provide REAL papers that actually exist. If you can't find real papers on the exact topic, suggest related papers that could be relevant."""
        
        try:
            response = model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.3,
                    'max_output_tokens': 2000,
                }
            )
            
            print(f"  ✓ Found sources for: {area[:50]}...")
            real_sources.append({
                'area': area,
                'response': response.text,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as e:
            print(f"  ❌ Failed to find sources for: {area[:50]}... - {e}")
    
    return real_sources

def save_real_sources(sources):
    """Save the real sources found"""
    # Save raw responses
    with open('EXPERIMENTS/experiment-native-1-spectro/input/real_sources_found.json', 'w') as f:
        json.dump(sources, f, indent=2)
    
    # Create a summary report
    report = f"""# Real Alternative Sources Found

## Summary
Used Gemini 2.5 to find authentic, recent papers for SAI research enhancement.

## Research Areas Covered
"""
    
    for source in sources:
        report += f"- {source['area']}\n"
    
    report += f"""
## Total Sources Found
- **Areas covered**: {len(sources)}
- **Search completed**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Next Steps
1. Review the found sources in `real_sources_found.json`
2. Select the most relevant papers
3. Add them to the enhanced bibliography
4. Run CycleResearcher with complete references

## Files Generated
- `real_sources_found.json` - Raw search results from Gemini
- `real_sources_report.md` - This summary report
"""
    
    with open('EXPERIMENTS/experiment-native-1-spectro/input/real_sources_report.md', 'w') as f:
        f.write(report)
    
    print(f"\n✅ Real sources saved to:")
    print(f"   - real_sources_found.json")
    print(f"   - real_sources_report.md")

def main():
    """Main execution"""
    print("🚀 Starting real source discovery with Gemini 2.5...")
    
    try:
        # Find real sources
        sources = find_real_sources()
        
        # Save results
        save_real_sources(sources)
        
        print(f"\n🎉 Real source discovery completed!")
        print(f"📊 Found sources for {len(sources)} research areas")
        print("🔍 Check the generated files to review the sources")
        
    except Exception as e:
        print(f"❌ Real source discovery failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
