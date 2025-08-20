# AI Research Experiment Preparation Guide
## Systematic Framework for High-Quality Paper Generation

### Overview
This guide provides a comprehensive framework for preparing AI research paper generation experiments that can scale to hundreds of different topics while maintaining consistent high quality (target: >5.0/10 score).

---

## 🎯 **CORE INPUT REQUIREMENTS**

### 1. **Research Topic Specification**
**MANDATORY - Highest Impact on Quality**

#### A. Primary Research Question
- **Format**: Clear, specific, actionable research question
- **Length**: 2-3 sentences maximum
- **Example**: "How can active spectroscopy techniques using information-optimized pulsed signals improve the control precision and early-warning capabilities of stratospheric aerosol injection for climate intervention?"

#### B. Core Hypothesis
- **Format**: Falsifiable scientific hypothesis with clear mechanism
- **Structure**: "We hypothesize that [X method] will [achieve Y outcome] because [Z mechanism/theory]"
- **Specificity**: Include quantitative predictions where possible
- **Example**: "Small-amplitude, information-optimized pulsed SAI can identify frequency-dependent climate responses with 50% higher precision than continuous injection methods"

#### C. Technical Scope Definition
- **Domain**: Primary scientific field (climate science, ML, biology, etc.)
- **Methodology**: Core technical approaches required
- **Constraints**: Physical, computational, or ethical limitations
- **Novelty**: What makes this approach different from existing work

### 2. **Literature Foundation**
**CRITICAL - Determines Scientific Rigor**

#### A. Reference Quality Standards
- **Minimum**: 8-15 high-quality references
- **Recency**: At least 60% published within last 5 years
- **Impact**: Include key seminal papers + recent advances
- **Coverage**: Balance between foundational theory and cutting-edge methods

#### B. BibTeX Requirements
```bibtex
# Each entry MUST include:
@article{key,
    title = {Complete Title},
    author = {Full Author Names},
    journal = {Journal Name},
    year = {Year},
    volume = {Vol},
    pages = {Pages},
    doi = {DOI when available},
    abstract = {Abstract text - HIGHLY RECOMMENDED}
}
```

#### C. Reference Categorization
- **Foundational Theory**: 2-3 papers establishing scientific basis
- **Technical Methods**: 3-5 papers on specific methodologies  
- **Recent Advances**: 3-4 papers from last 2 years
- **Comparative Work**: 2-3 papers for benchmarking/comparison

### 3. **Experimental Design Framework**
**ESSENTIAL - Ensures Implementability**

#### A. Experimental Protocol Structure
**Required Format**: Numbered protocols (E1, E2, E3...)
- **E1**: Primary experimental design and setup
- **E2**: Data collection and analysis methods
- **E3**: Validation and comparison protocols
- **E4**: Sensitivity/robustness testing
- **E5**: Cross-validation or replication studies
- **E6**: Practical implementation considerations

#### B. Technical Methodology Requirements
- **Signal Processing**: Specific algorithms/techniques required
- **Statistical Methods**: Analysis frameworks and significance tests
- **Computational Tools**: Software/hardware requirements
- **Validation Methods**: How results will be verified
- **Metrics**: Quantitative success criteria

### 4. **Quality Assurance Specifications**
**CRITICAL - Ensures High Standards**

#### A. Expected Outcomes Definition
- **Quantitative Goals**: Specific numerical targets
- **Scientific Contributions**: Novel insights expected
- **Practical Applications**: Real-world utility
- **Reproducibility**: How others can replicate work

#### B. Risk Assessment
- **Technical Risks**: Methodology limitations
- **Computational Risks**: Resource constraints
- **Validation Risks**: Verification challenges
- **Mitigation Strategies**: How to address each risk

---

## 📊 **QUALITY OPTIMIZATION FACTORS**

### High Impact (>0.5 points improvement)
1. **Comprehensive Experimental Protocol** (6 detailed protocols)
2. **Strong Literature Foundation** (12+ quality references)
3. **Clear Technical Methodology** (specific algorithms/tools)
4. **Quantitative Success Metrics** (measurable outcomes)
5. **Novel Scientific Contribution** (clear advancement)

### Medium Impact (0.2-0.5 points improvement)
1. **Mathematical Formulation** (equations/models)
2. **Comparative Analysis** (benchmarking against existing methods)
3. **Cross-Validation Strategy** (robustness testing)
4. **Practical Constraints** (real-world limitations addressed)
5. **Reproducibility Details** (implementation specifics)

### Lower Impact (0.1-0.2 points improvement)
1. **Writing Quality** (clear, scientific prose)
2. **Figure/Table Planning** (visual data presentation)
3. **Timeline Specification** (research phases)
4. **Collaboration Requirements** (interdisciplinary needs)
5. **Ethical Considerations** (responsible research practices)

---

## 🛠 **PREPARATION TEMPLATES**

### Template 1: STEM/Engineering Research
```json
{
  "research_focus": "Technical Problem Statement",
  "core_hypothesis": "Quantitative hypothesis with mechanism",
  "technical_methods": [
    "Method 1 with specific algorithms",
    "Method 2 with validation approach",
    "Method 3 with comparison metrics"
  ],
  "experimental_protocols": [
    "E1: System setup and parameter optimization",
    "E2: Data collection under controlled conditions", 
    "E3: Performance benchmarking vs. state-of-art",
    "E4: Robustness testing under variation",
    "E5: Cross-validation with independent datasets",
    "E6: Computational efficiency and scaling analysis"
  ],
  "success_metrics": {
    "primary": "Quantitative performance improvement %",
    "secondary": ["Robustness measure", "Efficiency gain"],
    "statistical": "Significance level and power analysis"
  }
}
```

### Template 2: Life Sciences/Biology Research  
```json
{
  "research_focus": "Biological mechanism or phenomenon",
  "core_hypothesis": "Mechanistic hypothesis with pathway",
  "technical_methods": [
    "Experimental techniques (wet lab/computational)",
    "Statistical analysis methods",
    "Validation approaches"
  ],
  "experimental_protocols": [
    "E1: Sample preparation and experimental design",
    "E2: Data collection with proper controls",
    "E3: Statistical analysis and significance testing",
    "E4: Mechanism validation experiments", 
    "E5: Cross-species or cross-condition validation",
    "E6: Clinical relevance and translation potential"
  ],
  "success_metrics": {
    "primary": "Effect size and biological significance",
    "secondary": ["Reproducibility", "Clinical relevance"],
    "statistical": "Power analysis and multiple testing correction"
  }
}
```

### Template 3: Computational/ML Research
```json
{
  "research_focus": "Algorithm or model development",
  "core_hypothesis": "Performance or capability improvement",
  "technical_methods": [
    "Algorithm design and implementation",
    "Training/optimization procedures",
    "Evaluation methodologies"
  ],
  "experimental_protocols": [
    "E1: Algorithm development and implementation",
    "E2: Training data preparation and methodology",
    "E3: Comprehensive evaluation on benchmarks",
    "E4: Ablation studies and sensitivity analysis",
    "E5: Cross-dataset generalization testing",
    "E6: Computational efficiency and scalability"
  ],
  "success_metrics": {
    "primary": "Performance metric improvement",
    "secondary": ["Generalization", "Efficiency"],
    "statistical": "Significance testing across multiple runs"
  }
}
```

---

## 📋 **EXPERIMENT PREPARATION CHECKLIST**

### Phase 1: Topic Development (CRITICAL)
- [ ] **Research Question**: Clear, specific, answerable
- [ ] **Hypothesis**: Falsifiable with measurable predictions
- [ ] **Novelty**: Distinct from existing approaches
- [ ] **Feasibility**: Achievable with available resources
- [ ] **Impact**: Significant scientific/practical contribution

### Phase 2: Literature Foundation (ESSENTIAL)
- [ ] **Reference Count**: 8-15 high-quality sources
- [ ] **Reference Quality**: High-impact journals/conferences
- [ ] **Reference Diversity**: Theory + methods + recent work
- [ ] **BibTeX Completeness**: All required fields present
- [ ] **Abstract Inclusion**: Enhanced context for AI model

### Phase 3: Experimental Design (CRITICAL)
- [ ] **Protocol Structure**: 6 detailed experimental protocols
- [ ] **Methodology Specificity**: Concrete algorithms/techniques
- [ ] **Validation Strategy**: Multiple verification approaches
- [ ] **Success Metrics**: Quantitative, measurable outcomes
- [ ] **Risk Assessment**: Limitations and mitigation strategies

### Phase 4: Quality Assurance (ESSENTIAL)
- [ ] **Technical Depth**: Advanced methodology requirements
- [ ] **Mathematical Rigor**: Equations/models where appropriate
- [ ] **Comparative Analysis**: Benchmarking strategy
- [ ] **Reproducibility**: Implementation details sufficient
- [ ] **Ethical Considerations**: Responsible research practices

---

## 🚀 **AUTOMATED PREPARATION PIPELINE**

### Input Data Structure
```json
{
  "experiment_id": "experiment-native-N-[topic-tag]",
  "timestamp": "YYYYMMDD_HHMMSS",
  "topic": {
    "title": "Research Paper Title",
    "research_question": "Primary research question",
    "hypothesis": "Core scientific hypothesis",
    "domain": "Scientific field (climate, ML, bio, etc.)",
    "novelty": "What makes this unique"
  },
  "literature": {
    "bibtex_content": "Complete BibTeX database",
    "reference_count": 12,
    "coverage": {
      "foundational": 3,
      "methodological": 4, 
      "recent": 3,
      "comparative": 2
    }
  },
  "experimental_design": {
    "protocols": [
      "E1: Protocol description",
      "E2: Protocol description", 
      "...E6: Protocol description"
    ],
    "technical_methods": [
      "Method 1 specification",
      "Method 2 specification",
      "Method 3 specification"
    ],
    "success_metrics": {
      "primary": "Main quantitative metric",
      "secondary": ["Supporting metrics"],
      "statistical": "Significance criteria"
    }
  },
  "quality_assurance": {
    "expected_score": 5.5,
    "target_acceptance_rate": 40,
    "risk_factors": ["Risk 1", "Risk 2"],
    "mitigation_strategies": ["Strategy 1", "Strategy 2"]
  }
}
```

### Quality Validation Pipeline
1. **Content Analysis**: Verify all required fields present
2. **Literature Quality**: Check reference impact/recency
3. **Technical Depth**: Assess methodology sophistication  
4. **Experimental Rigor**: Validate protocol completeness
5. **Novelty Assessment**: Confirm scientific contribution
6. **Feasibility Check**: Verify implementation possibility

---

## 📈 **QUALITY PREDICTION METRICS**

### Scoring Factors (0-10 scale)
```python
def calculate_quality_prediction(input_data):
    score = 0.0
    
    # Literature Foundation (25% weight)
    score += min(2.5, len(input_data['references']) * 0.2)
    
    # Experimental Protocols (25% weight) 
    score += min(2.5, len(input_data['protocols']) * 0.4)
    
    # Technical Methodology (20% weight)
    score += min(2.0, len(input_data['methods']) * 0.3)
    
    # Hypothesis Clarity (15% weight)
    score += assess_hypothesis_quality() * 1.5
    
    # Novelty Factor (15% weight)
    score += assess_novelty() * 1.5
    
    return min(10.0, score)
```

### Expected Quality Ranges
- **Score 3.0-4.0**: Basic research, needs enhancement
- **Score 4.0-5.0**: Solid methodology, publishable quality
- **Score 5.0-6.0**: High-quality research, conference-level
- **Score 6.0+**: Exceptional research, top-tier venues

---

## 🎯 **OPTIMIZATION RECOMMENDATIONS**

### For Maximum Quality (Target: >6.0/10)
1. **Enhanced Literature**: 15+ references, 70% recent
2. **Advanced Methodology**: State-of-art techniques + novel combinations
3. **Comprehensive Protocols**: 6+ detailed experimental procedures
4. **Quantitative Predictions**: Specific numerical targets
5. **Cross-Validation**: Multiple validation approaches
6. **Practical Impact**: Clear real-world applications

### For Efficiency (Target: 4-5 hour completion)
1. **Focused Scope**: Well-defined, specific research question
2. **Established Methods**: Build on proven techniques
3. **Clear Protocols**: Unambiguous experimental procedures  
4. **Quality References**: High-impact, relevant literature
5. **Realistic Targets**: Achievable within computational limits

### For Scalability (Hundreds of experiments)
1. **Template-Based**: Standardized input structures
2. **Automated Validation**: Quality checks before execution
3. **Modular Design**: Reusable experimental components
4. **Progress Monitoring**: Real-time quality tracking
5. **Error Recovery**: Graceful failure handling

This framework ensures consistent high-quality research paper generation across diverse scientific domains while maintaining scalability for large-scale experimentation.