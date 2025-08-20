# Researcher - Quick Start Guide

## ✅ Installation Complete!

Your Researcher codebase has been successfully installed and configured.

## 🚀 Getting Started

### 1. Activate the Environment
```bash
source activate    # Activate virtual environment
deactivate         # Deactivate when done
```

### 2. Test Your Installation
```bash
python test_installation.py
```

### 3. Basic Usage Examples

#### CycleResearcher (Paper Generation)
```python
from ai_researcher import CycleResearcher

# Initialize with your local model
researcher = CycleResearcher(
    model_path="/Users/apple/code/Researcher/westlake-12b",
    model_size="12B"
)

# Load references (BibTeX format)
with open('Tutorial/cycleresearcher_references.bib', 'r') as f:
    references = f.read()

# Generate paper
papers = researcher.generate_paper(
    topic="AI Research",
    references=references,
    n=1
)
```

#### CycleReviewer (Paper Review)
```python
from ai_researcher import CycleReviewer

# Initialize reviewer
reviewer = CycleReviewer(model_size="8B")

# Review a paper
with open('path/to/paper.txt', 'r') as f:
    paper_text = f.read()

review_results = reviewer.evaluate(paper_text)
print(f"Average score: {review_results[0]['avg_rating']}")
```

#### DeepReviewer (Multi-perspective Review)
```python
from ai_researcher import DeepReviewer

# Initialize deep reviewer
deep_reviewer = DeepReviewer(model_size="14B")

# Multi-perspective review
review_results = deep_reviewer.evaluate(
    paper_text,
    mode="Standard Mode",
    reviewer_num=4
)
```

### 4. Available Tutorials

Check the `Tutorial/` directory for comprehensive examples:
- `tutorial_1.ipynb` - Getting Started with CycleResearcher
- `tutorial_2.ipynb` - Understanding CycleReviewer  
- `tutorial_3.ipynb` - Mastering DeepReviewer

### 5. OpenScholar Setup (Optional)

For the RAG-based research system:

1. Get a Semantic Scholar API key from https://www.semanticscholar.org/product/api
2. Start model services:
   ```bash
   cd OpenScholar
   ./start_models.sh
   ```
3. Configure and start API:
   ```bash
   python openscholar_api.py --s2_api_key YOUR_API_KEY --reranker_path OpenSciLM/OpenScholar_Reranker
   ```

## 📁 Key Directories

- **westlake-12b/** - Your downloaded 12B model (ready to use)
- **Tutorial/** - Jupyter notebooks with examples
- **OpenScholar/** - RAG-based research Q&A system
- **ai_researcher/** - Core source code
- **.venv/** - Python virtual environment

## 🔧 Environment Details

- **Python**: 3.11.3
- **Virtual Environment**: `/Users/apple/code/Researcher/.venv`
- **Activation**: `source activate`
- **Deactivation**: `deactivate`

## 🎯 Key Features Installed

✅ **CycleResearcher**: AI-powered research paper generation  
✅ **CycleReviewer**: Automated peer review system  
✅ **DeepReviewer**: Multi-perspective review simulation  
✅ **AI Detection**: FastDetectGPT-based detection  
✅ **OpenScholar**: RAG-based research Q&A (with setup)  
✅ **Local Model**: Westlake-12B ready to use  

## 📚 Documentation

- Main README: `readme.md`
- OpenScholar Guide: `OpenScholar/README.md`
- License: `LICENSE.md`

## 🛠️ Troubleshooting

If you encounter issues:
1. Ensure you're in the virtual environment: `source activate`
2. Check the installation: `python test_installation.py`
3. For OpenScholar issues, check model logs in `OpenScholar/` directory
4. For API keys, ensure they're properly set in your `.env` file

---
**Happy Researching! 🎉**