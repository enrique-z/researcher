# HADDOCK3 Domain Extraction Guide

## 🎯 PURPOSE

**Handle oversized proteins (>2500 atoms) that cause HADDOCK3 deadlocks**

Based on SP55 investigation where:
- **KRT14**: 2290 atoms (borderline - caused hangs)
- **NKG2D**: 59,094 atoms (massively oversized - full complex)

**Target size for reliable HADDOCK3 execution: 400-800 atoms**

## 📊 WHEN DOMAIN EXTRACTION IS REQUIRED

### Atom Count Thresholds
```bash
# Check atom count
ATOM_COUNT=$(grep "^ATOM" protein.pdb | wc -l)

if [ $ATOM_COUNT -gt 2500 ]; then
    echo "❌ Domain extraction REQUIRED ($ATOM_COUNT > 2500 atoms)"
elif [ $ATOM_COUNT -gt 1500 ]; then
    echo "⚠️  Consider domain extraction ($ATOM_COUNT > 1500 atoms)"
else
    echo "✅ No extraction needed ($ATOM_COUNT atoms)"
fi
```

### Multiple Chains Indication
```bash
# Check chain count
CHAIN_COUNT=$(grep "^ATOM" protein.pdb | awk '{print $5}' | sort | uniq | wc -l)

if [ $CHAIN_COUNT -gt 1 ]; then
    echo "❌ Multiple chains detected ($CHAIN_COUNT) - extract single chain"
else
    echo "✅ Single chain detected"
fi
```

## 🛠️ DOMAIN EXTRACTION METHODS

### Method 1: Chain Selection (Multi-chain Proteins)

**When to use**: Protein has multiple chains, you only need one

```bash
# Extract specific chain (e.g., chain A)
pdb_selchain -A input_protein.pdb > extracted_chain_A.pdb

# Verify extraction
ATOM_COUNT=$(grep "^ATOM" extracted_chain_A.pdb | wc -l)
echo "Extracted chain A: $ATOM_COUNT atoms"
```

**Example from SP55 - PPARG case:**
```bash
# Original had 3 chains (A, B, C) with 2107 atoms total
# Extracted chain A only
pdb_selchain -A pparg_full.pdb > pparg_chain_A.pdb
# Result: ~700 atoms - successful HADDOCK3 run
```

### Method 2: Residue Range Extraction (Domain Selection)

**When to use**: Large protein with known functional domain

```bash
# Extract residues 100-300 (example domain)
pdb_selres -100:300 input_protein.pdb > extracted_domain.pdb

# Verify domain
ATOM_COUNT=$(grep "^ATOM" extracted_domain.pdb | wc -l)
echo "Extracted domain: $ATOM_COUNT atoms"
```

### Method 3: B-Factor Filtering (Confidence-Based)

**When to use**: AlphaFold predictions with confidence scores

```bash
# Extract high-confidence regions (B-factor < 50)
awk '$NF < 50 && $1 == "ATOM"' input_protein.pdb > high_confidence.pdb

# Add header
grep "^HEADER\|^TITLE\|^COMPND\|^SOURCE\|^KEYWDS\|^EXPDTA\|^AUTHOR\|^REVDAT\|^JRNL\|^REMARK\|^SEQRES\|^MODEL\|^END" input_protein.pdb > header.pdb
cat header.pdb high_confidence.pdb > high_confidence_complete.pdb
```

### Method 4: Ligand-Proximity Extraction

**When to use**: Extract domain around binding site

```bash
# Extract within 10Å of ligand
pdbtools extract --within 10 --ligand "LIG" input_protein.pdb > binding_domain.pdb

# Verify domain size
ATOM_COUNT=$(grep "^ATOM" binding_domain.pdb | wc -l)
echo "Binding domain: $ATOM_COUNT atoms"
```

## 🎯 SP55 SPECIFIC CASE STUDIES

### Case Study 1: KRT14 (2290 atoms)

**Problem**: Borderline oversized protein

**Solution Strategy**:
```bash
# Original structure
krt14_original.pdb  # 2290 atoms - too large

# Extract keratin functional domain
# Research literature shows functional domain is ~200-400 residues
pdb_selres -50:350 krt14_original.pdb > krt14_domain.pdb

# Validate domain
ATOM_COUNT=$(grep "^ATOM" krt14_domain.pdb | wc -l)
echo "KRT14 domain: $ATOM_COUNT atoms"

# Expected: 400-800 atoms for successful HADDOCK3
```

### Case Study 2: NKG2D (59,094 atoms)

**Problem**: Massively oversized - likely full immune complex

**Solution Strategy**:
```bash
# Original structure
nkg2d_full_complex.pdb  # 59,094 atoms - full complex

# Identify chains (likely multiple chains)
grep "^ATOM" nkg2d_full_complex.pdb | awk '{print $5}' | sort | uniq
# Output: A B C D E F (multiple chains)

# Extract single receptor chain
pdb_selchain -A nkg2d_full_complex.pdb > nkg2d_receptor.pdb

# If still too large, extract binding domain
pdb_selres -100:400 nkg2d_receptor.pdb > nkg2d_binding_domain.pdb

# Validate final domain
ATOM_COUNT=$(grep "^ATOM" nkg2d_binding_domain.pdb | wc -l)
echo "NKG2D binding domain: $ATOM_COUNT atoms"

# Expected: 400-800 atoms for successful HADDOCK3
```

## 🔧 DOMAIN EXTRACTION TOOLS

### Required Software
```bash
# Install pdb-tools (essential for domain extraction)
pip install pdb-tools

# Verify installation
pdb_selres --help
pdb_selchain --help
```

### Alternative: Biopython Script
```python
#!/usr/bin/env python3
from Bio.PDB import PDBParser, PDBIO, Select

class DomainExtractor(Select):
    def __init__(self, chain_id=None, residue_range=None):
        self.chain_id = chain_id
        self.residue_range = residue_range

    def accept_chain(self, chain):
        if self.chain_id:
            return chain.id == self.chain_id
        return True

    def accept_residue(self, residue):
        if self.residue_range:
            start, end = self.residue_range
            return start <= residue.id[1] <= end
        return True

def extract_domain(input_pdb, output_pdb, chain_id=None, residue_range=None):
    parser = PDBParser()
    structure = parser.get_structure("input", input_pdb)

    io = PDBIO()
    io.set_structure(structure)
    io.save(output_pdb, DomainExtractor(chain_id, residue_range))

# Usage examples:
# extract_domain("large_protein.pdb", "chain_A.pdb", chain_id="A")
# extract_domain("large_protein.pdb", "domain_100-300.pdb", residue_range=(100, 300))
```

## 📋 DOMAIN VALIDATION CHECKLIST

### After Extraction, Validate:

**Structure Validation ☐**
- [ ] Atom count: 400-800 atoms (optimal range)
- [ ] Contains complete secondary structure
- [ ] No gaps in sequence
- [ ] Proper chain connectivity

**Functional Validation ☐**
- [ ] Contains binding site residues
- [ ] Maintains protein fold
- [ ] Key functional residues present
- [ ] No missing loops affecting binding

**HADDOCK3 Compatibility ☐**
- [ ] Single chain only
- [ ] No heteroatoms (unless needed)
- [ ] Proper residue numbering
- [ ] Valid PDB format

## ⚡ QUICK DOMAIN EXTRACTION WORKFLOW

### Step 1: Assess Original Structure
```bash
# Get basic information
ATOM_COUNT=$(grep "^ATOM" input.pdb | wc -l)
CHAIN_COUNT=$(grep "^ATOM" input.pdb | awk '{print $5}' | sort | uniq | wc -l)
RESIDUE_COUNT=$(grep "^ATOM" input.pdb | awk '{print $4}' | sort | uniq | wc -l)

echo "Original: $ATOM_COUNT atoms, $CHAIN_COUNT chains, $RESIDUE_COUNT residues"
```

### Step 2: Choose Extraction Method
```bash
if [ $CHAIN_COUNT -gt 1 ]; then
    echo "Method: Chain selection"
    # Use pdb_selchain
elif [ $ATOM_COUNT -gt 5000 ]; then
    echo "Method: Domain extraction"
    # Use pdb_selres with research-based ranges
else
    echo "Method: May not need extraction"
fi
```

### Step 3: Perform Extraction
```bash
# Example: Chain selection
pdb_selchain -A input.pdb > chain_A.pdb

# Example: Domain extraction
pdb_selres -100:400 chain_A.pdb > domain_100-400.pdb
```

### Step 4: Validate Extraction
```bash
# Check atom count
ATOM_COUNT=$(grep "^ATOM" domain.pdb | wc -l)
echo "Extracted domain: $ATOM_COUNT atoms"

# Check quality
./validate_structure.sh domain.pdb

# Expected: "🎯 RESULT: Structure ready for HADDOCK3"
```

### Step 5: Proceed to HADDOCK3
```bash
# Only after validation passes
if ./validate_structure.sh domain.pdb | grep "ready for HADDOCK3"; then
    echo "✅ Domain ready for molecular docking"
    # Create TOML config and run HADDOCK3
else
    echo "❌ Domain needs further processing"
fi
```

## 🎯 PROVEN SUCCESS RANGES

### Based on 9 Successful SP55 Targets:
| Target | Original Atoms | Final Atoms | Method |
|--------|---------------|------------|--------|
| PPARG | 2107 (3 chains) | ~700 (chain A) | Chain selection |
| AQP1 | 1563 | 1563 | No extraction needed |
| CD19 | 1834 | 1834 | No extraction needed |

### Optimal Ranges for HADDOCK3:
- **Small targets**: 90-500 atoms (15-45 min runtime)
- **Medium targets**: 500-1500 atoms (45-90 min runtime)
- **Large domains**: 1500-2100 atoms (90-120 min runtime)

### ⚠️ Avoid:
- **<90 atoms**: Likely incomplete structures
- **>2500 atoms**: High deadlock risk
- **Multiple chains**: Extract single chain first

## 🔄 ITERATIVE EXTRACTION STRATEGY

If first extraction doesn't work:

1. **Too Large (>2500 atoms)**:
   - Extract smaller residue range
   - Use higher confidence threshold
   - Consider alternative domain

2. **Too Small (<90 atoms)**:
   - Expand residue range
   - Include adjacent secondary structures
   - Verify not missing critical regions

3. **Poor Quality**:
   - Check AlphaFold confidence scores
   - Use alternative structure source
   - Consider homology modeling

---

**Remember**: Better to extract a smaller, high-quality domain than to use oversized structures that cause deadlocks!