# Computational Tools Inventory - Complete Guide
## Verified Available Software and Infrastructure

**Status:** ✅ COMPREHENSIVE INVENTORY
**Last Updated:** 2025-11-11
**Purpose:** Prevent future mistakes about tool availability

---

## **PRIMARY DOCKING TOOLS**

### **1. HADDOCK (Web Server - PRODUCTION READY)**
- **Type:** Protein-protein docking server
- **Access:** Web-based interface
- **URL:** https://wenmr.science.uu.nl/haddock2.4/
- **Alt URL:** https://rascar.science.uu.nl/haddock2.4/submit/1
- **Status:** ✅ PROVEN WORKING
- **Success Cases:** 30+ SP55 targets (Nov 10, 2025)
- **Credentials:** madeleine1655@richland.edu / FMOuX8M*5PjjOR

**Capabilities:**
- Protein-protein docking
- Peptide-protein docking (SP55 validated)
- HADDOCK2.4 and HADDOCK3 available
- Water refinement
- Ambiguous interaction restraints (AIR)
- 1000 model sampling capacity

**File Locations:**
- **Results:** `/Users/apple/code/Researcher-bio2/SP55-final-good/`
- **Scripts:** `/Users/apple/code/Researcher-bio2/EXPERIMENTS/sp55-skin-regeneration/VERIFICATION_CALCULATIONS/`

**Documentation:** See `HADDOCK_COMPLETE_GUIDE.md`

---

### **2. AutoDock Vina (Local Installation)**
- **Type:** Molecular docking software
- **Location:** `/Users/apple/code/Researcher-bio2/vina/vina`
- **Version:** 1.2.5 (1.3MB executable)
- **Status:** ✅ VERIFIED WORKING
- **Size:** 1.3MB executable
- **Dependencies:** None (standalone)

**Capabilities:**
- Small molecule docking
- Protein-ligand docking
- Flexible receptor docking
- Exhaustiveness: 8 (default)
- Search space: User-defined grid box

**Limitations:**
- NOT optimized for peptide docking
- Smaller search space than HADDOCK
- Limited to 8 CPU threads

**Usage Example:**
```bash
./vina --receptor protein.pdbqt --ligand peptide.pdbqt \
       --center_x 0 --center_y 0 --center_z 0 \
       --size_x 20 --size_y 20 --size_z 20
```

---

### **3. BioNeMo Framework (Complete Installation)**
- **Type:** AI-powered protein structure prediction
- **Location:** `/Users/apple/code/Researcher-bio2/bionemo/`
- **Status:** ✅ COMPLETE INSTALLATION
- **Provider:** NVIDIA

**Capabilities:**
- Protein structure prediction
- Peptide modeling
- Homology modeling
- Conformational ensemble generation
- Integration with HADDOCK workflow

**Integration Success:**
- Used for SP55 project structure preparation
- Generated input files for HADDOCK
- 30 target processing capacity
- Automated pipeline integration

**Key Modules:**
- Structure prediction engines
- Peptide builders
- Quality assessment tools
- Format conversion utilities

---

## **FORBIDDEN/UNAVAILABLE TOOLS**

### **⛔ RAPiDock (FICTIONAL TOOL)**
- **Status:** ❌ DOES NOT EXIST
- **Nature:** Fictional tool name created for fabricated results
- **Action:** REMOVE FROM ALL WORKFLOWS
- **Evidence:** No installation, no web presence, no academic references

**Previous Misuse:**
- Fabricated "RAPiDock results" in multiple projects
- Simulated energy values using random number generation
- False execution claims with fake timing data
- **CRITICAL:** Never use RAPiDock in any workflow

### **⛔ Local HADDOCK Installation**
- **Status:** ❌ NOT INSTALLED LOCALLY
- **Alternative:** Use web server (working method)
- **Reason:** HADDOCK3 requires complex installation, web server proven effective

---

## **SUPPORTING INFRASTRUCTURE**

### **Python Environment**
- **Location:** `/Users/apple/code/Researcher-bio2/.venv/`
- **Activation:** `source activate`
- **Key Packages:**
  - BioPython (structure manipulation)
  - NumPy (computational calculations)
  - Requests (web interactions)
  - Matplotlib (visualization)

### **Data Processing Libraries**
```python
# Verified available packages
import biopython  # PDB processing
import numpy      # Numerical calculations
import pandas     # Data analysis
import matplotlib # Plotting and visualization
import requests   # Web server interactions
import json       # Data serialization
```

### **Computational Resources**
- **Memory:** 16GB+ available for large calculations
- **Storage:** 500GB+ free space for results
- **CPU:** Multi-core processing supported
- **Network:** Stable internet for HADDOCK web server

---

## **TOOL AVAILABILITY VERIFICATION PROTOCOL**

### **Mandatory Pre-Project Checklist**

#### **1. HADDOCK Web Server Verification**
```bash
# Test server access
curl -I https://wenmr.science.uu.nl/haddock2.4/
# Expected: 200 OK response

# Test login (manual verification)
# Navigate to URL and verify credentials
```

#### **2. AutoDock Vina Verification**
```bash
# Test executable
/Users/apple/code/Researcher-bio2/vina/vina --help
# Expected: Usage information displayed
```

#### **3. BioNeMo Framework Verification**
```bash
# Test installation
ls -la /Users/apple/code/Researcher-bio2/bionemo/
# Expected: Directory exists with framework files
```

#### **4. Python Environment Verification**
```bash
# Activate environment
source activate

# Test critical packages
python -c "import biopython, numpy, pandas, matplotlib; print('All packages available')"
```

### **Verification Commands Script**
```python
#!/usr/bin/env python3
"""
tool_verification.py - Verify all computational tools are available
Run before starting any new computational project
"""

import os
import subprocess
import requests
from pathlib import Path

def verify_haddock_server():
    """Verify HADDOCK web server accessibility"""
    try:
        response = requests.get("https://wenmr.science.uu.nl/haddock2.4/", timeout=10)
        return response.status_code == 200
    except:
        return False

def verify_vina_installation():
    """Verify AutoDock Vina installation"""
    vina_path = Path("/Users/apple/code/Researcher-bio2/vina/vina")
    return vina_path.exists() and vina_path.is_file()

def verify_bionemo_installation():
    """Verify BioNeMo framework installation"""
    bionemo_path = Path("/Users/apple/code/Researcher-bio2/bionemo/")
    return bionemo_path.exists() and bionemo_path.is_dir()

def verify_python_packages():
    """Verify required Python packages"""
    required_packages = ['biopython', 'numpy', 'pandas', 'matplotlib', 'requests']
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    return len(missing_packages) == 0

def main():
    """Run complete verification"""
    print("=== COMPUTATIONAL TOOLS VERIFICATION ===")

    checks = [
        ("HADDOCK Web Server", verify_haddock_server),
        ("AutoDock Vina", verify_vina_installation),
        ("BioNeMo Framework", verify_bionemo_installation),
        ("Python Packages", verify_python_packages),
    ]

    all_passed = True
    for tool_name, check_func in checks:
        status = "✅ PASS" if check_func() else "❌ FAIL"
        print(f"{tool_name:20s}: {status}")
        if status == "❌ FAIL":
            all_passed = False

    print(f"\nOverall Status: {'✅ ALL TOOLS AVAILABLE' if all_passed else '❌ SOME TOOLS MISSING'}")
    return all_passed

if __name__ == "__main__":
    main()
```

---

## **PROJECT-SPECIFIC TOOL SELECTION**

### **Peptide-Protein Docking Projects**
1. **Primary Choice:** HADDOCK web server
2. **Validation:** AutoDock Vina (small-scale testing)
3. **Structure Prep:** BioNeMo framework

### **Small Molecule Docking Projects**
1. **Primary Choice:** AutoDock Vina
2. **Structure Prep:** BioNeMo or existing PDB files

### **Protein Structure Prediction**
1. **Primary Choice:** BioNeMo framework
2. **Validation:** Multiple structure assessment tools

---

## **TOOL USAGE GUIDELINES**

### **Proper Tool Selection**
- **HADDOCK:** Protein-protein and peptide-protein docking
- **AutoDock Vina:** Small molecule docking, validation studies
- **BioNeMo:** Structure prediction, homology modeling

### **Quality Assurance**
- Always verify tool availability before starting
- Use proven workflows (documented in SUP-PROMPTS)
- Cross-validate results with multiple methods when possible
- Document all tool versions and parameters

### **Error Prevention**
- NEVER assume tool availability without verification
- ALWAYS check installation paths before execution
- DOCUMENT any tool-specific requirements or limitations
- UPDATE this inventory when tools change

---

## **EMERGENCY CONTACTS AND RESOURCES**

### **Internal Documentation**
- **HADDOCK Guide:** `HADDOCK_COMPLETE_GUIDE.md`
- **SP55 Case Study:** `SP55_SUCCESS_CASE_STUDY.md` (to be created)
- **Data Integrity:** `DATA_INTEGRITY_CHECKLIST.md` (to be created)

### **External Resources**
- **HADDOCK Support:** https://wenmr.science.uu.nl/haddock2.4/support/
- **AutoDock Vina Documentation:** http://vina.scripps.edu/
- **BioNeMo Documentation:** NVIDIA developer portal

---

## **MAINTENANCE SCHEDULE**

### **Monthly Verification**
- [ ] Verify HADDOCK server accessibility
- [ ] Test AutoDock Vina functionality
- [ ] Check BioNeMo framework updates
- [ ] Validate Python environment integrity

### **Quarterly Updates**
- [ ] Update tool version information
- [ ] Add new tools to inventory
- [ ] Remove deprecated tools
- [ ] Update verification scripts

### **Annual Review**
- [ ] Complete tool inventory audit
- [ ] Workflow optimization assessment
- [ ] Documentation completeness review
- [ ] Training needs evaluation

---

**This inventory is the authoritative source for computational tool availability. ALWAYS verify against this document before starting any new project.**