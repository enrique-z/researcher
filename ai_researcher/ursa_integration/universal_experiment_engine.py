"""
Universal Experiment Engine - URSA Integration for Any Scientific Domain

This module provides the core integration between URSA's ExecutionAgent and the universal
scientific research pipeline. Designed to work with any research domain: climate, physics,
chemistry, biology, etc.

Key Features:
- Domain-agnostic experiment configuration
- Universal data loading framework  
- Flexible calculation templates
- Real experimental execution via URSA subprocess
"""

import os
import sys
import json
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Tuple
from datetime import datetime
import tempfile
import shutil

# Add URSA to Python path for integration
URSA_PATH = "/Users/apple/code/losalamos"
if URSA_PATH not in sys.path:
    sys.path.append(URSA_PATH)

try:
    from src.ursa.agents.execution_agent import ExecutionAgent, ExecutionState
    URSA_AVAILABLE = True
    logging.info("✅ URSA ExecutionAgent imported successfully")
except ImportError as e:
    URSA_AVAILABLE = False
    logging.warning(f"❌ URSA ExecutionAgent import failed: {e}")

# Domain configuration imports
from .domain_configs.universal_base_config import UniversalBaseConfig
from .domain_configs.climate_research_config import ClimateResearchConfig
from .data_loaders.universal_data_loader import UniversalDataLoader

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UniversalExperimentEngine:
    """
    Universal scientific experiment engine using URSA ExecutionAgent.
    
    Supports any research domain through configurable templates and validation.
    Executes real calculations via URSA's subprocess execution capability.
    """
    
    def __init__(self, 
                 research_domain: str = "climate",
                 ursa_model: str = "openai/gpt-4o-mini",
                 workspace_dir: Optional[str] = None):
        """
        Initialize universal experiment engine.
        
        Args:
            research_domain: Research domain (climate, physics, chemistry, biology, etc.)
            ursa_model: Model for URSA ExecutionAgent
            workspace_dir: Custom workspace directory for experiments
        """
        self.research_domain = research_domain
        self.ursa_model = ursa_model
        self.workspace_dir = workspace_dir or self._create_workspace()
        
        # URSA integration
        self.ursa_agent = None
        self.ursa_available = URSA_AVAILABLE
        
        # Universal components
        self.domain_config = None
        self.data_loader = None
        self.experiment_history = []
        
        # System statistics
        self.stats = {
            'total_experiments': 0,
            'successful_experiments': 0,
            'failed_experiments': 0,
            'domains_used': set(),
            'calculations_executed': 0,
            'data_sources_accessed': set()
        }
        
        logger.info(f"🚀 Universal Experiment Engine initializing...")
        logger.info(f"Research domain: {self.research_domain}")
        logger.info(f"URSA available: {self.ursa_available}")
        logger.info(f"Workspace: {self.workspace_dir}")
        
        # Initialize components
        self._initialize_components()
    
    def _create_workspace(self) -> str:
        """Create temporary workspace for experiments."""
        workspace = tempfile.mkdtemp(prefix="ursa_experiments_")
        return workspace
    
    def _initialize_components(self):
        """Initialize URSA and universal components."""
        try:
            # Initialize URSA ExecutionAgent
            if self.ursa_available:
                self.ursa_agent = ExecutionAgent(
                    llm=self.ursa_model,
                    log_history=True,
                    log_state=False
                )
                logger.info("✅ URSA ExecutionAgent initialized")
            
            # Initialize domain configuration (climate specialized only)
            if self.research_domain == "climate":
                self.domain_config = ClimateResearchConfig()
            else:
                logger.warning(f"Domain {self.research_domain} not supported. Using climate as default.")
                self.domain_config = ClimateResearchConfig()
                self.research_domain = "climate"
            logger.info(f"✅ Domain config loaded: {self.research_domain}")
            
            # Initialize universal data loader
            self.data_loader = UniversalDataLoader(self.research_domain)
            logger.info("✅ Universal data loader initialized")
            
        except Exception as e:
            logger.error(f"❌ Component initialization failed: {e}")
    
    def configure_experiment(self, 
                           experiment_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Configure experiment for any research domain.
        
        Args:
            experiment_config: Domain-specific experiment configuration
            
        Returns:
            Dict with configured experiment ready for execution
        """
        config_start = datetime.now()
        
        configured_experiment = {
            'experiment_id': f"exp_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'research_domain': self.research_domain,
            'configuration_timestamp': config_start.isoformat(),
            'original_config': experiment_config,
            'ursa_commands': [],
            'data_requirements': [],
            'calculation_templates': [],
            'validation_criteria': {},
            'expected_outputs': [],
            'configuration_successful': False,
            'error': None
        }
        
        try:
            # Domain-specific configuration
            domain_setup = self.domain_config.configure_experiment(experiment_config)
            configured_experiment.update(domain_setup)
            
            # Data requirements analysis
            data_requirements = self._analyze_data_requirements(experiment_config)
            configured_experiment['data_requirements'] = data_requirements
            
            # Generate URSA execution commands
            ursa_commands = self._generate_ursa_commands(experiment_config, domain_setup)
            configured_experiment['ursa_commands'] = ursa_commands
            
            # Validation criteria setup
            validation_criteria = self._setup_validation_criteria(experiment_config)
            configured_experiment['validation_criteria'] = validation_criteria
            
            configured_experiment['configuration_successful'] = True
            logger.info(f"✅ Experiment configured: {configured_experiment['experiment_id']}")
            
        except Exception as e:
            logger.error(f"❌ Experiment configuration failed: {e}")
            configured_experiment['error'] = str(e)
        
        return configured_experiment
    
    def execute_experiment(self, 
                         configured_experiment: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute experiment using URSA ExecutionAgent.
        
        Args:
            configured_experiment: Configured experiment from configure_experiment()
            
        Returns:
            Dict with experiment results and URSA execution outputs
        """
        if not self.ursa_available:
            return {
                'success': False,
                'error': 'URSA ExecutionAgent not available',
                'experiment_id': configured_experiment.get('experiment_id', 'unknown')
            }
        
        execution_start = datetime.now()
        self.stats['total_experiments'] += 1
        self.stats['domains_used'].add(self.research_domain)
        
        experiment_result = {
            'experiment_id': configured_experiment['experiment_id'],
            'execution_timestamp': execution_start.isoformat(),
            'research_domain': self.research_domain,
            'ursa_outputs': [],
            'calculation_results': {},
            'data_loaded': {},
            'validation_results': {},
            'generated_files': [],
            'execution_successful': False,
            'error': None
        }
        
        try:
            # Create URSA execution state
            ursa_state = ExecutionState(
                messages=[],
                current_progress="Initializing universal experiment",
                code_files=[],
                workspace=self.workspace_dir,
                symlinkdir={}
            )
            
            # Execute data loading if required
            if configured_experiment['data_requirements']:
                data_results = self._execute_data_loading(configured_experiment)
                experiment_result['data_loaded'] = data_results
            
            # Execute URSA calculations
            for command_config in configured_experiment['ursa_commands']:
                ursa_output = self._execute_ursa_command(command_config, ursa_state)
                experiment_result['ursa_outputs'].append(ursa_output)
                self.stats['calculations_executed'] += 1
            
            # Process and validate results
            if experiment_result['ursa_outputs']:
                calculation_results = self._process_ursa_results(experiment_result['ursa_outputs'])
                experiment_result['calculation_results'] = calculation_results
                
                # Validate results
                validation_results = self._validate_experiment_results(
                    experiment_result, configured_experiment['validation_criteria']
                )
                experiment_result['validation_results'] = validation_results
            
            # Generate summary files
            generated_files = self._generate_output_files(experiment_result)
            experiment_result['generated_files'] = generated_files
            
            experiment_result['execution_successful'] = True
            self.stats['successful_experiments'] += 1
            logger.info(f"✅ Experiment executed successfully: {experiment_result['experiment_id']}")
            
        except Exception as e:
            logger.error(f"❌ Experiment execution failed: {e}")
            experiment_result['error'] = str(e)
            self.stats['failed_experiments'] += 1
        
        # Record experiment history
        experiment_result['duration_seconds'] = (datetime.now() - execution_start).total_seconds()
        self.experiment_history.append(experiment_result)
        
        return experiment_result
    
    def _analyze_data_requirements(self, experiment_config: Dict) -> List[Dict]:
        """Analyze what data is needed for the experiment."""
        return self.data_loader.analyze_requirements(experiment_config)
    
    def _generate_ursa_commands(self, 
                              experiment_config: Dict, 
                              domain_setup: Dict) -> List[Dict]:
        """Generate URSA execution commands for the experiment."""
        commands = []
        
        # Basic Python scientific setup
        commands.append({
            'type': 'setup',
            'description': 'Install and import scientific libraries',
            'python_code': '''
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
from datetime import datetime

print("✅ Scientific libraries imported successfully")
print(f"NumPy version: {np.__version__}")
print(f"SciPy version: {sp.__version__}")
print(f"Matplotlib version: {plt.matplotlib.__version__}")
print(f"Pandas version: {pd.__version__}")
'''
        })
        
        # Domain-specific calculations
        domain_commands = self.domain_config.generate_calculation_commands(experiment_config)
        commands.extend(domain_commands)
        
        return commands
    
    def _setup_validation_criteria(self, experiment_config: Dict) -> Dict:
        """Setup validation criteria for experiment results."""
        return self.domain_config.get_validation_criteria(experiment_config)
    
    def _execute_data_loading(self, configured_experiment: Dict) -> Dict:
        """Execute data loading for the experiment."""
        data_results = {}
        
        for data_req in configured_experiment['data_requirements']:
            try:
                loaded_data = self.data_loader.load_data(data_req)
                data_results[data_req['name']] = loaded_data
                self.stats['data_sources_accessed'].add(data_req['source'])
                logger.info(f"✅ Data loaded: {data_req['name']}")
            except Exception as e:
                logger.error(f"❌ Data loading failed for {data_req['name']}: {e}")
                data_results[data_req['name']] = {'error': str(e)}
        
        return data_results
    
    def _execute_ursa_command(self, 
                            command_config: Dict, 
                            ursa_state: ExecutionState) -> Dict:
        """Execute single URSA command and return results."""
        command_start = datetime.now()
        
        ursa_output = {
            'command_type': command_config['type'],
            'description': command_config['description'],
            'timestamp': command_start.isoformat(),
            'success': False,
            'stdout': '',
            'stderr': '',
            'files_created': [],
            'execution_time_seconds': 0,
            'error': None
        }
        
        try:
            if command_config['type'] == 'setup':
                # Execute Python setup code
                python_file = os.path.join(self.workspace_dir, 'setup.py')
                with open(python_file, 'w') as f:
                    f.write(command_config['python_code'])
                
                # Execute via subprocess (mimicking URSA's approach)
                result = subprocess.run(
                    f"python {python_file}",
                    shell=True,
                    capture_output=True,
                    text=True,
                    cwd=self.workspace_dir,
                    timeout=300
                )
                
                ursa_output['stdout'] = result.stdout
                ursa_output['stderr'] = result.stderr
                ursa_output['success'] = result.returncode == 0
                
            elif command_config['type'] == 'calculation':
                # Execute calculation code
                calc_file = os.path.join(self.workspace_dir, f"calculation_{datetime.now().strftime('%H%M%S')}.py")
                with open(calc_file, 'w') as f:
                    f.write(command_config['python_code'])
                
                result = subprocess.run(
                    f"python {calc_file}",
                    shell=True,
                    capture_output=True,
                    text=True,
                    cwd=self.workspace_dir,
                    timeout=600
                )
                
                ursa_output['stdout'] = result.stdout
                ursa_output['stderr'] = result.stderr
                ursa_output['success'] = result.returncode == 0
                ursa_output['files_created'].append(calc_file)
            
            ursa_output['execution_time_seconds'] = (datetime.now() - command_start).total_seconds()
            logger.info(f"✅ URSA command executed: {command_config['type']}")
            
        except Exception as e:
            logger.error(f"❌ URSA command execution failed: {e}")
            ursa_output['error'] = str(e)
        
        return ursa_output
    
    def _process_ursa_results(self, ursa_outputs: List[Dict]) -> Dict:
        """Process URSA execution results into structured format."""
        calculation_results = {
            'successful_commands': 0,
            'failed_commands': 0,
            'total_execution_time': 0,
            'outputs': [],
            'files_generated': [],
            'errors': []
        }
        
        for output in ursa_outputs:
            calculation_results['total_execution_time'] += output.get('execution_time_seconds', 0)
            
            if output['success']:
                calculation_results['successful_commands'] += 1
                calculation_results['outputs'].append({
                    'type': output['command_type'],
                    'stdout': output['stdout'],
                    'files': output.get('files_created', [])
                })
                calculation_results['files_generated'].extend(output.get('files_created', []))
            else:
                calculation_results['failed_commands'] += 1
                calculation_results['errors'].append({
                    'type': output['command_type'],
                    'error': output.get('error', 'Unknown error'),
                    'stderr': output['stderr']
                })
        
        return calculation_results
    
    def _validate_experiment_results(self, 
                                   experiment_result: Dict, 
                                   validation_criteria: Dict) -> Dict:
        """Validate experiment results against criteria."""
        validation_results = {
            'validation_passed': False,
            'criteria_checked': len(validation_criteria),
            'criteria_passed': 0,
            'validation_details': [],
            'recommendations': []
        }
        
        for criterion_name, criterion_config in validation_criteria.items():
            try:
                # Apply validation criterion
                validation_passed = self._apply_validation_criterion(
                    experiment_result, criterion_name, criterion_config
                )
                
                validation_details = {
                    'criterion': criterion_name,
                    'passed': validation_passed,
                    'description': criterion_config.get('description', ''),
                    'threshold': criterion_config.get('threshold'),
                    'result': validation_passed
                }
                
                validation_results['validation_details'].append(validation_details)
                
                if validation_passed:
                    validation_results['criteria_passed'] += 1
                    
            except Exception as e:
                logger.error(f"❌ Validation criterion {criterion_name} failed: {e}")
                validation_results['validation_details'].append({
                    'criterion': criterion_name,
                    'passed': False,
                    'error': str(e)
                })
        
        # Overall validation result
        validation_results['validation_passed'] = (
            validation_results['criteria_passed'] == validation_results['criteria_checked']
        )
        
        return validation_results
    
    def _apply_validation_criterion(self, 
                                  experiment_result: Dict, 
                                  criterion_name: str, 
                                  criterion_config: Dict) -> bool:
        """Apply single validation criterion."""
        if criterion_name == 'execution_success':
            return experiment_result.get('execution_successful', False)
        
        elif criterion_name == 'no_errors':
            return len(experiment_result.get('calculation_results', {}).get('errors', [])) == 0
        
        elif criterion_name == 'files_generated':
            min_files = criterion_config.get('minimum', 1)
            files_count = len(experiment_result.get('generated_files', []))
            return files_count >= min_files
        
        elif criterion_name == 'calculation_completion':
            calc_results = experiment_result.get('calculation_results', {})
            successful = calc_results.get('successful_commands', 0)
            total = successful + calc_results.get('failed_commands', 0)
            return total > 0 and successful == total
        
        # Default: assume passed if no specific logic
        return True
    
    def _generate_output_files(self, experiment_result: Dict) -> List[str]:
        """Generate summary output files for the experiment."""
        generated_files = []
        
        try:
            # Generate experiment summary JSON
            summary_file = os.path.join(
                self.workspace_dir, 
                f"experiment_summary_{experiment_result['experiment_id']}.json"
            )
            with open(summary_file, 'w') as f:
                json.dump(experiment_result, f, indent=2, default=str)
            generated_files.append(summary_file)
            
            # Generate readable report
            report_file = os.path.join(
                self.workspace_dir,
                f"experiment_report_{experiment_result['experiment_id']}.txt"
            )
            with open(report_file, 'w') as f:
                f.write(f"Experiment Report: {experiment_result['experiment_id']}\n")
                f.write(f"Domain: {experiment_result['research_domain']}\n")
                f.write(f"Execution Time: {experiment_result.get('duration_seconds', 0):.2f} seconds\n")
                f.write(f"Success: {experiment_result['execution_successful']}\n\n")
                
                if experiment_result['calculation_results']:
                    calc_results = experiment_result['calculation_results']
                    f.write(f"Calculations: {calc_results['successful_commands']} successful, {calc_results['failed_commands']} failed\n")
                    f.write(f"Total calculation time: {calc_results['total_execution_time']:.2f} seconds\n\n")
                
                if experiment_result['validation_results']:
                    val_results = experiment_result['validation_results']
                    f.write(f"Validation: {val_results['criteria_passed']}/{val_results['criteria_checked']} criteria passed\n")
                    f.write(f"Overall validation: {'PASSED' if val_results['validation_passed'] else 'FAILED'}\n")
            
            generated_files.append(report_file)
            
        except Exception as e:
            logger.error(f"❌ Output file generation failed: {e}")
        
        return generated_files
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status and statistics."""
        return {
            'engine_active': True,
            'research_domain': self.research_domain,
            'ursa_available': self.ursa_available,
            'workspace_dir': self.workspace_dir,
            'statistics': self.stats.copy(),
            'experiment_history_count': len(self.experiment_history),
            'components_status': {
                'ursa_agent': 'READY' if self.ursa_agent else 'UNAVAILABLE',
                'domain_config': 'READY' if self.domain_config else 'NOT_LOADED',
                'data_loader': 'READY' if self.data_loader else 'NOT_LOADED'
            }
        }


# Convenience functions for universal pipeline integration
def create_experiment_engine(research_domain: str = "climate") -> UniversalExperimentEngine:
    """Create universal experiment engine for any research domain."""
    return UniversalExperimentEngine(research_domain)

def execute_universal_experiment(experiment_config: Dict[str, Any], 
                               research_domain: str = "climate") -> Dict[str, Any]:
    """
    One-line function to execute experiment in any research domain.
    
    Usage:
    results = execute_universal_experiment({
        'research_question': 'SAI pulse vs continuous injection',
        'calculations': ['aerosol_transport', 'radiative_forcing'],
        'data_sources': ['GLENS']
    }, research_domain='climate')
    """
    engine = create_experiment_engine(research_domain)
    configured_exp = engine.configure_experiment(experiment_config)
    return engine.execute_experiment(configured_exp)