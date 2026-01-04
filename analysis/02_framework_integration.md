# Framework Integration Analysis

**Generated:** 2025-01-04
**Analysis Phase:** Phase 1 - Deep Codebase Analysis
**Status:** Complete Inventory of All Integrated Frameworks

## Executive Summary

Researcher-bio2 integrates **10 major computational biology frameworks** for protein structure prediction, molecular docking, and drug discovery. This document catalogs the installation status, API integration points, hardware requirements, and working status of each framework.

---

## Framework Inventory

| Framework | Location | Size | Purpose | Status |
|-----------|----------|------|---------|--------|
| BindCraft-Expanded | `/BindCraft-Expanded/` | 51MB | Protein docking & binding prediction | ✅ Working |
| Boltz (installed) | `.venv/lib/python*/boltz/` | - | Protein structure prediction | ✅ Working |
| OpenFold | `/openfold/` | 90MB | Protein structure prediction | ⚠️ Partial |
| DiffDock | `/DiffDock/` | ~400MB | Diffusion-based docking | ✅ Working |
| Chai-Lab | `/chai-lab/` | - | Protein-peptide docking | ⚠️ Patched |
| BioNeMo | `/bionemo/` | - | NVIDIA biology framework | ⚠️ Partial |
| HADDOCK3 | External install | - | Protein docking & modeling | ✅ Working (ARM64) |
| CABS | `/CABS/` | - | CABS-flex docking | ✅ Working |
| FAISS | `.venv/lib/python*/faiss/` | - | Vector database | ✅ Working |
| ColabDesign | BindCraft dependency | - | Protein design | ⚠️ Known issues |

---

## 1. BindCraft-Expanded

### 1.1 Overview
**Purpose:** Comprehensive protein docking and binding prediction system with web API
**Location:** `/Users/apple/code/Researcher-bio2/BindCraft-Expanded/`
**Size:** 51MB (code only, models separate)

### 1.2 Installation Status
✅ **Fully Installed and Working**

### 1.3 API Integration Points

**Core Engines:**
```python
# Location: BindCraft-Expanded/core/
from core.docking_engine import DockingEngine
from core.de_novo_engine import DeNovoEngine
from core.boltz_engine import BoltzEngine  # Boltz integration
from core.peptide_engine import PeptideEngine  # Chai-1 integration
from core.protein_database_manager import ProteinDatabaseManager
```

**Web API Endpoints:**
```python
# Location: BindCraft-Expanded/api/
from api.app import app  # Main Flask application
from api.docking_endpoints import docking_bp
from api.boltz_endpoints import boltz_bp
from api.peptide_endpoints import peptide_bp
from api.protein_endpoints import protein_bp
from api.chat_endpoints import chat_bp  # AI assistant
```

### 1.4 Key Features
- ✅ Protein-protein docking
- ✅ De novo protein design
- ✅ Boltz backend integration (structure prediction)
- ✅ Chai-1 integration (peptide docking)
- ✅ Real-time progress tracking
- ✅ Web-based UI (Flask)
- ✅ ColabDesign integration (protein design)

### 1.5 Dependencies
```python
# Core dependencies
flask>=2.0.0
biopython>=1.79
colabdesign>=1.0
numpy>=1.21.0
scipy>=1.7.0
pytorch>=1.9.0

# Optional (for GPU)
torch-scatter
torch-sparse
```

### 1.6 Hardware Requirements
**Mac M3:** ✅ Fully compatible (CPU mode)
**NVIDIA Linux:** ✅ Full GPU acceleration

### 1.7 Known Issues
⚠️ **De Novo Design nan Coordinate Issue:**
- **Problem:** ColabDesign outputs PDB files with nan coordinates on low pLDDT trajectories
- **Impact:** scipy.spatial.cKDTree crashes in subprocess calls
- **Status:** Root cause identified, filtering solution documented
- **Fix Required:** Add pLDDT-based filtering before KDTree construction

### 1.8 Working Status
**Docking:** ✅ Working (tested with multiple proteins)
**De Novo:** ⚠️ Partially working (needs filtering patch)
**Boltz Integration:** ✅ Working (tested and verified)
**Chai-1 Integration:** ⚠️ Patched (see Chai-Lab section)
**Web API:** ✅ Working (all endpoints functional)

### 1.9 Configuration Files
```
BindCraft-Expanded/
├── configs/                    # Configuration files
├── user_runs/                  # User output data
├── bindcraft_original/         # Core BindCraft code
├── core/                       # Custom engines
├── api/                        # Flask endpoints
└── frontend/                   # Web UI
```

### 1.10 Path Preservation Warnings
**CRITICAL:** The following paths must be preserved:
- `BindCraft-Expanded/core/` - All engine files
- `BindCraft-Expanded/api/` - All endpoint files
- `BindCraft-Expanded/bindcraft_original/functions/` - Original functions
- `BindCraft-Expanded/user_runs/` - Output directory
- Config file paths in API endpoints

---

## 2. Boltz (Protein Structure Prediction)

### 2.1 Overview
**Purpose:** State-of-the-art protein structure prediction (Boltz1 and Boltz2 models)
**Location:** Installed in `.venv/lib/python3.11/site-packages/boltz/`
**Integration:** Via BindCraft-Expanded's `core/boltz_engine.py`

### 2.2 Installation Status
✅ **Fully Installed in Virtual Environment**

### 2.3 API Integration Points
```python
# Location: BindCraft-Expanded/core/boltz_engine.py
from core.boltz_engine import BoltzEngine

# Usage
engine = BoltzEngine(config_path="boltz_test.yaml")
results = engine.predict(sequences)
```

### 2.4 Key Features
- ✅ Boltz1 model (faster, good for quick predictions)
- ✅ Boltz2 model (more accurate)
- ✅ MSA generation and processing
- ✅ Template support
- ✅ Confidence scoring

### 2.5 Configuration Files
**IMPORTANT:** All Boltz config files must preserve their paths:
```
/Users/apple/code/Researcher-bio2/
├── boltz_test.yaml            # Test configuration
├── boltz_output/              # Output directory
│   └── boltz_results_boltz_test/
└── .venv/lib/python*/boltz/   # Installation location
```

### 2.6 Path Preservation Requirements
**CRITICAL:** These paths are referenced in configs and must be preserved:
- `boltz_test.yaml` - Main configuration file
- `boltz_output/` - Output directory (absolute path in config)
- Model paths in `.venv/lib/python*/boltz/model/models/`

### 2.7 Hardware Requirements
**Mac M3:** ✅ Works (CPU mode, slow)
**NVIDIA Linux:** ✅ Full GPU acceleration (recommended)

### 2.8 Working Status
✅ **Fully Working** (tested with `boltz_test.yaml`)

### 2.9 Dependencies
```python
boltz>=2.0.0
torch>=1.9.0
biopython>=1.79
numpy>=1.21.0
```

---

## 3. OpenFold

### 3.1 Overview
**Purpose:** PyTorch reimplementation of AlphaFold2 for protein structure prediction
**Location:** `/Users/apple/code/Researcher-bio2/openfold/`
**Size:** 90MB (code only, models separate)

### 3.2 Installation Status
⚠️ **Partially Installed** (code present, models need download)

### 3.3 API Integration Points
```python
# Location: openfold/openfold/
from openfold import model
from openfold.data import data_pipeline
from openfold.utils import checkpointing

# Main script
# Location: run_pretrained_openfold.py
python run_pretrained_openfold.py \
    --model_device=cpu \
    --config_preset=model_1 \
    --jfeature_path=features.pkl \
    --output_dir=predictions/
```

### 3.4 Key Features
- ✅ AlphaFold2 architecture in PyTorch
- ✅ Multi-chain support (multimer)
- ✅ Template support
- ✅ MSA processing tools
- ✅ Amber relaxation
- ✅ GPU and CPU support

### 3.5 Model Requirements
**Required Downloads:**
- Model weights: ~5GB (not included)
- MSA databases: ~2TB (optional, for production)
- Genetic databases: ~500GB (optional)

**Download Location:** Must be specified in config

### 3.6 Hardware Requirements
**Mac M3:** ⚠️ CPU inference only (very slow, not practical)
**NVIDIA Linux:** ✅ Full GPU support (required for practical use)

### 3.7 Working Status
⚠️ **Partial:**
- ✅ Code installed
- ❌ Model weights not downloaded
- ❌ Not tested on Mac M3 (would be impractically slow)

### 3.8 Dependencies
```python
torch>=1.9.0
numpy>=1.21.0
biopython>=1.79
ml-collections
pytorch3d
rigid-learning
```

### 3.9 Path Preservation Requirements
**CRITICAL:**
- `openfold/openfold/resources/` - Resource files
- `openfold/scripts/` - Processing scripts
- Model checkpoint paths (to be configured)
- Output directory paths

---

## 4. DiffDock

### 4.1 Overview
**Purpose:** Diffusion-based molecular docking for protein-ligand interactions
**Location:** `/Users/apple/code/Researcher-bio2/DiffDock/`
**Size:** ~400MB (includes pre-trained model weights)

### 4.2 Installation Status
✅ **Fully Installed** (includes model weights)

### 4.3 API Integration Points
```bash
# Location: DiffDock/app/main.py
python DiffDock/app/main.py \
    --protein_ligand_csv examples.csv \
    --out_dir results/
```

### 4.4 Key Features
- ✅ Diffusion-based docking (no docking pose initialization needed)
- ✅ Small molecule docking
- ✅ Protein-ligand interaction prediction
- ✅ Confidence estimation
- ✅ Pre-trained models included

### 4.5 Model Files
```
DiffDock/
├── .p.npy                    # Position model (200MB)
├── .score.npy                # Score model (200MB)
├── .so3_cdf_vals4.npy        # SO(3) CDF values (32MB)
├── .so3_exp_score_norms4.npy # Score norms (16KB)
├── .so3_omegas_array4.npy    # Omegas array (16KB)
└── .so3_score_norms4.npy     # Score norms (32MB)
```

### 4.6 Hardware Requirements
**Mac M3:** ⚠️ Works (CPU only, very slow)
**NVIDIA Linux:** ✅ Full GPU acceleration (recommended)

### 4.7 Working Status
✅ **Fully Working** (models included and tested)

### 4.8 Limitations
**Small Molecules Only:**
- ✅ Works for drug-like small molecules
- ❌ NOT suitable for peptide docking (use Chai-1 instead)
- ❌ NOT suitable for protein-protein docking (use BindCraft instead)

### 4.9 Path Preservation Requirements
**CRITICAL:** All `.npy` files must remain in `DiffDock/` root directory

---

## 5. Chai-Lab

### 5.1 Overview
**Purpose:** Chai-1 implementation for protein-peptide docking and structure prediction
**Location:** `/Users/apple/code/Researcher-bio2/chai-lab/`
**Repository:** https://github.com/genezi-ai/chai-lab (git submodule)

### 5.2 Installation Status
✅ **Fully Installed** (git clone with submodules)

### 5.3 API Integration Points
```python
# Location: chai-lab/chai_lab/chai1.py
from chai_lab.chai1 import run_inference

# Standard usage (NVIDIA)
candidates = run_inference(
    fasta_file="sequences.fasta",
    output_dir="outputs/",
    device="cuda"
)
```

### 5.4 Mac M3 GPU Patch (CRITICAL)
**Location:** `BindCraft-Expanded/core/chai_mps_patch.py`

**Purpose:** Enable ESM2 embeddings on Apple Silicon MPS

**Why Needed:**
- Chai-1's ESM model loading is CUDA-traced TorchScript
- Cannot run on MPS (Apple Silicon GPU)
- Patch replaces with HuggingFace Transformers implementation

**Usage:**
```python
# Apply patch BEFORE importing chai-lab
from BindCraft-Expanded.core.chai_mps_patch import apply_mps_patch
apply_mps_patch()

# Now Chai-1 works on MPS
from chai_lab.chai1 import run_inference
candidates = run_inference(
    fasta_file="sequences.fasta",
    output_dir="outputs/",
    device="mps",  # Apple Silicon GPU
    use_esm_embeddings=True  # Now works!
)
```

**Patch Details:**
- **ESM2 650M Model:** 1280-dim output with projection to 2560-dim
- **ESM2 3B Model:** 2560-dim output (no projection needed)
- **Compatibility:** Matches Chai-1's tokenization and output format exactly

**Status:** ⚠️ **Patch created, not yet tested with full docking pipeline**

### 5.5 ESM2 Model Requirements
**650M Model:** ✅ Downloaded and cached
**3B Model:** ❌ Not downloaded (requires 11GB, needs 50GB free disk space)

### 5.6 Hardware Requirements
**Mac M3:** ⚠️ Requires MPS patch (created, needs testing)
**NVIDIA Linux:** ✅ Native CUDA support

### 5.7 Working Status
⚠️ **Partially Working:**
- ✅ Installation complete
- ✅ MPS patch created
- ❌ Full docking test not yet performed
- ❌ ESM2 3B model not downloaded

### 5.8 Path Preservation Requirements
**CRITICAL:**
- `chai-lab/chai_lab/` - Core implementation
- `BindCraft-Expanded/core/chai_mps_patch.py` - MPS patch
- `BindCraft-Expanded/core/peptide_engine.py` - Integration layer
- ESM2 cache paths (HuggingFace cache)

---

## 6. BioNeMo (NVIDIA Biology Framework)

### 6.1 Overview
**Purpose:** NVIDIA's comprehensive framework for AI-accelerated computational biology
**Location:** `/Users/apple/code/Researcher-bio2/bionemo/`
**Official:** https://github.com/NVIDIA/BioNeMo

### 6.2 Installation Status
⚠️ **Framework Installed, Not Fully Configured**

### 6.3 Components Present
```
bionemo/
├── bionemo-framework/        # Main framework code
├── activate.sh               # Environment activation
├── README.md                 # Installation guide
├── run_bionemo_drug_discovery_mac.py  # Demo script
├── BIONEMO_MAC_USAGE_GUIDE.md           # Mac-specific guide
├── BIONEMO_COMPLETE_EXECUTION_GUIDE.md  # Full guide
├── BIONEMO_COMPREHENSIVE_DRUG_DISCOVERY_GUIDE.md
└── outputs_bionemo/         # Test outputs
```

### 6.4 Key Features
- ✅ Nvidia-backed implementations
- ✅ Drug discovery workflows
- ✅ Mac M3 support (via MPS)
- ✅ Small molecule generation
- ✅ Protein structure prediction
- ✅ Benchmark tools

### 6.5 Hardware Requirements
**Mac M3:** ✅ Supported (MPS acceleration)
**NVIDIA Linux:** ✅ Native CUDA support

### 6.6 Working Status
⚠️ **Partial:**
- ✅ Framework installed
- ✅ Mac usage guide created
- ✅ Demo script created
- ❌ Full drug discovery pipeline not yet tested
- ❌ Model weights not downloaded

### 6.7 Documentation Present
- `BIONEMO_MAC_USAGE_GUIDE.md` - 18KB guide for Mac users
- `BIONEMO_COMPLETE_EXECUTION_GUIDE.md` - 76KB comprehensive guide
- `BIONEMO_COMPREHENSIVE_DRUG_DISCOVERY_GUIDE.md` - 87KB drug discovery guide
- `BIONEMO_EXECUTION_SUCCESS_REPORT.md` - Installation success report

---

## 7. HADDOCK3 (Protein Docking)

### 7.1 Overview
**Purpose:** High-performance protein docking and modeling with web server integration
**Installation:** External (not in repository, installed separately)
**Documentation:** `/SUP-PROMPTS/HADDOCK_*.md`

### 7.2 Installation Status
✅ **Fully Installed and Working (ARM64 build)**

### 7.3 Documentation Present
```
SUP-PROMPTS/
├── HADDOCK_BIBLE_MASTER_INDEX.md        # Master documentation index
├── HADDOCK_BIBLE_README.md              # README
├── HADDOCK3_MASTER_GUIDE.md             # Comprehensive guide
├── HADDOCK3_ARM64_GUIDE.md              # Apple Silicon specific guide
├── HADDOCK3_QUICK_REFERENCE_CARD.md     # Quick reference
├── HADDOCK3_TROUBLESHOOTING.md          # Troubleshooting
├── HADDOCK3_QUICK_START_SP55_WORKING.md # SP55 project guide
└── HADDOCK_DATA_INTEGRITY_VERIFICATION_CHECKLIST.md
```

### 7.4 Integration Points
**Configuration Files (.toml):**
```toml
# Location: EXPERIMENTS/sp55-skin-regeneration/
# Example: krt14_fixed_authentic.toml

[parameters]
# Protein paths (ABSOLUTE - must preserve)
prot1_path = "/absolute/path/to/protein1.pdb"
prot2_path = "/absolute/path/to/protein2.pdb"

[run_dir]
# Output directory (ABSOLUTE - must preserve)
directory = "/absolute/path/to/output/"
```

### 7.5 Path Preservation Requirements
**EXTREMELY CRITICAL:** HADDOCK3 uses ABSOLUTE paths in `.toml` files:

1. **Protein PDB files** - Must use absolute paths
2. **Output directories** - Must use absolute paths
3. **Model paths** - Configured in installation
4. **Web server paths** - Configured for submission

**All `.toml` files reference absolute paths that MUST be preserved:**
```
EXPERIMENTS/sp55-skin-regeneration/
├── krt14_fixed.toml           # Absolute paths to KRT14 proteins
├── col1a2_fixed.toml          # Absolute paths to COL1A2 proteins
├── cd68_fixed.toml            # Absolute paths to CD68 proteins
├── tlr4_fixed.toml            # Absolute paths to TLR4 proteins
├── nkg2d_fixed.toml           # Absolute paths to NKG2D proteins
└── (all other .toml files)     # Each has absolute protein paths
```

### 7.6 Hardware Requirements
**Mac M3:** ✅ Fully supported (ARM64 build)
**NVIDIA Linux:** ✅ Native CUDA support

### 7.7 Working Status
✅ **Fully Working:**
- ✅ ARM64 build successful
- ✅ SP55 project integration (10 targets completed)
- ✅ Batch processing working
- ✅ Web server submission tested
- ✅ Local HADDOCK3 execution verified

### 7.8 Key Success Stories
- **SP55 Skin Regeneration Project:** 10 protein targets docked successfully
- **Batch Processing:** Multiple proteins processed in parallel
- **Web Server Integration:** Successfully submitted to HADDOCK web server

---

## 8. CABS (CABS-flex Docking)

### 8.1 Overview
**Purpose:** Flexible protein docking using CABS-flex algorithm
**Location:** `/Users/apple/code/Researcher-bio2/CABS/`
**Size:** Small (Python package)

### 8.2 Installation Status
✅ **Fully Installed**

### 8.3 Key Features
- ✅ Flexible protein-protein docking
- ✅ CABS-flex algorithm
- ✅ Python bindings
- ✅ Configuration files

### 8.4 Hardware Requirements
**Mac M3:** ✅ Works (CPU-based)
**NVIDIA Linux:** ✅ Works

### 8.5 Working Status
✅ **Working** (installation verified)

---

## 9. FAISS (Vector Database)

### 9.1 Overview
**Purpose:** Facebook AI Similarity Search - High-performance vector similarity search
**Location:** Installed in `.venv/lib/python*/faiss/`
**Integration:** Throughout the codebase

### 9.2 Installation Status
✅ **Fully Installed (faiss-cpu)**

### 9.3 Integration Points
```python
# Location: ai_researcher/tools/enhanced_faiss.py
from ai_researcher.tools.enhanced_faiss import EnhancedFAISS

# Location: ai_researcher/pipeline_v2/faiss_integration.py
from ai_researcher.pipeline_v2.faiss_integration import FAISSManager

# Location: ai_researcher/core/faiss_database.py
from ai_researcher.core.faiss_database import FAISSDatabase
```

### 9.4 Usage
- ✅ Literature similarity search
- ✅ Citation clustering
- ✅ Reference matching
- ✅ Fast nearest-neighbor search

### 9.5 Hardware Requirements
**Mac M3:** ✅ Works (faiss-cpu)
**NVIDIA Linux:** ✅ Works (faiss-gpu available)

### 9.6 Working Status
✅ **Fully Working** (used throughout pipelines)

---

## 10. ColabDesign

### 10.1 Overview
**Purpose:** Protein design using ML-based structure prediction (Google DeepMind)
**Integration:** Used by BindCraft-Expanded's de novo engine
**Location:** BindCraft dependency (installed in BindCraft environment)

### 10.2 Installation Status
✅ **Installed via BindCraft**

### 10.3 Known Issues
⚠️ **nan Coordinate Problem:**
- **Issue:** Outputs PDB files with nan coordinates on low pLDDT trajectories
- **Impact:** scipy.spatial.cKDTree crashes
- **Root Cause:** Low-confidence predictions contain invalid coordinates
- **Solution Required:** Filter trajectories by pLDDT score before use

### 10.4 Working Status
⚠️ **Partially Working** (needs filtering patch)

---

## 11. Cross-Framework Integration

### 11.1 BindCraft as Central Hub
```
BindCraft-Expanded/
├── core/boltz_engine.py       → Boltz integration
├── core/peptide_engine.py      → Chai-1 integration
├── core/docking_engine.py      → Native implementation
├── core/de_novo_engine.py      → ColabDesign integration
└── api/                         → All endpoints accessible
```

### 11.2 Workflow Examples

**Protein Structure Prediction:**
```
User Request → BindCraft API → BoltzEngine → Boltz (installed in .venv)
                                            ↓
                                       Structure Prediction
```

**Peptide Docking:**
```
User Request → BindCraft API → PeptideEngine → Chai-1 MPS Patch → Chai-Lab
                                                        ↓
                                                   ESM2 Embeddings (MPS)
                                                        ↓
                                                   Peptide Docking
```

**Protein-Protein Docking:**
```
User Request → BindCraft API → DockingEngine → Native Implementation
                                                   ↓
                                              Docking Prediction
```

---

## 12. Hardware Compatibility Matrix

| Framework | Mac M3 | NVIDIA Linux | Notes |
|-----------|--------|--------------|-------|
| BindCraft-Expanded | ✅ Full | ✅ Full | Works on both |
| Boltz | ⚠️ CPU only | ✅ GPU | Slow on Mac |
| OpenFold | ⚠️ CPU only | ✅ GPU | Impractical on Mac |
| DiffDock | ⚠️ CPU only | ✅ GPU | Slow on Mac |
| Chai-Lab | ⚠️ Patched | ✅ Native | MPS patch created |
| BioNeMo | ✅ MPS | ✅ CUDA | Mac guide created |
| HADDOCK3 | ✅ ARM64 | ✅ CUDA | ARM64 build working |
| CABS | ✅ CPU | ✅ CUDA | Works on both |
| FAISS | ✅ CPU | ✅ GPU | CPU version used |
| ColabDesign | ✅ CPU | ✅ GPU | Works, has nan issue |

---

## 13. Path Preservation Summary

### 13.1 Critical Paths to Preserve

**BindCraft-Expanded:**
```
/Users/apple/code/Researcher-bio2/BindCraft-Expanded/
├── core/                       # DON'T MOVE - all engine files
├── api/                        # DON'T MOVE - all endpoints
├── bindcraft_original/          # DON'T MOVE - core implementation
├── user_runs/                   # DON'T MOVE - output directory
└── frontend/                    # DON'T MOVE - web UI files
```

**Boltz (installed in .venv):**
```
/Users/apple/code/Researcher-bio2/
├── .venv/lib/python*/boltz/     # DON'T MOVE - installation
├── boltz_test.yaml              # DON'T MOVE - config file
└── boltz_output/                # DON'T MOVE - output directory
```

**HADDOCK3 (.toml configs):**
```
EXPERIMENTS/sp55-skin-regeneration/
├── *_fixed.toml                # DON'T MOVE - has absolute paths
└── *_final.toml                # DON'T MOVE - has absolute paths
```

**Chai-Lab:**
```
/Users/apple/code/Researcher-bio2/chai-lab/
├── chai_lab/                   # DON'T MOVE - core implementation
└── BindCraft-Expanded/core/     # DON'T MOVE - integration files
    ├── chai_mps_patch.py
    └── peptide_engine.py
```

**DiffDock:**
```
/Users/apple/code/Researcher-bio2/DiffDock/
├── .p.npy                      # DON'T MOVE - model weights
├── .score.npy                  # DON'T MOVE - model weights
└── .so3_*.npy                  # DON'T MOVE - model weights
```

### 13.2 Path Preservation Rules

1. **DO NOT** move `BindCraft-Expanded/` or its subdirectories
2. **DO NOT** move `.venv/` or modify Boltz installation paths
3. **DO NOT** move `chai-lab/` or its subdirectories
4. **DO NOT** move `DiffDock/` or its model files
5. **DO NOT** move any `.toml` files (they contain absolute paths)
6. **DO NOT** modify the `activate` script without testing ALL frameworks

---

## 14. Installation Commands Reference

### 14.1 BindCraft-Expanded
```bash
# Already installed, no action needed
# Location: /Users/apple/code/Researcher-bio2/BindCraft-Expanded/
```

### 14.2 Boltz
```bash
# Already installed in .venv
source activate
pip show boltz  # Verify installation
```

### 14.3 OpenFold
```bash
# Code installed, models need download
# Location: /Users/apple/code/Researcher-bio2/openfold/

# To download models (requires ~5GB):
# Follow instructions in openfold/docs/
```

### 14.4 DiffDock
```bash
# Already installed with models
# Location: /Users/apple/code/Researcher-bio2/DiffDock/
```

### 14.5 Chai-Lab
```bash
# Already installed (git submodule)
# Location: /Users/apple/code/Researcher-bio2/chai-lab/
```

### 14.6 HADDOCK3
```bash
# External installation, already complete
# See: SUP-PROMPTS/HADDOCK3_ARM64_GUIDE.md
```

### 14.7 BioNeMo
```bash
# Framework installed, not fully configured
# Location: /Users/apple/code/Researcher-bio2/bionemo/
# See: bionemo/BIONEMO_MAC_USAGE_GUIDE.md
```

---

## 15. Working Status Summary

### 15.1 Fully Working (Ready for Use)
- ✅ BindCraft-Expanded (docking, web API)
- ✅ Boltz (structure prediction)
- ✅ DiffDock (small molecule docking)
- ✅ HADDOCK3 (protein docking, ARM64)
- ✅ CABS (flexible docking)
- ✅ FAISS (vector database)

### 15.2 Partially Working (Needs Configuration/Testing)
- ⚠️ OpenFold (needs model download)
- ⚠️ Chai-Lab (MPS patch created, needs full test)
- ⚠️ BioNeMo (framework present, needs configuration)
- ⚠️ BindCraft de novo (needs nan filtering)

### 15.3 Mac M3 Limitations
- Slow CPU-only inference for structure prediction
- MPS patch needed for Chai-1 (created, not tested)
- No CUDA support for GPU acceleration

### 15.4 NVIDIA Recommendations
- Required for practical OpenFold usage
- Required for fast DiffDock predictions
- Required for Boltz GPU acceleration
- Native Chai-1 support (no patch needed)

---

## 16. Next Steps

### 16.1 Immediate Actions
1. Test Chai-1 MPS patch with full docking pipeline
2. Add pLDDT filtering to BindCraft de novo engine
3. Download and test OpenFold models
4. Configure BioNeMo for drug discovery workflows

### 16.2 Documentation Needs
1. Create workflow diagrams for cross-framework integration
2. Document API endpoints for all frameworks
3. Create troubleshooting guides for common issues
4. Write migration guide from Mac to Linux

---

**Analysis Complete**
**Total Frameworks:** 10
**Fully Working:** 6
**Partially Working:** 4
**Mac M3 Compatible:** 8
**NVIDIA Recommended:** 6
