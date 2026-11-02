# PhD Interview Preparation: CMS DE-SynPUF Claims Pipeline and Professor Rachel Richesson

**Use:** A preparation module for a prospective PhD interview. It is also a source document for an AI question-answering agent.  
**Project:** A reproducible Medicare-style claims data engineering and analytics pipeline.  
**Repository snapshot:** Current working tree, reviewed on 2026-11-01.  
**Speaker:** The sole builder of this repository, as confirmed by its owner.  
**Important boundary:** Every beneficiary and every model result discussed here comes from synthetic CMS DE-SynPUF data. No result in this project validates a method for clinical care or describes the real Medicare population.

## How an AI agent should use this document

Answer in the first person when speaking for the project owner. Use only claims marked **implemented** or **observed** to describe completed work. Use the words *I would*, *I propose*, or *a next study could* for work marked **proposed**. Name the source of a number when giving one. Keep CMS Sample 1 and the tiny demo fixture separate. If asked about personal decisions, collaboration, time spent, or a clinical deployment, do not invent facts. Say which part needs the owner's confirmation.

For a short answer, start with the direct answer and one limitation. For a deep answer, add the data grain, code path, validation method, and the next research question. If a question assumes that an LLM generated the current explanation, correct that assumption. The current explanation is rule based. If a question assumes that a strong synthetic-data score proves usefulness on real patients, correct that assumption too. CMS says this data has very limited value for drawing inferences about real beneficiaries [CMS SynPUF overview](https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-claims-synthetic-public-use-files).

Paths below are relative to the repository root. Code and saved reports establish implementation or local results, not clinical validity. Recheck the working tree before an interview if it changes.

## 01. Project identity

### What I built

I built a local pipeline for the CMS 2008–2010 Data Entrepreneurs' Synthetic Public Use File, called DE-SynPUF. I use DE1.0 Sample 1. The pipeline loads CMS-style CSV files into DuckDB. It cleans five kinds of source data. It builds one row per synthetic beneficiary and year. It then supports descriptive analytics, a next-year high-cost classification exercise, a Streamlit dashboard, a FastAPI service, and a plain-language explanation layer. The project is an engineering and research-methods demonstration. It is not a clinical study. The source files are public synthetic files, although the raw files and generated database stay out of Git. See `README.md`, `docs/project_summary.md`, and `src/ingest/load_raw_files.py`.

CMS Sample 1 has eight files: three annual beneficiary files, inpatient, outpatient, prescription drug events, and two carrier splits [CMS Sample 1 downloads](https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-claims-synthetic-public-use-files/cms-2008-2010-data-entrepreneurs-synthetic-public-use-file-de-synpuf/de10-sample-1). All eight ZIPs are under `data/raw/cms_sample_1/`. `data/raw/demo_sample/` is a tiny software fixture.

My contribution is the repository implementation. That includes ingestion, SQL-based transformations, feature tables, model training and evaluation, quality checks, reporting, the API, the dashboard, and the fixture-based test path. This description reflects the owner's confirmed sole-builder role. It does not make claims about an employer, a laboratory, external collaborators, or previous clinical research experience. Those personal facts must be supplied by the owner if an interviewer asks.

### Project status, in precise terms

The pipeline is implemented and has been run locally against CMS Sample 1. The local saved quality report has status `pass`. The saved model report lists 227,292 modeling rows. The model and quality artifacts exist in `data/processed/`; their Markdown summaries live in `docs/`. The repository also contains a small end-to-end demo and tests. These are **observed local artifacts**, not an external replication or a peer-reviewed evaluation. The latest saved model is a random forest selected by test-set average precision. An API and dashboard read the warehouse and saved artifacts. They are demonstration interfaces, not production clinical services. See `data/processed/quality_report.json`, `data/processed/model_metrics.json`, `docs/latest_quality_report.md`, and `docs/latest_model_report.md`.

There are no clinical notes, labs, chart review, or validated outcomes here. CMS warns that DE-SynPUF analyses can mislead when used to infer facts about real beneficiaries [CMS user manual](https://www.cms.gov/research-statistics-data-and-systems/downloadable-public-use-files/synpufs/downloads/synpuf_dug.pdf). I can claim a working pipeline, not a real-patient risk tool.

### One-line project identity

> I built a reproducible local claims pipeline on CMS synthetic Medicare-style data to study data quality, patient-year feature design, and the limits of a high-cost prediction workflow.

### Evidence tags for interview use

**Implemented** means there is code in this repository. **Observed** means a saved local report or database contains the result. **Documented intention** means a design goal appears in repository documentation. **Proposed** means a future research idea in this guide. These labels prevent an AI agent from turning a research plan into an invented accomplishment.

## 02. Interview explanations

### Rehearsable two-minute version

> I built a claims data pipeline using CMS DE-SynPUF, a public synthetic version of Medicare-style data. I wanted to learn how messy, linked claims files become a reproducible analysis dataset. I used DuckDB because it lets me run the full workflow locally. The first layer imports the source files as text. The next layer standardizes IDs, dates, amounts, chronic-condition flags, and diagnosis and procedure codes. The final layer gives me one row per synthetic beneficiary-year, with utilization counts, paid amounts, and code counts.
>
> I then framed a simple prediction task. For a person-year in 2008 or 2009, I use that year's features to predict whether the same synthetic person is in the top ten percent of total synthetic cost in the following year. I train on 2008-to-2009 pairs and test on 2009-to-2010 pairs. I compare logistic regression with a random forest. In the saved Sample 1 run, the random forest had an AUROC of about 0.748 and an AUPRC of about 0.266. Those values are software workflow diagnostics. They do not establish clinical performance, because the data are synthetic.
>
> The most interesting part for me is not the score by itself. It is the work needed to define a reliable person-year, preserve source lineage, avoid temporal leakage, check missingness and odd payment values, and explain what a label actually means. I also built quality checks, a dashboard, an API, and a safe rule-based text explanation. The project made me more interested in the research questions behind computable phenotypes and fitness for use. I would like to study how a phenotype definition, its data sources, and its validation can be made transparent and portable across settings. That connects directly to Professor Richesson's work on data quality, standards, and reusable phenotypes.

This version takes roughly two minutes at a calm pace. Practice it aloud. The final sentence is a research interest, not a claim that this repository already implements a validated phenotype. Professor Richesson's published framework emphasizes sharing phenotype definitions and evidence about their use [Richesson, Smerek, and Cameron, 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4975566/).

### Thirty-second version

> I built a local DuckDB pipeline for CMS synthetic Medicare claims. It turns raw files into checked patient-year features and demonstrates next-year high-cost prediction, reporting, and safe explanations. The key lesson is that a model score depends on how the cohort, time window, outcome, and data quality are defined. I want to move from a clean engineering demonstration toward rigorous, validated definitions for real-world research.

### If asked for the main technical contribution

> The main contribution is the end-to-end, inspectable data path. I can trace a field from a CMS file into a cleaned claims table, then into a patient-year feature and the model. I also made quality checks and saved evaluation artifacts part of the workflow. This is a portfolio implementation. It is not a new clinical algorithm.

### If asked why this fits a PhD interview

> Building the system raised research questions that code alone does not settle. How do we know a claims-based condition flag is fit for a particular research question? How do we measure missingness and coding differences? How do we transport a phenotype to another site? How do we validate it against clinical evidence? I can point to where my prototype stops, and I want to learn how to answer those questions rigorously.

## 03. Problem and motivation

Claims record billed services and payments across files with different grains. One beneficiary has annual records, many claims, and many drug events. Claims have several code positions. Dates and amounts need parsing. Naive joins can inflate totals; careless models can use future information. The project practices the full path from source to defensible statement.

Why use DE-SynPUF? It gives realistic file structures and names without access to protected real claims. CMS explicitly positions the files for development and training while protecting beneficiary privacy [CMS SynPUF overview](https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-claims-synthetic-public-use-files). That makes it suitable for testing ingestion, joins, feature code, API routes, and reports. It is weak evidence for epidemiology, care management, or real-world prediction. The privacy treatment changes the joint distribution of variables. If an interviewer asks whether a synthetic AUROC can be deployed, the answer is no. External validation on appropriately governed real data would be required, along with a clearly defined use case and outcomes.

I chose a next-year high-cost label because it forces careful handling of time. It links a baseline year to the following year. It also creates a rare positive class of roughly ten percent by construction. This makes precision, ranking, and calibration more informative than accuracy alone. Yet “high cost” is an operational proxy. It is not a diagnosis, a measure of unmet need, or a direct patient benefit. High billed or paid amounts can reflect price, coverage, services, coding, and administrative processes. In my implementation, “total synthetic cost” is a specific sum of selected claim and prescription fields. It is not a validated comprehensive spending measure.

Professor Richesson studies data quality, standards, registries, and phenotyping [IHPI profile](https://ihpi.umich.edu/our-experts/richessr). My traceable pipeline is an entry point. I should be candid about the gap between working software and a research-grade phenotype.

## 04. Data and methodology

### Data sources and units

DE1.0 Sample 1 has the three beneficiary summary years, inpatient claims, outpatient claims, two carrier splits, and prescription drug events. A beneficiary summary row is annual. An inpatient or outpatient row is a claim. The carrier data contain professional claims and arrive in two source files. A prescription row is a drug event. The original files are linked through `DESYNPUF_ID`, standardized here as `beneficiary_id`. CMS provides the official file structure and user documentation [CMS Sample 1 downloads](https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-claims-synthetic-public-use-files/cms-2008-2010-data-entrepreneurs-synthetic-public-use-file-de-synpuf/de10-sample-1).

The loader discovers CSV, TXT, GZIP CSV, and ZIP inputs under `data/raw/`. It assigns a Bronze table from the file name. It normalizes header names to lowercase snake case and disambiguates repeated normalized names. DuckDB reads every source value as text with `all_varchar = true`. Each row gets `_source_file` and `_loaded_at`. The loader also writes `etl_load_log`. This design delays type decisions until the cleaning layer. It makes raw source values easier to inspect. It does not preserve byte-for-byte source files inside DuckDB; the source ZIP files remain separately on disk. See `src/ingest/load_raw_files.py`.

The loader uses `ignore_errors = true`, so malformed CSV rows may be skipped. The quality report does not reconcile each source count. For research use, I would log rejects and reconcile counts. ZIP extraction uses member basenames; a production loader should also check duplicate names and archive sizes.

### Cleaning assumptions

The Silver layer maps text to typed fields. `TRY_CAST` turns invalid numbers into null rather than stopping the whole build. Date parsing tries `%Y%m%d`, `%Y-%m-%d`, and `%m/%d/%Y`. Empty strings become null. A missing optional source column also becomes null. The chronic-condition normalizer maps `1`, `Y`, `YES`, and `TRUE` to one, and all other values to zero. This choice is simple, but it merges negative, missing, and unfamiliar codes. It could undercount burden if the CMS coding semantics differ. I must not describe these flags as clinically adjudicated disease status. The mapping is in `src/transform/common.py`, and the selected 11 flags are listed in `docs/data_dictionary.md`.

Claim year comes from the parsed claim start date. Prescription service year comes from the parsed service date. Age is calculated from birth date to December 31 of the beneficiary summary year. This is an approximate annual age, not age on every claim date. Claim payments come from `CLM_PMT_AMT`; prescription cost comes from `TOT_RX_CST_AMT`. These fields have different source semantics. Their sum is a project-defined feature, not a standardized total-cost definition. Beneficiary summary reimbursement fields are kept separately in Gold and are not added to that sum. This avoids an obvious double count, although it does not solve every cost-definition issue.

### Cohort and outcome definition

Gold starts with the union of person-year keys found in annual beneficiary data, claims, and prescription events. It keeps years 2008 through 2010. It left-joins beneficiary attributes and separate, pre-aggregated claim, prescription, diagnosis, and procedure summaries. Pre-aggregation matters. If I directly joined claims to drug events, a person with three claims and four drug events could create twelve rows. Counts and sums would be wrong. The Gold query creates one row per key and the quality check tests that grain. See `create_gold_patient_year_summary()` in `src/transform/common.py`.

The prediction table contains a row only when a synthetic beneficiary has both an input-year Gold record and a following-year Gold record. The target-year threshold is the 90th percentile of `total_synthetic_cost` among **all Gold person-years in that target year**. A target is one when that person's target-year cost is greater than or equal to the threshold. The use of `>=` means ties can yield slightly more than ten percent positive rows. The model sees features from year `t`; its label is based on year `t+1`. The 2008-to-2009 rows are training examples. The 2009-to-2010 rows are the held-out test examples. See `create_high_cost_prediction_dataset()` and `train_models()`.

The split is temporal, not person-disjoint: a person can occur in both periods. The code falls back to a random 75/25 row split if only one input year exists. The saved Sample 1 run used the temporal path. A publication study should fix the split in advance.

### Reproducible commands

The normal flow is `make ingest`, `make transform`, `make validate`, `make train`, `make explain`, and `make packet`. `make dashboard` launches Streamlit. The separate `make demo-all` path creates a tiny local fixture and runs a smoke workflow. `README.md` and `Makefile` show the commands. The tests and CI run the small demo because it is quick and has no dependency on the large raw CMS download. This reproducibility covers the software path. It is not a substitute for independent replication of a clinical finding.

## 05. Architecture and implementation

### Layered warehouse and table grains

Bronze retains source provenance; Silver exposes typed fields; Gold has declared analysis grains. Executed transformations are generated SQL in `src/transform/common.py`. The `sql/` files are not the sole executed pipeline. `src/transform/build_claims_mart.py` runs Silver and Gold in order.

| Layer | Actual table or group | Grain and purpose |
| --- | --- | --- |
| Bronze | `bronze_beneficiary_2008`, `_2009`, `_2010` | One imported beneficiary file row per source year. |
| Bronze | `bronze_inpatient_claims`, `bronze_outpatient_claims` | Imported claim rows with text fields and source provenance. |
| Bronze | `bronze_carrier_claims_a`, `_b` | The two carrier source splits. |
| Bronze | `bronze_prescription_drug_events` | Imported drug-event rows. |
| Silver | `silver_beneficiaries` | One annual beneficiary record as built; the Gold quality check enforces unique person-years after aggregation. |
| Silver | `silver_inpatient_claims`, `silver_outpatient_claims`, `silver_carrier_claims` | One cleaned source claim row; carrier splits are combined. |
| Silver | `silver_prescription_events` | One cleaned drug event. |
| Silver | `silver_diagnosis_codes`, `silver_procedure_codes` | One nonblank code occurrence at a claim position. |
| Gold | `gold_patient_year_summary` | One synthetic beneficiary-year with annual features. |
| Gold | `gold_patient_utilization_summary`, `gold_patient_cost_summary` | One aggregate row per year. |
| Gold | `gold_patient_chronic_condition_summary` | One aggregate row per year and condition. |
| Gold | `gold_high_cost_prediction_dataset` | One matched input year and next-year label per beneficiary. |

The Silver claim builder uses `DESYNPUF_ID` for the person and `CLM_ID` for a claim. It handles source-specific diagnosis and procedure positions. Inpatient and outpatient claims can have up to ten diagnosis positions and six ICD procedure positions in this implementation. Outpatient also has up to 45 HCPCS positions. Carrier rows use line-level diagnosis and HCPCS source fields, mapped into the shared claim shape. The long code tables unpivot nonblank positions with a `UNION ALL` over fields. The procedure table carries `procedure_system`, although the current `ICD9_OR_HCPCS` value is ambiguous for some mapped fields. A research-grade vocabulary layer should resolve code system and version more carefully. See `_create_silver_claims()`, `create_silver_diagnosis_codes()`, and `create_silver_procedure_codes()`.

Gold aggregates each source separately, then left-joins rollups to person-year keys. Activity counts and amounts default to zero. A claim-only person-year can have missing demographics. Without coverage context, zero claims and no captured claims are hard to distinguish.

The annual cost feature is:

```text
total_synthetic_cost = inpatient_total_paid
                     + outpatient_total_paid
                     + carrier_total_paid
                     + prescription_total_cost
```

This formula is implemented in `create_gold_patient_year_summary()`. It is a mixture of selected payment and drug-cost fields. I should say exactly that in an interview. Calling it “true total Medicare expenditure” would overstate the measure. The pipeline also stores beneficiary summary reimbursement fields, but those are separate columns and do not enter this formula.

### Feature set and model code

The 15 numeric fields cover age, chronic burden, utilization, costs, code breadth, and inpatient flags. Five categorical fields cover sex, race, state, county, and ESRD. Exact lists are in `src/models/train_high_cost_model.py`. All-null features are dropped. Numeric values use median imputation and scaling; categorical values use mode imputation and one-hot encoding. Preprocessing fits inside the training pipeline, reducing leakage from test-set preprocessing.

Logistic regression uses balanced weights and `max_iter=1000`. The random forest has 250 trees, minimum leaf size five, seed 42, and balanced subsample weights. Selection uses test-set AUPRC, which weakens the final test estimate. I should call it a diagnostic comparison. A stronger study would select on validation data and evaluate once on untouched data.

The target table contains future cost and threshold columns. An explicit feature allowlist excludes them, guarding against direct leakage. The model is saved with `joblib`; metrics, curves, comparison, and importance are saved as JSON and Markdown. Tree impurity importance and absolute logistic coefficients have different meanings; neither is causal.

### Quality, reporting, and interfaces

`src/quality/validate_warehouse.py` checks required Silver and Gold tables, required Gold columns, duplicate person-years, null person-year keys, allowed years, negative utilization counts, and label integrity. It counts negative payment adjustments as information. It fails if any annual cost component is below the configured extreme threshold of -5000. It also checks that the model table has rows, nonnull labels, next-year pairs, and at least one positive. A `pass` means those specific rules passed. It does not certify completeness, coding correctness, calibration, or clinical validity. See `docs/quality_checks.md`.

`src/api/main.py` exposes health, aggregate analytics, synthetic patient-year, explanation, model, and quality endpoints. It reads DuckDB in read-only mode and loads saved JSON. A database name starting with `demo_` selects demo artifacts. It has no production access controls or audit logging.

`dashboard/streamlit_app.py` reads the warehouse and reports. Pages cover overview, analytics, cohort exploration, model diagnostics, methodology, explanation, and quality. Altair renders charts. This is an inspection interface, not a validated decision workflow. `.gitignore` excludes raw files and generated artifacts.

`src/llm/patient_risk_explainer.py` makes deterministic text from cost, utilization thresholds, and condition flags, then adds a synthetic-data disclaimer. `src/llm/claims_summary_prompt.py` builds a guarded prompt. `explain_patient_year()` returns that prompt only in prompt-only mode; otherwise it uses rules. No LLM is called. See `docs/llm_explainer.md`.

### Tests and run path

The tests cover schema and feature functions, row counts, model training, quality checks, API behavior, explanation wording, and professor packet generation. The GitHub Actions workflow installs core dependencies, compiles code, runs the small demo warehouse, trains the demo models, produces demo explanations, and runs pytest. That is useful evidence that the demonstration can be exercised on a clean runner. The CI job does not run the large Sample 1 ingestion or independently verify all saved Sample 1 artifacts. See `.github/workflows/ci.yml`, `Makefile`, and `tests/`.

## 06. Evaluation and results

### What was evaluated

The quality report records 343,644 Gold patient-year rows and 227,292 matched modeling rows. The 2008, 2009, and 2010 beneficiary Bronze tables have 116,352, 114,538, and 112,754 rows. The Silver carrier table has 4,741,335 rows; the prescription table has 5,552,421. The report has overall status `pass`, zero duplicate Gold person-year grains, zero null Gold keys, and zero model rows with invalid next-year pairing. It also reports 228 person-years with some negative payment adjustment and zero with a component below -5000. These are saved local results in `data/processed/quality_report.json` and `docs/latest_quality_report.md`. The large row counts do not by themselves prove that every input row was parsed correctly.

The modeling report records 227,292 rows, with 114,538 training rows and 112,754 test rows. There are 22,754 positive labels across the modeling table, or about 10.01%. Because the threshold is computed within each target year, because ties can occur, and because the modeling table includes only linked consecutive-year people, the overall positive rate need not be exactly ten percent. The selected model is the random forest because its saved AUPRC is higher. See `data/processed/model_metrics.json`, `data/processed/model_comparison.json`, and `docs/latest_model_report.md`.

| Saved Sample 1 metric | Logistic regression | Random forest | How to say it |
| --- | ---: | ---: | --- |
| AUROC | 0.7432 | 0.7485 | Ranking across positive and negative synthetic labels. |
| AUPRC / average precision | 0.2515 | 0.2657 | Precision-recall summary; useful with a roughly 10% positive class. |
| F1 at 0.50 | 0.2909 | 0.3024 | Balance of precision and recall at a chosen cutoff. |
| Precision at 0.50 | 0.1862 | 0.2057 | Fraction of predicted positives that are positive labels. |
| Precision among top 10% scored rows | 0.2738 | 0.2917 | Yield if the highest-scored tenth is reviewed. |
| Brier score | 0.2168 | 0.1688 | Mean squared error of predicted probabilities; lower is better. |

These numbers are rounded from `data/processed/model_metrics.json` and `data/processed/model_comparison.json`. The comparison is descriptive. It has no confidence intervals, no independent external validation, and no claim of clinical utility. The code reports a “best F1 threshold” from a sweep on the test set. That threshold is an exploratory diagnostic, not a deployable operating point. The saved comparison table lists 0.64 for logistic regression and 0.60 for random forest. A threshold for a real service must be selected using a predefined objective and a validation set, then checked on a separate test set.

AUROC measures ranking of positive versus negative labels. AUPRC summarizes precision and recall and depends on prevalence. Top-ten-percent precision is the positive fraction among the highest-scored tenth. The random forest yields about 0.292 against a roughly 0.10 synthetic positive rate. This is not evidence of patient benefit. F1 omits true negatives, and a single Brier score cannot prove calibration. Saved JSON contains ROC, precision-recall, calibration, threshold, and confusion-matrix data.

The top saved random-forest importance features are diagnosis-code count, carrier-claim count, chronic count, total synthetic cost, and procedure-code count. Their approximate values are 0.132, 0.124, 0.102, 0.073, and 0.072 in `docs/latest_model_report.md`. Importance is not causality and can shift with correlated features.

### Demo fixture: a separate result

The demo has nine Gold person-years and six modeling pairs, split three and three. Its selected model is logistic regression. AUROC and AUPRC are `N/A` in the saved report; top-decile precision of 1.0 is meaningless with three test rows. See `docs/demo_model_report.md` and `data/processed/demo_model_metrics.json`. This fixture checks that software runs.

### What a stronger evaluation would add

A publishable study would define population, use case, outcome, coverage, and feature timing. It would assess completeness, coding, missingness, calibration, subgroup behavior, uncertainty, and external transport. A phenotype study also needs a defensible reference standard. These are proposed steps, not completed results.

## 07. Design decisions and alternatives

**Why DuckDB?** I wanted a local, reproducible analytical store for large flat files. DuckDB executes SQL over local data and supports a simple single-machine workflow. A server database such as PostgreSQL would make more sense for concurrent application writes, user management, and long-running services. Spark or a cloud warehouse would make more sense if scale or organization needs exceeded one machine. The current choice matches a portfolio prototype. It should not be presented as a universal architecture decision.

**Why Bronze, Silver, and Gold?** The layers make raw provenance, cleaning rules, and analysis grain easier to inspect. A single script could be shorter, but it would make it harder to separate source errors from feature errors. The Bronze layer stores all values as text. That avoids premature cast failures, although it pushes type validation later. The Gold layer enforces an explicit person-year target and pre-aggregates one-to-many sources. See `docs/architecture.md` and `src/transform/common.py`.

**Why dynamic optional columns?** CMS-like exports may vary. The cleaning helpers return null for an absent source field, allowing a build to continue. That is useful in a demo fixture. For rigorous research, silent absence is risky. A required-field contract should separate mandatory columns from optional ones, record null rates by source, and fail when a core column is missing. The current implementation only checks selected Gold columns after transformation.

**Why a patient-year unit?** Annual records align with the three beneficiary summary years and a next-year label. Annual units simplify the first model. They also hide within-year order. A claim in December and one in January are treated differently by calendar boundary, while claims within one year lose sequence. A future study may need a rolling 12-month lookback and a clearly defined index date. That would change features, eligibility, and censoring.

**Why the top ten percent outcome?** It gives an operational target that can be computed from the synthetic data without clinical adjudication. It also yields a clear class imbalance. Another target might be hospitalization, a condition-specific outcome, or a validated endpoint. Those would require a new definition and stronger validation. A high-cost target should not be confused with a medical phenotype or a measure of need.

**Why logistic regression and random forest?** Logistic regression is a readable baseline. Random forest can represent nonlinear interactions without manual interaction terms. Comparing them checks whether a more flexible model helps under the same broad feature set. The current comparison uses test-set AUPRC for selection, so the result is exploratory. A stronger design would reserve a validation period for selection and an untouched period for final reporting. More complex models are not automatically better, especially when labels and data semantics are uncertain.

**Why a rule-based explainer?** It is deterministic and easy to audit. It allows clear synthetic-data guardrails without sending data to an external model. Its wording can still overstate “drivers” because the listed conditions and thresholds are descriptive heuristics, not feature-level causal explanations. An LLM might improve fluency, but it would add hallucination, privacy, and evaluation problems. The prompt template is an integration starting point, not evidence that LLM generation has been tested.

## 08. Limitations and failures

### Data validity and measurement

The largest limitation is the source. CMS explicitly says DE-SynPUF variables have been imputed, suppressed, and coarsened, which sharply limits inference about real beneficiaries [CMS DE-SynPUF user manual](https://www.cms.gov/research-statistics-data-and-systems/downloadable-public-use-files/synpufs/downloads/synpuf_dug.pdf). A good result here can mean the code learned patterns in a synthetic construction. It cannot establish real-world effect size, fairness, clinical relevance, or transportability. The right interview phrase is: “I use it as a workflow test bed.”

Claims reflect billing and coverage, not a full clinical state. A condition code can be a billing signal rather than a confirmed diagnosis. No chart review validates the chronic-condition indicators. The implementation treats unfamiliar flag values as zero. Age is approximate. Drug cost and claim payments are combined under a project-specific definition. Some annual records may have missing demographic attributes. The code does not use enrollment months to require continuous observation. A zero claim count can therefore reflect no captured event or incomplete observation. These issues affect both features and the target.

The loader's `ignore_errors = true` may skip malformed CSV rows. The quality report counts resulting tables but does not compare them to an expected row count for every source file. Duplicate source claims are not systematically deduplicated by claim ID. The Gold person-year uniqueness check can pass even when duplicated claims inflate totals, because it checks the final key rather than input claim uniqueness. The long code tables preserve code positions but do not provide a fully governed vocabulary mapping. These are concrete engineering gaps, not merely generic cautions.

### Model validity and confounding

The model predicts next-year high synthetic cost from current-year cost and utilization. Those features may proxy for underlying health, benefit design, service access, coding intensity, provider practice, and administrative processing. The project cannot separate those effects. It does not claim causality. The label is relative to a year-specific distribution and is known only after the year ends. The train and test sets overlap in people across years. Model choice and best-F1 threshold are derived using the test set. There are no confidence intervals, external validation, or subgroup analyses. The saved Brier score alone does not settle calibration. These issues would have to be addressed before a rigorous performance claim.

The code does prevent direct use of future target columns by an explicit feature allowlist. That is a useful control, but a temporal audit would still ask when every field becomes available. Claims can be delayed or revised. In a real prospective workflow, even a current-year total may be unavailable at the decision date. The current project assumes a completed calendar year. It does not simulate claim runout or processing delays.

### Product and explanation validity

### How to discuss an error without sounding defensive

For a failure, state its effect, detection, and repair. If a CSV row is skipped, cost may be understated; reconcile source counts and log rejects. If unknown flags become zero, burden may be understated; check codebooks and preserve missingness. Do not claim these repairs are already implemented.

## 09. Technical Q&A

The answers below are written in first person so they can be rehearsed or retrieved by an AI agent. They are short on purpose. Add detail from Sections 04–08 when an interviewer asks for it. Every answer about performance refers to synthetic data.

### Basic questions

**B01. What is DE-SynPUF?**  
It is a public synthetic set of Medicare-style claims and beneficiary files from CMS. I use it to develop and test a pipeline. CMS warns that it has very limited value for inference about real beneficiaries.

**B02. What did you personally build?**  
I built the repository pipeline as the sole builder. It includes ingestion, transformations, quality checks, model training, reports, a dashboard, an API, and a rule-based explainer. I would describe any outside help only after confirming it separately.

**B03. What does one Gold row represent?**  
One synthetic beneficiary in one calendar year. It combines annual beneficiary attributes with separately aggregated claims, drug events, and code counts.

**B04. What do Bronze, Silver, and Gold mean?**  
Bronze preserves imported source values and provenance. Silver gives typed, cleaned records. Gold gives analysis tables with declared grains.

**B05. What is the prediction target?**  
For a synthetic person-year, I predict whether the same person's following-year project-defined total synthetic cost meets or exceeds that year's 90th percentile.

**B06. Is high cost a disease phenotype?**  
No. It is an operational cost label. It does not mean a person has a particular condition or needs an intervention.

**B07. Which two models did you compare?**  
Logistic regression and random forest. The first is a simple baseline. The second can represent nonlinear patterns.

**B08. What does the quality report prove?**  
It shows that the listed structural checks passed in the saved local run. It does not prove complete source ingestion or clinical validity.

**B09. Does the app call an LLM today?**  
No. The default explanation is deterministic and rule based. There is a prompt template for possible future use.

**B10. Why show a dashboard?**  
It makes aggregate tables, model diagnostics, and quality reports easier to inspect. It is a demonstration interface, not a care tool.

### Intermediate questions

**I01. How do you avoid multiplying claim rows?**  
I aggregate claims, drug events, and code tables separately by beneficiary-year. I join those small rollups to a unique person-year key set. Directly joining multiple one-to-many tables would multiply rows.

**I02. Where does claim year come from?**  
The Silver claim builder extracts the year from the parsed claim start date. Prescription year comes from the parsed service date.

**I03. What does your cost feature include?**  
It sums inpatient, outpatient, and carrier claim payment amounts plus prescription total drug cost. I call it `total_synthetic_cost` and explain that it is my project definition.

**I04. How do you encode chronic-condition flags?**  
I map a small set of affirmative text values to one and other values to zero. I know that this can collapse unknown and negative values, so I would revisit it for research use.

**I05. What is the temporal split?**  
The saved Sample 1 model trains on 2008 features for 2009 labels and tests on 2009 features for 2010 labels. The same person may occur in both periods.

**I06. How do you avoid direct target leakage?**  
The modeling code uses an explicit feature allowlist. It excludes target-year cost, target threshold, target year, and label columns from `X`.

**I07. Why not use accuracy?**  
Only about one tenth of rows are positive. A classifier that predicts everyone negative could look accurate while finding no positives.

**I08. How is precision at ten percent computed?**  
I sort test rows by model score, select the top ceiling of ten percent, and calculate the positive-label fraction among them. It is a ranking metric, not a treatment effect.

**I09. What does the model comparison select?**  
It selects the higher AUPRC on the test set. That makes the comparison exploratory because I used test data for model choice.

**I10. How does the API use saved artifacts?**  
It reads the DuckDB database in read-only mode and loads model and quality JSON files. It switches to demo artifacts when the database filename begins with `demo_`.

### Advanced questions

**A01. What is the exact denominator for your 90th-percentile threshold?**  
The threshold uses every Gold person-year in a target calendar year. The modeling table then keeps only people linked to the prior year. That difference can change positive prevalence in modeling rows.

**A02. Is your test set person independent?**  
No. It is later in time, but one synthetic person can have both a training pair and a test pair. A person-disjoint or external-site evaluation would answer a different question.

**A03. How would you design a cleaner prospective split?**  
I would choose a fixed decision date, define feature availability and claim runout, reserve validation time for tuning, and test once on a later untouched period. I would report uncertainty and subgroup results.

**A04. What is the difference between discrimination and calibration?**  
Discrimination asks whether positives tend to rank above negatives. Calibration asks whether predicted probabilities match observed frequencies. A model can do one well and the other poorly.

**A05. What is wrong with choosing the best F1 threshold from the test set?**  
It uses the held-out labels to tune a decision rule. The resulting threshold performance is optimistic for a new sample. I would tune on validation data and report final test results once.

**A06. Is random-forest feature importance causal?**  
No. It reports how much features reduced tree impurity. Correlated or high-cardinality features can affect the ranking. It cannot show the effect of changing a clinical variable.

**A07. How would you validate a computable phenotype?**  
I would first specify its purpose, population, data sources, logic, and time window. Then I would compare output with an appropriate reference standard, report sensitivity and positive predictive value with uncertainty, and study site and subgroup differences. This repository does not do that.

**A08. How would you test data fitness for use?**  
I would measure completeness, conformance, plausibility, and temporal stability for the variables needed by the question. I would also check source lineage, code semantics, coverage, and whether missingness differs across sites or groups.

**A09. How does a code-count feature differ from a diagnosis phenotype?**  
Code count measures diversity of recorded codes. A phenotype needs a defined clinical concept and logic to identify it, often with timing and validation. A high code count can reflect utilization or coding intensity.

**A10. What would portability require?**  
I would specify concepts and code sets, versions, data mappings, eligibility, and validation results. I would test the same definition across sites and document local adaptations. A SQL query alone is not enough.

### Adversarial questions

**D01. Your data are synthetic. Why should I care about the model score?**  
The score is useful as a software diagnostic. It shows that the evaluation path runs and exposes issues such as split design and metric choice. I would not use it as evidence about real people. The stronger contribution here is the traceable pipeline and an honest account of its limits.

**D02. Are you claiming you built a clinically valid risk model?**  
No. I built a demonstration classifier for a synthetic, project-defined cost label. Clinical use would require a specific decision context, real-data validation, calibration, subgroup analysis, governance, and evidence of benefit.

**D03. Why call it an LLM explainer if no model is called?**  
The repository has an LLM-oriented prompt module, but the current default output is rule based. I would name it accurately in an interview. The prompt is a future integration point, not a completed LLM evaluation.

**D04. Your quality report says PASS. Can rows still be missing?**  
Yes. It checks specific downstream properties. The CSV loader can ignore parse errors, and the report does not reconcile every expected source row. A pass is conditional on those checks.

**D05. Could duplicated claims inflate spending while Gold grain still passes?**  
Yes. The Gold table can have one row per person-year even if duplicate claim rows were aggregated into that row. I would add claim-ID and source-file duplicate checks.

**D06. Why is your selected model's score potentially optimistic?**  
I chose the model using the test-set AUPRC. That reuses held-out data for selection. I would add a validation set and keep a final test period untouched.

**D07. Do chronic-condition flags equal confirmed clinical diagnoses?**  
No. They are source indicators normalized by my code. I have not validated them against charts or clinical adjudication.

**D08. Could your model encode inequity?**  
Yes, if applied to real data. Claims reflect access, coverage, billing, and coding. My synthetic run cannot establish fairness. A real study would test group-specific measurement, calibration, error rates, and the effects of acting on predictions.

**D09. Why not just use a common data model?**  
A common data model could improve portability and standard field definitions. I chose a small local schema to learn the source and build an end-to-end prototype. A research extension should map the source to a governed model and test information loss.

**D10. What if a professor asks for a finding about Medicare patients?**  
I would say this project cannot support that finding. I can describe synthetic table patterns and code behavior. I would need an approved real-data study to make a claim about Medicare patients.

## 10. Research relevance to Professor Richesson

Professor Richesson's University of Michigan profile describes work on the quality and usability of EHR data for research, data standards, patient registries, and pragmatic trials [IHPI profile](https://ihpi.umich.edu/our-experts/richessr). Her faculty page also lists current publications and mentoring information [Michigan Medical School faculty page](https://medschool.umich.edu/profile/7125/rachel-richesson). I should use her current Michigan affiliation. Older papers list Duke because that was her affiliation when those papers were written. I should not describe her as currently based at Duke.

Her 2016 paper with Smerek and Cameron argues that phenotype definitions need sharing infrastructure and information about whether they fit a new purpose [2016 framework paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC4975566/). A 2026 paper from the NIH Pragmatic Trials Collaboratory emphasizes reporting a phenotype's purpose, data types and sources, validation, and modifications across sites [Conte and colleagues, 2026](https://academic.oup.com/jamiaopen/article/9/4/ooag158/8752922). These are useful anchors for an interview. I should not pretend that my cost label is already one of those validated EHR phenotypes.

My honest connection is methodological. The pipeline makes source-to-feature logic visible. It separates a data quality check from a model result. It exposes how a cohort definition and time window change the analysis. Those are habits that support research on computable definitions. Yet this repository is claims only. EHR-based phenotyping can use labs, observations, medications, notes, and clinical workflows. My project lacks those modalities, site mappings, clinical adjudication, and evidence that the same definition works elsewhere. That gap is an opportunity for doctoral training, not a completed contribution.

One possible research direction is to turn a claims-oriented indicator into a documented computable phenotype candidate. I would state its purpose, code systems, inclusion and exclusion rules, time window, and expected data availability. I would compare candidate definitions against a defensible clinical reference, quantify uncertainty, and study changes across sites. Another direction is to create a data-fitness report for each phenotype. It could report missingness, code coverage, unexpected value distributions, temporal shifts, and local mapping differences before the phenotype is reused. These are **proposals**. They should be discussed as questions to explore with a mentor, not as promises that this project already supports multi-site research.

I can also connect this work to pragmatic trials carefully. A trial may need computable definitions for eligibility, outcomes, and safety events. The usefulness of a definition depends on where and why it is used. A model that ranks synthetic cost does not answer those trial questions. But the disciplined steps of specifying the data source, population, timing, and validation are directly relevant. An earlier Richesson-led perspective discusses phenotyping, standards, and data quality when EHR data support pragmatic trials [Richesson and colleagues, 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3861929/).

### Questions I can ask Professor Richesson

1. When a phenotype is reused across sites, which documentation gap most often causes trouble: the clinical concept, code mapping, time window, or validation evidence?
2. What minimum data-quality evidence would make a claims or EHR phenotype worth testing at a second site?
3. How do your teams decide when a common definition needs a local adaptation, and how do they report that change?
4. For a doctoral student starting from an engineering prototype, what would be a strong first validation study?
5. Which outcomes in pragmatic trials are most difficult to capture reliably from routinely collected data, and why?
6. Where could an automated data-fitness report save investigators time without giving false reassurance?
7. What kinds of negative results or failed transport attempts are most valuable to publish in phenotyping research?
8. How would you balance reusable standards with the local clinical context needed to interpret a code or data field?

These are conversation questions, not claims about her current projects. Listen to the answer and follow its terms. Do not assume she wants to supervise this exact repository or that a specific dataset is available.

## 11. Interview interruptions, follow-ups, and counterquestions

An interview can interrupt the prepared story. The goal is to answer the question first, then return to the core point. Use a short bridge: “The direct answer is …”; then give one example; then name the limit. Do not recite the two-minute script when asked a narrow question.

**Interrupt: “What exactly is the unit of analysis?”**  
> A synthetic beneficiary-year. Each Gold row combines annual attributes and separately aggregated events for that year. The prediction row links that unit to the same beneficiary in the next year.

**Interrupt: “Where does the 90th percentile come from?”**  
> From all Gold person-years in each target year. It is calculated within the database before the input and target years are paired. It is a relative synthetic-cost threshold.

**Interrupt: “Give me a concrete leakage example.”**  
> If I used `target_total_synthetic_cost` as a feature, the model would see the answer. The modeling code excludes it with a feature allowlist. A subtler risk is a feature whose claim arrives only after the intended prediction date.

**Interrupt: “What does 0.748 AUROC mean?”**  
> It is discrimination against my synthetic cost label on the saved later-year test rows. It is not a clinical performance estimate. I would also look at precision-recall and calibration.

**Interrupt: “Why should I trust the PASS report?”**  
> You should trust it only for the checks it runs: table presence, Gold grain and keys, year range, selected numeric rules, and label pairing. It does not yet reconcile every source row or validate clinical semantics.

**Interrupt: “What would you improve first?”**  
> I would strengthen input reconciliation and definition metadata before adding a more complex model. That would make the data path and the outcome easier to trust.

**Interrupt: “How is this related to computable phenotypes?”**  
> It is related through explicit definitions, provenance, and quality checks. My current target is a cost label, not a validated clinical phenotype. I want to learn how to make such definitions fit for research and portable.

**Interrupt: “What if I disagree with your cost definition?”**  
> I would welcome that challenge. I can show the exact four terms in the formula. Then I would revise the measure for the intended use, document the change, and rerun the evaluation.

**Interrupt: “Why do your two models have different Brier scores?”**  
> They output different probabilities, and Brier score measures squared probability error. Class weighting and model structure can affect calibration. I would inspect the calibration plots and compare baselines rather than infer a clinical meaning from the difference.

**Interrupt: “Is a negative payment an error?”**  
> Not always. Adjustments and reversals can create negative values. My validator counts them as information and fails only on an extreme threshold. A research workflow should inspect source semantics and document its correction policy.

**Interrupt: “Show me where this is implemented.”**  
> I would start at `Makefile`, then show `src/ingest/load_raw_files.py`, `src/transform/common.py`, `src/quality/validate_warehouse.py`, and `src/models/train_high_cost_model.py`. For a number, I would open the saved JSON report.

**Interrupt: “Would you deploy this?”**  
> No. I would first need a real use case, lawful data access, a validated target, prospective data timing, external evaluation, governance, and evidence that acting on predictions helps rather than harms.

### Counterquestions that deepen a technical discussion

If the professor challenges portability, ask: “Would you treat code mapping, local data completeness, or reference-standard choice as the main first constraint?” If she challenges the outcome, ask: “For a first methods study, would a simpler adjudicated event be more informative than a broad cost proxy?” If she challenges data quality, ask: “Which quality dimensions should be checked before a phenotype is run, and which must be checked after seeing its output?” These questions seek guidance. They do not put words in her mouth.

### If I do not know an answer

> I do not know that from this dataset or the current code. I can show the exact definition I used. To answer your question, I would check the source documentation, design a validation analysis, and report the result with its limits.

That is better than inventing a result. The interviewer may value the boundary between evidence and inference more than a quick but unsupported answer.

## 12. Evidence and verification

### Local evidence ledger

| Claim an agent may make | Source | Status and limits |
| --- | --- | --- |
| I built a CMS DE-SynPUF Sample 1 claims pipeline. | `README.md`; `src/ingest/load_raw_files.py`; `src/transform/common.py` | Implemented. Sole-builder role is owner-confirmed, not proven by code history alone. |
| There are eight expected source files. | `data/raw/cms_sample_1/`; CMS Sample 1 downloads | Observed locally and confirmed by CMS. |
| Bronze imports source values as text and keeps file provenance. | `src/ingest/load_raw_files.py` | Implemented. CSV parse errors can be ignored. |
| Silver standardizes dates, amounts, IDs, flags, and code positions. | `src/transform/common.py` | Implemented. Flag semantics need stricter validation for research. |
| Gold has one row per beneficiary-year in the saved run. | `src/transform/common.py`; `data/processed/quality_report.json` | Implemented query and observed zero duplicate-key failures. |
| Total synthetic cost is a four-term sum. | `src/transform/common.py` | Implemented project definition; not a validated spending measure. |
| Next-year high cost uses target-year 90th percentile. | `src/transform/common.py` | Implemented. Ties and cohort selection affect prevalence. |
| The saved Sample 1 model used 227,292 rows. | `data/processed/model_metrics.json`; `docs/latest_model_report.md` | Observed local artifact. Not a real-patient result. |
| The selected random forest has AUROC 0.7485 and AUPRC 0.2657. | `data/processed/model_metrics.json`; `docs/latest_model_report.md` | Observed synthetic test result; rounded. Test set also used for model choice. |
| The saved Sample 1 warehouse quality status is pass. | `data/processed/quality_report.json`; `docs/latest_quality_report.md` | Observed for listed checks only. |
| The demo has six modeling rows. | `data/processed/demo_model_metrics.json`; `docs/demo_model_report.md` | Observed fixture result; only a smoke test. |
| The API and dashboard expose saved summaries. | `src/api/main.py`; `dashboard/streamlit_app.py` | Implemented as local demonstration surfaces. |
| Default explanations are rule based; an LLM prompt exists. | `src/llm/patient_risk_explainer.py`; `src/llm/claims_summary_prompt.py` | Implemented. No LLM model call or evaluation. |
| The current working tree has uncommitted edits. | `git status --short` at review time | Observed on 2026-11-01. Recheck before the interview. |
| The owner is the sole builder. | Owner's answer during preparation | Owner-confirmed. Personal history and other contributions still need owner confirmation if discussed. |

### External sources and how they are used

- [CMS SynPUF overview](https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-claims-synthetic-public-use-files): why the files exist and why they should not be used for inference about real beneficiaries.
- [CMS Sample 1 download page](https://www.cms.gov/data-research/statistics-trends-and-reports/medicare-claims-synthetic-public-use-files/cms-2008-2010-data-entrepreneurs-synthetic-public-use-file-de-synpuf/de10-sample-1): official file count and source categories.
- [CMS DE-SynPUF user manual](https://www.cms.gov/research-statistics-data-and-systems/downloadable-public-use-files/synpufs/downloads/synpuf_dug.pdf): source semantics and synthetic-data limitations. Recheck field-level meanings before extending the cost measure.
- [University of Michigan IHPI profile](https://ihpi.umich.edu/our-experts/richessr) and [Medical School faculty page](https://medschool.umich.edu/profile/7125/rachel-richesson): current affiliation and described research interests.
- [Richesson, Smerek, and Cameron, 2016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4975566/): first-party publication on sharing and reuse of computable phenotype definitions.
- [Richesson and colleagues, 2013](https://pmc.ncbi.nlm.nih.gov/articles/PMC3861929/): first-party perspective on EHR phenotyping, standards, and data quality in pragmatic trials.
- [Conte and colleagues, 2026](https://academic.oup.com/jamiaopen/article/9/4/ooag158/8752922): first-party publication on documenting phenotype purpose, sources, validation, and site adaptation.

The Google Scholar profile supplied for this preparation was inaccessible through the research tool. I used the university pages and primary publications instead. Do not invent a publication rank, citation count, active grant, or current lab project from that inaccessible profile. If the interview depends on a very recent paper, recheck the faculty page and the actual paper before naming it.

### Claims requiring personal confirmation before speaking

The repository cannot establish why the owner first chose this topic, how long the work took, whether anyone gave advice, which bugs were hardest, or which parts were written in what order. The owner confirmed sole-builder status, but should personally verify any story about motivation, setbacks, collaborators, or career goals. The exact local metrics should be refreshed if code or data change. The current report is a snapshot. It is not a permanent benchmark.

### Final answer rule

When a question asks what I did, answer with the implementation and an evidence path. When it asks what I found, answer with the saved synthetic result and its limit. When it asks what I would study with Professor Richesson, answer with a specific validation or data-quality question and label it as proposed. That three-part distinction is the safest way to use this guide in a serious PhD interview.
