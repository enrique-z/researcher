# 🎯 **PIPELINE 1: EXPERIMENT TEMPLATES FOR ANY DOMAIN**

These are **proven templates** based on the successful spectroscopy experiment. Use these to generate papers for ANY research topic.

---

## 📋 **TEMPLATE 1: CLIMATE SCIENCE RESEARCH**

### **Example: Chemical Composition of SAI Particles**

#### **File: `input/research_topic_formatted.txt`**
```
Chemical Composition and Atmospheric Fate of Stratospheric Aerosol Injection Particles: Multi-Phase Analysis and Environmental Impact Assessment

RESEARCH OBJECTIVE: Comprehensive Chemical Characterization of SAI Particle Formation, Evolution, and Atmospheric Interactions

CORE HYPOTHESIS: Stratospheric aerosol injection particles undergo complex chemical transformations involving H2SO4 nucleation, multi-phase reactions, and heterogeneous chemistry that significantly alter their radiative properties, atmospheric lifetime, and environmental impacts. Understanding the detailed chemical composition and reaction pathways is essential for predicting SAI effectiveness and unintended consequences.

COMPREHENSIVE RESEARCH FRAMEWORK:
We propose a multi-scale chemical analysis framework for stratospheric aerosol injection particles that combines laboratory experiments, atmospheric modeling, and in-situ observations to characterize particle composition, formation mechanisms, and chemical evolution. The research integrates aerosol chemistry, atmospheric physics, and environmental chemistry to develop predictive models for SAI particle behavior across different stratospheric conditions.

DETAILED EXPERIMENTAL PROTOCOL:
- E1. Laboratory synthesis and characterization: Synthesize H2SO4-based aerosol particles under stratospheric conditions (200-250K, 10-100 hPa) with controlled nucleation and growth processes. Characterize particle size distribution, chemical composition, and physical properties using mass spectrometry, electron microscopy, and optical analysis.
- E2. Multi-phase reaction studies: Investigate heterogeneous reactions between SAI particles and stratospheric trace gases (H2O, O3, NOx, ClOx) using atmospheric pressure chemical ionization and flow tube experiments. Quantify reaction rates, product formation, and particle property changes.
- E3. Atmospheric modeling integration: Implement chemical mechanisms into CESM/WACCM atmospheric models to simulate particle evolution, transport, and interactions. Compare model predictions with observational data and validate chemical pathways.
- E4. Environmental impact assessment: Evaluate potential impacts on stratospheric chemistry, ozone depletion, and atmospheric composition using integrated assessment models and sensitivity analyses.

TECHNICAL METHODOLOGY REQUIREMENTS:
- Mass spectrometry analysis (LC-MS, GC-MS, AMS)
- Atmospheric pressure chemical ionization (APCI)
- Electron microscopy (SEM, TEM) for particle morphology
- Optical property measurements (extinction, scattering)
- Atmospheric chemical transport modeling (CESM/WACCM)
- Thermodynamic equilibrium modeling

EXPECTED OUTCOMES:
- Detailed chemical composition database for SAI particles
- Quantified reaction mechanisms and rate constants
- Predictive models for particle evolution and atmospheric impacts
- Environmental risk assessment framework for SAI deployment
```

#### **File: `input/references.bib`**
```bibtex
@article{mills2016radiative,
  author = {M. J. Mills and A. Schmidt and R. Easter and S. Solomon and D. E. Kinnison and S. J. Ghan and R. R. Neely and D. R. Marsh and A. Conley and C. G. Bardeen and A. Gettelman},
  title = {Global volcanic aerosol properties derived from emissions, 1990–2014, using CESM1(WACCM)},
  journal = {Journal of Geophysical Research: Atmospheres},
  volume = {121},
  pages = {2332--2348},
  year = {2016},
  doi = {10.1002/2015JD024290}
}

@article{english2012microphysical,
  author = {J. M. English and O. B. Toon and M. J. Mills and F. Yu},
  title = {Microphysical simulations of new particle formation in the upper troposphere and lower stratosphere},
  journal = {Atmospheric Chemistry and Physics},
  volume = {12},
  pages = {9207--9226},
  year = {2012},
  doi = {10.5194/acp-12-9207-2012}
}
```

#### **File: `input/experiment_config.json`**
```json
{
  "experiment_name": "sai-chemical-composition",
  "research_domain": "atmospheric_chemistry",
  "target_quality": 6.5,
  "experimental_protocols": [
    "Laboratory aerosol synthesis under stratospheric conditions",
    "Multi-phase heterogeneous reaction studies",
    "Atmospheric chemical transport modeling",
    "Environmental impact assessment"
  ],
  "technical_methods": [
    "Mass spectrometry analysis",
    "Atmospheric pressure chemical ionization", 
    "CESM/WACCM atmospheric modeling",
    "Thermodynamic equilibrium modeling"
  ],
  "expected_duration": "36 months",
  "research_type": "experimental_and_computational"
}
```

---

## 📋 **TEMPLATE 2: MACHINE LEARNING RESEARCH**

### **Example: Transformer Architecture for Scientific Reasoning**

#### **File: `input/research_topic_formatted.txt`**
```
Scientific Reasoning Transformer: Graph-Enhanced Architecture for Multi-Domain Knowledge Integration and Hypothesis Generation

RESEARCH OBJECTIVE: Development of Advanced Transformer Architecture for Automated Scientific Discovery and Reasoning

CORE HYPOTHESIS: A novel transformer architecture that integrates graph neural networks, knowledge graphs, and multi-modal attention mechanisms can significantly outperform existing models in scientific reasoning tasks, knowledge integration, and hypothesis generation across multiple scientific domains.

COMPREHENSIVE RESEARCH FRAMEWORK:
We propose ScientificTransformer, a specialized transformer architecture that combines structured scientific knowledge representation with advanced attention mechanisms to enable automated scientific reasoning, hypothesis generation, and cross-domain knowledge transfer.

DETAILED EXPERIMENTAL PROTOCOL:
- E1. Architecture design: Develop hybrid transformer-GNN architecture with scientific knowledge graph integration, multi-modal attention, and domain-specific encoding modules for chemistry, biology, and physics domains.
- E2. Training methodology: Create large-scale scientific reasoning datasets, implement curriculum learning strategies, and develop novel pre-training objectives for scientific knowledge acquisition and reasoning.
- E3. Benchmark evaluation: Evaluate on scientific reasoning benchmarks (SciBench, ScienceQA, scientific paper understanding) and compare with state-of-the-art models (GPT-4, Claude, PaLM).
- E4. Hypothesis generation: Test model's ability to generate novel scientific hypotheses and validate through expert evaluation and automated consistency checking.

TECHNICAL METHODOLOGY REQUIREMENTS:
- Transformer architecture with graph neural network integration
- Multi-modal attention mechanisms
- Knowledge graph embedding techniques
- Scientific dataset curation and preprocessing
- Distributed training on GPU clusters
- Automated hypothesis validation systems

EXPECTED OUTCOMES:
- Novel transformer architecture for scientific reasoning
- Performance improvements on scientific benchmarks
- Automated hypothesis generation capabilities
- Open-source implementation for research community
```

#### **File: `input/references.bib`**
```bibtex
@article{vaswani2017attention,
  title={Attention is all you need},
  author={Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and Uszkoreit, Jakob and Jones, Llion and Gomez, Aidan N and Kaiser, {\L}ukasz and Polosukhin, Illia},
  journal={Advances in neural information processing systems},
  volume={30},
  year={2017}
}

@article{lu2022learn,
  title={Learn to explain: Multimodal reasoning via thought chains for science question answering},
  author={Lu, Pan and Mishra, Swaroop and Xia, Tony and Qiu, Liang and Chang, Kai-Wei and Zhu, Song-Chun and Tafjord, Oyvind and Clark, Peter and Kalyan, Ashwin},
  journal={Advances in Neural Information Processing Systems},
  volume={35},
  pages={2507--2521},
  year={2022}
}
```

---

## 📋 **TEMPLATE 3: BIOLOGY RESEARCH**

### **Example: CRISPR Gene Editing Optimization**

#### **File: `input/research_topic_formatted.txt`**
```
AI-Guided CRISPR-Cas9 Optimization: Machine Learning-Enhanced Guide RNA Design and Off-Target Prediction for Therapeutic Applications

RESEARCH OBJECTIVE: Development of AI-Enhanced CRISPR System for Improved Precision and Safety in Gene Therapy

CORE HYPOTHESIS: Machine learning models trained on comprehensive genomic and epigenetic data can significantly improve CRISPR-Cas9 guide RNA design, reduce off-target effects, and enhance on-target editing efficiency for therapeutic applications.

COMPREHENSIVE RESEARCH FRAMEWORK:
We propose CRISPRopt, an integrated AI platform that combines deep learning, genomic analysis, and experimental validation to optimize CRISPR-Cas9 gene editing systems for therapeutic applications with enhanced precision and safety.

DETAILED EXPERIMENTAL PROTOCOL:
- E1. Data integration: Compile comprehensive datasets of CRISPR experiments, genomic sequences, epigenetic marks, chromatin accessibility, and off-target measurements from public databases and literature.
- E2. Model development: Design deep learning architectures (CNN, RNN, Transformer) for guide RNA efficiency prediction, off-target scoring, and editing outcome prediction using genomic and epigenetic features.
- E3. Experimental validation: Synthesize predicted guide RNAs, perform CRISPR experiments in cell culture, and measure on-target efficiency and off-target effects using targeted sequencing and genome-wide analysis.
- E4. Therapeutic application: Apply optimized CRISPR systems to disease-relevant targets and evaluate therapeutic potential in relevant cellular models.

TECHNICAL METHODOLOGY REQUIREMENTS:
- Deep learning model development (TensorFlow/PyTorch)
- Genomic data processing and analysis
- CRISPR experimental protocols
- High-throughput sequencing analysis
- Statistical modeling and validation
- Bioinformatics pipeline development

EXPECTED OUTCOMES:
- AI-enhanced CRISPR guide RNA design platform
- Improved on-target efficiency and reduced off-target effects
- Validated therapeutic CRISPR applications
- Open-source software tools for research community
```

---

## 🛠️ **QUICK SETUP SCRIPTS**

### **For Chemical Composition Experiment:**
```bash
#!/bin/bash
# setup_chemistry_experiment.sh

TOPIC="sai-chemical-composition"
mkdir -p EXPERIMENTS/experiment-$TOPIC/input
cd EXPERIMENTS/experiment-$TOPIC/input

# Use template above - copy chemical composition template files
echo "Created chemistry experiment directory"
echo "Add the template files from EXPERIMENT_TEMPLATES.md"
echo "Then run: cd /Users/apple/code/Researcher && python comprehensive_enhancer.py EXPERIMENTS/experiment-$TOPIC"
```

### **For Machine Learning Experiment:**
```bash
#!/bin/bash
# setup_ml_experiment.sh

TOPIC="scientific-transformer"
mkdir -p EXPERIMENTS/experiment-$TOPIC/input
cd EXPERIMENTS/experiment-$TOPIC/input

echo "Created ML experiment directory"
echo "Add the template files from EXPERIMENT_TEMPLATES.md"
echo "Then run: cd /Users/apple/code/Researcher && python comprehensive_enhancer.py EXPERIMENTS/experiment-$TOPIC"
```

---

## 📊 **QUALITY GUIDELINES**

### **High-Quality Topic Requirements (6.0+ Score):**
1. **Clear Research Objective**: Specific, measurable goals
2. **Strong Hypothesis**: Testable predictions with clear rationale
3. **Detailed Protocols**: 4-6 specific experimental steps (E1-E6)
4. **Technical Depth**: Specific methodologies and tools
5. **Expected Outcomes**: Concrete deliverables and impacts

### **Template Structure (Proven Pattern):**
```
[Descriptive Title with Technical Terms]

RESEARCH OBJECTIVE: [Clear, specific goal]
CORE HYPOTHESIS: [Testable prediction with rationale]
COMPREHENSIVE RESEARCH FRAMEWORK: [Overall approach]

DETAILED EXPERIMENTAL PROTOCOL:
- E1. [First experiment with specifics]
- E2. [Second experiment with specifics]
- [Continue with 4-6 protocols]

TECHNICAL METHODOLOGY REQUIREMENTS:
- [List specific methods, tools, techniques]

EXPECTED OUTCOMES:
- [Concrete deliverables]
- [Research impact]
```

---

## 🎯 **USAGE INSTRUCTIONS**

1. **Choose template** closest to your research domain
2. **Customize content** for your specific research question
3. **Maintain structure** (proven format from successful experiments)
4. **Follow naming** conventions for files and directories
5. **Run enhancement** before generation
6. **Use tmux interface** for monitoring

**These templates are based on the successful 128-page spectroscopy paper generation and designed to work with the proven Pipeline 1 system.**