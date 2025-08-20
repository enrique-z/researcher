"""
Pipeline Configuration for Researcher + Sakana Integration

Defines the three pipeline flow options and provides configuration
for the recommended Pre-Validation Gateway approach.
"""

from typing import Dict, List, Union, Optional
from dataclasses import dataclass
from enum import Enum


class PipelineMode(Enum):
    """Pipeline execution modes based on strategic analysis."""
    SEQUENTIAL = "sequential"           # Researcher → Sakana validation
    PARALLEL = "parallel"              # Researcher + Sakana simultaneously  
    PRE_VALIDATION = "pre_validation"  # Sakana → Researcher (RECOMMENDED)


@dataclass
class PipelineConfig:
    """Configuration for the integration pipeline."""
    
    # Pipeline flow configuration
    mode: PipelineMode = PipelineMode.PRE_VALIDATION
    enable_pre_screening: bool = True
    max_correction_cycles: int = 3
    strict_validation: bool = True
    
    # Data paths
    glens_data_path: str = "/path/to/glens/data"
    output_path: str = "/path/to/output"
    
    # Validation thresholds (from Sakana Principle)
    snr_undetectable_limit: float = -15.54  # Critical threshold from Hangzhou case
    snr_minimum_threshold: float = 0.0      # Minimum detectable
    required_confidence_level: float = 0.95  # Statistical significance
    minimum_ensemble_size: int = 20          # GLENS standard
    
    # Quality control
    enable_synthetic_detection: bool = True
    enable_plausibility_checking: bool = True
    require_institutional_validation: bool = True
    
    # Performance optimization
    enable_mac_m3_optimization: bool = True
    chunk_size_gb: float = 1.0
    parallel_processing: bool = True
    
    # Researcher integration
    researcher_api_endpoint: Optional[str] = None
    researcher_timeout: int = 300  # 5 minutes for 128-page generation
    researcher_model_size: str = "12B"
    
    # Output configuration
    generate_validation_reports: bool = True
    save_intermediate_results: bool = True
    export_metrics: bool = True


# Predefined configuration templates

DEVELOPMENT_CONFIG = PipelineConfig(
    mode=PipelineMode.PRE_VALIDATION,
    enable_pre_screening=True,
    strict_validation=False,  # More lenient for development
    max_correction_cycles=5,
    enable_synthetic_detection=True,
    save_intermediate_results=True
)

PRODUCTION_CONFIG = PipelineConfig(
    mode=PipelineMode.PRE_VALIDATION,
    enable_pre_screening=True,
    strict_validation=True,
    max_correction_cycles=3,
    enable_synthetic_detection=True,
    require_institutional_validation=True,
    save_intermediate_results=False  # For performance
)

RESEARCH_CONFIG = PipelineConfig(
    mode=PipelineMode.PARALLEL,  # For comparison studies
    enable_pre_screening=True,
    strict_validation=True,
    max_correction_cycles=3,
    generate_validation_reports=True,
    export_metrics=True
)

# Pipeline flow definitions based on your strategic question

PIPELINE_FLOWS = {
    "sequential": {
        "description": "Researcher → Sakana Validation",
        "pros": ["Full eloquent paper generated first", "Simple linear flow"],
        "cons": ["Wasted effort if validation fails", "Matches your current manual correction problem"],
        "recommended": False,
        "flow": [
            "1. Generate 128-page paper with Researcher",
            "2. Send paper to Sakana for validation", 
            "3. Manual corrections if validation fails",
            "4. Repeat until validation passes"
        ]
    },
    
    "parallel": {
        "description": "Researcher + Sakana Simultaneously",
        "pros": ["No wasted effort", "Faster processing", "Independent validation"],
        "cons": ["Complex result merging", "Potential conflicts between outputs"],
        "recommended": False,
        "flow": [
            "1. Send experiment to both Researcher and Sakana",
            "2. Researcher generates eloquent paper",
            "3. Sakana performs empirical validation",
            "4. Merge results with conflict resolution"
        ]
    },
    
    "pre_validation": {
        "description": "Sakana Pre-Screening → Researcher",
        "pros": ["Prevents wasted effort", "Automates your manual corrections", "High efficiency"],
        "cons": ["Requires upfront validation investment"],
        "recommended": True,
        "flow": [
            "1. Sakana pre-validates experiment proposal",
            "2. Apply automated corrections if needed",
            "3. ONLY send validated experiments to Researcher", 
            "4. Generate enhanced paper with validation context",
            "5. Final quality assurance check"
        ]
    }
}


def get_recommended_config(use_case: str = "production") -> PipelineConfig:
    """
    Get recommended configuration based on use case.
    
    Args:
        use_case: One of 'development', 'production', 'research'
        
    Returns:
        Configured PipelineConfig instance
    """
    config_map = {
        "development": DEVELOPMENT_CONFIG,
        "production": PRODUCTION_CONFIG,
        "research": RESEARCH_CONFIG
    }
    
    return config_map.get(use_case, PRODUCTION_CONFIG)


def validate_config(config: PipelineConfig) -> Dict[str, List[str]]:
    """
    Validate pipeline configuration for common issues.
    
    Returns:
        Dict containing validation results and warnings
    """
    validation_result = {
        "errors": [],
        "warnings": [],
        "recommendations": []
    }
    
    # Check critical thresholds
    if config.snr_undetectable_limit > -15.54:
        validation_result["errors"].append(
            f"SNR undetectable limit ({config.snr_undetectable_limit}) must be <= -15.54 dB"
        )
    
    if config.minimum_ensemble_size < 10:
        validation_result["warnings"].append(
            f"Ensemble size ({config.minimum_ensemble_size}) below recommended minimum of 20"
        )
    
    # Check mode-specific settings
    if config.mode == PipelineMode.PRE_VALIDATION and not config.enable_pre_screening:
        validation_result["errors"].append(
            "Pre-validation mode requires enable_pre_screening=True"
        )
    
    # Performance recommendations
    if config.enable_mac_m3_optimization and config.chunk_size_gb > 2.0:
        validation_result["recommendations"].append(
            "Consider reducing chunk_size_gb to 1.0 for Mac M3 64GB systems"
        )
    
    return validation_result


# Example usage configurations for your specific scenario

YOUR_CURRENT_WORKFLOW_CONFIG = PipelineConfig(
    mode=PipelineMode.SEQUENTIAL,  # This matches your current manual process
    enable_pre_screening=False,
    strict_validation=True,
    max_correction_cycles=999,  # Unlimited manual corrections (your current pain point)
    glens_data_path="/Users/apple/code/ai-s-plus/data/glens",
    researcher_timeout=600  # 10 minutes for complex papers
)

RECOMMENDED_IMPROVED_CONFIG = PipelineConfig(
    mode=PipelineMode.PRE_VALIDATION,  # Pre-screening gateway
    enable_pre_screening=True,
    strict_validation=True,
    max_correction_cycles=3,  # Automated correction cycles
    enable_synthetic_detection=True,  # Automates your forensic detection
    require_institutional_validation=True,
    glens_data_path="/Users/apple/code/ai-s-plus/data/glens",
    save_intermediate_results=True  # For debugging automated corrections
)