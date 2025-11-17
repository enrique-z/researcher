#!/usr/bin/env python3
"""
Universal PDB Preprocessor for CNS/HADDOCK Compatibility
Eliminates duplicate residue errors for ANY number of proteins

Author: Claude Code
Date: 2025-11-12
Updated: 2025-11-15 - Enhanced with SP55 failure analysis
Purpose: Permanent solution for CNS "SEGMNT-ERR: attempt to enter duplicate residue" errors
         Critical for HADDOCK3 success - 36.4% failure rate without preprocessing (SP55 data)

Usage: python universal_pdb_preprocessor.py input.pdb output.pdb
       python universal_pdb_preprocessor.py --input input.pdb --output output.pdb --verbose
       python universal_pdb_preprocessor.py --validate input.pdb
"""

import sys
import os
import subprocess
import tempfile
from pathlib import Path
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class UniversalPDBPreprocessor:
    """Universal PDB preprocessing pipeline for CNS/HADDOCK compatibility"""

    def __init__(self, verbose=False):
        self.temp_dir = tempfile.mkdtemp(prefix="pdb_preprocess_")
        self.verbose = verbose
        logger.info(f"Created temporary directory: {self.temp_dir}")
        if self.verbose:
            logger.setLevel(logging.DEBUG)
            print("🔬 PDB Preprocessor initialized in VERBOSE mode")
            print(f"📁 Temporary directory: {self.temp_dir}")

    def cleanup(self):
        """Clean up temporary files"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        logger.info(f"Cleaned up temporary directory: {self.temp_dir}")

    def analyze_pdb_structure(self, input_file):
        """
        Detailed PDB structure analysis (SP55 enhancement)
        Returns comprehensive information about the PDB file
        """
        if self.verbose:
            print(f"\n🔍 Analyzing PDB structure: {input_file}")

        analysis = {
            'file_size': os.path.getsize(input_file),
            'atoms': 0,
            'hetatm': 0,
            'residues': set(),
            'chains': set(),
            'chain_atom_counts': {},
            'duplicate_residues': [],
            'multi_chain': False,
            'has_ligands': False,
            'has_waters': False,
            'has_ter_records': False,
            'residue_ranges': {},
            'potential_issues': []
        }

        with open(input_file, 'r') as f:
            lines = f.readlines()

        # Analyze each line
        for line in lines:
            if line.startswith('ATOM'):
                analysis['atoms'] += 1
                chain_id = line[21].strip()
                res_num = line[22:26].strip()
                res_name = line[17:20].strip()

                # Track chains
                if chain_id:
                    analysis['chains'].add(chain_id)
                    analysis['chain_atom_counts'][chain_id] = analysis['chain_atom_counts'].get(chain_id, 0) + 1

                    # Track residue ranges per chain
                    if chain_id not in analysis['residue_ranges']:
                        analysis['residue_ranges'][chain_id] = {'min': 999999, 'max': -1}
                    try:
                        res_int = int(res_num)
                        analysis['residue_ranges'][chain_id]['min'] = min(analysis['residue_ranges'][chain_id]['min'], res_int)
                        analysis['residue_ranges'][chain_id]['max'] = max(analysis['residue_ranges'][chain_id]['max'], res_int)
                    except ValueError:
                        pass

                # Track residues (for duplicate detection)
                if chain_id and res_num:
                    res_key = (chain_id, res_num, res_name)
                    analysis['residues'].add(res_key)

            elif line.startswith('HETATM'):
                analysis['hetatm'] += 1
                res_name = line[17:20].strip()
                if res_name == 'HOH':
                    analysis['has_waters'] = True
                else:
                    analysis['has_ligands'] = True

            elif line.startswith('TER'):
                analysis['has_ter_records'] = True

        # Check for multi-chain (critical for SP55 PPARG case)
        analysis['multi_chain'] = len(analysis['chains']) > 1

        # Estimate residue count
        analysis['estimated_residues'] = len(analysis['residues'])

        # Identify potential issues
        if analysis['multi_chain'] and not analysis['has_ter_records']:
            analysis['potential_issues'].append("Multi-chain protein without TER records - HADDOCK3 may fail")

        if analysis['estimated_residues'] > 10000:
            analysis['potential_issues'].append(f"Large protein ({analysis['estimated_residues']} residues) - CNS limit is 10,000")

        if analysis['file_size'] < 5000:
            analysis['potential_issues'].append(f"Small file size ({analysis['file_size']} bytes) - may be incomplete")

        # Verbose output
        if self.verbose:
            print(f"📊 PDB Analysis Results:")
            print(f"   File size: {analysis['file_size']:,} bytes")
            print(f"   Atoms: {analysis['atoms']:,}")
            print(f"   HETATM: {analysis['hetatm']:,}")
            print(f"   Estimated residues: {analysis['estimated_residues']:,}")
            print(f"   Chains: {sorted(analysis['chains'])} ({'MULTI-CHAIN ⚠️' if analysis['multi_chain'] else 'Single chain'})")

            for chain in sorted(analysis['chains']):
                count = analysis['chain_atom_counts'][chain]
                if chain in analysis['residue_ranges']:
                    res_range = f"{analysis['residue_ranges'][chain]['min']}-{analysis['residue_ranges'][chain]['max']}"
                else:
                    res_range = "Unknown"
                print(f"     Chain {chain}: {count:,} atoms, residues {res_range}")

            print(f"   Waters: {'Yes' if analysis['has_waters'] else 'No'}")
            print(f"   Other ligands: {'Yes' if analysis['has_ligands'] else 'No'}")
            print(f"   TER records: {'Yes' if analysis['has_ter_records'] else 'No'}")

            if analysis['potential_issues']:
                print(f"   ⚠️  Potential issues:")
                for issue in analysis['potential_issues']:
                    print(f"      - {issue}")
            else:
                print(f"   ✅ No obvious issues detected")

        return analysis

    def validate_pdb_exists(self, input_file):
        """Validate input PDB file exists and is readable"""
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"Input PDB file not found: {input_file}")

        if os.path.getsize(input_file) == 0:
            raise ValueError(f"Input PDB file is empty: {input_file}")

        # Enhanced validation with structure analysis
        analysis = self.analyze_pdb_structure(input_file)

        # Check if it's a valid PDB file
        if analysis['atoms'] == 0 and analysis['hetatm'] == 0:
            raise ValueError(f"File does not contain any ATOM or HETATM records: {input_file}")

        if self.verbose:
            print(f"✅ PDB file validation passed: {input_file}")

        return analysis

    def run_pdb_tool(self, cmd, input_file, output_file):
        """Run a pdb-tools command with error handling"""
        try:
            full_cmd = f"{cmd} {input_file} > {output_file}"
            logger.info(f"Running: {full_cmd}")
            result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True, check=True)
            return output_file
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {full_cmd}")
            logger.error(f"Error output: {e.stderr}")
            raise RuntimeError(f"PDB tool command failed: {e}")

    def preprocess_pdb(self, input_pdb, output_pdb, keep_ligands=None, keep_waters=False):
        """
        Universal PDB preprocessing pipeline

        Args:
            input_pdb: Path to input PDB file
            output_pdb: Path to output cleaned PDB file
            keep_ligands: List of ligand names to preserve (optional)
            keep_waters: Whether to keep water molecules (default: False)
        """
        if self.verbose:
            print(f"\n🚀 Starting PDB preprocessing pipeline")
            print(f"📁 Input: {input_pdb}")
            print(f"📁 Output: {output_pdb}")

        logger.info(f"Processing PDB file: {input_pdb} -> {output_pdb}")

        # Enhanced validation with structure analysis
        analysis = self.validate_pdb_exists(input_pdb)

        # Create temporary working files
        current_file = input_pdb
        step = 1

        try:
            # SP55 WARNING: Check for multi-chain situation like PPARG
            if analysis['multi_chain']:
                if self.verbose:
                    print(f"⚠️  SP55 ALERT: Multi-chain protein detected!")
                    print(f"   Chains: {sorted(analysis['chains'])}")
                    print(f"   Recommendation: Extract single chain before HADDOCK3")
                    print(f"   Example: pdb_selchain -A {input_pdb} > {input_pdb.replace('.pdb', '_chainA.pdb')}")
                logger.warning(f"Multi-chain protein detected ({len(analysis['chains'])} chains). SP55 failed on PPARG without chain extraction.")

            # Step 1: Standardize PDB format and add basic TER records
            temp_file1 = os.path.join(self.temp_dir, f"step1_{os.path.basename(input_pdb)}")
            if self.verbose:
                print(f"\n📋 Step {step}: Standardizing PDB format with strict tidying")
            self.run_pdb_tool("pdb_tidy -strict", current_file, temp_file1)
            current_file = temp_file1
            logger.info(f"Step {step}: Standardized PDB format with strict tidying")
            if self.verbose:
                print(f"   ✅ PDB format standardized")
            step += 1

            # Step 2: Handle alternate conformations (keep highest occupancy)
            temp_file2 = os.path.join(self.temp_dir, f"step2_{os.path.basename(input_pdb)}")
            if self.verbose:
                print(f"\n📋 Step {step}: Removing alternate conformations")
            self.run_pdb_tool("pdb_selaltloc", current_file, temp_file2)
            current_file = temp_file2
            logger.info(f"Step {step}: Removed alternate conformations")
            if self.verbose:
                print(f"   ✅ Alternate conformations removed")
            step += 1

            # Step 3: Keep only coordinate records (remove headers, remarks, etc.)
            temp_file3 = os.path.join(self.temp_dir, f"step3_{os.path.basename(input_pdb)}")
            if self.verbose:
                print(f"\n📋 Step {step}: Keeping only coordinate records")
            self.run_pdb_tool("pdb_keepcoord", current_file, temp_file3)
            current_file = temp_file3
            logger.info(f"Step {step}: Kept only coordinate records")
            if self.verbose:
                print(f"   ✅ Non-coordinate records removed")
            step += 1

            # Step 4: Handle heteroatoms and ligands
            if not keep_ligands and not keep_waters:
                temp_file4 = os.path.join(self.temp_dir, f"step4_{os.path.basename(input_pdb)}")
                self.run_pdb_tool("pdb_delhetatm", current_file, temp_file4)
                current_file = temp_file4
                logger.info(f"Step {step}: Removed heteroatoms (waters, ions, ligands)")
            elif keep_waters and not keep_ligands:
                # Keep only waters, remove other heteroatoms
                temp_file4 = os.path.join(self.temp_dir, f"step4_{os.path.basename(input_pdb)}")
                with open(current_file, 'r') as f_in, open(temp_file4, 'w') as f_out:
                    for line in f_in:
                        if line.startswith('HETATM'):
                            if 'HOH' in line:  # Keep water molecules
                                f_out.write(line)
                        else:
                            f_out.write(line)
                current_file = temp_file4
                logger.info(f"Step {step}: Kept waters, removed other heteroatoms")
            elif keep_ligands:
                # Custom ligand handling
                temp_file4 = os.path.join(self.temp_dir, f"step4_{os.path.basename(input_pdb)}")
                with open(current_file, 'r') as f_in, open(temp_file4, 'w') as f_out:
                    for line in f_in:
                        if line.startswith('HETATM'):
                            # Check if this heteroatom should be kept
                            for ligand in keep_ligands:
                                if ligand in line:
                                    f_out.write(line)
                                    break
                        else:
                            f_out.write(line)
                current_file = temp_file4
                logger.info(f"Step {step}: Kept specified ligands: {keep_ligands}")
            step += 1

            # Step 5: Renumber residues sequentially starting from 1
            temp_file5 = os.path.join(self.temp_dir, f"step5_{os.path.basename(input_pdb)}")
            if self.verbose:
                print(f"\n📋 Step {step}: Renumbering residues sequentially from 1")
            self.run_pdb_tool("pdb_reres -1", current_file, temp_file5)
            current_file = temp_file5
            logger.info(f"Step {step}: Renumbered residues sequentially from 1")
            if self.verbose:
                print(f"   ✅ Residues renumbered sequentially")
            step += 1

            # Step 6: Final tidying and validation
            if self.verbose:
                print(f"\n📋 Step {step}: Final tidying and validation")
            self.run_pdb_tool("pdb_tidy -strict", current_file, output_pdb)
            logger.info(f"Step {step}: Final tidying and validation")
            if self.verbose:
                print(f"   ✅ Final tidying complete")

            # Verify output file
            if not os.path.exists(output_pdb) or os.path.getsize(output_pdb) == 0:
                raise RuntimeError(f"Output file not created or is empty: {output_pdb}")

            # Final analysis of processed file
            if self.verbose:
                print(f"\n🎉 Preprocessing complete! Analyzing final result...")

            final_analysis = self.analyze_pdb_structure(output_pdb)

            logger.info(f"Processing complete:")
            logger.info(f"  - Atoms: {final_analysis['atoms']}")
            logger.info(f"  - Estimated residues: {final_analysis['estimated_residues']}")
            logger.info(f"  - Chains: {sorted(final_analysis['chains'])}")
            logger.info(f"  - TER records: {final_analysis['has_ter_records']}")

            # Validate CNS requirements
            if len(final_analysis['chains']) > 0 and not final_analysis['has_ter_records']:
                logger.warning("No TER records found but chains exist. This may cause CNS issues.")

            if final_analysis['estimated_residues'] > 10000:
                logger.warning(f"Large protein detected ({final_analysis['estimated_residues']} residues). CNS limit is 10,000 residues.")

            # SP55 SUCCESS CRITERIA
            success_criteria_met = True
            if final_analysis['atoms'] < 100:
                success_criteria_met = False
                logger.error("Too few atoms - preprocessing may have failed")

            if final_analysis['estimated_residues'] < 10:
                success_criteria_met = False
                logger.error("Too few residues - preprocessing may have failed")

            # Verbose success report
            if self.verbose:
                print(f"\n✅ PREPROCESSING SUCCESSFUL!")
                print(f"📊 Final Results:")
                print(f"   Output file: {output_pdb}")
                print(f"   File size: {final_analysis['file_size']:,} bytes")
                print(f"   Atoms: {final_analysis['atoms']:,}")
                print(f"   Estimated residues: {final_analysis['estimated_residues']:,}")
                print(f"   Chains: {sorted(final_analysis['chains'])}")
                print(f"   TER records: {'Yes' if final_analysis['has_ter_records'] else 'No'}")

                if final_analysis['multi_chain']:
                    print(f"⚠️  Multi-chain protein - ensure HADDOCK3 config is correct")

                if final_analysis['potential_issues']:
                    print(f"⚠️  Remaining issues to check:")
                    for issue in final_analysis['potential_issues']:
                        print(f"      - {issue}")
                else:
                    print(f"✅ No obvious issues detected")

                # Compare with input
                if analysis and final_analysis:
                    atom_reduction = analysis['atoms'] - final_analysis['atoms']
                    if atom_reduction > 0:
                        print(f"📉 Removed {atom_reduction:,} atoms during cleaning")
                    print(f"🔧 File ready for HADDOCK3!")

            if not success_criteria_met:
                raise RuntimeError("Preprocessing failed - success criteria not met")

            return output_pdb

        except Exception as e:
            logger.error(f"Preprocessing failed: {e}")
            raise

    def validate_pdb_for_cns(self, pdb_file):
        """
        Validate PDB file for CNS compatibility

        Returns:
            list: List of validation errors/warnings
        """
        errors = []
        warnings = []

        try:
            with open(pdb_file, 'r') as f:
                lines = f.readlines()
        except Exception as e:
            return [f"Cannot read PDB file: {e}"]

        # Basic format checks
        if not lines:
            return ["Empty PDB file"]

        # Check for standard PDB format
        atom_lines = [line for line in lines if line.startswith(('ATOM', 'HETATM'))]
        if not atom_lines:
            errors.append("No ATOM or HETATM records found")

        # Check for duplicate residues
        residues = {}
        for line in atom_lines:
            if len(line) >= 27:  # Minimum length for residue info
                chain_id = line[21].strip()
                res_num = line[22:26].strip()
                res_name = line[17:20].strip()

                if chain_id and res_num:
                    key = (chain_id, res_num)
                    if key in residues:
                        if residues[key] != res_name:
                            errors.append(f"Duplicate residue {res_num} in chain {chain_id}: {residues[key]} vs {res_name}")
                    else:
                        residues[key] = res_name

        # Check for TER records
        ter_lines = [line for line in lines if line.startswith('TER')]
        if len(residues) > 100 and not ter_lines:
            warnings.append("Large protein with no TER records - CNS may have issues")

        # Check for CNS limits
        total_residues = len(residues)
        if total_residues > 10000:
            errors.append(f"Too many residues for CNS: {total_residues} > 10000")

        # Check for unusual formats
        unusual_lines = 0
        for line in atom_lines:
            if len(line) < 54:  # Minimum expected length for coordinate data
                unusual_lines += 1

        if unusual_lines > 0:
            warnings.append(f"{unusual_lines} ATOM/HETATM lines with unusual format")

        return errors + warnings

    def batch_process_directory(self, input_dir, output_dir, **kwargs):
        """
        Process all PDB files in a directory

        Args:
            input_dir: Directory containing input PDB files
            output_dir: Directory for processed PDB files
            **kwargs: Additional arguments for preprocess_pdb
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        logger.info(f"Processing all PDB files in: {input_dir}")
        logger.info(f"Output directory: {output_dir}")

        pdb_files = list(input_path.glob("*.pdb"))
        if not pdb_files:
            logger.warning(f"No PDB files found in {input_dir}")
            return []

        results = []
        for pdb_file in pdb_files:
            logger.info(f"\n{'='*60}")
            logger.info(f"Processing: {pdb_file.name}")

            output_file = output_path / f"{pdb_file.stem}_clean.pdb"

            try:
                processed_file = self.preprocess_pdb(str(pdb_file), str(output_file), **kwargs)

                # Validate processed file
                validation_issues = self.validate_pdb_for_cns(processed_file)

                results.append({
                    'input_file': str(pdb_file),
                    'output_file': processed_file,
                    'status': 'success',
                    'validation_issues': validation_issues
                })

                if validation_issues:
                    logger.warning(f"Validation issues for {pdb_file.name}:")
                    for issue in validation_issues:
                        logger.warning(f"  - {issue}")
                else:
                    logger.info(f"✓ Successfully processed {pdb_file.name}")

            except Exception as e:
                logger.error(f"✗ Failed to process {pdb_file.name}: {e}")
                results.append({
                    'input_file': str(pdb_file),
                    'output_file': None,
                    'status': 'failed',
                    'error': str(e)
                })

        # Summary
        successful = sum(1 for r in results if r['status'] == 'success')
        total = len(results)
        logger.info(f"\n{'='*60}")
        logger.info(f"Batch processing complete: {successful}/{total} files processed successfully")

        return results


def main():
    """Main function for command line interface"""
    parser = argparse.ArgumentParser(
        description="Universal PDB Preprocessor for CNS/HADDOCK Compatibility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process single file
  python universal_pdb_preprocessor.py input.pdb output.pdb

  # Process single file keeping specific ligands
  python universal_pdb_preprocessor.py input.pdb output.pdb --keep-ligands ZN MG

  # Process single file keeping waters
  python universal_pdb_preprocessor.py input.pdb output.pdb --keep-waters

  # Process entire directory
  python universal_pdb_preprocessor.py --batch input_dir/ output_dir/

  # Validate existing file
  python universal_pdb_preprocessor.py --validate input.pdb
        """
    )

    parser.add_argument('input', help='Input PDB file or directory (use --batch for directories)')
    parser.add_argument('output', nargs='?', help='Output PDB file or directory (use --batch for directories)')
    parser.add_argument('--keep-ligands', nargs='*', help='List of ligand names to preserve')
    parser.add_argument('--keep-waters', action='store_true', help='Keep water molecules')
    parser.add_argument('--batch', action='store_true', help='Batch process directory of PDB files')
    parser.add_argument('--validate', action='store_true', help='Validate existing PDB file for CNS compatibility')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output with SP55 enhancements')
    parser.add_argument('--input-short', '--input_file', help='Input PDB file (alternative format)')
    parser.add_argument('--output-short', '--output_file', help='Output PDB file (alternative format)')

    args = parser.parse_args()

    # Support alternative parameter names
    if hasattr(args, 'input_short') and args.input_short:
        args.input = args.input_short
    if hasattr(args, 'output_short') and args.output_short:
        args.output = args.output_short

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        print("🔬 Verbose mode enabled")
        print(f"📋 Command: {' '.join(sys.argv)}")
        print(f"📅 Timestamp: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("")

    # Create preprocessor instance with verbose flag
    preprocessor = UniversalPDBPreprocessor(verbose=args.verbose)

    try:
        if args.validate:
            # Validate mode
            if not args.input or os.path.isdir(args.input):
                parser.error("Validation requires a single PDB file as input")

            validation_issues = preprocessor.validate_pdb_for_cns(args.input)

            if validation_issues:
                print(f"Validation issues found for {args.input}:")
                for issue in validation_issues:
                    print(f"  - {issue}")
                sys.exit(1)
            else:
                print(f"✓ {args.input} appears valid for CNS/HADDOCK")
                sys.exit(0)

        elif args.batch:
            # Batch processing mode
            if not args.input or not args.output:
                parser.error("Batch mode requires both input and output directories")

            if not os.path.isdir(args.input):
                parser.error(f"Input directory not found: {args.input}")

            kwargs = {}
            if args.keep_ligands:
                kwargs['keep_ligands'] = args.keep_ligands
            if args.keep_waters:
                kwargs['keep_waters'] = args.keep_waters

            results = preprocessor.batch_process_directory(args.input, args.output, **kwargs)

            # Print summary
            successful = sum(1 for r in results if r['status'] == 'success')
            total = len(results)
            print(f"\nProcessing complete: {successful}/{total} files successful")

            if successful < total:
                print("\nFailed files:")
                for result in results:
                    if result['status'] == 'failed':
                        print(f"  - {result['input_file']}: {result.get('error', 'Unknown error')}")
                sys.exit(1)

        else:
            # Single file processing mode
            if not args.input or not args.output:
                parser.error("Single file mode requires both input and output files")

            kwargs = {}
            if args.keep_ligands:
                kwargs['keep_ligands'] = args.keep_ligands
            if args.keep_waters:
                kwargs['keep_waters'] = args.keep_waters

            processed_file = preprocessor.preprocess_pdb(args.input, args.output, **kwargs)

            # Validate processed file
            validation_issues = preprocessor.validate_pdb_for_cns(processed_file)

            if validation_issues:
                print(f"\nProcessed file: {processed_file}")
                print(f"Validation issues:")
                for issue in validation_issues:
                    print(f"  - {issue}")
            else:
                print(f"✓ Successfully processed: {processed_file}")
                print("✓ File appears valid for CNS/HADDOCK")

    except KeyboardInterrupt:
        logger.info("Processing interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Processing failed: {e}")
        sys.exit(1)
    finally:
        preprocessor.cleanup()


if __name__ == "__main__":
    main()