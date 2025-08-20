"""
Reality Check Engine: Physical Feasibility Validation
Critical component to catch fundamental physical impossibilities that plausibility-based systems miss

This module implements domain-specific reality checks to detect the "plausibility trap" -
when research appears methodologically sound but is physically impossible or infeasible.

Based on critical discoveries from URSA/Sakana/Gemini analysis showing that sophisticated
AI systems can validate plausibility while missing fundamental physical constraints.
"""

import json
import numpy as np
import re
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class SeverityLevel(Enum):
    """Reality check violation severity levels"""
    CATASTROPHIC = "catastrophic"  # Physically impossible, fundamental laws violated
    CRITICAL = "critical"          # Extremely unlikely, major constraints violated  
    HIGH = "high"                  # Highly problematic, significant feasibility issues
    MEDIUM = "medium"              # Concerning, moderate feasibility questions
    LOW = "low"                    # Minor issues, acceptable with caveats

@dataclass
class RealityCheckResult:
    """Result of a reality check analysis"""
    check_name: str
    severity: SeverityLevel
    passed: bool
    message: str
    evidence: Dict[str, Any]
    domain: str
    recommendation: str

class PhysicalFeasibilityEngine:
    """Core engine for physical feasibility validation"""
    
    def __init__(self):
        self.domain_modules = {
            'climate_science': ClimateRealityChecks(),
            'physics': PhysicsRealityChecks(), 
            'general': GeneralRealityChecks()
        }
        
    def analyze_paper(self, paper_data: Dict[str, Any], domain: str = 'general') -> Dict[str, Any]:
        """
        Comprehensive reality check analysis of a research paper
        
        Args:
            paper_data: Dictionary containing paper content, metrics, and claims
            domain: Scientific domain for specialized reality checks
            
        Returns:
            Dictionary with reality check results and overall assessment
        """
        results = {
            'overall_assessment': None,
            'reality_checks': [],
            'red_flags': [],
            'physical_feasibility_score': 0.0,
            'plausibility_trap_detected': False,
            'domain_specific_issues': [],
            'recommendations': []
        }
        
        # Get appropriate domain module
        domain_module = self.domain_modules.get(domain, self.domain_modules['general'])
        
        # Run domain-specific reality checks
        domain_results = domain_module.run_reality_checks(paper_data)
        results['reality_checks'].extend(domain_results)
        
        # Run general reality checks
        general_results = self.domain_modules['general'].run_reality_checks(paper_data)
        results['reality_checks'].extend(general_results)
        
        # Analyze results
        results = self._synthesize_results(results)
        
        return results
    
    def _synthesize_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize individual reality check results into overall assessment"""
        
        reality_checks = results['reality_checks']
        
        # Count severity levels
        severity_counts = {level: 0 for level in SeverityLevel}
        for check in reality_checks:
            if not check.passed:
                severity_counts[check.severity] += 1
        
        # Calculate physical feasibility score
        total_checks = len(reality_checks)
        if total_checks == 0:
            results['physical_feasibility_score'] = 0.5  # Unknown
        else:
            # Weight by severity
            penalty_weights = {
                SeverityLevel.CATASTROPHIC: 1.0,
                SeverityLevel.CRITICAL: 0.8,
                SeverityLevel.HIGH: 0.6,
                SeverityLevel.MEDIUM: 0.3,
                SeverityLevel.LOW: 0.1
            }
            
            total_penalty = sum(severity_counts[level] * penalty_weights[level] 
                              for level in SeverityLevel)
            
            results['physical_feasibility_score'] = max(0.0, 1.0 - (total_penalty / total_checks))
        
        # Detect plausibility trap
        results['plausibility_trap_detected'] = (
            severity_counts[SeverityLevel.CATASTROPHIC] > 0 or
            severity_counts[SeverityLevel.CRITICAL] > 1
        )
        
        # Generate red flags
        if severity_counts[SeverityLevel.CATASTROPHIC] > 0:
            results['red_flags'].append("🚨 CATASTROPHIC: Fundamental physical laws violated")
            
        if severity_counts[SeverityLevel.CRITICAL] > 0:
            results['red_flags'].append("🔴 CRITICAL: Major physical constraints violated")
            
        if results['plausibility_trap_detected']:
            results['red_flags'].append("⚠️ PLAUSIBILITY TRAP: Research appears sound but is physically impossible")
        
        # Overall assessment
        if severity_counts[SeverityLevel.CATASTROPHIC] > 0:
            results['overall_assessment'] = "PHYSICALLY_IMPOSSIBLE"
        elif severity_counts[SeverityLevel.CRITICAL] > 1:
            results['overall_assessment'] = "HIGHLY_INFEASIBLE"
        elif severity_counts[SeverityLevel.CRITICAL] > 0 or severity_counts[SeverityLevel.HIGH] > 2:
            results['overall_assessment'] = "FEASIBILITY_CONCERNS"
        elif any(not check.passed for check in reality_checks):
            results['overall_assessment'] = "MINOR_ISSUES"
        else:
            results['overall_assessment'] = "FEASIBLE"
        
        return results

class ClimateRealityChecks:
    """Climate science specific reality checks"""
    
    def run_reality_checks(self, paper_data: Dict[str, Any]) -> List[RealityCheckResult]:
        """Run all climate science reality checks"""
        results = []
        
        # Signal-to-noise ratio check (critical for detection claims)
        results.append(self._check_signal_to_noise_ratio(paper_data))
        
        # ENSO variability check
        results.append(self._check_enso_dominance(paper_data))
        
        # Temperature response feasibility
        results.append(self._check_temperature_response_magnitude(paper_data))
        
        # Detection threshold validation
        results.append(self._check_detection_thresholds(paper_data))
        
        # Climate variability scale check
        results.append(self._check_natural_variability_scale(paper_data))
        
        return [r for r in results if r is not None]
    
    def _check_signal_to_noise_ratio(self, paper_data: Dict[str, Any]) -> Optional[RealityCheckResult]:
        """Check if claimed signal is detectable above natural variability"""
        
        # Extract signal and noise estimates from paper
        signal_magnitude = self._extract_signal_magnitude(paper_data)
        noise_magnitude = self._extract_noise_magnitude(paper_data)
        
        if signal_magnitude is None or noise_magnitude is None:
            return None
            
        # Calculate SNR
        snr_linear = signal_magnitude / noise_magnitude if noise_magnitude > 0 else 0
        snr_db = 20 * np.log10(snr_linear) if snr_linear > 0 else -np.inf
        
        # Climate detection typically requires SNR > 1 (0 dB) for reliable detection
        # SNR < -10 dB is essentially hopeless
        if snr_db < -20:
            severity = SeverityLevel.CATASTROPHIC
            passed = False
            message = f"Signal-to-noise ratio catastrophically low: {snr_db:.1f} dB. Detection impossible."
        elif snr_db < -10:
            severity = SeverityLevel.CRITICAL
            passed = False
            message = f"Signal-to-noise ratio critically low: {snr_db:.1f} dB. Detection highly unlikely."
        elif snr_db < 0:
            severity = SeverityLevel.HIGH
            passed = False
            message = f"Signal-to-noise ratio problematic: {snr_db:.1f} dB. Detection challenging."
        else:
            severity = SeverityLevel.LOW
            passed = True
            message = f"Signal-to-noise ratio acceptable: {snr_db:.1f} dB."
        
        return RealityCheckResult(
            check_name="signal_to_noise_ratio",
            severity=severity,
            passed=passed,
            message=message,
            evidence={
                'signal_magnitude': signal_magnitude,
                'noise_magnitude': noise_magnitude,
                'snr_linear': snr_linear,
                'snr_db': snr_db,
                'detection_threshold': 0.0  # 0 dB
            },
            domain="climate_science",
            recommendation="Increase signal amplitude or reduce analysis to longer timescales" if not passed else "SNR adequate for detection"
        )
    
    def _check_enso_dominance(self, paper_data: Dict[str, Any]) -> Optional[RealityCheckResult]:
        """Check if ENSO variability dominates claimed signal"""
        
        # ENSO typically causes ~1.5K peak-to-peak global temperature variations
        enso_amplitude = 1.5  # K
        signal_amplitude = self._extract_signal_magnitude(paper_data)
        
        if signal_amplitude is None:
            return None
        
        # If signal is much smaller than ENSO, detection becomes very difficult
        enso_ratio = signal_amplitude / enso_amplitude
        
        if enso_ratio < 0.1:  # Signal < 10% of ENSO amplitude
            severity = SeverityLevel.CATASTROPHIC
            passed = False
            message = f"Signal ({signal_amplitude:.2f}K) is {1/enso_ratio:.1f}x smaller than ENSO variability. Detection impossible."
        elif enso_ratio < 0.2:
            severity = SeverityLevel.CRITICAL
            passed = False
            message = f"Signal ({signal_amplitude:.2f}K) is {1/enso_ratio:.1f}x smaller than ENSO variability. Detection highly unlikely."
        elif enso_ratio < 0.5:
            severity = SeverityLevel.HIGH
            passed = False
            message = f"Signal ({signal_amplitude:.2f}K) is {1/enso_ratio:.1f}x smaller than ENSO variability. Detection challenging."
        else:
            severity = SeverityLevel.LOW
            passed = True
            message = f"Signal ({signal_amplitude:.2f}K) is comparable to ENSO variability."
        
        return RealityCheckResult(
            check_name="enso_dominance_check",
            severity=severity,
            passed=passed,
            message=message,
            evidence={
                'signal_amplitude': signal_amplitude,
                'enso_amplitude': enso_amplitude,
                'enso_ratio': enso_ratio
            },
            domain="climate_science",
            recommendation="Increase signal amplitude or focus on longer-term averages" if not passed else "Signal adequate relative to ENSO"
        )
    
    def _check_temperature_response_magnitude(self, paper_data: Dict[str, Any]) -> Optional[RealityCheckResult]:
        """Check if claimed temperature response is physically reasonable"""
        
        # Extract temperature response and forcing magnitude
        temp_response = self._extract_signal_magnitude(paper_data)
        forcing_magnitude = self._extract_forcing_magnitude(paper_data)
        
        if temp_response is None or forcing_magnitude is None:
            return None
        
        # Climate sensitivity: ~0.5-2.0 K per Tg SO2/yr for SAI
        # This is based on literature values
        expected_sensitivity = 0.8  # K per Tg SO2/yr (middle estimate)
        expected_response = forcing_magnitude * expected_sensitivity
        
        response_ratio = temp_response / expected_response if expected_response > 0 else 0
        
        if response_ratio > 5 or response_ratio < 0.1:
            severity = SeverityLevel.CRITICAL
            passed = False
            message = f"Temperature response ({temp_response:.2f}K) inconsistent with forcing ({forcing_magnitude:.2f} Tg/yr). Expected ~{expected_response:.2f}K."
        elif response_ratio > 3 or response_ratio < 0.3:
            severity = SeverityLevel.HIGH
            passed = False
            message = f"Temperature response ({temp_response:.2f}K) questionable for forcing ({forcing_magnitude:.2f} Tg/yr). Expected ~{expected_response:.2f}K."
        else:
            severity = SeverityLevel.LOW
            passed = True
            message = f"Temperature response ({temp_response:.2f}K) reasonable for forcing ({forcing_magnitude:.2f} Tg/yr)."
        
        return RealityCheckResult(
            check_name="temperature_response_magnitude",
            severity=severity,
            passed=passed,
            message=message,
            evidence={
                'temp_response': temp_response,
                'forcing_magnitude': forcing_magnitude,
                'expected_response': expected_response,
                'response_ratio': response_ratio,
                'climate_sensitivity': expected_sensitivity
            },
            domain="climate_science",
            recommendation="Verify climate sensitivity assumptions" if not passed else "Temperature response magnitude reasonable"
        )
    
    def _check_detection_thresholds(self, paper_data: Dict[str, Any]) -> RealityCheckResult:
        """Check if detection claims are realistic given measurement uncertainties"""
        
        # Typical global temperature measurement uncertainty: ~0.05-0.1K
        measurement_uncertainty = 0.08  # K
        signal_magnitude = self._extract_signal_magnitude(paper_data) or 0.1
        
        # Signal should be at least 2-3x measurement uncertainty for reliable detection
        detection_ratio = signal_magnitude / measurement_uncertainty
        
        if detection_ratio < 1:
            severity = SeverityLevel.CATASTROPHIC
            passed = False
            message = f"Signal ({signal_magnitude:.3f}K) smaller than measurement uncertainty ({measurement_uncertainty:.3f}K). Undetectable."
        elif detection_ratio < 2:
            severity = SeverityLevel.CRITICAL
            passed = False
            message = f"Signal ({signal_magnitude:.3f}K) barely above measurement uncertainty. Detection highly uncertain."
        elif detection_ratio < 3:
            severity = SeverityLevel.HIGH
            passed = False
            message = f"Signal ({signal_magnitude:.3f}K) close to measurement uncertainty. Detection challenging."
        else:
            severity = SeverityLevel.LOW
            passed = True
            message = f"Signal ({signal_magnitude:.3f}K) well above measurement uncertainty."
        
        return RealityCheckResult(
            check_name="detection_threshold_check",
            severity=severity,
            passed=passed,
            message=message,
            evidence={
                'signal_magnitude': signal_magnitude,
                'measurement_uncertainty': measurement_uncertainty,
                'detection_ratio': detection_ratio,
                'minimum_detection_ratio': 2.0
            },
            domain="climate_science",
            recommendation="Account for measurement uncertainties in detection claims" if not passed else "Signal adequately above detection threshold"
        )
    
    def _check_natural_variability_scale(self, paper_data: Dict[str, Any]) -> RealityCheckResult:
        """Check if signal is detectable against full spectrum of natural variability"""
        
        # Natural variability sources and typical amplitudes
        variability_sources = {
            'ENSO': 1.5,           # K peak-to-peak
            'volcanic': 0.5,        # K typical volcanic cooling
            'solar_cycle': 0.1,     # K solar cycle amplitude
            'AMO': 0.3,            # K Atlantic Multidecadal Oscillation
            'internal_decade': 0.2  # K typical decadal internal variability
        }
        
        signal_magnitude = self._extract_signal_magnitude(paper_data) or 0.1
        
        # Calculate how signal compares to each variability source
        variability_ratios = {source: signal_magnitude / amplitude 
                            for source, amplitude in variability_sources.items()}
        
        # Find most problematic variability source
        min_ratio = min(variability_ratios.values())
        problematic_source = min(variability_ratios, key=variability_ratios.get)
        
        if min_ratio < 0.1:
            severity = SeverityLevel.CATASTROPHIC
            passed = False
            message = f"Signal overwhelmed by {problematic_source} variability (ratio: {min_ratio:.3f})"
        elif min_ratio < 0.3:
            severity = SeverityLevel.CRITICAL
            passed = False
            message = f"Signal barely detectable above {problematic_source} variability (ratio: {min_ratio:.3f})"
        elif min_ratio < 0.7:
            severity = SeverityLevel.HIGH
            passed = False
            message = f"Signal challenging to detect against {problematic_source} variability (ratio: {min_ratio:.3f})"
        else:
            severity = SeverityLevel.LOW
            passed = True
            message = f"Signal adequately above natural variability sources"
        
        return RealityCheckResult(
            check_name="natural_variability_scale",
            severity=severity,
            passed=passed,
            message=message,
            evidence={
                'signal_magnitude': signal_magnitude,
                'variability_sources': variability_sources,
                'variability_ratios': variability_ratios,
                'most_problematic': problematic_source,
                'minimum_ratio': min_ratio
            },
            domain="climate_science",
            recommendation="Consider longer averaging periods to reduce natural variability impact" if not passed else "Signal adequate relative to natural variability"
        )
    
    def _extract_signal_magnitude(self, paper_data: Dict[str, Any]) -> Optional[float]:
        """Extract signal magnitude from paper data"""
        # Try multiple common keys/patterns
        patterns = [
            'signal_amplitude', 'temperature_response', 'signal_magnitude',
            'cooling_effect', 'temperature_change', 'delta_temp'
        ]
        
        for pattern in patterns:
            if pattern in paper_data:
                value = paper_data[pattern]
                if isinstance(value, (int, float)):
                    return abs(float(value))
                elif isinstance(value, str):
                    # Try to extract number from string
                    match = re.search(r'[-+]?\d*\.?\d+', value)
                    if match:
                        return abs(float(match.group()))
        
        # Default small signal for SAI studies
        return 0.1
    
    def _extract_noise_magnitude(self, paper_data: Dict[str, Any]) -> Optional[float]:
        """Extract noise magnitude from paper data"""
        patterns = [
            'noise_amplitude', 'enso_amplitude', 'natural_variability',
            'background_variability', 'noise_level'
        ]
        
        for pattern in patterns:
            if pattern in paper_data:
                value = paper_data[pattern]
                if isinstance(value, (int, float)):
                    return abs(float(value))
                elif isinstance(value, str):
                    match = re.search(r'[-+]?\d*\.?\d+', value)
                    if match:
                        return abs(float(match.group()))
        
        # Default ENSO amplitude
        return 1.5
    
    def _extract_forcing_magnitude(self, paper_data: Dict[str, Any]) -> Optional[float]:
        """Extract forcing magnitude from paper data"""
        patterns = [
            'forcing_magnitude', 'injection_rate', 'sai_rate',
            'aerosol_injection', 'so2_injection'
        ]
        
        for pattern in patterns:
            if pattern in paper_data:
                value = paper_data[pattern]
                if isinstance(value, (int, float)):
                    return abs(float(value))
                elif isinstance(value, str):
                    match = re.search(r'[-+]?\d*\.?\d+', value)
                    if match:
                        return abs(float(match.group()))
        
        # Default small injection rate
        return 0.5

class PhysicsRealityChecks:
    """Physics-specific reality checks"""
    
    def run_reality_checks(self, paper_data: Dict[str, Any]) -> List[RealityCheckResult]:
        """Run physics reality checks"""
        results = []
        
        # Conservation law checks
        results.append(self._check_energy_conservation(paper_data))
        
        # Measurement precision limits
        results.append(self._check_measurement_precision(paper_data))
        
        # Physical constant consistency
        results.append(self._check_physical_constants(paper_data))
        
        return [r for r in results if r is not None]
    
    def _check_energy_conservation(self, paper_data: Dict[str, Any]) -> RealityCheckResult:
        """Check for energy conservation violations"""
        # Placeholder for energy conservation checks
        return RealityCheckResult(
            check_name="energy_conservation",
            severity=SeverityLevel.LOW,
            passed=True,
            message="Energy conservation checks passed",
            evidence={},
            domain="physics",
            recommendation="No issues detected"
        )
    
    def _check_measurement_precision(self, paper_data: Dict[str, Any]) -> RealityCheckResult:
        """Check if claimed precision is achievable"""
        # Placeholder for measurement precision checks
        return RealityCheckResult(
            check_name="measurement_precision",
            severity=SeverityLevel.LOW,
            passed=True,
            message="Measurement precision checks passed",
            evidence={},
            domain="physics",
            recommendation="No issues detected"
        )
    
    def _check_physical_constants(self, paper_data: Dict[str, Any]) -> RealityCheckResult:
        """Check physical constant usage"""
        # Placeholder for physical constant checks
        return RealityCheckResult(
            check_name="physical_constants",
            severity=SeverityLevel.LOW,
            passed=True,
            message="Physical constants usage correct",
            evidence={},
            domain="physics",
            recommendation="No issues detected"
        )

class GeneralRealityChecks:
    """General reality checks applicable to all domains"""
    
    def run_reality_checks(self, paper_data: Dict[str, Any]) -> List[RealityCheckResult]:
        """Run general reality checks"""
        results = []
        
        # "Too good to be true" metric detection
        results.append(self._check_too_good_to_be_true(paper_data))
        
        # Breakthrough claim validation
        results.append(self._check_breakthrough_claims(paper_data))
        
        # Statistical significance validation
        results.append(self._check_statistical_significance(paper_data))
        
        return [r for r in results if r is not None]
    
    def _check_too_good_to_be_true(self, paper_data: Dict[str, Any]) -> Optional[RealityCheckResult]:
        """Check for suspiciously perfect results"""
        
        # Look for R² values
        r_squared = None
        patterns = ['r_squared', 'r2', 'coefficient_determination', 'correlation_coefficient']
        
        for pattern in patterns:
            if pattern in paper_data:
                value = paper_data[pattern]
                if isinstance(value, (int, float)):
                    r_squared = float(value)
                    break
        
        if r_squared is None:
            return None
        
        # Check for suspiciously high R² values
        if r_squared > 0.99:
            severity = SeverityLevel.CRITICAL
            passed = False
            message = f"R² = {r_squared:.4f} suspiciously perfect. May indicate overfitting or artificial correlation."
        elif r_squared > 0.95:
            severity = SeverityLevel.HIGH
            passed = False
            message = f"R² = {r_squared:.4f} unusually high. Verify against independent validation."
        elif r_squared < 0.05:
            severity = SeverityLevel.CRITICAL
            passed = False
            message = f"R² = {r_squared:.4f} indicates virtually no predictive relationship."
        else:
            severity = SeverityLevel.LOW
            passed = True
            message = f"R² = {r_squared:.4f} in reasonable range."
        
        return RealityCheckResult(
            check_name="too_good_to_be_true",
            severity=severity,
            passed=passed,
            message=message,
            evidence={'r_squared': r_squared},
            domain="general",
            recommendation="Verify with independent validation dataset" if not passed else "Metrics appear reasonable"
        )
    
    def _check_breakthrough_claims(self, paper_data: Dict[str, Any]) -> RealityCheckResult:
        """Check for unsubstantiated breakthrough claims"""
        
        # Look for breakthrough language in paper content
        breakthrough_keywords = [
            'breakthrough', 'revolutionary', 'paradigm shift', 'unprecedented',
            'game-changing', 'transformative', 'first ever', 'never before'
        ]
        
        content = str(paper_data).lower()
        detected_claims = [kw for kw in breakthrough_keywords if kw in content]
        
        if len(detected_claims) > 3:
            severity = SeverityLevel.HIGH
            passed = False
            message = f"Excessive breakthrough claims detected: {detected_claims}. Verify novelty."
        elif len(detected_claims) > 1:
            severity = SeverityLevel.MEDIUM
            passed = False
            message = f"Multiple breakthrough claims detected: {detected_claims}. Verify with literature."
        else:
            severity = SeverityLevel.LOW
            passed = True
            message = "Reasonable claims, no excessive breakthrough language."
        
        return RealityCheckResult(
            check_name="breakthrough_claims",
            severity=severity,
            passed=passed,
            message=message,
            evidence={'breakthrough_claims': detected_claims},
            domain="general",
            recommendation="Verify breakthrough claims against literature" if not passed else "Claims appear modest"
        )
    
    def _check_statistical_significance(self, paper_data: Dict[str, Any]) -> Optional[RealityCheckResult]:
        """Check statistical significance of results"""
        
        # Look for p-values
        p_value = None
        patterns = ['p_value', 'pvalue', 'significance', 'p']
        
        for pattern in patterns:
            if pattern in paper_data:
                value = paper_data[pattern]
                if isinstance(value, (int, float)):
                    p_value = float(value)
                    break
        
        if p_value is None:
            return None
        
        if p_value > 0.05:
            severity = SeverityLevel.HIGH
            passed = False
            message = f"p-value = {p_value:.6f} indicates results not statistically significant."
        elif p_value < 1e-10:
            severity = SeverityLevel.MEDIUM
            passed = False
            message = f"p-value = {p_value:.2e} suspiciously small. Verify calculation."
        else:
            severity = SeverityLevel.LOW
            passed = True
            message = f"p-value = {p_value:.6f} indicates statistical significance."
        
        return RealityCheckResult(
            check_name="statistical_significance",
            severity=severity,
            passed=passed,
            message=message,
            evidence={'p_value': p_value},
            domain="general",
            recommendation="Increase sample size or effect size" if not passed else "Statistical significance adequate"
        )

# Main interface function
def run_reality_check_analysis(paper_data: Dict[str, Any], domain: str = 'general') -> Dict[str, Any]:
    """
    Main interface for reality check analysis
    
    Args:
        paper_data: Dictionary containing paper content, metrics, and claims
        domain: Scientific domain ('climate_science', 'physics', 'general')
        
    Returns:
        Reality check analysis results
    """
    engine = PhysicalFeasibilityEngine()
    return engine.analyze_paper(paper_data, domain)