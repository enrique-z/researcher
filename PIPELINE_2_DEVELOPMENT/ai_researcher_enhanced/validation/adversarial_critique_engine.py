"""
Adversarial Critique Engine: Multi-Iteration Critical Analysis System
Implements mandatory adversarial validation loops with Gemini Deep Research integration

This module is designed to catch fundamental flaws that plausibility-based validation misses
by implementing progressive adversarial questioning through multiple iterations.

Based on the critical discovery that even sophisticated systems like URSA and initial Sakana
can validate methodological soundness while missing physical impossibility - requiring
4 iterations of Gemini Deep Research to expose the truth.
"""

import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class CritiqueStage(Enum):
    """Stages of adversarial critique process"""
    INITIAL_REVIEW = "initial_review"
    METHODOLOGY_CHALLENGE = "methodology_challenge"
    ASSUMPTION_QUESTIONING = "assumption_questioning"
    FUNDAMENTAL_FEASIBILITY = "fundamental_feasibility"
    FINAL_SYNTHESIS = "final_synthesis"

class CritiqueResult(Enum):
    """Results of critique iteration"""
    PASSED = "passed"
    CONCERNS_RAISED = "concerns_raised"
    FUNDAMENTAL_FLAWS = "fundamental_flaws"
    PHYSICALLY_IMPOSSIBLE = "physically_impossible"

@dataclass
class CritiqueIteration:
    """Single iteration of adversarial critique"""
    iteration_number: int
    stage: CritiqueStage
    critique_prompt: str
    gemini_response: Optional[str]
    key_findings: List[str]
    red_flags: List[str]
    result: CritiqueResult
    confidence_rating: float  # 0-1 scale
    requires_next_iteration: bool
    timestamp: str

@dataclass
class AdversarialCritiqueSession:
    """Complete adversarial critique session"""
    session_id: str
    paper_title: str
    domain: str
    iterations: List[CritiqueIteration]
    overall_result: CritiqueResult
    final_assessment: str
    critical_flaws_detected: List[str]
    plausibility_trap_score: float  # 0-1, higher = more likely to be plausibility trap
    created_at: str
    completed_at: Optional[str]

class AdversarialCritiqueEngine:
    """Main engine for adversarial critique process"""
    
    def __init__(self, workspace_dir: str = "/Users/apple/code/Researcher/.claude/adversarial_critiques"):
        self.workspace_dir = workspace_dir
        os.makedirs(workspace_dir, exist_ok=True)
        
        # Critique stages and their focus
        self.critique_stages = {
            CritiqueStage.INITIAL_REVIEW: {
                'focus': 'General methodological soundness and result plausibility',
                'adversarial_intensity': 'moderate',
                'key_questions': [
                    'Are the claimed results too good to be true?',
                    'Do the metrics make sense in context?',
                    'Are the experimental methods appropriate?'
                ]
            },
            CritiqueStage.METHODOLOGY_CHALLENGE: {
                'focus': 'Deep dive into experimental design and analytical methods',
                'adversarial_intensity': 'high',
                'key_questions': [
                    'Are there fundamental flaws in the experimental design?',
                    'Do the analytical methods match the problem complexity?',
                    'Are key assumptions violated?'
                ]
            },
            CritiqueStage.ASSUMPTION_QUESTIONING: {
                'focus': 'Challenge core assumptions and underlying physics',
                'adversarial_intensity': 'very_high',
                'key_questions': [
                    'Are the underlying physical assumptions valid?',
                    'Do the claimed effects violate known physics?',
                    'Are signal-to-noise considerations adequate?'
                ]
            },
            CritiqueStage.FUNDAMENTAL_FEASIBILITY: {
                'focus': 'Physical impossibility and feasibility barriers',
                'adversarial_intensity': 'maximum',
                'key_questions': [
                    'Is this physically possible given known constraints?',
                    'Are there fundamental barriers that make this impossible?',
                    'Does this violate basic physics or measurement limits?'
                ]
            }
        }
    
    def start_adversarial_critique(self, paper_data: Dict[str, Any], domain: str = 'general') -> str:
        """
        Start a new adversarial critique session
        
        Args:
            paper_data: Dictionary containing paper content and metadata
            domain: Scientific domain for domain-specific critique
            
        Returns:
            Session ID for tracking the critique process
        """
        session_id = str(uuid.uuid4())
        
        session = AdversarialCritiqueSession(
            session_id=session_id,
            paper_title=paper_data.get('title', 'Unknown Paper'),
            domain=domain,
            iterations=[],
            overall_result=CritiqueResult.PASSED,  # Innocent until proven guilty
            final_assessment="",
            critical_flaws_detected=[],
            plausibility_trap_score=0.0,
            created_at=datetime.now().isoformat(),
            completed_at=None
        )
        
        # Save session
        self._save_session(session)
        
        # Generate first iteration
        first_iteration = self._generate_iteration(
            session, 
            CritiqueStage.INITIAL_REVIEW, 
            paper_data, 
            iteration_number=1
        )
        
        session.iterations.append(first_iteration)
        self._save_session(session)
        
        logger.info(f"Started adversarial critique session {session_id}")
        return session_id
    
    def process_gemini_response(self, session_id: str, iteration_number: int, gemini_response: str) -> Dict[str, Any]:
        """
        Process Gemini Deep Research response and determine next steps
        
        Args:
            session_id: Session identifier
            iteration_number: Current iteration number
            gemini_response: Response from Gemini Deep Research
            
        Returns:
            Dictionary with next steps and analysis results
        """
        session = self._load_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        # Find the current iteration
        current_iteration = None
        for iteration in session.iterations:
            if iteration.iteration_number == iteration_number:
                current_iteration = iteration
                break
        
        if not current_iteration:
            raise ValueError(f"Iteration {iteration_number} not found in session {session_id}")
        
        # Process the response
        current_iteration.gemini_response = gemini_response
        
        # Analyze the response for critical findings
        analysis_results = self._analyze_gemini_response(gemini_response, current_iteration.stage)
        
        # Update iteration with analysis results
        current_iteration.key_findings = analysis_results['key_findings']
        current_iteration.red_flags = analysis_results['red_flags']
        current_iteration.result = analysis_results['result']
        current_iteration.confidence_rating = analysis_results['confidence_rating']
        current_iteration.requires_next_iteration = analysis_results['requires_next_iteration']
        
        # Determine if we need another iteration
        next_iteration = None
        if current_iteration.requires_next_iteration and len(session.iterations) < 5:  # Max 5 iterations
            next_stage = self._get_next_stage(current_iteration.stage, current_iteration.result)
            if next_stage:
                paper_data = {'title': session.paper_title}  # Minimal data for next iteration
                next_iteration = self._generate_iteration(
                    session, 
                    next_stage, 
                    paper_data, 
                    iteration_number + 1,
                    previous_findings=current_iteration.key_findings + current_iteration.red_flags
                )
                session.iterations.append(next_iteration)
        
        # Update overall session assessment
        self._update_session_assessment(session)
        
        # Save updated session
        self._save_session(session)
        
        return {
            'session_id': session_id,
            'current_iteration_completed': True,
            'critical_findings': current_iteration.key_findings,
            'red_flags': current_iteration.red_flags,
            'result': current_iteration.result.value,
            'confidence': current_iteration.confidence_rating,
            'next_iteration_needed': current_iteration.requires_next_iteration,
            'next_iteration': asdict(next_iteration) if next_iteration else None,
            'session_status': 'in_progress' if next_iteration else 'completed',
            'overall_assessment': session.final_assessment if not next_iteration else "In progress"
        }
    
    def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get current status of adversarial critique session"""
        session = self._load_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        return {
            'session_id': session_id,
            'paper_title': session.paper_title,
            'domain': session.domain,
            'iterations_completed': len([i for i in session.iterations if i.gemini_response]),
            'total_iterations': len(session.iterations),
            'current_stage': session.iterations[-1].stage.value if session.iterations else None,
            'overall_result': session.overall_result.value,
            'critical_flaws': session.critical_flaws_detected,
            'plausibility_trap_score': session.plausibility_trap_score,
            'is_completed': session.completed_at is not None,
            'created_at': session.created_at,
            'completed_at': session.completed_at
        }
    
    def get_manual_gemini_package(self, session_id: str, iteration_number: int) -> Dict[str, Any]:
        """
        Generate package for manual Gemini Deep Research submission
        
        Returns structured prompt and instructions for manual submission
        """
        session = self._load_session(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        # Find the iteration
        iteration = None
        for iter_obj in session.iterations:
            if iter_obj.iteration_number == iteration_number:
                iteration = iter_obj
                break
        
        if not iteration:
            raise ValueError(f"Iteration {iteration_number} not found")
        
        # Generate comprehensive package
        package = {
            'session_info': {
                'session_id': session_id,
                'iteration': iteration_number,
                'stage': iteration.stage.value,
                'paper_title': session.paper_title,
                'domain': session.domain
            },
            'gemini_prompt': iteration.critique_prompt,
            'submission_instructions': self._generate_submission_instructions(iteration.stage),
            'expected_response_format': self._generate_response_format_guide(),
            'critique_focus': self.critique_stages[iteration.stage]['focus'],
            'adversarial_intensity': self.critique_stages[iteration.stage]['adversarial_intensity'],
            'key_questions': self.critique_stages[iteration.stage]['key_questions']
        }
        
        return package
    
    def _generate_iteration(self, session: AdversarialCritiqueSession, stage: CritiqueStage, 
                          paper_data: Dict[str, Any], iteration_number: int,
                          previous_findings: List[str] = None) -> CritiqueIteration:
        """Generate a new critique iteration"""
        
        # Generate adversarial prompt based on stage
        prompt = self._generate_adversarial_prompt(stage, paper_data, session.domain, previous_findings)
        
        iteration = CritiqueIteration(
            iteration_number=iteration_number,
            stage=stage,
            critique_prompt=prompt,
            gemini_response=None,
            key_findings=[],
            red_flags=[],
            result=CritiqueResult.PASSED,
            confidence_rating=0.0,
            requires_next_iteration=True,
            timestamp=datetime.now().isoformat()
        )
        
        return iteration
    
    def _generate_adversarial_prompt(self, stage: CritiqueStage, paper_data: Dict[str, Any], 
                                   domain: str, previous_findings: List[str] = None) -> str:
        """Generate adversarial prompt for Gemini Deep Research"""
        
        base_context = f"""
You are conducting a critical scientific review with the goal of identifying fundamental flaws that might be missed by standard peer review. This is part of an adversarial validation process designed to catch the "plausibility trap" - research that appears methodologically sound but contains fundamental physical impossibilities.

**CRITICAL CONTEXT**: Recent analysis has shown that sophisticated AI systems can validate plausibility (form, citations, mathematical consistency) while completely missing physical impossibility. Your role is to be maximally adversarial and skeptical.

**Paper Domain**: {domain}
**Paper Title**: {paper_data.get('title', 'Research Paper')}
**Critique Stage**: {stage.value}
**Focus**: {self.critique_stages[stage]['focus']}
**Adversarial Intensity**: {self.critique_stages[stage]['adversarial_intensity']}
"""
        
        if previous_findings:
            base_context += f"\n**Previous Findings**: {previous_findings}\n"
        
        # Stage-specific prompts
        stage_prompts = {
            CritiqueStage.INITIAL_REVIEW: """
**INITIAL REVIEW - MODERATE ADVERSARIAL APPROACH**

Conduct a general critical review focusing on:

1. **Result Plausibility**: Are the claimed results realistic? Look for:
   - Performance metrics that seem too good to be true
   - Claims that appear to solve long-standing problems too easily
   - Results that lack proper context or benchmarking

2. **Methodological Soundness**: Evaluate the experimental approach:
   - Are the methods appropriate for the research questions?
   - Is the experimental design adequate?
   - Are there obvious methodological flaws?

3. **Statistical Validity**: Check statistical claims:
   - Are significance tests appropriate?
   - Is the sample size adequate?
   - Are confidence intervals reasonable?

**Be skeptical but fair. Focus on obvious red flags and implausible claims.**
""",
            
            CritiqueStage.METHODOLOGY_CHALLENGE: """
**METHODOLOGY CHALLENGE - HIGH ADVERSARIAL APPROACH**

Conduct a deep methodological critique focusing on:

1. **Experimental Design Flaws**: Look for fundamental design problems:
   - Are controls appropriate and adequate?
   - Are confounding variables properly addressed?
   - Is the experimental setup realistic?

2. **Analytical Method Mismatch**: Challenge the analytical approach:
   - Do the methods match the complexity of the problem?
   - Are simplifying assumptions justified?
   - Are there better analytical approaches?

3. **Data Quality and Processing**: Scrutinize data handling:
   - Is the data of sufficient quality and quantity?
   - Are processing steps appropriate?
   - Could processing artifacts explain the results?

**Be highly skeptical. Challenge every methodological choice. Look for fatal flaws.**
""",
            
            CritiqueStage.ASSUMPTION_QUESTIONING: """
**ASSUMPTION QUESTIONING - VERY HIGH ADVERSARIAL APPROACH**

Challenge core assumptions with maximum skepticism:

1. **Physical Assumptions**: Question fundamental physical premises:
   - Are the underlying physics correctly understood?
   - Do claimed effects violate known physical principles?
   - Are approximations and simplifications valid?

2. **Signal-to-Noise Considerations**: Focus on detectability:
   - Is the claimed signal actually detectable above noise?
   - Are noise sources properly characterized?
   - Is the signal-to-noise ratio adequate?

3. **Scaling and Feasibility**: Challenge practical feasibility:
   - Do laboratory results scale to real-world conditions?
   - Are claimed sensitivities achievable?
   - Are there fundamental barriers ignored?

**Be maximally adversarial. Assume the authors are wrong until proven otherwise.**
""",
            
            CritiqueStage.FUNDAMENTAL_FEASIBILITY: """
**FUNDAMENTAL FEASIBILITY - MAXIMUM ADVERSARIAL APPROACH**

This is the final, most critical stage. Your goal is to determine if this research is fundamentally impossible:

1. **Physical Impossibility**: Look for violations of fundamental physics:
   - Do claimed effects violate conservation laws?
   - Are measurement claims beyond physical limits?
   - Does the approach violate thermodynamic constraints?

2. **Measurement Limits**: Focus on detection feasibility:
   - Is the signal below fundamental measurement noise?
   - Are claimed precisions achievable with available instruments?
   - Do natural variabilities overwhelm claimed signals?

3. **Order-of-Magnitude Analysis**: Perform sanity checks:
   - Are the scales (energy, time, distance) reasonable?
   - Do claimed effects make sense in context?
   - Are the magnitudes physically plausible?

**BE RUTHLESS. This is the last chance to catch fundamental impossibilities. If this research violates basic physics or measurement limits, expose it completely.**

**SPECIFIC FOCUS FOR CLIMATE RESEARCH**: If this involves climate science, pay special attention to:
- Signal detection against ENSO and other natural variabilities (ENSO ~1.5K amplitude)
- Typical measurement uncertainties (~0.05-0.1K for global temperature)
- Climate sensitivity ranges (0.5-2.0K per unit forcing)
- Whether claimed detection is possible given these constraints
"""
        }
        
        prompt = base_context + "\n" + stage_prompts[stage] + f"""

**KEY QUESTIONS FOR THIS STAGE**:
{chr(10).join(f"- {q}" for q in self.critique_stages[stage]['key_questions'])}

**OUTPUT FORMAT**:
Please provide a detailed critical analysis including:
1. **Critical Findings**: List all significant issues found
2. **Red Flags**: Highlight major concerns or impossibilities
3. **Confidence Assessment**: Rate your confidence in the criticism (0-100%)
4. **Overall Assessment**: Is this research sound, flawed, or fundamentally impossible?
5. **Recommendation**: Should this research be accepted, require major revision, or be rejected?

**REMEMBER**: Your role is to be adversarial and skeptical. Err on the side of criticism rather than acceptance.
"""
        
        return prompt
    
    def _analyze_gemini_response(self, response: str, stage: CritiqueStage) -> Dict[str, Any]:
        """Analyze Gemini response to extract key insights"""
        
        # Keywords indicating different levels of concern
        catastrophic_keywords = [
            'impossible', 'violates', 'fundamental flaw', 'physically impossible',
            'catastrophic', 'fatal flaw', 'completely wrong', 'ridiculous'
        ]
        
        critical_keywords = [
            'major flaw', 'serious problem', 'highly questionable', 'unrealistic',
            'implausible', 'deeply flawed', 'cannot work', 'fundamentally wrong'
        ]
        
        concerning_keywords = [
            'problematic', 'questionable', 'concerning', 'doubtful',
            'suspicious', 'unclear', 'inadequate', 'insufficient'
        ]
        
        positive_keywords = [
            'sound', 'reasonable', 'valid', 'appropriate', 'adequate',
            'correct', 'well done', 'proper', 'acceptable'
        ]
        
        response_lower = response.lower()
        
        # Count keyword occurrences
        catastrophic_count = sum(1 for kw in catastrophic_keywords if kw in response_lower)
        critical_count = sum(1 for kw in critical_keywords if kw in response_lower)
        concerning_count = sum(1 for kw in concerning_keywords if kw in response_lower)
        positive_count = sum(1 for kw in positive_keywords if kw in response_lower)
        
        # Extract key findings (simplified - in real implementation would use NLP)
        key_findings = []
        red_flags = []
        
        # Simple extraction based on patterns
        lines = response.split('\n')
        for line in lines:
            line = line.strip()
            if any(kw in line.lower() for kw in catastrophic_keywords + critical_keywords):
                red_flags.append(line)
            elif any(kw in line.lower() for kw in concerning_keywords):
                key_findings.append(line)
        
        # Determine result based on keyword analysis
        if catastrophic_count > 0:
            result = CritiqueResult.PHYSICALLY_IMPOSSIBLE
            confidence = min(0.9, 0.5 + catastrophic_count * 0.1)
            requires_next = catastrophic_count < 3  # Continue if not overwhelming evidence
        elif critical_count > 2:
            result = CritiqueResult.FUNDAMENTAL_FLAWS
            confidence = min(0.8, 0.4 + critical_count * 0.1)
            requires_next = True
        elif critical_count > 0 or concerning_count > 3:
            result = CritiqueResult.CONCERNS_RAISED
            confidence = min(0.7, 0.3 + (critical_count + concerning_count) * 0.05)
            requires_next = True
        else:
            result = CritiqueResult.PASSED
            confidence = min(0.8, max(0.2, positive_count * 0.1))
            requires_next = stage != CritiqueStage.FUNDAMENTAL_FEASIBILITY  # Continue unless final stage
        
        return {
            'key_findings': key_findings[:10],  # Limit to top 10
            'red_flags': red_flags[:10],
            'result': result,
            'confidence_rating': confidence,
            'requires_next_iteration': requires_next,
            'keyword_analysis': {
                'catastrophic': catastrophic_count,
                'critical': critical_count,
                'concerning': concerning_count,
                'positive': positive_count
            }
        }
    
    def _get_next_stage(self, current_stage: CritiqueStage, current_result: CritiqueResult) -> Optional[CritiqueStage]:
        """Determine next critique stage based on current results"""
        
        stage_progression = [
            CritiqueStage.INITIAL_REVIEW,
            CritiqueStage.METHODOLOGY_CHALLENGE,
            CritiqueStage.ASSUMPTION_QUESTIONING,
            CritiqueStage.FUNDAMENTAL_FEASIBILITY
        ]
        
        try:
            current_index = stage_progression.index(current_stage)
            
            # If we found fundamental flaws or physical impossibility, jump to final stage
            if current_result in [CritiqueResult.FUNDAMENTAL_FLAWS, CritiqueResult.PHYSICALLY_IMPOSSIBLE]:
                if current_stage != CritiqueStage.FUNDAMENTAL_FEASIBILITY:
                    return CritiqueStage.FUNDAMENTAL_FEASIBILITY
                else:
                    return None  # Already at final stage
            
            # Otherwise, proceed to next stage
            if current_index < len(stage_progression) - 1:
                return stage_progression[current_index + 1]
                
        except ValueError:
            pass
        
        return None
    
    def _update_session_assessment(self, session: AdversarialCritiqueSession):
        """Update overall session assessment based on all iterations"""
        
        if not session.iterations:
            return
        
        # Find worst result
        worst_result = CritiqueResult.PASSED
        all_red_flags = []
        total_confidence = 0
        
        for iteration in session.iterations:
            if iteration.result.value == 'physically_impossible':
                worst_result = CritiqueResult.PHYSICALLY_IMPOSSIBLE
            elif iteration.result.value == 'fundamental_flaws' and worst_result != CritiqueResult.PHYSICALLY_IMPOSSIBLE:
                worst_result = CritiqueResult.FUNDAMENTAL_FLAWS
            elif iteration.result.value == 'concerns_raised' and worst_result == CritiqueResult.PASSED:
                worst_result = CritiqueResult.CONCERNS_RAISED
            
            all_red_flags.extend(iteration.red_flags)
            total_confidence += iteration.confidence_rating
        
        session.overall_result = worst_result
        session.critical_flaws_detected = list(set(all_red_flags))  # Remove duplicates
        
        # Calculate plausibility trap score
        # Higher score if sophisticated methodology but fundamental physical flaws
        if worst_result == CritiqueResult.PHYSICALLY_IMPOSSIBLE:
            session.plausibility_trap_score = 0.9
        elif worst_result == CritiqueResult.FUNDAMENTAL_FLAWS:
            session.plausibility_trap_score = 0.7
        elif worst_result == CritiqueResult.CONCERNS_RAISED:
            session.plausibility_trap_score = 0.4
        else:
            session.plausibility_trap_score = 0.1
        
        # Generate final assessment
        avg_confidence = total_confidence / len(session.iterations) if session.iterations else 0
        
        if worst_result == CritiqueResult.PHYSICALLY_IMPOSSIBLE:
            session.final_assessment = f"PHYSICALLY IMPOSSIBLE - Fundamental physical constraints violated (confidence: {avg_confidence:.2f})"
        elif worst_result == CritiqueResult.FUNDAMENTAL_FLAWS:
            session.final_assessment = f"FUNDAMENTAL FLAWS - Major methodological or theoretical problems (confidence: {avg_confidence:.2f})"
        elif worst_result == CritiqueResult.CONCERNS_RAISED:
            session.final_assessment = f"SIGNIFICANT CONCERNS - Multiple issues requiring major revision (confidence: {avg_confidence:.2f})"
        else:
            session.final_assessment = f"PASSED - No fundamental issues detected (confidence: {avg_confidence:.2f})"
        
        # Mark as completed if we've reached the end
        if not any(i.requires_next_iteration for i in session.iterations):
            session.completed_at = datetime.now().isoformat()
    
    def _generate_submission_instructions(self, stage: CritiqueStage) -> str:
        """Generate instructions for manual Gemini submission"""
        return f"""
**MANUAL GEMINI DEEP RESEARCH SUBMISSION INSTRUCTIONS**

1. **Go to**: https://gemini.google.com/advanced
2. **Select**: Deep Research mode
3. **Copy and paste** the entire prompt below into Gemini
4. **Wait** for the deep research process to complete (typically 3-5 minutes)
5. **Copy the complete response** and paste it back into the pipeline

**IMPORTANT NOTES**:
- Use Deep Research mode, not regular Gemini
- Allow the full research process to complete
- Copy the entire response including reasoning steps
- This is iteration focusing on: {self.critique_stages[stage]['focus']}
- Adversarial intensity: {self.critique_stages[stage]['adversarial_intensity']}
"""
    
    def _generate_response_format_guide(self) -> str:
        """Generate guide for expected response format"""
        return """
**EXPECTED RESPONSE FORMAT FROM GEMINI**:

The response should include:
1. **Critical Findings**: List of significant issues
2. **Red Flags**: Major concerns or impossibilities  
3. **Confidence Assessment**: Numerical confidence in criticism
4. **Overall Assessment**: Sound/flawed/impossible determination
5. **Recommendation**: Accept/revise/reject recommendation

Look for these elements in the Gemini response when processing.
"""
    
    def _save_session(self, session: AdversarialCritiqueSession):
        """Save session to disk"""
        session_file = os.path.join(self.workspace_dir, f"session_{session.session_id}.json")
        
        # Convert to dict for JSON serialization
        session_dict = asdict(session)
        
        with open(session_file, 'w') as f:
            json.dump(session_dict, f, indent=2)
    
    def _load_session(self, session_id: str) -> Optional[AdversarialCritiqueSession]:
        """Load session from disk"""
        session_file = os.path.join(self.workspace_dir, f"session_{session_id}.json")
        
        if not os.path.exists(session_file):
            return None
        
        with open(session_file, 'r') as f:
            session_dict = json.load(f)
        
        # Convert back to dataclass
        # Convert iterations
        iterations = []
        for iter_dict in session_dict['iterations']:
            iter_dict['stage'] = CritiqueStage(iter_dict['stage'])
            iter_dict['result'] = CritiqueResult(iter_dict['result'])
            iterations.append(CritiqueIteration(**iter_dict))
        
        session_dict['iterations'] = iterations
        session_dict['overall_result'] = CritiqueResult(session_dict['overall_result'])
        
        return AdversarialCritiqueSession(**session_dict)

# Main interface functions
def start_adversarial_critique(paper_data: Dict[str, Any], domain: str = 'general') -> str:
    """Start new adversarial critique session"""
    engine = AdversarialCritiqueEngine()
    return engine.start_adversarial_critique(paper_data, domain)

def process_gemini_response(session_id: str, iteration_number: int, gemini_response: str) -> Dict[str, Any]:
    """Process Gemini response and get next steps"""
    engine = AdversarialCritiqueEngine()
    return engine.process_gemini_response(session_id, iteration_number, gemini_response)

def get_session_status(session_id: str) -> Dict[str, Any]:
    """Get current session status"""
    engine = AdversarialCritiqueEngine()
    return engine.get_session_status(session_id)

def get_manual_gemini_package(session_id: str, iteration_number: int) -> Dict[str, Any]:
    """Get package for manual Gemini submission"""
    engine = AdversarialCritiqueEngine()
    return engine.get_manual_gemini_package(session_id, iteration_number)