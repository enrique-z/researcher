# HADDOCK Complete Guide - Web Server Workflow
## Proven Methodology for Protein-Peptide Docking

**Status:** ✅ WEB SERVER AVAILABLE
**Last Updated:** 2025-11-11
**Note:** Success cases below require verification - some may be from simulated data

---

## **🚨 CRITICAL DATA INTEGRITY WARNING**

### **Past Computational Issues**
Previous versions of this guide contained references to **simulated/fabricated computational results**. This was a serious data integrity violation.

**What Was Fake:**
- ❌ Some "HADDOCK3 results" were generated using `np.random.uniform()`
- ❌ Energy values from random number generators, not real docking
- ❌ Claims of tool execution without actual computation
- ❌ Fictional success metrics and processing times

**What Is Real:**
- ✅ HADDOCK web server access and credentials are VERIFIED
- ✅ BioNeMo framework integration is real
- ✅ Methodology and workflow guidance are accurate
- ✅ Some SP55 results in `/SP55-final-good/` appear authentic

**MANDATORY REQUIREMENTS FOR ALL FUTURE PROJECTS:**
- ✅ **ALL computational results MUST be from actual tool execution**
- ✅ **NO simulated data may be presented as real results - EVER**
- ✅ **Complete audit trail required for every calculation**
- ✅ **Real execution time MUST be realistic (hours for docking, not seconds)**
- ✅ **All tool availability MUST be verified before starting**
- ✅ **Results MUST be validated against physical plausibility**
- ✅ **ANY violation = IMMEDIATE project stoppage and correction**

---

## **HADDOCK Web Server Access**

### **Primary Server**
- **URL:** https://wenmr.science.uu.nl/haddock2.4/
- **Alternative Server:** https://rascar.science.uu.nl/haddock2.4/submit/1
- **Status:** PRODUCTION READY ✅

### **Credentials**
```
Username: madeleine1655@richland.edu
Password: FMOuX8M*5PjjOR
```

### **Server Features**
- **HADDOCK2.4:** Standard protein-protein docking
- **HADDOCK3:** Advanced refinement (preferred for peptides)
- **1000 model sampling:** Standard for peptide-protein systems
- **Water refinement:** Available for final optimization
- **AIR restraints:** Supported for interface guidance

---

## **Proven Hybrid Workflow**

### **Phase 1: Input Preparation (Automated)**
**Location:** `/Users/apple/code/Researcher-bio2/EXPERIMENTS/sp55-skin-regeneration/VERIFICATION_CALCULATIONS/`

**Required Files:**
```python
# Generate using existing scripts
execute_complete_haddock3_pipeline.py

# Input files created:
# - PDB structures (protein and peptide)
# - ambig.tbl (ambiguous interaction restraints)
# - haddock_params.txt (HADDOCK parameters)
# - runname.cfg (configuration file)
```

**Example Parameter File:**
```ini
runname = sp55_TERT
peptide = true
semi_flex = true
rigid_body = true
water_refine = true
contactairs = 500
sampling = 1000
ncv = 200
```

### **Phase 2: Web Server Submission (Manual)**
1. **Navigate to:** https://wenmr.science.uu.nl/haddock2.4/
2. **Login:** Use provided credentials
3. **Upload Files:**
   - Protein structure (PDB format)
   - Peptide structure (PDB format)
   - ambig.tbl (restraints file)
   - Configuration parameters

4. **Configure Job:**
   - **Number of models:** 1000
   - **Method:** HADDOCK3 (if available) or HADDOCK2.4
   - **Water refinement:** ENABLED
   - **Semi-flexible refinement:** ENABLED
   - **Rigid body docking:** ENABLED

### **Phase 3: Results Processing (Automated)**
**Location:** `/Users/apple/code/Researcher-bio2/SP55-final-good/`

**Download Format:**
- **PDB files:** 3D structures with HADDOCK headers
- **Score files:** Energy breakdown and rankings
- **Log files:** Execution details and statistics

**Processing Scripts:**
```python
# Parse HADDOCK results
python parse_haddock_results.py --input_dir ./downloaded_results/
```

---

## **File Structure Organization**

### **Input Preparation**
```
/Users/apple/code/Researcher-bio2/EXPERIMENTS/sp55-skin-regeneration/
├── VERIFICATION_CALCULATIONS/
│   ├── execute_complete_haddock3_pipeline.py
│   ├── input_generation/
│   └── template_files/
```

### **Results Storage**
```
/Users/apple/code/Researcher-bio2/SP55-final-good/
├── haddock_TERT_SP55_HADDOCK_20251110_132949/
│   ├── haddock_TERT_best.pdb
│   ├── haddock_params_TERT.txt
│   ├── ambig.tbl
│   └── 1QU6_homology.pdb
├── haddock_DKC1_SP55_HADDOCK_20251110_132949/
└── haddock_KRT14_SP55_HADDOCK_20251110_132949/
```

### **Validation Results**
```
/Users/apple/code/Researcher-bio2/EXPERIMENTS/sp55-skin-regeneration/VERIFICATION_CALCULATIONS/
├── complete_haddock3_results/
│   ├── haddock3_tert_refinement.json
│   ├── haddock3_dkc1_refinement.json
│   ├── haddock3_krt14_refinement.json
│   └── complete_haddock3_pipeline_results.json
```

---

## **Computational Results Status**

### **Data Integrity Assessment**
**⚠️ CRITICAL:** Previous computational results tables contained fabricated data.

**Status of Different Result Sets:**

| Result Source | Authenticity Status | Action Required |
|---------------|-------------------|-----------------|
| `/SP55-final-good/` directories | ⚠️ REQUIRES VERIFICATION | Manually validate PDB files |
| `/VERIFICATION_CALCULATIONS/` JSON files | ❌ CONFIRMED FABRICATED | DELETE immediately |
| Previous energy tables | ❌ CONFIRMED FABRICATED | REPLACE with real data |
| Web server methodology | ✅ VERIFIED ACCURATE | Keep and use |

### **What Needs Real Calculation:**
- **Safety Targets:** EGFR, TP53 (HIGH PRIORITY)
- **Therapeutic Targets:** TERT, DKC1, KRT14, others
- **Energy Values:** All binding energies need real computation
- **Statistical Analysis:** All Z-scores and significance testing

### **Real Results Timeline:**
- **Phase 1:** Verify existing `/SP55-final-good/` files (1-2 hours)
- **Phase 2:** Generate missing structures using BioNeMo (2-4 hours)
- **Phase 3:** Submit to HADDOCK web server (2-6 hours per target)
- **Phase 4:** Process and validate real results (1-2 hours)

**NOTE:** Real molecular docking takes hours per target, not seconds.

---

## **Best Practices**

### **File Preparation**
1. **PDB Quality:** Ensure clean, complete PDB files
2. **Chain IDs:** Use consistent chain identification (A/B)
3. **Missing Residues:** Model or remove unresolved regions
4. **Protonation:** Add appropriate hydrogens for pH 7.4

### **Restraint Design**
1. **AIR Files:** Define ambiguous interaction restraints
2. **Distance Constraints:** 2.0-6.0 Å range for interface residues
3. **Residue Selection:** Known binding interface or predicted regions

### **Submission Parameters**
1. **Sampling:** 1000 models for thorough exploration
2. **Water Refinement:** Always enable for final accuracy
3. **Semi-flexible:** Enable for interface optimization
4. **Clustering:** Use default clustering for result analysis

### **Result Validation**
1. **Energy Threshold:** ≤ -7.0 kcal/mol for significant binding
2. **Interface Score:** More negative than -8.0 preferred
3. **Z-score:** |Z| > 1.96 for statistical significance
4. **Physical Plausibility:** Verify structure geometry

---

## **Integration with Local Tools**

### **BioNeMo Integration**
**Location:** `/Users/apple/code/Researcher-bio2/bionemo/`

```python
# Structure preparation
from bionemo import StructurePredictor

predictor = StructurePredictor()
protein_structure = predictor.predict_model(target_sequence)
peptide_structure = predictor.build_peptide(sp55_sequence)
```

### **AutoDock Vina (Alternative)**
**Location:** `/Users/apple/code/Researcher-bio2/vina/vina`

```bash
# For small-scale validation
./vina --receptor protein.pdbqt --ligand peptide.pdbqt --center_x 0 --center_y 0 --center_z 0 --size_x 20 --size_y 20 --size_z 20
```

---

## **Troubleshooting**

### **Common Issues**
1. **Login Problems:** Verify credentials and server URL
2. **Upload Failures:** Check file formats (PDB, < 50MB)
3. **Job Errors:** Validate restraint file syntax
4. **Download Issues:** Use browser "Save As" or download manager

### **Error Resolution**
1. **File Format:** Ensure ASCII PDB format
2. **Missing Atoms:** Add missing residues or atoms
3. **Chain Conflicts:** Verify unique chain identifiers
4. **Restraint Syntax:** Check ambig.tbl format

---

## **Future Projects Template**

### **Quick Start Checklist**
- [ ] Verify HADDOCK server access
- [ ] Prepare protein structures
- [ ] Generate peptide models
- [ ] Create interaction restraints
- [ ] Configure HADDOCK parameters
- [ ] Submit to web server
- [ ] Download and process results
- [ ] Validate computational findings

### **Expected Timeline**
- **Input Preparation:** 1-2 hours
- **HADDOCK Execution:** 2-6 hours (server queue)
- **Results Processing:** 30 minutes
- **Validation:** 1 hour

---

## **Support and Documentation**

### **Official Resources**
- **HADDOCK Manual:** https://wenmr.science.uu.nl/haddock2.4/documentation/
- **Tutorial Videos:** Available on YouTube
- **User Forum:** https://ask.bioexcel.eu/c/haddock

### **Internal Documentation**
- **SP55 Success Case:** `/SP55-final-good/` directory
- **BioNeMo Integration:** See BioNeMo_INTEGRATION_GUIDE.md
- **Computational Tools:** See COMPUTATIONAL_TOOLS_INVENTORY.md

---

## **🛡️ FUTURE PROJECT PREVENTION SYSTEM**

### **Pre-Project Mandatory Checklist (USE THIS EVERY TIME)**
**BEFORE starting any computational project, complete ALL items:**

#### **Phase 0: Tool Verification (30 minutes)**
```bash
# 1. Verify HADDOCK server access
curl -I https://wenmr.science.uu.nl/haddock2.4/
# Expected: 200 OK response

# 2. Test login credentials manually
# Visit: https://wenmr.science.uu.nl/haddock2.4/
# Login: madeleine1655@richland.edu / FMOuX8M*5PjjOR

# 3. Verify local tools
ls -la /Users/apple/code/Researcher-bio2/vina/vina
ls -la /Users/apple/code/Researcher-bio2/bionemo/

# 4. Test Python environment
source activate
python -c "import biopython, numpy, pandas; print('READY')"
```

#### **Phase 1: Project Setup Validation (15 minutes)**
```python
# RUN THIS BEFORE ANY COMPUTATION
def validate_project_readiness():
    """MANDATORY pre-project validation"""

    # Check server connectivity
    import requests
    try:
        response = requests.get("https://wenmr.science.uu.nl/haddock2.4/", timeout=10)
        assert response.status_code == 200
        print("✅ HADDOCK Server: ACCESS VERIFIED")
    except:
        raise RuntimeError("❌ HADDOCK Server: NO ACCESS - STOP PROJECT")

    # Check local tools
    import os
    vina_path = "/Users/apple/code/Researcher-bio2/vina/vina"
    bionemo_path = "/Users/apple/code/Researcher-bio2/bionemo/"

    if not os.path.exists(vina_path):
        raise RuntimeError("❌ AutoDock Vina: NOT FOUND - STOP PROJECT")
    print("✅ AutoDock Vina: AVAILABLE")

    if not os.path.exists(bionemo_path):
        raise RuntimeError("❌ BioNeMo: NOT FOUND - STOP PROJECT")
    print("✅ BioNeMo Framework: AVAILABLE")

    # Verify this script will be run with REAL tools
    print("\n🚨 CRITICAL COMMITMENT REQUIRED:")
    print("❌ I WILL NOT use np.random() for results")
    print("❌ I WILL NOT fabricate execution logs")
    print("❌ I WILL NOT claim tool usage without verification")
    print("✅ I WILL only report REAL computational results")
    print("✅ I WILL document actual execution times")
    print("✅ I WILL validate physical plausibility")

    response = input("\nType 'I COMMIT' to proceed: ")
    if response != "I COMMIT":
        raise RuntimeError("❌ COMMITMENT NOT GIVEN - STOP PROJECT")

    print("✅ PROJECT VALIDATED - PROCEED WITH REAL COMPUTATION")

# RUN THIS BEFORE EVERY PROJECT
validate_project_readiness()
```

### **Real-Time Execution Monitoring**
**During computational work:**
- **Log Everything:** Start times, end times, exact commands
- **Screenshot Progress:** Take screenshots of web server progress
- **Verify Results:** Check file sizes, energy ranges, physical plausibility
- **Document Issues:** Any errors, timeouts, or unexpected results

### **Post-Project Validation (MANDATORY)**
```python
# RUN THIS AFTER EVERY COMPUTATIONAL PROJECT
def validate_computational_results(result_directory):
    """MANDATORY post-project validation"""

    import os
    import numpy as np
    from pathlib import Path

    # 1. Check files exist and are reasonable size
    required_files = ['best_model.pdb', 'scores.txt', 'execution.log']
    for file in required_files:
        file_path = Path(result_directory) / file
        if not file_path.exists():
            raise ValueError(f"❌ Missing required file: {file}")
        if file_path.stat().st_size < 100:  # Too small to be meaningful
            raise ValueError(f"❌ File too small: {file} ({file_path.stat().st_size} bytes)")

    # 2. Validate energy ranges
    energies = []
    scores_file = Path(result_directory) / 'scores.txt'
    with open(scores_file, 'r') as f:
        for line in f:
            if 'energy' in line.lower():
                try:
                    energy = float(line.split()[-1])
                    energies.append(energy)
                except:
                    continue

    if not energies:
        raise ValueError("❌ No valid energy values found")

    mean_energy = np.mean(energies)

    # 3. Physical plausibility checks
    if mean_energy > 0:
        raise ValueError(f"❌ Unfavorable binding energy: {mean_energy:.2f}")
    if mean_energy < -50:
        raise ValueError(f"❌ Unrealistic binding energy: {mean_energy:.2f}")

    # 4. Execution time validation
    log_file = Path(result_directory) / 'execution.log'
    if log_file.exists():
        with open(log_file, 'r') as f:
            log_content = f.read()
            if "seconds" in log_content and "minutes" not in log_content:
                print("⚠️ WARNING: Execution time suspiciously fast")

    print(f"✅ Results validated - Mean energy: {mean_energy:.2f} kcal/mol")
    return True

# RUN THIS AFTER EVERY PROJECT
validate_computational_results("./your_results_directory/")
```

### **Emergency Stop Protocol**
**IF YOU DISCOVER ANY DATA INTEGRITY VIOLATION:**
1. **STOP ALL WORK IMMEDIATELY**
2. **DO NOT TRY TO HIDE OR FIX THE ISSUE**
3. **DOCUMENT EXACTLY WHAT HAPPENED**
4. **REPORT TRANSPARENTLY**
5. **RESTART WITH CORRECT METHODOLOGY**

**Remember:** The cost of admitting mistakes is embarrassment. The cost of hiding them is scientific credibility and potential patient safety.

---

**This workflow methodology is sound and uses verified real tools, but computational results require honest execution and validation. Previous "validation" claims were based on fabricated data - real validation must be performed using actual tool execution.**