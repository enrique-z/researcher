#!/usr/bin/env python3
"""
QUICK START DRUG DISCOVERY EXPERIMENT SETUP
==========================================

Automated experiment setup following SP55 template.
Supports ALL experiment types: peptides, small molecules, antibodies, PPIs.

Usage:
    python start_drug_discovery_experiment.py --customer CUSTOMER_NAME --compound COMPOUND_NAME --type EXPERIMENT_TYPE

Example:
    python start_drug_discovery_experiment.py --customer WorldPathol --compound NK1R --type small_molecule
"""

import os
import sys
import argparse
import shutil
import json
from pathlib import Path
from datetime import datetime

# Configuration
SP55_TEMPLATE_DIR = "/Users/apple/code/Researcher-bio2/EXPERIMENTS/bazo-digital/sp55-toxicity-screening"
BASE_EXPERIMENTS_DIR = "/Users/apple/code/Researcher-bio2/EXPERIMENTS/bazo-digital"

# Experiment type configurations
EXPERIMENT_CONFIGS = {
    "peptide": {
        "description": "Therapeutic Peptide Analysis (20-100 AA)",
        "tools": ["ESM2", "BioPython", "AlphaFold2", "AutoDock Vina", "UniProt"],
        "timeline": "2 hours",
        "receptors": 20,
        "input_type": "sequence",
        "sequence_length_range": (20, 100)
    },
    "small_molecule": {
        "description": "Small Molecule Virtual Screening",
        "tools": ["RDKit", "PubChem", "ChEMBL", "AutoDock Vina", "DrugBank"],
        "timeline": "6-11 hours",
        "receptors": "multi-target",
        "input_type": "smiles",
        "molecular_weight_range": (150, 600)
    },
    "antibody": {
        "description": "Antibody-Antigen Analysis",
        "tools": ["RosettaAntibody", "ABodyBuilder", "AutoDock Vina", "PyMOL"],
        "timeline": "5-8 hours",
        "receptors": 1,
        "input_type": "cdr_sequences",
        "framework": "antibody"
    },
    "protein_interaction": {
        "description": "Protein-Protein Interaction Analysis",
        "tools": ["AlphaFold2", "HADDOCK", "Rosetta", "Cytoscape"],
        "timeline": "6-12 hours",
        "receptors": 1,
        "input_type": "protein_sequences",
        "complex_size": "large"
    },
    "polypharmacology": {
        "description": "Multi-Target Polypharmacology Analysis",
        "tools": ["STRING", "KEGG", "AutoDock Vina", "Cytoscape", "NetworkX"],
        "timeline": "11-15 hours",
        "receptors": "50-200",
        "input_type": "compound_or_protein",
        "network_analysis": True
    },
    "ai_enhanced": {
        "description": "AI-Enhanced Drug Discovery",
        "tools": ["BioNeMo", "ESM2", "RDKit", "XGBoost", "AutoDock Vina"],
        "timeline": "10-18 hours",
        "receptors": "multi",
        "input_type": "any",
        "gpu_required": True
    }
}

def validate_input(experiment_type, input_value):
    """Validate input based on experiment type"""
    config = EXPERIMENT_CONFIGS.get(experiment_type)
    if not config:
        raise ValueError(f"Unknown experiment type: {experiment_type}")

    input_type = config["input_type"]

    if input_type == "sequence":
        # Validate peptide sequence
        aa_count = len(input_value)
        min_len, max_len = config["sequence_length_range"]
        if not (min_len <= aa_count <= max_len):
            raise ValueError(f"Sequence length {aa_count} not in range {min_len}-{max_len}")
        if not all(aa in "ACDEFGHIKLMNPQRSTVWY" for aa in input_value.upper()):
            raise ValueError("Invalid amino acids in sequence")

    elif input_type == "smiles":
        # Basic SMILES validation
        if len(input_value) < 3:
            raise ValueError("SMILES string too short")
        if not any(c in input_value for c in "CNOPSFClBrI"):
            raise ValueError("SMILES appears invalid (no common atoms)")

    elif input_type in ["cdr_sequences", "protein_sequences"]:
        # Validate protein sequences
        if not input_value or len(input_value) < 10:
            raise ValueError("Protein sequence too short")

    return True

def create_experiment_directory(customer_name, compound_name, experiment_type):
    """Create experiment directory structure"""
    experiment_name = f"{customer_name}-{compound_name}-{experiment_type}"
    experiment_dir = os.path.join(BASE_EXPERIMENTS_DIR, experiment_name)

    if os.path.exists(experiment_dir):
        raise ValueError(f"Experiment directory already exists: {experiment_dir}")

    os.makedirs(experiment_dir, exist_ok=True)
    print(f"✓ Created experiment directory: {experiment_dir}")

    # Create subdirectories
    subdirs = ["structures", "receptors", "config", "results", "logs", "report", "data"]
    for subdir in subdirs:
        os.makedirs(os.path.join(experiment_dir, subdir), exist_ok=True)

    return experiment_dir

def copy_template_files(experiment_dir, experiment_type):
    """Copy and adapt template files from SP55"""
    config = EXPERIMENT_CONFIGS[experiment_type]

    # Files to always copy
    essential_files = [
        "execute_master_plan.py",
        "update_customer_report_simple.py",
        "comprehensive_safety_analysis.py",
        "SP55_structure_real.pdb",
        "TABLE_IV_BINDING_AFFINITIES.tex",
        "TABLE_V_TISSUE_RISK.tex"
    ]

    for file_name in essential_files:
        src_path = os.path.join(SP55_TEMPLATE_DIR, file_name)
        if os.path.exists(src_path):
            dst_path = os.path.join(experiment_dir, file_name)
            shutil.copy2(src_path, dst_path)
            print(f"✓ Copied template: {file_name}")
        else:
            print(f"⚠ Template file not found: {file_name}")

    # Copy receptor data if needed
    if config.get("receptors") and not config.get("receptors") == "multi-target":
        receptor_dir = os.path.join(experiment_dir, "receptors")
        src_receptor_dir = os.path.join(SP55_TEMPLATE_DIR, "receptors")
        if os.path.exists(src_receptor_dir):
            shutil.copytree(src_receptor_dir, os.path.join(experiment_dir, "receptors_copy"), dirs_exist_ok=True)

def create_experiment_config(experiment_dir, customer_name, compound_name, experiment_type, input_value):
    """Create experiment-specific configuration"""
    config = EXPERIMENT_CONFIGS[experiment_type]

    experiment_config = {
        "experiment_metadata": {
            "customer": customer_name,
            "compound_name": compound_name,
            "experiment_type": experiment_type,
            "description": config["description"],
            "created_date": datetime.now().isoformat(),
            "tools_required": config["tools"],
            "expected_timeline": config["timeline"],
            "input_value": input_value
        },
        "tool_paths": {
            "vina": "/Users/apple/code/Researcher-bio2/vina/vina",
            "python": "/Users/apple/code/Researcher-bio2/.venv/bin/python",
            "template_dir": SP55_TEMPLATE_DIR
        },
        "analysis_parameters": {
            "number_of_receptors": config.get("receptors", 20),
            "docking_exhaustiveness": 8,
            "grid_size": [25, 25, 25],
            "energy_range": 3.0
        },
        "output_requirements": {
            "binding_energy_units": "kcal/mol",
            "table_format": "double_column",
            "report_format": "latex_pdf",
            "anti_fabrication_checks": True
        }
    }

    config_path = os.path.join(experiment_dir, "experiment_config.json")
    with open(config_path, 'w') as f:
        json.dump(experiment_config, f, indent=2)

    print(f"✓ Created experiment configuration: {config_path}")

def adapt_master_script(experiment_dir, experiment_type, input_value):
    """Adapt the master execution script for the specific experiment"""
    script_path = os.path.join(experiment_dir, "execute_master_plan.py")

    if not os.path.exists(script_path):
        print(f"⚠ Master script not found: {script_path}")
        return

    # Read the script
    with open(script_path, 'r') as f:
        script_content = f.read()

    # Adapt based on experiment type
    if experiment_type == "peptide":
        script_content = script_content.replace(
            'SP55_SEQUENCE = "MGFINLDKPSNPSSHEVVGWIRRILKVEKTAHSGTLDPKVTGCLIVSIERGTRVLK"',
            f'SP55_SEQUENCE = "{input_value}"'
        )
    elif experiment_type == "small_molecule":
        script_content = script_content.replace(
            '# Sequence: MGFINLDKPSNPSSHEVVGWIRRILKVEKTAHSGTLDPKVTGCLIVSIERGTRVLK',
            f'# SMILES: {input_value}'
        )
        script_content = script_content.replace(
            "SP55_SEQUENCE =",
            "SMILES_STRING ="
        )

    # Update experiment type in comments
    script_content = script_content.replace(
        "SP55 MASTER EXECUTION PLAN",
        f"{experiment_type.upper()} MASTER EXECUTION PLAN"
    )

    # Write adapted script
    with open(script_path, 'w') as f:
        f.write(script_content)

    print(f"✓ Adapted master script for {experiment_type}")

def create_checklist_file(experiment_dir, experiment_type):
    """Create a validation checklist for the experiment"""
    config = EXPERIMENT_CONFIGS[experiment_type]

    checklist = f"""
# {config['description']} - VALIDATION CHECKLIST
# Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## PRE-EXPERIMENT VALIDATION
- [ ] Tools installed and accessible
- [ ] Python environment activated
- [ ] Input data validated ({config['input_type']})
- [ ] Template files copied successfully
- [ ] Directory structure created

## DURING EXECUTION
- [ ] Real tool execution (no simulations)
- [ ] Execution logs with timestamps
- [ ] Binding energies in kcal/mol
- [ ] No dimensionless scores (/10 format)
- [ ] Cross-reference validation

## POST-EXPERIMENT
- [ ] All values consistent across report
- [ ] Tables IV and V generated
- [ ] No "fabricated" references remain
- [ ] M3 Pro references replaced with "Computer"
- [ ] Cost references removed
- [ ] PDF compiles successfully

## CRITICAL SAFETY CHECKS
- [ ] Patient safety considerations documented
- [ ] Regulatory compliance verified
- [ ] Data integrity confirmed
- [ ] Anti-fabrication protocols followed

## TIMELINE EXPECTATION: {config['timeline']}
## TOOLS REQUIRED: {', '.join(config['tools'])}
"""

    checklist_path = os.path.join(experiment_dir, "VALIDATION_CHECKLIST.md")
    with open(checklist_path, 'w') as f:
        f.write(checklist)

    print(f"✓ Created validation checklist: {checklist_path}")

def generate_startup_commands(experiment_dir, experiment_type):
    """Generate specific commands to start the experiment"""
    config = EXPERIMENT_CONFIGS[experiment_type]

    commands = f"""
#!/bin/bash
# STARTUP COMMANDS FOR {experiment_type.upper()} EXPERIMENT
# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

cd {experiment_dir}

# 1. Activate Python Environment
source /Users/apple/code/Researcher-bio2/.venv/bin/activate

# 2. Verify Tools Available
echo "Checking tools..."
ls -la /Users/apple/code/Researcher-bio2/vina/vina && echo "✓ Vina available"
python -c "import torch; print('✓ PyTorch available')"
python -c "from Bio.SeqUtils.ProtParam import ProteinAnalysis; print('✓ BioPython available')"

# 3. Run Master Execution Plan
echo "Starting {config['description']}..."
python execute_master_plan.py

# 4. Generate Report
echo "Generating customer report..."
python update_customer_report_simple.py

# 5. Compile PDF
echo "Compiling final PDF..."
cd report
export PATH="/usr/local/texlive/2025/bin/universal-darwin:$PATH"
pdflatex *.tex && bibtex *.tex && pdflatex *.tex && pdflatex *.tex

echo "Experiment complete! Check report/ directory for final PDF."
"""

    commands_path = os.path.join(experiment_dir, "run_experiment.sh")
    with open(commands_path, 'w') as f:
        f.write(commands)

    # Make executable
    os.chmod(commands_path, 0o755)
    print(f"✓ Created startup script: {commands_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Quick setup for drug discovery experiments",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available experiment types:
  peptide           - Therapeutic peptide analysis (20-100 AA)
  small_molecule     - Small molecule virtual screening
  antibody          - Antibody-antigen analysis
  protein_interaction - Protein-protein interaction analysis
  polypharmacology   - Multi-target network pharmacology
  ai_enhanced       - AI-enhanced drug discovery

Example usage:
  python start_drug_discovery_experiment.py --customer WorldPathol --compound SP55 --type peptide --sequence "MGFINLDKPSNPSSHEVVGWIRRILKVEKTAHSGTLDPKVTGCLIVSIERGTRVLK"

  python start_drug_discovery_experiment.py --customer PharmaCo --compound NK1R --type small_molecule --smiles "CC(C)C1=CC=C(C=C1)C(=O)NC2=NC=NC3=C2N=CN3"
        """
    )

    parser.add_argument("--customer", required=True, help="Customer name")
    parser.add_argument("--compound", required=True, help="Compound/therapeutic name")
    parser.add_argument("--type", required=True, choices=EXPERIMENT_CONFIGS.keys(), help="Experiment type")

    # Input options
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--sequence", help="Peptide sequence")
    input_group.add_argument("--smiles", help="SMILES string for small molecule")
    input_group.add_argument("--protein1", help="First protein sequence (for PPI)")
    input_group.add_argument("--protein2", help="Second protein sequence (for PPI)")
    input_group.add_argument("--cdr_sequences", help="CDR sequences (for antibodies)")
    input_group.add_argument("--custom_input", help="Custom input for other experiment types")

    args = parser.parse_args()

    # Determine input value based on experiment type
    input_value = None
    if args.sequence:
        input_value = args.sequence
    elif args.smiles:
        input_value = args.smiles
    elif args.protein1:
        input_value = f"{args.protein1}|{args.protein2 or ''}"
    elif args.cdr_sequences:
        input_value = args.cdr_sequences
    else:
        input_value = args.custom_input

    # Validate input
    try:
        validate_input(args.type, input_value)
    except ValueError as e:
        print(f"❌ Input validation error: {e}")
        sys.exit(1)

    print(f"🚀 Setting up {args.customer} {args.compound} {args.type} experiment...")

    # Create experiment directory
    try:
        experiment_dir = create_experiment_directory(args.customer, args.compound, args.type)
    except Exception as e:
        print(f"❌ Failed to create experiment directory: {e}")
        sys.exit(1)

    # Copy template files
    print("\n📋 Copying template files...")
    copy_template_files(experiment_dir, args.type)

    # Create configuration
    print("\n⚙️ Creating experiment configuration...")
    create_experiment_config(experiment_dir, args.customer, args.compound, args.type, input_value)

    # Adapt master script
    print("\n🔄 Adapting execution scripts...")
    adapt_master_script(experiment_dir, args.type, input_value)

    # Create validation checklist
    print("\n📝 Creating validation checklist...")
    create_checklist_file(experiment_dir, args.type)

    # Generate startup commands
    print("\n🚀 Generating startup script...")
    generate_startup_commands(experiment_dir, args.type)

    # Success message
    config = EXPERIMENT_CONFIGS[args.type]
    print(f"\n✅ EXPERIMENT SETUP COMPLETE!")
    print(f"📁 Location: {experiment_dir}")
    print(f"⏱️ Expected timeline: {config['timeline']}")
    print(f"🛠️ Tools required: {', '.join(config['tools'])}")
    print(f"\n🚀 To start the experiment:")
    print(f"   cd {experiment_dir}")
    print(f"   ./run_experiment.sh")
    print(f"\n📋 Follow the VALIDATION_CHECKLIST.md for quality assurance")
    print(f"⚠️ REMEMBER: Patient safety depends on authentic results!")

if __name__ == "__main__":
    main()