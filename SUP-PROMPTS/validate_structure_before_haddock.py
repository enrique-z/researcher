#!/usr/bin/env python3
"""
HADDOCK3 Structure Validation Script

Prevents the 3 discovered deadlock categories:
1. Broken Preprocessing (5-atom placeholder files)
2. Oversized Proteins (>2500 atoms)
3. Truncated Structures (<90 atoms)

Usage: python validate_structure_before_haddock.py protein.pdb
"""

import sys
import os
import argparse
from pathlib import Path

def validate_structure(pdb_file):
    """Validate PDB structure for HADDOCK3 compatibility."""

    if not os.path.exists(pdb_file):
        return False, f"File not found: {pdb_file}"

    issues = []
    warnings = []

    # Read PDB file
    try:
        with open(pdb_file, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        return False, f"Error reading file: {e}"

    # Count atoms and residues
    atom_lines = [line for line in lines if line.startswith('ATOM')]
    atom_count = len(atom_lines)

    if atom_count == 0:
        issues.append("No ATOM records found - file may be empty or corrupted")
    elif atom_count < 90:
        issues.append(f"Too few atoms ({atom_count} < 90) - Category 1/3: Broken/Truncated structure")
    elif atom_count > 2500:
        issues.append(f"Too many atoms ({atom_count} > 2500) - Category 2: Oversized protein")

    # Count unique residues
    if atom_lines:
        residues = set()
        for line in atom_lines:
            if len(line) >= 22:
                residue_id = line[17:26].strip()  # Residue number + chain
                residues.add(residue_id)
        residue_count = len(residues)

        if residue_count < 30:
            issues.append(f"Too few residues ({residue_count} < 30) - incomplete structure")

    # Check file size
    file_size_kb = os.path.getsize(pdb_file) / 1024
    if file_size_kb < 10:
        issues.append(f"File too small ({file_size_kb:.1f}KB < 10KB) - likely placeholder")
    elif file_size_kb > 1000:
        warnings.append(f"Large file ({file_size_kb:.1f}KB) - verify not multi-chain complex")

    # Check for real ATOM records
    if atom_lines:
        # Sample first few atoms to verify coordinates
        sample_atoms = atom_lines[:5]
        for atom in sample_atoms:
            if len(atom) < 54:
                issues.append("Invalid ATOM record format - missing coordinates")
                break

            try:
                x = float(atom[30:38].strip())
                y = float(atom[38:46].strip())
                z = float(atom[46:54].strip())
            except ValueError:
                issues.append("Invalid coordinate values in ATOM records")
                break
    else:
        issues.append("No ATOM records to validate")

    # Check for multiple chains
    chains = set()
    for line in atom_lines:
        if len(line) >= 22:
            chain_id = line[21]
            chains.add(chain_id)

    if len(chains) > 1:
        warnings.append(f"Multiple chains detected: {', '.join(sorted(chains))} - extract single chain for HADDOCK3")

    # Overall assessment
    is_valid = len(issues) == 0

    # Build result message
    result_lines = [f"Structure validation for: {pdb_file}"]
    result_lines.append(f"Atoms: {atom_count}")
    if atom_lines:
        result_lines.append(f"Residues: {len(set(line[17:26].strip() for line in atom_lines))}")
    result_lines.append(f"File size: {file_size_kb:.1f}KB")
    result_lines.append(f"Chains: {len(chains)} ({', '.join(sorted(chains))})")
    result_lines.append("")

    if issues:
        result_lines.append("❌ VALIDATION FAILED:")
        for issue in issues:
            result_lines.append(f"   • {issue}")

    if warnings:
        result_lines.append("⚠️  WARNINGS:")
        for warning in warnings:
            result_lines.append(f"   • {warning}")

    if is_valid:
        result_lines.append("")
        result_lines.append("🎯 RESULT: Structure ready for HADDOCK3")

        # Add recommendations
        if atom_count < 200:
            result_lines.append("💡 Tip: Small protein - expect 15-45 minute runtime")
        elif atom_count < 1000:
            result_lines.append("💡 Tip: Medium protein - expect 45-90 minute runtime")
        else:
            result_lines.append("💡 Tip: Large protein - expect 90-120 minute runtime")
    else:
        result_lines.append("")
        result_lines.append("🚨 RESULT: Fix structure before HADDOCK3 execution")

        # Add specific fix recommendations
        if any("atoms (< 90)" in issue for issue in issues):
            result_lines.append("")
            result_lines.append("🔧 Fix for Broken/Truncated structures:")
            result_lines.append("   1. Download proper structure from AlphaFold/PDB")
            result_lines.append("   2. Verify correct UniProt ID")
            result_lines.append("   3. Check for missing residues")

        if any("atoms (> 2500)" in issue for issue in issues):
            result_lines.append("")
            result_lines.append("🔧 Fix for Oversized proteins:")
            result_lines.append("   1. Extract functional domain (400-800 atoms)")
            result_lines.append("   2. Use domain extraction guide: HADDOCK3_DOMAIN_EXTRACTION_GUIDE.md")
            result_lines.append("   3. Research literature for binding domain boundaries")

        if any("File too small" in issue for issue in issues):
            result_lines.append("")
            result_lines.append("🔧 Fix for Placeholder files:")
            result_lines.append("   1. Delete placeholder file")
            result_lines.append("   2. Download real protein structure")
            result_lines.append("   3. Validate proper protein (not DNA/RNA/ligand)")

    result_message = "\n".join(result_lines)

    return is_valid, result_message

def main():
    parser = argparse.ArgumentParser(description="Validate PDB structure for HADDOCK3 compatibility")
    parser.add_argument("pdb_file", help="PDB file to validate")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    is_valid, message = validate_structure(args.pdb_file)

    print(message)

    if not is_valid:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()