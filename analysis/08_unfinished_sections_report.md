# Unfinished Sections Report

**Generated:** 2025-01-04
**Analysis Phase:** Phase 1 - Deep Codebase Analysis
**Status:** Identification of Confusing/Unfinished Code Sections

## Executive Summary

This document identifies areas of the codebase that are **unfinished, confusing, or have unclear hardware requirements**. These sections need clarification to distinguish between what requires **NVIDIA Linux** vs what works on **Mac M3**.

**Purpose:** Help future developers (and the user) understand:
- What code is incomplete and needs work
- What requires NVIDIA GPU vs Mac M3
- What was attempted but abandoned
- What needs clarification before use

---

## Critical Unfinished Sections

### 1. Chai-1 MPS Patch (Created but Untested)

**Location:** `BindCraft-Expanded/core/chai_mps_patch.py`

**Status:** ⚠️ **CREATED BUT NOT FULLY TESTED**

**Problem:**
- Chai-1's ESM2 model is CUDA-traced TorchScript
- Cannot run on Apple Silicon MPS (GPU)
- Blocks Chai-1 usage on Mac M3

**Solution Created:**
```python
# File: BindCraft-Expanded/core/chai_mps_patch.py
# Purpose: Replace CUDA-traced ESM2 with HuggingFace Transformers

from core.chai_mps_patch import apply_mps_patch
apply_mps_patch()

# Now Chai-1 works on MPS
from chai_lab.chai1 import run_inference
candidates = run_inference(device="mps", use_esm_embeddings=True)
```

**What's Untested:**
- ⏳ Full pipeline execution with MPS patch
- ⏳ ESM2 3B model (requires 50GB disk space)
- ⏳ Production-level peptide docking
- ⏳ Performance benchmarks vs CUDA

**Hardware Requirements:**
- **Mac M3:** Requires MPS patch (created but untested)
- **NVIDIA Linux:** Native support, no patch needed

**Test Files Created:**
- `BindCraft-Expanded/test_chai_mps.py` - MPS test (needs patch)
- `BindCraft-Expanded/test_chai_mps_hq.py` - High-quality test (needs 3B model)

**Blocker:** Disk space - Need 50GB free for ESM2 3B model

---

### 2. ColabDesign nan Coordinate Filtering

**Location:** `BindCraft-Expanded/core/` (de novo engine)

**Status:** ⚠️ **ROOT CAUSE IDENTIFIED, SOLUTION DESIGNED, IMPLEMENTATION PENDING**

**Problem:**
- ColabDesign outputs PDB files with nan coordinates on low pLDDT trajectories
- scipy.spatial.cKDTree crashes when processing these files
- De novo design subprocess fails

**Root Cause:**
```python
# Low-confidence predictions produce invalid coordinates
# pLDDT < 70 trajectories → nan coordinates
# scipy.spatial.cKDTree cannot handle nan → crash
```

**Solution Designed:**
```python
# Add pLDDT threshold filtering before KDTree construction
def filter_low_plddt(pdb_file, threshold=70):
    """Filter trajectories by pLDDT score."""
    # Keep only high-confidence structures
    # Implementation pending
```

**What's Missing:**
- ⏳ pLDDT filtering implementation
- ⏳ Integration into de novo pipeline
- ⏳ Testing with real data
- ⏳ Performance validation

**Hardware Requirements:**
- **Both Mac M3 and NVIDIA Linux:** Same issue (ColabDesign problem)
- **Fix Location:** BindCraft de novo subprocess code

**Test Files Affected:**
- `test_bindcraft_denovo.py` - May fail due to nan coordinates

---

### 3. BindCraft De Novo Subprocess Failures

**Location:** `BindCraft-Expanded/core/` (subprocess management)

**Status:** ⚠️ **INTERMITTENT FAILURES DUE TO nan COORDINATES**

**Symptoms:**
- De novo design subprocess crashes randomly
- Some trajectories succeed, others fail
- Error: `ValueError: array contains NaN, not a valid number`

**What's Known:**
- ✅ Root cause identified (nan coordinates)
- ✅ Solution designed (pLDDT filtering)
- ❌ Implementation incomplete

**What's Needed:**
1. Implement pLDDT filtering in subprocess
2. Add error handling for nan values
3. Filter low-confidence trajectories before processing
4. Test with comprehensive dataset

**Hardware Requirements:**
- **Mac M3:** Same issue (CPU-based ColabDesign)
- **NVIDIA Linux:** Same issue (ColabDesign problem)

---

### 4. OpenFold Integration (Incomplete)

**Location:** `OpenFold/` directory

**Status:** ⚠️ **INSTALLED BUT NOT INTEGRATED**

**Problem:**
- OpenFold installed but not actively used
- No clear integration point in pipelines
- Performance impractical on Mac M3 (CPU only)

**Hardware Requirements:**
- **Mac M3:** ⚠️ CPU only, extremely slow (not recommended)
- **NVIDIA Linux:** ✅ GPU acceleration, production-ready

**Integration Status:**
- ❌ No BindCraft integration
- ❌ No pipeline integration
- ❌ No API endpoints
- ❌ No documentation for usage

**What's Missing:**
- Integration into BindCraft or Boltz
- Performance benchmarks
- Usage examples
- Documentation

**Recommendation:** Use Boltz instead (already integrated and working)

---

### 5. DiffDock Integration (Partial)

**Location:** `DiffDock/` directory

**Status:** ⚠️ **INSTALLED WITH PRE-TRAINED MODELS, PARTIALLY INTEGRATED**

**What's Working:**
- ✅ DiffDock installed with dependencies
- ✅ Pre-trained models downloaded
- ✅ Basic inference functional

**What's Missing:**
- ⏳ BindCraft API integration
- ⏳ Batch processing pipeline
- ⏳ Production-ready endpoints
- ⏳ Performance optimization

**Hardware Requirements:**
- **Mac M3:** ⚠️ CPU only, slow but functional
- **NVIDIA Linux:** ✅ GPU acceleration, fast

**Tool Suitability:**
- ✅ **Best For:** Small molecule docking
- ❌ **NOT For:** Peptides or protein-protein docking

**Current Status:**
- Can run inference manually
- Not integrated into automated pipelines
- No API endpoints

---

### 6. Modulus Integration (Not Started)

**Location:** Not clearly present in codebase

**Status:** ❌ **NOT INTEGRATED**

**Problem:**
- Modulus mentioned in documentation
- No clear installation or integration
- No usage examples

**Hardware Requirements:**
- **Mac M3:** ❌ Not compatible (requires CUDA)
- **NVIDIA Linux:** ✅ Native support

**What's Needed:**
- Installation verification
- Integration planning
- Documentation
- Hardware requirements clarification

---

### 7. CycleReviewer Local Models (NVIDIA Only)

**Location:** `ai_researcher/cycle_reviewer.py`

**Status:** ⚠️ **REQUIRES NVIDIA GPU, NOT TESTED ON MAC M3**

**Problem:**
- CycleReviewer requires local model inference
- Models (8B, 70B, 123B) need GPU
- No Mac M3 MPS support documented

**Hardware Requirements:**
- **Mac M3:** ❌ Not supported (no MPS conversion)
- **NVIDIA Linux:** ✅ Required for local models

**Workaround:**
- Use GPT-5 API instead (CycleResearcher does this)
- Or use cloud inference for local models

**Current Status:**
- CycleReviewer exists but likely non-functional on Mac
- No error handling for missing GPU
- No fallback to CPU/MPS documented

---

### 8. DeepReviewer Multi-Perspective Review (Partial)

**Location:** `ai_researcher/deep_reviewer.py`

**Status:** ⚠️ **GPT-5 INTEGRATION WORKING, LOCAL MODELS UNTESTED**

**What Works:**
- ✅ GPT-5 based review (cloud API)
- ✅ Multi-perspective simulation
- ✅ Self-verification logic

**What's Untested:**
- ⏳ Local model integration (7B, 14B)
- ⏳ Mac M3 compatibility
- ⏳ Performance benchmarks

**Hardware Requirements:**
- **Mac M3:** ✅ GPT-5 API works perfectly
- **NVIDIA Linux:** ✅ Full support (API + local)

**Clarification Needed:**
- Local model support status on Mac M3
- MPS conversion for local review models
- Fallback behavior when GPU unavailable

---

## Confusing Sections Needing Clarification

### 1. BindCraft API Endpoints (Mixed Status)

**Location:** `BindCraft-Expanded/api/`

**Issue:** Some endpoints work, others don't - not clearly documented

**Endpoints Status:**
- `/predict` - ✅ Working (Boltz)
- `/design` - ⚠️ Partial (de novo issues)
- `/peptide` - ⚠️ Needs MPS patch testing
- `/analyze` - ✅ Working (basic analysis)
- `/chat` - ✅ Working (AI assistant)

**What's Confusing:**
- No clear status documentation for each endpoint
- No error handling for unsupported features
- No hardware requirement indicators

**Needs:**
- Clear endpoint status matrix
- Hardware requirement tags
- Error handling for unsupported features
- Usage examples for each endpoint

---

### 2. HADDOCK3 Configuration Files (Path Issues)

**Location:** `EXPERIMENTS/sp55-skin-regeneration/*.toml`

**Issue:** ABSOLUTE paths hardcoded in all configs

**Example:**
```toml
# krt14_fixed.toml
[parameters]
prot1 = "/Users/apple/code/Researcher-bio2/EXPERIMENTS/sp55-skin-regeneration/protein_krt14.pdb"
```

**Problem:**
- Moving files breaks all configs
- No relative path support
- 20+ config files to update if moved

**Hardware Requirements:**
- **Both Mac M3 and NVIDIA Linux:** Same issue (path problem)

**Needs:**
- Path migration strategy
- Relative path conversion script
- Documentation of path dependencies

---

### 3. Model Path Configuration (Scattered)

**Issue:** Model paths hardcoded in multiple locations

**Affected Components:**
- BindCraft: Model paths in config
- Boltz: Checkpoint paths in config
- Chai-1: Model cache paths
- DiffDock: Model paths in code

**What's Confusing:**
- No centralized model management
- No clear model location documentation
- Scattered path references

**Needs:**
- Centralized model path configuration
- Model location documentation
- Path verification scripts

---

### 4. Environment Variable Dependencies (Unclear)

**Issue:** Some components require specific environment variables

**Examples:**
- `OPENAI_API_KEY` - Required for GPT-5
- `CUDA_VISIBLE_DEVICES` - Required for NVIDIA
- `SAKANA_PRINCIPLE_STRICT` - Validation framework
- `TESTING` - Test mode flag

**What's Confusing:**
- No comprehensive list of required env vars
- No documentation of defaults
- No validation of env vars at startup

**Needs:**
- Environment variable documentation
- Startup validation
- Clear error messages for missing vars

---

### 5. Pipeline Configuration (Complex)

**Location:** `PIPELINE_2_DEVELOPMENT/`

**Issue:** Multiple configuration files, unclear relationships

**Config Files:**
- `universal_research_config.py`
- `cambridge_sai_config.py`
- Various experiment configs

**What's Confusing:**
- How configs relate to each other
- Which config takes precedence
- How to customize for specific needs

**Needs:**
- Config hierarchy documentation
- Usage examples
- Customization guide

---

## Abandoned or Deprecated Sections

### 1. Old BindCraft (Original)

**Location:** `BindCraft/` (not BindCraft-Expanded)

**Status:** ⚠️ **DEPRECATED, USE BindCraft-Expanded**

**Why Deprecated:**
- Replaced by BindCraft-Expanded
- Missing newer features
- Not actively maintained

**Recommendation:** Remove or archive

---

### 2. Westlake-12B Model

**Location:** `westlake-12b/` directory

**Status:** ⚠️ **UNUSED, MARKED FOR CLEANUP**

**Issue:**
- 13GB model files
- Not used in any pipeline
- Taking up disk space

**Recommendation:** Delete or archive externally

---

### 3. Duplicate Experiment Folders

**Issue:** Multiple experiment folders with similar names

**Examples:**
- `n1kr-antagonist-screening/` (430 files)
- `nk1r_antagonist-screening/` (15 files)
- `nk1r-antagonist-screening/` (12 files)

**Status:** ⚠️ **CONFUSING, POSSIBLE DUPLICATES**

**Needs:**
- Consolidation or clarification
- Clear naming conventions
- Documentation of differences

---

### 4. Old Test Files

**Issue:** Multiple redundant test files

**Examples:**
- `test_bindcraft*.py` (multiple variants)
- Duplicate test names
- Unclear which tests are current

**Status:** ⚠️ **NEEDS CLEANUP**

**Recommendation:** Consolidate into single test file per functionality

---

## Missing Documentation Sections

### 1. Installation Guides (Incomplete)

**What's Missing:**
- ❌ BindCraft installation guide
- ❌ Chai-1 installation steps
- ❌ MPS patch application instructions
- ❌ HADDOCK3 ARM64 build guide
- ❌ Environment setup from scratch

**Needs:**
- Step-by-step installation guides
- Platform-specific instructions
- Troubleshooting sections
- Verification steps

---

### 2. Usage Examples (Scarce)

**What's Missing:**
- ❌ BindCraft API usage examples
- ❌ Chai-1 docking examples
- ❌ Pipeline execution examples
- ❌ Custom experiment setup

**Needs:**
- Jupyter notebooks
- Example scripts
- Usage documentation
- Expected outputs

---

### 3. Troubleshooting Guides (Missing)

**What's Missing:**
- ❌ Common error patterns
- ❌ Hardware-specific issues
- ❌ Debug procedures
- ❌ Log interpretation

**Needs:**
- Troubleshooting guides
- FAQ sections
- Debug checklists
- Error message explanations

---

## Hardware-Specific Clarifications Needed

### Mac M3 Specific Issues

**Works Well:**
- ✅ BindCraft-Expanded (full functionality)
- ✅ HADDOCK3 (ARM64 build)
- ✅ CycleResearcher (GPT-5 API)
- ✅ DeepReviewer (GPT-5 API)
- ✅ Validation frameworks

**Needs Work:**
- ⚠️ Chai-1 (MPS patch created, untested)
- ⚠️ Boltz (CPU only, slow)
- ⚠️ DiffDock (CPU only, slow)
- ⚠️ OpenFold (CPU only, impractical)

**Doesn't Work:**
- ❌ CycleReviewer local models
- ❌ Modulus (CUDA required)
- ❌ Some BioNeMo features

---

### NVIDIA Linux Specific Advantages

**Major Benefits:**
- ✅ Full GPU acceleration
- ✅ All frameworks native support
- ✅ CycleReviewer local models
- ✅ OpenFold practical performance
- ✅ Boltz full speed
- ✅ DiffDock GPU acceleration

**Recommended For:**
- Production pipelines
- Large-scale experiments
- GPU-intensive workloads
- Local model inference

---

## Recommendations for Resolution

### Immediate Actions (Critical)

1. **Complete MPS Patch Testing**
   - Free up 50GB disk space
   - Download ESM2 3B model
   - Test Chai-1 with full pipeline
   - Document performance

2. **Implement pLDDT Filtering**
   - Add nan coordinate filtering
   - Integrate into de novo pipeline
   - Test with real data
   - Update test files

3. **Document Hardware Requirements**
   - Add hardware requirement tags
   - Create compatibility matrix
   - Update all documentation
   - Add error messages for unsupported hardware

### Medium-Term Actions

1. **Clean Up Unused Code**
   - Remove or archive deprecated sections
   - Consolidate duplicate files
   - Delete unused models (westlake-12b)
   - Organize experiment folders

2. **Improve Documentation**
   - Write installation guides
   - Create usage examples
   - Add troubleshooting sections
   - Document all configurations

3. **Clarify Confusing Sections**
   - Add status indicators
   - Create endpoint status matrix
   - Document path dependencies
   - Centralize model management

### Long-Term Actions

1. **Improve Error Handling**
   - Add hardware detection
   - Provide clear error messages
   - Suggest alternatives
   - Document workarounds

2. **Enhanced Testing**
   - Increase test coverage
   - Add hardware-specific tests
   - Create integration tests
   - Set up CI/CD

3. **Performance Optimization**
   - Benchmark Mac M3 vs NVIDIA
   - Optimize critical paths
   - Document performance characteristics
   - Provide scaling guidance

---

## Summary Table

| Section | Status | Mac M3 | NVIDIA | Action Needed |
|---------|--------|--------|--------|---------------|
| Chai-1 MPS Patch | Created but untested | ⚠️ Needs testing | ✅ Works | Test with full pipeline |
| ColabDesign nan fix | Solution designed | ⚠️ Same issue | ⚠️ Same issue | Implement pLDDT filter |
| BindCraft De Novo | Intermittent failures | ⚠️ Nan issue | ⚠️ Nan issue | Fix nan coordinates |
| OpenFold | Installed only | ❌ Too slow | ✅ Works | Integrate or remove |
| DiffDock | Partially integrated | ⚠️ Slow | ✅ Fast | Complete integration |
| Modulus | Not integrated | ❌ No CUDA | ✅ Required | Plan integration |
| CycleReviewer | NVIDIA only | ❌ No GPU | ✅ Required | Document workaround |
| DeepReviewer | GPT-5 works | ✅ API only | ✅ Full | Clarify local status |
| HADDOCK3 | Working | ✅ ARM64 | ✅ CUDA | Document paths |
| BindCraft API | Mixed status | ✅ Mostly | ✅ Full | Document endpoints |

---

**Analysis Complete**
**Unfinished Sections Identified:** 25+
**Critical Issues:** 8
**Hardware Clarifications Needed:** 15+
**Documentation Gaps:** 10+
**Recommendations:** Immediate, Medium, Long-term actions

**Next Steps:**
1. Prioritize critical issues (MPS patch, pLDDT filtering)
2. Document hardware requirements clearly
3. Clean up deprecated code
4. Improve documentation
5. Enhance testing coverage
