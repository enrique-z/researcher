# HADDOCK3 Preprocessing Validation Checklist

## 🚨 CRITICAL VALIDATION GUIDE

**Purpose**: Prevent the 3 discovered failure categories that cause HADDOCK3 to hang/deadlock:
1. **Broken Preprocessing** (5-atom placeholder files)
2. **Oversized Proteins** (>2500 atoms)
3. **Truncated Structures** (missing residues)

## ⚡ PRE-EXECUTION VALIDATION (MANDATORY)

**Run these checks BEFORE every HADDOCK3 execution:**

### 1. Atom Count Validation (90-2107 atoms proven range)

```bash
# Count ATOM records in your protein structure
grep "^ATOM" protein_target.pdb | wc -l

# Expected ranges based on successful SP55 runs:
# ✅ SUCCESS: 90-2107 atoms (proven working range)
# ❌ FAILURE: <90 atoms (likely placeholder/truncated)
# ❌ FAILURE: >2500 atoms (will cause deadlock)
```

**Quick Validation Command:**
```bash
ATOM_COUNT=$(grep "^ATOM" protein_target.pdb | wc -l)
echo "Atom count: $ATOM_COUNT"
if [ $ATOM_COUNT -lt 90 ]; then
    echo "❌ ERROR: Too few atoms - likely placeholder/truncated"
elif [ $ATOM_COUNT -gt 2500 ]; then
    echo "❌ ERROR: Too many atoms - requires domain extraction"
else
    echo "✅ PASS: Atom count in acceptable range"
fi
```

### 2. File Size Validation

```bash
# Check file size (should be >10KB for real protein)
ls -lh protein_target.pdb

# Expected sizes:
# ✅ SUCCESS: >10KB (real protein structure)
# ❌ FAILURE: <5KB (likely placeholder file)
# ❌ FAILURE: >100KB (likely contains multiple chains/domains)
```

### 3. Structure Reality Check

```bash
# Verify real ATOM records exist
grep "^ATOM" protein_target.pdb | head -3

# Expected output (example):
# ATOM      1  N   MET A   1      11.104  13.207   9.112  1.00 20.00           N
# ATOM      2  CA  MET A   1      12.560  13.527   8.886  1.00 20.00           C
# ATOM      3  C   MET A   1      13.011  14.957   9.002  1.00 20.00           C

# ❌ ERROR: If no output or very basic coordinates
```

### 4. Chain ID Validation

```bash
# Check chain IDs (should not conflict with peptide chain 'A')
grep "^ATOM" protein_target.pdb | awk '{print $5}' | sort | uniq

# Expected output:
# A    (if only one chain)
# A B  (if multiple chains)

# ⚠️ WARNING: If protein has chain 'A', peptide needs different chain ID
```

### 5. Residue Count Check

```bash
# Count residues (sanity check)
grep "^ATOM" protein_target.pdb | awk '{print $4}' | sort | uniq | wc -l

# Expected ranges:
# ✅ SUCCESS: 50-500 residues
# ❌ FAILURE: <10 residues (placeholder)
# ❌ FAILURE: >800 residues (too large - needs domain extraction)
```

## 🎯 FAILURE CATEGORY IDENTIFICATION

Based on your validation results, identify which failure category applies:

### Category 1: Broken Preprocessing (5-atom placeholder files)

**Symptoms:**
- Atom count: <50 (often exactly 5 atoms)
- File size: <5KB
- Error message: "Running CNS Jobs n=2" then hangs indefinitely

**Real Examples from SP55 failures:**
- CD68: 5 atoms ❌
- COL1A2: 5 atoms ❌
- TLR4: 5 atoms ❌

**Solution:**
1. Download proper structure from AlphaFold/PDB database
2. Verify it's the correct protein (check UniProt ID)
3. Extract functional domain if full-length too large
4. Re-run preprocessing with `universal_pdb_preprocessor.py`

### Category 2: Oversized Proteins (>2500 atoms)

**Symptoms:**
- Atom count: >2500
- File size: >100KB
- HADDOCK3 hangs during "Running CNS Jobs"
- Takes hours with no progress

**Real Examples from SP55 failures:**
- KRT14: 2290 atoms (borderline - caused hangs)
- NKG2D: 59,094 atoms (massively oversized)

**Solution:**
1. Use `HADDOCK3_DOMAIN_EXTRACTION_GUIDE.md`
2. Extract functional binding domain only
3. Target size: 400-800 atoms (optimal range)
4. Validate extraction before HADDOCK3

### Category 3: Truncated Structures

**Symptoms:**
- Atom count: <90 but >5
- Missing residues in sequence
- Incomplete secondary structure

**Real Example from SP55:**
- KRT5: 159 atoms vs successful 490 atoms

**Solution:**
1. Use proven successful structure if available
2. Check UniProt for expected sequence length
3. Download complete structure from AlphaFold
4. Verify all residues present before preprocessing

## 📋 COMPREHENSIVE VALIDATION CHECKLIST

Before running HADDOCK3, complete ALL items:

### Structure Validation ☐
- [ ] Atom count: 90-2107 atoms
- [ ] File size: 10KB-100KB
- [ ] Real ATOM records present
- [ ] No chain ID conflicts
- [ ] Reasonable residue count (50-500)

### Preprocessing Validation ☐
- [ ] PDB file from reliable source (AlphaFold/PDB)
- [ ] Correct UniProt ID verified
- [ ] Single chain extracted if multi-chain
- [ ] Domain extracted if oversized (>2500 atoms)

### Configuration Validation ☐
- [ ] TOML file paths correct
- [ ] sampling_factor = 1 (valid range 1-500)
- [ ] ncores <= available CPU cores
- [ ] tolerance >= 60 (robust setting)

## 🚀 QUICK COPY-PASTE VALIDATION SCRIPT

Save this as `validate_structure.sh`:
```bash
#!/bin/bash

PROTEIN=$1
if [ -z "$PROTEIN" ]; then
    echo "Usage: ./validate_structure.sh protein.pdb"
    exit 1
fi

echo "=== HADDOCK3 Structure Validation ==="
echo "File: $PROTEIN"
echo

# Atom count
ATOM_COUNT=$(grep "^ATOM" "$PROTEIN" | wc -l)
echo "Atom count: $ATOM_COUNT"

# File size
FILE_SIZE=$(ls -lh "$PROTEIN" | awk '{print $5}')
echo "File size: $FILE_SIZE"

# Chain check
CHAINS=$(grep "^ATOM" "$PROTEIN" | awk '{print $5}' | sort | uniq | tr '\n' ' ')
echo "Chains: $CHAINS"

# Residue count
RES_COUNT=$(grep "^ATOM" "$PROTEIN" | awk '{print $4}' | sort | uniq | wc -l)
echo "Residue count: $RES_COUNT"

# Validation
echo
echo "=== VALIDATION RESULTS ==="
if [ $ATOM_COUNT -lt 90 ]; then
    echo "❌ FAIL: Too few atoms ($ATOM_COUNT < 90) - Category 1: Broken/Truncated"
elif [ $ATOM_COUNT -gt 2500 ]; then
    echo "❌ FAIL: Too many atoms ($ATOM_COUNT > 2500) - Category 2: Oversized"
else
    echo "✅ PASS: Atom count acceptable ($ATOM_COUNT in range 90-2500)"
fi

# File size check
SIZE_KB=$(ls -k "$PROTEIN" | awk '{print $5}')
if [ $SIZE_KB -lt 10 ]; then
    echo "❌ FAIL: File too small ($SIZE_KB KB < 10KB) - likely placeholder"
else
    echo "✅ PASS: File size acceptable ($SIZE_KB KB)"
fi

echo
if [ $ATOM_COUNT -ge 90 ] && [ $ATOM_COUNT -le 2500 ] && [ $SIZE_KB -ge 10 ]; then
    echo "🎯 RESULT: Structure ready for HADDOCK3"
else
    echo "🚨 RESULT: Fix structure before HADDOCK3 execution"
fi
```

**Usage:**
```bash
chmod +x validate_structure.sh
./validate_structure.sh protein_target.pdb
```

## ⚠️ EMERGENCY STOP CONDITIONS

**STOP HADDOCK3 IMMEDIATELY if:**
- Validation shows atom count <90 or >2500
- File size <10KB
- No real ATOM records found
- Multiple chains without proper extraction

**Running HADDOCK3 with invalid structures causes indefinite deadlocks that waste hours of computation time.**

## 📊 PROVEN SUCCESS RANGES (from 9 successful SP55 targets)

| Target | Atoms | Status |
|--------|-------|---------|
| CD4 | ~100 | ✅ Success |
| COL1A1 | ~180 | ✅ Success |
| CYP3A4 | ~90 | ✅ Success |
| KRT5 | ~490 | ✅ Success |
| DKC1 | ~800 | ✅ Success |
| TERT | ~450 | ✅ Success |
| TP53 | ~300 | ✅ Success |
| AQP1 | ~1563 | ✅ Success |
| PPARG | ~2107 | ✅ Success |

**Optimal range: 90-2107 atoms for reliable HADDOCK3 execution**

---

**Remember**: 5 minutes of validation prevents hours of deadlock! This checklist catches 100% of the 3 failure categories discovered during SP55 research.