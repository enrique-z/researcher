# 📚 Documentation Quick Reference Guide

**Last Updated:** January 4, 2025
**Status:** Complete - All documentation pushed to GitHub

---

## 🎯 Where to Find What's Working and What's Not

### PRIMARY GUIDES (Start Here)

| Document | Location | Purpose |
|----------|----------|---------|
| **README** | `/readme.md` | Main overview, features, quick start |
| **Hardware Requirements** | `/HARDWARE_REQUIREMENTS.md` | ⭐ **What works on Mac M3 vs NVIDIA** |
| **Unfinished Sections** | `/analysis/08_unfinished_sections_report.md` | ⭐ **What's broken, what needs work** |

---

## 📖 Complete Documentation Index

### Core Documentation (Phase 2)

```
/Users/apple/code/Researcher-bio2/
├── README.md                          ⭐ Main project overview
├── HARDWARE_REQUIREMENTS.md            ⭐ Platform compatibility matrix
├── REPRODUCIBILITY_GUIDE.md           ⭐ How to reproduce all experiments
└── DEVELOPMENT_HISTORY.md             ⭐ Timeline of what succeeded/failed
```

### Analysis Documents (Phase 1)

```
/Users/apple/code/Researcher-bio2/analysis/
├── 01_core_package_inventory.md       - 95 Python modules documented
├── 02_framework_integration.md        - 10 frameworks with path warnings
├── 03_experiments_catalog.md          - 17 experiments catalogued
├── 04_test_file_audit.md             - 22 test files audited
├── 05_hardware_requirements.md       - Detailed hardware analysis
├── 06_claude_code_history_summary.md  - 9,510 sessions summary
├── 07_antigravity_history_detailed.md - 8 conversations detailed
└── 08_unfinished_sections_report.md   - ⭐ Known issues and blockers
```

---

## ⚡ Quick Status Checks

### What Works on Mac M3 ✅

**Fully Working:**
- ✅ **CycleResearcher** - GPT-5 paper generation (~$5/paper)
- ✅ **DeepReviewer** - Multi-perspective review
- ✅ **BindCraft-Expanded** - Full API, protein docking
- ✅ **HADDOCK3** - ARM64 build optimized
- ✅ **Validation frameworks** - Domain-agnostic system

**Partial (Works with limitations):**
- ⚠️ **Boltz** - CPU only (slow), GPU on NVIDIA
- ⚠️ **DiffDock** - CPU only (slow), GPU on NVIDIA
- ⚠️ **Chai-1** - MPS patch created, needs testing

**Not Working:**
- ❌ **CycleReviewer** - Local models need NVIDIA GPU
- ❌ **OpenFold** - Too slow on Mac CPU
- ❌ **Modulus** - CUDA required

**See:** `/HARDWARE_REQUIREMENTS.md` (lines 18-36) for complete matrix

---

## 🔍 Known Issues and Blockers

### Critical Issues (from `/analysis/08_unfinished_sections_report.md`)

1. **Chai-1 MPS Patch** (Created but Untested)
   - Status: ⚠️ Patch created, needs testing
   - Blocker: Need 50GB disk space for ESM2 3B model
   - File: `BindCraft-Expanded/core/chai_mps_patch.py`

2. **ColabDesign nan Coordinates** (Root Cause Found)
   - Status: ⚠️ Solution designed, implementation pending
   - Issue: Low pLDDT trajectories produce invalid coordinates
   - Fix: Add pLDDT threshold filtering

3. **BindCraft De Novo Failures** (Intermittent)
   - Status: ⚠️ Related to nan coordinates issue
   - Symptom: Subprocess crashes randomly

4. **OpenFold Integration** (Incomplete)
   - Status: ⚠️ Installed but not integrated
   - Recommendation: Use Boltz instead

5. **DiffDock Integration** (Partial)
   - Status: ⚠️ Installed with models, not integrated into pipelines
   - Best for: Small molecule docking (NOT peptides)

**See:** `/analysis/08_unfinished_sections_report.md` for complete list

---

## 🚨 Critical Path Warnings

### ABSOLUTE PATH PRESERVATION (CRITICAL)

**From:** `/analysis/02_framework_integration.md` (lines 20-60)

⚠️ **ALL projects must maintain existing ABSOLUTE paths:**

```bash
# HADDOCK3 Configs (20+ files)
EXPERIMENTS/sp55-skin-regeneration/*.toml
# Example: prot1 = "/Users/apple/code/Researcher-bio2/..."

# Model Paths (scattered across frameworks)
BindCraft-Expanded/config/
Boltz/config/
Chai-1/cache/
DiffDock/ (in code)
```

**DO NOT CHANGE THESE PATHS** without updating all 20+ config files!

---

## 📊 Project Status Summary

### Completed Projects ✅

**SP55 Customer Project:**
- Status: **100% COMPLETE** (10/10 targets)
- Timeline: Nov-Dec 2025
- Targets: KRT14, COL1A2, CD68, TLR4, NKG2D, TP53, AQP1, CD19, CD3E, PPARG
- Deliverables: 50+ page report, 100+ validation files
- Location: `/EXPERIMENTS/sp55-skin-regeneration/`

**Published Papers:**
- ✅ NeurIPS 2025 - Drug discovery
- ✅ NVIDIA PhysicsNeMo - Molecular modeling

**See:** `/DEVELOPMENT_HISTORY.md` (lines 189-260) for SP55 details

---

## 🔧 Development History Timeline

### Key Phases (from `/DEVELOPMENT_HISTORY.md`)

1. **Phase 1:** Initial Setup (Early 2025)
2. **Phase 2:** Framework Integration (Early-Mid 2025)
3. **Phase 3:** Pipeline Development (Mid 2025)
4. **Phase 4:** Validation Systems (Mid-Late 2025)
5. **Phase 5:** Production Readiness (Nov-Dec 2025)
   - SP55 Customer Project completed
   - 2 papers published
6. **Phase 6:** Optimization (Dec 19-27, 2025)
   - Chai-1 MPS patch created
   - ColabDesign nan issue identified
   - Tool suitability analysis completed

**See:** `/DEVELOPMENT_HISTORY.md` for calendarized timeline

---

## 🛠️ How to Use This Codebase

### For AI Coders Working on This Project

**Step 1: Read the status guides**
```bash
# What works on your platform
cat HARDWARE_REQUIREMENTS.md | grep -A 20 "Quick Reference"

# What's broken and needs work
cat analysis/08_unfinished_sections_report.md | grep -A 5 "Critical"
```

**Step 2: Check framework status**
```bash
# Framework integration status
cat analysis/02_framework_integration.md | grep -E "Status:|Mac M3:|NVIDIA:"
```

**Step 3: Understand path dependencies**
```bash
# CRITICAL path warnings
cat analysis/02_framework_integration.md | grep -A 30 "CRITICAL.*Path"
```

**Step 4: Check recent development**
```bash
# Latest work (Dec 19-27, 2025)
cat analysis/07_antigravity_history_detailed.md | grep -A 10 "MOST RECENT"
```

**Step 5: Know what's tested**
```bash
# Test coverage
cat analysis/04_test_file_audit.md | grep -E "Status:|Coverage:"
```

---

## 📝 Git Commit Messages Guide

### Recent Commit with Full Documentation

**Commit:** `723b4ed` (just pushed)
**Message:** "docs: Comprehensive codebase analysis and documentation"

**This commit contains:**
- ✅ Working components clearly marked
- ✅ Partial/needs work components flagged
- ✅ NOT working components documented
- ✅ Critical path warnings
- ✅ SP55 project status
- ✅ Published papers listed

**Future commits should follow this pattern:**
1. Clearly state what's working
2. Flag what's partial/broken
3. Include platform compatibility (Mac M3 vs NVIDIA)
4. Reference relevant documentation files

---

## 🎯 Quick Reference Commands

### Check component status
```bash
# What works on Mac M3
grep -E "✅ Full|⚠️|❌" HARDWARE_REQUIREMENTS.md | head -20

# Known issues
grep -E "Status:.*⚠️|Status:.*❌" analysis/08_unfinished_sections_report.md

# Framework status
grep -E "Status:|Integration:" analysis/02_framework_integration.md
```

### Find specific guides
```bash
# SP55 project documentation
ls -la EXPERIMENTS/sp55-skin-regeneration/*.md | head -10

# HADDOCK3 guides
ls -la SUP-PROMPTS/HADDOCK*

# Test files
ls -la TESTS/
```

---

## 📞 Documentation for Future AI Coders

**When working on this codebase, always:**

1. ✅ **Check hardware compatibility first**
   - Read: `HARDWARE_REQUIREMENTS.md`
   - Know what works on your platform

2. ✅ **Review unfinished sections**
   - Read: `analysis/08_unfinished_sections_report.md`
   - Don't repeat work that's been done

3. ✅ **Respect critical path warnings**
   - Read: `analysis/02_framework_integration.md`
   - MAINTAIN all absolute paths

4. ✅ **Understand the history**
   - Read: `DEVELOPMENT_HISTORY.md`
   - Learn from past successes/failures

5. ✅ **Use the right tool for the job**
   - DiffDock: Small molecules
   - Chai-1: Peptides
   - BindCraft: Protein-protein
   - HADDOCK3: Comprehensive docking

---

## 📂 File Locations Summary

### Documentation
```
/Users/apple/code/Researcher-bio2/
├── readme.md                         (Main overview)
├── HARDWARE_REQUIREMENTS.md           (Platform compatibility)
├── REPRODUCIBILITY_GUIDE.md          (Reproduction guide)
├── DEVELOPMENT_HISTORY.md            (Timeline)
├── DOCUMENTATION_INDEX.md            (This file)
└── analysis/
    ├── 01_core_package_inventory.md
    ├── 02_framework_integration.md    (Path warnings)
    ├── 03_experiments_catalog.md
    ├── 04_test_file_audit.md
    ├── 05_hardware_requirements.md
    ├── 06_claude_code_history_summary.md
    ├── 07_antigravity_history_detailed.md
    └── 08_unfinished_sections_report.md  (Known issues)
```

### Key Projects
```
/Users/apple/code/Researcher-bio2/
├── EXPERIMENTS/sp55-skin-regeneration/    (Customer project - 100% done)
├── BindCraft-Expanded/                    (Protein docking - working)
├── chai-lab/                              (Peptide docking - MPS patch created)
├── DiffDock/                              (Small molecules - partial)
└── OpenFold/                              (Not integrated)
```

---

**🎉 All documentation is now on GitHub!**
**Repository:** https://github.com/enrique-z/researcher.git
**Commit:** 723b4ed
**Date:** January 4, 2025

---

## 💡 Pro Tips for AI Coders

1. **Start here:** `HARDWARE_REQUIREMENTS.md` (lines 18-36)
2. **Check issues:** `analysis/08_unfinished_sections_report.md`
3. **Respect paths:** `analysis/02_framework_integration.md` (CRITICAL section)
4. **Learn history:** `DEVELOPMENT_HISTORY.md` (Phase 6 for latest work)
5. **Reproduce results:** `REPRODUCIBILITY_GUIDE.md`

---

*This index created to help all future AI coders understand what's working, what's not, and where to find everything.*
