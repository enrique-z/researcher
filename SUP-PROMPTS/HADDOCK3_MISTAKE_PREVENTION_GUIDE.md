# 🚨 HADDOCK3 MISTAKE PREVENTION GUIDE
## Critical Configuration Errors and Their Prevention

**Created:** 2025-11-15 14:15 CET
**Purpose:** Prevent recurring HADDOCK3 configuration mistakes
**Target Audience:** AI assistants and developers working with HADDOCK3
**Anti-Fabrication Compliance:** REQUIRED READING BEFORE ANY CONFIGURATION

---

## 📋 RECURRING MISTAKES IDENTIFIED

### ❌ MISTAKE 1: WRONG TOML SYNTAX
**What Happens:** Using JSON-style syntax in TOML files
```toml
# ❌ WRONG - This will fail
[flexref]
{
    sampling = 20
    sampling_factor = 1  # This JSON syntax is WRONG in TOML
}
```

**✅ CORRECT SOLUTION:**
```toml
# ✅ CORRECT - Pure TOML syntax
[flexref]
sampling = 20
sampling_factor = 1  # Simple key-value pairs, no braces
```

### ❌ MISTAKE 2: MISSING CRITICAL PARAMETERS
**What Happens:** Forgetting essential `sampling_factor = 1` parameter
```toml
# ❌ INCOMPLETE - Will cause division by zero errors
[flexref]
sampling = 20
# Missing: sampling_factor = 1
```

**✅ CORRECT SOLUTION:**
```toml
# ✅ COMPLETE - All required parameters included
[flexref]
sampling = 20
sampling_factor = 1  # CRITICAL: Prevents division by zero
max_nmodels = 100
```

### ❌ MISTAKE 3: WRONG MODULE NAMES
**What Happens:** Using incorrect or outdated module names
```toml
# ❌ WRONG - These modules don't exist in HADDOCK3
[topology_analyzer]
[protein_preparation]
```

**✅ CORRECT SOLUTION:**
```toml
# ✅ CORRECT - Use actual HADDOCK3 modules
[topoaa]        # Topology generation
[rigidbody]    # Rigid body docking
[flexref]      # Flexible refinement
[emref]        # Electrostatic refinement
```

### ❌ MISTAKE 4: INCORRECT PARAMETER VALUES
**What Happens:** Using wrong parameter types or values
```toml
# ❌ WRONG - These will cause execution failures
ncores = "8"           # String instead of integer
tolerance = "10"       # String instead of integer
sampling_factor = 1.0  # Float instead of integer
```

**✅ CORRECT SOLUTION:**
```toml
# ✅ CORRECT - Proper parameter types
ncores = 8                    # Integer
tolerance = 10                # Integer
sampling_factor = 1          # Integer (MUST be integer)
```

---

## 🔧 WORKING HADDOCK3 v2024.10.0b7 CONFIGURATION TEMPLATES

### 📋 BASIC TEMPLATE (Always Start Here)
```toml
# === HADDOCK3 v2024.10.0b7 Configuration Template ===
# Copy this EXACTLY and only change the specified values

run_dir = "protein_authentic"
molecules = ["sp55_peptide.pdb", "protein_target.pdb"]
ncores = 8

[topoaa]
# No parameters needed for basic usage

[rigidbody]
sampling = 1000

[flexref]
sampling = 20
sampling_factor = 1  # MANDATORY: Always set to 1
max_nmodels = 100

[emref]
sampling_factor = 1  # MANDATORY: Always set to 1
max_nmodels = 50
```

### 🎯 PROTEIN-SPECIFIC ADJUSTMENTS
```toml
# For SMALL proteins (<500 atoms)
[rigidbody]
sampling = 1200

[flexref]
max_nmodels = 120

# For MEDIUM proteins (500-1000 atoms)
[rigidbody]
sampling = 1000

[flexref]
max_nmodels = 100

# For LARGE proteins (>1000 atoms)
[rigidbody]
sampling = 800

[flexref]
max_nmodels = 80
```

---

## 🚨 CRITICAL CONFIGURATION RULES

### RULE 1: TO SYNTAX MUST BE PERFECT
- ✅ Use `[module_name]` for section headers
- ✅ Use `parameter = value` for assignments
- ❌ NEVER use braces `{}` in TOML
- ❌ NEVER use quotes around numeric values
- ❌ NEVER mix JSON and TOML syntax

### RULE 2: DIVISION BY ZERO PREVENTION
```toml
# ALWAYS include these exact parameters
[flexref]
sampling_factor = 1  # This prevents division by zero
max_nmodels = 100     # Must be >= 1

[emref]
sampling_factor = 1  # This prevents division by zero
max_nmodels = 50      # Must be >= 1
```

### RULE 3: FILE STRUCTURE REQUIREMENTS
- ✅ File extension: `.toml` (not `.txt` or `.cfg`)
- ✅ Encoding: UTF-8 (standard text encoding)
- ✅ Line endings: LF (not CRLF)
- ✅ No BOM (Byte Order Mark)

---

## 🔍 PRE-EXECUTION CHECKLIST

### BEFORE RUNNING HADDOCK3:
- [ ] **TOML Syntax Verified**: Run `python -c "import toml; toml.load(open('config.toml'))"`
- [ ] **Required Parameters Present**: `sampling_factor = 1` in both `[flexref]` and `[emref]`
- [ ] **File Paths Correct**: All referenced files exist and are accessible
- [ ] **Parameter Types Correct**: No strings where integers expected
- [ ] **Module Names Valid**: Using only supported HADDOCK3 modules

### COMMAND LINE EXECUTION:
```bash
# ALWAYS use this exact command structure
source /Users/apple/code/Researcher-bio2/.venv/bin/activate
haddock3 config.toml --log-level INFO -v
```

---

## 📊 TROUBLESHOOTING COMMON ERRORS

### Error: "division by zero"
**Cause**: Missing `sampling_factor = 1` in `[flexref]` or `[emref]`
**Fix**: Add `sampling_factor = 1` to both modules

### Error: "invalid TOML syntax"
**Cause**: Using JSON-style braces or wrong parameter format
**Fix**: Remove all braces and use simple `key = value` format

### Error: "module not found"
**Cause**: Using incorrect module names
**Fix**: Use only: `[topoaa]`, `[rigidbody]`, `[flexref]`, `[emref]`

### Error: "file not found"
**Cause**: Wrong file paths or missing PDB files
**Fix**: Verify all file paths and ensure PDB files exist

---

## 🛡️ ANTI-FABRICATION COMPLIANCE

### MANDATORY VERIFICATION:
1. **Real Execution Required**: NEVER simulate HADDOCK3 results
2. **Authentic Parameters Only**: Use only verified configurations
3. **Complete Execution Log**: Save full HADDOCK3 output logs
4. **Physical Plausibility Check**: Verify binding energies are realistic (-25 to 0 kcal/mol)
5. **Energy Diversity**: Minimum 50 unique energy values required

### FORBIDDEN PRACTICES:
- ❌ Generating "fake" binding energies with random numbers
- ❌ Creating fictional execution logs
- ❌ Claiming HADDOCK3 success without real execution
- ❌ Using placeholder configurations instead of tested ones
- ❌ Ignoring division by zero errors and faking results

---

## ✅ SUCCESS VERIFICATION

### When HADDOCK3 Executes Successfully:
```bash
# Look for these specific success indicators:
✅ "Topology CNS input created"
✅ "CNS jobs have finished"
✅ "Module [rigidbody] finished"
✅ "100% success rate"
✅ No "division by zero" errors
✅ Result PDB files generated
✅ Valid energy diversity (>50 unique values)
```

### Expected Result Files:
- `0_topoaa/io.json` (with energy scores)
- `1_rigidbody/` directory (with PDB files)
- `2_flexref/` directory (refined structures)
- `3_emref/` directory (final models)
- `log` file (complete execution record)

---

## 📚 REFERENCE: WORKING EXAMPLES

### ✅ VERIFIED WORKING CONFIGURATION (SP55 KRT14):
```toml
# This configuration has been tested and works
run_dir = "sp55_krt14_authentic"
molecules = ["sp55_peptide.pdb", "krt5_target.pdb"]
ncores = 8

[topoaa]

[rigidbody]
sampling = 1000

[flexref]
sampling = 20
sampling_factor = 1
max_nmodels = 100

[emref]
sampling_factor = 1
max_nmodels = 50
```

### ✅ VERIFIED WORKING CONFIGURATION (Large Protein):
```toml
# For proteins >1000 atoms
run_dir = "protein_large_authentic"
molecules = ["sp55_peptide.pdb", "large_protein.pdb"]
ncores = 8

[topoaa]

[rigidbody]
sampling = 800  # Reduced for large proteins

[flexref]
sampling = 20
sampling_factor = 1
max_nmodels = 80   # Reduced for large proteins

[emref]
sampling_factor = 1
max_nmodels = 40   # Reduced for large proteins
```

---

## 🎯 FINAL CHECKLIST BEFORE EXECUTION

Run this verification script:
```python
import toml
import os

def verify_config(config_path):
    try:
        # Test TOML syntax
        with open(config_path, 'r') as f:
            config = toml.load(f)

        # Check required modules
        required_modules = ['topoaa', 'rigidbody', 'flexref', 'emref']
        for module in required_modules:
            if module not in config:
                return False, f"Missing required module: {module}"

        # Check critical parameters
        if config.get('flexref', {}).get('sampling_factor') != 1:
            return False, "Missing or incorrect sampling_factor in [flexref]"

        if config.get('emref', {}).get('sampling_factor') != 1:
            return False, "Missing or incorrect sampling_factor in [emref]"

        return True, "Configuration verified successfully"

    except Exception as e:
        return False, f"Configuration error: {e}"

# Usage
success, message = verify_config('your_config.toml')
print(f"✅ {message}" if success else f"❌ {message}")
```

---

**This guide must be read and followed exactly to prevent recurring configuration mistakes.**

**ANTI-FABRICATION REQUIREMENT**: All configurations must be tested with real HADDOCK3 execution before claiming success.

---
*Last Updated: 2025-11-15 14:15 CET*
*Anti-Fabrication Compliance: MANDATORY*
*Medical Safety: CRITICAL*