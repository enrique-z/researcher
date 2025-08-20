#!/usr/bin/env python3
"""
Test script to verify Researcher installation
"""

def test_imports():
    """Test all required imports"""
    print("🧪 Testing imports...")
    
    # Core dependencies
    try:
        import torch
        print(f"✅ PyTorch {torch.__version__}")
    except ImportError as e:
        print(f"❌ PyTorch import failed: {e}")
        return False
    
    try:
        import transformers
        print(f"✅ Transformers {transformers.__version__}")
    except ImportError as e:
        print(f"❌ Transformers import failed: {e}")
        return False
    
    try:
        import vllm
        print(f"✅ vLLM {vllm.__version__}")
    except ImportError as e:
        print(f"❌ vLLM import failed: {e}")
        return False
        
    try:
        import bibtexparser
        print(f"✅ bibtexparser")
    except ImportError as e:
        print(f"❌ bibtexparser import failed: {e}")
        return False
    
    # AI Researcher components
    try:
        from ai_researcher.cycle_researcher import CycleResearcher
        print("✅ CycleResearcher")
    except ImportError as e:
        print(f"❌ CycleResearcher import failed: {e}")
        return False
    
    try:
        from ai_researcher.cycle_reviewer import CycleReviewer
        print("✅ CycleReviewer")
    except ImportError as e:
        print(f"❌ CycleReviewer import failed: {e}")
        return False
    
    try:
        from ai_researcher.deep_reviewer import DeepReviewer
        print("✅ DeepReviewer")
    except ImportError as e:
        print(f"❌ DeepReviewer import failed: {e}")
        return False
    
    # Optional components
    try:
        import flask
        print(f"✅ Flask (for OpenScholar)")
    except ImportError as e:
        print(f"⚠️ Flask not available (OpenScholar won't work): {e}")
    
    return True

def test_model_files():
    """Test that the westlake-12b model files are present"""
    print("\n🔍 Testing model files...")
    
    import os
    westlake_path = "/Users/apple/code/Researcher/westlake-12b"
    
    if not os.path.exists(westlake_path):
        print(f"❌ Model directory not found: {westlake_path}")
        return False
    
    print(f"✅ Model directory found: {westlake_path}")
    
    required_files = [
        'config.json',
        'tokenizer.json',
        'tokenizer_config.json',
        'model.safetensors.index.json'
    ]
    
    all_present = True
    for file in required_files:
        file_path = os.path.join(westlake_path, file)
        if os.path.exists(file_path):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} missing")
            all_present = False
    
    # Count model shards
    model_shards = [f for f in os.listdir(westlake_path) if f.startswith('model-') and f.endswith('.safetensors')]
    print(f"✅ Found {len(model_shards)} model shard files")
    
    return all_present

def test_basic_functionality():
    """Test basic functionality"""
    print("\n⚡ Testing basic functionality...")
    
    try:
        # Test BibTeX parsing
        import bibtexparser
        sample_bibtex = """
        @article{sample2024,
            title = {Sample Paper Title},
            author = {Author, A. and Author, B.},
            journal = {Journal Name},
            year = {2024},
            abstract = {This is a sample abstract.}
        }
        """
        bib_db = bibtexparser.loads(sample_bibtex)
        if len(bib_db.entries) > 0:
            print("✅ BibTeX parsing works")
        else:
            print("❌ BibTeX parsing failed")
            return False
            
    except Exception as e:
        print(f"❌ BibTeX test failed: {e}")
        return False
    
    return True

def main():
    """Main test function"""
    print("🚀 Researcher Installation Test")
    print("=" * 50)
    
    success = True
    
    # Test imports
    if not test_imports():
        success = False
    
    # Test model files
    if not test_model_files():
        success = False
    
    # Test basic functionality
    if not test_basic_functionality():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Installation is working correctly.")
        print("\n📝 Next steps:")
        print("1. Activate environment: source activate")
        print("2. Check tutorials in Tutorial/ directory")
        print("3. For OpenScholar, configure API keys and run: ./OpenScholar/start_models.sh")
        print("4. Use your westlake-12b model at: /Users/apple/code/Researcher/westlake-12b")
    else:
        print("❌ Some tests failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    main()