"""
Universal Base Configuration for Any Research Domain

This module provides the base configuration class that adapts to any scientific research domain.
Specific domains (climate, physics, chemistry, biology) inherit from this base class.

Key Features:
- Domain-agnostic experiment configuration
- Flexible calculation template generation
- Universal validation criteria setup
- Extensible for new research domains
"""

import os
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union, Any, Tuple
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UniversalBaseConfig(ABC):
    """
    Abstract base class for all research domain configurations.
    
    Provides common functionality and interface that all domain-specific
    configurations must implement. Ensures consistency across domains.
    """
    
    def __init__(self, research_domain: str):
        """
        Initialize base configuration.
        
        Args:
            research_domain: Research domain identifier (climate, physics, chemistry, etc.)
        """
        self.research_domain = research_domain
        self.domain_templates = {}
        self.validation_criteria_templates = {}
        self.calculation_templates = {}
        
        # Load domain-specific configuration
        self._load_domain_config()
        
        logger.info(f"✅ Universal base config loaded for domain: {research_domain}")
    
    def _load_domain_config(self):
        """Load domain-specific configuration."""
        # Load universal templates
        self._load_universal_templates()
        
        # Load domain-specific templates
        self._load_domain_specific_templates()
    
    def _load_universal_templates(self):
        """Load universal templates that work across all domains."""
        self.calculation_templates['statistical_analysis'] = {
            'description': 'Universal statistical analysis template',
            'python_template': '''
# Universal Statistical Analysis
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

def perform_statistical_analysis(data, analysis_type="descriptive"):
    """Universal statistical analysis for any research domain."""
    results = {{}}
    
    if analysis_type == "descriptive":
        results['mean'] = np.mean(data)
        results['std'] = np.std(data)
        results['median'] = np.median(data)
        results['min'] = np.min(data)
        results['max'] = np.max(data)
        
    elif analysis_type == "hypothesis_test":
        # Example t-test (can be adapted for domain needs)
        t_stat, p_value = stats.ttest_1samp(data, 0)
        results['t_statistic'] = t_stat
        results['p_value'] = p_value
        results['significant'] = p_value < 0.05
    
    return results

# Execute analysis
print("Executing universal statistical analysis...")
test_data = np.random.normal(0, 1, 100)  # Replace with real data
desc_results = perform_statistical_analysis(test_data, "descriptive")
print(f"Descriptive statistics: {{desc_results}}")

test_results = perform_statistical_analysis(test_data, "hypothesis_test")
print(f"Hypothesis test results: {{test_results}}")
''',
            'parameters': ['data', 'analysis_type'],
            'outputs': ['statistical_summary', 'test_results']
        }
        
        self.calculation_templates['data_visualization'] = {
            'description': 'Universal data visualization template',
            'python_template': '''
# Universal Data Visualization
import matplotlib.pyplot as plt
import numpy as np

def create_universal_plots(data, plot_type="timeseries", title="Universal Plot"):
    """Create universal plots for any research domain."""
    plt.figure(figsize=(10, 6))
    
    if plot_type == "timeseries":
        plt.plot(data)
        plt.title(f"{{title}} - Time Series")
        plt.xlabel("Time")
        plt.ylabel("Value")
        
    elif plot_type == "histogram":
        plt.hist(data, bins=30, alpha=0.7)
        plt.title(f"{{title}} - Distribution")
        plt.xlabel("Value")
        plt.ylabel("Frequency")
        
    elif plot_type == "scatter":
        # Assuming data is 2D for scatter plot
        if len(data.shape) > 1 and data.shape[1] >= 2:
            plt.scatter(data[:, 0], data[:, 1])
            plt.title(f"{{title}} - Scatter Plot")
            plt.xlabel("X Variable")
            plt.ylabel("Y Variable")
    
    plt.tight_layout()
    plt.savefig(f"universal_plot_{{plot_type}}.png", dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Plot saved: universal_plot_{{plot_type}}.png")

# Execute visualization
print("Creating universal visualizations...")
sample_data = np.random.normal(0, 1, 1000)
create_universal_plots(sample_data, "timeseries", "Sample Data Analysis")
create_universal_plots(sample_data, "histogram", "Sample Data Distribution")
''',
            'parameters': ['data', 'plot_type', 'title'],
            'outputs': ['plot_files']
        }
        
        self.validation_criteria_templates['universal'] = {
            'execution_success': {
                'description': 'Experiment executed without errors',
                'required': True
            },
            'no_errors': {
                'description': 'No errors in calculation outputs',
                'required': True
            },
            'files_generated': {
                'description': 'Required output files generated',
                'minimum': 1,
                'required': True
            },
            'calculation_completion': {
                'description': 'All calculations completed successfully',
                'required': True
            }
        }
    
    def _load_domain_specific_templates(self):
        """Load domain-specific templates. Climate domain specialized."""
        if self.research_domain == "climate":
            self._load_climate_templates()
        else:
            logger.warning(f"Domain {self.research_domain} not yet supported. Using climate domain as base.")
    
    def _load_climate_templates(self):
        """Load climate research specific templates."""
        self.calculation_templates['climate_analysis'] = {
            'description': 'Climate data analysis template',
            'python_template': '''
# Climate Data Analysis
import numpy as np
import xarray as xr

def analyze_climate_data(data_path=None, analysis_type="temperature_trend"):
    """Analyze climate data with domain-specific methods."""
    results = {{}}
    
    if analysis_type == "temperature_trend":
        # Simulate temperature trend analysis
        # In real implementation, load actual climate data
        years = np.arange(1980, 2024)
        temp_data = 15.0 + 0.02 * (years - 1980) + np.random.normal(0, 0.5, len(years))
        
        # Calculate trend
        trend_coeff = np.polyfit(years, temp_data, 1)[0]
        results['temperature_trend_per_year'] = trend_coeff
        results['total_warming'] = trend_coeff * len(years)
        
        print(f"Temperature trend: {{trend_coeff:.4f}} °C/year")
        print(f"Total warming over period: {{results['total_warming']:.2f}} °C")
        
    elif analysis_type == "aerosol_transport":
        # Simulate aerosol transport calculation
        print("Calculating aerosol transport patterns...")
        results['transport_efficiency'] = 0.85
        results['residence_time_days'] = 365 * 2  # 2 years typical for stratosphere
        results['global_coverage_percent'] = 75
        
    return results

# Execute climate analysis
print("Executing climate-specific analysis...")
climate_results = analyze_climate_data(analysis_type="temperature_trend")
aerosol_results = analyze_climate_data(analysis_type="aerosol_transport")
print(f"Climate analysis complete: {{climate_results}}")
print(f"Aerosol analysis complete: {{aerosol_results}}")
''',
            'parameters': ['data_path', 'analysis_type'],
            'outputs': ['climate_analysis_results']
        }
        
        # SAI-specific calculation template
        self.calculation_templates['sai_analysis'] = {
            'description': 'Stratospheric Aerosol Injection analysis template',
            'python_template': '''
# SAI Pulse vs Continuous Analysis
import numpy as np
import matplotlib.pyplot as plt

def sai_injection_analysis(injection_type="pulse"):
    """Analyze SAI injection strategies: pulse vs continuous using GeoMIP conventions."""
    results = {{}}
    
    # Simulation parameters
    time_years = np.linspace(0, 10, 121)  # 10 years, monthly resolution
    
    if injection_type == "pulse":
        # Pulse injection: large amounts at intervals
        injection_schedule = np.zeros_like(time_years)
        pulse_times = [0, 2, 4, 6, 8]  # Every 2 years
        pulse_amount = 5.0  # Mt SO2 equivalent
        
        for t in pulse_times:
            idx = np.argmin(np.abs(time_years - t))
            injection_schedule[idx] = pulse_amount
        
        # Atmospheric concentration with decay
        concentration = np.zeros_like(time_years)
        for i, inj in enumerate(injection_schedule):
            if inj > 0:
                # Add exponential decay from this injection
                decay_times = time_years[i:] - time_years[i]
                decay_profile = inj * np.exp(-decay_times / 1.5)  # 1.5 year decay
                concentration[i:] += decay_profile
        
        results['injection_type'] = 'pulse'
        results['total_injected'] = np.sum(injection_schedule)
        results['peak_concentration'] = np.max(concentration)
        results['average_concentration'] = np.mean(concentration)
        
    elif injection_type == "continuous":
        # Continuous injection: steady rate
        annual_injection = 2.5  # Mt SO2 per year
        monthly_injection = annual_injection / 12
        
        injection_schedule = np.full_like(time_years, monthly_injection)
        
        # Steady state concentration with continuous input and decay
        tau = 1.5  # years decay time constant
        steady_state_conc = monthly_injection * tau * 12  # equilibrium
        
        # Build up to steady state
        concentration = steady_state_conc * (1 - np.exp(-time_years / tau))
        
        results['injection_type'] = 'continuous'
        results['total_injected'] = np.sum(injection_schedule)
        results['peak_concentration'] = steady_state_conc
        results['average_concentration'] = np.mean(concentration)
    
    # Calculate climate effects (simplified)
    results['cooling_effect_K'] = results['average_concentration'] * 0.1  # K per concentration unit
    results['ozone_depletion_percent'] = results['average_concentration'] * 0.05
    
    # Economic and operational considerations
    if injection_type == "pulse":
        results['operational_complexity'] = 'high'
        results['aircraft_requirements'] = 'high_capacity_intermittent'
        results['cost_efficiency'] = 0.7
    else:
        results['operational_complexity'] = 'medium'
        results['aircraft_requirements'] = 'steady_continuous'
        results['cost_efficiency'] = 0.9
    
    # Create visualization
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    plt.plot(time_years, injection_schedule)
    plt.title(f'{{injection_type.title()}} Injection Schedule')
    plt.xlabel('Years')
    plt.ylabel('Injection Rate (Mt SO2/month)')
    
    plt.subplot(2, 2, 2)
    plt.plot(time_years, concentration)
    plt.title(f'Atmospheric Concentration - {{injection_type.title()}}')
    plt.xlabel('Years')
    plt.ylabel('Concentration (arbitrary units)')
    
    plt.subplot(2, 2, 3)
    cooling = concentration * 0.1
    plt.plot(time_years, cooling)
    plt.title(f'Climate Cooling Effect - {{injection_type.title()}}')
    plt.xlabel('Years')
    plt.ylabel('Cooling (K)')
    
    plt.subplot(2, 2, 4)
    ozone = concentration * 0.05
    plt.plot(time_years, ozone)
    plt.title(f'Ozone Depletion - {{injection_type.title()}}')
    plt.xlabel('Years')
    plt.ylabel('Ozone Loss (%)')
    
    plt.tight_layout()
    plt.savefig(f'sai_analysis_{{injection_type}}.png', dpi=150, bbox_inches='tight')
    print(f"SAI analysis plot saved: sai_analysis_{{injection_type}}.png")
    
    return results

# Execute SAI analysis for both strategies
print("Executing SAI pulse vs continuous analysis...")
pulse_results = sai_injection_analysis("pulse")
continuous_results = sai_injection_analysis("continuous")

print("\\n=== SAI PULSE INJECTION RESULTS ===")
for key, value in pulse_results.items():
    print(f"{{key}}: {{value}}")

print("\\n=== SAI CONTINUOUS INJECTION RESULTS ===")
for key, value in continuous_results.items():
    print(f"{{key}}: {{value}}")

# Comparison analysis
print("\\n=== COMPARATIVE ANALYSIS ===")
print(f"Efficiency comparison:")
print(f"  Pulse cooling per Mt injected: {{pulse_results['cooling_effect_K'] / pulse_results['total_injected']:.4f}} K/Mt")
print(f"  Continuous cooling per Mt injected: {{continuous_results['cooling_effect_K'] / continuous_results['total_injected']:.4f}} K/Mt")

print(f"Environmental impact comparison:")
print(f"  Pulse ozone depletion: {{pulse_results['ozone_depletion_percent']:.2f}}%")
print(f"  Continuous ozone depletion: {{continuous_results['ozone_depletion_percent']:.2f}}%")

print(f"Operational considerations:")
print(f"  Pulse operational complexity: {{pulse_results['operational_complexity']}}")
print(f"  Continuous operational complexity: {{continuous_results['operational_complexity']}}")
''',
            'parameters': ['injection_type'],
            'outputs': ['sai_analysis_results', 'comparison_plots']
        }
        
        # Climate validation criteria
        self.validation_criteria_templates['climate'] = {
            'temperature_range_check': {
                'description': 'Temperature values within realistic range',
                'min_value': -100,  # Celsius
                'max_value': 60,
                'required': True
            },
            'physical_consistency': {
                'description': 'Results consistent with physical laws',
                'required': True
            },
            'data_completeness': {
                'description': 'All required climate variables present',
                'required': True
            }
        }
    
    def _load_physics_templates(self):
        """Load physics research specific templates."""
        self.calculation_templates['physics_simulation'] = {
            'description': 'Physics simulation template',
            'python_template': '''
# Physics Simulation Template
import numpy as np
import scipy.integrate as integrate

def physics_simulation(simulation_type="kinematics"):
    """Universal physics simulation template."""
    results = {{}}
    
    if simulation_type == "kinematics":
        # Example: projectile motion
        g = 9.81  # m/s^2
        v0 = 50   # m/s initial velocity
        angle = 45 * np.pi / 180  # launch angle
        
        t_flight = 2 * v0 * np.sin(angle) / g
        max_range = v0**2 * np.sin(2*angle) / g
        max_height = (v0 * np.sin(angle))**2 / (2 * g)
        
        results['flight_time'] = t_flight
        results['max_range'] = max_range
        results['max_height'] = max_height
        
    return results

print("Executing physics simulation...")
physics_results = physics_simulation("kinematics")
print(f"Physics results: {{physics_results}}")
''',
            'parameters': ['simulation_type'],
            'outputs': ['physics_results']
        }
    
    def _load_chemistry_templates(self):
        """Load chemistry research specific templates."""
        self.calculation_templates['chemistry_analysis'] = {
            'description': 'Chemistry analysis template',
            'python_template': '''
# Chemistry Analysis Template
import numpy as np

def chemistry_analysis(analysis_type="reaction_kinetics"):
    """Universal chemistry analysis template."""
    results = {{}}
    
    if analysis_type == "reaction_kinetics":
        # Example: first-order reaction kinetics
        k = 0.1  # rate constant
        t = np.linspace(0, 50, 100)
        c0 = 1.0  # initial concentration
        
        concentration = c0 * np.exp(-k * t)
        half_life = np.log(2) / k
        
        results['rate_constant'] = k
        results['half_life'] = half_life
        results['final_concentration'] = concentration[-1]
        
    return results

print("Executing chemistry analysis...")
chem_results = chemistry_analysis("reaction_kinetics")
print(f"Chemistry results: {{chem_results}}")
''',
            'parameters': ['analysis_type'],
            'outputs': ['chemistry_results']
        }
    
    def _load_biology_templates(self):
        """Load biology research specific templates."""
        self.calculation_templates['biology_analysis'] = {
            'description': 'Biology analysis template',
            'python_template': '''
# Biology Analysis Template
import numpy as np

def biology_analysis(analysis_type="population_growth"):
    """Universal biology analysis template."""
    results = {{}}
    
    if analysis_type == "population_growth":
        # Example: exponential growth model
        r = 0.05  # growth rate
        K = 1000  # carrying capacity
        N0 = 10   # initial population
        t = np.linspace(0, 100, 100)
        
        # Logistic growth
        N = K / (1 + ((K - N0) / N0) * np.exp(-r * t))
        
        results['growth_rate'] = r
        results['carrying_capacity'] = K
        results['final_population'] = N[-1]
        results['doubling_time'] = np.log(2) / r
        
    return results

print("Executing biology analysis...")
bio_results = biology_analysis("population_growth")
print(f"Biology results: {{bio_results}}")
''',
            'parameters': ['analysis_type'],
            'outputs': ['biology_results']
        }
    
    def configure_experiment(self, experiment_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Configure experiment for the specific research domain.
        
        Args:
            experiment_config: Domain-specific experiment configuration
            
        Returns:
            Dict with domain-specific setup and templates
        """
        domain_setup = {
            'domain': self.research_domain,
            'available_templates': list(self.calculation_templates.keys()),
            'selected_templates': [],
            'domain_parameters': {},
            'calculation_sequence': []
        }
        
        # Analyze experiment requirements
        if 'calculations' in experiment_config:
            for calc_type in experiment_config['calculations']:
                if calc_type in self.calculation_templates:
                    domain_setup['selected_templates'].append(calc_type)
                else:
                    logger.warning(f"Unknown calculation type: {calc_type}")
        
        # Set domain-specific parameters
        if 'parameters' in experiment_config:
            domain_setup['domain_parameters'] = experiment_config['parameters']
        
        # Generate calculation sequence
        domain_setup['calculation_sequence'] = self._generate_calculation_sequence(
            domain_setup['selected_templates'], domain_setup['domain_parameters']
        )
        
        return domain_setup
    
    def generate_calculation_commands(self, experiment_config: Dict[str, Any]) -> List[Dict]:
        """
        Generate URSA calculation commands for the experiment.
        
        Args:
            experiment_config: Experiment configuration
            
        Returns:
            List of command dictionaries for URSA execution
        """
        commands = []
        
        # Add universal statistical analysis if requested
        if 'statistical_analysis' in experiment_config.get('calculations', []):
            commands.append({
                'type': 'calculation',
                'description': 'Universal statistical analysis',
                'python_code': self.calculation_templates['statistical_analysis']['python_template']
            })
        
        # Add universal visualization if requested
        if 'visualization' in experiment_config.get('calculations', []):
            commands.append({
                'type': 'calculation',
                'description': 'Universal data visualization',
                'python_code': self.calculation_templates['data_visualization']['python_template']
            })
        
        # Add domain-specific calculations
        for calc_type in experiment_config.get('calculations', []):
            if calc_type in self.calculation_templates and calc_type not in ['statistical_analysis', 'visualization']:
                commands.append({
                    'type': 'calculation',
                    'description': self.calculation_templates[calc_type]['description'],
                    'python_code': self.calculation_templates[calc_type]['python_template']
                })
        
        return commands
    
    def get_validation_criteria(self, experiment_config: Dict[str, Any]) -> Dict:
        """
        Get validation criteria for the experiment.
        
        Args:
            experiment_config: Experiment configuration
            
        Returns:
            Dict with validation criteria for the domain
        """
        # Start with universal criteria
        criteria = self.validation_criteria_templates['universal'].copy()
        
        # Add domain-specific criteria if available
        if self.research_domain in self.validation_criteria_templates:
            criteria.update(self.validation_criteria_templates[self.research_domain])
        
        return criteria
    
    def _generate_calculation_sequence(self, 
                                     selected_templates: List[str], 
                                     parameters: Dict) -> List[Dict]:
        """Generate sequence of calculations for execution."""
        sequence = []
        
        for template_name in selected_templates:
            if template_name in self.calculation_templates:
                template = self.calculation_templates[template_name]
                sequence.append({
                    'template_name': template_name,
                    'description': template['description'],
                    'parameters': template.get('parameters', []),
                    'expected_outputs': template.get('outputs', []),
                    'execution_order': len(sequence) + 1
                })
        
        return sequence