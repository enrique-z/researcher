"""
Universal Research Configuration System
Generic framework for any research topic using Pipeline 2 infrastructure

This replaces topic-specific configurations with a flexible system that can
handle hundreds of different research topics, from climate science to any
academic domain requiring empirical validation and real data analysis.
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union
import logging
from datetime import datetime
from dataclasses import dataclass

# Add Pipeline 2 to path
PIPELINE_2_PATH = "/Users/apple/code/Researcher/PIPELINE_2_DEVELOPMENT"
sys.path.append(PIPELINE_2_PATH)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ResearchTopic:
    """Generic research topic specification."""
    title: str
    research_question: str
    domain: str  # e.g., 'climate_science', 'materials', 'biology', 'physics'
    methodology: str
    data_requirements: List[str]
    validation_criteria: Dict[str, Any]
    quality_target: float = 7.0
    expected_length: str = "128_pages"


class UniversalResearchConfiguration:
    """
    Universal configuration system for any research topic.
    
    Provides flexible framework that adapts Pipeline 2 infrastructure
    to any research domain while maintaining quality and validation standards.
    """
    
    def __init__(self, research_topic: ResearchTopic):
        """
        Initialize universal research configuration.
        
        Args:
            research_topic: Specification of the research topic to analyze
        """
        self.research_topic = research_topic
        self.config_id = f"research_{int(datetime.now().timestamp())}"
        
        # Universal Pipeline 2 component configuration
        self.universal_config = {
            'data_validation': {
                'real_data_mandatory': True,
                'synthetic_data_forbidden': True,
                'institutional_verification': True
            },
            
            'empirical_validation': {
                'strict_mode': True,
                'minimum_snr_threshold_db': 0.0,
                'undetectable_limit_db': -15.54,  # Universal Hangzhou threshold
                'required_confidence_level': 0.95,
                'minimum_sample_size': 20
            },
            
            'quality_standards': {
                'academic_rigor': 'publication_ready',
                'empirical_grounding': 'mandatory',
                'statistical_significance': 'required',
                'peer_review_ready': True
            },
            
            'output_specifications': {
                'format': 'academic_paper',
                'length_target': research_topic.expected_length,
                'quality_score_target': research_topic.quality_target,
                'citation_style': 'academic_standard'
            }
        }
        
        # Domain-specific adaptations
        self.domain_adaptations = self._configure_domain_adaptations()
        
        # Workflow stages (universal)
        self.workflow_stages = [
            'research_question_analysis',
            'hypothesis_generation',
            'data_requirement_identification',
            'data_loading_and_validation',
            'domain_specific_analysis',
            'empirical_validation',
            'anti_hallucination_check',
            'quality_assessment',
            'gemini_review_preparation',  # User manual step
            'final_synthesis'
        ]
        
        logger.info(f"✅ Universal Research Configuration initialized")
        logger.info(f"Topic: {research_topic.title}")
        logger.info(f"Domain: {research_topic.domain}")
    
    def _configure_domain_adaptations(self) -> Dict[str, Any]:
        """
        Configure domain-specific adaptations based on research topic.
        
        Returns domain-specific settings while maintaining universal framework.
        """
        domain = self.research_topic.domain.lower()
        
        # Universal domain configurations
        domain_configs = {
            'climate_science': {
                'data_sources': ['GLENS', 'ARISE-SAI', 'GeoMIP', 'CMIP6'],
                'validation_domains': ['climate_response', 'chemical_composition', 'radiative_forcing'],
                'analysis_variables': {
                    'temperature': ['TREFHT', 'tas'],
                    'precipitation': ['PRECT', 'pr'],
                    'clouds': ['CLDTOT', 'clt'],
                    'aerosols': ['BURDEN1', 'od550aer']
                },
                'specialized_validators': ['climate_response', 'atmospheric_transport']
            },
            
            'materials_science': {
                'data_sources': ['Materials_Project', 'ICSD', 'experimental_databases'],
                'validation_domains': ['crystal_structure', 'mechanical_properties', 'electronic_properties'],
                'analysis_variables': {
                    'structure': ['lattice_parameters', 'space_group', 'atomic_positions'],
                    'properties': ['band_gap', 'formation_energy', 'elastic_moduli'],
                    'stability': ['phonon_frequencies', 'thermodynamic_stability']
                },
                'specialized_validators': ['crystal_structure', 'property_prediction']
            },
            
            'biology': {
                'data_sources': ['GenBank', 'UniProt', 'PDB', 'experimental_data'],
                'validation_domains': ['sequence_analysis', 'structure_function', 'evolutionary_analysis'],
                'analysis_variables': {
                    'sequence': ['DNA', 'RNA', 'protein'],
                    'structure': ['secondary_structure', 'tertiary_structure', 'quaternary_structure'],
                    'function': ['enzymatic_activity', 'binding_affinity', 'regulatory_function']
                },
                'specialized_validators': ['sequence_validation', 'structure_validation']
            },
            
            'physics': {
                'data_sources': ['experimental_data', 'simulation_results', 'theoretical_predictions'],
                'validation_domains': ['theoretical_consistency', 'experimental_validation', 'numerical_accuracy'],
                'analysis_variables': {
                    'fundamental': ['energy', 'momentum', 'angular_momentum'],
                    'fields': ['electromagnetic', 'gravitational', 'nuclear'],
                    'particles': ['fermions', 'bosons', 'composite_particles']
                },
                'specialized_validators': ['theoretical_physics', 'experimental_physics']
            },
            
            'chemistry': {
                'data_sources': ['chemical_databases', 'experimental_data', 'quantum_calculations'],
                'validation_domains': ['molecular_structure', 'reaction_mechanisms', 'thermodynamics'],
                'analysis_variables': {
                    'structure': ['molecular_geometry', 'electronic_structure', 'conformations'],
                    'energetics': ['enthalpy', 'entropy', 'free_energy'],
                    'kinetics': ['activation_energy', 'reaction_rates', 'catalysis']
                },
                'specialized_validators': ['molecular_validation', 'reaction_validation']
            },
            
            'generic': {
                'data_sources': ['published_literature', 'experimental_data', 'databases'],
                'validation_domains': ['empirical_validation', 'statistical_analysis', 'methodological_rigor'],
                'analysis_variables': {
                    'quantitative': ['measurements', 'statistics', 'correlations'],
                    'qualitative': ['observations', 'classifications', 'patterns'],
                    'theoretical': ['models', 'hypotheses', 'predictions']
                },
                'specialized_validators': ['generic_empirical', 'statistical_validation']
            }
        }
        
        # Return domain-specific config or generic fallback
        return domain_configs.get(domain, domain_configs['generic'])
    
    def generate_universal_analysis_framework(self) -> Dict[str, Any]:
        """
        Generate universal analysis framework for any research topic.
        
        Returns comprehensive framework that adapts to any research domain
        while maintaining Pipeline 2 quality and validation standards.
        """
        framework = {
            'research_specification': {
                'title': self.research_topic.title,
                'research_question': self.research_topic.research_question,
                'domain': self.research_topic.domain,
                'methodology': self.research_topic.methodology,
                'quality_target': self.research_topic.quality_target
            },
            
            'data_requirements': {
                'required_datasets': self.research_topic.data_requirements,
                'domain_data_sources': self.domain_adaptations['data_sources'],
                'validation_requirements': {
                    'real_data_mandatory': True,
                    'synthetic_data_forbidden': True,
                    'institutional_verification': True,
                    'provenance_tracking': True
                }
            },
            
            'analysis_methodology': {
                'domain_specific_analysis': self.domain_adaptations['analysis_variables'],
                'validation_domains': self.domain_adaptations['validation_domains'],
                'specialized_validators': self.domain_adaptations['specialized_validators'],
                'universal_validation': {
                    'empirical_grounding': 'mandatory',
                    'statistical_significance': 'required',
                    'anti_hallucination': 'comprehensive',
                    'quality_control': 'strict'
                }
            },
            
            'pipeline2_integration': {
                'glens_loader': 'if_climate_science',
                'sakana_bridge': 'universal_real_data_validation',
                'empirical_validation': 'universal_framework',
                'oxford_bridge': 'literature_search_and_novelty',
                'ursa_integration': 'multi_agent_research_when_available',
                'gemini_quality_control': 'manual_expert_review'
            },
            
            'workflow_execution': {
                'stage_1_preparation': {
                    'research_question_decomposition': 'break_into_testable_hypotheses',
                    'data_requirement_identification': 'specify_exact_datasets_needed',
                    'methodology_specification': 'define_analysis_approach'
                },
                'stage_2_data_validation': {
                    'data_authenticity_verification': 'sakana_bridge_validation',
                    'empirical_grounding_check': 'ensure_real_data_availability',
                    'institutional_verification': 'confirm_data_provenance'
                },
                'stage_3_analysis': {
                    'domain_specific_analysis': 'apply_specialized_methods',
                    'statistical_validation': 'ensure_significance_and_power',
                    'cross_validation': 'verify_results_across_methods'
                },
                'stage_4_validation': {
                    'empirical_validation': 'comprehensive_reality_check',
                    'anti_hallucination': 'prevent_synthetic_contamination',
                    'quality_assessment': 'verify_academic_standards'
                },
                'stage_5_synthesis': {
                    'result_integration': 'synthesize_findings',
                    'uncertainty_quantification': 'assess_limitations',
                    'recommendation_generation': 'evidence_based_conclusions'
                }
            },
            
            'quality_assurance': {
                'validation_checkpoints': [
                    'data_authenticity_verified',
                    'empirical_grounding_confirmed',
                    'statistical_significance_achieved',
                    'domain_expertise_validated',
                    'anti_hallucination_passed',
                    'quality_score_target_met'
                ],
                'manual_review_preparation': {
                    'gemini_package': 'comprehensive_review_materials',
                    'expert_questions': 'domain_specific_validation_queries',
                    'quality_checklist': 'academic_publication_standards'
                }
            },
            
            'output_specifications': {
                'format': self.universal_config['output_specifications']['format'],
                'length': self.universal_config['output_specifications']['length_target'],
                'quality_target': self.universal_config['output_specifications']['quality_score_target'],
                'structure': [
                    'executive_summary',
                    'research_question_and_context',
                    'methodology_and_data',
                    'domain_specific_analysis',
                    'results_and_findings',
                    'validation_and_verification',
                    'discussion_and_implications',
                    'limitations_and_uncertainties',
                    'conclusions_and_recommendations',
                    'references_and_appendices'
                ]
            }
        }
        
        return framework
    
    def prepare_pipeline2_execution(self) -> Dict[str, Any]:
        """
        Prepare Pipeline 2 for execution with current research topic.
        
        Returns specific configuration for Pipeline 2 components
        adapted to the current research domain and question.
        """
        execution_config = {
            'component_configuration': {
                'data_loader': {
                    'type': 'domain_adaptive',
                    'real_data_mandatory': True,
                    'data_sources': self.domain_adaptations['data_sources'],
                    'validation_level': 'strict'
                },
                'sakana_bridge': {
                    'validation_mode': 'universal',
                    'real_data_enforcement': True,
                    'synthetic_data_blocking': True,
                    'domain_adaptation': self.research_topic.domain
                },
                'validation_framework': {
                    'domain_validators': self.domain_adaptations['specialized_validators'],
                    'universal_validation': True,
                    'quality_threshold': self.research_topic.quality_target,
                    'empirical_requirements': 'mandatory'
                },
                'oxford_bridge': {
                    'literature_search': True,
                    'novelty_detection': True,
                    'domain_specific': self.research_topic.domain
                }
            },
            
            'execution_parameters': {
                'research_topic': self.research_topic,
                'domain_adaptations': self.domain_adaptations,
                'universal_config': self.universal_config,
                'workflow_stages': self.workflow_stages
            },
            
            'quality_control': {
                'automated_validation': 'comprehensive',
                'manual_review_required': True,
                'gemini_integration': 'manual_expert_process',
                'final_verification': 'academic_publication_standards'
            }
        }
        
        return execution_config
    
    def create_research_topic_from_question(self, research_question: str, 
                                          domain: str = "generic") -> 'ResearchTopic':
        """
        Create ResearchTopic from simple research question.
        
        Args:
            research_question: The research question to analyze
            domain: Research domain (climate_science, materials, biology, etc.)
            
        Returns:
            Configured ResearchTopic object
        """
        # Extract title from research question
        title = research_question.split('?')[0].strip()
        if len(title) > 80:
            title = title[:77] + "..."
        
        # Determine data requirements based on domain
        domain_data_map = {
            'climate_science': ['climate_models', 'observational_data', 'reanalysis'],
            'materials': ['experimental_data', 'computational_results', 'databases'],
            'biology': ['sequence_data', 'experimental_results', 'literature'],
            'physics': ['experimental_data', 'theoretical_calculations', 'simulations'],
            'chemistry': ['experimental_data', 'quantum_calculations', 'databases'],
            'generic': ['published_literature', 'experimental_data', 'databases']
        }
        
        data_requirements = domain_data_map.get(domain.lower(), domain_data_map['generic'])
        
        return ResearchTopic(
            title=title,
            research_question=research_question,
            domain=domain,
            methodology="Pipeline 2 enhanced validation with empirical verification",
            data_requirements=data_requirements,
            validation_criteria={'empirical_grounding': True, 'real_data': True},
            quality_target=7.0,
            expected_length="128_pages"
        )


def main():
    """
    Demonstrate universal research configuration system.
    """
    print("🔬 Universal Research Configuration System")
    print("=" * 60)
    
    # Example 1: Climate Science (SAI question)
    sai_topic = ResearchTopic(
        title="SAI Injection Strategy Analysis",
        research_question="What are the potential pros and cons of injecting materials for stratospheric aerosol injection (SAI) in a pulsed fashion versus a continuous flow?",
        domain="climate_science",
        methodology="Pipeline 2 climate data analysis",
        data_requirements=["GLENS", "ARISE-SAI", "GeoMIP"],
        validation_criteria={'snr_threshold': 0.0, 'real_data': True}
    )
    
    # Example 2: Materials Science
    materials_topic = ResearchTopic(
        title="High-Entropy Alloy Properties",
        research_question="How do compositional variations affect the mechanical properties of high-entropy alloys?",
        domain="materials_science",
        methodology="Pipeline 2 materials data analysis",
        data_requirements=["Materials_Project", "experimental_data"],
        validation_criteria={'property_validation': True, 'real_data': True}
    )
    
    # Example 3: Generic topic
    generic_topic = ResearchTopic(
        title="Generic Research Analysis",
        research_question="What factors influence the effectiveness of intervention X in system Y?",
        domain="generic",
        methodology="Pipeline 2 empirical validation",
        data_requirements=["experimental_data", "literature"],
        validation_criteria={'empirical_grounding': True, 'real_data': True}
    )
    
    # Test universal configuration
    for i, topic in enumerate([sai_topic, materials_topic, generic_topic], 1):
        print(f"\n📋 Example {i}: {topic.domain.title()}")
        print(f"   Question: {topic.research_question}")
        
        config = UniversalResearchConfiguration(topic)
        framework = config.generate_universal_analysis_framework()
        execution_config = config.prepare_pipeline2_execution()
        
        print(f"   Domain Adaptations: {len(config.domain_adaptations)}")
        print(f"   Workflow Stages: {len(config.workflow_stages)}")
        print(f"   Quality Target: {topic.quality_target}")
    
    print(f"\n✅ Universal system ready for hundreds of research topics")
    print(f"   Simply provide: research_question + domain → full Pipeline 2 analysis")
    
    return config, framework


if __name__ == "__main__":
    config, framework = main()