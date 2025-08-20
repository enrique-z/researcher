"""
Plausibility Checker

Implements sophisticated checks to prevent the "plausibility trap" where theoretical
elegance is mistaken for empirical validity. This module provides detailed analysis
to distinguish between genuine empirical support and persuasive but ungrounded claims.

Key Functions:
- Theoretical elegance vs empirical support analysis
- Quantitative evidence requirements validation
- Sophisticated claim pattern detection
- Integration with SNR analysis for comprehensive validation
"""

import numpy as np
import re
from typing import Dict, List, Union, Optional
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PlausibilityChecker:
    """
    Advanced plausibility checker to prevent acceptance of theoretical claims
    that appear sophisticated but lack adequate empirical support.
    
    Implements pattern recognition for common "plausibility trap" scenarios
    where complex mathematical formulations mask insufficient empirical grounding.
    """
    
    def __init__(self):
        """Initialize plausibility checker with detection patterns."""
        
        # Patterns that suggest theoretical sophistication without empirical backing
        self.sophistication_indicators = [
            r'\b(?:Volterra|kernel|spectroscopy|eigenvalue|tensor|manifold)\b',
            r'\b(?:stochastic|optimization|variational|Hamiltonian)\b', 
            r'\b(?:nonlinear|dynamical|perturbation|asymptotic)\b',
            r'(?:∂|∇|∫|∑|∏|⊗|⊕)',  # Mathematical symbols
            r'\b(?:LaTeX|equation|formula|theorem|lemma)\b'
        ]
        
        # Patterns that suggest empirical grounding
        self.empirical_indicators = [
            r'\b(?:dataset|observation|measurement|experiment)\b',
            r'\b(?:GLENS|ARISE-SAI|GeoMIP|NCAR|UCAR)\b',
            r'\b(?:NetCDF|xarray|ensemble|statistical)\b',
            r'\b(?:p-value|confidence|correlation|regression)\b',
            r'\b(?:validation|verification|calibration)\b'
        ]
        
        # Red flag patterns for classic plausibility traps
        self.red_flag_patterns = [
            r'(?:undetectable|below noise|theoretical|proposed)',
            r'(?:elegant|sophisticated|novel|advanced).*(?:framework|approach)',
            r'(?:complex|intricate|elaborate).*(?:mathematics|formulation)',
            r'(?:state-of-the-art|cutting-edge|breakthrough).*(?:without|lacking)'
        ]
        
        self.check_history = []
        
    def analyze_claim_plausibility(self, claim_text: str, evidence: Dict) -> Dict:
        """
        Comprehensive plausibility analysis of a theoretical claim.
        
        Args:
            claim_text: Text description of the theoretical claim
            evidence: Dictionary containing supporting evidence and validation results
            
        Returns:
            Dict containing detailed plausibility analysis and risk assessment
        """
        analysis_result = {
            'claim_text': claim_text,
            'analysis_timestamp': datetime.now().isoformat(),
            'sophistication_score': 0,
            'empirical_support_score': 0,
            'red_flag_score': 0,
            'plausibility_risk_level': 'UNKNOWN',
            'plausibility_assessment': 'PENDING',
            'detailed_analysis': {},
            'recommendations': []
        }
        
        try:
            # Analyze theoretical sophistication
            sophistication_analysis = self._analyze_sophistication(claim_text)
            analysis_result['sophistication_score'] = sophistication_analysis['score']
            analysis_result['detailed_analysis']['sophistication'] = sophistication_analysis
            
            # Analyze empirical support
            empirical_analysis = self._analyze_empirical_support(claim_text, evidence)
            analysis_result['empirical_support_score'] = empirical_analysis['score']
            analysis_result['detailed_analysis']['empirical_support'] = empirical_analysis
            
            # Check for red flag patterns
            red_flag_analysis = self._check_red_flags(claim_text)
            analysis_result['red_flag_score'] = red_flag_analysis['score']
            analysis_result['detailed_analysis']['red_flags'] = red_flag_analysis
            
            # Calculate overall plausibility risk
            risk_assessment = self._assess_plausibility_risk(analysis_result)
            analysis_result.update(risk_assessment)
            
            # Log analysis result
            self.check_history.append(analysis_result)
            
            return analysis_result
            
        except Exception as e:
            analysis_result['plausibility_assessment'] = 'ERROR'
            analysis_result['recommendations'].append(f'Analysis error: {str(e)}')
            logger.error(f"Plausibility analysis failed: {e}")
            return analysis_result
    
    def _analyze_sophistication(self, claim_text: str) -> Dict:
        """
        Analyze the theoretical sophistication level of a claim.
        
        High sophistication without empirical support is a classic plausibility trap indicator.
        """
        sophistication_analysis = {
            'score': 0,
            'indicators_found': [],
            'sophistication_level': 'UNKNOWN',
            'mathematical_complexity': 'LOW',
            'theoretical_depth': 'SHALLOW'
        }
        
        # Count sophistication indicators
        total_matches = 0
        for pattern in self.sophistication_indicators:
            matches = re.findall(pattern, claim_text, re.IGNORECASE)
            if matches:
                sophistication_analysis['indicators_found'].extend(matches)
                total_matches += len(matches)
        
        # Calculate sophistication score (normalized)
        sophistication_analysis['score'] = min(total_matches / 5.0, 1.0)  # Cap at 1.0
        
        # Determine sophistication level
        if sophistication_analysis['score'] >= 0.8:
            sophistication_analysis['sophistication_level'] = 'VERY_HIGH'
            sophistication_analysis['mathematical_complexity'] = 'VERY_HIGH'
            sophistication_analysis['theoretical_depth'] = 'DEEP'
        elif sophistication_analysis['score'] >= 0.6:
            sophistication_analysis['sophistication_level'] = 'HIGH'
            sophistication_analysis['mathematical_complexity'] = 'HIGH'
            sophistication_analysis['theoretical_depth'] = 'MODERATE'
        elif sophistication_analysis['score'] >= 0.4:
            sophistication_analysis['sophistication_level'] = 'MODERATE'
            sophistication_analysis['mathematical_complexity'] = 'MODERATE'
        elif sophistication_analysis['score'] >= 0.2:
            sophistication_analysis['sophistication_level'] = 'LOW'
        else:
            sophistication_analysis['sophistication_level'] = 'MINIMAL'
        
        return sophistication_analysis
    
    def _analyze_empirical_support(self, claim_text: str, evidence: Dict) -> Dict:
        """
        Analyze the empirical support level for a theoretical claim.
        
        Combines textual evidence indicators with quantitative evidence validation.
        """
        empirical_analysis = {
            'score': 0,
            'textual_indicators': [],
            'evidence_validation': {},
            'support_level': 'UNKNOWN',
            'data_authenticity': 'UNVERIFIED',
            'quantitative_support': False
        }
        
        # Analyze textual empirical indicators
        textual_score = 0
        for pattern in self.empirical_indicators:
            matches = re.findall(pattern, claim_text, re.IGNORECASE)
            if matches:
                empirical_analysis['textual_indicators'].extend(matches)
                textual_score += len(matches)
        
        textual_score = min(textual_score / 5.0, 0.5)  # Max 0.5 from text alone
        
        # Analyze quantitative evidence
        quantitative_score = 0
        evidence_types = ['snr_analysis', 'statistical_validation', 'real_data_verification']
        
        for evidence_type in evidence_types:
            if evidence_type in evidence and evidence[evidence_type] is not None:
                empirical_analysis['evidence_validation'][evidence_type] = 'PRESENT'
                quantitative_score += 1
            else:
                empirical_analysis['evidence_validation'][evidence_type] = 'MISSING'
        
        quantitative_score = quantitative_score / len(evidence_types) * 0.5  # Max 0.5 from evidence
        
        # Check for real data authenticity
        if 'real_data_verification' in evidence:
            data_verification = evidence['real_data_verification']
            if isinstance(data_verification, dict) and data_verification.get('authentic_data_confirmed', False):
                empirical_analysis['data_authenticity'] = 'VERIFIED'
                quantitative_score += 0.2  # Bonus for verified real data
            else:
                empirical_analysis['data_authenticity'] = 'FAILED'
        
        # Check for statistical significance
        if 'snr_analysis' in evidence:
            snr_data = evidence['snr_analysis']
            if isinstance(snr_data, dict) and snr_data.get('snr_db', -np.inf) > 0:
                empirical_analysis['quantitative_support'] = True
                quantitative_score += 0.2  # Bonus for detectable signal
        
        # Combine scores
        empirical_analysis['score'] = min(textual_score + quantitative_score, 1.0)
        
        # Determine support level
        if empirical_analysis['score'] >= 0.8:
            empirical_analysis['support_level'] = 'STRONG'
        elif empirical_analysis['score'] >= 0.6:
            empirical_analysis['support_level'] = 'MODERATE'
        elif empirical_analysis['score'] >= 0.4:
            empirical_analysis['support_level'] = 'WEAK'
        elif empirical_analysis['score'] >= 0.2:
            empirical_analysis['support_level'] = 'MINIMAL'
        else:
            empirical_analysis['support_level'] = 'INSUFFICIENT'
        
        return empirical_analysis
    
    def _check_red_flags(self, claim_text: str) -> Dict:
        """
        Check for red flag patterns that strongly suggest plausibility trap scenarios.
        """
        red_flag_analysis = {
            'score': 0,
            'flags_detected': [],
            'risk_indicators': [],
            'severity_level': 'NONE'
        }
        
        total_flags = 0
        for pattern in self.red_flag_patterns:
            matches = re.findall(pattern, claim_text, re.IGNORECASE)
            if matches:
                red_flag_analysis['flags_detected'].extend(matches)
                total_flags += len(matches)
                red_flag_analysis['risk_indicators'].append(f"Pattern detected: {pattern}")
        
        # Calculate red flag score
        red_flag_analysis['score'] = min(total_flags / 3.0, 1.0)  # Normalize to max 1.0
        
        # Determine severity level
        if red_flag_analysis['score'] >= 0.7:
            red_flag_analysis['severity_level'] = 'CRITICAL'
        elif red_flag_analysis['score'] >= 0.5:
            red_flag_analysis['severity_level'] = 'HIGH'
        elif red_flag_analysis['score'] >= 0.3:
            red_flag_analysis['severity_level'] = 'MODERATE'
        elif red_flag_analysis['score'] > 0:
            red_flag_analysis['severity_level'] = 'LOW'
        else:
            red_flag_analysis['severity_level'] = 'NONE'
        
        return red_flag_analysis
    
    def _assess_plausibility_risk(self, analysis_result: Dict) -> Dict:
        """
        Assess overall plausibility risk based on sophistication, empirical support, and red flags.
        
        High sophistication + Low empirical support + Red flags = High plausibility trap risk
        """
        sophistication_score = analysis_result['sophistication_score']
        empirical_score = analysis_result['empirical_support_score']
        red_flag_score = analysis_result['red_flag_score']
        
        # Calculate plausibility trap risk using weighted formula
        # High sophistication is risky when empirical support is low
        sophistication_risk = sophistication_score * (1 - empirical_score)
        
        # Red flags multiply the risk
        red_flag_multiplier = 1 + red_flag_score
        
        # Combined risk score
        overall_risk = min(sophistication_risk * red_flag_multiplier, 1.0)
        
        # Determine risk level and assessment
        risk_assessment = {
            'overall_risk_score': overall_risk,
            'risk_factors': [],
            'protective_factors': []
        }
        
        # Identify risk factors
        if sophistication_score > 0.6 and empirical_score < 0.4:
            risk_assessment['risk_factors'].append('High sophistication with low empirical support')
        
        if red_flag_score > 0.3:
            risk_assessment['risk_factors'].append('Red flag patterns detected')
        
        if empirical_score < 0.2:
            risk_assessment['risk_factors'].append('Insufficient empirical evidence')
        
        # Identify protective factors
        if empirical_score > 0.6:
            risk_assessment['protective_factors'].append('Strong empirical support')
        
        if red_flag_score == 0:
            risk_assessment['protective_factors'].append('No red flag patterns detected')
        
        if analysis_result['detailed_analysis']['empirical_support']['data_authenticity'] == 'VERIFIED':
            risk_assessment['protective_factors'].append('Verified authentic data usage')
        
        # Determine final risk level and assessment
        if overall_risk >= 0.8:
            risk_assessment['plausibility_risk_level'] = 'CRITICAL'
            risk_assessment['plausibility_assessment'] = 'PLAUSIBILITY_TRAP_LIKELY'
            risk_assessment['recommendations'] = [
                'REJECT: High risk of plausibility trap',
                'Claim appears sophisticated but lacks adequate empirical support',
                'Require stronger empirical validation before acceptance'
            ]
        elif overall_risk >= 0.6:
            risk_assessment['plausibility_risk_level'] = 'HIGH'
            risk_assessment['plausibility_assessment'] = 'PLAUSIBILITY_TRAP_POSSIBLE'
            risk_assessment['recommendations'] = [
                'CAUTION: Moderate to high plausibility trap risk',
                'Additional empirical validation strongly recommended',
                'Verify theoretical claims against real data'
            ]
        elif overall_risk >= 0.4:
            risk_assessment['plausibility_risk_level'] = 'MODERATE'
            risk_assessment['plausibility_assessment'] = 'REQUIRES_VALIDATION'
            risk_assessment['recommendations'] = [
                'Additional validation recommended',
                'Strengthen empirical support for theoretical claims'
            ]
        elif overall_risk >= 0.2:
            risk_assessment['plausibility_risk_level'] = 'LOW'
            risk_assessment['plausibility_assessment'] = 'ACCEPTABLE_WITH_CAVEATS'
            risk_assessment['recommendations'] = [
                'Generally acceptable but monitor for empirical support'
            ]
        else:
            risk_assessment['plausibility_risk_level'] = 'MINIMAL'
            risk_assessment['plausibility_assessment'] = 'EMPIRICALLY_GROUNDED'
            risk_assessment['recommendations'] = [
                'Well-supported claim with adequate empirical grounding'
            ]
        
        return risk_assessment
    
    def check_quantitative_grounding(self, parameters: Dict) -> Dict:
        """
        Check that theoretical parameters have quantitative grounding in reality.
        
        Prevents order-of-magnitude errors and physically impossible parameter values.
        """
        grounding_result = {
            'overall_status': 'UNKNOWN',
            'parameter_checks': [],
            'violations': [],
            'warnings': []
        }
        
        # Define reasonable ranges for common climate parameters
        parameter_ranges = {
            'temperature_change': (-20.0, 20.0),     # °C reasonable range
            'precipitation_change': (-80.0, 100.0),   # % change reasonable range
            'radiative_forcing': (-15.0, 15.0),      # W/m² reasonable range
            'sai_injection': (0.0, 100.0),           # Tg/yr reasonable range
            'snr_threshold': (-30.0, 50.0),          # dB reasonable range
            'signal_strength': (0.0, 1000.0),        # Normalized units
            'noise_level': (0.0, 1000.0)             # Normalized units
        }
        
        violations_found = False
        
        for param_name, param_value in parameters.items():
            param_check = {
                'parameter': param_name,
                'value': param_value,
                'status': 'UNKNOWN',
                'range_check': 'NOT_APPLICABLE'
            }
            
            # Find applicable range check
            applicable_range = None
            for range_key, range_values in parameter_ranges.items():
                if range_key.lower() in param_name.lower():
                    applicable_range = range_values
                    break
            
            if applicable_range and isinstance(param_value, (int, float)):
                min_val, max_val = applicable_range
                
                if min_val <= param_value <= max_val:
                    param_check['status'] = 'VALID'
                    param_check['range_check'] = 'PASSED'
                else:
                    param_check['status'] = 'VIOLATION'
                    param_check['range_check'] = 'FAILED'
                    violations_found = True
                    grounding_result['violations'].append(
                        f'{param_name}: {param_value} outside reasonable range [{min_val}, {max_val}]'
                    )
                
                # Check for order-of-magnitude issues
                if abs(param_value) > 10 * max_val or abs(param_value) < min_val / 10:
                    grounding_result['warnings'].append(
                        f'{param_name}: Possible order-of-magnitude issue ({param_value})'
                    )
            
            grounding_result['parameter_checks'].append(param_check)
        
        # Set overall status
        if violations_found:
            grounding_result['overall_status'] = 'VIOLATIONS_FOUND'
        elif grounding_result['parameter_checks']:
            grounding_result['overall_status'] = 'QUANTITATIVELY_GROUNDED'
        else:
            grounding_result['overall_status'] = 'NO_PARAMETERS_TO_CHECK'
        
        return grounding_result
    
    def get_check_history_summary(self) -> Dict:
        """Get summary of all plausibility checks performed."""
        if not self.check_history:
            return {'total_checks': 0, 'summary': 'No checks performed'}
        
        risk_level_counts = {}
        assessment_counts = {}
        
        for check in self.check_history:
            risk_level = check['plausibility_risk_level']
            assessment = check['plausibility_assessment']
            
            risk_level_counts[risk_level] = risk_level_counts.get(risk_level, 0) + 1
            assessment_counts[assessment] = assessment_counts.get(assessment, 0) + 1
        
        total_checks = len(self.check_history)
        plausibility_traps_detected = sum(1 for check in self.check_history 
                                        if check['plausibility_assessment'] in ['PLAUSIBILITY_TRAP_LIKELY', 'PLAUSIBILITY_TRAP_POSSIBLE'])
        
        return {
            'total_checks': total_checks,
            'risk_level_distribution': risk_level_counts,
            'assessment_distribution': assessment_counts,
            'plausibility_trap_detection_rate': plausibility_traps_detected / total_checks,
            'protection_effectiveness': (total_checks - plausibility_traps_detected) / total_checks
        }