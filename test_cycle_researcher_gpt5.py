#!/usr/bin/env python3
"""
Test CycleResearcher with gpt-5 (recommended approach)
"""

import os
from ai_researcher import CycleResearcher

def test_cycle_researcher_gpt5():
    """Test CycleResearcher with gpt-5"""
    
    # Check if OpenAI API key is available
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not found in environment")
        return
    
    print("Testing CycleResearcher with gpt-5...")
    
    # Initialize with gpt-5 (default)
    researcher = CycleResearcher(model_size="gpt-5", max_model_len=4000)
    
    print(f"Model: {researcher.model_name}")
    print(f"Using OpenAI: {researcher.use_openai}")
    print(f"Config: {researcher.model_config}")
    
    # Test with a simple topic
    topic = "QBO dynamics and stratospheric aerosol injection"
    
    print(f"\nGenerating paper on: {topic}")
    papers = researcher.generate_paper(
        topic=topic,
        max_tokens=1000,  # Small test
        n=1
    )
    
    print(f"\nGenerated {len(papers)} paper(s)")
    for i, paper in enumerate(papers):
        print(f"\nPaper {i+1}:")
        print(f"  Title: {paper.get('title', 'N/A')}")
        print(f"  Abstract: {paper.get('abstract', 'N/A')[:100]}...")
        print(f"  Content length: {len(paper.get('content', ''))}")

if __name__ == "__main__":
    test_cycle_researcher_gpt5()