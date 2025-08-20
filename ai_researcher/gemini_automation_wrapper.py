"""
Gemini Automation Wrapper
=========================

Interactive coordination system for manual Gemini Deep Research workflows.
Designed to integrate manual Gemini expertise with automated pipeline processes.

Key Features:
- Interactive prompts for structured Gemini research sessions
- Research session documentation and tracking
- Standardized output templates for pipeline integration
- Progress monitoring and result aggregation
- Integration hooks for multi-system coordination

This wrapper enables coordinated use of Gemini's advanced reasoning capabilities
within the automated research pipeline while maintaining manual control.
"""

import os
import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Union, Optional, Any
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResearchMode(Enum):
    """Research session modes for different objectives."""
    HYPOTHESIS_GENERATION = "hypothesis_generation"
    LITERATURE_ANALYSIS = "literature_analysis"
    EXPERIMENTAL_DESIGN = "experimental_design"
    THEORETICAL_VALIDATION = "theoretical_validation"
    BREAKTHROUGH_EXPLORATION = "breakthrough_exploration"
    GAP_IDENTIFICATION = "gap_identification"

@dataclass
class GeminiSession:
    """Structured representation of a Gemini research session."""
    session_id: str
    mode: ResearchMode
    research_focus: str
    start_time: datetime
    end_time: Optional[datetime] = None
    prompts_used: List[str] = None
    key_insights: List[str] = None
    output_summary: str = ""
    follow_up_questions: List[str] = None
    integration_notes: str = ""
    quality_rating: Optional[int] = None  # 1-10 scale
    
    def __post_init__(self):
        if self.prompts_used is None:
            self.prompts_used = []
        if self.key_insights is None:
            self.key_insights = []
        if self.follow_up_questions is None:
            self.follow_up_questions = []

@dataclass
class ResearchCoordination:
    """Coordination requirements for multi-system research."""
    primary_system: str  # "gemini", "sakana", "oxford", "ursa"
    supporting_systems: List[str]
    research_objective: str
    expected_timeline: str
    deliverables: List[str]
    integration_points: List[str]

class GeminiAutomationWrapper:
    """
    Wrapper for coordinating manual Gemini research within automated pipelines.
    
    Provides structured interfaces for:
    - Research session planning and execution
    - Output standardization and documentation
    - Integration with other pipeline systems
    - Progress tracking and result aggregation
    """
    
    def __init__(self, output_dir: str = "./gemini_sessions"):
        """Initialize Gemini automation wrapper with session tracking."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.sessions_file = self.output_dir / "gemini_sessions.json"
        self.templates_dir = self.output_dir / "templates"
        self.templates_dir.mkdir(exist_ok=True)
        
        self.active_sessions: Dict[str, GeminiSession] = {}
        self.completed_sessions: List[GeminiSession] = []
        
        self._load_session_history()
        self._create_prompt_templates()
        
        logger.info("✅ Gemini Automation Wrapper initialized")
        logger.info(f"📁 Session output directory: {self.output_dir}")
        logger.info(f"📊 Previous sessions loaded: {len(self.completed_sessions)}")
    
    def _load_session_history(self):
        """Load previous session history if available."""
        if self.sessions_file.exists():
            try:
                with open(self.sessions_file, 'r') as f:
                    data = json.load(f)
                    for session_data in data.get('completed_sessions', []):
                        session = GeminiSession(**session_data)
                        # Convert string datetime back to datetime objects
                        session.start_time = datetime.fromisoformat(session_data['start_time'])
                        if session_data.get('end_time'):
                            session.end_time = datetime.fromisoformat(session_data['end_time'])
                        session.mode = ResearchMode(session_data['mode'])
                        self.completed_sessions.append(session)
                logger.info(f"📚 Loaded {len(self.completed_sessions)} previous sessions")
            except Exception as e:
                logger.warning(f"Could not load session history: {e}")
    
    def _save_session_history(self):
        """Save session history to persistent storage."""
        # Convert sessions to serializable format
        serializable_sessions = []
        for session in self.completed_sessions:
            session_dict = asdict(session)
            session_dict['start_time'] = session.start_time.isoformat()
            if session.end_time:
                session_dict['end_time'] = session.end_time.isoformat()
            session_dict['mode'] = session.mode.value
            serializable_sessions.append(session_dict)
        
        data = {
            'completed_sessions': serializable_sessions,
            'last_updated': datetime.now().isoformat()
        }
        
        with open(self.sessions_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _create_prompt_templates(self):
        """Create standardized prompt templates for different research modes."""
        templates = {
            'hypothesis_generation': """
# Gemini Hypothesis Generation Session

## Research Context
{research_focus}

## Objective
Generate novel, testable hypotheses that address current research gaps.

## Analysis Framework
1. **Literature Gap Assessment**: What aspects are understudied?
2. **Methodological Innovation**: What new approaches could advance the field?
3. **Cross-Disciplinary Insights**: What insights from other fields apply?
4. **Breakthrough Potential**: What hypotheses could lead to significant advances?

## Expected Outputs
- 3-5 novel hypotheses with strong theoretical foundations
- Testability assessment for each hypothesis
- Experimental design recommendations
- Expected impact and significance evaluation

## Prompt for Gemini
Please analyze the research context above and generate novel hypotheses following the framework provided. Focus on genuinely innovative ideas that could advance scientific understanding.
""",
            
            'literature_analysis': """
# Gemini Literature Analysis Session

## Research Focus
{research_focus}

## Objective
Comprehensive analysis of current literature to identify patterns, gaps, and opportunities.

## Analysis Framework
1. **Current State Assessment**: What is the current consensus?
2. **Methodological Trends**: What approaches are being used?
3. **Knowledge Gaps**: What questions remain unanswered?
4. **Conflicting Evidence**: What controversies exist?
5. **Future Directions**: What opportunities for advancement exist?

## Expected Outputs
- Comprehensive literature synthesis
- Gap identification with specificity
- Methodological assessment and recommendations
- Research priority recommendations

## Prompt for Gemini
Please conduct a comprehensive literature analysis of the research focus above, following the structured framework to identify gaps and opportunities.
""",
            
            'experimental_design': """
# Gemini Experimental Design Session

## Research Hypothesis
{research_focus}

## Objective
Design rigorous experimental methodology to test the specified hypothesis.

## Design Framework
1. **Variable Identification**: Independent, dependent, and control variables
2. **Experimental Controls**: What controls are necessary?
3. **Measurement Strategy**: How will variables be measured?
4. **Statistical Framework**: What analyses will be performed?
5. **Feasibility Assessment**: What resources and constraints exist?

## Expected Outputs
- Detailed experimental protocol
- Statistical analysis plan
- Resource requirements assessment
- Risk analysis and mitigation strategies

## Prompt for Gemini
Please design a comprehensive experimental methodology for testing the hypothesis above, ensuring scientific rigor and practical feasibility.
"""
        }
        
        for mode, template in templates.items():
            template_file = self.templates_dir / f"{mode}_template.md"
            with open(template_file, 'w') as f:
                f.write(template)
    
    def start_research_session(self, 
                             mode: ResearchMode, 
                             research_focus: str,
                             coordination: Optional[ResearchCoordination] = None) -> str:
        """
        Start a new Gemini research session with structured guidance.
        
        Args:
            mode: Research session mode (hypothesis generation, literature analysis, etc.)
            research_focus: Specific research question or topic
            coordination: Optional coordination with other systems
            
        Returns:
            session_id: Unique identifier for tracking the session
        """
        session_id = f"gemini_{mode.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        session = GeminiSession(
            session_id=session_id,
            mode=mode,
            research_focus=research_focus,
            start_time=datetime.now()
        )
        
        self.active_sessions[session_id] = session
        
        # Create session directory
        session_dir = self.output_dir / session_id
        session_dir.mkdir(exist_ok=True)
        
        # Generate customized prompt
        self._generate_session_prompt(session, coordination, session_dir)
        
        # Display session initiation information
        self._display_session_start_info(session, coordination, session_dir)
        
        logger.info(f"🚀 Started Gemini session: {session_id}")
        logger.info(f"📋 Mode: {mode.value}")
        logger.info(f"🎯 Focus: {research_focus}")
        
        return session_id
    
    def _generate_session_prompt(self, 
                                session: GeminiSession, 
                                coordination: Optional[ResearchCoordination],
                                session_dir: Path):
        """Generate customized prompt for the research session."""
        # Load template
        template_file = self.templates_dir / f"{session.mode.value}_template.md"
        if template_file.exists():
            with open(template_file, 'r') as f:
                template = f.read()
        else:
            template = "# Gemini Research Session\n\n## Research Focus\n{research_focus}\n\nPlease analyze the research focus and provide comprehensive insights."
        
        # Customize template
        customized_prompt = template.format(research_focus=session.research_focus)
        
        # Add coordination information if provided
        if coordination:
            coordination_info = f"""
## Multi-System Coordination

**Primary System**: {coordination.primary_system}
**Supporting Systems**: {', '.join(coordination.supporting_systems)}
**Research Objective**: {coordination.research_objective}
**Expected Timeline**: {coordination.expected_timeline}
**Deliverables**: {', '.join(coordination.deliverables)}
**Integration Points**: {', '.join(coordination.integration_points)}

Please consider how your analysis integrates with the other systems mentioned above.
"""
            customized_prompt += coordination_info
        
        # Save prompt to session directory
        prompt_file = session_dir / "gemini_prompt.md"
        with open(prompt_file, 'w') as f:
            f.write(customized_prompt)
        
        session.prompts_used.append(str(prompt_file))
    
    def _display_session_start_info(self, 
                                   session: GeminiSession,
                                   coordination: Optional[ResearchCoordination],
                                   session_dir: Path):
        """Display comprehensive session start information."""
        print("\n" + "="*80)
        print("🔬 GEMINI DEEP RESEARCH SESSION INITIATED")
        print("="*80)
        print(f"📋 Session ID: {session.session_id}")
        print(f"🎯 Research Mode: {session.mode.value.upper()}")
        print(f"📅 Start Time: {session.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🎯 Research Focus: {session.research_focus}")
        print(f"📁 Session Directory: {session_dir}")
        
        if coordination:
            print(f"\n🔗 MULTI-SYSTEM COORDINATION:")
            print(f"   Primary System: {coordination.primary_system}")
            print(f"   Supporting Systems: {', '.join(coordination.supporting_systems)}")
            print(f"   Objective: {coordination.research_objective}")
        
        print(f"\n📝 NEXT STEPS:")
        print(f"   1. Open Gemini at: https://gemini.google.com/")
        print(f"   2. Copy prompt from: {session_dir}/gemini_prompt.md")
        print(f"   3. Conduct research session")
        print(f"   4. Use complete_session() to document results")
        
        print(f"\n💡 SESSION GUIDANCE:")
        print(f"   - Focus on {session.mode.value.replace('_', ' ')} objectives")
        print(f"   - Document key insights systematically")
        print(f"   - Consider integration with pipeline systems")
        print(f"   - Aim for actionable, specific recommendations")
        
        print("="*80)
        
        # Also save this information to a session info file
        info_file = session_dir / "session_info.md"
        with open(info_file, 'w') as f:
            f.write(f"# Gemini Session Information\n\n")
            f.write(f"**Session ID**: {session.session_id}\n")
            f.write(f"**Mode**: {session.mode.value}\n")
            f.write(f"**Start Time**: {session.start_time}\n")
            f.write(f"**Research Focus**: {session.research_focus}\n\n")
            if coordination:
                f.write(f"## Coordination\n")
                f.write(f"- Primary System: {coordination.primary_system}\n")
                f.write(f"- Supporting Systems: {', '.join(coordination.supporting_systems)}\n")
                f.write(f"- Objective: {coordination.research_objective}\n\n")
    
    def complete_session(self, 
                        session_id: str,
                        output_summary: str,
                        key_insights: List[str],
                        follow_up_questions: Optional[List[str]] = None,
                        integration_notes: str = "",
                        quality_rating: Optional[int] = None) -> Dict[str, Any]:
        """
        Complete an active research session and document results.
        
        Args:
            session_id: Session identifier
            output_summary: Comprehensive summary of research results
            key_insights: List of key insights discovered
            follow_up_questions: Optional follow-up questions for future research
            integration_notes: Notes on integration with other systems
            quality_rating: Optional quality rating (1-10)
            
        Returns:
            session_results: Structured session results for pipeline integration
        """
        if session_id not in self.active_sessions:
            raise ValueError(f"Session {session_id} not found in active sessions")
        
        session = self.active_sessions[session_id]
        session.end_time = datetime.now()
        session.output_summary = output_summary
        session.key_insights = key_insights
        session.follow_up_questions = follow_up_questions or []
        session.integration_notes = integration_notes
        session.quality_rating = quality_rating
        
        # Save session results
        session_dir = self.output_dir / session_id
        self._save_session_results(session, session_dir)
        
        # Move to completed sessions
        self.completed_sessions.append(session)
        del self.active_sessions[session_id]
        
        # Save updated history
        self._save_session_history()
        
        # Generate structured results for pipeline integration
        session_results = self._generate_integration_results(session)
        
        logger.info(f"✅ Completed Gemini session: {session_id}")
        logger.info(f"⏱️ Duration: {session.end_time - session.start_time}")
        logger.info(f"🎯 Insights generated: {len(key_insights)}")
        
        # Display completion summary
        self._display_session_completion(session, session_results)
        
        return session_results
    
    def _save_session_results(self, session: GeminiSession, session_dir: Path):
        """Save comprehensive session results to files."""
        # Save structured session data
        session_data = asdict(session)
        session_data['start_time'] = session.start_time.isoformat()
        if session.end_time:
            session_data['end_time'] = session.end_time.isoformat()
        session_data['mode'] = session.mode.value
        
        with open(session_dir / "session_results.json", 'w') as f:
            json.dump(session_data, f, indent=2)
        
        # Save formatted results summary
        results_md = f"""# Gemini Research Session Results

## Session Information
- **Session ID**: {session.session_id}
- **Mode**: {session.mode.value}
- **Start Time**: {session.start_time}
- **End Time**: {session.end_time}
- **Duration**: {session.end_time - session.start_time if session.end_time else 'In Progress'}
- **Quality Rating**: {session.quality_rating}/10

## Research Focus
{session.research_focus}

## Output Summary
{session.output_summary}

## Key Insights
"""
        for i, insight in enumerate(session.key_insights, 1):
            results_md += f"{i}. {insight}\n"
        
        if session.follow_up_questions:
            results_md += "\n## Follow-up Questions\n"
            for i, question in enumerate(session.follow_up_questions, 1):
                results_md += f"{i}. {question}\n"
        
        if session.integration_notes:
            results_md += f"\n## Integration Notes\n{session.integration_notes}\n"
        
        with open(session_dir / "results_summary.md", 'w') as f:
            f.write(results_md)
    
    def _generate_integration_results(self, session: GeminiSession) -> Dict[str, Any]:
        """Generate structured results for pipeline integration."""
        return {
            'session_id': session.session_id,
            'mode': session.mode.value,
            'research_focus': session.research_focus,
            'duration_minutes': (session.end_time - session.start_time).total_seconds() / 60,
            'key_insights': session.key_insights,
            'output_summary': session.output_summary,
            'follow_up_questions': session.follow_up_questions,
            'integration_notes': session.integration_notes,
            'quality_rating': session.quality_rating,
            'timestamp': session.end_time.isoformat(),
            'pipeline_integration': {
                'ready_for_verification': session.mode in [ResearchMode.HYPOTHESIS_GENERATION, ResearchMode.EXPERIMENTAL_DESIGN],
                'supports_hypothesis_generation': session.mode == ResearchMode.HYPOTHESIS_GENERATION,
                'provides_literature_analysis': session.mode == ResearchMode.LITERATURE_ANALYSIS,
                'experimental_design_ready': session.mode == ResearchMode.EXPERIMENTAL_DESIGN
            }
        }
    
    def _display_session_completion(self, session: GeminiSession, results: Dict[str, Any]):
        """Display session completion summary."""
        print("\n" + "="*80)
        print("✅ GEMINI RESEARCH SESSION COMPLETED")
        print("="*80)
        print(f"📋 Session ID: {session.session_id}")
        print(f"⏱️ Duration: {session.end_time - session.start_time}")
        print(f"🎯 Quality Rating: {session.quality_rating}/10" if session.quality_rating else "🎯 Quality Rating: Not provided")
        print(f"💡 Key Insights: {len(session.key_insights)}")
        
        if session.follow_up_questions:
            print(f"❓ Follow-up Questions: {len(session.follow_up_questions)}")
        
        print(f"\n📊 PIPELINE INTEGRATION STATUS:")
        integration = results['pipeline_integration']
        print(f"   ✅ Ready for Verification: {integration['ready_for_verification']}")
        print(f"   🧪 Supports Hypothesis Generation: {integration['supports_hypothesis_generation']}")
        print(f"   📚 Provides Literature Analysis: {integration['provides_literature_analysis']}")
        print(f"   🔬 Experimental Design Ready: {integration['experimental_design_ready']}")
        
        print(f"\n💾 Results saved to: {self.output_dir}/{session.session_id}/")
        print("="*80)
    
    def get_session_summary(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get summary of a completed session."""
        for session in self.completed_sessions:
            if session.session_id == session_id:
                return self._generate_integration_results(session)
        return None
    
    def list_sessions(self, mode: Optional[ResearchMode] = None) -> List[Dict[str, Any]]:
        """List all sessions, optionally filtered by mode."""
        sessions = []
        for session in self.completed_sessions:
            if mode is None or session.mode == mode:
                sessions.append({
                    'session_id': session.session_id,
                    'mode': session.mode.value,
                    'research_focus': session.research_focus,
                    'start_time': session.start_time.isoformat(),
                    'duration_minutes': (session.end_time - session.start_time).total_seconds() / 60 if session.end_time else None,
                    'quality_rating': session.quality_rating,
                    'insights_count': len(session.key_insights)
                })
        return sorted(sessions, key=lambda x: x['start_time'], reverse=True)
    
    def coordinate_multi_system_research(self, 
                                       primary_objective: str,
                                       systems_config: Dict[str, Dict[str, Any]]) -> str:
        """
        Coordinate research across multiple systems with Gemini as facilitator.
        
        Args:
            primary_objective: Overall research objective
            systems_config: Configuration for each system's role
            
        Returns:
            coordination_id: Unique identifier for the coordinated research
        """
        coordination_id = f"multi_coord_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print("\n" + "="*80)
        print("🔗 MULTI-SYSTEM RESEARCH COORDINATION")
        print("="*80)
        print(f"🎯 Primary Objective: {primary_objective}")
        print(f"📋 Coordination ID: {coordination_id}")
        
        print(f"\n🛠️ SYSTEM CONFIGURATION:")
        for system, config in systems_config.items():
            print(f"   {system.upper()}: {config.get('role', 'Not specified')}")
        
        print(f"\n📋 RECOMMENDED WORKFLOW:")
        if 'gemini' in systems_config:
            print(f"   1. Start Gemini session for {systems_config['gemini'].get('mode', 'analysis')}")
        if 'oxford' in systems_config:
            print(f"   2. Utilize Oxford system for {systems_config['oxford'].get('role', 'literature analysis')}")
        if 'sakana' in systems_config:
            print(f"   3. Generate hypotheses via Sakana {systems_config['sakana'].get('role', 'hypothesis generation')}")
        if 'ursa' in systems_config:
            print(f"   4. Verify results with URSA {systems_config['ursa'].get('role', 'verification')}")
        
        print("="*80)
        
        # Save coordination plan
        coord_dir = self.output_dir / f"coordination_{coordination_id}"
        coord_dir.mkdir(exist_ok=True)
        
        coordination_plan = {
            'coordination_id': coordination_id,
            'primary_objective': primary_objective,
            'systems_config': systems_config,
            'created_at': datetime.now().isoformat(),
            'status': 'initiated'
        }
        
        with open(coord_dir / "coordination_plan.json", 'w') as f:
            json.dump(coordination_plan, f, indent=2)
        
        logger.info(f"🔗 Initiated multi-system coordination: {coordination_id}")
        return coordination_id


def main():
    """Example usage and testing of Gemini automation wrapper."""
    # Initialize wrapper
    wrapper = GeminiAutomationWrapper()
    
    # Example: Start hypothesis generation session
    print("🧪 Example: Starting hypothesis generation session...")
    session_id = wrapper.start_research_session(
        mode=ResearchMode.HYPOTHESIS_GENERATION,
        research_focus="Novel approaches to marine cloud brightening with minimal environmental impact"
    )
    
    print(f"\n📋 Session {session_id} started. In practice, you would:")
    print("1. Use the generated prompt in Gemini")
    print("2. Conduct research")
    print("3. Call complete_session() with results")
    
    # Example: Multi-system coordination
    print("\n🔗 Example: Multi-system coordination...")
    coord_id = wrapper.coordinate_multi_system_research(
        primary_objective="Develop novel Arctic SAI governance framework",
        systems_config={
            'gemini': {'mode': 'literature_analysis', 'role': 'Policy analysis and framework design'},
            'oxford': {'role': 'Literature gap identification from 1171 PDFs'},
            'sakana': {'role': 'Automated hypothesis generation for governance mechanisms'},
            'ursa': {'role': 'Experimental verification of proposed frameworks'}
        }
    )
    
    print(f"\n✅ Multi-system coordination {coord_id} initiated")


if __name__ == "__main__":
    main()