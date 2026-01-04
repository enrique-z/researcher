# Researcher-bio2: AI-Powered Scientific Research Ecosystem

<div align="center">

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Mac%20M3%20%7C%20NVIDIA%20Linux-lightgrey.svg)](HARDWARE_REQUIREMENTS.md)
[![Status](https://img.shields.io/badge/status-Production%20Ready-success.svg)]()
[![Documentation](https://img.shields.io/badge/docs-Comprehensive-blue.svg)]()

**A comprehensive ecosystem for AI-powered academic research, review, and computational biology**

[Features](#-features) • [Quick Start](#-quick-start) • [Hardware](#-hardware-requirements) • [Documentation](#-documentation)

</div>

---

##  Quick Overview

**Researcher-bio2** is a production-ready AI-powered research ecosystem that automates:

- 📝 **Paper Generation** - GPT-5 powered 128+ page academic papers
- 🔍 **Multi-Perspective Review** - Comprehensive review with self-verification
- 🧬 **Protein Docking & Design** - BindCraft, HADDOCK3, Chai-1 integration
- 🧪 **Structure Prediction** - Boltz/Boltz2, OpenFold for protein structures
- ✅ **Domain-Agnostic Validation** - Universal validation across research fields
- 🔬 **Computational Biology** - Complete workflow for protein research

### Key Achievements

- ✅ **SP55 Customer Project** - 100% complete (10 targets, 50+ page report)
- ✅ **2 Published Papers** - NeurIPS 2025, NVIDIA PhysicsNeMo
- ✅ **9,510+ Development Sessions** - Comprehensive development history
- ✅ **Production Ready** - Mac M3 and NVIDIA Linux support
- ✅ **Anti-Fabrication Certified** - Zero tolerance for mock data

**Latest Documentation:** January 4, 2025 | **Version:** 2.0.0

---

##  Documentation Index

**Core Documentation:**
- **[REPRODUCIBILITY_GUIDE.md](REPRODUCIBILITY_GUIDE.md)** - Complete guide for reproducing all experiments
- **[HARDWARE_REQUIREMENTS.md](HARDWARE_REQUIREMENTS.md)** - Platform compatibility and requirements
- **[DEVELOPMENT_HISTORY.md](DEVELOPMENT_HISTORY.md)** - Calendarized timeline of development

**Phase 1 Analysis (8 documents):**
- [Core Package Inventory](analysis/01_core_package_inventory.md) - 95 Python modules
- [Framework Integration](analysis/02_framework_integration.md) - 10 frameworks documented
- [Experiments Catalog](analysis/03_experiments_catalog.md) - 17 experiment folders
- [Test File Audit](analysis/04_test_file_audit.md) - 22 test files
- [Hardware Requirements Analysis](analysis/05_hardware_requirements.md) - Detailed analysis
- [Claude Code History](analysis/06_claude_code_history_summary.md) - 9,510 sessions
- [Antigravity History](analysis/07_antigravity_history_detailed.md) - 8 conversations
- [Unfinished Sections](analysis/08_unfinished_sections_report.md) - Known issues

---

## 🔍 Overview (Original Documentation)

CycleResearcher is a comprehensive open-source ecosystem for AI-powered academic research and review. Our system features three integrated components:

- **CycleResearcher**: Generates high-quality research papers
- **CycleReviewer**: Provides detailed academic reviews
- **DeepReviewer**: Delivers multi-perspective review simulations with self-verification

By creating a complete feedback loop between research generation and evaluation, we aim to:

- 🤖 Automate academic research processes
- 📝 Provide rigorous, multi-perspective research reviews
- 🔄 Establish research-review feedback loops
- 🚀 Accelerate scientific discovery

<img src="img/method.png" alt="CycleResearcher Architecture" width="80%">

### Update:
[04/26/2025] We hosted [AI Co-scientist Discussion](https://ai-researcher.net/social-iclr-2025) in ICLR 2025, over 300 people gathered together!

[04/06/2025] We have collected 400 papers related to AI Scientists in our [Awesome-AI-Scientist GitHub repository](https://github.com/ResearAI/Awesome-AI-Scientist). If you're interested in this field, don't miss out!

[03/22/2025] We've just rolled out an exciting new feature for https://ai-researcher.net! 🎉 Now you can directly read arXiv papers with unprecedented ease! 📚✨ 

Transform any arXiv link from: `https://arxiv.org/abs/2503.08569` -> `https://ai-researcher.net/abs/2503.08569`


## 🔍 Overview

CycleResearcher is a comprehensive open-source ecosystem for AI-powered academic research and review. Our system features three integrated components:

- **CycleResearcher**: Generates high-quality research papers
- **CycleReviewer**: Provides detailed academic reviews
- **DeepReviewer**: Delivers multi-perspective review simulations with self-verification

By creating a complete feedback loop between research generation and evaluation, we aim to:

- 🤖 Automate academic research processes
- 📝 Provide rigorous, multi-perspective research reviews
- 🔄 Establish research-review feedback loops
- 🚀 Accelerate scientific discovery

<img src="img/method.png" alt="CycleResearcher Architecture" width="80%">

## 🚀 Getting Started

### Installation

```bash
pip install ai_researcher
```

### Using CycleResearcher

```python
# Import necessary libraries
from ai_researcher import CycleResearcher
from ai_researcher.utils import print_paper_summary

# Initialize CycleResearcher with the default 12B model
researcher = CycleResearcher(model_size="12B")

# Load references from BibTeX file
with open('cycleresearcher_references.bib', 'r') as f:
    references_content = f.read()

# Generate a paper with specific references
generated_papers = researcher.generate_paper(
    topic = "AI Researcher",
    references = references_content,
    n = 1  # Generate a single paper
)

# Print summary of generated paper
print_paper_summary(generated_papers[0])
```

### Using CycleReviewer

```python
# Import necessary libraries
from ai_researcher import CycleReviewer

# Initialize CycleReviewer with the default 8B model
reviewer = CycleReviewer(model_size="8B")

# Review a paper (assuming paper_text contains the paper content)
review_results = reviewer.evaluate(paper_text)

# Print review results
print(f"Average score: {review_results[0]['avg_rating']}")
print(f"Decision: {review_results[0]['paper_decision']}")
```

### Using DeepReviewer

```python
# Import necessary libraries
from ai_researcher import DeepReviewer

# Initialize DeepReviewer with 14B model
deep_reviewer = DeepReviewer(model_size="14B")

# Review a paper with multiple simulated reviewers in Standard Mode
review_results = deep_reviewer.evaluate(
    paper_text,
    mode="Standard Mode",  # Options: "Fast Mode", "Standard Mode", "Best Mode"
    reviewer_num=4         # Simulate 4 different reviewers
)

# Print review results
for i, review in enumerate(review_results[0]['reviews']):
    print(f"Reviewer {i+1} Rating: {review.get('rating', 'N/A')}")
    print(f"Reviewer {i+1} Summary: {review.get('summary', 'N/A')[:100]}...")
```

#### Launching DeepReviewer Best Mode

##### Using OpenScholar

OpenScholar is a retrieval-augmented generation-based academic research question-answering system. For detailed usage instructions, please refer to the [OpenScholar directory](./OpenScholar/).

##### Quick Start Guide for OpenScholar

1. **Apply for Semantic Scholar API Key**: Visit [Semantic Scholar API](https://www.semanticscholar.org/product/api)

2. **Start Model Services**:
   ```bash
   # For Linux/Mac users
   cd OpenScholar
   chmod +x start_models.sh
   ./start_models.sh
   ```

3. **Start API Service**:
   ```bash
   python openscholar_api.py \
       --s2_api_key YOUR_SEMANTIC_SCHOLAR_API_KEY \
       --reranker_path OpenSciLM/OpenScholar_Reranker
   ```

4. **Using the API**:
   ```python
   import requests
   
   # Send questions to OpenScholar API
   response = requests.post("http://localhost:38015/batch_ask", json={
       "questions": ["How do retrieval-augmented LMs perform in knowledge-intensive tasks?"]
   })
   
   result = response.json()
   print("OpenScholar Answer:", result["results"][0]["output"])
   ```

#### Best Mode
DeepReviewer's Best Mode provides the most comprehensive review experience, including background knowledge search, multi-reviewer simulation, and self-verification:

```python
# Use Best Mode for in-depth review
review_results = deep_reviewer.evaluate(
    paper_text,
    mode="Best Mode",      # Most comprehensive review mode
    reviewer_num=6,        # Simulate 6 different reviewers
    enable_search=True,    # Enable background knowledge search
    self_verification=True # Enable self-verification
)
```



<img src="img/deepreviewer.png" alt="DeepReviewer Architecture" width="80%">

## 📊 Model Evaluation

<div class="evaluation-grid">
  <div class="evaluation-card">
    <h3>CycleResearcher</h3>
    <img src="img/cycleresearcher.png" alt="CycleResearcher Evaluation" width="100%">
    <p>CycleResearcher-12B achieves an average score of 5.36, approaching the 5.69 average for conference-accepted papers and surpassing AI Scientist's score of 4.31.</p>
  </div>
  
  <div class="evaluation-card">
    <h3>CycleReviewer</h3>
    <img src="img/cyclereviewer.png" alt="CycleReviewer Evaluation" width="100%">
    <p>CycleReviewer outperforms both proprietary systems and human experts with a 48.77% reduction in Proxy MSE and a 26.89% reduction in Proxy MAE compared to human reviewers. With a decision accuracy of 74.24%, our model demonstrates a significant lead over other closed-source systems.</p>
  </div>
  
  <div class="evaluation-card">
    <h3>DeepReviewer</h3>
    <img src="img/deepreviewer.png" alt="DeepReviewer Evaluation" width="100%">
    <p>DeepReviewer provides multi-perspective simulation with self-verification, enabling more comprehensive and balanced feedback. It offers three distinct review modes: Fast Mode, Standard Mode, and Best Mode to accommodate different use cases.</p>
  </div>
</div>

## 🧠 Models & Datasets

### Models Overview

<details open>
<summary><b>CycleResearcher Models</b></summary>
<table>
  <tr>
    <th>Model Name</th>
    <th>Pre-training Language Model</th>
    <th>HF Link</th>
  </tr>
  <tr>
    <td>CycleResearcher-ML-12B</td>
    <td><a href="https://huggingface.co/mistralai/Mistral-Nemo-Instruct-2407">Mistral-Nemo-Instruct-2407</a></td>
    <td><a href="https://huggingface.co/WestlakeNLP/CycleResearcher-ML-12B">🤗 link</a></td>
  </tr>
  <tr>
    <td>CycleResearcher-ML-72B</td>
    <td><a href="https://huggingface.co/Qwen/Qwen2.5-72B-Instruct">Qwen2.5-72B-Instruct</a></td>
    <td><a href="https://huggingface.co/WestlakeNLP/CycleResearcher-ML-72B">🤗 link</a></td>
  </tr>
  <tr>
    <td>CycleResearcher-ML-123B</td>
    <td><a href="https://huggingface.co/mistralai/Mistral-Large-Instruct-2407">Mistral-Large-2</a></td>
    <td><a href="https://huggingface.co/WestlakeNLP/CycleResearcher-ML-123B">🤗 link</a></td>
  </tr>
</table>
</details>

<details open>
<summary><b>CycleReviewer Models</b></summary>
<table>
  <tr>
    <th>Model Name</th>
    <th>Pre-training Language Model</th>
    <th>HF Link</th>
  </tr>
  <tr>
    <td>CycleReviewer-ML-Llama3.1-8B</td>
    <td><a href="https://huggingface.co/meta-llama/Meta-Llama-3.1-8B-Instruct">Llama3.1-8B-Instruct</a></td>
    <td><a href="https://huggingface.co/WestlakeNLP/CycleReviewer-ML-Llama3.1-8B">🤗 link</a></td>
  </tr>
  <tr>
    <td>CycleReviewer-ML-Llama3.1-70B</td>
    <td><a href="https://huggingface.co/meta-llama/Meta-Llama-3.1-70B-Instruct">Llama3.1-70B-Instruct</a></td>
    <td><a href="https://huggingface.co/WestlakeNLP/CycleReviewer-ML-Llama3.1-70B">🤗 link</a></td>
  </tr>
  <tr>
    <td>CycleReviewer-ML-Pro-123B</td>
    <td><a href="https://huggingface.co/mistralai/Mistral-Large-Instruct-2407">Mistral-Large-2</a></td>
    <td><a href="https://huggingface.co/WestlakeNLP/CycleReviewer-ML-Pro-123B">🤗 link</a></td>
  </tr>
</table>
</details>

<details open>
<summary><b>DeepReviewer Models</b></summary>
<table>
  <tr>
    <th>Model Name</th>
    <th>Parameters</th>
    <th>HF Link</th>
  </tr>
  <tr>
    <td>DeepReviewer-7B</td>
    <td>7B</td>
    <td><a href="https://huggingface.co/WestlakeNLP/DeepReviewer-7B">🤗 link</a></td>
  </tr>
  <tr>
    <td>DeepReviewer-14B</td>
    <td>14B</td>
    <td><a href="https://huggingface.co/WestlakeNLP/DeepReviewer-14B">🤗 link</a></td>
  </tr>
</table>
</details>

### Datasets

<div align="center">
  <img src="img/dataset.png" alt="Datasets Overview" width="80%">
</div>

<table>
  <tr>
    <th>Dataset Name</th>
    <th>Train Data</th>
    <th>Test Data</th>
    <th>Description</th>
    <th>HF Link</th>
  </tr>
  <tr>
    <td>Review-5K</td>
    <td>4,189</td>
    <td>781</td>
    <td>Peer review dataset for CycleReviewer training</td>
    <td><a href="https://huggingface.co/datasets/WestlakeNLP/Review-5K">🤗 link</a></td>
  </tr>
  <tr>
    <td>Research-14K</td>
    <td>12,696</td>
    <td>802</td>
    <td>Research paper dataset for CycleResearcher training</td>
    <td><a href="https://huggingface.co/datasets/WestlakeNLP/Research-14K">🤗 link</a></td>
  </tr>
  <tr>
    <td>DeepReview-13K</td>
    <td>13,378</td>
    <td>1,286</td>
    <td>Multi-perspective review dataset for DeepReviewer training</td>
    <td><a href="https://huggingface.co/datasets/WestlakeNLP/DeepReview-13K">🤗 link</a></td>
  </tr>
</table>

## 💡 Features

### DeepReviewer Review Modes

DeepReviewer offers three distinct review modes to accommodate different use cases:

<div class="feature-cards">
  <div class="feature-card">
    <h4>🏃‍♂️ Fast Mode</h4>
    <p>Quick review generation for rapid feedback. Provides essential evaluation without multi-reviewer simulation.</p>
  </div>
  
  <div class="feature-card">
    <h4>🔄 Standard Mode</h4>
    <p>Default mode that simulates multiple reviewers and includes self-verification to ensure reliable assessments.</p>
  </div>
  
  <div class="feature-card">
    <h4>⭐ Best Mode</h4>
    <p>Most comprehensive mode with background knowledge search, multi-reviewer simulation, and self-verification for in-depth analysis.</p>
  </div>
</div>

### AI Detection

Detect if content was generated by AI models:

```python
from ai_researcher import AIDetector

# Initialize AI detector
detector = AIDetector(device='cpu')

# Analyze the generated paper
detection_result = detector.analyze_paper(paper)

print("Detection Results:")
print(f"Probability of AI generation: {detection_result['probability'] * 100:.2f}%")
print(f"Confidence Level: {detection_result['confidence_level']}")
```

## 📚 Tutorials and Demos

We have prepared comprehensive tutorials to help users understand and utilize our models:

- [Tutorial 1:](https://github.com/zhu-minjun/Researcher/blob/main/Tutorial/tutorial_1.ipynb) Getting Started with CycleResearcher 🚀
- [Tutorial 2:](https://github.com/zhu-minjun/Researcher/blob/main/Tutorial/tutorial_2.ipynb) Understanding CycleReviewer 📝
- [Tutorial 3:](https://github.com/zhu-minjun/Researcher/blob/main/Tutorial/tutorial_3.ipynb) Mastering DeepReviewer 🔍
- [Tutorial 4:](https://github.com/zhu-minjun/Researcher/blob/main/Tutorial/tutorial_4.ipynb) Creating an End-to-End Research Workflow 🔄

## 🚀 Experiment Input Enhancement System

### Overview
Our **Comprehensive Experiment Enhancement System** automatically analyzes and enhances any experiment input to ensure optimal CycleResearcher performance. The system works for ALL research domains automatically - no hardcoding required.

### Quick Start for Experiment Enhancement

#### 1. Setup Environment
```bash
# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements_enhancement.txt
```

#### 2. Prepare Your Experiment
Place your experiment data in the `EXPERIMENTS/` directory with this structure:
```
EXPERIMENTS/your-experiment-name/
├── input/
│   ├── experiment_config.json      # Experiment configuration
│   ├── research_topic_formatted.txt # Research topic description
│   ├── references.bib             # Initial bibliography
│   └── researcher_input_package_*.json # Input package
├── output/                        # Generated papers will go here
└── logs/                         # System logs
```

#### 3. Enhance Your Experiment Input
```bash
# Enhance the default experiment
python comprehensive_enhancer.py

# Or specify a custom experiment directory
python comprehensive_enhancer.py EXPERIMENTS/your-experiment-name
```

#### 4. Run CycleResearcher
```bash
# Navigate to experiment directory
cd EXPERIMENTS/your-experiment-name

# Run the experiment
python experiment_runner.py
```

### How the Enhancement System Works

#### What It Does Automatically:
1. **Content Analysis** - Analyzes your experiment's research topic, protocols, and methods
2. **Smart Source Discovery** - Uses Gemini AI to identify missing research areas and find relevant literature
3. **Bibliography Enhancement** - Expands your references from ~8 to 20+ high-quality sources
4. **Quality Validation** - Scores your input and predicts paper generation success
5. **Universal Compatibility** - Works for ANY research domain automatically

#### Key Features:
- ✅ **No Hardcoding** - Adapts to any research topic automatically
- ✅ **AI-Powered Discovery** - Finds real, recent academic papers using Gemini
- ✅ **Content-Aware** - Analyzes your specific experiment to identify gaps
- ✅ **Quality Prediction** - Tells you expected paper quality and generation time

#### Output Files:
- `comprehensive_results.json` - Complete enhancement data
- `comprehensive_report.md` - Quality assessment report
- `references.bib` - Enhanced bibliography (20+ references)
- `references_enhanced.bib` - Backup enhanced bibliography

### Example: SAI Research Enhancement

For the "Stratospheric Aerosol Injection" experiment:

**Before Enhancement:**
- 8 basic references
- Limited coverage of research areas
- Basic quality score

**After Enhancement:**
- 32 comprehensive references
- 12 research areas covered:
  - SAI climate impacts and uncertainties
  - Information theory in climate science
  - Volterra kernel methods for nonlinear systems
  - Robust control techniques (H-infinity, MPC)
  - Early warning signals for climate tipping points
  - Fisher information maximization
  - Cross-model validation techniques
  - Uncertainty quantification methods
  - Spectral regression techniques
  - PRBS in climate model excitation
  - Climate model emulation
  - Multi-objective climate control optimization

### For Future Experiments

#### Step 1: Create Experiment Directory
```bash
mkdir -p EXPERIMENTS/your-new-experiment/input
```

#### Step 2: Add Your Input Files
- `research_topic_formatted.txt` - Your research topic (detailed description)
- `references.bib` - Initial bibliography (even just 1-2 papers is fine)
- `experiment_config.json` - Basic experiment configuration

#### Step 3: Run Enhancement
```bash
python comprehensive_enhancer.py EXPERIMENTS/your-new-experiment
```

**The system will automatically:**
- Analyze your research topic
- Identify what literature is missing
- Find relevant, recent academic papers
- Enhance your bibliography
- Score your input quality
- Prepare everything for CycleResearcher

#### Step 4: Generate Paper
```bash
cd EXPERIMENTS/your-new-experiment
python experiment_runner.py
```

### What the Enhancement System Does

#### Automatic Research Area Identification
The system analyzes your experiment and identifies 8-12 specific research areas that need additional literature:

1. **Content Analysis** - Reads your research topic and protocols
2. **Gap Detection** - Identifies what's missing from current references
3. **Dynamic Discovery** - Uses AI to find relevant research areas
4. **Source Finding** - Locates real, recent academic papers for each area

#### Quality Scoring
The system provides a quality score (0-10) based on:
- **Literature Foundation** (25%) - Reference count and quality
- **Experimental Protocols** (25%) - Protocol completeness
- **Technical Methodology** (20%) - Methodological depth
- **Hypothesis Clarity** (15%) - Research question clarity
- **Novelty Factor** (15%) - Innovation indicators

#### Expected Outcomes
- **6.0+**: Excellent (Top-tier venues)
- **5.0+**: High Quality (Conference-level)
- **4.0+**: Publishable (Journal-level)
- **3.0+**: Basic (Needs improvement)

### Technical Requirements

#### Dependencies
```bash
pip install google-generativeai python-dotenv
```

#### Environment Variables
Create a `.env` file with:
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

#### File Structure
```
Researcher/
├── comprehensive_enhancer.py    # Main enhancement system
├── EXPERIMENTS/                # Your experiments go here
├── ai_researcher/              # CycleResearcher core system
├── .env                        # API keys
└── README.md                   # This file
```

### Troubleshooting

#### Common Issues

**"Missing GEMINI_API_KEY"**
- Check your `.env` file exists
- Verify the API key is correct
- Restart your terminal after adding the key

**"Enhancement failed"**
- Check internet connection
- Verify Gemini API key is valid
- Check experiment directory structure

**"No references found"**
- The system will use fallback research areas
- Check the generated report for details
- Verify your research topic is clear and detailed

#### Getting Help

1. Check the `comprehensive_report.md` in your experiment's input directory
2. Review `comprehensive_results.json` for detailed enhancement data
3. Verify your experiment directory structure matches the expected format

### Success Stories

#### SAI Research Example
- **Input**: 8 basic references on geoengineering
- **Enhanced**: 32 comprehensive references covering 12 research areas
- **Result**: Ready for high-quality paper generation with CycleResearcher

#### Universal Application
The system works for ANY research domain:
- Climate science
- Machine learning
- Biomedical research
- Engineering systems
- Social sciences
- And more!

### Workflow Summary

```
Your Experiment Input → Comprehensive Enhancement → Enhanced Bibliography → CycleResearcher → High-Quality Paper
       ↓                           ↓                        ↓                    ↓
    Basic refs               AI-powered discovery     20+ references      Publication-ready paper
```

**Remember**: The enhancement system is designed to be universal and automatic. Just provide your research topic and basic input, and it will handle the rest! 🚀

## 📄 License

This code and the models' weights are provided under the *CycleResearcher-License*. See the [LICENSE.md](LICENSE.md) file for details.

## 📚 Citation

If CycleResearcher is helpful to your work, please cite our paper:

```bibtex
@inproceedings{
weng2025cycleresearcher,
title={CycleResearcher: Improving Automated Research via Automated Review},
author={Yixuan Weng and Minjun Zhu and Guangsheng Bao and Hongbo Zhang and Jindong Wang and Yue Zhang and Linyi Yang},
booktitle={The Thirteenth International Conference on Learning Representations},
year={2025},
url={https://openreview.net/forum?id=bjcsVLoHYs}
}
```


if DeepReviewer is helpful to your work, please cite our paper:

```bibtex
@misc{zhu2025deepreviewimprovingllmbasedpaper,
      title={DeepReview: Improving LLM-based Paper Review with Human-like Deep Thinking Process}, 
      author={Minjun Zhu and Yixuan Weng and Linyi Yang and Yue Zhang},
      year={2025},
      eprint={2503.08569},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2503.08569}, 
}
```

## 📮 Contact

- [Submit an Issue](https://github.com/zhu-minjun/Researcher/issues)
- Email: zhuminjun@westlake.edu.cn


## 🚨 **TWO RESEARCH PIPELINES AVAILABLE**

### **🟢 Pipeline 1: Production GPT-5 System (✅ PROVEN & READY)**
**📊 RESULTS: Successfully generated 128-page papers + 6 additional papers**

**📂 Complete System**: See [`PIPELINE_1_PRODUCTION/`](PIPELINE_1_PRODUCTION/) directory  
**📍 Quick Start**: [`PIPELINE_1_PRODUCTION/README.md`](PIPELINE_1_PRODUCTION/README.md)  
**📋 Templates**: [`PIPELINE_1_PRODUCTION/EXPERIMENT_TEMPLATES.md`](PIPELINE_1_PRODUCTION/EXPERIMENT_TEMPLATES.md)

This is the **working system** that generated your successful spectroscopy papers. Designed for **hundreds of different topics** automatically.

#### **⚡ Quick Start - Any Research Topic:**

```bash
# 1. Create experiment directory
mkdir -p EXPERIMENTS/experiment-your-topic/input

# 2. Add 3 input files (see PIPELINE_1_PRODUCTION_GPT5.md for templates)
# - research_topic_formatted.txt (your detailed research topic)
# - references.bib (initial bibliography, even 1-2 papers)
# - experiment_config.json (basic configuration)

# 3. AI Enhancement (universal - works for ANY domain)
python comprehensive_enhancer.py EXPERIMENTS/experiment-your-topic

# 4. Generate paper with GPT-5
cd EXPERIMENTS/experiment-your-topic
# Copy scripts from working example:
cp ../experiment-native-1-spectro/start_openai_long_tmux.sh .
cp ../experiment-native-1-spectro/openai_long_experiment.py .
# Start 4-hour high-quality generation:
./start_openai_long_tmux.sh
```

**🌟 Universal Domain Support:**
- ✅ **Climate Science** (spectroscopy - demonstrated)
- ✅ **Machine Learning** (transformers, RL, etc.)
- ✅ **Biology** (gene editing, protein folding, etc.)
- ✅ **Engineering** (materials, robotics, etc.)
- ✅ **Physics, Chemistry, Medicine, Social Sciences** (all supported)

**📈 Quality Metrics:**
- **Length**: 128+ page academic papers
- **Quality**: 6.0+ scores (top-tier venue ready)
- **Time**: 4 hours for high-quality generation
- **Bibliography**: Auto-enhanced from few → 20+ references

### **🔶 Pipeline 2: Enhanced Validation System (🚧 IN DEVELOPMENT)**
**Adds Automatic Sakana Validation to Pipeline 1**

**📂 Development System**: See [`PIPELINE_2_DEVELOPMENT/`](PIPELINE_2_DEVELOPMENT/) directory  
**📍 Development Guide**: [`PIPELINE_2_DEVELOPMENT/README.md`](PIPELINE_2_DEVELOPMENT/README.md)  
**📋 Task Tracking**: [`PIPELINE_2_DEVELOPMENT/tasks/`](PIPELINE_2_DEVELOPMENT/tasks/)

Will enhance Pipeline 1 with:
- Automatic domain-specific validation before paper generation
- Chemical composition validation for SAI experiments  
- Pre-screening to prevent failed experiments
- Multi-domain empirical validation

**Status**: Phase 1.6 of 5 phases complete (~20% done, 2-3 weeks until ready)

---

## 🖥️ Experiment UI (tmux), outputs, and controls

### **For Spectroscopy Experiment (Example):**
The spectroscopy experiment demonstrates the system. Located at `EXPERIMENTS/experiment-native-1-spectro/`, it uses tmux with four panes:

- Pane 0: the long process running `openai_long_experiment.py` (no input expected)
- Pane 1: live logs (`logs/openai_long_*.log`)
- Pane 2: growing paper (`output/paper_gpt5_integrated.tex`)
- Pane 3: review checkpoints (`output/paper_gpt5_integrated_review.md`)

Notes:
- The “questions” you see in `paper_gpt5_integrated_review.md` are reviewer prompts written by the model for your awareness. The system does not read user replies; no keyboard input is required.
- The LaTeX “formulas” and math are generated text (no numeric simulation). There is no GLENS/GeoMIP data download or numerical solver in this experiment; it writes LaTeX sections based on your `input/references.bib` and optional `input/comprehensive_results.json`.

Duration and progress:
- Default runtime is 4 hours (configurable via `OPENAI_EXPERIMENT_HOURS`). The script appends one section per loop and periodically appends review checkpoints. Progress is also written to `output/paper_gpt5_integrated_meta.json`.

Stop/Restart:
- Detach tmux: `Ctrl-b d`
- Stop: `tmux kill-session -t gpt5_long_run`
- Restart: re-run `EXPERIMENTS/experiment-native-1-spectro/start_openai_long_tmux.sh` (it kills any existing session and starts fresh)

Outputs:
- Paper (LaTeX): `EXPERIMENTS/experiment-native-1-spectro/output/paper_gpt5_integrated.tex`
- Reviews: `EXPERIMENTS/experiment-native-1-spectro/output/paper_gpt5_integrated_review.md`
- Logs: `EXPERIMENTS/experiment-native-1-spectro/logs/openai_long_*.log`
- Meta/checkpoints: `EXPERIMENTS/experiment-native-1-spectro/output/paper_gpt5_integrated_meta.json` and `EXPERIMENTS/experiment-native-1-spectro/checkpoints/`

One-shot alternatives (no tmux):
- `openai_runner.py` generates one or more full papers quickly.
- `integrated_runner.py` generates a single paper and a single review in one pass.

Using real datasets:
- This repository, as configured, does not fetch GLENS/GeoMIP or run physical models. To incorporate data-driven analysis, add your own preprocessing and pass summaries/tables into the prompts, or integrate an external computation pipeline and include its outputs as figures/tables referenced by LaTeX.


### LaTeX → PDF quick guide (experiment outputs)

- Entry files live in `EXPERIMENTS/experiment-native-1-spectro/output/`.
- The long-run integrated paper `paper_gpt5_integrated.tex` is section-only LaTeX. Wrap it in a minimal preamble, then compile.
- Prefer `xelatex` for Unicode. Use a 3-pass build with bibliography.

Minimal wrapper example:

```bash
cd EXPERIMENTS/experiment-native-1-spectro/output
cat > paper_wrapper.tex <<'EOF'
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{geometry}\geometry{margin=1in}
\usepackage{cite}
\title{Generated Paper}
\author{AI-Generated}
\date{\today}
\begin{document}
\maketitle
\input{paper_gpt5_integrated.tex}
\clearpage
\bibliographystyle{plain}
\bibliography{../input/references,../input/references_enhanced}
\end{document}
EOF
```

Unicode/maths fixes:

```bash
# Common replacements if pdflatex fails or math breaks
sed -i '' 's/±/\\pm/g; s/μ/\\mu/g; s/τ/\\tau/g; s/α/\\alpha/g; s/σ/\\sigma/g; s/ω/\\omega/g; s/π/\\pi/g; s/≤/\\le/g; s/≥/\\ge/g; s/≈/\\approx/g; s/∈/\\in/g; s/∝/\\propto/g; s/⋆/\\star/g; s/Δ/\\Delta/g; s/Γ/\\Gamma/g; s/∂/\\partial/g' paper_gpt5_integrated.tex
```

Compile (3-pass with bibliography):

```bash
/Library/TeX/texbin/xelatex -interaction=nonstopmode paper_wrapper.tex | cat
/Library/TeX/texbin/bibtex paper_wrapper | cat
/Library/TeX/texbin/xelatex -interaction=nonstopmode paper_wrapper.tex | cat
/Library/TeX/texbin/xelatex -interaction=nonstopmode paper_wrapper.tex | cat
```

Directly compiling a one-shot paper (already a full document), e.g. `paper_openai_*.tex`:

```bash
# If it lacks preamble, create wrapper as above; otherwise compile directly
/Library/TeX/texbin/xelatex -interaction=nonstopmode paper_openai_20250812_160417_1.tex | cat
/Library/TeX/texbin/bibtex paper_openai_20250812_160417_1 | cat
/Library/TeX/texbin/xelatex -interaction=nonstopmode paper_openai_20250812_160417_1.tex | cat
/Library/TeX/texbin/xelatex -interaction=nonstopmode paper_openai_20250812_160417_1.tex | cat
```

Tips:
- Fix ALL Unicode issues before compiling; there are usually many.
- Keep equation labels unique to avoid collisions.
- If citations are placeholder-like, add stubs to `../input/references_enhanced.bib`.

## LaTeX → PDF Conversion Guide

### For Experiment Outputs

The experiment outputs in `EXPERIMENTS/experiment-native-1-spectro/output/` contain LaTeX files that need conversion to PDF.

#### Key Files
- `paper_gpt5_integrated.tex` - Main integrated paper (section-only, needs wrapper)
- `paper_openai_*.tex` - OpenAI-generated papers (may need wrapper)

#### Step 1: Create Complete LaTeX Document

If the .tex file lacks preamble (no `\documentclass`), create a wrapper:

```bash
cd EXPERIMENTS/experiment-native-1-spectro/output

# Create complete document with wrapper
cat > paper_wrapper.tex <<'EOF'
\documentclass[11pt]{article}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{geometry}
\geometry{margin=1in}
\usepackage{cite}

\title{Your Paper Title}
\author{AI-Generated}
\date{\today}

\begin{document}
\maketitle

\input{paper_gpt5_integrated.tex}

\clearpage
\bibliographystyle{plain}
\bibliography{../input/references,../input/references_enhanced}

\end{document}
EOF
```

#### Step 2: Fix Unicode and Math Issues

Common replacements for Unicode characters:

```bash
# Fix Greek letters and symbols
sed -i '' 's/ω/\\omega/g; s/π/\\pi/g; s/δ/\\delta/g; s/θ/\\theta/g; s/α/\\alpha/g; s/σ/\\sigma/g; s/τ/\\tau/g; s/μ/\\mu/g' paper_wrapper.tex

# Fix superscripts and special symbols
sed -i '' 's/²/^2/g; s/³/^3/g; s/±/\\pm/g; s/≤/\\le/g; s/≥/\\ge/g; s/≈/\\approx/g; s/∈/\\in/g; s/∝/\\propto/g; s/⋆/\\star/g; s/Δ/\\Delta/g; s/Γ/\\Gamma/g; s/∂/\\partial/g' paper_wrapper.tex

# Fix citation issues
sed -i '' 's/{Comprehensive Discovery System}/{comprehensive_discovery_system}/g; s/{Smart Discovery System}/{smart_discovery_system}/g' paper_wrapper.tex
```

#### Step 3: Compile with 3-Pass Build

Use xelatex for better Unicode handling:

```bash
# First pass
/Library/TeX/texbin/xelatex -interaction=nonstopmode -file-line-error paper_wrapper.tex

# Process bibliography
/Library/TeX/texbin/bibtex paper_wrapper

# Second pass
/Library/TeX/texbin/xelatex -interaction=nonstopmode -file-line-error paper_wrapper.tex

# Third pass (stabilize references)
/Library/TeX/texbin/xelatex -interaction=nonstopmode -file-line-error paper_wrapper.tex
```

#### Step 4: Add Missing References

If citations are undefined, add placeholder entries to `../input/references_enhanced.bib`:

```bibtex
@misc{comprehensive_discovery_system,
  title = {Comprehensive Discovery System},
  note = {Placeholder reference},
  year = {2025}
}

@article{keith2010researchon,
  title = {Research on climate engineering: A review},
  author = {Keith, David W},
  journal = {Climatic Change},
  volume = {102},
  number = {3-4},
  pages = {427--431},
  year = {2010}
}
```

#### Troubleshooting

- **Unicode errors**: Use xelatex instead of pdflatex
- **Missing references**: Add placeholder entries to bibliography
- **Math mode errors**: Ensure proper `$...$` delimiters
- **Bibliography issues**: Run bibtex between xelatex passes

#### CRITICAL: Common LaTeX Syntax Errors to Fix BEFORE Compilation

**AVOID WASTING TOKENS** by fixing these issues first:

1. **Citations in Math Mode** - This causes `\spacefactor` errors:
   ```bash
   # WRONG: \cite{...} inside math mode
   $y = x + \cite{reference}$
   
   # CORRECT: Citations outside math mode
   $y = x + \text{reference}$
   ```

2. **Missing Math Delimiters** - Wrap math expressions with `$...$`:
   ```bash
   # WRONG: g_{0}, yr^{-1} without math mode
   g_{0} and yr^{-1}
   
   # CORRECT: With math mode
   $g_{0}$ and $yr^{-1}$
   ```

3. **Bad Math Environment Delimiters** - Fix broken `\[...\]` or `\begin{align}...\end{align}`:
   ```bash
   # Check for unmatched math environments
   grep -n "\\\\\[\\|\\\\\\]" paper.tex
   grep -n "\\\\begin{align\\|\\\\end{align}" paper.tex
   ```

4. **Old Citation Keys** - Replace placeholder keys before compilation:
   ```bash
   # Replace old keys with valid ones
   sed -i '' 's/{Comprehensive Discovery System}/{comprehensive_discovery_system}/g' paper.tex
   sed -i '' 's/{Smart Discovery System}/{smart_discovery_system}/g' paper.tex
   ```

5. **Clean Auxiliary Files** - Remove stale compilation data:
   ```bash
   rm -f *.aux *.bbl *.blg *.log
   ```

**IMPORTANT**: Fix ALL syntax errors before running the 3-pass build. LaTeX will fail with the same errors repeatedly if syntax issues aren't resolved first.

#### Direct Compilation (if already complete document)

```bash
# For papers with full preamble
/Library/TeX/texbin/xelatex -interaction=nonstopmode paper_openai_*.tex
/Library/TeX/texbin/bibtex paper_openai_*
/Library/TeX/texbin/xelatex -interaction=nonstopmode paper_openai_*.tex
/Library/TeX/texbin/xelatex -interaction=nonstopmode paper_openai_*.tex
```

### Results

Successfully converted:
- `paper_gpt5_integrated.tex` → `paper_gpt5_integrated_fixed.pdf` (127 pages with conclusion)
- `paper_openai_20250812_160417_1.tex` → `paper_openai_20250812_160417_1_complete.pdf`

Both PDFs include proper bibliography and conclusion sections.