

### What I found (ai-s-plus)
- GeoMIP integration design (text doc):
  - A modular `GeoMIPDataset` using xarray for NetCDF, DRS-style path patterns, optional control experiment, time slicing, and PyTorch indexing. Aligns experiment/control via `xr.align`, handles unit/calendar harmonization, multi-model support, and ensemble selection.
  - ESGF-driven downloads (Wget scripts, esgf-pyclient), guidance on versioning and re-runs.
  - Preprocessing: convert calendars, align time, unit conversions (e.g., `pr` to mm/day), optional anomalies, optional regrid/weights.
  - Analysis utilities: scenario deltas, global means (area-weighted), inter-model stats (mean/std/RMSE), decadal aggregation.
  - “No synthetic fallback” safeguards and config flags.
- Data download guide:
  - Directory structure under `AI-Scientist-v2/data_organized/REAL_DATA_DOWNLOADED/{GLENS_data,CMIP6_data,...}`.
  - Concrete GLENS, CMIP6 steps, verification scripts, env vars to force real data usage, and an automated scaffolding script.

### Integration plan into `Researcher` (deterministic, minimal, no hallucinations)
- Data detection (automatic):
  - Add `ai_researcher/data/needs_detector.py` that inspects the experiment topic, keywords in `input/researcher_input_package_*.json`, and extracted citations to decide if GLENS/GeoMIP/CMIP variables are needed.
  - Heuristics: if topic includes “geoengineering/SAI/GLENS/GeoMIP/CMIP/SSP”, request `tas`, `pr`, `clt`, `od550aer` for `Amon`, plus pair experiment/control (e.g., G6sulfur vs SSP245) and target time slice.
  - Emit a “data plan” JSON (models, experiments, variables, period, base_dir).
- Downloader orchestrator:
  - Add `ai_researcher/data/downloader.py` that:
    - For GeoMIP/CMIP6: generates and runs ESGF Wget scripts or uses `esgf-pyclient` with non-interactive credentials; resumes via `-u`; logs persistent IDs and versions; verifies with `ncdump`/xarray open.
    - For GLENS: include direct links/workflow from your guide; verify required files exist.
    - Writes a manifest (dataset → files, checksum, version).
  - Put data under `~/data/real/CMIP6/GeoMIP/...` (configurable), don’t couple to ai-scientist’s directory scheme.
  - Hard guard: if data missing, raise, never synthesize.
- Minimal loaders (xarray-first, few lines):
  - Add `ai_researcher/data/loaders/geomip_loader.py` and `glens_loader.py` that:
    - Accept base_dir, models, experiment, control, variable, table, ensemble, time slice.
    - Use DRS-style glob: `{variable}_{table}_{model}_{experiment}_{ensemble}_{grid}_*.nc`.
    - Align times/calendars, convert units (`pr` to mm/day), optional anomalies.
    - Return xarray datasets (not PyTorch unless needed).
- Metrics and compute:
  - Add `ai_researcher/analysis/metrics.py`:
    - scenario_delta(exp, ctrl)
    - global_mean_weighted(data)
    - multi_model_stats(list_of_DA) → mean, std, RMSE
    - bootstrap_ci(series, n=1000) for robust CIs
  - Default compute: local xarray (+dask if big). Optional cloud: Intake-ESM/Pangeo Zarr (no local download) via a config flag.
- Pipe it into paper generation:
  - Extend your experiment runners (e.g., `EXPERIMENTS/.../integrated_runner.py`) to:
    - Run needs_detector → downloader → loader → metrics → plots/tables → inject into paper sections (methods, results, uncertainty).
  - Embed provenance (dataset PIDs, versions, file lists, variable units).
- Anti-hallucination controls:
  - Fail-fast if zero-length datasets or NaNs-only after slicing.
  - Require `REAL_DATA_MANDATORY=true` and `SYNTHETIC_DATA_FORBIDDEN=true` envs. Surface them in logs and paper appendix.
  - Store a “Data Evidence” appendix with N lines of `ncdump -h` and variable summaries.

### c) Computation choice
- c1 BFTS (from ai-scientist): ambiguous definition in the wild; higher integration risk, more coupling, unclear reproducibility. I would not rely on it as the primary method.
- c2 Online compute: viable via Pangeo/Intake-ESM Zarr on cloud with Dask (keeps results real and reproducible), but adds infra dependency.
- Recommendation:
  - Primary: local xarray (+dask) + bootstrap Monte Carlo for CIs + multi-model mean/std. This is standard, transparent, reproducible.
  - Optional: cloud toggle to compute against Pangeo CMIP6/GeoMIP Zarr catalogs (faster, no download).
  - If you want BFTS comparisons, wrap ai-scientist’s routine as an external subprocess with strict inputs/outputs and pin versions; don’t import its framework.

### d) Import ai-scientist modules vs call them
- Prefer not importing: dependency and agent-behavior coupling → risk of hallucinations leaking in.
- If needed, “call them” as an external tool:
  - Write data to a temp folder in a fixed schema.
  - Call ai-scientist’s compute script with CLI args.
  - Read back a JSON with metrics; validate against our own baseline metrics; include both in appendix.
- For loaders, copying the small, self-contained xarray loader pattern (from your doc) directly into `Researcher` is better and safer than importing the framework.

### Minimal example loader (few lines, deterministic)
```python
import xarray as xr, numpy as np

def load_pair(base_dir, model, exp, ctrl, var, table="Amon", ens="r1i1p1f1", grid="*", years=None):
    patt = "{v}_{t}_{m}_{e}_{r}_{g}_*.nc"
    pexp = f"{base_dir}/{model}/{exp}/" + patt.format(v=var,t=table,m=model,e=exp,r=ens,g=grid)
    pctrl = f"{base_dir}/{model}/{ctrl}/" + patt.format(v=var,t=table,m=model,e=ctrl,r=ens,g=grid)
    dx = xr.open_mfdataset(pexp, combine="by_coords", decode_times=True)
    dy = xr.open_mfdataset(pctrl, combine="by_coords", decode_times=True)
    if "calendar" in dx.time.attrs: dx = dx.convert_calendar("standard", align_on="year")
    if "calendar" in dy.time.attrs: dy = dy.convert_calendar("standard", align_on="year")
    if years: dx, dy = dx.sel(time=slice(f"{years[0]}-01-01", f"{years[1]}-12-31")), dy.sel(time=slice(f"{years[0]}-01-01", f"{years[1]}-12-31"))
    dx, dy = xr.align(dx, dy, join="inner", strict=True)
    if var == "pr":
        for d in (dx,dy): d[var] = (d[var]*86400.0).assign_attrs(units="mm/day")
    return dx[var], dy[var]
```

### Proper search queries (to use/automate)
- “GLENS dataset programmatic access xarray OPeNDAP THREDDS site:ncar.ucar.edu”
- “GeoMIP CMIP6 ESGF API wget script esgf-pyclient example”
- “CMIP6 intake-esm pangeo zarr example code tas pr Amon”
- “xarray convert_calendar standard align_on year example”
- “bootstrap confidence intervals time series python xarray”
- “area-weighted global mean xarray cos(lat) example”
- “ai-scientist BFTS method definition repository docs”

### Recommended concrete steps in this repo
- Add modules:
  - `ai_researcher/data/needs_detector.py`
  - `ai_researcher/data/downloader.py`
  - `ai_researcher/data/loaders/{glens_loader.py, geomip_loader.py}`
  - `ai_researcher/analysis/metrics.py`
- Add config flags:
  - `REAL_DATA_MANDATORY`, `SYNTHETIC_DATA_FORBIDDEN`, `USE_GEOMIP_DATA`, `USE_GLENS_DATA`, and `DATA_BASE_DIR`
- Extend runner to call: detect → download/verify → load → compute → inject plots/tables into paper.
- Provide a CLI:
  - `python -m ai_researcher.data.download --plan path/to/data_plan.json`
  - `python -m ai_researcher.analysis.run --plan path/to/data_plan.json`
- Optional cloud path:
  - Add `--use-intake-esm` to bypass download and compute against Pangeo catalogs.

### Summary current state
- `Researcher` produces strong narrative but misses deterministic real-data numerics; no GLENS/GeoMIP loader/compute.
- `ai-s-plus` docs provide a solid GeoMIP loader pattern and strict “no synthetic fallback” guidance; GLENS/CMIP6 download workflow is specified.
- Plan: embed a minimal xarray loader + downloader + metrics into `Researcher`, forbid synthetic, compute robust stats (bootstrap + multi-model), and optionally wrap ai-scientist compute as an external tool if desired.

- Suggested choice:
  - Calculations: use local xarray (+dask) with bootstrap and multi-model statistics; optionally cloud via Pangeo intake; avoid BFTS unless wrapped and version-pinned.
  - Reuse modules: copy minimal loader/metrics here; do not import the ai-scientist framework. If using its compute, call it as a subprocess with a strict I/O contract.

- Impact:
  - Real-data, reproducible figures/tables included in papers.
  - Clear provenance and no hallucination risk.
  - Swappable backend (local vs cloud) with one flag.