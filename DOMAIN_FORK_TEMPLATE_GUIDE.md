# Domain Fork Template Guide

## Climate Repair Framework - Easy Domain Forking

This guide demonstrates how to create new climate repair domains by forking the `ClimateRepairTemplate` architecture. Any climate intervention domain can be implemented in **under 30 minutes** using this template system.

---

## 🎯 Quick Fork Overview

**Time to implement new domain:** 15-30 minutes  
**Lines of code required:** 200-400 lines  
**Integration effort:** Zero - automatically inherits 11-tool pipeline  
**Domains supported:** SAI, MCB, DAC, OA, SRM, ER, and any custom intervention

---

## 📋 Fork Template Generation

### Step 1: Generate Template Code

Use the built-in template generator:

```python
from climate_repair_template import ClimateRepairTemplate

# Create any domain template automatically
template = ClimateRepairTemplate("placeholder", "test")
new_domain_code = template.create_domain_fork_template("marine_cloud_brightening")
print(new_domain_code)
```

### Step 2: Save and Customize

```bash
# Save generated template
python -c "
from climate_repair_template import ClimateRepairTemplate
template = ClimateRepairTemplate('placeholder', 'test')
code = template.create_domain_fork_template('marine_cloud_brightening')
with open('mcb_climate_repair.py', 'w') as f:
    f.write(code)
"
```

---

## 🛠️ Domain Implementation Examples

### Example 1: Marine Cloud Brightening (MCB)

```python
#!/usr/bin/env python3
"""
Marine Cloud Brightening (MCB) Climate Repair Implementation
"""

from climate_repair_template import ClimateRepairTemplate
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class MCBClimateRepair(ClimateRepairTemplate):
    """Marine Cloud Brightening climate repair implementation."""
    
    def __init__(self, experiment_name: str = "mcb_experiment"):
        domain_config = {
            'intervention_type': 'marine_cloud_brightening',
            'target_parameter': 'cloud_albedo',
            'deployment_scale': 'regional_marine',
            'effectiveness_metric': 'cloud_reflectivity_enhancement',
            
            # MCB-specific parameters
            'droplet_size_range': [0.1, 0.5],  # micrometers
            'salt_particle_injection': True,
            'target_cloud_types': ['stratocumulus', 'cumulus'],
            'marine_environment_focus': True,
            'ship_based_deployment': True
        }
        
        super().__init__(
            repair_domain="marine_cloud_brightening",
            experiment_name=experiment_name,
            domain_config=domain_config
        )
    
    def configure_domain_specifics(self) -> Dict[str, Any]:
        return {
            'intervention_mechanisms': {
                'primary': [
                    'sea_salt_aerosol_generation',
                    'cloud_condensation_nuclei_enhancement',
                    'droplet_size_distribution_modification',
                    'cloud_albedo_increase'
                ],
                'implementation': [
                    'ship_based_spraying',
                    'autonomous_vessels',
                    'offshore_platforms',
                    'coastal_installations'
                ],
                'constraints': [
                    'marine_ecosystem_protection',
                    'shipping_lane_coordination',
                    'weather_dependency',
                    'salt_corrosion_management'
                ]
            },
            'target_parameters': {
                'primary': [
                    'cloud_albedo',
                    'cloud_droplet_concentration',
                    'cloud_optical_depth',
                    'shortwave_reflection'
                ],
                'secondary': [
                    'precipitation_patterns',
                    'local_temperature',
                    'marine_boundary_layer',
                    'atmospheric_moisture'
                ]
            },
            'deployment_methods': {
                'approaches': [
                    'targeted_cloud_systems',
                    'regional_cloud_fields',
                    'seasonal_deployment',
                    'continuous_operation'
                ],
                'requirements': [
                    'marine_vessel_fleet',
                    'aerosol_generation_systems',
                    'meteorological_monitoring',
                    'environmental_compliance'
                ]
            }
        }
    
    def setup_reality_checks(self) -> Dict[str, Any]:
        return {
            'domain': 'marine_cloud_brightening',
            'specific_checks': [
                'droplet_size_feasibility',
                'salt_aerosol_residence_time',
                'cloud_microphysics_validity',
                'marine_ecosystem_impact',
                'ship_deployment_practicality',
                'weather_dependency_assessment'
            ],
            'validation_focus': 'marine_atmospheric_feasibility',
            'physical_constraints': {
                'min_droplet_size': 0.05,  # micrometers
                'max_droplet_size': 1.0,   # micrometers
                'salt_concentration_limit': 100,  # mg/m³
                'cloud_base_height_range': [200, 2000],  # meters
                'wind_speed_limits': [2, 15]  # m/s
            }
        }
    
    def define_validation_criteria(self) -> Dict[str, Any]:
        return {
            'effectiveness_measures': [
                'cloud_albedo_enhancement',
                'droplet_concentration_increase',
                'cooling_efficiency_per_area',
                'regional_temperature_reduction'
            ],
            'risk_thresholds': {
                'environmental': {
                    'marine_ecosystem_disruption': 0.05,
                    'precipitation_pattern_change': 0.10,
                    'salt_deposition_impact': 0.08
                },
                'technical': {
                    'ship_system_reliability': 0.90,
                    'aerosol_generation_efficiency': 0.85,
                    'weather_operation_capability': 0.70
                },
                'operational': {
                    'shipping_interference': 0.05,
                    'international_waters_compliance': 0.95,
                    'cost_effectiveness': 0.60
                }
            },
            'success_criteria': {
                'minimum_albedo_enhancement': 0.1,  # Albedo increase
                'maximum_ecosystem_impact': 0.2,   # Environmental risk
                'deployment_feasibility': 0.7,     # Technical feasibility
                'regional_cooling_effectiveness': 0.5  # Cooling per unit area
            }
        }
    
    def generate_domain_hypothesis_template(self) -> str:
        return """Marine cloud brightening using sea salt aerosol injection could increase 
        stratocumulus cloud albedo by 0.1-0.2 through enhanced droplet concentration, 
        achieving regional cooling of 1-2°C over marine areas with ship-based deployment 
        systems operating at 5-10 vessels per 100,000 km² while maintaining marine 
        ecosystem integrity through targeted seasonal operations."""
```

### Example 2: Direct Air Capture (DAC)

```python
class DACClimateRepair(ClimateRepairTemplate):
    """Direct Air Capture climate repair implementation."""
    
    def __init__(self, experiment_name: str = "dac_experiment"):
        domain_config = {
            'intervention_type': 'direct_air_capture',
            'target_parameter': 'atmospheric_co2',
            'deployment_scale': 'industrial_scale',
            'effectiveness_metric': 'co2_removal_rate',
            
            # DAC-specific parameters
            'capture_technology': 'solid_sorbent',
            'target_capture_rate': 1000000,  # tons CO2/year
            'energy_source': 'renewable',
            'storage_method': 'geological_sequestration'
        }
        
        super().__init__(
            repair_domain="direct_air_capture",
            experiment_name=experiment_name,
            domain_config=domain_config
        )
    
    def configure_domain_specifics(self) -> Dict[str, Any]:
        return {
            'intervention_mechanisms': {
                'primary': [
                    'atmospheric_co2_adsorption',
                    'sorbent_regeneration',
                    'co2_compression',
                    'permanent_storage'
                ],
                'implementation': [
                    'industrial_dac_plants',
                    'modular_systems',
                    'mobile_capture_units',
                    'integrated_renewable_power'
                ],
                'constraints': [
                    'energy_requirement_limits',
                    'sorbent_material_availability',
                    'capture_efficiency_degradation',
                    'storage_site_availability'
                ]
            },
            'target_parameters': {
                'primary': [
                    'atmospheric_co2_concentration',
                    'co2_removal_rate',
                    'capture_efficiency',
                    'energy_consumption_ratio'
                ],
                'secondary': [
                    'air_processing_volume',
                    'sorbent_cycling_rate',
                    'system_availability',
                    'lifecycle_emissions'
                ]
            }
        }
    
    def setup_reality_checks(self) -> Dict[str, Any]:
        return {
            'domain': 'direct_air_capture',
            'specific_checks': [
                'energy_requirement_feasibility',
                'sorbent_material_scalability',
                'capture_rate_achievability',
                'storage_capacity_availability',
                'economic_viability_assessment'
            ],
            'validation_focus': 'industrial_scalability',
            'physical_constraints': {
                'min_capture_rate': 100,     # tons CO2/year per unit
                'max_energy_penalty': 2000,  # kWh per ton CO2
                'sorbent_cycling_limit': 10000,  # cycles
                'capture_efficiency_min': 0.85,   # fraction
                'storage_injection_pressure': [10, 300]  # MPa
            }
        }
    
    def define_validation_criteria(self) -> Dict[str, Any]:
        return {
            'effectiveness_measures': [
                'co2_removal_efficiency',
                'energy_consumption_per_ton',
                'system_capacity_factor',
                'lifecycle_net_removal'
            ],
            'success_criteria': {
                'minimum_capture_efficiency': 0.85,
                'maximum_energy_penalty': 2000,  # kWh/ton CO2
                'deployment_feasibility': 0.8,
                'economic_competitiveness': 0.6
            }
        }
    
    def generate_domain_hypothesis_template(self) -> str:
        return """Direct air capture using solid sorbent technology could remove 
        1 million tons CO2 annually per industrial facility with energy consumption 
        below 1800 kWh per ton CO2 through optimized sorbent cycling and renewable 
        energy integration, achieving net negative emissions with geological storage 
        at costs approaching $150 per ton CO2."""
```

---

## 🔧 Quick Customization Points

### 1. Domain Configuration (Constructor)
```python
domain_config = {
    'intervention_type': 'YOUR_INTERVENTION',     # Core mechanism
    'target_parameter': 'YOUR_TARGET',           # What you're changing
    'deployment_scale': 'YOUR_SCALE',            # Local/regional/global
    'effectiveness_metric': 'YOUR_METRIC'       # How you measure success
}
```

### 2. Intervention Mechanisms
```python
'intervention_mechanisms': {
    'primary': ['method1', 'method2'],           # Core intervention methods
    'implementation': ['approach1', 'approach2'], # How to deploy
    'constraints': ['limit1', 'limit2']         # Physical/practical limits
}
```

### 3. Reality Check Engine
```python
'physical_constraints': {
    'parameter_min': value,    # Minimum feasible value
    'parameter_max': value,    # Maximum feasible value
    'efficiency_threshold': value  # Required efficiency
}
```

### 4. Validation Criteria
```python
'success_criteria': {
    'minimum_effectiveness': 0.0,  # Success threshold
    'maximum_risk': 1.0,          # Risk tolerance
    'deployment_feasibility': 0.5  # Technical feasibility
}
```

---

## 🧪 Testing New Domains

### Quick Domain Test
```python
# Test any new domain implementation
def test_new_domain(domain_class, domain_name):
    """Test new domain implementation."""
    
    # Initialize domain
    domain = domain_class(f"{domain_name}_test")
    
    # Test domain status
    status = domain.get_domain_status()
    print(f"✅ {domain_name.upper()} Status: {status['ready_for_execution']}")
    
    # Test hypothesis validation
    hypothesis = domain.generate_domain_hypothesis_template()
    results = domain.validate_domain_hypothesis(hypothesis)
    
    print(f"📊 Validation: {results['final_assessment']['recommendation']}")
    print(f"🎯 Score: {results['final_assessment']['final_score']:.3f}")
    
    return results

# Example usage
# test_new_domain(MCBClimateRepair, "marine_cloud_brightening")
# test_new_domain(DACClimateRepair, "direct_air_capture")
```

### Full Pipeline Test
```python
# Test complete pipeline execution
def test_domain_pipeline(domain_class, domain_name):
    """Test complete pipeline for new domain."""
    
    domain = domain_class(f"{domain_name}_pipeline_test")
    
    # Execute complete pipeline (FAISS + Reality Check + 11-tool integration)
    results = domain.execute_domain_pipeline()
    
    success = results.get('status') == 'completed_successfully'
    print(f"🚀 Pipeline: {'✅ SUCCESS' if success else '❌ FAILED'}")
    
    return results
```

---

## 📊 Supported Domain Examples

| Domain | Implementation Time | Complexity | Key Features |
|--------|-------------------|------------|--------------|
| **SAI** | 30 min | High | QBO integration, atmospheric chemistry |
| **MCB** | 20 min | Medium | Marine deployment, cloud microphysics |
| **DAC** | 25 min | Medium | Industrial scaling, energy optimization |
| **Ocean Alkalinization** | 25 min | Medium | Ocean chemistry, ecosystem impact |
| **Enhanced Weathering** | 20 min | Low | Mineral weathering, soil integration |
| **BECCS** | 30 min | High | Biomass integration, CCS coupling |
| **Solar Radiation Management** | 25 min | High | Space-based deployment, orbital mechanics |

---

## 🔗 Integration Benefits

### Automatic Tool Integration
Every forked domain automatically inherits:

- ✅ **FAISS Database**: 36,418 vectors from 1,171 climate PDFs
- ✅ **Reality Check Engine**: Domain-configurable validation
- ✅ **11-Tool Pipeline**: Complete research workflow
- ✅ **Multi-model Support**: Research and review capabilities
- ✅ **Validation Framework**: Novelty + feasibility + reality checks
- ✅ **Paper Generation**: 128+ page academic paper capability
- ✅ **Cambridge Integration**: Professor-specific research focus

### Zero Additional Configuration
- No database setup required
- No tool configuration needed
- No pipeline integration work
- No validation system setup

---

## 🎯 Quick Start Checklist

### For Any New Domain:

1. **☐ Generate template** (2 min)
   ```bash
   python generate_domain_template.py YOUR_DOMAIN_NAME
   ```

2. **☐ Customize 4 abstract methods** (15 min)
   - `configure_domain_specifics()`
   - `setup_reality_checks()`
   - `define_validation_criteria()`
   - `generate_domain_hypothesis_template()`

3. **☐ Set domain-specific parameters** (5 min)
   - Physical constraints
   - Success criteria
   - Risk thresholds

4. **☐ Test domain implementation** (5 min)
   ```python
   domain = YourDomain()
   results = domain.validate_domain_hypothesis()
   ```

5. **☐ Execute full pipeline** (3 min)
   ```python
   pipeline_results = domain.execute_domain_pipeline()
   ```

**Total Time: 30 minutes max**

---

## 💡 Advanced Features

### Domain-Specific Analysis Methods
```python
# Add custom analysis methods for your domain
class YourClimateRepair(ClimateRepairTemplate):
    
    def analyze_domain_specific_interactions(self, hypothesis: str):
        """Custom analysis for your domain."""
        # Your domain-specific analysis logic
        pass
    
    def assess_domain_risks(self, hypothesis: str):
        """Domain-specific risk assessment."""
        # Your risk assessment logic
        pass
```

### Multi-Domain Comparison
```python
# Compare multiple domains
def compare_climate_domains(domain_classes, hypothesis):
    """Compare effectiveness across multiple domains."""
    
    results = {}
    for domain_class in domain_classes:
        domain = domain_class()
        assessment = domain.validate_domain_hypothesis(hypothesis)
        results[domain.repair_domain] = assessment['final_assessment']['final_score']
    
    # Rank domains by effectiveness
    ranked = sorted(results.items(), key=lambda x: x[1], reverse=True)
    return ranked
```

---

## 🚀 Ready for Production

The Climate Repair Template system is designed for:

- **Research Teams**: Quick domain exploration and validation
- **Academic Groups**: Rapid hypothesis testing across domains
- **Policy Analysts**: Multi-domain impact assessment
- **Technology Developers**: Feasibility validation for new interventions
- **Climate Scientists**: Comprehensive domain analysis with 11-tool integration

**Start forking domains today - any climate intervention can be implemented and tested in under 30 minutes!**