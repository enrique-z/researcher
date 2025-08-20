# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
# AI Dev Tasks
	Use these files when I request structured feature development using PRDs:
  /PIPELINE_2_DEVELOPMENT/tasks/tasks-ai-research-integration.md
  /PIPELINE_2_DEVELOPMENT/tasks/AI_Research_Integration_PRD.md


## Plan & Review

### Before starting work

Always in plan mode to make a plan
After get the plan, make sure you Write the plan
to .claude/tasks/PLAN_NAME_DATE_TIME.md.

- The plan should be a detailed implementation
plan and the reasoning behind them, as well as
tasks broken down.
- If the task require external knowledge or
certain package, also research to get latest
knowledge (Use Task tool for research)
- Don't over plan it, always think MVP.
- Once you write the plan, firstly ask me to
review it. Do not continue until I approve the
plan.

# Important Notes

No test framework is currently configured

## 🚨 CRITICAL RULE: ZERO TOLERANCE FOR MOCK/FAKE DATA

**ABSOLUTELY NO MOCK DATA, HARDCODED RESPONSES, OR FAKE RESULTS ALLOWED**

- ALL verification systems MUST connect to real implementations
- ALL experimental validation MUST use real data processing
- ALL test results MUST be genuinely executed and traced
- ALL claims of "system tested" MUST show actual execution logs
- ALL integration points MUST connect to real systems, not placeholders

**FORBIDDEN PRACTICES:**
- ❌ Using `np.array([1, 2, 3])` as placeholder data
- ❌ Hardcoded responses like `{"status": "VERIFIED"}` without real computation
- ❌ Fake experimental claims without actual text parsing
- ❌ Mock validation results without real domain validation
- ❌ Claims of "system working perfectly" without execution proof

**REQUIRED EVIDENCE:**
- ✅ Show actual file paths that were processed
- ✅ Provide execution logs with timestamps
- ✅ Demonstrate real data flow through verification systems
- ✅ Trace actual function calls to real implementations
- ✅ Generate authentic results from real computational processes

**VIOLATION CONSEQUENCES:**
Any task using mock/fake data must be immediately identified, documented, and re-implemented with real systems. No exceptions.

## Rules

- Before you do any work, MUST view files in .claude/tasks/context_session_x.md file to get the full context (x being the id of the session we are operate, if file doesnt exist, then create one)
context_session_x.md should contain most of context of what we did, overall plan, and sub agents will continusly add context to the file
After you finish the work, MUST update the .claude/tasks/context_session_x.md file to make sure others can get full context of what you did

### Sub agents

### While implementing

- You should update the plan as you work.
- After you complete tasks in the plan, you should
update and append detailed descriptions of the
changes you made, so following tasks can be easily
hand over to other engineers.

## Project Overview

This is the **AI-powered Researcher** repository, a comprehensive ecosystem for AI-powered academic research and review. It consists of three main components integrated into a research-review feedback loop:

1. **CycleResearcher**: Generates high-quality research papers using gpt-5 exclusively
2. **CycleReviewer**: Provides detailed academic reviews and scoring (8B, 70B, 123B parameter models)  
3. **DeepReviewer**: Multi-perspective review simulation with self-verification (7B, 14B parameter models)
4. **OpenScholar**: RAG-based academic research Q&A system using Semantic Scholar API
5. **AI Detection**: FastDetectGPT-based detection for identifying AI-generated content

## Development Environment Setup

### Virtual Environment
The project uses a custom activation system:
```bash
source activate    # Activate environment (custom script, not conda/venv activate)
deactivate         # Standard deactivation
```
The python environment is in '/Users/apple/code/Researcher/.venv'     you must always consider, so dont run python commands if not in this environment, and install whatever necesary here.     

### Installation Commands
```bash
# Full installation from scratch
pip install -e .  # Install package in development mode
pip install flask matplotlib scikit-learn FlagEmbedding  # Additional dependencies

# Test installation
python test_installation.py
```

### Model Management
- **ONLY MODEL**: **gpt-5 via OpenAI API** - CycleResearcher ONLY works with gpt-5
- **Cost**: ~$5 USD for 128+ page comprehensive papers
- **Performance**: 3-4 hours for complete paper generation
- **Note**: CycleResearcher has been updated to use gpt-5 exclusively 

## Architecture Overview

### Core Package Structure (`ai_researcher/`)
- `cycle_researcher.py`: Paper generation engine with vLLM-based inference
- `cycle_reviewer.py`: Academic review and scoring system  
- `deep_reviewer.py`: Multi-reviewer simulation framework
- `detector.py`: AI-generated content detection using FastDetectGPT
- `utils.py`: Text parsing utilities for LaTeX/BibTeX processing
- `detect/`: FastDetectGPT implementation with pre-trained reference data

### Model Architecture Integration
All components use transformer-based architectures with different specializations:
- **Generation Models**: Fine-tuned on Research-14K dataset for paper generation
- **Review Models**: Trained on Review-5K dataset with peer review data
- **Detection Models**: Specialized for distinguishing human vs. AI-generated academic text

### Data Flow
1. **Input**: BibTeX references and research topics
2. **Processing**: Models generate structured academic papers with sections (motivation, methods, experiments)
3. **Review Loop**: CycleReviewer evaluates generated papers, providing feedback
4. **Detection**: AI detection validates content authenticity
5. **Output**: Structured papers with LaTeX formatting and experimental configurations

## Common Commands

### Basic Usage
```bash
# Test all functionality
python test_installation.py

# RECOMMENDED: Generate research paper with gpt-5
cd EXPERIMENTS/qbo-sai-cambridge-poc/
OPENAI_MODEL=gpt-5 OPENAI_REASONING_EFFORT=high \
OPENAI_MAX_TOKENS=12000 OPENAI_EXPERIMENT_HOURS=4 \
python openai_qbo_sai_experiment.py

# Monitor progress
tail -f logs/qbo_sai_generation_*.log
tail -f output/qbo_sai_cambridge_paper.tex

# Alternative: Use tmux for background execution
./start_qbo_sai_tmux.sh

# Review papers (if needed)
python -c "
from ai_researcher import CycleReviewer
reviewer = CycleReviewer()
results = reviewer.evaluate(paper_text)
"

# AI detection (if needed)
python -c "
from ai_researcher import AIDetector
detector = AIDetector(device='cpu')
result = detector.analyze_paper(paper_text)
"
```

### OpenScholar RAG System
```bash
# Start model services (requires GPU)
cd OpenScholar
./start_models.sh

# Start API service (requires Semantic Scholar API key)
python openscholar_api.py --s2_api_key YOUR_KEY --reranker_path OpenSciLM/OpenScholar_Reranker

# Test API
curl -X POST http://localhost:38015/batch_ask -H "Content-Type: application/json" \
  -d '{"questions": ["How do retrieval-augmented LMs perform in knowledge-intensive tasks?"]}'
```

### Model Configuration
- **GPU Memory**: Models use configurable `gpu_memory_utilization` (default: 0.95)
- **Tensor Parallelism**: `tensor_parallel_size` for multi-GPU setups
- **Context Length**: `max_model_len` varies by component (up to 70000 tokens)
- **Quantization**: OpenScholar uses FP8 quantization for efficiency

## Key Integration Points



### Data Processing Pipeline
1. **BibTeX Processing**: `bibtexparser` handles reference parsing
2. **Text Generation**: Structured prompts with section markers (`## Motivation`, `## Main Idea`, etc.)
3. **LaTeX Extraction**: Regex-based parsing for academic formatting
4. **JSON Configuration**: Experimental setups encoded as JSON within generated text

### Review Modes (DeepReviewer)
- **Fast Mode**: Single reviewer, no background search
- **Standard Mode**: Multiple reviewers with self-verification  
- **Best Mode**: Full pipeline with knowledge search, multi-reviewer simulation, and verification




### API Keys and Configuration

- Various model-specific configurations in `.env`

## Tutorials and Examples
- `Tutorial/tutorial_1.ipynb`: CycleResearcher paper generation
- `Tutorial/tutorial_2.ipynb`: CycleReviewer review systems  
- `Tutorial/tutorial_3.ipynb`: DeepReviewer multi-perspective analysis
- `Tutorial/cycleresearcher_references.bib`: Sample BibTeX references for testing