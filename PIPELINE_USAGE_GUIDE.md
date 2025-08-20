# Pipeline Usage Guide: Researcher + Sakana Integration

## 🎯 **Your Current Problem → Our Solution**

**Your Current Workflow (Pain Points):**
1. ❌ Generate experiments → Send to Researcher → Get beautiful 128-page papers
2. ❌ Send papers to Sakana → **Manual testing and corrections required**
3. ❌ **Continuous forensic anti-synthetic data detection needed**
4. ❌ **Repeat manual corrections until Sakana works**

**Our Automated Solution:**
1. ✅ **Pre-validate experiments** → Automated corrections → **Only send good experiments to Researcher**
2. ✅ **Automated synthetic data detection** → **Automated replacement with real data**
3. ✅ **Enhanced Researcher generation** with validated context → **Higher quality papers**
4. ✅ **Final quality assurance** → **Ready-to-publish super papers**

---

## 🚦 **Three Pipeline Flow Options**

### **Option 1: Sequential Flow (Your Current Process)**
```
Experiment → Researcher → 128-page Paper → Sakana → Manual Corrections → Repeat
```
**⚠️ Problem:** Wastes effort generating papers that fail validation (your current pain)

### **Option 2: Parallel Flow** 
```
Experiment → [Researcher + Sakana in parallel] → Merge Results
```
**⚠️ Problem:** Complex merging, potential conflicts

### **Option 3: Pre-Validation Gateway (RECOMMENDED)** ⭐
```
Experiment → Sakana Pre-Screen → [PASS: Enhanced Researcher] → Super Paper
                               → [FAIL: Reject before wasting effort]
```
**✅ Solution:** Prevents wasted effort, automates your manual corrections

---

## 🔧 **Recommended Pipeline: Pre-Validation Gateway**

This automates your manual correction workflow and implements the Sakana Principle as a **quality gate**.

### **Stage 1: Automated Pre-Screening (Replaces Manual Testing)**

```python
from ai_researcher.pipeline import IntegrationPipeline

# Initialize pipeline with your GLENS data
pipeline = IntegrationPipeline(
    glens_data_path="/Users/apple/code/ai-s-plus/data/glens",
    enable_pre_screening=True  # Pre-validation gateway
)

# Your experiment proposal
experiment = {
    "id": "sai_composition_v2",
    "title": "SAI Particle Chemical Composition Analysis", 
    "methodology": "Multi-domain validation using GLENS ensemble data",
    "parameters": {
        "h2so4_concentration_percent": 75.0,
        "temperature_k": 220.0,
        "ensemble_size": 20
    }
}

# Process through pipeline
result = pipeline.process_experiment(experiment)
```

### **What Happens Automatically:**

#### **🔍 Forensic Synthetic Data Detection (Automates Your Manual Process)**
- ✅ **Detects unrealistic parameters** (e.g., perfect values like 1.0, 10.0)
- ✅ **Identifies missing natural variability** (red flag for synthetic data)
- ✅ **Finds unit inconsistencies** (common in generated data)
- ✅ **Discovers perfect mathematical relationships** (unlikely in real data)

#### **🔄 Automated Corrections (Replaces Manual Changes)**
- ✅ **Replaces synthetic data with authentic GLENS values**
- ✅ **Adds natural variability indicators**
- ✅ **Fixes unit inconsistencies**
- ✅ **Adjusts unrealistic parameters to physical ranges**

#### **✅ Sakana Principle Validation**
- ✅ **Domain-specific validation** (chemical composition constraints for next experiments)
- ✅ **Real GLENS data verification** (institutional validation)
- ✅ **Statistical significance** (p < 0.05, confidence ≥ 0.95)
- ✅ **Order-of-magnitude parameter checking** (physically realistic ranges)

### **Stage 2: Enhanced Researcher Generation (Only for Validated Experiments)**

```python
# If pre-validation passes, experiment goes to Researcher with enhancement
enhanced_context = {
    "validated_domain": "Chemical composition validation passed",
    "approved_datasets": ["GLENS", "ARISE-SAI"],
    "statistical_requirements": "p < 0.05, 20-member ensemble",
    "quality_guidelines": "Avoid plausibility traps, require empirical grounding"
}

# Researcher generates 128-page paper with validated context
# This produces higher quality papers because they're based on validated foundations
```

### **Stage 3: Final Quality Assurance**

```python
# Final verification ensures consistency between validation and generation
final_check = {
    "validation_consistency": "Ensured",
    "sakana_compliance": "Verified", 
    "quality_metrics": "Above threshold",
    "ready_for_publication": True
}
```

---

## 📊 **Results Analysis**

### **Processing Results:**

```python
if result['final_status'] == 'SUCCESS':
    print("✅ Super paper generated successfully!")
    print(f"📄 Paper: {result['generated_paper']}")
    print(f"⏱️  Time: {result['pipeline_duration']} seconds")
    print(f"🎯 Quality: {result['stage_results']['post_verification']['quality_metrics']}")
    
elif result['final_status'] == 'REJECTED_AT_PRE_SCREENING':
    print("❌ Experiment rejected at pre-screening (saved time!)")
    print(f"💡 Issues: {result['stage_results']['pre_validation']['validation_details']['violations']}")
    print(f"⏱️  Time saved: ~300 seconds (avoided futile Researcher generation)")
    
else:
    print("🔄 Manual intervention required")
    print(f"📋 Report: {result['stage_results']}")
```

### **Efficiency Gains:**

```python
# Get pipeline statistics
stats = pipeline.get_pipeline_statistics()

print(f"📈 Success rate: {stats['success_rate']:.1%}")
print(f"⚡ Pre-screening efficiency: {stats['pre_screening_rejection_rate']:.1%}")
print(f"💰 Time saved: {stats['efficiency_improvement']}")
print(f"🤖 Automation effectiveness: {stats['automation_effectiveness']:.1%}")
```

---

## 🎛️ **Configuration Options**

### **For Your Current Situation (Recommended):**

```python
from ai_researcher.pipeline.pipeline_config import RECOMMENDED_IMPROVED_CONFIG

# This configuration automates your manual correction workflow
config = RECOMMENDED_IMPROVED_CONFIG
# - Pre-validation gateway enabled
# - Synthetic data detection automated  
# - 3 automated correction cycles
# - Institutional validation required
# - Mac M3 optimized
```

### **Development/Testing:**

```python
from ai_researcher.pipeline.pipeline_config import DEVELOPMENT_CONFIG

# More lenient settings for experimentation
config = DEVELOPMENT_CONFIG
# - 5 correction cycles allowed
# - Intermediate results saved for debugging
# - Less strict validation for testing
```

### **Production Deployment:**

```python
from ai_researcher.pipeline.pipeline_config import PRODUCTION_CONFIG

# Optimized for production efficiency
config = PRODUCTION_CONFIG  
# - Strict validation enforced
# - Performance optimized
# - Minimal intermediate storage
```

---

## 🚀 **Quick Start Example**

### **Replace Your Current Manual Process:**

```python
# OLD WAY (Your current pain):
# 1. experiment → researcher → paper (128 pages, 5+ minutes)
# 2. paper → sakana → manual testing and corrections
# 3. repeat until it works (could be many cycles)

# NEW WAY (Automated):
from ai_researcher.pipeline import IntegrationPipeline

pipeline = IntegrationPipeline("/Users/apple/code/ai-s-plus/data/glens")

experiment = {
    "title": "SAI Chemical Composition Study",
    "parameters": {"h2so4_concentration_percent": 75.0, "temperature_k": 220.0}
}

# Single call handles everything automatically
result = pipeline.process_experiment(experiment)

# Either get a validated super-paper OR early rejection (saving time)
if result['final_status'] == 'SUCCESS':
    publish_paper(result['generated_paper'])  # Ready to go!
elif result['final_status'] == 'REJECTED_AT_PRE_SCREENING':
    fix_experiment(result['violations'])  # Clear guidance on what to fix
```

---

## 🛠️ **Advanced Usage**

### **Custom Validation Rules:**

```python
# Add your own validation criteria
custom_validator = SakanaValidator(enforcement_level='strict')
custom_validator.validation_criteria.update({
    'custom_chemical_ranges': {'h2so4_concentration_percent': (60.0, 90.0)},  # Stricter composition ranges
    'required_ensemble_size': 30,   # Larger than standard 20
    'custom_confidence_level': 0.99 # Higher than standard 0.95
})

pipeline = IntegrationPipeline(
    glens_data_path="/path/to/data",
    custom_validator=custom_validator
)
```

### **Batch Processing:**

```python
# Process multiple experiments efficiently
experiments = [exp1, exp2, exp3, exp4, exp5]

results = []
for exp in experiments:
    result = pipeline.process_experiment(exp)
    results.append(result)
    
    # Pre-screening rejects bad experiments early (saves time)
    if result['final_status'] == 'REJECTED_AT_PRE_SCREENING':
        print(f"❌ {exp['title']} rejected - saved 5+ minutes")
    elif result['final_status'] == 'SUCCESS':
        print(f"✅ {exp['title']} - super paper generated!")

# Analyze batch results
successful = [r for r in results if r['final_status'] == 'SUCCESS']
print(f"📊 Batch success rate: {len(successful)}/{len(experiments)}")
```

### **Integration with Your Existing Researcher System:**

```python
# Connect to your existing Researcher framework
pipeline = IntegrationPipeline(
    glens_data_path="/Users/apple/code/ai-s-plus/data/glens",
    researcher_config={
        "model_size": "12B",  # Your current Researcher model
        "api_endpoint": "http://localhost:8000/generate",
        "timeout": 600  # 10 minutes for complex papers
    }
)

# The pipeline will call your Researcher system automatically
# when experiments pass pre-validation
```

---

## 🎯 **Key Benefits for Your Workflow**

1. **⚡ Prevents Wasted Effort:** No more generating 128-page papers that fail validation
2. **🤖 Automates Manual Corrections:** Replaces your "test and change reports" workflow  
3. **🔍 Automated Synthetic Detection:** No more manual forensic data checking
4. **📈 Higher Quality Papers:** Researcher gets validated input = better output
5. **💰 Time Savings:** Pre-screening rejects bad experiments in seconds vs. minutes
6. **🎯 Consistent Quality:** Sakana Principle enforcement prevents plausibility traps

**Bottom Line:** This transforms your manual, time-intensive correction process into an automated, efficient pipeline that produces higher quality results with less effort.

---

## 📞 **Next Steps**

1. **Test the pipeline** with one of your existing experiments
2. **Compare time/quality** vs. your current manual process  
3. **Configure settings** for your specific workflow
4. **Integrate with existing Researcher** system
5. **Scale to batch processing** for multiple experiments

The pipeline is designed to seamlessly replace your current manual workflow while maintaining the high quality standards of the Sakana Principle.