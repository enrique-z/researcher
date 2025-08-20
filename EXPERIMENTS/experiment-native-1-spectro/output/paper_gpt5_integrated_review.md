

## Review checkpoint




## Review checkpoint

Summary
The manuscript proposes an “active climate spectroscopy” framework for stratospheric aerosol injection (SAI) that treats small-amplitude, designed pulsed injections as probes to estimate frequency-dependent climate gains, lags, and weak nonlinear distortions. It integrates: (i) information-optimal multisine/PRBS/chirp input design under environmental constraints; (ii) nonparametric FRF estimation with multi-taper methods; (iii) compact rational fits and second-order Volterra kernels for nonlinear distortion; (iv) robust control synthesis (H-infinity, MPC) using spectroscopy-derived uncertainty; and (v) early-warning indicators based on spectral phase drift and harmonic distortion. Cross-model robustness, practicality, and minimal invasiveness are emphasized.

Soundness
- The use of frequency-domain system identification, Fisher-information/MI-based input design, and multi-taper spectral regression is methodologically sound and well grounded in control/identification literature.
- Assumptions: local linearity and (cyclo)stationarity around a baseline u0 are plausible for small perturbations, but climate exhibits seasonality, slow drift, and long memory; the manuscript partly acknowledges this (windowing, ensemble averaging) but should treat cyclostationary/LTP structure more explicitly.
- FRF and coherence-based uncertainty mapping are appropriate, but the proposed coherence-to-weight transformation for robust design is heuristic and should be justified or bounded.
- Quadratic Volterra modeling is reasonable for weak nonlinearities; identifiability with many interaction lines under colored noise requires careful line planning, sparsity, and ample data—feasibility needs quantitative power analyses.
- Control synthesis over identified MIMO surrogates is standard; small-gain/μ-based robustness with multiplicative uncertainty is appropriate. Ensuring integral action and constraint robustness for nonstationary baselines is critical.
- Early-warning via phase drift and HDI is intriguing but speculative; links between phase trends toward −π and impending instabilities in this application should be validated (e.g., controlled bifurcation experiments in ESMs).

Presentation
- Technically clear and rigorous, but dense. Notation shifts between G/H and time/frequency domains; define and stick to a single convention early (MIMO vs SISO, z vs e^{jω}).
- “E1–E6” are referenced but not defined in the provided text; include a brief experiment map.
- Some citations appear placeholder-like (e.g., enhanced_…_20250812); these must be replaced by archival references or removed.
- A schematic figure showing the workflow from probe design to identification, control, and monitoring would greatly aid readers.

Contribution
- Novel integration of information-optimal active probing, frequency-domain identification (including quadratic Volterra kernels), and robust control tailored to SAI.
- Moves beyond step/ramp protocols to directly measure control-relevant spectral pathways and to quantify weak nonlinear distortions.
- Introduces control-oriented VOI metrics linking Fisher information to expected regret reduction.
- Proposes spectral early-warning indicators that leverage the same probes as identification/control.

Strengths
- Well-founded methodology spanning input design, estimation, modeling, and control.
- Risk-aware constraints (SAOD, ozone) incorporated directly into probe design and MPC.
- Data efficiency via multisine/PRBS, multi-tapering, line-synchronized windows.
- Clear path to robust controller synthesis with explicit uncertainty shaping.
- Cross-model transfer and practicality considerations are built in.

Weaknesses
- LTI/cyclostationary assumptions may be violated by seasonal and secular evolution; treatment of LTP/TV dynamics is limited.
- Identifiability at interannual frequencies with RMS amplitudes 0.05–0.5 TgS/yr may demand long durations and/or large ensembles; quantitative feasibility is not demonstrated.
- Volterra identification could be underdetermined without careful tone grids and detection slots; sample-complexity analysis is missing.
- Coherence-based uncertainty weighting for robust design is heuristic; no bounds linking coherence to multiplicative model error are provided.
- MIMO aspects (multiple outputs and possibly multiple geographically distributed inputs) are underdeveloped; most derivations are SISO.
- Early-warning interpretations risk false positives from background variability or slow drift; statistical calibration not specified.
- Placeholder references and minor notation inconsistencies reduce polish.

Suggestions
- Explicitly adopt and analyze a cyclostationary/LTP framework: seasonally locked multisines, periodic FRFs, or time-frequency FRFs; report leakage/alias mitigation for seasonal harmonics.
- Provide power/feasibility calculations: target coherence curves vs. amplitude/duration/ensemble size using Svv from control runs and plausible |G(ω)|; include numeric examples at key bands (annual to multi-year).
- Formalize sample complexity for quadratic kernels (number of tones, detection slots, sparsity level, variance) and show synthetic recoveries under colored noise typical of ESMs.
- Justify uncertainty weights: derive conservative bounds from FRF CIs, instrumental-variable spectral regression, or bootstrap across ensembles; validate against held-out volcano-like shocks.
- Elevate MIMO formulation: jointly identify cross-channel FRFs, include cross-spectral structure, and design controllers with regional outputs and possibly multiple injection latitudes/altitudes.
- Ensure integral action/ref-tracking robustness in H∞/MPC to handle slow baseline drift; consider LPV or gain-scheduled controllers as u0/forcing changes.
- Calibrate and backtest early-warning indicators with controlled bifurcation tests (e.g., gradually tightening feedbacks) and report lead-time vs. false-alarm metrics against passive baselines.
- Replace placeholder citations; add references on periodic identification, nonlinear FRFs in practice, and climate-relevant early-warning theory.
- Define E1–E6 explicitly and add a workflow figure; unify notation (G vs H; q−1 vs z−1; ω units).
- State governance/operational feasibility: actuator limits, logistics of month-scale modulation, and acceptable SAOD excursions.

Questions
- What experiment lengths and ensemble sizes are required to achieve γ^2 ≥ 0.6–0.8 at 0.1–0.3 cycles/yr for GMST and key precipitation indices given typical Svv? Provide quantitative targets.
- How will seasonality be handled—deseasonalization, periodic identification, or explicit cyclostationary models?
- Can you demonstrate that RMS 0.05–0.5 TgS/yr perturbations remain within acceptable SAOD/ozone bounds across models, especially under differing aerosol microphysics?
- How sensitive are FRFs and Volterra kernels to background state (u0, GHG pathway)? Will you use LPV/TV identification or re-linearize periodically?
- What is the precise MIMO setup (inputs: latitude/altitude channels? outputs: which regional indices) and how do you handle cross-couplings in identification and control?
- How are multiplicative uncertainty weights W_m constructed from FRF CIs in practice, and how conservative are they across models?
- What guarantees link phase-drift and HDI growth to instability in this system class? How will you avoid confounding from ENSO/volcanic transients?
- Do controllers include integral action and constraint tightening to ensure feasibility under model mismatch and rate/SAOD limits?
- How will you validate transferability of controllers between ESMs with different aerosol microphysics and stratospheric circulation?
- Can you provide a minimal worked example (aquaplanet) with numbers: probe design, achieved information gain, FRF/Volterra recovery, and closed-loop performance?

Rating (1-10)
7


## Review checkpoint

Summary
The manuscript proposes “active climate spectroscopy” for stratospheric aerosol injection (SAI): injecting small, information-optimized multisine/PRBS/chirp perturbations atop a baseline to identify frequency-dependent gains, lags, and weak nonlinearities of climate responses. It develops (i) Fisher-information–optimal probe design under environmental constraints; (ii) frequency response estimation with multitaper methods and coherence QC; (iii) second-order Volterra kernel estimation for harmonic/intermodulation distortion; (iv) robust control synthesis (H-infinity, MPC) using identified surrogates; and (v) early-warning indicators based on phase drift and distortion growth. Cross-model practicality and identifiability budgeting are discussed.

Soundness
- Conceptual: Framing SAI as an active system-identification problem is well-motivated and aligns with control needs. The use of FRF, coherence, and Fisher-information design is standard and appropriate.
- Assumptions: Local linear time-invariant (LTI) behavior around a baseline with weak nonlinearity is plausible for small perturbations, but time-variation (seasonality, slow drifts) and structural nonstationarity in ESMs are significant. The text partially acknowledges cyclostationarity and sliding windows but could strengthen treatment of LTP (linear time-periodic) dynamics.
- Identifiability: Clear articulation of SNR/coherence, crest-factor control, and leakage handling. However, claims of resolving 0.02 yr−1 bands are hard to support without very long records/ensembles. Quadratic Volterra identification at scale may be challenging without careful sparsity design and frequency-grid planning.
- Control: Mapping FRF residuals and coherence into robust uncertainty weights is sensible; proposed H∞/MPC formulations are standard and compatible with surrogate models. Robustness to unmodeled dynamics and cross-model transfer needs empirical demonstration.

Presentation
- Generally clear, technically precise, and well-structured by tasks (design, estimation, nonlinearity, control, early warning).
- Repetition across sections (coherence, FIM) could be consolidated; notation alternates between G and H for FRFs.
- Several references appear as placeholders (e.g., enhanced_2_20250812), which are not standard citations and must be replaced or removed.
- Equation labels repeat across sections (e.g., coherence), risking ambiguity.

Contribution
- Introduces an integrated, control-oriented, frequency-domain methodology for SAI: info-optimal probing, FRF/Volterra identification, robust control synthesis, and active early-warning.
- Brings optimal input design and MI/Fisher calculus to climate-intervention experiments with explicit environmental/chemistry constraints.
- Proposes practically motivated EWS (phase-drift and distortion) derived from the same active probes that identify/control the system.

Strengths
- Strong, coherent integration of system identification, information theory, and robust control tailored to SAI.
- Careful attention to leakage, crest-factor, coherence, and ensemble design.
- Early-warning indicators grounded in dynamical phase and nonlinearity rather than passive variance alone.
- Clear control formulations (mixed-sensitivity H∞, constrained MPC) with uncertainty shaping tied to identified spectra.
- Emphasis on minimal intrusiveness via small amplitudes and constraints on SAOD/ozone.

Weaknesses
- LTI assumption is strained by seasonal LTP dynamics, slow drift in background forcings, and regime shifts; treatment of time-variation is incomplete.
- Low-frequency claims (≈0.02 yr−1) are impractical without decades-long windows or very large ensembles; feasibility not quantified.
- SISO input abstraction (global-equivalent injection rate) ignores strong dependence on latitude/altitude/season of injection; MIMO formulation is likely necessary for regional objectives.
- Volterra identification complexity and risk of spectral collisions are under-quantified; scalability to multi-output, colored noise settings requires more detail.
- Several nonstandard “enhanced_...” citations appear fabricated or placeholder; undermines credibility.
- Repetition and notation drift (G vs H, duplicate equation tags) reduce clarity.

Suggestions
- Replace LTI with an LTP/harmonic transfer function framework to explicitly handle seasonality; estimate harmonic FRFs and use cyclostationary identification tools.
- Provide a quantitative identifiability budget: for representative Svv and |G|, specify amplitude, window length, ensemble size needed to achieve γ^2 targets at selected bands; include a table/figure with power analyses.
- Extend to MIMO inputs reflecting injection latitude/altitude channels; identify MIMO FRFs and revisit controller structure for gradient/ITCZ control.
- Consolidate repeated material; unify notation (choose G or H consistently) and ensure unique equation numbering.
- Remove/replace all “enhanced_...” references with peer-reviewed sources or move derivations to an appendix without citing placeholders.
- Clarify how SAOD/ozone constraints are evaluated during design (emulator, linearization validity, safety factors), and how nonlinearity in aerosol microphysics is handled at higher amplitudes.
- Expand uncertainty modeling: structured model sets across multiple ESMs for robust design and μ-analysis; explicitly show transfer performance and margins.
- For early warning, add statistical control of false-alarm rates (e.g., sequential testing with FDR control) and show comparative ROC/lead-time results versus passive EWS in a toy or pilot dataset.
- Discuss operational/logistical constraints on injection scheduling and how they map into actuation limits or integer/scheduling constraints in MPC.

Questions
- What experiment durations and ensemble sizes are required to achieve γ^2 ≥ 0.6–0.8 at 0.25–1 yr−1 for GMST and key regional indices, given baseline Svv from specific ESMs?
- How will seasonality be handled formally—can you adopt an LTP/harmonic FRF approach rather than assuming LTI in sliding windows?
- How many tones and what spacing avoid intermodulation collisions given internal climate bands (annual, semiannual, QBO, ENSO)?
- Can you provide a concrete MIMO input design (e.g., two latitude bands × two altitudes) and show the gain/phase diversity it enables for regional precipitation control?
- How are SAOD/ozone constraints computed in design—via linear operators H_SAOD/H_chem, or via an emulator? What are their validated ranges?
- What sparsity levels and regularization paths are required to recover quadratic Volterra terms reliably with colored noise and limited data?
- How sensitive are the robust-control weights Wm and Wh to cross-ensemble variability and cross-model shifts? Do you certify margins via μ-analysis?
- How will you set detection thresholds for the early-warning index to control false alarms under time-varying backgrounds?

Rating (1-10)
7


## Review checkpoint




## Review checkpoint

Summary
The manuscript proposes an “active spectroscopy” framework for stratospheric aerosol injection (SAI) modeled as a control-oriented, frequency-domain system identification problem. It combines information-optimal input design (multi-sine/PRBS/chirps), leakage-aware spectral regression to estimate frequency response functions (FRFs), sparse second-order Volterra modeling of nonlinear distortions, robust control synthesis (H-infinity, MPC), and sliding-window early-warning indicators based on phase drift and harmonic/intermodulation growth. The authors outline uncertainty quantification, cross-model validation, and practicality trade-offs (amplitude–duration–ensemble). The work aims to produce compact, control-ready surrogates and actionable monitoring signals with minimal intrusion.

Soundness
- The core methodology (FRF estimation, Fisher information–based input design, coherence targeting, mixed-sensitivity H-infinity, MPC, Volterra kernels) is standard and sound in system identification and control.
- Assumptions (local LTI/LTV behavior around an operating point, small-signal regime, cyclostationarity under designed excitation) are plausible but will be strained by seasonal cycle, slow drift, and colored low-frequency variability in ESMs. The manuscript partly addresses this with multitapering, synchronized windows, and ensemble averaging.
- Early-warning use of phase-drift and harmonic distortion is reasonable, but statistical power and specificity versus confounders (seasonality, nonstationary variability, external shocks) must be demonstrated empirically.
- Some derivations adopt asymptotic/Whittle approximations; their validity under practical record lengths in ESMs warrants stress tests.

Presentation
- The exposition is thorough and technically rigorous, with clear links among design–identify–control–monitor loops.
- Notation drifts across sections (G vs H for FRF; y_t vs y[n]; v_t vs e_t; ω-range definitions). There are small inconsistencies in frequency bands (e.g., “0.02–2 cycles/yr” vs “50 months–6 months”).
- Several citations appear placeholder-like (e.g., enhanced_*, “Comprehensive/Smart Discovery System”) and should be replaced with citable sources or removed.
- A figure/table roadmap summarizing the workflow, bands, and constraints would improve accessibility.

Contribution
- Novel integration of optimal input design and frequency-domain identification with SAI modeling, robust control synthesis, and active early-warning—moving beyond step/ramp protocols.
- Clear, control-relevant surrogates and uncertainty sets tied to coherence and Fisher information.
- A concrete cross-model transferability and certification plan.

Strengths
- Methodologically mature: leverages best practices in frequency-domain identification, leakage control, and robust control.
- Decision relevance: turns identification uncertainty into controller weights, robustness margins, and VOI.
- Minimally intrusive probing with explicit environmental/chemistry constraints.
- Thoughtful UQ, cross-model validation, and practicality budgeting.
- Explicit nonlinear diagnostics (Volterra, HDI, bicoherence) and their use for early warning.

Weaknesses
- Realism risks: LTI/LTV approximations under strong seasonality, drift, and regime shifts; quadratic truncation may miss key nonlinearities (e.g., aerosol–chemistry–dynamics feedbacks).
- Frequency-band inconsistencies and limited discussion of cyclostationary/seasonal identification (PTV/BLA) beyond deseasonalization.
- Single-input emphasis early vs later MIMO—practical multi-actuator feasibility and identifiability need clearer treatment.
- Early-warning claims need quantitative comparison to passive baselines under realistic SNR and nonstationarity.
- Placeholder/unclear citations undermine credibility.
- Practical constraints (ozone, SAOD, microphysics adjustment, actuator slew) are modeled linearly; validation of these linearized constraint maps is needed.

Suggestions
- Unify notation and correct band definitions; explicitly adopt a cyclostationary/BLA or periodic time-varying identification framework to handle the seasonal cycle.
- Replace placeholder citations with established references; consolidate citation style.
- Provide a synthetic-truth study and a demonstration on at least one intermediate-complexity model to quantify: (i) SNR/coherence achieved, (ii) FRF parameter CIs vs amplitude–length–ensemble, (iii) bias/leakage under drift.
- Report power analyses for early-warning (lead time, false-alarm control) across ensembles; include volcano-shock stress tests.
- Clarify environmental constraints: how H_SAOD and H_chem are obtained/validated; sensitivity to their mis-specification.
- Detail MIMO actuation designs (orthogonal coding, line allocation) and identifiability, including actuator-region mapping and practicality.
- Compare against step/ramp baselines on equal computational budget to show efficiency gains.
- Release code and standardized protocols for reproducibility.

Questions
- What record lengths and ensemble sizes are required to achieve target coherence (e.g., γ^2≥0.6) across ENSO/monsoon bands at RMS 0.05–0.5 TgS/yr? Provide quantitative design charts.
- How do you handle cyclostationarity explicitly—seasonal BLA or time-periodic FRFs—instead of simple deseasonalization?
- How robust are the results to slow operating-point drift (e.g., rising GHG forcing) within identification windows?
- How were linearized maps for SAOD/ozone constraints constructed and validated across amplitudes and backgrounds?
- What is the observed magnitude of harmonic/intermodulation power relative to internal variability at the proposed amplitudes?
- For multi-actuator designs, what geographic configurations are assumed, and how well are cross-couplings identifiable with PRBS/multisine coding?
- How sensitive are controller robustness margins to cross-model FRF mismatch, and what are acceptable thresholds for J_rel and small-gain ρ?

Rating (1-10)
7


## Review checkpoint

Summary
- The manuscript proposes “active climate spectroscopy” for SAI: small, information-optimized multisine/PRBS/chirp perturbations superimposed on a baseline injection to estimate frequency-dependent gains, lags, and weak nonlinearities in ESMs. 
- It integrates frequency-domain system identification, Fisher-information-based input design, sparse Volterra modeling, robust H-infinity/MPC control synthesis, and early-warning indicators based on spectral phase drift and harmonic/intermodulation growth. 
- It further outlines cross-model validation, uncertainty quantification, spectral emulation, and multi-objective robust controller design aligned with ARISE-SAI/GeoMIP protocols.

Soundness
- Methodological core is solid and draws on mature system identification and robust control theory. The Fisher information and coherence-based design rules are appropriate for colored internal variability; leakage/tapering practices are standard.
- The linear time-invariant (LTI) approximation around a baseline with small RMS perturbations is plausible for GMST and some indices, but time variation (seasonality, slow drift) and aerosol-chemistry nonlinearities may be nontrivial for regional precipitation and stratospheric dynamics. The manuscript acknowledges this and proposes sliding windows and nonlinear diagnostics, but practical limits need empirical confirmation.
- Early-warning via phase drift and harmonic distortion is conceptually sound; however, evidence that these outperform passive EWS in ESMs remains to be demonstrated.
- Control synthesis is well-framed (mixed-sensitivity/structured uncertainty; MPC with chance constraints); constructing frequency-shaped uncertainty from identification residuals is appropriate.

Presentation
- Comprehensive and technically rigorous, but very dense and occasionally repetitive across sections.
- Notation is mostly consistent but reuses labels (e.g., eq:coherence) and has minor LaTeX issues (e.g., unmatched brace in the ozone constraint; repeated equation labels; some citation keys like “enhanced_…”, “Comprehensive/Smart Discovery System” appear placeholder-like and need replacement with real references).
- Clearer separation of assumptions, limitations, and required conditions for validity would improve readability. A schematic workflow figure would help.

Contribution
- Novel synthesis: brings information-optimal frequency-domain identification and nonlinear spectroscopy to SAI, directly linked to robust control and early warning.
- Provides a concrete, control-ready path from ESM experiments to certified controllers and monitoring tools, with cross-model transfer metrics and UQ.
- Fills a gap between scenario-based studies and closed-loop design by instrumenting temporal modulation explicitly.

Strengths
- Strong theoretical grounding; end-to-end pipeline from probe design to control and monitoring.
- Risk-aware constraints (SAOD/ozone) embedded in experiment design; emphasis on minimal invasiveness.
- Practical identification tactics (multitaper, line synchronization, crest-factor control).
- Explicit uncertainty propagation into robust control and early-warning statistics.
- Cross-model validation criteria and decision-relevant performance metrics.

Weaknesses
- Empirical feasibility not yet evidenced: required amplitudes/durations/ensemble sizes to achieve target coherence for sensitive outputs (regional hydrology) remain speculative.
- LTI assumption under slow nonstationarity and seasonal modulation may limit identifiability; more explicit time-varying modeling strategies could be needed.
- Volterra identification for precipitation/circulation may suffer from data hunger; risk of overfitting even with sparsity unless strong detection slots and held-out tests are shown.
- Placeholder citations and minor LaTeX errors; duplication of concepts across sections; some MIMO actuation assumptions (orthogonal coded channels) may be operationally unrealistic in current ESM infrastructures.
- Early-warning claims need systematic benchmarks against passive EWS with controlled false-alarm rates.

Suggestions
- Provide a compact proof-of-concept with at least one intermediate model and one CESM-class ESM: show FRFs for GMST and a regional precipitation index, coherence vs. frequency, confidence bands, and Fisher information growth vs. amplitude/duration/ensemble size.
- Report concrete identifiability budgets: minimal RMS amplitude and record length to reach γ^2 ≥ 0.5 in 0.1–1 yr−1 bands for key outputs, across multiple models.
- Demonstrate early-warning gain: lead-time and AUC improvements over passive variance/autocorrelation using sliding-window experiments and a volcanic shock scenario.
- Clarify treatment of seasonality and slow drift: detrending/co-trending steps, window lengths, and biases; consider explicit time-varying/BLA formulations and seasonal linear parameter-varying surrogates.
- Detail SAOD/chemistry constraints with a specific emulator or linearized operator; show that proposed probes stay within safe envelopes.
- Streamline and de-duplicate sections; fix LaTeX issues (duplicate labels, unmatched braces) and replace placeholder citations with authoritative sources.
- Discuss operational realism: actuator slew limits, vertical/latitudinal injection constraints; evaluate multi-input identification feasibility under current model forcing interfaces.
- Release code/notebooks for spectral regression, input design, and uncertainty-to-weights mapping to aid reproducibility.

Questions
- What amplitudes and durations (and ensemble sizes) are required in CESM(WACCM) to achieve γ^2 ≥ 0.5 for regional precipitation indices over 0.2–1 yr−1? Can you tabulate these by output?
- How robust are FRF estimates to seasonal leakage and slow drift? Did you test seasonal-LPV or BLA approaches versus fixed LTI windows?
- How do microphysical and chemistry nonlinearities limit the “small-signal” regime? Where does HDI begin to rise meaningfully in SAOD/winds channels?
- Can PRBS-based designs meet SAOD and ozone constraints while achieving the desired coherence, given actuator slew limits?
- How sensitive are early-warning phase-drift statistics to ENSO phase and external volcanic events? What is the false-alarm rate control?
- For cross-model transfer, what thresholds on J_rel and multiplicative uncertainty ensure H-infinity small-gain conditions are met across models?

Rating (1-10)
8


## Review checkpoint

Summary
The manuscript proposes “active climate spectroscopy” for stratospheric aerosol injection (SAI): small, information-optimized perturbations (multi-sine/PRBS/chirp) superimposed on a baseline in Earth system models to identify frequency-dependent gains, lags, and weak nonlinearities. It integrates frequency-domain system identification (FRF/coherence with leakage control), sparse Volterra kernels for distortion, Fisher information–based input design, robust control synthesis (H∞, MPC) with uncertainty sets derived from spectra, early-warning indicators based on phase drift and harmonic distortion, cross-model validation, and spectral emulation for rapid iteration. The aim is control-ready surrogates, decision-relevant uncertainty, and minimally invasive experiments aligned with GeoMIP/ARISE-SAI protocols.

Soundness
- Methodological core is strong and grounded in established theory: frequency-domain identification under designed excitation, Fisher-information optimal input design, coherence-based SNR control, leakage-aware spectral regression, and standard robust control formulations are correctly invoked.
- The local LTI assumption plus low-order Volterra correction for small perturbations is reasonable but will be strained by seasonal nonstationarity, evolving baselines, aerosol microphysics/chemistry nonlinearities, and potential time variation in stratosphere–troposphere coupling.
- Use of ensemble averaging, multi-tapering, DFT-line alignment, phase optimization, and held-out single-tone validation are appropriate for mitigating colored variability and leakage.
- Construction of multiplicative uncertainty weights from coherence/residuals and inclusion of harmonic-distortion channels in H∞ are plausible, though conservative certification (e.g., μ-analysis across structured uncertainties) will be important.
- Early-warning via phase drift and distortion growth is defensible in principle; statistical power and confounding by slow time variation merit careful evaluation with sliding-window uncertainty quantification.

Presentation
- Technically rich, comprehensive, and generally well-structured, but overly long and repetitive; several sections restate similar material.
- Two near-duplicate “SAI impacts and uncertainties” and “Information-theoretic design” sections; streamlining would help.
- Some notation drifts (u(t), u_t; H/G; multiple definitions of HDI). E1–E6 are referenced but not explicitly defined in this excerpt.
- Citations include placeholders (e.g., enhanced_*, “Comprehensive/Smart Discovery System”), which must be replaced by real references.
- Minor inconsistencies between scalar-input assumptions and later MIMO formulations should be harmonized early.

Contribution
- Introduces a unified, control-oriented, frequency-domain framework for SAI that is novel in this domain: information-optimal probing, FRF/Volterra identification, VOI-aware design, robust control with spectroscopy-derived uncertainty, and active early warning.
- Bridges identification and control with explicit uncertainty propagation; aligns experiment design with controller regret reduction.
- Proposes practical PRBS/multisine designs, cross-model transfer metrics, and spectral emulation targets.

Strengths
- Rigorous application of mature system ID and robust control tools to SAI.
- Clear linkage from Fisher information to probe design, identifiability, and VOI for control.
- Comprehensive treatment of leakage, coherence, and uncertainty quantification.
- Inclusion of nonlinear diagnostics (sparse Volterra, bicoherence) and their control implications.
- Concrete robust control formulations (mixed-sensitivity H∞, tube/stochastic MPC) with frequency-shaped weights tied to identified spectra.
- Cross-model validation protocol and metrics; emphasis on minimal invasiveness and governance-aligned constraints.

Weaknesses
- Practical feasibility and compute budgets for required ensemble lengths/amplitudes across ESMs are not quantified; identifiability may demand long runs.
- LTI-around-baseline assumption and linearized chemistry/SAOD constraints may understate nonstationarity and nonlinear microphysics/ozone feedbacks.
- Mismatch between early scalar-input framing and later multi-actuator MIMO setup; actuator geography and seasonality need earlier, explicit treatment.
- Early-warning power and false-alarm control under slow drifts and structural changes are asserted but not demonstrated.
- Duplicate content and placeholder citations reduce clarity and credibility.
- The mapping from identified uncertainty to robust control certificates is suggested but not fully specified for structured uncertainties (e.g., μ-analysis across outputs/regions).

Suggestions
- Provide a compact “methods pipeline” figure/table: probe design → data handling → FRF/Volterra estimation → uncertainty sets → control synthesis → validation → early warning.
- Replace all placeholder citations with peer-reviewed sources; prune redundancies and consolidate overlapping sections.
- Define E1–E6 explicitly once, and maintain consistent notation for variables and indices throughout.
- Quantify practicality: amplitude–duration–ensemble trade-offs with numeric examples, expected coherence targets, and HPC cost across model tiers; include a minimal viable experiment design.
- Elevate MIMO from the outset: specify actuator channels (lat/alt/time-of-year), orthogonal coding, and identifiability conditions; discuss seasonality handling (deseasonalization, cyclostationary models).
- Strengthen robustness analysis: present structured uncertainty sets and μ-analysis, and show how identification covariance/residuals map to WΔ/Wm with confidence.
- Demonstrate early-warning performance on synthetic benchmarks and one ESM case: lead time, AUC, false-alarm rate vs passive baselines.
- Clarify chemistry/SAOD constraints: justify linear proxies (H_SAOD, H_chem) or adopt emulator constraints validated against interactive chemistry.
- Add a simple end-to-end case study (e.g., intermediate model) showing controller design from spectroscopy, with regret and constraint metrics.

Questions
- How sensitive are identifiability and controller performance to seasonal cycle leakage and slow drift? How are cyclostationary effects handled beyond deseasonalization?
- What are realistic run lengths and ensemble sizes to achieve target coherence (e.g., γ^2 ≥ 0.6) at 0.1–0.3 yr−1, given internal variability?
- How many actuators (lat/alt bands) are needed for regional precipitation constraints, and can MIMO identifiability be achieved with practicable PRBS codes?
- How robust are SAOD/ozone constraints when using linearized proxies, especially under perturbation superposition and intermittent volcanic events?
- How are structured uncertainties across outputs/regions represented in robust synthesis and certified (μ margins)?
- What is the sensitivity of early-warning indices to window choice and to changes in baseline forcing trajectory?
- Can the spectral emulators reproduce cross-frequency nonlinearities without overfitting, and how is emulator uncertainty propagated into control?

Rating (1-10)
7


## Review checkpoint




## Review checkpoint

Summary
The manuscript proposes an ambitious, end-to-end framework for “active spectroscopy” of the climate response to stratospheric aerosol injection (SAI). It combines information-optimal excitation (multisine/PRBS/chirp), frequency-domain system identification (linear FRFs and second-order Volterra kernels), uncertainty quantification, robust control synthesis (H∞, MPC), and active early-warning indicators (phase drift, harmonic/intermodulation growth). It also outlines cross-model validation metrics and spectral emulation to speed controller design. The work is technically sophisticated and well-grounded in system identification/control theory, aiming to make SAI experimentation more data-efficient, safer, and decision-relevant.

Soundness
- Theory: The use of Fisher information, coherence, Welch variance, BLA, bispectra, and robust control with multiplicative uncertainty is standard and correctly adapted. MI-based VOI links are reasonable under Gaussian-linearized assumptions.
- Assumptions: Small-signal LTI around an operating point, WSS colored noise, and sliding-window quasi-stationarity are plausible for modest perturbations, but seasonal LTP/time-variation is a material caveat. Linearized SAOD/chemistry constraints are strong simplifications.
- Claims: Statements about improved lead time over passive EWS and controller dominance are plausible but require empirical evidence; currently they read as promises contingent on forthcoming benchmarks.
- Scope limits: The lower frequency bound (0.02 cycles/yr ≈ 50-year period) is inconsistent with stated 10–20 year experiments unless very large ensembles are used; identifiability there is doubtful.

Presentation
- Clarity: Technically clear and thorough, but very dense and repetitive. Several sections restate similar ideas; cross-references (E1–E6) help but could be streamlined.
- LaTeX hygiene: The excerpt begins mid-equation; equation labels (e.g., multiple eq:fim) would collide; some symbols change between sections (u(t) vs u_t; G/H notation); ensure consistent notation and unique labels.
- Citations: Numerous placeholder or non-standard citations (“enhanced_…”, “Comprehensive Discovery System”, “Smart Discovery System”) undermine credibility and traceability; these must be replaced with citable sources.

Contribution
- Unifies information-optimal probe design, leakage-aware frequency-domain identification, sparse Volterra spectroscopy, and robust control for SAI.
- Introduces active EWS based on phase drift and harmonic/intermodulation growth at probe-synchronous lines.
- Proposes frequency-shaped uncertainty from coherence/HDI for robust synthesis; cross-model generalization metrics; and spectral-training losses for emulators tied to FRFs/NFRFs.
- Provides an identifiability budgeting framework (amplitude–duration–ensemble trade-offs).

Strengths
- Methodologically rigorous; draws on mature identification/control literature.
- Clear operationalization: crest-factor constraints, leakage control, MIMO PRBS coding, and governance-aware constraints (SAOD/ozone, regional precipitation).
- UQ and robustness are first-class: Fisher-to-posterior propagation, multiplicative uncertainty weights, tube/chance-constrained MPC.
- Cross-model validation and emulation paths increase practical relevance and scalability.

Weaknesses
- Practical feasibility: The targeted low-frequency bands (down to 0.02 yr−1) are not identifiable in 10–20 years without very large ensembles; resource implications are not quantified.
- Time variation/seasonality: LTI approximations with deseasonalization may be insufficient; LTP/time-varying FRFs are not treated.
- Chemistry/SAOD constraints: Linear operator proxies (H_SAOD, H_chem) risk inaccuracy; no demonstration of safe bounds calibration.
- Heuristic uncertainty mapping: Converting coherence/HDI to multiplicative uncertainty weights is sensible but unvalidated; choice of safety factors not justified.
- Referencing/polish: Placeholder citations and repeated equation labels; some redundancy across sections.
- Evidence gap: No quantitative results shown (lead-time/AUC, closed-loop regret/margins, cross-model scores) to support performance claims.

Suggestions
- Narrow frequency bands to those identifiable under realistic budgets (e.g., 0.1–2 yr−1). Provide amplitude–duration–ensemble budget tables with expected FRF CI widths and coherence.
- Treat seasonality/time variation explicitly (e.g., linear time-periodic models, time-varying FRFs, or seasonal scheduling of probes).
- Replace linear SAOD/chemistry proxies with emulators or enforce constraints via scenario sets; validate constraint surrogates against chemistry-resolving ESM runs.
- Validate the coherence-to-uncertainty mapping: compare WΔ inferred from coherence/HDI to cross-validation error across ensembles/models; tune α,β systematically.
- Consolidate and de-duplicate sections; enforce unique labels and consistent notation. Replace placeholder citations with peer-reviewed sources or anonymized technical reports clearly marked.
- Provide at least one end-to-end demonstration (toy model and an ESM subset): (i) probe design, (ii) FRF/NFRF recovery with CIs, (iii) H∞/MPC synthesis with robustness certificates, (iv) EWS lead-time vs passive, (v) cross-model transfer metrics and controller regret.
- Consider LTP-aware probe/estimation (season-locked multisines, Floquet/BLA variants) and discuss leakage under slow drift.
- Detail MIMO actuation (latitudinal/seasonal channels) beyond a single-input focus and report condition numbers/identifiability.

Questions
- What experiment lengths and ensemble sizes are assumed per model tier to achieve target coherence and phase CI in each band? Please provide concrete budgets and sensitivity to S_v(ω) misestimation.
- How are H_SAOD and H_chem constructed and validated? What are acceptable thresholds δ_SAOD/δ_chem, and how sensitive are designs to these bounds?
- How are α, β chosen in WΔ from coherence/HDI, and how does this correlate with true multiplicative error across ensembles/models?
- Can the framework accommodate LTP dynamics explicitly (seasonal LTP BLA) and does this change input design?
- How do you avoid spectral collisions with strong exogenous periodicities (annual/semianual harmonics, QBO) in practice?
- For MI-based adaptive reweighting across campaigns, how robust is convergence when prior Jacobians J_k are biased?
- What is the computational cost to fit sparse Volterra kernels and perform μ-analysis across multi-output channels at monthly resolution?

Rating (1-10)
7/10. Strong, well-motivated methodology with clear potential impact, but needs polishing (citations/notation), realistic identifiability budgets, explicit handling of time variation/chemistry, and empirical validation of performance claims and uncertainty mappings.


## Review checkpoint

Summary
The manuscript proposes an “active spectroscopy” framework for stratospheric aerosol injection (SAI) research: design small, information-optimal multisine/PRBS perturbations on ESM baselines to estimate frequency responses and weak nonlinearities; use these to synthesize robust H-infinity/MPC controllers with explicit uncertainty weights; and deploy active early-warning indicators based on phase drift and harmonic/intermodulation growth. It further specifies Fisher-information–based probe design, spectral regression/Volterra identification, cross-model validation metrics, and uncertainty quantification, all aligned with GeoMIP/ARISE-SAI protocols.

Soundness
- Technically grounded in mature system identification (frequency-domain FRF estimation, Fisher information, leakage control), robust control (mixed-sensitivity H∞, tube/scenario MPC), and nonlinear identification (second-order Volterra/GFRFs). 
- Assumptions are clearly stated: small-signal, local LTI with weak quadratic nonlinearities, quasi-stationarity over windows, ensemble averaging to mitigate internal variability.
- Early-warning logic (phase-margin erosion and distortion growth) is well-motivated by control theory.
- Risks: validity under strong nonstationarity, structural model drift as baselines escalate, and the adequacy of small-amplitude perturbations relative to red internal variability in key bands.

Presentation
- Comprehensive and methodically detailed; however, overly long and occasionally repetitive (several sections recapitulate the same ideas).
- Multiple duplicated equation labels (e.g., eq:frf, eq:hdi) and cross-references (e.g., eq:msHinf referenced but not defined in the excerpt) will break LaTeX; ensure all labels are unique and defined.
- Inconsistent notation across sections (s vs z vs q−1, s/jω vs discrete ω; units not always restated).
- A number of citations appear as placeholders (enhanced_*, comprehensive_*, “Comprehensive/Smart Discovery System”); replace with archival references or remove.
- A high-level roadmap figure connecting E1–E6, data flows, and controller synthesis would improve readability.

Contribution
- A unified pipeline: information-optimal excitation → leakage-aware spectral identification (linear + quadratic) → uncertainty-calibrated robust control → active early-warning and adaptive safeguards → cross-model validation and robust envelopes.
- Novel integration for SAI: frequency-shaped uncertainty from coherence/HDI; early-warning indices tied to controller margins; robust, multi-model input design and transfer metrics.

Strengths
- Strong theoretical foundation and careful attention to identifiability, leakage, and UQ.
- Clear mapping from spectral evidence to controller weights and uncertainty sets.
- Governance-aware constraints (SAOD/ozone, rate limits) embedded in both design and control.
- Cross-model validation protocol with quantitative discrepancy/transfer metrics.

Weaknesses
- Empirical validation is not shown here; claims of tractability/skill remain prospective.
- Small-signal LTI assumption may be strained under evolving baselines, seasonal modulation, and chemistry–dynamics feedbacks; risk of time-variation biasing FRFs.
- SNR feasibility at low frequencies (interannual/decadal) may require long runs/large ensembles; practicality bounds need quantification for typical HPC budgets.
- Single-input framing (zonal-mean injection) underplays spatial actuation complexities and aerosol microphysics path-dependence.
- Repetition, placeholder citations, and label conflicts hinder clarity.

Suggestions
- Provide a compact synthetic and one ESM case study: show FRF/HDI estimates, coherence, uncertainty tubes, controller design, robustness margins, and early-warning lead-time vs passive EWS.
- Quantify amplitude–duration–ensemble trade-offs (E6) with concrete numbers for representative models and budgets; include minimum viable probe designs.
- Stress-tests: nonstationary baselines, seasonal leakage, ENSO/volcanic shocks, and slow parameter drift; show adaptive retuning procedures triggered by the EWI.
- Expand MIMO actuation (latitude/seasonal targeting), and compare PRBS vs multisine in practice.
- Consolidate duplicated sections; unify notation; fix labels; replace placeholder references with peer-reviewed sources.
- Discuss ethical/practical constraints of active probing even in silico, and pathways to observational analogs.

Questions
- What minimum RMS amplitudes, record lengths, and ensemble sizes achieve target coherence (e.g., γ2≥0.6) at 0.1–0.5 yr−1 in CESM/WACCM?
- How robust are phase-drift EWIs to slow nonstationarity and seasonal cycle residuals; what windowing/tapering choices optimize bias–variance?
- How is SAOD used as an actuation normalization across models with different microphysics, and does this affect MIMO identifiability?
- Can the proposed WΔ mapping from coherence/HDI be calibrated to deliver reliable small-gain margins across models?
- How does the framework extend when significant time-variation (gain scheduling) is detected?

Rating (1-10)
7


## Review checkpoint

Summary
The manuscript proposes an “active spectroscopy” framework for stratospheric aerosol injection (SAI) in Earth system models: design small-amplitude, information-optimal multi-sine/PRBS probes; estimate linear frequency responses and second-order Volterra kernels via leakage-aware spectral regression; propagate uncertainty via Fisher information and bootstrapping; synthesize robust H-infinity/MPC controllers; deploy phase-drift and harmonic-distortion early warnings; and validate transferability across models with frequency-domain metrics and controller regret.

Soundness
- Core methodology leverages well-established system identification and robust control theory (FIM-based OED, BLA/FRF estimation, coherence-weighted variance, H-infinity small-gain checks, PRBS design). Conceptually sound and technically consistent.
- Nonlinear identification via sparse second-order Volterra kernels and cross-bispectra is appropriate but data-hungry; feasibility in ESMs hinges on long records/ensembles.
- Some elements are heuristic and need justification: mapping coherence to multiplicative uncertainty bounds WΔ; using HDI growth as a proxy for instability risk; claims about solving E-opt via sequences of convex A-opt problems; and assuming quasi-LTI behavior despite strong seasonality/nonstationarity.

Presentation
- Scientifically rich but overly long and repetitive; at least one “Cross-model validation” section appears twice; several equations/labels (e.g., frf, hdi) are reused and would clash in LaTeX.
- Notation varies across sections (G/H/J/Svv/See), which can confuse readers; equation scaling factors differ between sections.
- Multiple citations appear to be placeholders (e.g., enhanced_*, Comprehensive/Smart/Comprehensive Discovery System). These must be replaced with real references or removed.
- Overall readability would benefit from consolidation, a consistent symbol table, and moving technical derivations to appendices.

Contribution
- Integrates information-optimal probe design, frequency-domain identification (linear and quadratic), uncertainty quantification, robust control, and early warning into a coherent workflow for SAI.
- Introduces cross-model generalization metrics (Jgen, Jrel, JV2, HDI consistency) and controller transfer/regret evaluation under multiplicative mismatch checks.
- Operationalizes amplitude–duration–ensemble trade-offs using FI scaling; proposes MIMO PRBS/orthogonal coding for geographically distinct actuators.

Strengths
- Strong, theory-grounded framework aligned with mature engineering practice.
- Detailed, actionable guidance on leakage control, crest-factor management, and coherence targeting.
- Robust control and cross-model transfer are treated explicitly with meaningful metrics and checks.
- Clear linkages from probe design to UQ, controller synthesis, and early-warning diagnostics.

Weaknesses
- No empirical demonstration; feasibility in full ESMs remains unproven (required N, ensemble size, coherence levels).
- Duplicate sections and inconsistent notation/labels; placeholder references undermine credibility.
- WΔ construction from coherence/HDI is heuristic; lacks a rigorous bound or empirical calibration.
- Practical SAI constraints (SAOD/ozone caps, microphysical adjustment, actuator geography) are invoked but not parameterized with concrete numbers.
- Volterra estimation and cross-bispectra in red-noise, slowly drifting systems may be fragile without strong regularization and long data.

Suggestions
- Replace all placeholder citations with real, verifiable references; prune redundant citations.
- Consolidate and de-duplicate sections; unify notation; provide a symbol table; ensure unique labels.
- Add a minimal working example (e.g., EBM or intermediate model) showing FRFs, coherence, OED vs. baseline, Volterra fits, and early-warning performance; then a small-scale ESM pilot.
- Calibrate WΔ empirically from spectral confidence intervals or Bayesian posteriors rather than heuristics; report coverage of the resulting uncertainty envelopes.
- Specify concrete environmental/operational constraints (numerical SAOD/ozone bounds, rate limits) and show they are respected by designed probes.
- Quantify practicality: required T, RMS amplitude, and ensemble size to reach γ^2≥0.6 at key frequencies; provide power budget tables.
- Detail robust OED algorithm (inputs, convexity conditions, solver, complexity) and provide pseudo-code.
- Address nonstationarity/seasonality explicitly (seasonal LTV models or seasonal normalization) and validate sliding-window FRFs.
- Provide guidelines for actuator geography and MIMO coding in ESM APIs; include mapping from injection to SAOD across models.
- Define early-warning thresholds and false-alarm control; compare PDI/HDI lead times against passive baselines with ROC/AUC.

Questions
- What experiment length and ensemble size are needed to achieve target coherence (e.g., γ^2≥0.6) at 0.1–1 yr−1 under CESM-like variability using 0.1 TgS/yr RMS probes?
- How are SAOD/ozone constraints quantitatively imposed in design (metrics, thresholds), and what amplitudes are demonstrably safe in WACCM-class chemistry?
- How is WΔ derived from FRF confidence intervals, and does it produce valid robust-stability certificates (empirical coverage)?
- How do you handle strong seasonality/QBO in practice: seasonal detrending only, or seasonal-LTV identification?
- What actuator configurations (latitude/altitude/season) are assumed for MIMO identification, and how are cross-channel coherences controlled?
- How sensitive are Volterra estimates to slow drift and red noise? What regularization and validation are used to prevent spurious intermodulation in ESMs?
- Can you provide computational cost estimates (CPU-years) for E1–E6 across two model tiers?
- Is the robust E-opt design provably convex under your assumptions, or is it a heuristic A-opt approximation? Please clarify.

Rating (1-10)
7


## Review checkpoint




## Review checkpoint

Summary
The manuscript proposes an “active spectroscopy” framework for probing and controlling the climate response to stratospheric aerosol injection (SAI). It designs small-amplitude, information-optimized multisine/PRBS/chirp inputs to estimate MIMO frequency responses via spectral regression (with leakage control), extends to weak nonlinearities via second-order Volterra kernels, and uses the identified dynamics for multi-objective robust control (H∞ and MPC) under quantified frequency-dependent uncertainty. It further introduces early-warning indicators based on phase-lag drift and harmonic distortion, and frames probe design through Fisher information and decision-aware value-of-information. Cross-model validation, uncertainty quantification, and practicality bounds (amplitude–duration–ensemble trade-offs) are discussed with links to GeoMIP/ARISE protocols.

Soundness
- Core methodology—frequency-domain identification with designed excitation, coherence-weighted regression, and Welch/multitaper leakage control—is technically sound and well-grounded in system identification literature (Ljung; Pintelon & Schoukens).
- PRBS/multisine orthogonalization for multi-input excitation and frequency-wise least squares for MIMO FRFs are appropriate; H1/Hv estimator choices are reasonable when input noise is negligible/handled.
- Mapping identification covariance and coherence into multiplicative uncertainty weights for H∞ synthesis is defensible; MPC formulation with frequency-shaped costs and constraints is standard.
- Second-order Volterra modeling for weak nonlinearity is plausible but can be ill-conditioned and data-hungry in colored, low-SNR climates; sparsity and careful experiment design are essential.
- Key assumptions (quasi-LTI over windows, stationarity of internal variability, small-signal regime) are explicit but should be stress-tested; seasonal/slow drift and structural model error may limit validity.

Presentation
- The text is comprehensive but overly long and repetitive; several sections restate similar ideas with different emphases.
- There are typographical/grammatical issues (e.g., initial “e each input channel…”), inconsistent notation (A vs A_i; m, N; T_b), and some dimensionally unclear statements (e.g., “TV ≈ 2A transitions per month”).
- Citation quality needs attention: placeholder-like entries (enhanced_*, comprehensive_*), duplicate citations in a single bracket, and repeated self-citations reduce credibility; ensure all references are real and consistently formatted.
- Acronyms and symbols (SAOD, HDI, DPSS, EMIC) should be defined once and used consistently; align units (TgS yr^-1) throughout.

Contribution
- Integrates designed spectral probing, frequency-domain identification, and robust control for SAI in a single, decision-aware workflow.
- Operationalizes early-warning via phase drift and harmonic distortion, linked to the same active probes used for identification.
- Frames probe design via Fisher information and control value-of-information, connecting experiment design to governance-relevant objectives.
- Provides practical guidance (frequency bands, amplitudes, ensembles) and cross-model validation concepts.

Strengths
- Strong theoretical grounding in frequency-domain system ID and robust control.
- Clear connection between identification uncertainty and controller robustness via frequency-dependent weights.
- Thoughtful probe design (multisine/PRBS, Gold/Hadamard coding, leakage control) and practicality considerations.
- Incorporation of weak nonlinearity (Volterra) with actionable diagnostics (HDI).
- Decision-aware, multi-objective control framing (GMST vs hydrology vs SAOD) and early-warning integration.
- Emphasis on cross-model transfer and uncertainty propagation.

Weaknesses
- Empirical validation is not shown here; claims about performance, early-warning lead time, and practicality remain hypothetical.
- Quasi-LTI assumption may be strained by seasonality, slow drift, and regime-dependent feedbacks; limited discussion of LTV/LTP alternatives.
- Second-order Volterra identification in colored, low-SNR settings may be fragile; identifiability and variance control need tighter guarantees.
- The “TV ≈ 2A transitions per month” statement is dimensionally unclear; actuator feasibility claims need quantitative support.
- Minimum-phase priors and sign constraints could be questionable for some climate channels; justification is thin.
- Multi-input orthogonality under nonstationary, coupled dynamics (e.g., annual cycle, QBO) needs more rigorous treatment.
- Reliance on placeholder citations (enhanced_*, comprehensive_*, repeated “Smart/Comprehensive Discovery System”) undermines credibility.
- Some practical constraints (input measurement error via SAOD realization vs commanded injection, chemistry/ozone side effects) are acknowledged but not integrated into identification as errors-in-variables.

Suggestions
- Provide a compact empirical demonstration: (i) pilot ESM runs with designed probes, (ii) FRF/HDI estimates with coherence/CIs, (iii) held-out single-tone validation, and (iv) a small H∞/MPC case study with uncertainty margins.
- Address seasonality and slow drift explicitly: deseasonalize, use sliding-window LTV FRFs, or incorporate seasonal bases/LPV models; report stability of estimates vs window length.
- Tighten the Volterra approach: specify feature selection, identifiability conditions (odd/even scheduling), SNR requirements, and cross-validation against held-out intermodulation lines.
- Clarify and correct dimensionalities (e.g., total variation vs amplitude), unify notation, and fix typos.
- Replace placeholder/duplicate citations with peer-reviewed sources; reduce self-citation density and consolidate repeated arguments.
- Justify amplitude and ensemble choices with coherence/SNR targets per output band; include amplitude–duration–ensemble contour plots from FI scaling.
- Discuss input realization uncertainty (commanded injection vs realized SAOD) and consider an errors-in-variables or IV estimator.
- Revisit priors (minimum phase, sign constraints) with physical arguments and sensitivity tests.
- Detail multi-input design under annual/QBO interference: frequency masks, DPSS tapers, integer-period selection, and leakage diagnostics.
- Provide reproducibility assets: probe generation code, spectral regression settings, weighting filters for H∞/MPC.

Questions
- What coherence thresholds and experiment lengths are required (per band/output) to achieve target confidence in Bode magnitude/phase?
- How are annual cycle and QBO handled (deseasonalization, frequency masks, integer-period design) to avoid bias/leakage?
- How robust is the Volterra identification under colored noise; what fraction of nonlinear distortion energy is captured in practice?
- How is input uncertainty treated when realized SAOD deviates from commanded injection (actuator/chemistry variability)?
- What are the computational costs (years×ensemble size) for E1–E4 in CESM/WACCM-class models?
- How are precipitation indices and regional outputs selected/weighted, and how do weights map to policy objectives?
- How is WΔ(ω) calibrated from coherence/HDI/covariance, and how conservative are the resulting robust-stability margins?
- What cross-model normalization (e.g., SAOD-based) is used to ensure comparability, and how transferable are controllers across models?

Rating (1-10)
7


## Review checkpoint

Summary
The manuscript proposes treating stratospheric aerosol injection (SAI) as an “active spectroscopy” experiment: small, information-optimized multisine/PRBS/chirp perturbations are superimposed on baseline SAI in Earth system models (ESMs) to estimate frequency responses and low-order nonlinearities (Volterra kernels). These identified surrogates then inform robust H-infinity and MPC controllers under frequency-shaped uncertainty, and yield early-warning indicators (phase drift toward −π and harmonic distortion growth). The workflow includes cross-model robustness, Fisher-information–based probe design, and evaluation metrics (tracking, hydrological constraints, SAOD, effort, regret).

Soundness
- Technical basis: Solid and well-grounded in frequency-domain system identification, optimal input design, and robust control. The use of coherence, Fisher information, and leakage controls is appropriate; Volterra methods for weak nonlinearity are standard.
- Modeling assumptions: The quasi-LTI assumption around a drifting baseline and weak nonlinearity are plausible for small probes but fragile in a seasonally forced, slowly evolving climate system. The plan partially mitigates this via sliding windows and ensembles.
- Robust control: Mixed-sensitivity H∞/MPC formulations are standard. However, the mapping from coherence/HDI to multiplicative uncertainty WΔ is heuristic and needs validation for robust guarantees.
- Early warning: Phase-drift and HDI as active, pathway-specific indicators are conceptually sound but require power analyses and null distributions under nonstationarity to establish reliability.
- Cross-model robustness: Sensible (envelopes, worst-case design), though the single-actuator assumption in parts of the text may understate controllability limits for regional hydrology.

Presentation
- Generally clear, comprehensive, and technically rigorous; strong linkage across identification–control–governance.
- Repetition across sections could be reduced; notation sometimes mixes continuous/discrete time and reuses equation labels.
- Several placeholder-looking citations (e.g., “enhanced_…”, “comprehensive_…”) appear nonstandard; these should be replaced with archival sources or removed.
- Minor inconsistencies (SISO vs MIMO treatment of u and y; units and timebase) should be harmonized.

Contribution
- Reframes SAI pulsing as information-optimal spectroscopy tailored to control design—novel in this domain.
- Introduces actionable, frequency-aware early-warning indicators.
- Provides a principled bridge from ESM experiments to robust control with explicit, frequency-shaped uncertainty.
- Offers a cross-model, decision-relevant evaluation framework (Pareto fronts, regret, constraint risk).

Strengths
- Strong theoretical grounding and end-to-end workflow from probe design to control and monitoring.
- Clear, quantitative connection between information content and controller robustness (VoI perspective).
- Practical safeguards: amplitude bounds, SAOD constraints, leakage mitigation, ensemble use.
- Cross-model robustness is explicitly considered.
- Rich, testable metrics and validation protocols.

Weaknesses
- Heuristic construction of WΔ from coherence/HDI may not ensure conservative robustness margins without empirical calibration.
- LTI/weak-nonlinearity assumptions may be violated under seasonal cycles, QBO, and drifting baselines; limited discussion of time-varying/periodic (LTP) models.
- Computational feasibility risks: required durations/ensembles to reach target coherence at 0.02–0.1 yr−1 may be large for CESM/WACCM-class runs.
- Volterra identification can be high-dimensional; sparsity priors help but practical identifiability with colored noise needs power analysis.
- Control objectives for regional precipitation with (mostly) single actuator u may be underdetermined; multi-actuator (latitudinal/seasonal) strategies are only lightly treated.
- Nonstandard placeholder citations undermine credibility.

Suggestions
- Replace all “enhanced_…/comprehensive_…” references with archival literature or clearly mark as in-prep/preprint with links.
- Derive WΔ from statistically validated bounds: use bootstrap/posterior FRF bands and held-out spectra; verify robust stability via μ-analysis or structured singular value tests.
- Explicitly address time-variation: adopt periodic/LTP identification (seasonal lifting), or time-varying FRF tracking with regularization; report sensitivity to window length.
- Provide power analyses (E6): amplitude–duration–ensemble budgets needed to achieve coherence ≥0.6 across monthly–interannual bands per output; include resource estimates.
- Expand multi-input actuation (latitude/season/altitude channels) and analyze controllability/observability trade-offs for regional hydrology.
- Clarify SAI-to-SAOD mapping and chemistry constraints across models; consider normalizing actuation by SAOD in identification/control loops.
- Add ablation studies: PRBS vs multisine vs chirp; leakage correction variants; Volterra sparsity patterns; early-warning thresholds.
- Consolidate notation (t vs k, discrete vs continuous), remove duplicate labels, and provide a concise algorithmic summary (pseudocode) for E1–E6.

Questions
- What experiment lengths and ensemble sizes are required to resolve the lowest frequencies (≈0.02 yr−1) with sufficient coherence under CESM-like internal variability?
- How sensitive are FRF/HDI estimates to seasonal aliasing and slow drift? Did you test periodic/LTP models or seasonal prewhitening?
- How is WΔ calibrated and validated to ensure robust-performance margins hold in held-out runs and under volcanic shocks?
- Can the framework support multiple actuators (e.g., hemispheric/seasonal injection) and demonstrate improved regional precipitation control?
- What are the practical SAOD/ozone constraints used in probe optimization, and how do they vary across models?
- How stable are early-warning indicators (phase drift, HDI) under different probe spectra and window choices?

Rating (1-10)
7


## Review checkpoint

Summary
The manuscript proposes an “active spectroscopy” framework for stratospheric aerosol injection (SAI): small-amplitude, information-optimized multi-sine/PRBS/chirp perturbations are superimposed on a steady baseline to estimate linear frequency responses and low-order nonlinear distortions (second-order Volterra) between SAI inputs and climate outputs. These identification results feed robust control synthesis (H-infinity and MPC), active early-warning indicators (phase drift, harmonic distortion), Fisher-information-based experiment design, uncertainty quantification, cross-model validation, and control-oriented emulation. The work aims to convert pulsing from an ad hoc strategy into a principled, frequency-aware experimental and control paradigm.

Soundness
- Conceptual grounding: Strong. The approach aligns with established frequency-domain system identification (Ljung; Pintelon & Schoukens) and robust control theory. Mapping coherence/HDI to uncertainty weights is a reasonable heuristic for multiplicative uncertainty.
- Assumptions: Clearly acknowledges small-signal, quasi-stationary windows, colored internal variability, and weak nonlinearity—appropriate but limiting in ESMs. Volterra-2 is defensible for diagnostics, but climate nonstationarity and multi-scale feedbacks remain challenging.
- Methodological correctness: Equations for BLA, FRF estimation, coherence, HDI, H∞ robust-stability margin, FIM-based input design are standard and correctly used. PRBS design and leakage control are well motivated. Early-warning via phase drift and bispectral/Volterra diagnostics is technically sound.
- Risks: Practical SNR at amplitudes 0.05–0.5 TgS/yr may be marginal for some outputs without large ensembles. The frequency band 0.02–2 yr^-1 includes multi-decadal scales (0.02 yr^-1 ~ 50 years) incompatible with proposed 5–10-year windows unless strong parametric priors are used. Time-variation (drifts) could violate stationarity assumptions for spectral estimators.

Presentation
- Clarity: Generally clear, rigorous, and well structured with equations and diagnostics.
- Redundancy: Multiple near-duplicate sections (e.g., two robust-control sections; two Fisher-information sections; two nonlinear/Volterra sections) could be consolidated.
- Notation: Occasional mixing of continuous-time (s/jω) and discrete-time (z) without explicit mapping; some symbols reused across sections with slightly different meanings.
- References: Many core citations are appropriate; however, several “enhanced_*_20250812” and “comprehensive_*_20250812” entries appear placeholder/self-references and must be replaced or substantiated.

Contribution
- Novelty: Brings frequency-domain system identification, Volterra-based nonlinear spectroscopy, and robust control/early-warning into the SAI modeling context in a tightly integrated workflow.
- Significance: If implemented, could materially improve data efficiency, controller robustness, and the interpretability of warnings compared to passive approaches or step/ramp protocols. Cross-model frequency-domain validation is a valuable addition.

Strengths
- Strong theoretical foundation with end-to-end pipeline from probe design to control and monitoring.
- Careful treatment of leakage, coherence, identifiability, and Fisher-information trade-offs.
- Explicit incorporation of uncertainty into controller synthesis and early warning.
- Practical design advice for PRBS/multisine construction and ensemble usage.
- Cross-model validation metrics (D_lin, D_nl) and envelope-based robust synthesis.
- Ethical/risk awareness via small-signal design, SAOD bounds, and constraint-aware MPC.

Weaknesses
- Redundancy and length hamper readability; overlapping sections dilute the core contributions.
- Placeholder/self-references (“enhanced_*”, “comprehensive_*”) undermine credibility.
- Feasibility gaps: unclear ensemble sizes/durations needed to reach target coherence at low amplitudes; limited quantitative guidance.
- Frequency band inconsistency: 0.02 yr^-1 requires windows far longer than 5–10 years to resolve nonparametrically.
- MIMO realism: much is phrased for scalar u; practical SAI actuation is multi-input (latitude/altitude/season), and outputs are strongly coupled; controller and ID implications need fuller treatment.
- Nonstationarity: escalating baselines and regime shifts challenge the stationarity assumptions underpinning spectral regression and Volterra kernels; time-varying ID needs more emphasis.

Suggestions
- Consolidate duplicates: merge the two robust-control sections; merge the Fisher-information sections; streamline Volterra content once with clear cross-references.
- Replace or justify placeholder citations; ensure all references are real, accessible, and properly formatted.
- Tighten notation: explicitly connect s-domain, z-domain, and monthly sampling; define symbols once and maintain consistency.
- Calibrate practicality: add quantitative amplitude–duration–ensemble tables/figures (even from pilot ESM runs) to show achievable coherence and variance reduction; specify minimal designs for key outputs.
- Re-scope bands: either lengthen windows or restrict the lower band edge (e.g., ≥0.1 yr^-1) for nonparametric FRF estimates; use parametric fits for multi-decadal structure and validate their robustness.
- Expand MIMO treatment: include multi-actuator designs (latitude/altitude channels), MIMO FRF estimation, and MIMO H∞ synthesis implications.
- Address time-variation: add explicit time-varying FRF/TVAR or linear parameter-varying (LPV) identification options and guardrails for nonstationarity.
- Provide a small, reproducible prototype: a minimal demonstration on an idealized model to anchor the methodology with concrete numbers and plots.

Questions
- What ensemble size and experiment duration are required to achieve target coherence (e.g., γ^2 ≥ 0.6) for GMST vs regional precipitation at amplitudes 0.05–0.5 TgS/yr?
- How will you handle multi-input actuation (hemispheric, latitude bands, altitude) in identification and control design; what is the intended MIMO structure?
- How sensitive are the FRF estimates and controllers to slow nonstationarity (e.g., under ramping GHG forcing) over a decade? Will you adopt LPV or adaptive identification?
- How is WΔ(ω) tuned from coherence and HDI in practice (α, β selection), and how conservative is the resulting multiplicative uncertainty?
- Can you provide numeric examples of the phase-drift and HDI early-warning lead times versus passive EWS under a controlled baseline-escalation experiment?
- How will leakage be managed in the presence of strong annual cycle and QBO signals beyond “integer-period” sampling?
- What is the governance-relevant interpretation of “alarm thresholds” for μ_rs and HDI, and how would these translate into operational decision rules?

Rating (1-10)
7


## Review checkpoint

Summary
This manuscript proposes “active spectroscopy” for stratospheric aerosol injection (SAI): small, information-optimal multi-sine/PRBS/chirp perturbations superimposed on a steady baseline to identify frequency responses and weak nonlinearities, design robust controllers (H-infinity and MPC), and compute active early-warning indicators (phase drift and harmonic distortion). It details Fisher-information-based probe design, spectral regression with leakage control, sparse Volterra estimation, uncertainty quantification, cross-model validation/transfer, and a performance evaluation protocol under ENSO-like variability and volcanic shocks.

Soundness
The core methods are well-grounded in frequency-domain system identification and robust control. The FRF/H1 estimator, coherence, FIM scaling, small-gain robust stability, tube/chance-constrained MPC, and mixed-sensitivity H∞ are correctly invoked. Assumptions (local linearity, stationarity within windows, Gaussian approximations) are standard but nontrivial in ESMs. Some links remain conceptual: explicit constructions of WΔ from coherence/HDI (eq: wdelta cited but undefined here), empirical validation of early-warning lead-time gains, and quantitative robustness margins across models are promised but not shown in this excerpt.

Presentation
Technically rich but overly long and partially repetitive (two “Cross-model validation” subsections; multiple Fisher-information sections). Notation is heavy and sometimes inconsistent (Qy vs W· weights; RΔ vs WU; WT, Wu in H∞ vs MPC weights). Minor issues: “inite-horizon” typo; references to equations not present in this excerpt (eq:wdelta), and forward references to eq:rs before definition. Many placeholder/self-citations (enhanced_*, comprehensive_*), which hinder verifiability.

Contribution
- Reframes SAI pulsing as optimal experiment design for control-relevant identifiability.
- Integrates FRF/Volterra identification, information-optimal probing, robust H∞/MPC synthesis, and active early warning within a single workflow.
- Proposes cross-model frequency-domain transfer metrics and uncertainty envelopes, connecting ensemble spread to control design.

Strengths
- Strong theoretical foundation in frequency-domain ID and robust control.
- Clear value-of-information framing (FIM, D-/A-optimality) tied to control regret.
- Practical design choices (crest-factor control, leakage mitigation, coherence thresholds, PRBS design).
- Direct mapping from spectral uncertainty to H∞ weights and MPC chance/tube constraints.
- Governance-aware constraints (SAOD bounds, hydrology limits) and stress-testing scenarios.

Weaknesses
- Redundant sections and heavy notation impede readability.
- Placeholder citations (enhanced_/comprehensive_) and undefined references reduce credibility.
- Empirical feasibility in full ESMs is asserted but not demonstrated (required amplitudes/ensembles to achieve target coherence, computational budgets).
- Early-warning claims (phase-drift/HDI lead time) lack quantitative results and baseline comparisons here.
- Transfer to heterogeneous SAI actuation patterns (spatial distribution, SAOD mapping) is under-specified.

Suggestions
- Consolidate duplicate sections; unify notation across H∞ and MPC (use a single weight vocabulary).
- Replace placeholder citations with archival references or preprints; ensure all cited equations appear.
- Provide a compact end-to-end demonstrator (SISO GMST channel) with real ESM or emulator results: coherence vs amplitude/length, FRF CIs, H∞ margins, MPC constraint satisfaction, and EWI lead-time vs passive baselines.
- Quantify minimal amplitude-duration-ensemble requirements for key bands using measured Svv(ω); include a feasibility table for typical ESM costs.
- Specify construction of WΔ from coherence/HDI and show how μrs triggers controller gain reduction (thresholds, hysteresis).
- Clarify actuation-to-SAOD mapping and normalization across models; report sensitivity to injection patterns.
- Release code/probes and spectral-regression settings (tapers, window lengths, leakage corrections) for reproducibility.

Questions
- What amplitudes and ensemble sizes are needed to reach γ2 ≥ 0.6 in seasonal–interannual bands in CESM/WACCM? Are 0.05–0.5 TgS yr−1 RMS probes sufficient under typical Svv?
- How is WΔ constructed quantitatively from coherence/HDI, and how robust is μrs to estimator variance?
- How sensitive are identified FRFs/Volterra kernels to spatial actuation patterns and SAOD-injection mapping differences across models?
- How is nonstationarity from evolving baselines handled in MPC predictors (time-varying A,B,C or windowed refits), and how often is retuning required?
- What are the computational budgets (years × members) per E1–E6 stage, and how do they scale with desired CI widths?

Rating (1-10)
7/10


## Review checkpoint

Summary
The manuscript proposes “active spectroscopy” for stratospheric aerosol injection (SAI): small, information-optimal multisine/PRBS/chirp perturbations superimposed on a baseline SAI schedule to identify frequency responses and weak nonlinearities, design robust controllers (H-infinity/MPC), and derive active early-warning indicators (phase drift, harmonic distortion). It develops Fisher-information–based input design, spectral regression estimators with leakage control, sparse Volterra modeling, cross-model validation protocols, and uncertainty propagation to control. The E1–E6 program outlines pilot identification, nonlinear diagnostics, robust control synthesis, early-warning, cross-model transfer, and practicality bounds.

Soundness
- Theoretical core is strong and consistent with mature system identification/control theory (FIM scaling ∝ T·|U|^2, H1 estimator assumptions, coherence diagnostics, multiplicative uncertainty, mixed-sensitivity H∞).
- Robustness considerations (noise shaping, leakage correction, crest-factor minimization, band-limited design, ensemble averaging) are appropriate.
- Claims about phase-drift as early-warning and quadratic distortion growth are plausible but would benefit from empirical validation in climate models; mapping “phase margin” intuition from engineering to the open-loop SAI–climate channel requires care.
- Assumptions of local LTI behavior and weak nonlinearity around a drifting operating point are explicitly stated but remain a risk in seasonally forced, multiscale climate dynamics.

Presentation
- Clear exposition of techniques and their integration into an experimental workflow; comprehensive references to system ID/control literature.
- Significant redundancy across sections; repeated subsections (e.g., “Cross-model validation,” “UQ,” “Spectral regression”) and repeated equation labels (eq:fim) will cause LaTeX label collisions.
- Placeholder or nonstandard citations (e.g., enhanced_*, comprehensive_*) need replacement with real references.
- A stray LaTeX error (“umber \end{align}”), inconsistent notation across sections, and dense equation reuse impede readability.

Contribution
- Reframes SAI “pulsing” as an optimal experiment design problem aligned with downstream robust control and monitoring.
- Bridges frequency-domain identification, nonlinear diagnostics, cross-model validation, and robust synthesis within SAI protocols.
- Provides decision-aware, value-of-information perspective linking identification precision to closed-loop regret.

Strengths
- Methodologically rigorous; leverages well-established ID/control theory.
- End-to-end pipeline: OED → identification → UQ → robust control → early warning → cross-model transfer.
- Safety-aware constraints (SAOD/ozone/crest factor) embedded in design.
- Practical advice (integer-period lines, random-phase multisines, PRBS options, ensemble use).

Weaknesses
- No empirical results; feasibility and performance are not demonstrated in any ESM/EMIC.
- Redundant sections and repeated equation labels; LaTeX errors and placeholder citations reduce polish.
- Some claims (phase-drift EWS superiority) are asserted without comparative evidence.
- Handling of strong seasonality/time-variation is only partially addressed (detrending/sliding windows).
- The mapping injection→SAOD→forcing variability is mentioned but not fully formalized in the identification/control loop.

Suggestions
- Consolidate overlapping sections; unify notation; ensure unique equation labels; fix LaTeX errors.
- Replace all placeholder citations with peer-reviewed sources; prune excessive self-referencing.
- Provide a minimal empirical validation: synthetic tests (energy-balance model) and one ESM/EMIC case study showing FIM gains, FRF CIs, controller margins, and EWS lead-time vs passive baselines.
- Quantify practicality: required ensemble size T×amplitude for target coherence in CESM/WACCM; report computational cost.
- Clarify treatment of nonstationarity/seasonality: explicit seasonal LTV model or seasonal lifting; quantify leakage/aliasing from the annual cycle and QBO.
- Detail crest-factor minimization and phase selection algorithms; include code/appendices for OED and spectral estimators.
- Tighten the argument for phase-based EWS by linking to control-relevant margins and providing ablation comparisons to variance/autocorrelation.

Questions
- What ensemble sizes and durations are required in a chemistry-coupled ESM to achieve coherence ≥0.6 across 0.02–2 yr−1 at RMS 0.1–0.3 TgS/yr?
- How robust are FRF estimates to seasonality and slow drift beyond sliding-window detrending? Would a periodic/LTV identification improve bias?
- Will you actuate in injection or SAOD space? How is the injection→SAOD map identified and constrained online?
- How sensitive are early-warning indicators (phase drift, HDI) to unforced variability (ENSO, volcanoes) when the probe is maintained?
- Can the robust OED across models be solved tractably at ESM scale, and how will you estimate Svv priors reliably?
- Beyond quadratic terms, when do higher-order nonlinearities or state-dependent noise undermine the Volterra approximation?

Rating (1-10)
7


## Review checkpoint

Summary
The manuscript proposes an “active spectroscopy” program for stratospheric aerosol injection (SAI): design small, information-optimized multisine/PRBS/chirp perturbations to identify frequency responses and weak nonlinearities (Volterra kernels) from SAI rate to climate outputs; propagate uncertainty through identification to robust H-infinity/MPC control; develop early-warning indicators based on phase drift and harmonic distortion; and assess cross-model transferability with explicit metrics. The work integrates Fisher-information-based experiment design, leakage-aware spectral regression, sparse nonlinear identification, hierarchical UQ, robust control synthesis, and cross-model validation within established SAI protocol constraints.

Soundness
- Technical foundation: Strong. Methods draw on mature frequency-domain system identification (H1/FRF estimators, coherence, local polynomial/multitaper leakage control), optimal input design via Fisher information, sparse Volterra estimation, and standard robust control (mixed-sensitivity H∞, chance-constrained MPC). Assumptions (small-signal, quasi-stationary windows) are stated.
- Climate-specific considerations: Thoughtful treatment of colored internal variability, seasonality/leakage, amplitude/SAOD/ozone constraints, ensemble use, and structural spread across models.
- Gaps/risks: Multiple repeated equation labels (e.g., eq:fim) and cross-references (e.g., Eq. ~ref{eq:transfer}) are inconsistent/missing; some citations appear as placeholders (“enhanced_*_20250812”), undermining traceability. Practical feasibility in chemistry-enabled ESMs and the stability of LTI assumptions under evolving backgrounds need clearer bounds. Controller synthesis across full posterior/model sets is outlined but not fully specified for MIMO cases.

Presentation
- Clarity: Dense and highly technical, but generally precise.
- Organization: Significant redundancy; several sections (spectral regression, PRBS, UQ, robust control) recur with overlapping content and redefined notation. E1–E6 experiment labels are referenced widely but not defined within this excerpt.
- Notation/labels: Notation drifts (q, z, e^{jω}, iω), and equation labels are reused across sections—this will break LaTeX builds and confuse readers.
- Citations: Many appear to be internal placeholders; needs replacement with verifiable references.

Contribution
- Conceptual: Reframes SAI “pulsing” as an optimal, minimally invasive experiment for identification, control, and early warning.
- Methodological: End-to-end pipeline linking Fisher-information design to FRF/Volterra estimation, uncertainty-aware robust control, and cross-model transfer metrics.
- Practical: Aligns with ARISE-SAI/GeoMIP protocols; proposes concrete metrics (coherence, HDI, robust margins, cross-model errors) and feasibility scaling (information ∝ A^2 T).

Strengths
- Cohesive integration of experiment design, identification, UQ, robust control, and monitoring.
- Careful frequency-domain treatment (leakage control, coherence-based diagnostics).
- Explicit attention to governance/safety constraints (SAOD/ozone, amplitude, slew limits).
- Cross-model transfer protocol and metrics; value-of-information framing.
- Early-warning indicators tied to control-relevant phase margins and nonlinear growth.

Weaknesses
- Redundancy and inconsistent notation; repeated/reused equation labels and missing references (e.g., eq:transfer) will render the manuscript hard to follow.
- Placeholder citations reduce credibility and verifiability.
- Limited discussion of MIMO details (multi-input SAI channels to multi-output climate indices) in robust synthesis and cross-model adaptation.
- Empirical validation is proposed but not demonstrated; no concrete results, ablations, or computational budgets.
- Potential under-specification of how SAOD/ozone constraints are enforced in input design and MPC beyond proxies.
- Assumption of quasi-LTI behavior over 5–10 year windows needs tighter justification and diagnostics for time variation.

Suggestions
- Streamline and de-duplicate: Merge the multiple “Spectral regression,” “PRBS,” “UQ,” and “Robust control” sections; present one canonical version each, with consistent notation.
- Fix labels and references: Ensure globally unique equation labels; reconcile all Eq. references; replace placeholder citations with peer-reviewed sources.
- Define E1–E6 once, early, and map each section to them; add a figure/flowchart summarizing the pipeline.
- Provide a notation table and symbol glossary; fix q/z/e^{jω} usage consistently.
- Include a minimal working example: a toy ESM/EMIC demonstration showing FRF recovery, HDI detection, FI scaling with A,T, and a simple H∞ loop-shaping outcome with uncertainty margins.
- Elaborate MIMO treatment: multi-channel PRBS design (orthogonal codes), MIMO FRF estimation with regularization, and robust MIMO synthesis across posterior sets.
- Make SAOD/ozone constraints explicit: include the surrogate mapping and thresholds used in optimization; report crest-factor management and spectral masks.
- Clarify cross-model adaptation: show SISO→MIMO generalization of W(f;θ) and quantify adaptation budget vs. improvement.
- Add computational budgets: expected years/ensemble size for target confidence; practicality curves.

Questions
- How is slow time variation handled beyond sliding windows? Would a time-varying FRF or parametric drift model improve robustness?
- What specific SAOD/ozone surrogate and limits are used in the input design and MPC constraints, and how are they validated?
- How sensitive are FI gains and coherence to mis-specified SEE(ω) under strongly colored variability or regime changes?
- In MIMO settings, how do you design mutually low-correlated multi-channel excitations while respecting global SAOD constraints?
- What are realistic amplitude and duration bounds in WACCM-like models before nonlinearity/chemistry invalidate the second-order Volterra approximation?
- How are exogenous shocks (volcanic aerosols) separated from probe lines in practice, and how does the controller avoid mis-tracking during such events?
- How will you ensure reproducibility (code, line sets, seeds, parameterizations) across different ESM tiers?

Rating (1-10)
7/10. High technical merit and a compelling end-to-end vision, but currently hampered by redundancy, notation/label issues, placeholder references, and lack of demonstrated results. Streamlining and a small empirical validation would substantially strengthen the paper.


## Review checkpoint

Summary
The manuscript proposes “active spectroscopy” of the climate system under stratospheric aerosol injection (SAI): superimposing small, information-optimized multi-sine/PRBS/chirp perturbations on a steady baseline to estimate frequency responses, diagnose weak nonlinearities (second-order Volterra), and enable robust control (H-infinity/MPC) and active early-warning (phase drift, harmonic distortion). It formulates Fisher-information–based input design under environmental constraints, uses leakage-aware spectral regression and coherence for identification, quantifies uncertainty for robust synthesis, and outlines cross-model validation and adaptation.

Soundness
- Methodological grounding: Strong. The use of frequency-domain system identification, optimal input design, coherence, generalized FRFs/Volterra, and robust control is technically sound and well cited (Ljung, Pintelon & Schoukens, MacMartin).
- Assumptions: Relies on local linearity, time-invariance, and quasi-stationarity within sliding windows—nontrivial in forced, seasonal, and multiscale ESMs. The text acknowledges leakage and proposes mitigation (coherent sampling, multi-taper, local polynomial de-biasing), but stronger justification and diagnostics for time variation are needed.
- Nonlinearity: Second-order Volterra approximation is reasonable for small amplitudes; sparse estimation is appropriate. Clearer separation between multisine “detection lines” (valid) and PRBS (no detection lines; rely on higher-order spectra) would avoid confusion.
- Control/UQ: Multiplicative uncertainty envelopes, mixed-sensitivity H-infinity, and chance-constrained MPC are appropriate, assuming reliable FRF uncertainty quantification. Link from FRF covariance to robust weights is plausible but needs concrete calibration recipes.

Presentation
- Comprehensive but overly long and repetitious; several sections recapitulate similar material (PRBS, spectral regression, information design).
- Some equations and labels are duplicated across sections (e.g., repeated tags like eq:fim), and there are minor dangling fragments (e.g., an incomplete sentence at the start).
- Heavy notation density could be lightened with schematic figures (probe spectra, identification/control pipeline), a consolidated algorithm box, and a single, consistent notation table.
- Multiple placeholder citations (enhanced_*) need replacement with stable references.

Contribution
- Conceptual unification: Treating pulsed SAI as active spectroscopy to produce control-ready surrogates and early-warning indicators.
- Methodological integration: Fisher-information–driven probe design, leakage-aware spectral regression, sparse Volterra, uncertainty propagation to robust control, and cross-model transfer/adaptation.
- Operational relevance: Embedding environmental constraints (SAOD/ozone, crest factor), ensembles, and protocol compatibility (ARISE-SAI, GeoMIP).

Strengths
- Rigorous connection between input design (FIM/MI), identification, and robust control objectives.
- Clear, actionable early-warning metrics (phase drift, HDI) tied to control margins.
- Practical excitation choices (PRBS and random-phase multisines), with crest-factor control and seasonality-aware line placement.
- Thoughtful UQ and robust synthesis pipeline; explicit cross-model validation/adaptation plan.
- Solid awareness of governance constraints and small-signal ethos.

Weaknesses
- Practical feasibility is not demonstrated: no quantitative SNR, sample-size, or runtime budgets on real ESMs to support claimed estimator precision at 0.05–0.5 TgS/yr amplitudes.
- Time variation and strong seasonality pose risks to LTI/Volterra assumptions; sliding-window handling is described but not validated.
- Conflation risk: “detection lines” belong to multisine designs, not PRBS; clarify nonlinear diagnostics per excitation.
- Mapping command u to SAOD and chemistry is simplified (linear proxy); uncertainty and nonlinearity in this actuator path may dominate.
- Early-warning hypothesis (phase trending toward −π, HDI growth) is plausible but unvalidated; specificity vs internal variability remains to be shown.
- Density and redundancy impede readability; duplicated equation tags and mixed notation increase cognitive load.
- Several “enhanced_*” references are nonstandard placeholders.

Suggestions
- Provide a minimal end-to-end demonstration: a mid-complexity ESM or emulator showing (i) probe design, (ii) recovered FRFs with coherence/CIs, (iii) sparse Volterra fit with held-out harmonics, (iv) H-infinity/MPC synthesis, and (v) early-warning tracking in a ramp.
- Quantify practicality: tables/plots of estimator variance and coherence vs amplitude, duration, and ensemble size; target bands where γ^2 ≥ 0.6 under ARISE-SAI variability.
- Adopt time-varying identification explicitly: local rational modeling, time–frequency FRFs, or parametric slowly varying models; report drift diagnostics beyond phase.
- Separate and clarify nonlinear diagnostics for multisine (detection lines) vs PRBS (bispectrum/cross-bispectrum).
- Replace SAOD linear proxy with a calibrated actuator model (and bounds) including uncertainty; propagate it into control constraints.
- Consolidate duplicated material; unify equation numbering and notation; add a figure summarizing the workflow.
- Predefine acceptance criteria (coherence thresholds, RMSE, stability margins) and a preregistered evaluation plan across model tiers.
- Replace placeholder citations; release code and probe schedules for reproducibility.

Questions
- What amplitudes and experiment lengths are required (per band) to achieve target FRF phase uncertainty (e.g., <10°) given ARISE-SAI noise spectra? Provide quantitative SNR curves.
- How robust are FRFs to slow nonstationarity (GHG trend, volcanic events) within 5–10 year windows? Do local rational de-biasing and deseasonalization suffice?
- How is the injection-to-SAOD actuator modeled and validated across models and baselines? What is its uncertainty and nonlinearity at proposed amplitudes?
- Can PRBS-based identification separate overlapping internal modes (ENSO, QBO) without line leakage? How do you enforce noncommensurability in multi-input settings?
- How are multiplicative uncertainty weights WΔ constructed from FRF CIs and inter-model spread? Show a recipe and sensitivity of H-infinity results to these envelopes.
- What is the false-alarm trade-off for phase-drift/HDI early-warning relative to passive EWS? Provide AUROC and lead-time benchmarks on at least one model.
- How does sparse Volterra performance degrade with memory length and limited averages? Any guarantees or empirical guidance on regularization tuning?
- For MIMO designs, how do you ensure code orthogonality and condition S_uu under colored noise and constraints? Any identifiability failures observed?

Rating (1-10)
7


## Review checkpoint

Summary
- Proposes “active spectroscopy” for SAI: small, information-optimal multi-sine/PRBS/chirp perturbations to identify frequency responses and weak nonlinearities in ESMs.
- Builds control-ready surrogates (rational FRFs, sparse Volterra, Koopman-lifted predictors) with quantified uncertainty, and synthesizes mixed-sensitivity H-infinity and frequency-weighted MPC.
- Introduces early-warning metrics based on phase-drift toward −π and harmonic distortion growth; includes Fisher-information-based probe design, cross-model transfer, and robust UQ.

Soundness
- Methodologically well-grounded in system identification and robust control; the math and algorithms are standard and appropriate for the stated goals.
- Key assumptions (local LTI over windows, weak nonlinearity, approximate stationarity, small-signal operation) are plausible but nontrivial in ESMs; risks include seasonal/LPTV effects, oceanic slow dynamics, and state dependence.
- Early-warning logic (phase margin erosion, HDI growth) is reasonable in control terms but requires empirical validation in ESMs for specificity and lead time claims.

Presentation
- Comprehensive but overly long and repetitive; several sections duplicate content.
- Reused equation labels (e.g., eq:fim) will break LaTeX cross-referencing; some placeholders (enhanced_*, comprehensive_*) look like nonstandard or missing citations.
- Notation occasionally shifts (SISO vs MIMO), and some labels (E1–E6) are referenced before being fully defined; could be streamlined with a single consistent notation block.

Contribution
- Integrates information-optimal identification, nonlinear diagnostics, robust control synthesis, and early warning into a unified SAI methodology.
- Shifts the “pulsing” debate to a value-of-information framework and ties spectroscopy outputs directly to controller design and governance-relevant constraints.
- Provides a concrete cross-model validation and adaptation plan, which is a needed step toward robustness.

Strengths
- Principled Fisher-information design of probes; clear link from spectral uncertainty to control weights and robustness margins.
- Careful treatment of leakage, coherence, and colored variability; explicit nonlinear handling via sparse Volterra and HDI.
- Dual-controller strategy (H-infinity baseline + constrained MPC) with uncertainty envelopes and scenario stress testing.

Weaknesses
- Heavy reliance on local LTI assumptions and long (5–10 year) windows may limit applicability under strong nonstationarity and slow ocean adjustment.
- Practical identifiability at interannual scales with small amplitudes may demand sizable ensembles; required budgets are not quantified with concrete numbers.
- Editorial issues (duplicate sections, labels, placeholder citations) hinder readability and reproducibility; some algorithmic details (hyperparameter selection, data preprocessing) are underspecified.

Suggestions
- Add a compact, end-to-end demonstration (single ESM tier): probe design → FRF/Volterra estimation → controller → stress tests → early-warning evaluation, with ablations.
- Treat seasonality/time-variation explicitly (e.g., LPTV/periodic FRFs, seasonal lifts, or window-conditioned models); report how this affects identifiability and control.
- Quantify practicality: tables/curves showing amplitude–duration–ensemble trade-offs for target coherence and parameter CIs in key bands.
- Expand MIMO actuation beyond a single scalar u (latitude/season channels) and report identifiability conditions (input code design, code orthogonality, condition numbers).
- Replace placeholder citations; fix equation labels; unify notation; provide pseudo-code and release planned code/data for reproducibility.
- Calibrate early-warning thresholds (false-alarm control) and compare to passive EWS with rigorous detection metrics (AUC, lead time) across multiple models.

Questions
- What minimal amplitude/duration/ensemble is required to achieve γ^2 > 0.8 at 0.1–1 yr−1 for GMST and selected regional indices in CESM1(WACCM)?
- How do you handle seasonal LPTV structure—periodic FRFs, or deseasonalization plus LTI windows? Does this change controller design?
- Can the approach accommodate multi-input SAI (latitudinal bands)? How are orthogonal codes or line assignments chosen to ensure MIMO identifiability?
- How sensitive are early-warning indicators to unrelated internal modes (e.g., ENSO) that may modulate phase independently of SAI-induced margin erosion?
- How frequently would you retune controllers as phase/HDI drifts, and what governance thresholds trigger a rollback?
- What is the mapping and uncertainty from commanded injection to SAOD (actuator dynamics), and how is it included in G and WΔ?

Rating (1-10)
7


## Review checkpoint

Summary
The manuscript proposes “active SAI spectroscopy”: designing small, band-limited perturbations (multisine/PRBS/chirp) to identify frequency responses and weak nonlinearities in Earth system models (ESMs), then using those surrogates for robust H-infinity/MPC control and for early-warning indicators based on phase drift and harmonic distortion. It develops a full pipeline: Fisher-information-based input design, spectral regression with leakage correction, sparse Volterra estimation, uncertainty quantification, controller synthesis, cross-model transfer, and sequential change detection.

Soundness
- Conceptual: Strong. The framework correctly leverages mature system identification, optimal input design, and robust control, adapted to SAI contexts. The link from Fisher information to controller-relevant uncertainty is coherent.
- Mathematical/statistical: Mostly sound but internally inconsistent in places. The frequency-domain FIM, coherence/SNR relations, and mixed-sensitivity H-infinity formulations are standard. However, the text repeats labels (eq:fim) with different meanings, mixes notations (Y/y, S_v/S_EE), and occasionally overstates identifiability under short, colored-noise records. Claims about phase-drift as a generic EWS need more rigorous justification in nonstationary, non-minimum-phase, time-varying settings.
- Modeling assumptions: Local LTI + weak quadratic nonlinearity around small probes is plausible but must be stress-tested against slow drifts, seasonality, and state dependence. Stationarity in 5–10 year windows may be optimistic for interannual bands.

Presentation
- Comprehensive but overly long, repetitive, and occasionally fragmented (opening fragment “othness…”, repeated sections on FIM and robust control, duplicated equation labels, mixed notation/units). Many placeholder citations (enhanced_x_20250812) and repeated references reduce clarity and credibility. A tighter, de-duplicated structure with a single canonical notation is needed.

Contribution
- Methodological synthesis: Adapts frequency-domain identification and optimal input design to SAI; introduces explicit Volterra-based nonlinear diagnostics; ties information design to robust control and value-of-information; proposes active EWS (phase/HDI).
- Practical relevance: If implemented, could sharpen inference in ESMs, quantify controller-relevant uncertainty, and improve specificity/lead time of EWS compared to passive metrics.

Strengths
- Clear end-to-end vision linking probing, identification, UQ, control, and monitoring.
- Solid grounding in system identification and robust control; appropriate use of coherence, multitaper, detection lines, and crest-factor control.
- Decision-aware information design and regret/value-of-information framing.
- Attention to cross-model transfer, uncertainty envelopes, and governance constraints (SAOD/ozone/TV norms).

Weaknesses
- Repetition and inconsistent notation/equation labeling; several eq:fim labels reused with different content; some sections essentially duplicated.
- Evidence gap: no empirical demonstration (even synthetic) of achievable coherence, FRF confidence bands, or EWS lead times under realistic ESM variability, seasonal leakage, and finite lengths.
- Stationarity and identifiability: 5–10 year windows may be insufficient at low frequencies; PRBS/monthly multisine under strong seasonality/chemistry may yield leakage and aliasing beyond what is acknowledged.
- Early-warning rationale: Phase trending to −π as a universal precursor is not established for open-loop, time-varying, multi-input climate pathways; could be confounded by non-minimum-phase zeros or changing background modes.
- Nonlinearity: Quadratic Volterra truncation may miss key state-dependent processes; HDI can be contaminated by seasonality unless very carefully isolated.
- Citations: Numerous placeholder/self-citations (enhanced_*) undermine reviewability; some key climate/chemistry references (e.g., aerosol microphysics response times, ozone sensitivity) are light.

Suggestions
- Consolidate and streamline: remove duplicated sections, unify notation, fix labels, and provide a single definitive FIM/estimator derivation with assumptions.
- Provide a minimal, quantitative demonstration: synthetic LTI+Volterra test and a pilot ESM case showing coherence vs frequency, FRF CI bands, and recovery error under designed probes; quantify amplitude–duration–ensemble trade-offs with actual spectra from a target model.
- Address seasonality/nonstationarity: specify deseasonalizing pipeline, integer-period synchronization, multitaper settings, and leakage diagnostics; justify window lengths for interannual bands.
- Early warnings: add theory/simulations showing when phase drift and HDI rise precede loss of stability; compare to passive EWS with controlled false-alarm rates.
- Chemistry/SAOD constraints: define concrete proxy models and thresholds; discuss realism of monthly PRBS/multisine given aerosol lifetimes and distribution control.
- MIMO clarity: detail multi-input coding (orthogonal PRBS/Gold codes), input measurement noise handling (errors-in-variables/IV), and SISO vs MIMO estimation choices.
- Reproducibility: replace placeholder citations with accessible references or supplementary material; include algorithmic pseudocode and hyperparameter choices (regularization, L-curves).
- Governance framing: explicitly discuss risk of cross-frequency excitation affecting monsoons/ENSO bands, and how safeguards are enforced.

Questions
- What ensemble sizes and record lengths are required to achieve γ^2 > 0.6 at 0.1–0.3 yr−1 for GMST and regional precipitation in a representative ESM? Provide a power analysis.
- How are annual/seasonal harmonics handled to prevent bias at nearby identification lines?
- Can you demonstrate robustness of FRF estimates to slow drift in the baseline and to unmodeled volcanic events?
- How sensitive are HDI and bispectral diagnostics to internal variability that coincidentally populates detection lines?
- What concrete SAOD/ozone constraints are enforced during design, and how are they computed online?
- How do controller designs behave under strong model spread (e.g., WACCM vs another ESM)? Provide multi-plant results.
- Is monthly PRBS physically realizable in the aerosol delivery/injection system you assume, and does stratospheric transport smooth it beyond useful bandwidth?
- How are input measurement errors (commanded vs realized injection/SAOD) treated in estimation?

Rating (1-10)
7/10. Ambitious and timely with strong methodological foundations and potential high impact, but needs consolidation, clearer empirical feasibility, and tighter justification of early-warning claims before acceptance.


## Review checkpoint

Summary
- The manuscript proposes “active spectroscopy” for stratospheric aerosol injection (SAI): small, information-optimized multisine/PRBS perturbations superimposed on a baseline to identify frequency-domain surrogates (FRFs and second-order Volterra/GFRFs), guide Fisher-information-based input design, synthesize robust H-infinity/MPC controllers, and derive active early-warning indicators (phase drift and harmonic distortion). It further outlines uncertainty quantification, cross-model validation/transfer, and surrogate modeling workflows aligned with ARISE/GeoMIP-style protocols.

Soundness
- Theoretical basis is strong and standard in system identification and robust control: spectral regression, coherence-based variance, detection-line multisine designs, sparse Volterra estimation, Fisher information optimization, multiplicative uncertainty shaping, mixed-sensitivity H-infinity, and robust/chance-constrained MPC.
- Key assumptions are stated (small-signal, local LTI/time-invariance within windows, stationarity of noise) and partially mitigated by windowing and deseasonalization.
- Some scope/feasibility tensions: the advertised frequency band (down to ~0.02 cycles/yr) is inconsistent with proposed 3–10-year windows; oceanic memory and red noise challenge resolvability at the lowest frequencies. Early-warning interpretation via “phase margin” is conceptually plausible but not fully formalized for an open-loop, time-varying climate system.
- Nonlinearity handling (second-order Volterra) and robust control treatment (nonlinear residual as additive channel) are reasonable but will require careful validation of sparsity/identifiability under colored variability.

Presentation
- Clear, technically detailed, and well-motivated, with concrete algorithms, metrics, and workflows.
- However, there is extensive redundancy; several sections repeat (two “Robust control synthesis” sections), equation labels are reused (e.g., eq:fim, eq:hdi) and may conflict, and numerous placeholder citations (enhanced_…_20250812) need replacement. Tightening and de-duplication would significantly improve readability.
- Some figures/illustrations would help (e.g., probe spectra, line sets, detection-line layout).

Contribution
- A coherent, end-to-end pipeline that brings mature frequency-domain identification and robust control to SAI modeling: information-optimal probing; FRF/Volterra-based surrogates; uncertainty-aware H-infinity/MPC; active early-warning tied to FRF phase and nonlinear distortion; cross-model transfer metrics. The integration and climate-specific tailoring are the main novelty.

Strengths
- Rigorous, state-of-the-art system ID methodology adapted to ESM constraints.
- Explicit Fisher information design under environmental/operational constraints and crest-factor control.
- Practical spectral estimators (leakage correction, multitaper, detection lines) with uncertainty quantification via coherence/FIM.
- Well-formulated robust control and MPC layers, plus clear evaluation metrics and stress tests.
- Cross-model validation and lightweight domain adaptation are thoughtfully specified.
- Early-warning indicators that are input-referenced and control-relevant.

Weaknesses
- Frequency-band/window-length mismatch: targeting ~0.02 cycles/yr is infeasible in 3–10-year windows; claims should be moderated or designs extended.
- Redundancy and structural duplication; repeated sections and reused equation labels.
- Placeholder/nonstandard citations (enhanced_…); some canonical references missing for climate EWS and bispectral methods in geoscience.
- Limited treatment of explicit nonstationarity (time-varying baseline warming) beyond sliding windows; limited discussion of seasonal leakage/aliasing and input measurement/actuation uncertainty (errors-in-variables).
- Identifiability of second-order kernels in high red-noise settings may be optimistic without stronger priors or longer runs/ensembles.
- Practical feasibility for regional precipitation channels (low SNR) not fully quantified; SAOD/ozone “constraints” are mentioned but not parameterized with concrete bounds.

Suggestions
- Align design claims with resolvable bands: either lengthen windows/campaigns or raise the low-frequency cutoff (e.g., ≥0.1 cycles/yr) and justify via E6 practicality curves.
- Consolidate duplicate sections; fix equation numbering and remove placeholder citations; streamline to a single robust-control section referencing earlier identification outputs.
- Add explicit seasonal handling: seasonal subspace removal, cyclostationary FRFs, or annually synchronized designs; discuss aliasing control.
- Include input-noise/actuation-uncertainty handling (errors-in-variables, total-least-squares, or IV estimators) and quantify SAOD/injection mapping uncertainty.
- Strengthen nonlinear identifiability: predefine sparse Volterra support based on physics (seasonal–interannual mixing), and report power analyses for HDI/bi-spectra under realistic ensemble sizes.
- Calibrate early-warning thresholds with formal change-point or sequential testing and report expected false-alarm rates; clarify linkage to closed-loop margins when no controller is yet deployed.
- Provide concrete parameter ranges and example designs (amplitude, line sets, number of averages, ensemble size) that meet target CI widths for key outputs.

Questions
- What minimal amplitude-duration-ensemble combinations achieve, say, ±10% magnitude and ±10° phase CI for GMST and a target regional index over 0.1–1 cycles/yr?
- How are seasonal harmonics and calendar effects prevented from contaminating detection lines, especially for precipitation?
- Can you quantify the bias/variance trade-off for H2 estimation under realistic red-noise spectra and limited averages?
- How will actuation-to-SAOD uncertainty (transport/chemistry variability) be modeled in identification and control (errors-in-variables, multiplicative input uncertainty)?
- How sensitive are early-warning lead times to probe amplitude reductions imposed by ozone/SAOD risk constraints?
- In cross-model transfer, how often does the lightweight discrepancy filter W(f;θ) suffice without re-probing, and what are acceptable performance degradations?

Rating (1-10)
7


## Review checkpoint

Summary
- The manuscript proposes an “active spectroscopy” framework for stratospheric aerosol injection (SAI) studies in Earth system models, using information-optimal multisine/PRBS perturbations to estimate frequency responses, weak nonlinearities (Volterra kernels), and early-warning indicators (phase drift, harmonic distortion) in sliding windows. Identified surrogates feed robust control (H-infinity/MPC), cross-model transfer tests, and uncertainty quantification grounded in Fisher information and spectral estimation theory.

Soundness
- The methodological core—frequency-domain identification with designed inputs, Fisher-information-optimal probe design, coherence-weighted estimators, and robust control synthesis—is well founded in system identification and control theory.
- Key assumptions merit tighter justification: local LTI behavior in 5–10 year windows despite seasonality and slow drift; use of χ2 approximations for change detection with overlapping windows; adequacy of small probe amplitudes (0.05–0.5 TgS/yr RMS) to achieve target coherence for regional hydrology; and reliable bispectrum/bicoherence estimates with limited averages.
- Frequency-resolution consistency: a 5–10 year window cannot resolve 0.02 cycles/yr (50-year period). The text alternates between very low-frequency targets and short windows; this is a feasibility inconsistency requiring correction.
- Nonlinearity handling is careful (odd/even line layouts, detection lines), but practical identifiability of quadratic kernels in colored, nonstationary climates still needs stronger evidence (e.g., power analyses, SNR budgets).
- Robust control layer is standard and appropriate given multiplicative uncertainty, though the mapping from injection to SAOD and hydrology constraints will require careful validation under model structural errors.

Presentation
- Clear motivation and comprehensive pipeline; however, the manuscript is excessively long and contains substantial duplication of sections (e.g., Fisher information design, spectral regression, PRBS, UQ, cross-model validation) with repeated equation labels (e.g., eq:fim, eq:frf, eq:hdi) that will cause LaTeX label collisions.
- Notation shifts (ω vs f, repeated symbol overloads) and reused equation tags hinder readability.
- Several references are placeholders (enhanced_*, 20250812), limiting verifiability. Consolidation and pruning would markedly improve clarity.

Contribution
- Novel integration of optimal input design, frequency-domain identification, nonlinear diagnostics, early-warning, and robust control for SAI within ESMs.
- Actionable bridge from identification uncertainty to controller synthesis and governance-relevant thresholds; explicit cross-model transfer metrics.
- If demonstrated empirically, this would significantly advance methodology for temporally modulated SAI assessment.

Strengths
- Rigorous use of Fisher information for probe design under environmental constraints (crest factor, SAOD/ozone).
- Coherent early-warning indicators tied to control margins (phase drift, HDI) rather than passive variance/autocorrelation.
- Comprehensive uncertainty propagation from spectral estimators to control margins.
- MIMO/PRBS designs and coherence-aware spectral regression suited to colored climate noise.
- Cross-model validation and adaptation workflow with explicit spectral discrepancy metrics.
- Practical controller formulations (H-infinity/MPC) with multi-objective trade-offs.

Weaknesses
- Feasibility gaps: window length vs frequency coverage; SNR for regional precipitation; number of required ensemble members not quantified.
- Heavy duplication and label reuse; inconsistent notation; reliance on non-public citations.
- Strong reliance on local stationarity around evolving baselines; seasonality is mostly de-trended rather than modeled as cyclostationary/TI systems.
- Change-detection distributional assumptions with overlapping windows may be optimistic.
- Limited discussion of computational cost (ensembles × models × decades) and operational realism of multi-tone control experiments in ESMs.
- Some control-interpretation claims (phase margin analogies) could be tempered for non-minimum-phase, multivariable climate pathways.

Suggestions
- Resolve frequency-resolution inconsistency: restrict target bands to what windows can support, or lengthen windows and quantify the trade-off; provide SNR/FRF variance budgets per band with required amplitudes, durations, and ensemble sizes.
- Consolidate duplicate sections; harmonize notation; ensure unique equation labels; move repeated material to a concise methods appendix.
- Replace or supplement “enhanced_*” placeholder citations with public sources; clearly mark any companion materials.
- Adopt cyclostationary or seasonally time-varying identification (or periodic LTV/BLA) rather than detrending as a catch-all; discuss QBO/annual aliasing explicitly.
- Provide power analyses for HDI/bispectrum estimation; include held-out single-tone validations and ablations (multisine vs PRBS vs ramp).
- Quantify computational cost and provide a minimal viable design (amplitude, lines, ensemble size) for each objective (FRF accuracy, H2 recovery, EWS lead time).
- Clarify closed-loop identification (use of instrumental variables) and guard against feedback bias when controllers operate.
- Add governance-facing thresholds and decision rules that map spectral indicators to control actions, with uncertainty bands.

Questions
- What is the minimal ensemble size and experiment length needed to reach γ^2 ≥ 0.6 for regional precipitation at 0.1–1 yr−1, given typical CESM/WACCM variability?
- How will you handle cyclostationarity formally? Would periodic BLA or time-varying FRFs yield better bias/variance trade-offs than detrending?
- Can you provide power calculations for detecting a specified phase drift (e.g., −20° at 0.2 yr−1) and HDI increase, under realistic noise spectra?
- How sensitive are the early-warning lead times to probe amplitude reductions (e.g., 0.05 vs 0.3 TgS/yr RMS)?
- In cross-model transfer, what bands dominate the FRF gaps, and how often does the adaptation filter W(f;θ) suffice without re-identification?
- How will you validate the injection→SAOD mapping uncertainty and include it in Wm(s) for robust control?

Rating (1-10)
8


## Review checkpoint

Summary
The manuscript proposes an “active spectroscopy” framework for stratospheric aerosol injection (SAI) research that embeds small, information-optimized perturbations (multisines/PRBS/chirps) into Earth system model (ESM) experiments to identify frequency-domain dynamics, weak nonlinearities (second-order Volterra), and to inform robust control design and early-warning indicators. It specifies cross-model validation metrics, Fisher-information-based probe design, spectral regression estimators with leakage control, MIMO identification, robust H-infinity/MPC synthesis under multiplicative uncertainty, and sliding-window phase/HDI early-warning diagnostics. The work is ambitious, technically rigorous, and well anchored in system identification and control theory, aiming to bridge ESM intercomparison protocols with control-ready, uncertainty-quantified surrogates.

Soundness
- Methodological rigor: Strong. The frequency-domain identification toolbox (coherence-weighted FRF estimation, detection lines, Volterra kernels), Fisher information design, and robust control formulations are standard and correctly adapted.
- Assumptions: Relies on small-signal linearization, weak nonlinearity, and (quasi-)stationarity in windows; these are reasonable for in-silico probing but should be stress-tested for cyclostationary seasonality and red noise.
- Feasibility: Technically feasible in ESMs, but the practicality of achieving the target coherence at low frequencies with realistic run lengths/ensemble sizes needs quantitative evidence.
- Gaps: No results are reported; several claims (e.g., earlier EWS lead times, controller transfer) remain hypothetical. Domain adaptation via W(f;θ) is plausible but under-justified physically.

Presentation
- Clear structure but highly repetitive: multiple sections repeat (spectral regression, PRBS, UQ, cross-model validation) with overlapping content and duplicated equation labels (e.g., eq:fim appears several times).
- Notation inconsistencies: f vs ω, H1/H2 vs H^{(2)}, G vs H for FRF, SISO/MIMO symbol reuse, and occasional shifts between m/n and m/m′.
- References: Many “enhanced_…_20250812” citations appear placeholder-like and should be replaced with citable sources or dropped.
- E1–E6 protocol is referenced across sections but not coherently introduced once; a single overview figure/table and consistent cross-references would help.

Contribution
- A unifying pipeline that connects optimal excitation, frequency-domain identification (linear and quadratic), robust control synthesis, cross-model validation, and active early warning for SAI.
- Concrete, control-relevant cross-model metrics (FRF and Volterra discrepancies, controller generalization gap, robustness margins).
- Information-optimal probe design under SAI constraints and explicit practicality bounds via FIM scaling.
- MIMO and detection-line designs tailored to hydrological/circulation pathways and nonlinear diagnostics.

Strengths
- Comprehensive and principled use of system identification/control theory in a climate intervention context.
- Well-specified metrics (FRF/phase errors, HDI, kernel mismatch, regret, robust margins) that are actionable.
- Attention to leakage correction, coherence diagnostics, closed-loop IV variants, and uncertainty propagation.
- Cross-model protocol and multi-plant robust control are appropriate for structural uncertainty.
- Early-warning indicators tied to the actuated pathway (phase drift, HDI) are novel and potentially higher SNR than passive EWS.

Weaknesses
- Redundancy and length obscure the core narrative; duplication of sections and equations.
- Placeholder-like references and inconsistent notation reduce credibility and readability.
- No empirical demonstration; practicality (runtime/ensembles) and achievable coherence at interannual frequencies remain unquantified.
- Seasonality/cyclostationarity and potential time-variability of FRFs are treated briefly; fixed LTI assumptions may be too restrictive for precipitation/circulation.
- Physical interpretation of the “discrepancy filter” W(f;θ) and guarantees (causal/stable mapping) are underdeveloped.
- Operational realism: monthly PRBS toggles, slew limits, and SAOD/ozone constraints need tighter linkage to actual SAI actuator/transport constraints.

Suggestions
- Consolidate: Merge duplicate sections (spectral regression, PRBS, UQ, cross-model validation) into single, crisp expositions; unify notation and equation numbering.
- Provide a schematic of the E1–E6 workflow with concrete parameter choices and a table of symbols.
- Replace or remove “enhanced_…_20250812” citations; add real references where possible.
- Add a pilot demonstration: idealized aquaplanet + WACCM-lite showing (i) coherence vs amplitude/duration/ensemble trade-offs; (ii) FRF with CIs; (iii) HDI/nonlinearity diagnostics; (iv) one robust controller with margins; (v) early-warning ROC/lead-time.
- Address cyclostationarity: use seasonal-LTP/LTV models or seasonally stratified FRFs; document deseasonalization impacts.
- Quantify practicality: explicit compute budgets and minimal designs to hit γ^2 targets at 0.1–1 yr−1; show FIM-based water-filling and L-curve choices.
- Clarify the physics of W(f;θ): constraints to ensure causality/stability and avoid nonphysical phase wrap corrections; consider parametric, low-order, stable discrepancy models.
- Expand on injection-to-SAOD dynamics: consider a two-stage identification (injection→SAOD→climate) to improve interpretability and constraint handling.

Questions
- How many simulated years and ensemble members are required to achieve γ^2≥0.6 at 0.1 yr−1 under typical ESM internal variability? Provide quantitative targets.
- How robust are the FRFs to seasonality? Would a seasonally varying FRF (periodic LTV) materially change controller design?
- Can the domain-adaptation filter W(f;θ) be constrained to be causal/minimum phase, and how is identifiability ensured with short adaptation runs?
- How sensitive are early-warning indicators (phase drift/HDI) to slow changes in internal variability unrelated to stability (e.g., ENSO modulation)?
- What is the performance degradation when excluding frequency bands that overlap with QBO/ENSO to avoid interference?
- Does PRBS excitation at monthly cadence survive stratospheric transport smoothing in realistic chemistry–dynamics models, and are the assumed slew limits implementable?

Rating (1-10)
7


## Review checkpoint




## Review checkpoint

Summary
The manuscript proposes an “active spectroscopy” framework for temporally modulated SAI in Earth system models, combining information-theoretic probe design (multisine/PRBS/chirp), frequency-domain system identification (FRF/BLA, sparse second-order Volterra), uncertainty quantification, robust control synthesis (H-infinity, MPC), early-warning diagnostics (phase drift, HDI), and cross-model validation. It argues that small, optimally designed perturbations can recover control-relevant dynamics with quantified uncertainty, enabling principled multi-objective SAI co-design.

Soundness
- Theoretical basis: Solid grounding in classical frequency-domain identification and optimal input design (Ljung; Pintelon & Schoukens), and robust control (mixed-sensitivity, MPC). The BLA/Volterra machinery and coherence-based UQ are standard and appropriate.
- Assumptions: Local linearity/WSS around a baseline, Gaussian colored noise, and sufficient persistent excitation are reasonable but strong; the manuscript acknowledges small-amplitude constraints and leakage mitigation.
- Mathematical details: Most formulations are correct, but there are inconsistencies and duplications: multiple “eq:fim” and “volterra” labels, G(iω)/G(jω) interchange, SISO/MIMO FIM placement of Suu versus Sε notationally ambiguous. Some objectives (e.g., MI/FIM) omit duration factors or switch between S_uu/S_ε and left/right pre-whitening without clarifying data model.
- Feasibility: Targets (coherence ≥ 0.6 over 0.02–2 yr−1, 10–30 year experiments, ensemble averaging) are plausible in ESM workflows but costly; sequential design and tiered models help.

Presentation
- Clear conceptual pipeline with repeated reinforcement, but the text is overly long and redundant across sections, with duplicated content, equations, and labels.
- Notation switches (i vs j for √−1; q/z; ω grids), mixed \cite/\citep usage, and placeholder citations (enhanced_…_20250812) harm polish and traceability.
- Good practical guidance (leakage control, guard bins, closed-loop IV), but key choices (seasonality treatment, detrending, sampling, windows) could be centralized and standardized.
- Figures/flowcharts and a consolidated glossary for FRF, BLA, HDI, FIM, PRBS, E1–E6 would improve readability.

Contribution
- Integrates information-optimal probing with spectral identification and robust control for SAI—a novel, coherent co-design pipeline beyond step/ramp scenarios.
- Introduces control-informed early-warning signals (phase drift and HDI) and cross-model spectral transfer tests.
- Emphasis on governance-compatible, small-amplitude, in-silico experimentation with explicit UQ is timely.

Strengths
- Rigorous grounding in established identification/control theory.
- Comprehensive pipeline: probe design → identification (linear + quadratic) → UQ → control synthesis → early warning → cross-model validation.
- Practical implementation details (multisine line schemes, leakage corrections, coherence thresholds, closed-loop IV).
- Risk-aware framing with explicit constraints (SAOD/ozone proxies, crest factor).
- Controller robustness tied directly to identified spectral uncertainty.

Weaknesses
- Redundancy and organizational sprawl; duplicated equations/labels and inconsistent notation.
- Placeholder/uncited references (enhanced_… series) and occasional typos reduce credibility.
- Strong stationarity/local linearity assumptions; limited discussion of cyclostationarity/seasonality and state dependence beyond brief mentions.
- Early-warning validation remains conceptual; detection power, false alarm control, and robustness to nonstationarity need empirical demonstration.
- Practical cost/benefit and identifiability under red noise at very low frequencies require more quantitative budgeting (amplitude-duration-ensemble trade-offs).
- Transfer claims would benefit from explicit multi-plant robustness metrics and results, not just plans.

Suggestions
- Streamline and consolidate: merge overlapping sections, unify notation (i/j, q/z, G(ω)), and ensure unique equation labels; centralize assumptions and data-processing steps.
- Replace placeholder citations with canonical sources (e.g., bicoherence: Nikias & Raghuveer; climate spectral analysis references) and ensure bibliography completeness.
- Formalize the noise/data model and FIM derivations consistently (SISO vs MIMO), with units and T-scaling explicit; clarify left/right weighting by Svv−1.
- Add a succinct algorithmic summary (one-page flowchart) and a table of symbols/acronyms.
- Provide a compact synthetic or reduced-ESM demonstration: (i) FIM-guided design improves FRF variance; (ii) Volterra kernel recovers known intermodulation; (iii) robust controller outperforms baselines under ENSO-like noise; (iv) early-warning ROC/lead-time versus passive metrics.
- Address cyclostationarity: outline deseasonalization or periodic FRF/BLA methods; discuss risks from secular trends and protocol-driven nonstationarity.
- Quantify practicality: include amplitude-duration-ensemble “design curves,” with compute budget estimates and coherence targets.
- Clarify controller portability: show multi-plant μ-analysis or ν-gap bounds; report regret across tiers.

Questions
- How will seasonality and slow drift be handled rigorously: deseasonalization, cyclostationary identification, or time-varying FRFs?
- What are the exact amplitude/duration/ensemble budgets needed to reach target FRF/phase uncertainties in the 0.02–0.1 yr−1 band under red noise?
- How sensitive are FRF and HDI estimates to baseline trajectory (nonstationary SAOD) and to probe–state interactions?
- How will you guard against closed-loop bias if identification proceeds under supervisory controllers? Which instruments/z-signals are available in practice?
- Can you provide concrete multi-plant robustness margins (e.g., ν-gap or multiplicative envelopes) that justify controller transfer across model tiers?
- What is the planned evaluation for early-warning efficacy (lead time, AUC, FDR control) under varying internal variability and volcanic scenarios?
- How will the “enhanced_…” references be replaced and the full reproducible toolchain (code/data) shared?

Rating (1-10)
7


## Review checkpoint

Summary
The manuscript proposes an “active spectroscopy” framework to study stratospheric aerosol injection (SAI) dynamics by superimposing small, information-optimized pulses (multisine/PRBS/chirps) on a baseline injection. It develops a frequency-domain system identification pipeline (Fisher-information–based input design, spectral regression for FRFs, sparse second-order Volterra kernels), links identification uncertainty to robust control synthesis (H-infinity, MPC), and defines active early-warning indicators (phase drift toward −π, harmonic/intermodulation growth). It further outlines cross-model transfer tests, emulation for computational efficiency, and practicality bounds that trade probe amplitude, duration, and ensemble size against identifiability. The work is ambitious, technically sophisticated, and well situated in both system identification and SAI literature.

Soundness
- Theoretical foundations (FIM-based design, spectral regression, coherence-based variance, multiplicative uncertainty, mixed-sensitivity H∞) are standard and correctly adapted; the mutual-information objective with Gaussian prior is appropriate.
- Assumptions (local linearity, weak nonlinearity, WSS in windows, approximate Gaussian colored noise) are reasonable for in-silico ESM probing but must be stress-tested under strong red noise and nonstationarity.
- Nonlinearity handling (odd/even multisine lines, sparse Volterra) is methodologically sound; dimensionality control via sparsity/group penalties is appropriate.
- Early-warning logic (phase drift and harmonic growth) is plausible but remains heuristic for climate-scale systems; mapping phase drift to “phase margin” without an explicit loop requires caution.
- Claims on variance scaling (∝1/(T A^2)) and water-filling allocation are correct within the stated approximations; leakage/bias caveats are appropriately noted.
- Cross-model robustness and closed-loop bias mitigation (IV spectral regression) are correctly identified as necessary.

Presentation
- Clear high-level narrative but overly long and repetitious across sections; several concepts (FIM, FRF estimation, HDI) recur verbatim.
- Repeated LaTeX labels (e.g., eq:fim, eq:frf, eq:hdi, eq:volterra_time) will clash; all labels should be unique.
- Mixed citation macros and several apparent placeholder citations (e.g., enhanced_*_20250812) undermine credibility; these must be replaced with real references or removed.
- Notation density is high; a consolidated notation table and a single canonical statement of the core model/assumptions would help.
- A succinct figure/flowchart of the E1–E6 pipeline would improve readability.

Contribution
- Introduces a coherent, information-theoretic experimental design for SAI dynamics in ESMs, bridging system ID and climate modeling.
- Provides an actionable link from identified spectra (with quantified uncertainty) to robust control synthesis and to active early-warning diagnostics.
- Advances nonlinear characterization via sparse Volterra spectroscopy tailored to the SAI actuation channel.
- Proposes cross-model transfer metrics (coherence-weighted Bode distance, HDI consistency, controller portability) that go beyond typical scenario means.

Strengths
- Methodologically rigorous; builds on mature identification/control theory tailored to climate constraints.
- Thoughtful treatment of leakage, coherence, closed-loop bias, crest factor, and safety constraints (SAOD/ozone proxies).
- Practicality emphasis (amplitude–duration–ensemble trade-offs, MI/FIM quantification).
- Integration across identification, control, early warning, and cross-model validation is unusually comprehensive.

Weaknesses
- Nonstationarity and cyclostationarity: WSS assumptions may be strained under ramps/seasonality; window lengths for low-frequency bands may be impractically long.
- Feasibility/SNR risks: achieving γ2 ≥ 0.6 at 0.02–0.1 yr−1 with small amplitudes may require very long runs or large ensembles; quantitative examples are missing.
- Early-warning interpretation: equating FRF phase drift with diminishing phase margin is tenuous without an explicit loop and could be confounded by state dependence.
- Volterra complexity: despite sparsity, practical identifiability of H2 across months–years memory may be limited; risks of overfitting and attribution biases remain.
- Referencing: placeholder “enhanced_…” citations are unacceptable; mixed macro usage; some claims need additional canonical climate references.
- Redundancy and length impede clarity; repeated equations/labels will break LaTeX.

Suggestions
- Replace all placeholder citations with vetted sources; unify citation style; ensure all labels are unique.
- Add quantitative practicality examples: given Svv(ω) from a baseline ensemble, show amplitude/duration needed to reach target FRF CIs at 0.05 and 0.2 yr−1.
- Treat seasonality explicitly: adopt cyclostationary modeling or seasonal regression before spectral ID; consider time-varying FRFs/BLAs in sliding windows.
- Validate small-signal regime: report HDI and BLA deviations versus amplitude to justify 0.05–0.5 TgS/yr RMS across outputs.
- Tighten early-warning methodology: include controlled experiments demonstrating lead time vs passive indicators with false-alarm control; clarify how loop margins are inferred when no controller is present.
- Streamline exposition: consolidate core equations (FIM, FRF estimator, HDI) once; move repetitions to SI; add a pipeline figure and a notation table.
- Provide open-source scripts for multisine/PRBS design (crest factor minimization, detection lines) and leakage-corrected spectral regression.
- Discuss microphysics/chemistry limits on monthly toggling and multi-input (lat/height) actuation feasibility in specific ESMs.

Questions
- What experiment length and ensemble size are required to achieve γ2 ≥ 0.6 at 0.03–0.1 yr−1 for GMST and key hydro indices under CESM(WACCM)-class variability?
- How is seasonality handled in practice: full deseasonalization, cyclostationary regression, or explicit seasonal lines excluded from Ω?
- How robust are the early-warning indicators to ENSO/QBO modulation and episodic volcanic forcing embedded in windows?
- What physical limits constrain monthly actuation (e.g., aerosol lifetime, microphysics) and do they constrain PRBS/multisine clock periods?
- For MIMO designs, which multi-location channels are realistically implementable in current ESM infrastructures, and how is Suu(ω) conditioning ensured?
- How are SAOD/ozone proxy constraints parameterized and validated across models for the optimization constraints?

Rating (1-10)
8


## Review checkpoint

Summary
The manuscript proposes an in-silico, frequency-domain “active spectroscopy” framework for stratospheric aerosol injection (SAI): design small, information-optimal probes (multisines/PRBS/chirps), identify best-linear-approximation FRFs and weak nonlinearities (sparse Volterra), synthesize robust controllers (H-infinity, MPC) with spectral uncertainty, and monitor early-warning signals via phase-drift and harmonic growth. It emphasizes Fisher-information-based input design, leakage-robust spectral regression, cross-model validation, and uncertainty quantification, aiming to deliver quantifiable robustness margins and governance-relevant safety constraints.

Soundness
- Technically well-grounded: frequency-domain identification, Fisher information design, multiplicative uncertainty, mixed-sensitivity H-infinity, chance-constrained/tube MPC, and early-warning via phase margin proxies are standard and appropriately adapted.
- Sensible attention to leakage control, coherence, closed-loop IV estimation, crest-factor limits, and ensemble-based UQ for red noise.
- Risks/assumptions: local LTI/weakly nonlinear approximations under nonstationary climate backgrounds; feasibility of short windows (3–5 years) for reliable low-frequency phase estimates; potential bias from residual seasonality/cyclostationarity; mapping FRF posteriors to Wm may underbound structural uncertainty; admissibility of quadratic Volterra truncation for hydrology and circulation responses; optimistic claims on cross-model transfer without empirical results.
- The proposed early-warning indicators (phase drift toward -π, HDI growth) are plausible but need rigorous calibration against confounders (ENSO, QBO, volcanism) and false-alarm control.

Presentation
- Clear motivation and consistent narrative linking design → identification → control → monitoring.
- Overlong and partially repetitive; multiple sections restate similar ideas.
- Mixed continuous/discrete-time notation and occasional unit/band description shifts could confuse readers.
- Cross-references to E1–E6 are frequent but not self-contained here.
- Several placeholder citations (enhanced_…_20250812) appear nonstandard; needs cleanup and verifiable references.
- A notation table and a single consolidated “Methods” section would improve readability.

Contribution
- Integrates optimal input design, frequency-domain ID, robust control, and early-warning into a single SAI workflow.
- Introduces coherence- and Fisher-weighted selection of performance weights and uncertainty envelopes linking experiment design to control robustness.
- Proposes cross-model spectral invariance tests and controller portability metrics tailored to SAI.
- Articulates practical experiment-sizing via Fisher information and crest-factor-aware probe realization.

Strengths
- Methodologically rigorous; leverages mature identification/control theory.
- Strong emphasis on uncertainty, robustness, and governance constraints.
- Concrete implementation details (multisine line placement, detection lines, PRBS spectra, leakage correction).
- Clear pathways to quantifiable performance and safety margins; explicit metrics for validation and regret.

Weaknesses
- Lack of demonstrated results in this excerpt (no figures, empirical error bars, or closed-loop performance).
- Potential underestimation of nonstationarity and state dependence in ESMs; linear surrogates may be fragile for regional hydrology.
- Early-warning windows may be too short to robustly resolve interannual bands, even with designed probes.
- Cross-model transfer claims remain hypothetical; constructing reliable Wm from inter-model spread is nontrivial.
- Placeholder citations and repeated material reduce polish and credibility.

Suggestions
- Provide a compact, end-to-end “core methods” section with unified notation; move repetitions to appendices.
- Replace all placeholder citations with real, accessible references; add a related-work section situating against existing SAI feedback-control studies.
- Report pilot results: FRF/phase bands with coherence, HDI/bicoherence maps, controller Bode/M-Δ margins, MPC constraint violation rates, and early-warning ROC/lead times versus passive baselines.
- Quantify nonstationarity handling: deseasonalization/cyclostationary regression; window selection; bias from regime shifts.
- Justify probe amplitudes relative to QBO/chemistry sensitivity; include safety analyses and SAOD/ozone proxies.
- Detail construction of Wm from posterior bands and inter-model envelopes; add stress tests showing small-gain conditions across models.
- Clarify discrete vs continuous-time design; provide reproducible algorithms and open-source code/data.

Questions
- How robust are phase-drift EWS to ENSO/QBO modulation and transient volcanism when probes coincide spectrally with these modes?
- What criteria determine the transition from linear FRF to quadratic Volterra models, and how is overfitting prevented with short windows?
- How are Wm and bandwidth choices tuned to avoid overconfidence when coherence is modest at low frequencies?
- What ensemble sizes and record lengths are needed to meet target CRBs at 0.02–0.1 yr^-1, and how do these costs scale across model tiers?
- How sensitive are controller performance and margins to mis-specification of SAOD mapping and injection-to-burden conversion?
- Can the framework accommodate multi-input spatial injection strategies and actuator delays (logistics/stratospheric transport) explicitly?

Rating (1-10)
7


## Review checkpoint

Summary
The manuscript develops an “active spectroscopy” framework for stratospheric aerosol injection (SAI) in Earth system models, combining information-optimal excitation (multisines/PRBS), frequency-domain system identification (FRF/BLA), sparse second-order Volterra modeling, uncertainty quantification, robust control synthesis (H∞/MPC), and cross-model transfer tests. It formalizes Fisher-information–based input design under environmental constraints, proposes coherence-weighted frequency-domain estimators with leakage control, defines invariance/portability metrics across models, and introduces phase-drift and harmonic-distortion early-warning indicators.

Soundness
- Theory: The Fisher information formulations, convex D-/A-optimal design in line powers, coherence-weighted spectral regression, and multiplicative-uncertainty H∞ synthesis are technically sound and consistent with system identification/control literature. The use of IV spectra in closed loop is appropriate.
- Assumptions: Local LTI/BLA with weak quadratic nonlinearity, Gaussian colored disturbances, and stationarity within windows are standard but strong for climate; the authors partially mitigate via deseasonalization, windows, and ensembles. Claims about CRB scaling O((TP)−1) and water-filling intuition are appropriate but will be challenged at very low frequencies (red noise/leakage).
- Scope: Multiplicative uncertainty may under-represent structural/model-form differences; nonlinear/chemistry feedbacks could violate assumed small-signal regimes at some bands/states.

Presentation
- Clear high-level narrative; extensive, well-motivated pipeline.
- Notation is inconsistent (G vs H; q, z, iω vs e^{jω}; S_e/S_ε/S_v), and some LaTeX glitches (“quation}”, repeated sections, duplicated E5-like content).
- Several placeholder/unclear citations (enhanced_…_20250812) need replacement by citable sources.
- Repetition across subsections could be consolidated; cross-references are numerous and occasionally redundant.

Contribution
- Bridges mature frequency-domain identification and optimal input design to SAI/ESM practice with an end-to-end, uncertainty-aware and control-oriented workflow.
- Introduces concrete cross-model frequency-domain invariance metrics, and operationalizes early-warning via phase drift and distortion growth under designed probes.
- Provides a clear optimization-based recipe for probe allocation under environmental guardrails.

Strengths
- Rigorous, integrated methodology (design → identify → quantify uncertainty → control → validate across models).
- Convex, implementable input design tied to Fisher information and environmental constraints.
- Careful attention to leakage, coherence, and closed-loop bias.
- Practical control layer (H∞/MPC) grounded in identified uncertainty; explicit performance/robustness margins.
- Cross-model transferability metrics and sequential/adaptive design are timely and valuable.

Weaknesses
- Feasibility risks: achieving γ²≥0.6 across many outputs/bands in comprehensive ESMs may require long runs/large ensembles; low-frequency identification remains leakage-limited.
- Strong small-signal LTI and stationarity assumptions; limited discussion of time-variation/seasonality beyond brief cyclostationary notes.
- Multiplicative-uncertainty envelope may not capture structural/model differences (e.g., chemistry–microphysics, state dependence).
- Sparse Volterra identification dimensionality/regularization choices and validation burden are under-quantified; potential for overfitting.
- Notation/citation issues and duplicated content reduce readability and confidence.

Suggestions
- Empirical sizing study: quantify required amplitude, duration, and ensemble size per band/output to hit target FRF CI widths (with realistic S_v(ω) from ESMs), including explicit trade-off plots.
- Strengthen nonstationarity handling: cyclostationary identification, time-varying FRF/TVAR or drifting-parameter tracking; clarify window lengths vs. target frequencies.
- Validate early-warning indicators: controlled case studies showing phase-drift/HDI lead times vs. passive EWS, with false-alarm calibration.
- Expand uncertainty models: include additive/coprime uncertainty and bounds informed by cross-model envelopes; discuss state dependence and operation outside small-signal regimes.
- Consolidate and standardize notation; fix LaTeX errors; remove duplicate sections; replace placeholder citations with peer-reviewed sources or mark as in-prep.
- Provide minimal reproducible examples (toy aqua-planet and a CESM(WACCM) pilot) with released code for spectral estimators, leakage correction, and input design.
- Detail practical constraints: SAOD/ozone proxy mappings with units, crest-factor targets, operational toggle limits, and aerosol lifetime impacts on PRBS spectra.

Questions
- What ensemble sizes and run lengths do you anticipate to reach γ²≥0.6 in key bands for precipitation/circulation outputs in WACCM-class models? Any preliminary results?
- How robust are phase-drift and HDI indicators to seasonal aliasing, regime shifts (ENSO/QBO), and slow baseline drift? How are thresholds calibrated to control false alarms?
- Can you report sensitivity to misspecified S_ε(ω) in the input design (robust/Bayesian design performance vs. prior errors)?
- How do you prevent overfitting in the Volterra layer (memory lengths, λ selection) and validate cross-frequency predictions on held-out two-tone tests?
- How will injection-to-SAOD mapping uncertainty be handled in design constraints, given model-dependent sulfate microphysics?
- Do cross-model discrepancies fit multiplicative envelopes, or do you observe phase non-minimum-phase behavior requiring alternative uncertainty structures?

Rating (1-10)
7


## Review checkpoint

Summary
The manuscript proposes an “active spectroscopy” framework for stratospheric aerosol injection (SAI) in Earth system models (ESMs): deliberately designed, small-amplitude pulses (multisines/PRBS/chirps) superimposed on a steady baseline to estimate frequency responses (FRFs), diagnose weak nonlinearities (second-order Volterra), and synthesize robust controllers (H-infinity, MPC). It integrates information-optimal input design via Fisher information, leakage-robust spectral regression, closed-loop identification variants, early-warning indicators (phase drift toward −π and harmonic distortion growth), and cross-model/ensemble uncertainty quantification. The work aims to convert pulsed experiments into control-ready, uncertainty-aware surrogates and to benchmark them across model tiers (E1–E6 experiments).

Soundness
- Methodological grounding: Strong. The use of frequency-domain system identification, optimal input design, instrumental variables for closed-loop bias removal, and robust control is textbook-consistent and well-motivated for in-silico experiments.
- Key assumptions/risks:
  - Stationarity and small-signal linearity: plausible for carefully bounded perturbations but fragile in climate settings with state dependence, regime shifts, and seasonal cyclostationarity. You partly address this (deseasonalization, windowing), but more care is needed.
  - Low-frequency identifiability: targeting 0.02 cycles/yr (50-year period) is inconsistent with 10–30 year experiments; even ensembles cannot overcome fundamental frequency-resolution limits (though they reduce variance). Claims here are optimistic.
  - Leakage/colored noise: good mitigation (commensurate lines, local polynomial, multitaper), but practical efficacy at interannual bands warrants demonstration.
  - Nonlinearity handling: second-order Volterra is reasonable for weak distortions; climate subsystems can be strongly nonlinear/non-normal in some regimes.
  - Chance-constrained MPC and H∞ weights: feasible, but the mapping from FRF/HDI posteriors to robust uncertainty weights needs more precise calibration/validation.
- Cross-model pooling and transfer: sensible in principle; structural differences may dominate in hydrology/circulation bands and should be explicitly bounded.

Presentation
- Comprehensive and technically rich, but lengthy and repetitive across sections; several concepts recur with slightly different notation (G vs H, SNR/coherence definitions).
- Some references are placeholders (e.g., enhanced_…_20250812) and should be replaced with citable sources or clearly marked as in-prep/preprint.
- A clearer separation of “protocol (E1–E6) overview,” “methods,” and “assumptions/limits” would improve readability; a consolidated notation table would help.

Contribution
- Novel synthesis for SAI of: information-optimal probing, frequency-domain identification with explicit UQ, weak-nonlinearity diagnostics, and robust control/early warning—all within coordinated ESM protocols.
- Shifts assessment from step/ramp means to temporal pathways (gain/phase) with governance-relevant uncertainty propagation. This is a valuable reframing for closed-loop geoengineering research.

Strengths
- Solid grounding in established system ID/control theory; careful treatment of leakage, coherence, and Fisher information.
- Thoughtful integration of PRBS and multisine designs, closed-loop IV identification, and MIMO considerations.
- UQ carried through from experiment design to control and early warning; cross-model transfer is explicitly considered.
- Governance-aware constraints (SAOD/ozone proxies, crest factor) and reporting metrics are clearly articulated.

Weaknesses
- Feasibility at very low frequencies is overstated given proposed record lengths; frequency resolution cannot be finessed by ensembles.
- Some assumptions (weak nonlinearity, time-invariance within windows) may be violated in key bands (hydrology/circulation).
- Calibration of uncertainty weights Wm from posterior bands/HDI is under-specified; robustness guarantees hinge on these.
- Heavy reliance on self-citations/placeholders; limited empirical results or case studies to demonstrate the end-to-end pipeline.
- Redundant exposition and occasional notation drift may impede reproducibility.

Suggestions
- Reconcile target bands with achievable frequency resolution. Consider narrowing the lowest band to ≥0.03–0.05 cycles/yr for 20–30 yr runs, or explicitly require ≥50–60 yr records when truly probing 0.02 cycles/yr.
- Add a compact, end-to-end case study (one ESM, a few outputs) showing: input design → FRF/Volterra estimates with CIs → robust control synthesis → early-warning performance vs passive baselines.
- Formalize the mapping from FRF posteriors/HDI to robust uncertainty weights (Wm), including conservative envelopes and validation against held-out scenarios (e.g., volcanic analogs).
- Clarify cyclostationarity handling (seasonal regression vs cyclo-FRF) and demonstrate that residual seasonality does not bias FRFs.
- Consolidate notation (choose G or H for FRF; standardize γ^2/coherence definitions), and move repeated material to a methods appendix.
- Replace placeholder citations with public references or label as preprints; minimize self-citation where possible.
- Quantify practicality with concrete budgets (ensemble sizes, wall-clock) and show L-curve trade-offs among amplitude, duration, and ensemble count.
- Discuss non-negativity of injection under PRBS/multisine and how crest-factor/phase optimization enforces operational constraints.

Questions
- How will you estimate FRFs at 0.02 cycles/yr with 10–30 year experiments? If ensembles are used, how do you address frequency resolution limits rather than variance alone?
- How are multiplicative uncertainty weights Wm and nonlinear residual bounds derived from posterior bands/HDI in a way that yields reliable H∞ guarantees?
- What concrete criteria determine when the small-signal linearization and second-order Volterra approximation remain valid (e.g., HDI thresholds), and how does the controller adapt when they are exceeded?
- How do you treat cyclostationarity: seasonal regression, cyclo-FRF, or both? Any risk of leakage from seasonal harmonics into target bands?
- In closed-loop identification, how is the instrumental variable constructed to remain sufficiently correlated with u but uncorrelated with feedback-contaminated noise?
- What injection non-negativity and SAOD constraints are enforced during PRBS/multisine realization, and how are crest-factor limits guaranteed in practice?
- How sensitive are early-warning detections (phase drift, HDI) to slow drift in background state or unmodeled variability (e.g., ENSO regime shifts), and how do you calibrate false-alarm rates?
- Which model tiers and outputs show cross-model invariance sufficient for transfer? Can you provide preliminary envelopes (gain/phase) indicating robust vs model-dependent bands?

Rating (1-10)
7
