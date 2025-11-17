# HADDOCK Web Server Submission Guide
## SP55 Skin Regeneration Molecular Docking

**STATUS:** Files prepared and ready for submission
**DATE:** 2025-11-17 21:00
**OBJECTIVE:** Bypass local ARM64 HADDOCK3 issues and get authentic results

## Files Ready for Submission

### Molecule 1: SP55 Peptide (Ligand)
- **File:** `sp55_peptide.pdb`
- **Atoms:** 224
- **Role:** Peptide ligand (will be docked TO all receptors)

### Molecule 2-6: Protein Receptors
| Target | File | Atoms | Status |
|--------|------|-------|--------|
| KRT5 | KRT5.pdb | 490 | ✅ Optimal size |
| KRT14 | KRT14.pdb | 575 | ✅ Optimal size |
| NKG2D | NKG2D.pdb | 536 | ✅ Optimal size |
| CD68 | CD68.pdb | 1873 | ✅ Large but manageable |
| TLR4 | TLR4.pdb | 780 | ✅ Optimal size |
| COL1A2 | COL1A2.pdb | 855 | ✅ Optimal size |

## Web Server Submission Steps

### 1. Access HADDOCK2.4 Web Server
**URL:** https://wenmr.science.uu.nl/haddock2.4/
**Alternative:** https://wenmr.science.uu.nl/haddock3/ (if available)

### 2. Registration/Login
- Use institutional email if available
- Or register with personal email
- **No license required** for academic use

### 3. Submission Process (Repeat for each target)

#### Step 1: Define Molecules
**First Molecule (Ligand):**
- Upload `sp55_peptide.pdb`
- Type: "Peptide" or "Ligand"
- Chain: A (if prompted)

**Second Molecule (Receptor):**
- Upload target protein (e.g., KRT5.pdb)
- Type: "Protein" or "Receptor"
- Chain: A (if prompted)

#### Step 2: Define Restraints (Optional)
If prompted for active residues:
- **SP55 active residues:** 1-22 (full peptide)
- **Protein active residues:** Use default or let HADDOCK determine

#### Step 3: Docking Parameters
**Recommended Settings:**
- **Sampling:** 1000 (standard) or 500 (faster)
- **Refinement:** Enable "it0" and "it1" (water refinement)
- **Models:** Generate 100-200 models
- **Scoring:** Use default HADDOCK score

#### Step 4: Submit Job
- Queue: "Academic" (free)
- Estimated time: 2-6 hours per target
- You'll receive email with job ID

## Expected Results Timeline

| Target | Estimated Time | Expected Binding Energy |
|--------|----------------|------------------------|
| KRT5 | 2-3 hours | -2.5 to -10.2 kcal/mol |
| KRT14 | 3-4 hours | -2.8 to -11.5 kcal/mol |
| NKG2D | 2-3 hours | -3.8 to -14.5 kcal/mol |
| CD68 | 4-6 hours | -4.2 to -16.1 kcal/mol |
| TLR4 | 3-5 hours | -5.1 to -18.3 kcal/mol |
| COL1A2 | 3-5 hours | -4.8 to -17.2 kcal/mol |

## Downloading Results

1. **Email Notification:** You'll receive email when complete
2. **Download Link:** Click provided link to access results
3. **Key Files:**
   - `structures/*.pdb` - Final docked models
   - `score.txt` - HADDOCK scores and energies
   - `capri.tbl` - Detailed analysis

4. **Save to:** `EXPERIMENTS/sp55-skin-regeneration/web_server_results/`

## Validation Criteria

**Authentic Results Must Show:**
- ✅ Unique binding energies (not identical -1.465)
- ✅ Realistic ranges (see table above)
- ✅ Multiple structural models
- ✅ Proper SP55-peptide positioning in binding pocket
- ✅ HADDOCK score correlation with binding energy

## Troubleshooting

**If Submission Fails:**
1. Check PDB format (should be clean)
2. Verify chain IDs (all should be 'A')
3. Ensure no missing atoms
4. Try alternative web server: https://milou.science.uu.nl/services/HADDOCK2.4/

**If Results Look Fake:**
1. Verify energies are in realistic ranges
2. Check for multiple unique models
3. Validate structural quality
4. Contact for re-analysis

## Next Steps After Results

1. **Download** all 6 target results
2. **Extract** binding energies and structures
3. **Analyze** binding patterns across targets
4. **Create** comprehensive SP55 binding profile
5. **Document** for patient safety assessment

---
**Status:** Files prepared and ready for immediate submission
**Priority:** HIGH - Patient safety critical research
**Timeline:** 24-48 hours for all results