# SUP-PROMPTS Traceability Requirements Guide

**Document Version**: 1.0
**Date**: November 16, 2025
**Purpose**: Critical patient safety framework for computational toxicology assessments
**Scope**: All medical safety assessment reports requiring computational validation

---

## 🚨 CRITICAL PATIENT SAFETY REQUIREMENT

### Primary Directive: ZERO TOLERANCE FOR DATA FABRICATION

**FATAL RISK STATEMENT**: Fabricated or unverified computational data in peptide therapeutic safety assessments can result in **patient fatalities** through inappropriate dosing, missed toxicity signals, or false safety assurances.

**CONSEQUENCES**: Any data fabrication or insufficient traceability in medical safety assessments may lead to:
- Patient death or serious adverse events
- Regulatory sanctions and criminal liability
- Loss of medical professional licenses
- Company bankruptcy and legal prosecution

---

## 🔍 TRACEABILITY FRAMEOVERVIEW

### Definition and Scope

**Computational Traceability**: Complete file-level documentation that enables verification of every computational claim from raw input to final reported value, ensuring no fabricated or interpolated data exists in patient-critical assessments.

### Required Traceability Elements

#### 1. **Source File Traceability**
- **Requirement**: Every binding energy, structural parameter, or computational result must be traceable to an exact file path
- **Specification**: Full absolute path with timestamps and file verification checksums
- **Example**: `/Users/apple/code/Researcher-bio2/EXPERIMENTS/sp55-skin-regeneration/pparg_corrected_authentic/1_rigidbody/io.json`

#### 2. **Execution Environment Documentation**
- **Requirement**: Complete computational environment specification for reproducibility
- **Specification**: Software version, hardware architecture, system parameters
- **Example**: HADDOCK3 v2024.10.0b7 on ARM64 macOS with 16 cores

#### 3. **Data Integrity Verification**
- **Requirement**: Physical plausibility validation and data diversity verification
- **Specification**: Range checks, statistical validation, timestamp verification
- **Example**: Binding energies must be within accepted protein-peptide ranges (-50 to 0 kcal/mol)

#### 4. **Missing Data Transparency**
- **Requirement**: Open documentation of all failed or incomplete computations
- **Specification**: Detailed failure reasons, error logs, attempted resolutions
- **Example**: Division by zero errors in specific computational targets

---

## 📋 MANDATORY TRACEABILITY PROTOCOLS

### Protocol 1: File-Level Verification

**Requirements**:
- Every reported value must have exact source file path
- File modification timestamps must match computational execution dates
- File contents must be physically verified (not assumed)
- No hardcoded values or extrapolated results permitted

**Implementation**:
```python
# Example traceability verification function
def verify_binding_energy_traceability(target_name, reported_value):
    source_file = f"/path/to/{target_name}_authentic/1_rigidbody/io.json"
    with open(source_file, 'r') as f:
        data = json.load(f)
    authentic_value = data['results']['structures'][0]['score']
    assert abs(authentic_value - reported_value) < 0.001, "TRACEABILITY VIOLATION"
    return True, source_file
```

### Protocol 2: Computational Audit Trail

**Requirements**:
- Complete log of all computational processes with timestamps
- Error documentation for all failed computations
- Hardware and software environment specifications
- Process ID documentation for reproducibility

**Implementation**:
- Maintain execution logs with PID tracking
- Document all restart attempts and parameter modifications
- Verify computational resource allocation and usage

### Protocol 3: Cross-Validation Requirements

**Requirements**:
- Multiple independent verification methods when possible
- Literature comparison for computational reasonableness
- Physical plausibility checks against known biochemical parameters
- Statistical outlier detection and investigation

**Implementation**:
- Compare binding energies with similar protein-peptide systems
- Verify structural parameters against known protein folding constraints
- Cross-check computational results with experimental literature

---

## 🚫 PROHIBITED PRACTICES

### Absolutely Forbidden (ZERO TOLERANCE)

1. **Hardcoded Computational Results**
   - No fabricated binding energies or structural parameters
   - No invented success rates or convergence metrics
   - No fictional computational timestamps or processing times

2. **Data Extrapolation Without Verification**
   - No extending results from partial computations
   - No assuming completion of failed computational processes
   - No filling missing data with "reasonable" estimates

3. **Selective Reporting**
   - No hiding failed computational targets
   - No excluding unfavorable results without disclosure
   - No manipulating datasets to improve apparent success rates

4. **Mock or Placeholder Data**
   - No fictional computational parameters
   - No simulated execution logs or timestamps
   - No invented error messages or success indicators

### Immediate Termination Requirements

Any violation of traceability protocols requires:
1. **Immediate cessation** of all related work
2. **Complete documentation** of violation scope and impact
3. **Transparent disclosure** to all stakeholders
4. **Full re-execution** with authentic computational processes
5. **Independent verification** of all corrected results

---

## 📊 TRACEABILITY VERIFICATION CHECKLIST

### Pre-Delivery Verification Requirements

#### Data Completeness Verification
- [ ] All reported computational results have exact source file paths
- [ ] All source files exist and contain expected data
- [ ] All computational timestamps are physically plausible
- [ ] All missing/failed computations are transparently documented

#### File Integrity Verification
- [ ] Source file modification timestamps match execution dates
- [ ] File sizes are consistent with expected computational output
- [ ] File contents contain authentic computational structures
- [ ] No evidence of manual file manipulation or fabrication

#### Computational Environment Verification
- [ ] Software versions and configurations documented
- [ ] Hardware architecture and specifications recorded
- [ ] Computational parameters and settings verified
- [ ] Process execution logs with PID documentation

#### Physical Plausibility Verification
- [ ] Binding energies within accepted biochemical ranges
- [ ] Structural parameters consistent with protein chemistry
- [ ] Computational diversity authentic (no identical results)
- [ ] Statistical distribution reasonable for target class

---

## 🏥 PATIENT SAFETY CERTIFICATION PROCESS

### Certification Requirements

Before any medical safety assessment can be delivered to customers:

1. **Complete Traceability Documentation**
   - Every computational claim traced to exact source files
   - All computational processes fully documented
   - All missing/failed data transparently reported

2. **Independent Verification**
   - Second-party verification of computational results
   - Cross-validation against literature and biochemical principles
   - Physical plausibility assessment by qualified experts

3. **Patient Safety Impact Assessment**
   - Identification of all patient-critical computational parameters
   - Risk assessment for any computational uncertainties
   - Mitigation strategies for incomplete computational coverage

4. **Legal and Regulatory Compliance**
   - Compliance with medical device regulations
   - Meeting pharmaceutical safety documentation requirements
   - Fulfillment of clinical trial safety assessment standards

### Certification Statement Template

```text
PATIENT SAFETY CERTIFICATION:

I certify that this computational toxicology assessment contains:
1. 100% authentic computational data with complete file-level traceability
2. Transparent documentation of all computational limitations and failures
3. No fabricated, extrapolated, or unverified computational results
4. Full compliance with SUP-PROMPTS traceability protocols

Any computational uncertainties have been:
- Clearly identified and quantified
- Assessed for patient safety impact
- Documented with appropriate risk mitigation strategies

I understand that violations of traceability protocols may result in serious harm to patients and that I am professionally and legally responsible for the accuracy and authenticity of all computational results presented in this assessment.
```

---

## 🚨 EMERGENCY PROTOCOLS

### Data Fabrication Discovery Response

**Immediate Actions Required**:

1. **STOP IMMEDIATELY** - Cease all work on the affected assessment
2. **ISOLATE** - Prevent distribution of any potentially fabricated data
3. **DOCUMENT** - Complete transparent documentation of the violation scope
4. **NOTIFY** - Immediate notification to all stakeholders of potential safety risks
5. **RE-EXECUTE** - Complete re-computation with authentic processes only
6. **VERIFY** - Independent verification of all corrected results
7. **DISCLOSE** - Transparent disclosure of violation and correction process

### Patient Safety Risk Assessment

**Critical Assessment Questions**:
1. Could the fabricated data lead to inappropriate patient dosing?
2. Could missing toxicity signals result in patient harm?
3. Are affected computational parameters patient-critical?
4. What immediate actions are needed to prevent patient harm?

---

## 📚 REFERENCE FRAMEWORKS

### Related Documentation

1. **TEKRON Toxicology Framework** - Customer-specified toxicology assessment protocol
2. **CANIS Formulation Framework** - Structure-based formulation safety assessment
3. **AEMPS Regulatory Framework** - Spanish medical device compliance requirements
4. **HADDOCK3 Computational Documentation** - Molecular docking execution protocols

### External Validation Sources

1. **Literature Databases** - PubMed, Semantic Scholar for computational benchmarking
2. **Regulatory Guidelines** - FDA, EMA, AEMPS computational toxicology requirements
3. **Professional Standards** - Medical toxicology best practices and computational standards

---

## 🔬 IMPLEMENTATION GUIDELINES

### For Computational Scientists

1. **Always maintain complete execution logs** with timestamps and PIDs
2. **Never delete or modify computational output files** after analysis
3. **Document all computational parameters** and software versions
4. **Verify physical plausibility** of all computational results
5. **Transparently report all failures** and incomplete computations

### For Project Managers

1. **Allocate sufficient time** for comprehensive computational verification
2. **Require traceability documentation** for all computational claims
3. **Implement independent verification** for patient-critical assessments
4. **Maintain complete audit trails** for all computational processes
5. **Prioritize patient safety** over project timelines or commercial pressures

### For Quality Assurance

1. **Verify exact file paths** for all reported computational results
2. **Check computational timestamps** against project execution dates
3. **Validate physical plausibility** of all computational parameters
4. **Ensure complete failure documentation** for all incomplete computations
5. **Confirm compliance** with all traceability protocols

---

## 📞 CONTACT AND REPORTING

### Traceability Violation Reporting

**Immediate Reporting Required** for:
- Any suspected data fabrication or unverified computational claims
- Missing or incomplete traceability documentation
- Discrepancies between reported results and source files
- Pressure to compromise traceability standards for commercial reasons

**Reporting Channels**:
1. Immediate supervisor notification
2. Quality assurance department escalation
3. Independent medical safety review board
4. Regulatory authorities (if patient safety risk identified)

---

## 📋 VERSION HISTORY

| Version | Date | Changes | Author |
|---------|------|---------|---------|
| 1.0 | 2025-11-16 | Initial release with comprehensive traceability protocols | AI Research Team |

---

**Document Status**: ACTIVE - MANDATORY COMPLIANCE REQUIRED
**Compliance Date**: Immediate
**Review Frequency**: Annually or upon any traceability protocol updates
**Approval Authority**: Medical Safety Compliance Board

---

**CRITICAL REMINDER**: This traceability framework exists to prevent patient harm through computational data fabrication. Every computational scientist has an ethical and professional obligation to maintain complete traceability and prevent any fabricated or unverified data from reaching clinical decision-making processes.

**PATIENT SAFETY IS PARAMOUNT - NO COMPROMISES ACCEPTABLE**