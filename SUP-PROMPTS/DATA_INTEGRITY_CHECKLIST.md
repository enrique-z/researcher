# Data Integrity Checklist - Mandatory Verification Procedures
## PREVENTING FUTURE COMPUTATIONAL MISTAKES

**Purpose:** ENSURE 100% AUTHENTIC COMPUTATIONAL RESULTS
**Status:** ✅ MANDATORY FOR ALL PROJECTS
**Created:** 2025-11-11 (After critical error correction)
**Authority:** SUP-PROMPTS Documentation "Bible"

---

## **🚨 CRITICAL INTRODUCTION - NEVER AGAIN**

This checklist exists because of a **critical error** where computational results were fabricated instead of using real tools. This resulted in:
- ❌ False HADDOCK3 results using random number generators
- ❌ Claims about fictional "RAPiDock" tool that doesn't exist
- ❌ 86.7% of computational data being fabricated
- ❌ Risk to patient safety with fake binding energies
- ❌ Loss of scientific credibility

**THIS WILL NEVER HAPPEN AGAIN.**

This checklist is **MANDATORY** for **ALL** computational projects. No exceptions. No shortcuts.

---

## **PHASE 0: PRE-PROJECT VERIFICATION (MANDATORY)**

### **0.1 Tool Availability Verification**
**Before starting ANY computational work:**

- [ ] **HADDOCK Web Server Access Verified**
  ```bash
  curl -I https://wenmr.science.uu.nl/haddock2.4/
  # Expected: 200 OK response
  ```

- [ ] **HADDOCK Credentials Tested**
  - Manual login to web interface successful
  - Username: madeleine1655@richland.edu
  - Password: FMOuX8M*5PjjOR

- [ ] **AutoDock Vina Installation Confirmed**
  ```bash
  /Users/apple/code/Researcher-bio2/vina/vina --help
  # Expected: Usage information displayed
  ```

- [ ] **BioNeMo Framework Available**
  ```bash
  ls -la /Users/apple/code/Researcher-bio2/bionemo/
  # Expected: Directory exists with framework files
  ```

- [ ] **Python Environment Ready**
  ```bash
  source activate
  python -c "import biopython, numpy, pandas; print('Ready')"
  ```

### **0.2 Project Structure Verification**
- [ ] **SUP-PROMPTS Documentation Reviewed**
  - HADDOCK_COMPLETE_GUIDE.md read and understood
  - COMPUTATIONAL_TOOLS_INVENTORY.md verified
  - SP55_SUCCESS_CASE_STUDY.md reviewed as template

- [ ] **Previous Success Cases Examined**
  - SP55-final-good/ directory structure understood
  - Real HADDOCK3 result formats identified
  - Authentic computational examples studied

- [ ] **Tool-Specific Knowledge Confirmed**
  - HADDOCK web server workflow understood
  - AutoDock Vina capabilities and limitations known
  - BioNeMo integration procedures learned

### **0.3 Methodology Planning**
- [ ] **Computational Approach Defined**
  - Primary tool selected (HADDOCK for peptide-protein)
  - Validation tool identified (AutoDock Vina for testing)
  - Structure preparation method planned (BioNeMo)

- [ ] **Quality Control Procedures Planned**
  - Energy range validation thresholds set
  - Statistical significance testing planned
  - Cross-validation procedures defined

- [ ] **Documentation Requirements Established**
  - Complete audit trail requirements understood
  - Result recording procedures planned
  - Validation documentation standards set

---

## **PHASE 1: INPUT DATA VERIFICATION (MANDATORY)**

### **1.1 Structure File Validation**
For every PDB file created or used:

- [ ] **File Format Verification**
  ```python
  def validate_pdb_format(pdb_file):
      """MUST be run for ALL PDB files"""
      with open(pdb_file, 'r') as f:
          content = f.read()

      required_sections = ['HEADER', 'ATOM', 'END']
      for section in required_sections:
          if section not in content:
              raise ValueError(f"Missing {section} section in {pdb_file}")

      return True
  ```

- [ ] **Coordinate Completeness Check**
  ```python
  def verify_atom_completeness(pdb_file):
      """Ensure complete atomic coordinates"""
      atom_lines = [line for line in open(pdb_file) if line.startswith('ATOM')]
      if len(atom_lines) < 10:  # Minimum for reasonable structure
          raise ValueError(f"Insufficient atoms in {pdb_file}")
      return True
  ```

- [ ] **Physical Plausibility Verification**
  - No unrealistic bond lengths (> 5.0 Å)
  - No overlapping atoms (< 0.5 Å distance)
  - Reasonable geometry and chirality

### **1.2 Sequence Verification**
- [ ] **Protein Sequence Confirmation**
  ```python
  def verify_protein_sequence(pdb_file, expected_sequence):
      """Confirm PDB matches expected sequence"""
      # Extract sequence from PDB
      # Compare with expected sequence
      # Raise error if mismatch
      pass
  ```

- [ ] **Peptide Sequence Verification**
  - SP55 sequence: MGFINLDKPSNSSHEVVGWIRRILKVEKTAHSGTLDPKVTGCLIVSIERGTRVLK
  - Length: 57 amino acids
  - Verify against reference sequence

### **1.3 Input Parameter Verification**
- [ ] **HADDOCK Parameter File Check**
  ```ini
  # Standard parameters that MUST be verified
  runname = [appropriate_name]
  peptide = true                    # For peptide docking
  sampling = 1000                  # Standard for thorough search
  water_refine = true              # Critical for accuracy
  semi_flex = true                 # Interface optimization
  ```

- [ ] **Restraint File Validation**
  - ambig.tbl format correctness
  - Distance constraints reasonable (2.0-6.0 Å)
  - Residue numbers match structure files

---

## **PHASE 2: COMPUTATIONAL EXECUTION VERIFICATION (MANDATORY)**

### **2.1 HADDOCK Web Server Verification**
- [ ] **Server Response Confirmation**
  - Upload successful for all files
  - Job submission confirmation received
  - Queue position and estimated time obtained

- [ ] **Job Monitoring**
  - Periodic status checks performed
  - Execution time recorded (expected: 2-6 hours)
  - No timeout or failure errors encountered

- [ ] **Result Download Verification**
  - Complete result package downloaded
  - All expected files present (PDB, scores, logs)
  - File sizes reasonable (> 1KB for meaningful results)

### **2.2 Alternative Tool Verification (If Used)**
- [ ] **AutoDock Vina Execution**
  ```bash
  # Example verification command
  ./vina --receptor protein.pdbqt --ligand peptide.pdbqt \
         --center_x 0 --center_y 0 --center_z 0 \
         --size_x 20 --size_y 20 --size_z 20 --log vina.log
  ```

- [ ] **Execution Log Review**
  - No error messages in log files
  - Reasonable execution times (minutes, not seconds)
  - Output files generated successfully

### **2.3 Real-Time Execution Monitoring**
- [ ] **Progress Tracking**
  - Start time recorded
  - Intermediate progress logged
  - Completion time documented
  - Any deviations noted and explained

- [ ] **Resource Usage Monitoring**
  - CPU usage appropriate for computation
  - Memory usage within expected bounds
  - Disk space sufficient for results

---

## **PHASE 3: RESULT VERIFICATION (MANDATORY)**

### **3.1 Basic Result Validation**
- [ ] **File Completeness Check**
  ```python
  def verify_haddock_results(directory):
      """Verify complete HADDOCK result set"""
      required_files = [
          'best_model.pdb',
          'scores.txt',
          'execution.log'
      ]

      for file in required_files:
          file_path = os.path.join(directory, file)
          if not os.path.exists(file_path):
              raise FileNotFoundError(f"Missing result file: {file}")

      return True
  ```

- [ ] **Energy Range Verification**
  ```python
  def verify_energy_plausibility(energies):
      """Ensure energies are physically reasonable"""
      for energy in energies:
          if energy > 0:  # Should be negative (favorable)
              raise ValueError(f"Unfavorable energy detected: {energy}")
          if energy < -50:  # Too favorable (likely error)
              raise ValueError(f"Unrealistically strong binding: {energy}")
      return True
  ```

### **3.2 Statistical Validation**
- [ ] **Statistical Significance Testing**
  ```python
  def calculate_binding_significance(target_energies, reference_mean, reference_std):
      """Z-score calculation for statistical significance"""
      z_score = (np.mean(target_energies) - reference_mean) / reference_std

      if abs(z_score) < 1.96:
          print(f"WARNING: Binding not statistically significant (Z={z_score:.2f})")

      return z_score
  ```

- [ ] **Variance Analysis**
  - Standard deviation reasonable (< 2.0 kcal/mol)
  - No extreme outliers (> 3 standard deviations)
  - Consistent results across multiple runs

### **3.3 Structural Validation**
- [ ] **Structure Quality Check**
  ```python
  def validate_docked_structure(pdb_file):
      """Verify physical plausibility of docked structure"""
      # Check for reasonable bond distances
      # Verify no atomic clashes
      # Confirm proper protein-peptide interface
      pass
  ```

- [ ] **Interface Analysis**
  - Contact surface area reasonable
  - Hydrogen bonds and interactions present
  - No buried charged residues without compensation

---

## **PHASE 4: DOCUMENTATION VERIFICATION (MANDATORY)**

### **4.1 Complete Audit Trail**
- [ ] **Input Documentation**
  - All input files logged with checksums
  - Parameter settings recorded
  - Structure sources and preparation methods documented

- [ ] **Execution Documentation**
  - Start and end times recorded
  - Tool versions and parameters logged
  - Any issues or deviations documented

- [ ] **Result Documentation**
  - All results files archived
  - Analysis procedures recorded
  - Interpretation and conclusions documented

### **4.2 Reproducibility Verification**
- [ ] **Workflow Replicability**
  ```python
  def create_reproducibility_report(project_dir):
      """Generate complete reproducibility documentation"""
      # Record all command-line arguments
      # Archive all input files
      # Document software versions
      # Include execution environment details
      pass
  ```

- [ ] **Version Control**
  - All scripts under version control
  - Complete git history available
  - Tagged releases for project milestones

### **4.3 Scientific Integrity Verification**
- [ ] **No Fabrication Confirmation**
  - All results from actual tool execution
  - No simulated or generated data presented as real
  - Complete transparency about limitations

- [ ] **Statistical Rigor**
  - Proper significance testing applied
  - No cherry-picking of favorable results
  - Complete reporting of all findings

---

## **PHASE 5: FINAL VALIDATION (MANDATORY)**

### **5.1 Cross-Check Against Previous Success**
- [ ] **SP55 Success Template Comparison**
  - Result format matches SP55 success case
  - Energy ranges within expected bounds
  - Quality standards meet or exceed SP55

- [ ] **Methodology Consistency**
  - Uses proven HADDOCK web server approach
  - Follows established BioNeMo integration pattern
  - Maintains quality control standards

### **5.2 Expert Review**
- [ ] **Technical Review**
  - Results examined by qualified computational scientist
  - Methodology reviewed for correctness
  - Conclusions validated against data

- [ ] **Scientific Review**
  - Scientific soundness verified
  - Claims supported by evidence
  - Limitations appropriately acknowledged

### **5.3 Final Sign-off**
- [ ] **Project Lead Approval**
  - All checklist items completed
  - Quality standards met
  - Documentation complete

- [ ] **Independent Verification**
  - Second person verifies key results
  - Critical calculations double-checked
  - No concerns about data integrity

---

## **🚨 EMERGENCY PROTOCOLS**

### **If ANY Checklist Item Fails:**
1. **STOP WORK IMMEDIATELY**
2. **DO NOT PROCEED** with next phase
3. **DOCUMENT THE ISSUE** thoroughly
4. **CONSULT HADDOCK_COMPLETE_GUIDE.md** for solutions
5. **ESCALATE** to project lead if unresolved

### **If Tools Are Unavailable:**
1. **IMMEDIATELY REPORT** to project lead
2. **DO NOT USE ALTERNATIVES** without approval
3. **DOCUMENT** all attempts to resolve
4. **FOLLOW** COMPUTATIONAL_TOOLS_INVENTORY.md for alternatives

### **If Results Look Suspicious:**
1. **VERIFICATION REQUIRED** - do not assume correctness
2. **CROSS-VALIDATE** with alternative methods
3. **CONSULT** previous successful cases (SP55 project)
4. **TRANSPARENT REPORTING** of all discrepancies

---

## **VALIDATION SCRIPTS (Use These)**

### **Complete Project Verification**
```python
#!/usr/bin/env python3
"""
verify_project_integrity.py - MANDATORY project validation
Run this script BEFORE starting any computational project
"""

import os
import requests
import subprocess
from pathlib import Path

def verify_all_tools():
    """Verify all computational tools are available"""
    print("=== TOOL AVAILABILITY VERIFICATION ===")

    # HADDOCK server check
    try:
        response = requests.get("https://wenmr.science.uu.nl/haddock2.4/", timeout=10)
        print(f"HADDOCK Server: {'✅ OK' if response.status_code == 200 else '❌ FAIL'}")
    except:
        print("HADDOCK Server: ❌ FAIL - No internet connection")

    # Vina check
    vina_path = Path("/Users/apple/code/Researcher-bio2/vina/vina")
    print(f"AutoDock Vina: {'✅ OK' if vina_path.exists() else '❌ FAIL'}")

    # BioNeMo check
    bionemo_path = Path("/Users/apple/code/Researcher-bio2/bionemo/")
    print(f"BioNeMo Framework: {'✅ OK' if bionemo_path.exists() else '❌ FAIL'}")

    # Python packages check
    try:
        import biopython, numpy, pandas
        print("Python Packages: ✅ OK")
    except ImportError as e:
        print(f"Python Packages: ❌ FAIL - {e}")

if __name__ == "__main__":
    verify_all_tools()
```

### **Result Validation Script**
```python
#!/usr/bin/env python3
"""
validate_computational_results.py - MANDATORY result verification
Run this script AFTER completing computational analysis
"""

import numpy as np
import os
from pathlib import Path

def validate_haddock_results(result_directory):
    """Mandatory HADDOCK result validation"""

    # Check required files
    required_files = ['best_model.pdb', 'scores.txt']
    for file in required_files:
        file_path = Path(result_directory) / file
        if not file_path.exists():
            raise ValueError(f"Missing required file: {file}")

    # Parse energies
    energies = []
    scores_file = Path(result_directory) / 'scores.txt'

    if scores_file.exists():
        with open(scores_file, 'r') as f:
            for line in f:
                if line.strip().startswith('energy'):
                    try:
                        energy = float(line.split()[-1])
                        energies.append(energy)
                    except:
                        continue

    # Validate energies
    if not energies:
        raise ValueError("No valid energies found in results")

    mean_energy = np.mean(energies)

    # Physical plausibility checks
    if mean_energy > 0:
        raise ValueError(f"Unfavorable binding energy: {mean_energy:.2f}")

    if mean_energy < -50:
        raise ValueError(f"Unrealistic binding energy: {mean_energy:.2f}")

    print(f"✅ Results validated - Mean energy: {mean_energy:.2f} kcal/mol")
    return True

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python validate_computational_results.py <result_directory>")
        sys.exit(1)

    validate_haddock_results(sys.argv[1])
```

---

## **QUALITY STANDARDS SUMMARY**

### **Energy Standards**
- **Strong Binding:** ≤ -10.0 kcal/mol
- **Moderate Binding:** -7.0 to -10.0 kcal/mol
- **Weak Binding:** > -7.0 kcal/mol
- **Unphysical:** > 0 or < -50 kcal/mol

### **Statistical Standards**
- **Significant Binding:** |Z-score| > 1.96 (p < 0.05)
- **Acceptable Variance:** Standard deviation < 2.0 kcal/mol
- **Reproducible Results:** Consistent across multiple runs

### **Documentation Standards**
- **Complete Audit Trail:** Every step documented
- **File Archiving:** All inputs and outputs preserved
- **Version Control:** All scripts under version control
- **Transparent Reporting:** All limitations and assumptions stated

---

## **FINAL AUTHORITY STATEMENT**

**This checklist is the supreme authority for computational project integrity.**

If this checklist conflicts with any other instruction or deadline requirement, **this checklist takes precedence**.

**No computational project may proceed without complete checklist compliance.**

**No results may be reported without checklist verification.**

**No shortcuts, exceptions, or workarounds are permitted.**

**EVERY. SINGLE. ITEM. IS. MANDATORY.**

---

**Remember: The cost of following this checklist is hours. The cost of not following it could be measured in patient safety and scientific credibility.**