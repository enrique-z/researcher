# 🎯 **CODEBASE VISUAL SEPARATION PLAN**

## **CURRENT PROBLEM**: Pipeline 1 and Pipeline 2 code is mixed, creating confusion

## **SOLUTION**: Clear directory structure and file organization

---

## 📂 **NEW DIRECTORY STRUCTURE**

### **🟢 PIPELINE 1: PRODUCTION GPT-5 SYSTEM** 
```
/Users/apple/code/Researcher/
├── 📁 PIPELINE_1_PRODUCTION/           # ✅ WORKING SYSTEM
│   ├── 📄 PIPELINE_1_PRODUCTION_GPT5.md
│   ├── 📄 EXPERIMENT_TEMPLATES.md
│   ├── 📄 WORKFLOW_RECOVERY_ANALYSIS.md
│   ├── 📄 comprehensive_enhancer.py    # Universal enhancement
│   ├── 📁 EXPERIMENTS/                 # All experiment directories
│   │   ├── 📁 experiment-native-1-spectro/  # Working example
│   │   ├── 📁 experiment-[topic-2]/
│   │   └── 📁 experiment-[topic-N]/
│   └── 📁 INPUT/                       # Input preparation area
│       └── 📁 experiment-1/            # Original spectroscopy input
│
├── 📁 ai_researcher/                   # ORIGINAL RESEARCHER FRAMEWORK
│   ├── cycle_researcher.py            # ✅ Production paper generation
│   ├── cycle_reviewer.py              # ✅ Production review system
│   ├── deep_reviewer.py               # ✅ Production multi-review
│   ├── detector.py                     # ✅ AI detection
│   ├── utils.py                        # ✅ Production utilities
│   └── data/                           # ✅ Original data handling
│       └── loaders/                    # ✅ Original loaders
```

### **🔶 PIPELINE 2: ENHANCED VALIDATION (DEVELOPMENT)**
```
├── 📁 PIPELINE_2_DEVELOPMENT/          # 🚧 IN DEVELOPMENT
│   ├── 📄 PIPELINE_2_ENHANCED_VALIDATION.md
│   ├── 📄 PIPELINE_2_TASKS.md
│   ├── 📁 ai_researcher_enhanced/      # NEW VALIDATION SYSTEM
│   │   ├── validation/                 # Domain-agnostic validators
│   │   │   ├── experiment_validator.py
│   │   │   ├── sakana_validator.py
│   │   │   ├── empirical_validation.py
│   │   │   └── domains/
│   │   │       ├── chemical_composition.py
│   │   │       └── signal_detection.py
│   │   ├── integration/                # Pipeline 1 integration
│   │   │   ├── framework_bridge.py
│   │   │   └── data_pipeline.py
│   │   └── data/                       # Enhanced data handling
│   │       └── loaders/
│   │           └── glens_loader.py     # Multi-domain GLENS
│   └── 📁 tasks/                       # Development task tracking
│       └── tasks-ai-research-integration.md
```

---

## 🔧 **CODE REORGANIZATION ACTIONS**

### **STEP 1: Create Pipeline Directories**
```bash
mkdir -p PIPELINE_1_PRODUCTION/EXPERIMENTS
mkdir -p PIPELINE_1_PRODUCTION/INPUT  
mkdir -p PIPELINE_2_DEVELOPMENT/ai_researcher_enhanced
```

### **STEP 2: Move Pipeline 1 Files (Production System)**
```bash
# Move working experiment and input
mv EXPERIMENTS/ PIPELINE_1_PRODUCTION/
mv INPUT/ PIPELINE_1_PRODUCTION/
mv comprehensive_enhancer.py PIPELINE_1_PRODUCTION/

# Move Pipeline 1 documentation
mv PIPELINE_1_PRODUCTION_GPT5.md PIPELINE_1_PRODUCTION/
mv EXPERIMENT_TEMPLATES.md PIPELINE_1_PRODUCTION/
mv WORKFLOW_RECOVERY_ANALYSIS.md PIPELINE_1_PRODUCTION/
```

### **STEP 3: Move Pipeline 2 Files (Development System)** 
```bash
# Move validation development code
mkdir -p PIPELINE_2_DEVELOPMENT/ai_researcher_enhanced/validation/domains
mkdir -p PIPELINE_2_DEVELOPMENT/ai_researcher_enhanced/integration  
mkdir -p PIPELINE_2_DEVELOPMENT/ai_researcher_enhanced/data/loaders

# Move validation files
mv ai_researcher/validation/experiment_validator.py PIPELINE_2_DEVELOPMENT/ai_researcher_enhanced/validation/
mv ai_researcher/validation/sakana_validator.py PIPELINE_2_DEVELOPMENT/ai_researcher_enhanced/validation/
mv ai_researcher/validation/empirical_validation.py PIPELINE_2_DEVELOPMENT/ai_researcher_enhanced/validation/
mv ai_researcher/validation/domains/ PIPELINE_2_DEVELOPMENT/ai_researcher_enhanced/validation/

# Move integration files  
mv ai_researcher/integration/ PIPELINE_2_DEVELOPMENT/ai_researcher_enhanced/

# Move enhanced data loaders
cp ai_researcher/data/loaders/glens_loader.py PIPELINE_2_DEVELOPMENT/ai_researcher_enhanced/data/loaders/

# Move Pipeline 2 documentation
mv PIPELINE_2_ENHANCED_VALIDATION.md PIPELINE_2_DEVELOPMENT/
mv tasks/ PIPELINE_2_DEVELOPMENT/
```

### **STEP 4: Create Clear Entry Points**

**Pipeline 1 Entry Point**: `PIPELINE_1_PRODUCTION/README.md`
**Pipeline 2 Entry Point**: `PIPELINE_2_DEVELOPMENT/README.md`