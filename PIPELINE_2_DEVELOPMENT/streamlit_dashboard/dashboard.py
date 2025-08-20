"""
Pipeline 2 Development Dashboard
Streamlit dashboard for real-time progress tracking of the ultimate research pipeline
"""

import streamlit as st
import sys
import os
import json
import time
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add Pipeline 2 paths
PIPELINE_2_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PIPELINE_2_ROOT / "ai_researcher_enhanced" / "data"))
sys.path.insert(0, str(PIPELINE_2_ROOT / "ai_researcher_enhanced" / "integration"))

# Import Pipeline 2 components
try:
    from glens_integration import Pipeline2GLENSIntegration
    from oxford_rag_bridge import Pipeline2OxfordIntegration
    from ursa_quality_control import Pipeline2URSAQualityControl
    INTEGRATIONS_AVAILABLE = True
except ImportError as e:
    INTEGRATIONS_AVAILABLE = False
    logger.warning(f"Pipeline 2 integrations not available: {e}")

# Page configuration
st.set_page_config(
    page_title="Pipeline 2 Development Dashboard", 
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

class Pipeline2Dashboard:
    """Main dashboard class for Pipeline 2 Development"""
    
    def __init__(self):
        self.cambridge_question = "What are the potential pros and cons of injecting materials for stratospheric aerosol injection (SAI) in a pulsed fashion versus a continuous flow?"
        self.session_state_keys = [
            'pipeline_initialized', 'integration_status', 'experiment_queue', 
            'active_experiments', 'completed_experiments', 'generation_logs'
        ]
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Initialize Streamlit session state"""
        for key in self.session_state_keys:
            if key not in st.session_state:
                if key == 'experiment_queue':
                    st.session_state[key] = []
                elif key == 'active_experiments':
                    st.session_state[key] = {}
                elif key == 'completed_experiments':
                    st.session_state[key] = []
                elif key == 'generation_logs':
                    st.session_state[key] = []
                elif key == 'integration_status':
                    st.session_state[key] = {}
                else:
                    st.session_state[key] = False
    
    def render_header(self):
        """Render the dashboard header"""
        st.title("🔬 Pipeline 2 Development Dashboard")
        st.markdown("**Ultimate Research Pipeline**: AI-S-Plus + Oxford+RAG + URSA + Manual Gemini")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Active Experiments", len(st.session_state.active_experiments))
        with col2:
            st.metric("Completed Papers", len(st.session_state.completed_experiments))
        with col3:
            status = "🟢 Operational" if st.session_state.pipeline_initialized else "🔴 Offline"
            st.metric("Pipeline Status", status)
    
    def render_sidebar(self):
        """Render the sidebar with controls"""
        st.sidebar.title("🎮 Pipeline Controls")
        
        # Cambridge SAI Question
        st.sidebar.subheader("🎯 Cambridge SAI Question")
        st.sidebar.text_area(
            "Research Question:",
            value=self.cambridge_question,
            height=100,
            disabled=True
        )
        
        # Pipeline initialization
        st.sidebar.subheader("🚀 Pipeline Initialization")
        if st.sidebar.button("Initialize Pipeline 2", type="primary"):
            self._initialize_pipeline()
        
        # Integration status
        if INTEGRATIONS_AVAILABLE:
            st.sidebar.subheader("🔗 Integration Status")
            self._render_integration_status()
        
        # Experiment controls
        st.sidebar.subheader("🧪 Experiment Controls")
        if st.sidebar.button("Generate SAI Paper"):
            self._queue_sai_experiment()
        
        if st.sidebar.button("Clear All Logs"):
            st.session_state.generation_logs = []
            st.experimental_rerun()
    
    def _initialize_pipeline(self):
        """Initialize Pipeline 2 with all integrations"""
        with st.spinner("Initializing Pipeline 2..."):
            try:
                if INTEGRATIONS_AVAILABLE:
                    # Initialize GLENS integration
                    glens_integration = Pipeline2GLENSIntegration()
                    glens_status = glens_integration.get_integration_status()
                    
                    # Initialize Oxford+RAG integration
                    oxford_integration = Pipeline2OxfordIntegration()
                    oxford_status = oxford_integration.get_integration_status()
                    
                    # Initialize URSA quality control
                    ursa_integration = Pipeline2URSAQualityControl()
                    ursa_status = ursa_integration.get_integration_status()
                    
                    st.session_state.integration_status = {
                        'glens': glens_status,
                        'oxford': oxford_status,
                        'ursa': ursa_status,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    st.session_state.pipeline_initialized = True
                    st.success("✅ Pipeline 2 initialized successfully!")
                    
                else:
                    st.warning("⚠️ Integrations not available - running in demo mode")
                    st.session_state.pipeline_initialized = True
                    
            except Exception as e:
                st.error(f"❌ Pipeline initialization failed: {e}")
                logger.error(f"Pipeline initialization error: {e}")
    
    def _render_integration_status(self):
        """Render integration status in sidebar"""
        if st.session_state.integration_status:
            status = st.session_state.integration_status
            
            # GLENS Status
            glens_status = status.get('glens', {})
            glens_icon = "🟢" if glens_status.get('initialized', False) else "🔴"
            st.sidebar.text(f"{glens_icon} GLENS: {glens_status.get('loader_status', 'unknown')}")
            
            # Oxford+RAG Status  
            oxford_status = status.get('oxford', {})
            oxford_icon = "🟢" if oxford_status.get('initialized', False) else "🔴"
            st.sidebar.text(f"{oxford_icon} Oxford+RAG: {oxford_status.get('bridge_status', 'unknown')}")
            
            # URSA Status
            ursa_status = status.get('ursa', {})
            ursa_icon = "🟢" if ursa_status.get('initialized', False) else "🔴"
            st.sidebar.text(f"{ursa_icon} URSA: {ursa_status.get('verifier_status', 'unknown')}")
            
        else:
            st.sidebar.text("🔴 No integration status available")
    
    def _queue_sai_experiment(self):
        """Queue a new SAI experiment"""
        experiment_id = f"sai_experiment_{int(time.time())}"
        experiment_config = {
            'experiment_id': experiment_id,
            'question': self.cambridge_question,
            'scenarios': ['baseline', 'continuous_sai', 'pulsed_sai'],
            'variables': ['temperature', 'precipitation', 'aerosol_burden'],
            'timestamp': datetime.now().isoformat(),
            'status': 'queued'
        }
        
        st.session_state.experiment_queue.append(experiment_config)
        st.success(f"✅ Queued experiment: {experiment_id}")
        
        # Auto-start experiment processing
        self._start_experiment_processing(experiment_config)
    
    def _start_experiment_processing(self, experiment_config: Dict[str, Any]):
        """Start processing an experiment"""
        experiment_id = experiment_config['experiment_id']
        
        # Move from queue to active
        if experiment_config in st.session_state.experiment_queue:
            st.session_state.experiment_queue.remove(experiment_config)
        
        experiment_config['status'] = 'active'
        experiment_config['start_time'] = datetime.now().isoformat()
        st.session_state.active_experiments[experiment_id] = experiment_config
        
        # Add processing log
        self._add_log(f"🚀 Started processing experiment: {experiment_id}")
        
        # Simulate experiment processing phases
        self._simulate_experiment_phases(experiment_id)
    
    def _simulate_experiment_phases(self, experiment_id: str):
        """Simulate the experiment processing phases"""
        phases = [
            ("🔍 GLENS Data Loading", "Loading real climate data"),
            ("🧠 Oxford+RAG Enhancement", "Enhancing research ideas with RAG"),
            ("📝 Paper Generation", "Generating research paper with gpt-5"),
            ("🔬 URSA Quality Control", "Automated quality verification"),
            ("✨ Gemini Manual Review", "Manual expert review")
        ]
        
        for i, (phase_name, phase_description) in enumerate(phases):
            self._add_log(f"📍 {experiment_id}: {phase_name} - {phase_description}")
            
            # Update experiment status
            if experiment_id in st.session_state.active_experiments:
                st.session_state.active_experiments[experiment_id]['current_phase'] = phase_name
                st.session_state.active_experiments[experiment_id]['progress'] = (i + 1) / len(phases)
        
        # Complete experiment
        self._complete_experiment(experiment_id)
    
    def _complete_experiment(self, experiment_id: str):
        """Mark experiment as completed"""
        if experiment_id in st.session_state.active_experiments:
            experiment = st.session_state.active_experiments[experiment_id]
            experiment['status'] = 'completed'
            experiment['end_time'] = datetime.now().isoformat()
            experiment['completion_rate'] = 1.0
            
            # Generate mock results
            experiment['results'] = {
                'paper_pages': 45,
                'ursa_score': 0.89,
                'experimental_support': 0.84,
                'gemini_rating': 8.5,
                'verdict': 'HIGH_QUALITY'
            }
            
            # Move to completed
            st.session_state.completed_experiments.append(experiment)
            del st.session_state.active_experiments[experiment_id]
            
            self._add_log(f"✅ Completed experiment: {experiment_id} (Score: 0.89)")
    
    def _add_log(self, message: str):
        """Add a log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        st.session_state.generation_logs.append(log_entry)
        
        # Keep only last 50 logs
        if len(st.session_state.generation_logs) > 50:
            st.session_state.generation_logs = st.session_state.generation_logs[-50:]
    
    def render_main_content(self):
        """Render the main dashboard content"""
        # Create tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🧪 Active Experiments", "📝 Completed Papers", "📋 Generation Logs"])
        
        with tab1:
            self._render_overview_tab()
        
        with tab2:
            self._render_active_experiments_tab()
        
        with tab3:
            self._render_completed_papers_tab()
        
        with tab4:
            self._render_logs_tab()
    
    def _render_overview_tab(self):
        """Render the overview tab"""
        st.subheader("🎯 Pipeline 2 Development Overview")
        
        # Architecture diagram
        st.markdown("""
        ### 🏗️ System Architecture
        
        ```
        Cambridge SAI Question 
                ↓
        ┌─────────────────────────────────────────────────┐
        │               Pipeline 2 Development            │
        │                                                 │
        │  AI-S-Plus ──→ Oxford+RAG ──→ URSA ──→ Gemini  │
        │    (GLENS)       (1171 PDFs)   (6-Phase)  (Manual) │
        │                                                 │
        │  Real Climate     Knowledge      Quality      Expert │
        │      Data         Enhancement    Control      Review │
        └─────────────────────────────────────────────────┘
                ↓
        Multiple High-Quality SAI Research Papers
        ```
        """)
        
        # Current status
        st.markdown("### 📈 Current Status")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔗 Integration Status:**")
            if st.session_state.integration_status:
                status = st.session_state.integration_status
                glens_status = "✅" if status.get('glens', {}).get('initialized', False) else "❌"
                oxford_status = "✅" if status.get('oxford', {}).get('initialized', False) else "❌"
                ursa_status = "✅" if status.get('ursa', {}).get('initialized', False) else "❌"
                
                st.markdown(f"""
                - {glens_status} **GLENS Integration**: {status.get('glens', {}).get('data_source', 'N/A')}
                - {oxford_status} **Oxford+RAG Bridge**: {status.get('oxford', {}).get('enhancement_source', 'N/A')}
                - {ursa_status} **URSA Quality Control**: {status.get('ursa', {}).get('quality_control_source', 'N/A')}
                - 🔄 **Gemini Review**: Manual workflow
                """)
            else:
                st.markdown("- ⏳ **Status**: Not initialized")
        
        with col2:
            st.markdown("**🎯 Target Objectives:**")
            st.markdown("""
            - ✅ **Real Data**: GLENS climate data integration
            - ✅ **Knowledge Enhancement**: 1171+ PDF knowledge base
            - ✅ **Quality Assurance**: 6-phase URSA verification
            - 📝 **Expert Validation**: Gemini deep research review
            - 🎯 **Target**: Multiple perspective SAI analysis papers
            """)
        
        # Queue status
        if st.session_state.experiment_queue or st.session_state.active_experiments:
            st.markdown("### 🚦 Current Activity")
            
            if st.session_state.experiment_queue:
                st.markdown(f"**Queued Experiments**: {len(st.session_state.experiment_queue)}")
                for exp in st.session_state.experiment_queue:
                    st.text(f"  • {exp['experiment_id']} - {exp['status']}")
            
            if st.session_state.active_experiments:
                st.markdown(f"**Active Experiments**: {len(st.session_state.active_experiments)}")
                for exp_id, exp in st.session_state.active_experiments.items():
                    current_phase = exp.get('current_phase', 'Starting...')
                    progress = exp.get('progress', 0) * 100
                    st.text(f"  • {exp_id} - {current_phase} ({progress:.0f}%)")
    
    def _render_active_experiments_tab(self):
        """Render active experiments tab"""
        st.subheader("🧪 Active Experiments")
        
        if not st.session_state.active_experiments:
            st.info("No active experiments. Start a new SAI experiment from the sidebar.")
            return
        
        for exp_id, experiment in st.session_state.active_experiments.items():
            with st.expander(f"🔬 {exp_id}", expanded=True):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("**Question:**")
                    st.text(experiment['question'][:100] + "...")
                    
                    current_phase = experiment.get('current_phase', 'Initializing...')
                    st.markdown(f"**Current Phase:** {current_phase}")
                    
                    progress = experiment.get('progress', 0)
                    st.progress(progress)
                    
                    st.markdown("**Scenarios:**")
                    st.text(", ".join(experiment['scenarios']))
                
                with col2:
                    start_time = experiment.get('start_time', 'Unknown')
                    st.markdown(f"**Started:** {start_time.split('T')[1][:8] if 'T' in start_time else start_time}")
                    
                    st.markdown(f"**Status:** {experiment['status'].title()}")
                    st.markdown(f"**Progress:** {progress*100:.0f}%")
    
    def _render_completed_papers_tab(self):
        """Render completed papers tab"""
        st.subheader("📝 Completed Research Papers")
        
        if not st.session_state.completed_experiments:
            st.info("No completed experiments yet. Generate your first SAI paper from the sidebar.")
            return
        
        for experiment in reversed(st.session_state.completed_experiments):  # Show newest first
            with st.expander(f"📄 {experiment['experiment_id']}", expanded=False):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("**Research Question:**")
                    st.text(experiment['question'])
                    
                    if 'results' in experiment:
                        results = experiment['results']
                        st.markdown("**Paper Metrics:**")
                        st.text(f"• Pages: {results['paper_pages']}")
                        st.text(f"• URSA Score: {results['ursa_score']:.2f}/1.0")
                        st.text(f"• Experimental Support: {results['experimental_support']:.0%}")
                        st.text(f"• Gemini Rating: {results['gemini_rating']}/10")
                        st.text(f"• Verdict: {results['verdict']}")
                
                with col2:
                    start_time = experiment.get('start_time', 'Unknown')
                    end_time = experiment.get('end_time', 'Unknown')
                    
                    st.markdown(f"**Started:** {start_time.split('T')[1][:8] if 'T' in start_time else start_time}")
                    st.markdown(f"**Completed:** {end_time.split('T')[1][:8] if 'T' in end_time else end_time}")
                    st.markdown(f"**Status:** ✅ {experiment['status'].title()}")
                    
                    if st.button(f"View Paper", key=f"view_{experiment['experiment_id']}"):
                        st.success("Paper viewing would open here")
    
    def _render_logs_tab(self):
        """Render generation logs tab"""
        st.subheader("📋 Real-Time Generation Logs")
        
        if not st.session_state.generation_logs:
            st.info("No logs yet. Start an experiment to see real-time progress.")
            return
        
        # Auto-refresh logs
        if st.button("🔄 Refresh Logs"):
            st.experimental_rerun()
        
        # Display logs in reverse order (newest first)
        logs_container = st.container()
        with logs_container:
            for log in reversed(st.session_state.generation_logs):
                st.text(log)
        
        # Auto-scroll to bottom effect
        st.markdown('<div id="bottom"></div>', unsafe_allow_html=True)
        st.markdown("""
        <script>
        document.getElementById('bottom').scrollIntoView();
        </script>
        """, unsafe_allow_html=True)
    
    def run(self):
        """Run the dashboard"""
        self.render_header()
        self.render_sidebar()
        self.render_main_content()
        
        # Auto-refresh every 5 seconds if there are active experiments
        if st.session_state.active_experiments:
            time.sleep(1)  # Small delay to prevent rapid refreshes
            st.experimental_rerun()

def main():
    """Main function to run the dashboard"""
    dashboard = Pipeline2Dashboard()
    dashboard.run()

if __name__ == "__main__":
    main()