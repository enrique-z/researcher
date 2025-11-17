# HADDOCK3 MANDATORY PREPROCESSING CHECKLIST

## ⚠️ CRITICAL WARNING: RUN THIS BEFORE ANY HADDOCK3 EXECUTION

**FAILURE TO PREPROCESS WILL RESULT IN DIVISION BY ZERO ERRORS AND WASTED COMPUTATIONAL TIME**

**Based on real SP55 experiment: 4/11 targets (36.4%) failed due to missing preprocessing**

---

## MANDATORY PREPROCESSING WORKFLOW

### Step 0: STRUCTURE VALIDATION (NEW - MANDATORY)

**🚨 CRITICAL ADDITION: Validate structures BEFORE preprocessing to prevent 3 deadlock categories**

**Based on SP55 deadlock investigation - prevents hours of wasted computation time:**

**✅ Atom Count Validation (90-2107 atoms proven range):**
```bash
# Check atom count - this identifies 3 failure categories
for file in *.pdb; do
  atoms=$(grep "^ATOM" "$file" | wc -l)
  echo "=== $file ==="
  echo "Atoms: $atoms"

  if [ $atoms -lt 90 ]; then
    echo "❌ Category 1/3: Broken/Truncated structure ($atoms < 90)"
  elif [ $atoms -gt 2500 ]; then
    echo "❌ Category 2: Oversized protein ($atoms > 2500) - needs domain extraction"
  else
    echo "✅ PASS: Atom count in acceptable range (90-2500)"
  fi
  echo ""
done
```

**✅ File Size Reality Check:**
```bash
# Real proteins should be >10KB
for file in *.pdb; do
  size_kb=$(ls -k "$file" | awk '{print $5}')
  echo "$file: ${size_kb}KB"

  if [ $size_kb -lt 10 ]; then
    echo "❌ Category 1: Likely placeholder file (${size_kb}KB < 10KB)"
  else
    echo "✅ PASS: Reasonable file size"
  fi
done
```

**✅ Structure Reality Verification:**
```bash
# Verify real ATOM records exist (not just headers)
for file in *.pdb; do
  real_atoms=$(grep "^ATOM" "$file" | head -1)
  if [[ -z "$real_atoms" ]]; then
    echo "❌ $file: No ATOM records found"
  else
    echo "✅ $file: Contains real protein structure"
  fi
done
```

**📋 Use the New Validation Tools:**
```bash
# Comprehensive validation script
/Users/apple/code/Researcher-bio2/SUP-PROMPTS/validate_structure_before_haddock.py your_protein.pdb

# Or use the detailed checklist
cat /Users/apple/code/Researcher-bio2/SUP-PROMPTS/HADDOCK3_PREPROCESSING_VALIDATION_CHECKLIST.md
```

**⚠️ STOP PREPROCESSING IF ANY VALIDATION FAILS**
- Fix Category 1: Download real structures (5-atom placeholders)
- Fix Category 2: Extract domains (>2500 atoms)
- Fix Category 3: Use complete structures (<90 atoms)

**✅ Check PDB File Status:**
```bash
# Verify you have clean PDB files
ls -la *.pdb
# Check for multiple chains (common failure point)
grep "^ATOM" your_protein.pdb | head -5
```

**✅ Verify Preprocessing Tool Available:**
```bash
# Check universal_pdb_preprocessor.py exists
ls -la /Users/apple/code/Researcher-bio2/universal_pdb_preprocessor.py
python -c "import sys; print(sys.version)"
```

**✅ Backup Original Files:**
```bash
mkdir -p backup_original_pdbs
cp *.pdb backup_original_pdbs/
```

---

### Step 1: IDENTIFY MULTI-CHAIN PROTEINS (CRITICAL)

**Multi-chain proteins caused PPARG failure - handle with care:**

```bash
# Check chain count in your protein
grep "^ATOM" PPARG.pdb | cut -c 22 | sort | uniq -c

# Expected output for multi-chain:
#   1563 A  (Chain A has 1563 atoms)
#    456 B  (Chain B has 456 atoms)
#    234 C  (Chain C has 234 atoms)

# If multiple chains exist, you MUST extract chains individually
```

**🚨 MULTI-CHAIN HANDLING (PPARG Lesson Learned):**
```bash
# Extract single chain for HADDOCK3 (usually Chain A)
pdb_selchain -A PPARG.pdb > PPARG_chainA.pdb

# Verify extraction worked
grep "^ATOM" PPARG_chainA.pdb | wc -l
# Should show reasonable atom count (~1500-2500 for typical proteins)
```

---

### Step 2: RUN UNIVERSAL PREPROCESSOR (MANDATORY)

**Execute preprocessing on ALL PDB files:**

```bash
# Run preprocessor on each target
python /Users/apple/code/Researcher-bio2/universal_pdb_preprocessor.py \
  --input PPARG_chainA.pdb \
  --output PPARG_preprocessed.pdb \
  --verbose

python /Users/apple/code/Researcher-bio2/universal_pdb_preprocessor.py \
  --input AQP1.pdb \
  --output AQP1_preprocessed.pdb \
  --verbose

python /Users/apple/code/Researcher-bio2/universal_pdb_preprocessor.py \
  --input CD19.pdb \
  --output CD19_preprocessed.pdb \
  --verbose

python /Users/apple/code/Researcher-bio2/universal_pdb_preprocessor.py \
  --input CD3E.pdb \
  --output CD3E_preprocessed.pdb \
  --verbose
```

**Expected Success Indicators:**
- `PDB file successfully preprocessed for CNS compatibility`
- `Number of atoms: XXXX`
- `Number of residues: YYY`
- `No chain breaks detected`

---

### Step 3: VALIDATE PREPROCESSED FILES

**Critical validation before HADDOCK3:**

```bash
# Check file sizes (should be > 10KB for real proteins)
ls -lh *_preprocessed.pdb

# Verify atom counts are reasonable
for file in *_preprocessed.pdb; do
  echo "=== $file ==="
  grep "^ATOM" "$file" | wc -l
  echo "Atoms: $(grep "^ATOM" "$file" | wc -l)"
  echo "Residues: $(grep "^ATOM" "$file" | cut -c 23 - | uniq | wc -l)"
  echo ""
done

# Verify no missing residues in critical regions
# (Look for gaps > 4 residues)
```

**🚨 RED FLAGS - STOP IF YOU SEE:**
- File size < 5KB (likely failed preprocessing)
- Atom count < 500 (too small for real protein)
- Error messages about missing atoms/chains

---

### Step 4: UPDATE HADDOCK3 CONFIGURATION PATHS

**CRITICAL: Use preprocessed file paths in TOML:**

```toml
# BEFORE (WRONG - causes division by zero):
[topoaa]
molecules = ["PPARG.pdb"]  # ❌ Raw PDB - WILL FAIL

# AFTER (CORRECT - works reliably):
[topoaa]
molecules = ["PPARG_preprocessed.pdb"]  # ✅ Preprocessed - SUCCESS
```

**Complete working configuration example:**
```toml
[tolerance] = 50

[topoaa]
molecules = ["PPARG_preprocessed.pdb"]

[rigidbody]
sampling_factor = 1000

[flexref]
sampling_factor = 1  # CRITICAL: Missing this causes division by zero

[emref]
sampling_factor = 1  # CRITICAL: Missing this causes division by zero

[mdref]
...
```

---

## COMMON ERROR MESSAGES & SOLUTIONS

### Error: "division by zero" in flexref/emref
**Cause**: Missing `sampling_factor = 1` parameter
**Solution**: Add `sampling_factor = 1` to both `[flexref]` and `[emref]` sections

### Error: "No models selected for docking"
**Cause**: PDB file not preprocessed or empty models_to_dock list
**Solution**: Run universal_pdb_preprocessor.py and verify output files

### Error: "CNS topology generation failed"
**Cause**: Non-standard residues or chain breaks in PDB
**Solution**: Check preprocessing logs for warnings, consider alternative chain

### Error: "Unexpected token in PDB file"
**Cause**: Unicode characters or formatting issues
**Solution**: Ensure clean ASCII PDB files, run preprocessing tool

---

## ANTI-FABRICATION VERIFICATION CHECKLIST

**Before running HADDOCK3, verify:**

- [ ] All PDB files exist and are > 5KB
- [ ] Preprocessing completed without errors
- [ ] Atom counts are reasonable (500-5000 atoms typical)
- [ ] Multi-chain proteins properly extracted
- [ ] Configuration uses preprocessed file paths
- [ ] `sampling_factor = 1` added to flexref and emref
- [ ] `tolerance = 50` set in topoaa section
- [ ] Backup of original files created
- [ ] All steps documented for traceability

**Remember: Patient safety depends on authentic results. No shortcuts allowed.**

---

## SP55 LESSONS LEARNED (Case Study)

### What Went Wrong:
1. **PPARG**: 3 chains (A, B, C) not extracted → models_to_dock empty → division by zero
2. **AQP1**: 50% CNS topology failure → no valid structures for docking
3. **CD19/CD3E**: Likely similar preprocessing issues
4. **Missing Parameter**: `sampling_factor = 1` absent from flexref/emref

### What Should Have Happened:
1. **Preprocessing First**: Run universal_pdb_preprocessor.py on ALL targets
2. **Chain Extraction**: Extract PPARG chain A before preprocessing
3. **Configuration Update**: Use preprocessed file paths in TOML
4. **Parameter Addition**: Include sampling_factor in all sampling modules

### Result of Skipping Preprocessing:
- **Wasted Time**: 8-32 hours of failed computations
- **Data Gaps**: 36.4% missing binding energies
- **Safety Concerns**: Incomplete toxicology assessment
- **Cost Impact**: Delayed clinical development timeline

---

## QUICK VERIFICATION COMMANDS

**Run this before starting HADDOCK3:**
```bash
#!/bin/bash
# Quick preprocessing verification
echo "=== Preprocessing Verification ==="

# Check preprocessed files exist
for target in PPARG AQP1 CD19 CD3E; do
  if [[ -f "${target}_preprocessed.pdb" ]]; then
    atoms=$(grep "^ATOM" "${target}_preprocessed.pdb" | wc -l)
    size=$(ls -lh "${target}_preprocessed.pdb" | awk '{print $5}')
    echo "✅ $target: $atoms atoms, $size"
  else
    echo "❌ $target: MISSING preprocessed file"
  fi
done

echo "=== Verification Complete ==="
```

**Expected output:**
```
=== Preprocessing Verification ===
✅ PPARG: 2107 atoms, 145K
✅ AQP1: 1563 atoms, 98K
✅ CD19: 1834 atoms, 121K
✅ CD3E: 1678 atoms, 109K
=== Verification Complete ===
```

---

## 📞 EMERGENCY CONTACT

If preprocessing fails and you cannot resolve:
1. Check the preprocessing tool logs for specific error messages
2. Verify PDB file integrity and chain structure
3. Consider alternative chain selection for multi-chain proteins
4. Document all attempts for troubleshooting purposes

**Remember: 30 minutes of preprocessing prevents 8+ hours of failed computations.**

---

*This checklist was created based on real SP55 experimental failures to prevent future researchers from making the same mistakes. Follow exactly - patient safety depends on authentic computational results.*