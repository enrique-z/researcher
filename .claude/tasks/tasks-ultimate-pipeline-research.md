# 🎯 **ULTIMATE PIPELINE RESEARCH TASK LIST - Super-Paper Generation System**
*Generated from: ultimate-pipeline-research-plan_2025-08-15_1339.md*  
*Date: 2025-08-15*  
*Mission: Integrate 5 codebases into definitive research system for Cambridge SAI analysis*

## **📋 PROJECT OVERVIEW**

**Objective**: Create the ultimate AI research pipeline by integrating:
1. **Researcher (Hangzhou)** - Eloquent 128-page papers per each experiment/hypothese
2. **AI-S-Plus (Sakana)** - Real calculations with GLENS data for each experiment/hypothese
3. **URSA (LANL)** - Multi-agent workflow system
4. **Oxford + RAG** - 1100 PDFs corpus for novelty
5. **Gemini 2.5 Pro** - Quality control automation

**Critical Goal**: Solve Cambridge professor's SAI pulse vs continuous flow analysis with breakthrough quality, by providing him several experiments and hypotheses, so we must create a pipeline that creates seamless papers with experiments that solve his question. 

**Timeline**: 6-8 hours for complete strategic analysis + implementation roadmap

Always check that there is already a plan to do pipeline 2 /Users/apple/code/Researcher/.claude/doc/pipeline2-overview_2025-08-15_1101.md  but it is not yet finished.  /Users/apple/code/Researcher/PIPELINE_2_DEVELOPMENT/PIPELINE_2_TASKS.md  and  here /Users/apple/code/Researcher/PIPELINE_2_DEVELOPMENT

---

## **Phase 1: Deep Codebase Analysis (Priority: Critical)**
*Duration: 3-4 hours | Critical Path | Must Complete First*

### Task 1.0
check that there is already a plan to do pipeline 2 so check how to use some of the existing code and tasks and plan and improve it with the new findings  /Users/apple/code/Researcher/.claude/doc/pipeline2-overview_2025-08-15_1101.md  but it is not yet finished.  /Users/apple/code/Researcher/PIPELINE_2_DEVELOPMENT/PIPELINE_2_TASKS.md  and  here /Users/apple/code/Researcher/PIPELINE_2_DEVELOPMENT


### Task 1.1: AI-S-Plus GLENS Data Loader Deep Analysis (Priority: Critical)
- **Description**: Reverse-engineer how AI-S-Plus loads and processes real GLENS/GeoMIP climate data to understand integration requirements
- **Files to Analyze**:
  ```
  /Users/apple/code/ai-s-plus/AI-Scientist-v2/core/ai_scientist/utils/glens_loader.py
  /Users/apple/code/ai-s-plus/AI-Scientist-v2/core/ai_scientist/utils/ (entire directory)
  ```
- **MCP Tools Required**: Sequential thinking for code analysis, Task agent for deep understanding
- **Research Questions**:
  - How does GLENS loader download and process NetCDF climate data?
  - What's the data chunking mechanism for large datasets (>1GB)?
  - How does it differentiate GLENS vs GeoMIP vs ARISE-SAI datasets?
  - What API interfaces exist for external integration?
  - How can this module be extracted for Researcher integration?
- **Deliverables**:
  - Complete GLENS loader specification document
  - Data flow diagram and processing pipeline
  - Module extraction feasibility assessment
  - Integration interface requirements
- **Acceptance Criteria**: 
  - Document every function and class in glens_loader.py
  - Understand complete data processing workflow
  - Identify extraction points for Researcher integration
- **Estimated Time**: 1.5 hours
- **Dependencies**: None (start immediately)

### Task 1.2: BFTS vs Monte Carlo Calculation Engine Analysis (Priority: Critical)
- **Description**: Analyze existing BFTS implementation and research Monte Carlo alternatives for scientific calculations
- **Files to Research**:
  ```
  /Users/apple/code/ai-s-plus/AI-Scientist-v2/core/ai_scientist/analysis/ (find BFTS implementation)
  /Users/apple/code/ai-s-plus/AI-Scientist-v2/ (search for calculation engines)
  ```
- **MCP Tools Required**: Perplexity for external research, Task agent for code analysis
- **Research Topics**:
  - "BFTS vs Monte Carlo Tree Search for scientific calculations 2025"
  - "Real-time physics calculation methods climate science"
  - "Online scientific calculation APIs stratospheric aerosol injection"
- **Deliverables**:
  - BFTS implementation analysis report
  - Monte Carlo vs BFTS comparison matrix
  - Online calculation services evaluation
  - Recommendation for optimal calculation method
- **Acceptance Criteria**:
  - Understand current BFTS computational requirements
  - Provide quantitative comparison (speed, accuracy, complexity)
  - Recommend specific implementation approach
- **Estimated Time**: 1 hour
- **Dependencies**: None

### Task 1.3: Hallucination Problem Root Cause Analysis (Priority: Critical)
- **Description**: Investigate why AI-S-Plus hallucinates despite real data availability and design prevention strategies
- **Files to Study**:
  ```
  /Users/apple/code/ai-s-plus/FINAL-SOLUTION-IMPLEMENTATION-PLAN.md
  /Users/apple/code/ai-s-plus/opinions gemini + openai including DEVASTATING-OPINION-FIRST-SAKANA/hard-critic-codebase.md
  /Users/apple/code/ai-s-plus/opinions gemini + openai including DEVASTATING-OPINION-FIRST-SAKANA/gemini 2.5 opinion 7 experiments.json
  ```
- **MCP Tools Required**: Task agent for document analysis, Sequential thinking for pattern recognition
- **Research Questions**:
  - What specific hallucination patterns occur in AI-S-Plus?
  - Why does it use synthetic data despite real data availability?
  - What triggers hallucination in the generation process?
  - How effective are current countermeasures?
  - How can hallucination be prevented in Researcher integration?
- **Deliverables**:
  - Hallucination pattern analysis report
  - Root cause identification document
  - Prevention strategy specifications
  - Quality control gate designs
- **Acceptance Criteria**:
  - Identify specific hallucination triggers
  - Design concrete prevention mechanisms
  - Create validation checkpoints
- **Estimated Time**: 1 hour
- **Dependencies**: None

### Task 1.4: Sakana Novelty Generation Framework Analysis (Priority: High)
- **Description**: Understand how AI-S-Plus generates novel experiment hypotheses and compare with alternatives
- **Files to Study**:
  ```
  /Users/apple/code/ai-s-plus/NEW novelty experiments framework/input and output of sakana generation of hypothesis
  /Users/apple/code/ai-s-plus/NEW novelty experiments framework/Novel SAI Experiment Selection Framework.docx
  /Users/apple/code/ai-s-plus/run-experiment-novel-1/experiments/2025-08-09_22-45-07_sai_system_spectroscopy_attempt_0/latex/sai_active_spectroscopy_comprehensive.pdf
  ```
- **MCP Tools Required**: Task agent for document analysis
- **Research Questions**:
  - How does the novelty generation algorithm work?
  - What makes it effective at creating breakthrough ideas?
  - How does it verify novelty against existing literature?
  - Can this be extracted and used independently?
  - How does it compare to URSA and Oxford+RAG approaches?
- **Deliverables**:
  - Novelty generation algorithm specification
  - Comparative analysis vs URSA and Oxford+RAG
  - Extraction feasibility assessment
  - Integration recommendations
- **Acceptance Criteria**:
  - Document complete novelty generation workflow
  - Provide comparison matrix with other systems
  - Recommend optimal combination strategy
- **Estimated Time**: 45 minutes
- **Dependencies**: Task 1.1 completion

### Task 1.5: Researcher Framework Integration Points Analysis (Priority: High)
- **Description**: Analyze Researcher's paper generation pipeline to identify integration points for real data and calculations
- **Files to Analyze**:
  ```
  /Users/apple/code/Researcher/ai_researcher/ (entire directory structure)
  /Users/apple/code/Researcher/comprehensive_enhancer.py
  /Users/apple/code/Researcher/PIPELINE_1_PRODUCTION/
  /Users/apple/code/Researcher/PIPELINE_2_DEVELOPMENT/ai_researcher_enhanced/integration/
  ```
- **MCP Tools Required**: Task agent for codebase analysis
- **Research Questions**:
  - How does the 128-page paper generation pipeline work?
  - Where can real data calculations be injected?
  - How does comprehensive_enhancer.py expand references?
  - What integration hooks exist in Pipeline 2?
  - How can GLENS data be integrated during generation?
- **Deliverables**:
  - Researcher framework architecture document
  - Integration point specifications
  - Enhancement pipeline analysis
  - Data injection recommendations
- **Acceptance Criteria**:
  - Map complete paper generation workflow
  - Identify specific integration hooks
  - Design data injection architecture
- **Estimated Time**: 1 hour
- **Dependencies**: None



---

## **Phase 2: External System Evaluation (Priority: High)**
*Duration: 1.5 hours | Parallel Execution Possible*

### Task 2.1: URSA Physics Calculation Capabilities Verification (Priority: High)
- **Description**:  evaluate URSA's multi-agent system to determine physics calculation capabilities
- **Source**: /Users/apple/code/Researcher/ursa
- **MCP Tools Required**: 
- **Research Method**:
  - Examine Planning Agent, Execution Agent, ArXiv Agent capabilities
  - Test execution agent with sample physics calculations
  - Compare hypothesis generation quality to Oxford+RAG
- **Critical Questions**:
  - Can the Execution Agent run scientific Python code (NumPy, SciPy)?
  - Does it have access to computational resources for physics calculations?
  - How does it handle complex stratospheric aerosol calculations?
  - Is it superior to Oxford+RAG for SAI research?
- **Deliverables**:
  - URSA capabilities assessment report
  - Physics calculation verification results
  - Comparison matrix vs Oxford+RAG
  - Integration feasibility analysis
- **Acceptance Criteria**:
  - Verify actual physics calculation capabilities
  - Provide quantitative comparison with alternatives
  - Recommend integration approach
- **Estimated Time**: 45 minutes
- **Dependencies**: None

### Task 2.2: Oxford + RAG System Deep Analysis (Priority: Medium)
- **Description**: Evaluate the 1100 PDFs corpus system for novelty detection and hypothesis generation
- **Location**: `/Users/apple/code/scientificoxford-try-shaun`
- **MCP Tools Required**: Task agent for codebase analysis
- **Research Questions**:
  - How does the 1100 PDFs corpus work for SAI research?
  - What's the quality of hypothesis generation vs Sakana?
  - How effective is the novelty verification system?
  - What are the computational requirements?
  - How complex would integration be with other systems?
- **Deliverables**:
  - Oxford+RAG system analysis report
  - Corpus quality assessment
  - Integration complexity evaluation
  - Performance characteristics
- **Acceptance Criteria**:
  - Document complete RAG workflow
  - Assess hypothesis generation quality
  - Evaluate integration requirements
- **Estimated Time**: 30 minutes
- **Dependencies**: None

### Task 2.3: Gemini 2.5 Pro Automation Strategy Design (Priority: Medium)
- **Description**: Design strategy to automate the manual Gemini quality control iterations currently required for AI-S-Plus
- **Current Issue**: Manual 4+ iteration process for quality control
- **MCP Tools Required**: Perplexity for research on automation approaches
- **Research Topics**:
  - "Automated LLM quality control pipelines 2025"
  - "Gemini API automation batch processing"
  - "Scientific paper quality scoring automation"
- **Deliverables**:
  - Gemini automation architecture design
  - Quality control gate specifications
  - Batch processing workflow
  - Error handling and retry mechanisms
- **Acceptance Criteria**:
  - Design automated quality scoring system
  - Create batch processing pipeline
  - Define quality thresholds and gates
- **Estimated Time**: 30 minutes
- **Dependencies**: Task 1.3 (hallucination analysis)

---

## **Phase 3: Integration Architecture Design (Priority: Critical)**
*Duration: 2 hours | Dependent on Phase 1 completion*

### Task 3.1: Optimal Pipeline Flow Architecture Design (Priority: Critical)
- **Description**: Design the perfect combination of all 5 systems into a unified super-paper generation pipeline
- **Key Decisions Required**:
  1. **Novelty Generation**: URSA vs Oxford+RAG vs Sakana hypothesis generator?
  2. **Data Integration**: Import AI-S-Plus modules vs API calls vs hybrid approach?
  3. **Calculation Method**: BFTS vs Monte Carlo vs online services?
  4. **Quality Control**: How to automate Gemini iterations?
  5. **Paper Generation**: How to enhance Researcher with real calculations?
- **MCP Tools Required**: Sequential thinking for architecture design
- **Deliverables**:
  - Complete pipeline architecture diagram
  - Stage-by-stage workflow specification
  - Integration decision matrix with rationale
  - Data flow and control specifications
- **Acceptance Criteria**:
  - Design addresses all 5 system integrations
  - Provides clear technical implementation path
  - Solves hallucination and quality control issues
- **Estimated Time**: 1 hour
- **Dependencies**: All Phase 1 tasks completed

### Task 3.2: Technical Integration Strategy Specification (Priority: Critical)
- **Description**: Define the technical approach for integrating systems (module imports vs APIs vs hybrid)
- **Key Questions**:
  - Should we import AI-S-Plus modules into Researcher codebase?
  - Or make API calls between separate systems?
  - How to handle the data pipeline from hypothesis to calculations?
  - Where to inject quality control gates?
  - How to prevent hallucination propagation?
- **MCP Tools Required**: Sequential thinking for technical design
- **Deliverables**:
  - Module import vs API integration specifications
  - Data pipeline technical architecture
  - Quality control gate implementation design
  - Error handling and rollback mechanisms
- **Acceptance Criteria**:
  - Provide detailed technical implementation specs
  - Address performance and reliability requirements
  - Include fallback and error recovery
- **Estimated Time**: 45 minutes
- **Dependencies**: Task 3.1 completion

### Task 3.3: Cambridge SAI Solution Pipeline Configuration (Priority: Critical)
- **Description**: Design specific pipeline configuration to solve the Cambridge professor's SAI pulse vs continuous flow question
- **Client Question**: "What are the potential pros and cons of injecting materials for stratospheric aerosol injection (SAI) in a pulsed fashion versus a continuous flow?"
- **Requirements**:
  - Use real GLENS/GeoMIP/ARISE-SAI data
  - Generate novel hypotheses about injection strategies
  - Provide quantitative analysis and calculations
  - Deliver publication-quality 128-page analysis
- **MCP Tools Required**: Perplexity for SAI research background
- **Deliverables**:
  - SAI-specific pipeline configuration
  - Research methodology specification
  - Data sources and calculation requirements
  - Expected output format and quality metrics
- **Acceptance Criteria**:
  - Pipeline specifically addresses SAI pulse vs continuous analysis
  - Uses real climate data and calculations
  - Meets academic publication standards
- **Estimated Time**: 15 minutes
- **Dependencies**: Tasks 3.1 and 3.2 completion

---

## **Phase 4: Proof of Concept Development (Priority: High)**
*Duration: 2-3 hours | Implementation begins*

### Task 4.1: GLENS Data Loader Integration with Researcher (Priority: High)
- **Description**: Extract AI-S-Plus GLENS loader and integrate it with Researcher framework
- **Technical Approach**:
  - Extract glens_loader.py and dependencies from AI-S-Plus
  - Create integration module in Researcher framework
  - Test data loading with sample GLENS datasets
  - Verify data flow into paper generation pipeline
- **Files to Create**:
  ```
  /Users/apple/code/Researcher/ai_researcher/data_integration/
  ├── glens_loader.py          # Extracted from AI-S-Plus
  ├── data_processor.py        # Data formatting for Researcher
  ├── integration_manager.py   # Main integration controller
  └── __init__.py
  ```
- **MCP Tools Required**: Task agent for code extraction and integration
- **Deliverables**:
  - Working GLENS data integration module
  - Test verification with sample data
  - Integration documentation
  - Performance benchmarks
- **Acceptance Criteria**:
  - Successfully loads real GLENS climate data
  - Integrates with existing Researcher pipeline
  - Passes basic functionality tests
- **Estimated Time**: 1.5 hours
- **Dependencies**: Task 1.1 completion (GLENS analysis)

### Task 4.2: Calculation Injection Proof of Concept (Priority: High)
- **Description**: Create proof of concept for injecting real calculations into Researcher's paper generation
- **Technical Approach**:
  - Identify calculation injection points in paper generation
  - Create calculation module wrapper
  - Test with simple SAI calculations
  - Verify quality preservation
- **Files to Create**:
  ```
  /Users/apple/code/Researcher/ai_researcher/calculations/
  ├── calculation_engine.py    # Main calculation interface
  ├── sai_calculations.py      # SAI-specific calculations
  ├── injection_manager.py    # Inject calculations into papers
  └── __init__.py
  ```
- **MCP Tools Required**: Task agent for implementation
- **Deliverables**:
  - Working calculation injection system
  - Test calculations for SAI scenarios
  - Quality verification results
  - Integration performance metrics
- **Acceptance Criteria**:
  - Successfully injects calculations into generated papers
  - Maintains Researcher's writing quality
  - Provides accurate computational results
- **Estimated Time**: 1 hour
- **Dependencies**: Task 1.5 completion (Researcher analysis)

### Task 4.3: Hallucination Prevention Implementation (Priority: High)
- **Description**: Implement hallucination prevention mechanisms based on Phase 1 analysis
- **Technical Approach**:
  - Create validation gates for all generated content
  - Implement real data verification checkpoints
  - Add quality scoring for authenticity
  - Test with known hallucination scenarios
- **Files to Create**:
  ```
  /Users/apple/code/Researcher/ai_researcher/validation/
  ├── hallucination_detector.py  # Main detection system
  ├── data_validator.py         # Real data verification
  ├── quality_scorer.py         # Authenticity scoring
  └── __init__.py
  ```
- **MCP Tools Required**: Task agent for implementation
- **Deliverables**:
  - Working hallucination prevention system
  - Validation checkpoint implementation
  - Test results with hallucination scenarios
  - Quality control documentation
- **Acceptance Criteria**:
  - Detects and prevents known hallucination patterns
  - Validates all content against real data
  - Provides quantitative quality scores
- **Estimated Time**: 45 minutes
- **Dependencies**: Task 1.3 completion (hallucination analysis)

---

## **Phase 5: Quality Control & Automation (Priority: Medium)**
*Duration: 1-2 hours | Optimization and automation*

### Task 5.1: Automated Gemini Quality Control Implementation (Priority: Medium)
- **Description**: Implement automated Gemini 2.5 Pro quality control to replace manual iterations
- **Technical Approach**:
  - Create batch processing system for Gemini API
  - Implement quality scoring and feedback loops
  - Add automatic retry mechanisms
  - Test with AI-S-Plus style corrections
- **Files to Create**:
  ```
  /Users/apple/code/Researcher/ai_researcher/quality_control/
  ├── gemini_validator.py      # Main Gemini integration
  ├── batch_processor.py       # Batch API processing
  ├── feedback_loop.py         # Automatic iteration system
  └── __init__.py
  ```
- **Deliverables**:
  - Automated Gemini quality control system
  - Batch processing implementation
  - Quality improvement metrics
  - Automation performance results
- **Acceptance Criteria**:
  - Reduces manual iterations from 4+ to 0
  - Maintains or improves quality scores
  - Provides automated feedback and corrections
- **Estimated Time**: 1 hour
- **Dependencies**: Task 2.3 completion (Gemini automation design)

### Task 5.2: Novelty Generation Integration (Priority: Medium)
- **Description**: Integrate the best novelty generation system based on Phase 2 evaluation
- **Technical Approach**:
  - Implement winner from URSA vs Oxford+RAG vs Sakana comparison
  - Create unified novelty interface
  - Test with SAI research scenarios
  - Verify integration with main pipeline
- **Files to Create**:
  ```
  /Users/apple/code/Researcher/ai_researcher/novelty/
  ├── novelty_engine.py        # Main novelty interface
  ├── [system]_integration.py  # Specific system integration
  ├── novelty_validator.py     # Novelty verification
  └── __init__.py
  ```
- **Deliverables**:
  - Integrated novelty generation system
  - Novelty verification implementation
  - Test results with SAI scenarios
  - Performance comparison metrics
- **Acceptance Criteria**:
  - Generates novel SAI research hypotheses
  - Integrates seamlessly with main pipeline
  - Provides verifiable novelty scores
- **Estimated Time**: 45 minutes
- **Dependencies**: Phase 2 completion (system evaluation)

### Task 5.3: End-to-End Pipeline Testing (Priority: Medium)
- **Description**: Test complete integrated pipeline with Cambridge SAI question
- **Test Scenario**: Generate analysis for SAI pulse vs continuous flow injection
- **Technical Approach**:
  - Run complete pipeline with real GLENS data
  - Generate full paper with calculations
  - Validate quality and novelty
  - Measure performance metrics
- **Deliverables**:
  - Complete test run results
  - Generated SAI analysis paper
  - Performance benchmarks
  - Quality verification report
- **Acceptance Criteria**:
  - Generates 128-page quality paper with real calculations
  - Addresses Cambridge professor's specific question
  - Achieves 7.0+ quality scores
  - Completes in reasonable time (under 6 hours)
- **Estimated Time**: 30 minutes
- **Dependencies**: Tasks 4.1, 4.2, 5.1, 5.2 completion

---

## **Phase 6: Documentation & Strategic Analysis (Priority: Low)**
*Duration: 1 hour | Final deliverables*

### Task 6.1: Ultimate Pipeline Strategy Document Creation (Priority: Low)
- **Description**: Create comprehensive strategy document with all findings and recommendations
- **File**: `/Users/apple/code/Researcher/.claude/doc/ultimate-pipeline-strategy_2025-08-15_HHMM.md`
- **Required Sections**:
  1. **Executive Summary** - Key findings and strategic recommendations
  2. **Codebase Analysis Results** - All 5 systems analysis
  3. **Technical Integration Strategy** - Complete implementation plan
  4. **The Perfect Pipeline Design** - Stage-by-stage workflow
  5. **Implementation Roadmap** - Phased development plan
  6. **Risk Assessment & Mitigation** - Quality and performance plans
  7. **Client Solution: SAI Pulse vs Continuous** - Specific configuration
  8. **Technical Appendix** - Code specs and interfaces
- **Deliverables**:
  - Complete strategy document (30+ pages)
  - Technical specifications
  - Implementation roadmap
  - Risk mitigation plans
- **Acceptance Criteria**:
  - Addresses all research questions from PRD
  - Provides definitive integration strategy
  - Includes working implementation plan
- **Estimated Time**: 45 minutes
- **Dependencies**: All previous phases completed

### Task 6.2: Implementation Roadmap and Timeline (Priority: Low)
- **Description**: Create detailed implementation roadmap with timeline and resource estimates
- **Deliverables**:
  - Phase-by-phase implementation plan
  - Resource requirements and timeline
  - Risk assessment and mitigation
  - Success metrics and validation criteria
- **Acceptance Criteria**:
  - Provides clear path from current state to full integration
  - Includes realistic timeline and resource estimates
  - Addresses all identified risks and challenges
- **Estimated Time**: 15 minutes
- **Dependencies**: Task 6.1 completion

---

## **📊 SUCCESS METRICS & VALIDATION**

### **Critical Success Factors**
1. **Super-Papers**: Researcher eloquence + AI-S-Plus calculations
2. **Novelty**: Breakthrough ideas with real scientific value  
3. **Quality**: 7.0+ scores with complete empirical validation
4. **Efficiency**: Practical generation times (<6 hours)
5. **Reliability**: Consistent results without manual intervention
6. **Client Value**: Direct solution to Cambridge SAI question

### **Cannot Compromise**
- Researcher's eloquent writing quality (6.0+ scores maintained)
- Real data authenticity (no synthetic contamination)
- Academic rigor and verification standards
- Computational efficiency and scalability
- Integration reliability and error handling

### **Final Validation Criteria**
- [ ] Pipeline generates many 128-page papers with real GLENS calculations. Each of them for each experiment/hypothese
- [ ] Solves Cambridge professor's SAI pulse vs continuous question, providing him several papers/experiments/hypotheses
- [ ] Achieves 7.0+ quality scores consistently
- [ ] Completes generation in under 6 hours per experimnet
- [ ] Prevents hallucination and maintains data authenticity
- [ ] Provides novel insights for SAI research, so each experiment is novel

---

## **⚡ EXECUTION PRIORITY**

### **Start Immediately (Critical Path)**
1. Task 1.1: GLENS Data Loader Analysis
2. Task 1.2: BFTS vs Monte Carlo Analysis  
3. Task 1.3: Hallucination Problem Analysis

### **Parallel Execution Possible**
- Phase 2 tasks (URSA, Oxford+RAG, Gemini automation)
- Can run concurrent with Phase 1 analysis tasks

### **Sequential Dependencies**
- Phase 3 (Architecture) requires Phase 1 completion
- Phase 4 (POC) requires Phase 3 completion
- Phase 5 (Quality Control) requires Phase 4 completion

**Total Estimated Time**: 8-10 hours for complete implementation
**Critical Path**: 6 hours (Phases 1-4)
**Documentation**: 1 hour (Phase 6)

---

*Task list ready for execution | Ultimate pipeline research begins*