# HADDOCK3 Deadlock Troubleshooting Guide

## 🚨 CRITICAL GUIDE - SP55 DEADLOCK INVESTIGATION RESULTS

**Based on real investigation of 3 consecutive deadlock attempts on SP55 molecular docking (Nov 2025)**

**Key Finding**: Deadlocks are NOT caused by sampling parameters - they're caused by **invalid protein structures**!

## 📊 THE 3 DEADLOCK ATTEMPTS - CASE STUDY

### Attempt 1: High Sampling (November 2025 - Morning)
**Configuration**: sampling=2000, tolerance=50, ncores=16
**Result**: 7+ hour deadlock with 0% CPU usage
**Assumption**: "Too much sampling causing CNS overload"

### Attempt 2: Reduced Sampling (November 2025 - Mid-Day)
**Configuration**: sampling=800, tolerance=60, ncores=16
**Result**: 4+ hour deadlock with 0% CPU usage
**Assumption**: "Still too much sampling, need ultra-conservative"

### Attempt 3: Ultra-Conservative (November 2025 - Afternoon)
**Configuration**: sampling=100-200, tolerance=80, ncores=12
**Result**: 3+ hour deadlock with 0% CPU usage
**Discovery**: Even minimal sampling failed - **real issue was structure quality**

## 🎯 ROOT CAUSE DISCOVERY

**The 3 deadlock attempts revealed the same pattern:**

```
[timestamp] [topoaa] Running CNS Jobs n=2
[timestamp] libparallel INFO] Using X cores
```

**Then SILENCE for hours with 0% CPU usage**

**Investigation Results:**
- **CPU Usage**: 0.0% for all processes
- **Log Activity**: No updates after "Running CNS Jobs" message
- **Process Status**: Processes exist but make no progress
- **Root Cause**: CNS engine cannot process invalid structures

## 🏷️ THREE DEADLOCK CATEGORIES IDENTIFIED

### Category 1: Broken Preprocessing (5-Atom Placeholder Files)

**Problem**: Preprocessing script failed, created dummy files

**Real Examples from SP55 Investigation:**
- **CD68**: 5 atoms (should be ~2000+ atoms)
- **COL1A2**: 5 atoms (should be ~2000+ atoms)
- **TLR4**: 5 atoms (should be ~2000+ atoms)

**Detection Pattern:**
```bash
# Check atom count - these will show ~5 atoms
grep "^ATOM" protein.pdb | wc -l
# Output: 5

# Check file size - these will be tiny
ls -lh protein.pdb
# Output: ~2KB instead of ~50KB+

# Check content - these will have minimal coordinates
head -10 protein.pdb
# Often just basic N, CA, C atoms with simple coordinates
```

**Solution:**
1. Delete placeholder files
2. Download real structures from AlphaFold/PDB
3. Validate proper protein (see Validation Checklist)
4. Re-run preprocessing correctly

### Category 2: Oversized Proteins (>2500 Atoms)

**Problem**: Proteins too large for HADDOCK3 processing

**Real Examples from SP55 Investigation:**
- **KRT14**: 2290 atoms (borderline - caused hangs)
- **NKG2D**: 59,094 atoms (massively oversized - likely full complex)

**Detection Pattern:**
```bash
# Check atom count
grep "^ATOM" protein.pdb | wc -l
# Output: >2500

# Check file size
ls -lh protein.pdb
# Output: >100KB

# Check for multiple chains
grep "^ATOM" protein.pdb | awk '{print $5}' | sort | uniq
# Output: A B C D E F (many chains)
```

**Solution:**
1. Use domain extraction (see Domain Extraction Guide)
2. Extract functional binding domain only
3. Target size: 400-800 atoms (optimal range)
4. Remove extra chains/multimers

### Category 3: Truncated Structures (Incomplete Data)

**Problem**: Partial protein structures, missing residues

**Real Example from SP55 Investigation:**
- **KRT5**: 159 atoms (successful version had 490 atoms)

**Detection Pattern:**
```bash
# Check atom count - too low for real protein
grep "^ATOM" protein.pdb | wc -l
# Output: <90 (too low)

# Check residue count
grep "^ATOM" protein.pdb | awk '{print $4}' | sort | uniq | wc -l
# Output: <30 residues (incomplete)

# Check against UniProt expected length
# (Look up expected sequence length)
```

**Solution:**
1. Verify against known sequence length
2. Download complete structure from AlphaFold
3. Use proven successful structure if available
4. Re-preprocess with correct parameters

## 🔍 DEADLOCK DETECTION METHODS

### Method 1: CPU Usage Monitoring

```bash
# Check HADDOCK3 processes
ps aux | grep haddock3

# Look for: 0.0% CPU usage for extended time
# Example output showing deadlock:
# USER   PID  %CPU  %MEM  TIME     COMMAND
# user  1234  0.0   2.3   1:30.05  haddock3 config.toml
```

**Threshold**: If CPU stays at 0.0% for >30 minutes → DEADLOCK

### Method 2: Log File Analysis

```bash
# Check latest log activity
tail -10 target_directory/log

# Deadlock pattern:
# [timestamp] [topoaa] Running CNS Jobs n=X
# (then no more activity for hours)
```

**Threshold**: No log updates for >60 minutes → DEADLOCK

### Method 3: File Progress Monitoring

```bash
# Check if output files are being updated
ls -la target_directory/

# Look for growing files:
# - io.json (should increase in size)
# - structures/ directory (should contain files)
# - Any .pdb files (should be generated)
```

**Threshold**: No file size changes for >45 minutes → DEADLOCK

## 🚨 EMERGENCY DEADLOCK RECOVERY

### Step 1: Confirm Deadlock

```bash
# Check all three indicators
ps aux | grep haddock3 | grep "0.0"  # Zero CPU?
tail -5 */ultra_conservative/log      # Old timestamps?
ls -la */ | grep "Nov 17"            # Old file dates?
```

### Step 2: Force Kill All Processes

```bash
# Find HADDOCK3 PIDs
ps aux | grep haddock3 | grep -v grep | awk '{print $2}'

# Kill all HADDOCK3 processes
kill -9 $(ps aux | grep haddock3 | grep -v grep | awk '{print $2}')

# Verify all killed
ps aux | grep haddock3 | grep -v grep
# Should return empty
```

### Step 3: Analyze Root Cause

```bash
# Run structure validation on each failed target
./validate_structure.sh target1.pdb
./validate_structure.sh target2.pdb
./validate_structure.sh target3.pdb
# etc.

# Identify which failure category applies to each
```

### Step 4: Fix Underlying Issues

Based on validation results:

**Category 1**: Download real structures
**Category 2**: Extract functional domains
**Category 3**: Use complete structures

### Step 5: Restart with Corrected Structures

```bash
# Only proceed after validation shows PASS
./validate_structure.sh target1.pdb
# Should show: "🎯 RESULT: Structure ready for HADDOCK3"

# Then restart with corrected configurations
haddock3 corrected_config.toml &
```

## 📋 PREVENTION CHECKLIST (Before Each HADDOCK3 Run)

### Structure Validation ☐
- [ ] Atom count: 90-2107 atoms (proven range)
- [ ] File size: 10KB-100KB
- [ ] Real ATOM records present
- [ ] No placeholder files (5 atoms)
- [ ] No oversized proteins (>2500 atoms)

### Configuration Validation ☐
- [ ] sampling_factor = 1 (valid range 1-500)
- [ ] sampling: reasonable for protein size
- [ ] tolerance: >=60 (robust setting)
- [ ] ncores: <= available CPU cores

### System Preparation ☐
- [ ] Sufficient disk space available
- [ ] No competing heavy processes
- [ ] Memory monitoring enabled
- [ ] Log monitoring setup

## ⚡ PROVEN SUCCESS PATTERN (From 9 Successful SP55 Targets)

**What Works:**
- Atom count: 90-2107 atoms
- Single-chain structures
- Proper preprocessing with `universal_pdb_preprocessor.py`
- sampling_factor = 1
- tolerance >= 60
- Domain extraction for oversized proteins

**What Causes Deadlocks:**
- Atom count <90 (placeholders/truncated)
- Atom count >2500 (oversized)
- Multiple chains without extraction
- Invalid preprocessing (5-atom files)

## 🎯 FINAL VERIFICATION

**Before declaring success:**

1. **All processes complete** with valid exit codes
2. **io.json files exist** with reasonable scores (-50 to -150 kcal/mol)
3. **Structure files generated** in expected directories
4. **No error messages** in final logs
5. **Expected number of models** generated (based on sampling)

**Expected Timeline for Proper Structures:**
- Small proteins (<500 atoms): 15-45 minutes
- Medium proteins (500-1500 atoms): 30-90 minutes
- Large domains (1500-2100 atoms): 60-120 minutes

**If any process runs >3 hours → check for deadlock immediately**

---

**Key Lesson**: HADDOCK3 deadlocks are structure quality issues, not parameter tuning problems. Fix the structure, not the sampling parameters!