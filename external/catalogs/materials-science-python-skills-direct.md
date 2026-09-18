# Direct Skill List — Computational Materials Science (v2, pruned)

Cut down from the previous version. Anything that was domain-general-physics, domain-general-chemistry,
domain-general-engineering, or otherwise a stretch for someone doing *computational* materials science
specifically is gone — not just astronomy.

## Removed, and why

| Removed | Why it's out |
|---|---|
| `astropy` | Astronomy/astrophysics (your example) |
| `qiskit`, `cirq`, `pennylane`, `qutip` | Quantum **computing** (building circuits/algorithms for quantum hardware) — a different field from quantum-mechanical simulation *of* materials. Only relevant if you specifically research qubit materials or quantum algorithms for chemistry, which you didn't mention. |
| `fluidsim`, `openpiv`, `simpy` | CFD, experimental particle-image-velocimetry, and discrete-event/queueing simulation — mechanical/fluids/ops-research, not atomistic or electronic-structure materials work |
| `matlab` | Not Python, and not materials-specific |
| `lab-hardware-cad` | Physical lab-equipment design — you're computational, not experimental |
| `transformers` (Hugging Face) | General NLP/vision library; not part of a typical materials-simulation stack |
| `statsmodels` | Redundant with `statistical-analysis` below (same job, lower-level API) |
| `seaborn` | Redundant with `matplotlib`/`scientific-visualization` (more of a survey-data/social-science plotting default) |
| `polars`, `vaex` | Redundant with `dask` for the same "bigger than RAM" job |
| `experimental-design`, `statistical-power` | Physical-experiment sample-size/randomization planning — your simulation-campaign equivalent is already covered by `parameter-optimization` below |
| `hugging-science` | Spans bio/astronomy/climate/ecology/medicine etc. — materials is one slice of a very wide catalog |
| `database-lookup` | 78 databases, but mostly clinical/genomic (ClinicalTrials.gov, FDA, ClinVar...); the two materials-relevant ones (PubChem, USPTO) aren't worth the bundle |
| `scientific-critical-thinking` | Its actual frameworks (GRADE, Cochrane Risk of Bias) are medical evidence-grading standards, not simulation/materials methodology |
| `literature-review`, `research-lookup`, `exa-search` | Three more ways to do what `paper-lookup` already does for free — kept one, cut the paid-API/heavier alternatives |
| `ontology-explorer`, `ontology-mapper`, `ontology-validator` | Real materials-science content, but a semantic-web/metadata-curation specialty most simulation work never touches |

`rdkit` survives but flagged: keep it only if your materials have a molecular/organic component
(MOFs, polymers, electrolytes, organic electronics). Cut it if you're doing purely inorganic/solid-state work.

---

## 1. Computational materials science — numerical methods, HPC, verification

21 of the original 24 from `HeshamFS/materials-simulation-skills` (dropped the 3 ontology ones above).
This is still the single most on-target repo — every skill here is genuinely about materials/PDE
simulation.

| Skill | Does | Tier | Link |
|---|---|---|---|
| `convergence-study` | Grid/timestep convergence, Richardson extrapolation, GCI per ASME V&V 20 | HIGH | [link](https://github.com/HeshamFS/materials-simulation-skills/tree/main/skills/core-numerical/convergence-study) |
| `differentiation-schemes` | Finite-difference stencils, central/upwind/compact/spectral schemes | HIGH | [link](https://github.com/HeshamFS/materials-simulation-skills/tree/main/skills/core-numerical/differentiation-schemes) |
| `linear-solvers` | Direct (LU/Cholesky) vs iterative (CG/GMRES/BiCGSTAB) solver selection, conditioning | MEDIUM | [link](https://github.com/HeshamFS/materials-simulation-skills/tree/main/skills/core-numerical/linear-solvers) |
| `mesh-generation` | Grid resolution from physics scales, aspect ratio/skewness checks | MEDIUM | [link](https://github.com/HeshamFS/materials-simulation-skills/tree/main/skills/core-numerical/mesh-generation) |
| `nonlinear-solvers` | Newton, Newton-Krylov, quasi-Newton, Anderson acceleration, Levenberg-Marquardt | HIGH | [link](https://github.com/HeshamFS/materials-simulation-skills/tree/main/skills/core-numerical/nonlinear-solvers) |
| `numerical-integration` | Explicit RK, BDF, Rosenbrock, Adams, adaptive step-size control | MEDIUM | [link](https://github.com/HeshamFS/materials-simulation-skills/tree/main/skills/core-numerical/numerical-integration) |
| `numerical-stability` | CFL/Fourier criteria, von Neumann analysis, stiffness detection | HIGH | [link](https://github.com/HeshamFS/materials-simulation-skills/tree/main/skills/core-numerical/numerical-stability) |
| `time-stepping` | Adaptive time-step policy, ramping through phase changes/sharp gradients | HIGH | [link](https://github.com/HeshamFS/materials-simulation-skills/tree/main/skills/core-numerical/time-stepping) |
| `fair-simulation-packager` | FAIR reproducibility bundles: hashes, provenance, NOMAD/OPTIMADE/MP framing | HIGH | [link](https://github.com/HeshamFS/materials-simulation-skills/tree/main/skills/data-management/fair-simulation-packager) |
| `hpc-runtime-doctor` | Diagnoses MPI/OpenMP/GPU layout, module, walltime, scheduler problems | HIGH | [link](https://github.com/HeshamFS/materials-simulation-skills/tree/main/skills/hpc-deployment/hpc-runtime-doctor) |
| `slurm-job-script-generator` | Generates + sanity-checks SLURM `sbatch` scripts (nodes, MPI/OMP, GPUs, walltime) | HIGH | [link](https://github.com/HeshamFS/materials-simulation-skills/tree/main/skills/hpc-deployment/slurm-job-script-generator) |
| `skill-evaluator` | Tests whether any Agent Skill (yours included) actually does what it claims | HIGH | [link](https://github.com/HeshamFS/materials-simulation-skills/tree/main/skills/meta/skill-evaluator) |
| `simulation-failure-triage` | First-response triage for LAMMPS/VASP/QE/MOOSE crashes (NaN, blow-up, etc.) | HIGH | [link](https://github.com/HeshamFS/materials-simulation-skills/tree/main/skills/robustness/simulation-failure-triage) |
| `md-analysis-planner` | Plans RDF, MSD/diffusion, VACF/VDOS, coordination numbers, PBC unwrapping | HIGH | [link](https://github.com/HeshamFS/materials-simulation-skills/tree/main/skills/simulation-workflow/md-analysis-planner) |
| `parameter-optimization` | DOE (Latin Hypercube, factorial), sensitivity ranking, optimizer selection | MEDIUM | [link](https://github.com/HeshamFS/materials-simulation-skills/tree/main/skills/simulation-workflow/parameter-optimization) |
| `performance-profiling` | Parses timing logs, parallel scaling, memory estimates for sim codes | MEDIUM | [link](https://github.com/HeshamFS/materials-simulation-skills/tree/main/skills/simulation-workflow/performance-profiling) |
| `post-processing` | Extract fields/line-profiles, detect steady state, statistical summaries | MEDIUM | [link](https://github.com/HeshamFS/materials-simulation-skills/tree/main/skills/simulation-workflow/post-processing) |
| `simulation-orchestrator` | Parameter-sweep campaigns (grid/linspace/LHS), batch job tracking | MEDIUM | [link](https://github.com/HeshamFS/materials-simulation-skills/tree/main/skills/simulation-workflow/simulation-orchestrator) |
| `simulation-validator` | Pre-flight config checks, runtime NaN/residual monitoring, post-hoc validation | HIGH | [link](https://github.com/HeshamFS/materials-simulation-skills/tree/main/skills/simulation-workflow/simulation-validator) |
| `workflow-engine-mapper` | Chooses among atomate2, jobflow, AiiDA, pyiron, or a plain script for your campaign | HIGH | [link](https://github.com/HeshamFS/materials-simulation-skills/tree/main/skills/simulation-workflow/workflow-engine-mapper) |
| `benchmark-and-mms-planner` | V&V campaigns via manufactured solutions, canonical benchmarks, uncertainty | HIGH | [link](https://github.com/HeshamFS/materials-simulation-skills/tree/main/skills/verification-validation/benchmark-and-mms-planner) |

## 2. Materials structure & chemistry

| Skill | Does | Link |
|---|---|---|
| `pymatgen` | Crystal structures, symmetry/space-groups, phase diagrams, VASP/CIF/POSCAR I/O, Materials Project API | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/pymatgen) |
| `rdkit` *(keep only if molecular/organic materials — MOFs, polymers, electrolytes)* | Cheminformatics core: SMILES/SDF, descriptors, fingerprints, substructure search | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/rdkit) |

## 3. Math

| Skill | Does | Link |
|---|---|---|
| `sympy` | Exact symbolic algebra/calculus — deriving elastic-constant relations, thermodynamic identities, equation solving, LaTeX/code generation via `lambdify` | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/sympy) |

## 4. Machine learning & optimization for materials informatics

| Skill | Does | Link |
|---|---|---|
| `scikit-learn` | Classical ML: classification/regression/clustering, pipelines, hyperparameter tuning | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/scikit-learn) |
| `pytorch-lightning` | Structured deep-learning training: multi-GPU/TPU, DDP/FSDP, logging | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/pytorch-lightning) |
| `torch-geometric` | Graph neural networks — crystal-graph / molecular-graph property prediction (CGCNN/MEGNet-style models) | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/torch-geometric) |
| `pymc` | Bayesian modeling/MCMC — Bayesian optimization loops for autonomous materials discovery | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/pymc) |
| `pymoo` | Multi-objective optimization: NSGA-II/III, Pareto fronts — trading off competing material properties | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/pymoo) |
| `shap` | Explain/audit ML property-prediction models (feature attribution) | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/shap) |
| `umap-learn` | Nonlinear dimensionality reduction — visualizing composition/property feature spaces | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/umap-learn) |
| `networkx` | Graph algorithms — defect/bond networks, structure-graph analysis | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/networkx) |
| `arbor` | Iteratively improve a model/simulation pipeline against an evaluator without overfitting to the dev set | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/arbor) |

## 5. Data handling & plotting

| Skill | Does | Link |
|---|---|---|
| `dask` | Scale existing pandas/NumPy code beyond RAM or across a cluster (screening-database-scale work) | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/dask) |
| `zarr-python` | Chunked N-D array storage for large simulation output (trajectories, field data) | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/zarr-python) |
| `matplotlib` | Fine-grained plotting, novel plot types, PNG/PDF/SVG export | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/matplotlib) |
| `scientific-visualization` | Publication-ready multi-panel figures, colorblind/contrast auditing, journal export | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/scientific-visualization) |

## 6. Data quality & uncertainty

| Skill | Does | Link |
|---|---|---|
| `uncertainty-and-units` | pint unit-checking, GUM uncertainty budgets, Monte Carlo propagation, CODATA constants, "is this number physically reasonable" checks — local only, no network | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/uncertainty-and-units) |
| `statistical-analysis` | Guided test selection, assumption checks, effect sizes for comparing simulation/property distributions | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/statistical-analysis) |
| `exploratory-data-analysis` | Bounded, local EDA on CSV/NumPy/HDF5 output: missingness, outliers, transform sensitivity | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/exploratory-data-analysis) |

## 7. Research compute infrastructure

| Skill | Does | Link |
|---|---|---|
| `optimize-for-gpu` | Rewrites CPU-bound NumPy/SciPy/pandas/NetworkX code into CuPy/Numba-CUDA/cuML/RAFT | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/optimize-for-gpu) |
| `get-available-resources` | Read-only CPU/memory/disk/scheduler/accelerator inventory before a heavy local run | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/get-available-resources) |
| `modal` | Serverless GPU/CPU cloud for scaling Python jobs — needs `MODAL_TOKEN_ID`/`SECRET` | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/modal) |

## 8. Software engineering practice

All 14 from `obra/superpowers` — general SWE discipline, directly applicable to maintaining
simulation/analysis code:

| Skill | Does | Link |
|---|---|---|
| `test-driven-development` | Red-green-refactor before writing implementation code | [link](https://github.com/obra/superpowers/tree/main/skills/test-driven-development) |
| `systematic-debugging` | Structured root-cause process before proposing any fix | [link](https://github.com/obra/superpowers/tree/main/skills/systematic-debugging) |
| `verification-before-completion` | Requires running/showing verification output before claiming success | [link](https://github.com/obra/superpowers/tree/main/skills/verification-before-completion) |
| `writing-plans` | Turns a spec into a concrete multi-step plan before touching code | [link](https://github.com/obra/superpowers/tree/main/skills/writing-plans) |
| `executing-plans` | Executes a written plan with review checkpoints | [link](https://github.com/obra/superpowers/tree/main/skills/executing-plans) |
| `brainstorming` | Explores intent/requirements before implementation work | [link](https://github.com/obra/superpowers/tree/main/skills/brainstorming) |
| `using-git-worktrees` | Isolated workspace per feature/experiment via git worktree | [link](https://github.com/obra/superpowers/tree/main/skills/using-git-worktrees) |
| `finishing-a-development-branch` | Decides how to integrate finished, tested work | [link](https://github.com/obra/superpowers/tree/main/skills/finishing-a-development-branch) |
| `requesting-code-review` | Structured self-check before opening a review | [link](https://github.com/obra/superpowers/tree/main/skills/requesting-code-review) |
| `receiving-code-review` | Verifies feedback technically instead of blindly implementing it | [link](https://github.com/obra/superpowers/tree/main/skills/receiving-code-review) |
| `dispatching-parallel-agents` | Splits independent tasks across parallel subagents | [link](https://github.com/obra/superpowers/tree/main/skills/dispatching-parallel-agents) |
| `subagent-driven-development` | Executes independent-task plans within one session via subagents | [link](https://github.com/obra/superpowers/tree/main/skills/subagent-driven-development) |
| `writing-skills` | Meta: create/edit/verify your own skills (e.g. your lab's VASP conventions) | [link](https://github.com/obra/superpowers/tree/main/skills/writing-skills) |
| `using-superpowers` | Entry point — **heads-up:** forces a skill check before any response once installed | [link](https://github.com/obra/superpowers/tree/main/skills/using-superpowers) |

Official Anthropic tool-building/document skills (authoritative source — other repos' copies are
vendored from here):

| Skill | Does | Link |
|---|---|---|
| `mcp-builder` | Build an MCP server to wrap your lab's internal APIs/databases as a callable tool | [link](https://github.com/anthropics/skills/tree/main/skills/mcp-builder) |
| `skill-creator` | Create/edit/benchmark your own skills | [link](https://github.com/anthropics/skills/tree/main/skills/skill-creator) |
| `docx` / `pdf` / `pptx` / `xlsx` | Word/PDF/PowerPoint/Excel creation (already built into Claude.ai; only needed via API/Claude Code) | [docx](https://github.com/anthropics/skills/tree/main/skills/docx) · [pdf](https://github.com/anthropics/skills/tree/main/skills/pdf) · [pptx](https://github.com/anthropics/skills/tree/main/skills/pptx) · [xlsx](https://github.com/anthropics/skills/tree/main/skills/xlsx) |

From `AutumnsGrove/ClaudeSkills` (mechanics, not workflow — don't overlap with the superpowers set):

| Skill | Does | Link |
|---|---|---|
| `git-advanced` | Interactive rebase, bisect, reflog recovery, cherry-picking | [link](https://github.com/AutumnsGrove/ClaudeSkills/tree/master/git-advanced) |
| `docker-workflow` | Multi-stage builds, docker-compose — reproducible simulation environments | [link](https://github.com/AutumnsGrove/ClaudeSkills/tree/master/docker-workflow) |
| `env-config` | `.env`/secrets management via `uv` — handling `MP_API_KEY`, `MODAL_TOKEN`, etc. safely | [link](https://github.com/AutumnsGrove/ClaudeSkills/tree/master/env-config) |
| `sql-expert` | Query writing/schema design — if tracking simulation campaigns in a DB | [link](https://github.com/AutumnsGrove/ClaudeSkills/tree/master/sql-expert) |

## 9. Scientific writing, literature & documents

| Skill | Does | Link |
|---|---|---|
| `paper-lookup` | 18 free scholarly APIs (arXiv, OpenAlex, Crossref, Semantic Scholar, Zenodo, etc.) — no API key needed | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/paper-lookup) |
| `citation-management` | OpenAlex/PubMed/Scholar search, DOI→BibTeX, reference validation | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/citation-management) |
| `pyzotero` | Programmatic CRUD on your actual Zotero library | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/pyzotero) |
| `scientific-writing` | Drafts/audits manuscripts with evidence provenance and consistency checks — local, no API key | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/scientific-writing) |
| `peer-review` | Structured, evidence-bounded review drafts for manuscripts/proposals — local, no API key | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/peer-review) |
| `venue-templates` | Journal/conference template selection, page/anonymity rules, LaTeX scaffolds | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/venue-templates) |
| `latex-posters` | LaTeX conference posters (beamerposter/tikzposter/baposter) | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/latex-posters) |
| `scientific-slides` | Research-talk slide decks (PowerPoint or LaTeX Beamer), thesis-defense structure | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/scientific-slides) |
| `markdown-mermaid-writing` | Text-based diagrams/documents as the default (free, local, no image-gen API) | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/markdown-mermaid-writing) |
| `research-grants` | NSF/NIH/DOE/DARPA proposal structure, budgets, significance narratives — DOE and NSF both fund materials work directly | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/research-grants) |
| `scientific-brainstorming` | Structured early-stage ideation with explicit assumptions and adversarial review | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/scientific-brainstorming) |
| `hypothesis-generation` | Turns observations into testable, preregistration-ready hypotheses — local, no network | [link](https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/hypothesis-generation) |

*Bonus, free right now: I already have Consensus (220M+ peer-reviewed papers) and PubMed connectors available directly in this chat — no skill install needed if you just want me to search literature for you here.*

---

**Total: 21 + 2 + 1 + 9 + 4 + 3 + 3 + 24 + 12 = 79 skills**, down from ~93+ before, and every single one
survives a "would a computational materials scientist actually reach for this" test.
