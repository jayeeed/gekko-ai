# PhD interview preparation: MIMIC-IV Clinical Data Warehouse

**Audience:** the project builder, an interviewer, or an AI agent preparing answers.  
**Interview context:** a prospective conversation with Professor Rachel L. Richesson.  
**Evidence checked:** 2026-11-01.  
**Speaking voice:** first person. The project builder confirmed that they were the sole builder.  

> **The one sentence to keep accurate:** I built a reproducible EHR data engineering and research methods platform. Its published experiments use invented data. I have not shown that its models work on real patients.

## How to use this module

Read Sections 1 and 2 before a short conversation. Use Sections 3 through 8 when the interviewer asks how the system works or challenges a result. Use Sections 9 and 11 to practice aloud. Use Section 12 to check any claim before repeating it. An AI agent should answer from the most specific section, cite the linked repository evidence, and state the limit of the evidence. It should never turn a synthetic score into a clinical claim.

This document separates **three different data situations**. The six-patient local seed is a software smoke test. The 1,000-patient research workshop is a larger invented teaching dataset. The registered 24-hour ICU mortality study is a narrower experiment built from the invented research source. The openly available MIMIC-IV demo contains real deidentified records from 100 patients, but it is a separate possible input. Full MIMIC-IV requires credentialed access. These situations must not be blended in an interview. See the [PhysioNet demo description](https://physionet.org/content/mimic-iv-demo/2.2/) and the [MIMIC-IV v3.1 description](https://physionet.org/content/mimiciv/3.1/).

---

## 01. Project identity

### What I built

I built a local clinical data warehouse and a connected synthetic research platform. The warehouse ingests MIMIC-IV shaped hospital and ICU tables. It turns source tables into cleaned tables and then into analysis tables. It includes validation, cohort definitions, feature creation, an aggregate dashboard, an API, and a guarded natural language query path. The research extension adds a versioned study contract, a time-aware ICU cohort, model evaluation, quality scenarios, and aggregate publication packages. The repository's [README](../README.md) gives the system overview. The [architecture document](03_architecture.md) describes the layers. The [research blueprint](11_trustworthy_research_platform_blueprint.md) records the implemented synthetic path and its roadmap.

The central engineering question is: **Can I make the path from a source EHR-like record to a research answer inspectable and repeatable?** That requires more than a model. I need to define the population, the time at which a prediction would be made, the data that would actually be known at that time, the target, the split, and the checks that could stop a bad run. I also need to know where each value came from. A model score alone cannot answer those questions.

I was the sole builder. In an interview I can say, “I designed and implemented the pipeline, the synthetic study workflow, and its checks.” I should then name the precise part under discussion. I should not imply that I collected clinical data, established a validated phenotype, conducted a real-world clinical study, or obtained a finding on full MIMIC-IV. My authorship is a personal statement confirmed for this document. The repository can show the implementation, but it cannot independently prove who wrote each line.

The declared warehouse scope is implemented for demo, full-local, and LocalStack paths. The configuration and command surfaces are in [`src/cli.py`](../src/cli.py), the [`Makefile`](../Makefile), and `configs/`. BigQuery is a metadata scaffold, not a live query execution path. Full-local support means that a credentialed user can supply files and run the pipeline. It does not mean this public repository contains restricted MIMIC-IV data or a validated full-data result. The synthetic research extension is an educational simulation. The [limitations document](08_limitations_and_ethics.md) explicitly rules out clinical use.

### The evidence ladder

I should use five labels when I describe evidence. **Implemented** means a code path exists. **Tested** means a test exercised that behavior on its fixture. **Observed locally** means a local run produced an output. **Published artifact** means an aggregate file was copied into the public output folder. **Clinically validated** would mean a properly designed real-data study with suitable external checks. The last label does not apply to this project. A unit test of a time predicate is useful evidence for the predicate, but it cannot establish that a mortality model is useful in practice.

The current test run on 2026-11-01 was `23 passed in 5.98s` with `.venv/bin/pytest -q tests`. This proves that the current suite passed in this workspace at that time. It does not prove that all behavior is correct. The stored [`validation_report.md`](../outputs/private/validation_report.md) says 20 passed, zero failed, and zero warnings. It was generated on 2026-05-27, so it is historical validation evidence. It is not a fresh validation of the current checkout. The tiny counts in that report are six patients, seven admissions, and seven ICU stays in the local synthetic seed.

### One-line identity answer

> “I built a reproducible MIMIC-IV shaped warehouse and an invented-data research platform to study how cohort definitions, data availability, and data quality affect an ICU prediction workflow. The work demonstrates engineering and research design; it does not establish a clinical finding.”

## 02. Interview explanations

### Two-minute version

> “I built this project because EHR data can look ready for modeling before the research question is actually defined. A row may have a lab value, but that result may have become available after the time at which the model is supposed to predict. A diagnosis code may be entered after discharge. A patient may have several ICU stays. If I join all of those fields without a time contract, I can get a convincing score from information that was unavailable in practice.
>
> I first built a local warehouse for MIMIC-IV shaped hospital and ICU data. Bronze holds source-like tables with provenance. Silver cleans keys, dates, and clinical entities. Gold creates analysis tables for patients, admissions, ICU stays, and first-24-hour features. The CLI, dashboard, API, and validation checks use those tables. The repository accepts an open demo layout, credentialed local files, or a LocalStack S3 layout. The public project contains no restricted MIMIC-IV records.
>
> I then added an isolated invented-data research workshop and a registered ICU mortality study. The study chooses each adult patient's first ICU stay. It predicts 24 hours after ICU entry. A measurement is eligible only if it was recorded in that first day and was available by prediction time. Patients who died or left the ICU before that time are excluded. The outcome is death after prediction time and by hospital discharge. I split by patient, fit preprocessing on training data, report discrimination and calibration, and test quality failures such as delayed labs and duplicate keys.
>
> The important result is methodological. The system can show exactly which rows and measurements enter the study. Its synthetic model scores are weak and unstable. That is useful evidence of a working evaluation path, not clinical performance. Professor Richesson's work on data quality, phenotype definitions, provenance, and fitness for use is directly relevant. I would like to learn how to make these checks valid across real sites and research questions.”

This is a script, not a claim that the model is ready for patients. Speak slowly. If interrupted, stop at the end of the current sentence and answer the specific challenge. Do not try to finish a memorized speech while the interviewer is asking about a denominator or a definition.

### Thirty-second version

> “I built a local EHR warehouse and a synthetic ICU research workflow. My main focus was traceability: where a field came from, whether it was known at prediction time, and who entered the cohort. I used an invented dataset to exercise the workflow and expose errors. The result is a reproducible methods demonstration. I have not validated a clinical prediction model.”

### One concrete example

Suppose a creatinine sample was taken 10 hours after ICU entry. The lab result was stored 26 hours after ICU entry. The model predicts at hour 24. My prospective study excludes that result. The sample time fits the first 24 hours, but the value was not known when the prediction would be made. The relevant predicate is implemented in [`src/research/features.py`](../src/research/features.py). The count of timing reasons is produced by [`src/research/timing.py`](../src/research/timing.py). This example is a hypothetical explanation of the rule, not a patient record.

## 03. Problem and motivation

EHRs are built for care and operations. Research asks different questions. The meaning of a field depends on how and when it was recorded. A lab count may reflect severity, clinician concern, or hospital workflow. A missing lab can mean that no test was ordered, the result arrived later, or a data feed failed. A diagnosis code can describe a discharge conclusion rather than knowledge available when a bedside prediction was needed. Those differences can change both the study population and the measured model performance.

The project addresses two linked problems. The first is **data engineering**: source files vary, optional tables may be absent, IDs and time columns need consistent treatment, and analysts need stable tables at a known grain. The second is **research specification**: a cohort and feature set must be tied to an index time, an observation window, and an outcome window. A clean warehouse does not by itself solve the second problem. The registered study service exists to make that contract explicit. See [`configs/studies/icu_mortality_24h.yaml`](../configs/studies/icu_mortality_24h.yaml) and the [cohort time contract](12_cohort_time_contract.md).

This matters because a technically valid SQL join can still be scientifically wrong. Consider a patient who has two ICU stays. If I first filter stays to those with complete labs and then select the “first” stay, I may silently select the second stay. That changes the research question. In this project, the rank is assigned before the age, care-unit, and prediction-time filters. The code chooses the first-ever ICU stay per patient, with `stay_id` breaking a tie. Later stays cannot replace an ineligible first stay. This rule is in [`src/research/cohorts.py`](../src/research/cohorts.py).

The broader motivation matches the research problems Professor Richesson has described. Her [work on clinical research informatics and EHR data](https://pubmed.ncbi.nlm.nih.gov/25123746/) discusses quality, completeness, provenance, explicit phenotype definitions, and governance. Her [fitness-for-use study](https://pubmed.ncbi.nlm.nih.gov/35171985/) emphasizes assessing data quality for a specific research purpose early enough to affect design. The [NIH Pragmatic Trials Collaboratory's phenotype guidance](https://rethinkingclinicaltrials.org/chapters/conduct/electronic-health-records-based-phenotyping/evaluating-phenotype-definitions/) stresses explicit and reproducible definitions. My project is a small engineering demonstration of these concerns. It is not a reproduction of her studies or a claim that the same conclusions have been tested here.

The most useful research question for a future PhD is therefore not “Can I get a higher synthetic AUROC?” It is closer to: **How can we measure whether time-aware EHR data and phenotype definitions are fit for a stated research use, especially when data collection differs across sites?** That is a proposed direction, not a result from this repository.

## 04. Data and methodology

### Four inputs that must remain separate

| Input | What it is | What I can safely claim |
| --- | --- | --- |
| Small local seed | Six invented patients created by [`src/ingest/seed_synthetic.py`](../src/ingest/seed_synthetic.py) | It exercises ingestion, transformations, reports, dashboard, and tests. Its counts are not research estimates. |
| Research workshop | Normally 1,000 invented patients from [`src/research/seed.py`](../src/research/seed.py), using `configs/research_synthetic.duckdb.yaml` | It exercises four teaching tasks and evaluation code. Its patterns are arbitrary and do not reproduce a real hospital distribution. |
| Open MIMIC-IV demo | A separate public 100-patient subset described by [PhysioNet](https://physionet.org/content/mimic-iv-demo/2.2/) | The code supports its layout. The stored synthetic results are not results on this demo. |
| Full MIMIC-IV v3.1 | Credentialed deidentified EHR dataset described by [PhysioNet](https://physionet.org/content/mimiciv/3.1/) | The full-local ingestion path exists. This public document has no full-data result to report. |

The LocalStack path is a **storage mode**, not a fifth scientific population. It reads MIMIC-style objects from a configured S3 endpoint. A bucket can contain invented files or other allowed inputs. The scientific status of a result depends on the actual data and its permissions, not on whether a file came from S3 or a local directory. The LocalStack loader and preflight are in [`src/ingest/load_localstack_s3.py`](../src/ingest/load_localstack_s3.py) and [`src/ingest/check_localstack.py`](../src/ingest/check_localstack.py).

### The registered study population

The flagship study is intentionally narrow. It begins at ICU stay grain. It ranks ICU stays within each patient by entry time and `stay_id`. It keeps rank one, requires adult age, optionally filters care unit, and requires the person to remain in the ICU and alive at the 24-hour prediction time. The row is one first ICU stay for one patient. The outcome is positive when death occurs **strictly after** prediction time and **on or before** hospital discharge. The outcome is `death_after_prediction_flag`. A death at or before prediction time makes the patient ineligible. This is a conditional prediction among those still alive and in ICU at hour 24. It is not an admission-time model and is not a whole-hospital mortality estimate. The executable definitions are in [`src/research/cohorts.py`](../src/research/cohorts.py), [`src/research/features.py`](../src/research/features.py), and [`src/research/tasks.py`](../src/research/tasks.py).

The time line is compact:

```text
ICU entry (t0) ---- observations in [t0, t0 + 24h) ---- prediction at t0 + 24h ---- outcome through hospital discharge
```

For chart and lab measurements, `charttime` must be at or after ICU entry and before prediction time. `storetime` must be present, no earlier than `charttime`, and no later than prediction time. For input events, `starttime` is the event time and `storetime` is the availability time. The half-open event interval avoids including an event first recorded at the prediction instant. An unknown availability time causes exclusion. A late result causes exclusion even if its sample was taken early. The care-unit filter is applied to the selected first stay. These are software rules, not proof that real EHR timestamps always reflect what a clinician knew.

The predictor allowlist includes age at admission, selected mean vital signs, selected mean laboratory values, first-day chart and lab event counts, a norepinephrine proxy, gender, admission type, and first care unit. The exact task contract is in [`src/research/tasks.py`](../src/research/tasks.py); the registry adds provenance and timing metadata in [`configs/research/prospective_feature_registry.yaml`](../configs/research/prospective_feature_registry.yaml). The model does not use identifiers, discharge outcomes, whole-stay summaries, diagnosis codes, procedure codes, or a site identifier as predictors. Those exclusions reduce obvious leakage. They do not guarantee absence of all clinical or workflow bias.

The broader research workshop has a different grain and different tasks. Its row is the first hospital admission per invented patient. It compares hospital length of stay, in-hospital death, urgent readmission within 30 days after discharge, and a small primary diagnosis class. The workshop can use some transparent diagnosis and intervention proxies for teaching. Those fields are **not** part of the narrower prospective ICU mortality allowlist. Confusing the two feature sets would be a serious interview error. The workshop's [method document](10_synthetic_research_workshop.md), [`src/research/evaluate.py`](../src/research/evaluate.py), and feature definitions in `configs/research/` state its rules.

### Methodological assumptions

The invented generator uses deterministic patterns and a seed. It does not learn a distribution from MIMIC-IV. Its fixed codes and simulated measurements exist to test software behavior. One first ICU stay per patient also means a patient-level split is easy to inspect. This is a convenient teaching case. A real multi-admission study would need stronger grouping checks and a clinical review of index events. The code uses patient-level assignment in the registered study; it does not claim that random splitting alone makes a result transportable. See [`src/research/study_service.py`](../src/research/study_service.py).

The study's target also depends on the quality of `deathtime` and `dischtime`. If a real source recorded those fields inconsistently, the label could be wrong. The current synthetic generator controls them. That makes the exercise reproducible, but it hides many real-world failure modes. A real study would need endpoint adjudication or an evidence-based operational definition, site-specific checks, and a plan for incomplete follow-up.

## 05. Architecture and implementation

### End-to-end data flow

```text
CSV / CSV.GZ or LocalStack S3 objects
  -> ingestion and typed Bronze tables
  -> cleaned Silver patients, admissions, ICU stays, events
  -> Gold summaries and feature marts
  -> validation, reports, dashboard, API, aggregate query assistant
  -> isolated synthetic research study service and aggregate package
```

The command entry point is [`src/cli.py`](../src/cli.py). The `run-all` command ingests, builds through Gold, validates, and reports. The `Makefile` provides short commands. The configured mode determines which loader is called. Local files go through the demo or full-local loader. LocalStack objects go through the S3 loader. BigQuery execution is outside this build; its module collects metadata only. This matters if I am asked whether the project is “cloud deployed.” The honest answer is that it has a LocalStack cloud-style ingestion path, not a production cloud service.

Bronze keeps a source-like shape and provenance fields such as `source_file`, `loaded_at`, `source_module`, and `pipeline_run_id`. It also creates typed placeholders when expected optional inputs are absent. That makes engineering smoke tests possible. It does **not** mean missing source data were observed to have zero events. A placeholder is a known absence of an input file and should be treated as such in research. Bronze creation is in [`src/transform/build_bronze.py`](../src/transform/build_bronze.py) and `sql/bronze/`.

Silver normalizes core entities and event streams. It standardizes IDs, timestamps, and useful derived fields. Tables include patients, admissions, ICU stays, labs, chart events, diagnoses, medications, procedures, services, transfers, and other event types. The build code is [`src/transform/build_silver.py`](../src/transform/build_silver.py); SQL definitions are under `sql/silver/`. The key scientific benefit is a consistent join surface. The danger is that cleaning or deduplication can hide source defects. The research quality checks therefore inspect Bronze source keys before Silver deduplication can mask duplicate admissions or ICU stays. See [`src/validation/validate_research_quality.py`](../src/validation/validate_research_quality.py).

Gold holds analysis-oriented tables. The standard marts cover patient, admission, and ICU-stay summaries; first-24-hour features; lab, vital, diagnosis, and medication aggregates; and a mortality baseline table. The SQL is under `sql/gold/`, with orchestration in [`src/transform/build_gold.py`](../src/transform/build_gold.py). The standard first-24-hour feature mart uses event-time filtering. The registered prospective study adds an explicit **availability-time** check and a narrower task-specific allowlist. I should not describe the standard Gold feature mart and the registered study table as identical. The latter is materialized as `gold_research_prospective_icu_24h` by [`src/research/features.py`](../src/research/features.py).

The study specification is YAML, not a free-form prompt. [`src/research/contracts.py`](../src/research/contracts.py) parses it into a typed `StudySpec` and rejects unsupported choices. The supported task is a first-ICU-stay, 24-hour, invented-data mortality study. The spec includes the cohort, prediction time, feature registry, split proportions, seed, and publication settings. A hash of the canonical definition is included in a run manifest. This makes a run easier to identify. It does not by itself prove that source contents are unchanged. In particular, the code's `dataset_snapshot` hashes a sorted list of Silver table **names**, not the table rows. I must not call it a full data-content fingerprint. Source hashes used in the paired scenario comparison cover that separate comparison path. See [`src/research/study_service.py`](../src/research/study_service.py) and [`src/research/comparison.py`](../src/research/comparison.py).

The study service is shared by CLI, API, and dashboard. It validates a spec, previews aggregate cohort flow and timing counts, builds a feature table, evaluates a model, and stores a private run. Successful invented-data runs can be copied to an aggregate-only public package. The publisher uses an artifact allowlist and SHA-256 checksums. This makes accidental row-level publication less likely and allows package integrity checks. It is not a complete privacy proof for arbitrary future code or data. See [`src/research/study_service.py`](../src/research/study_service.py), [`src/research/publication.py`](../src/research/publication.py), and [`src/api/routes_studies.py`](../src/api/routes_studies.py).

### A small code-level explanation I can speak

The study cohort first computes:

```sql
row_number() over (
  partition by subject_id
  order by intime, stay_id
) as first_icu_rank
```

It keeps `first_icu_rank = 1` before later eligibility filters. Feature joins then use the selected `stay_id` for ICU charts and input events. Labs join by hospital admission and are restricted to the ICU time window. The exact SQL is generated in [`src/research/cohorts.py`](../src/research/cohorts.py) and [`src/research/features.py`](../src/research/features.py). This is a simple but important defense against mixing measurements from a later ICU stay. It does not solve every identity, coding, or timestamp problem in a real EHR.

### Evaluation code path

The registered study assigns unique `subject_id` values to train, validation, and test in 70/15/15 proportions with seed 42. Numeric fields receive median imputation and standard scaling. Categorical fields receive most-frequent imputation and one-hot encoding. These steps and logistic regression sit in one scikit-learn pipeline. The model uses `class_weight="balanced"`. This setting adjusts the fitting objective; it does not guarantee calibrated probabilities. The code computes validation AUPRC, held-out test AUROC, AUPRC, and Brier score. It also computes repeated stratified cross-validation on the combined development set and a bootstrap interval on held-out patient rows. The exact implementation is [`src/research/study_service.py`](../src/research/study_service.py).

The model summary records `selection_partition="validation"`, but the registered path contains only one logistic regression candidate. The validation set is reported; it is not evidence of a broad model search. The repeated cross-validation measures stability of this chosen pipeline on development rows. It is not a nested model-selection estimate. The test split is scored separately. A 200-resample bootstrap is attempted on the test rows, skipping one-class resamples. With a small death count, that interval can be wide or unavailable. A small test set should not be oversold.

The attribution output uses transformed feature values times logistic coefficients. The intercept plus the contributions reconstructs the model's decision score on the **log-odds** scale. The code verifies this additivity. It is a linear decomposition, not a causal effect and not an external SHAP analysis. The interpretation code is [`src/research/interpretation.py`](../src/research/interpretation.py). A coefficient can change with correlated predictors, encoding, or data shift.

### Interfaces and guardrails

The dashboard shows aggregate overviews, cohorts, and research study views. The API has aggregate analytics and cohort routes, plus typed `/studies` routes for listing, validation, preview, run, publication, and status. The study API checks study names and optional age and care-unit overrides. It can reject a stale expected dataset snapshot. Its `/assistant/draft` route returns a typed draft; it does not execute a study. See [`src/api/routes_studies.py`](../src/api/routes_studies.py) and [`src/research/assistant.py`](../src/research/assistant.py).

The separate natural-language-to-SQL feature maps predefined aggregate questions to SQL. Its guardrail blocks write keywords, multiple statements, `SELECT *`, Bronze access, projected raw IDs, non-aggregate queries, and tables outside an allowlist. It adds a default result limit. The rules are in [`src/llm/sql_guardrails.py`](../src/llm/sql_guardrails.py). These are useful checks for a local demo. They are regex-based and should not be presented as a formal SQL security boundary for hostile arbitrary input. A production service would need a real parser, a restricted read-only database role, query resource limits, audit controls, and security review. This is a design limitation, not a claim that a known exploit succeeded.

## 06. Evaluation and results

### How to read the numbers

There are three levels of result here. The small seed produces warehouse counts and a dated validation report. The workshop produces a four-task model comparison on 1,000 invented patients. The registered study produces one prospective mortality run on a narrower invented ICU cohort. Numbers from one level cannot be used as the denominator for another. They also cannot be used as estimates for MIMIC-IV patients.

For the local seed, the dated validation artifact reports six patient rows, seven admissions, seven ICU stays, and 20 passing checks. It reported zero failed checks and zero warnings on 2026-05-27. The check list covers required columns, unique keys, joins, LOS signs, date presence, categories, and source row counts. It is a small smoke-test signal. It cannot evaluate clinical plausibility or statistical validity. Source: [`outputs/private/validation_report.md`](../outputs/private/validation_report.md).

For the 1,000-patient workshop, the saved [aggregate report](../outputs/public/research_synthetic/aggregate_results/research_demo_summary.md) gives an illustrative historical result. Its selected **in-hospital mortality** random forest had held-out test AUROC `0.376`, AUPRC `0.148`, Brier `0.078`, and recall `0.000` at the report's classification threshold. Its test denominator was 150 of 1,000 eligible invented patients after a 700/150/150 split. This is a poor discrimination result, and the zero recall means that threshold detected no positive cases in that test split. The Brier value alone cannot rescue the model: it is affected by outcome prevalence and probability scale. The workshop also reports LOS, readmission, and diagnosis-class teaching tasks, but those are different targets with different eligibility rules. Do not merge their scores into a single “model performance” claim. The saved workshop artifacts are currently untracked local outputs, so cite them as a workspace snapshot.

The registered ICU study has two published historical packages in this workspace. They share the same study ID and a recorded dataset snapshot, but their scores differ. The newer package by recorded completion time is `synthetic_icu_mortality_24h_v1-bc1ca463`, completed 2026-10-16. Its [manifest](../outputs/public/research_synthetic/studies/synthetic_icu_mortality_24h_v1-bc1ca463/manifest.json) records code revision `e8fdf87c9626ed02f22f377133b44a7fdfb3ba67`. The current checkout was `2f231d5be3b18b51929bfe142da085e2a8a8041d` at documentation time. Thus the package is **historical run evidence**, not a current checkout benchmark. Its public outputs are also untracked in this workspace.

For run `synthetic_icu_mortality_24h_v1-bc1ca463`, the saved [evaluation summary](../outputs/public/research_synthetic/studies/synthetic_icu_mortality_24h_v1-bc1ca463/evaluation_summary.json) reports 800 eligible invented ICU rows: 560 train, 120 validation, and 120 held-out test. The target is death after hour 24 and by discharge. The held-out test AUROC is `0.537`, AUPRC `0.216`, and Brier score `0.218` when rounded to three decimals. Validation AUPRC is `0.062`. Development repeated cross-validation AUPRC mean is `0.098` with standard deviation `0.012` across six fold scores. This does not support a strong prediction claim. AUROC near 0.5 shows little rank separation in that held-out set. AUPRC needs a prevalence reference to judge meaning. The public evaluation summary does not include prevalence, so I should not claim an improvement over a prevalence baseline from that number alone. The [cohort flow](../outputs/public/research_synthetic/studies/synthetic_icu_mortality_24h_v1-bc1ca463/cohort_flow.csv) records the 800-row cohort. The saved [timing audit](../outputs/public/research_synthetic/studies/synthetic_icu_mortality_24h_v1-bc1ca463/timing_audit.csv) records 6,885 eligible lab events in that run; it is an event count, not a patient count.

The older package `synthetic_icu_mortality_24h_v1-970d76be` reports held-out AUROC `0.535`, AUPRC `0.109`, and Brier `0.241`, also with 120 test rows. Its [evaluation summary](../outputs/public/research_synthetic/studies/synthetic_icu_mortality_24h_v1-970d76be/evaluation_summary.json) is evidence that saved runs can differ. The current public summaries do not explain the difference enough to attribute it to one cause. The safe interview answer is: “Those are different historical run packages. I would compare their exact source content, run settings, and implementation revisions before making a causal explanation.” The recorded `dataset_snapshot` cannot settle that question because, in this code, it fingerprints table names rather than row contents.

The saved [two-site simulation](../outputs/public/research_synthetic/studies/simulated_site_transferability.json) is another historical invented-data result. The code makes two invented sources, delays one in three site-B lab results, trains on site A, evaluates an unchanged model on A and B, and calibrates separately using a disjoint B calibration partition. The artifact reports A test AUROC `0.350` on 72 rows and B test AUROC `0.589` on 384 rows. B test Brier changes from `0.166` before recalibration to `0.082` after the separate calibration fit. These different test populations and prevalences do not establish that site B is clinically easier or that a model transfers well. The experiment shows how measurement shift and recalibration can be inspected. The code and output are in [`src/research/sites.py`](../src/research/sites.py) and the linked artifact.

The saved [assistant evaluation](../outputs/public/research_synthetic/studies/assistant_evaluation.json) has five invented prompt cases. It reports five expected response states matched and zero failures. That tests the reviewed cases, including ambiguity and unsupported questions. It does not establish broad language understanding or adversarial robustness. The state comparison is implemented in [`src/research/evaluate_assistant.py`](../src/research/evaluate_assistant.py).

### What each metric means in a spoken answer

**AUROC** asks how often a randomly chosen positive receives a higher risk score than a randomly chosen negative. It does not say whether a probability of 0.2 is well calibrated. It can look tolerable under class imbalance while precision remains poor. **AUPRC** summarizes precision and recall over thresholds. It is sensitive to outcome prevalence, so report the prevalence and test population before comparing AUPRC across datasets. **Brier score** is the mean squared error between predicted probability and binary outcome. Lower is better, but it also depends on prevalence and the quality of the probabilities. **Calibration** asks whether people assigned a given risk have roughly that observed event frequency. A small synthetic test set can make calibration bins noisy. **Recall** at a chosen threshold is the share of actual positive cases detected. Threshold results require the threshold and a reason for choosing it. The workshop's zero recall is a useful reason to discuss threshold choice and class imbalance, not to quietly report only AUROC.

### What I would say if asked for “the main result”

> “The main demonstrated result is that I can run an explicit, time-aware synthetic study and audit its cohort and feature timing. The saved mortality scores are weak and differ across historical runs. They show why I need strong provenance and evaluation, not that I have a clinically useful model.”

## 07. Design decisions

**Why Bronze, Silver, and Gold?** I wanted each transformation stage to be inspectable. Bronze keeps source-like inputs and provenance. Silver establishes stable entities and timestamps. Gold provides known analysis grains. A single giant query would be shorter at first, but harder to audit and reuse. Layering does not fix a bad phenotype automatically. It gives me places to detect and explain it. See [`src/transform/run_sql_layer.py`](../src/transform/run_sql_layer.py).

**Why DuckDB?** It gives a simple local analytical database for CSV-heavy, reproducible experiments. It avoids a server requirement for the interview demo. The alternative is a managed warehouse or a production database, which would help with concurrent users and operational scale. The current project should be described as local research engineering. Large-table performance and incremental rebuild controls remain development work, as recorded in [`AGENTS.md`](../AGENTS.md).

**Why one first ICU stay?** It makes patient-level evaluation and cohort interpretation clearer. It prevents a patient's later stay from replacing an ineligible first stay. The tradeoff is a narrower target population and less statistical power. Another study might include repeated stays with patient-level grouping and a different estimand. That would require a new written protocol, not a quiet SQL tweak. See [`src/research/cohorts.py`](../src/research/cohorts.py).

**Why predict at hour 24?** The observation and prediction times are easy to state and test. That makes leakage checks concrete. The cost is that patients who die or leave ICU before hour 24 are excluded. This creates a conditional population and possible survivor selection. An admission-time model or dynamic landmark model would answer a different question. It would need separate feature and outcome rules. See the [time contract](12_cohort_time_contract.md).

**Why check `storetime` as well as `charttime`?** A value can be measured earlier but become available later. Checking only the measurement time would let a retrospective query use information unavailable at the prediction moment. `storetime` is an imperfect proxy for actual user visibility, but it is stronger than no availability check. A future system should validate how each site's timestamps are generated. See [`src/research/features.py`](../src/research/features.py).

**Why use a feature allowlist?** I wanted a task-specific set of predictors whose timing and provenance I could explain. This blocks obvious discharge and whole-stay leakage. The alternative is broad automated feature selection, but it would increase the audit burden and risk using post-index information. The allowlist does not mean all chosen variables are causally valid or transportable. See [`src/research/tasks.py`](../src/research/tasks.py).

**Why logistic regression for the registered study?** It is a comprehensible baseline. The pipeline and coefficients can be inspected. A more complex model might improve synthetic discrimination, but that would not solve the underlying clinical validation problem. In this repository, the single registered candidate also makes the evaluation story simpler. The broader teaching workshop compares dummy, linear, and random-forest models for different tasks. I should not claim a broad model search for the registered study. See [`src/research/study_service.py`](../src/research/study_service.py) and [`src/research/evaluate.py`](../src/research/evaluate.py).

**Why split by patient?** Records from one patient are related. Putting a patient's encounters in both train and test can inflate performance. The study assigns each `subject_id` once. This addresses one leakage path. It does not simulate a future hospital, a new calendar period, or a different documentation system. Temporal and site-based validation would be stronger for a real deployment question. See [`src/research/study_service.py`](../src/research/study_service.py).

**Why create deliberate bad-data scenarios?** A quality gate is more convincing when I can show that it reacts to a known fault. The scenario registry includes delayed labs, a duplicate admission key, a missing ICU anchor, and an impossible oxygen saturation value. These are invented faults applied in isolated copies. The duplicate-key and impossible-value checks are designed to stop affected runs. The delayed-lab case changes feature availability and supports a frozen-model comparison. This demonstrates behavior for these faults, not coverage of all real EHR errors. See [`src/research/scenarios.py`](../src/research/scenarios.py) and [`src/validation/validate_research_quality.py`](../src/validation/validate_research_quality.py).

**Why aggregate-only publication?** The public repository should show evidence without exporting row-level patient-like data or encouraging sharing of restricted data. The publisher allows only named aggregate artifacts from successful invented-data runs. An alternative is to publish a notebook with row-level examples; that would be risky for a general MIMIC-IV path and would confuse the synthetic and restricted sources. The allowlist and checksums are practical controls, not a legal or formal privacy certification. See [`src/research/publication.py`](../src/research/publication.py).

## 08. Limitations and failures

The most important limitation is **data origin**. The research generator makes its own arbitrary patterns. It does not preserve real clinical distributions, measurement processes, coding habits, or treatment decisions. A model can learn those invented rules. Even a high score would only show recovery of generator structure. The saved ICU mortality scores are weak, which makes overclaiming especially easy to detect. I should say this plainly rather than defend the numbers as promising clinical results. See [`src/research/seed.py`](../src/research/seed.py) and the [workshop description](10_synthetic_research_workshop.md).

The second limitation is **phenotype validity**. A code-based “sepsis-like” cohort is a proxy, not a validated sepsis phenotype. A ventilation-like cohort is also a proxy. The ICU mortality task has a clear synthetic outcome rule, but it has not been checked against real chart review, site conventions, or endpoint adjudication. A technically explicit definition can still have poor clinical validity. A professor focused on phenotyping may ask for sensitivity, specificity, positive predictive value, chart review sampling, terminology mapping, and transportability. This project does not have those real-data estimates. See `sql/cohorts/`, the [cohort definitions](05_cohort_definitions.md), and the [NIH phenotype evaluation guidance](https://rethinkingclinicaltrials.org/chapters/conduct/electronic-health-records-based-phenotyping/evaluating-phenotype-definitions/).

The third limitation is **selection and confounding**. The hour-24 cohort excludes early deaths and early ICU departures. The resulting population is conditional on surviving and remaining in ICU. A measured association between a treatment proxy and death could reflect clinician response to severity, not treatment effect. A lab count may be a marker of clinician attention. An observational model cannot by itself estimate causal treatment benefit. My model is for synthetic risk prediction, not causal inference or treatment recommendation. A future causal question would need a new target trial style design, treatment timing, confounder strategy, and assumptions.

The fourth limitation is **missingness**. The code can report missing rates and exclude results not known at prediction time. It uses median or most-frequent imputation inside a training pipeline. That prevents preprocessing from learning test-set medians, but imputation does not make missingness random. In a real ICU, ordering and recording are linked to severity and workflow. A missing value may be informative. I would want missingness by site, shift, time, subgroup, and source system, plus sensitivity analyses. The current workshop's missingness summaries describe invented data only. See [`src/research/features.py`](../src/research/features.py), [`src/research/study_service.py`](../src/research/study_service.py), and the [aggregate workshop report](../outputs/public/research_synthetic/aggregate_results/research_demo_summary.md).

The fifth limitation is **time semantics**. `storetime` is a useful operational proxy, but it may not equal the moment a clinician saw a result. A delayed interface, backdated chart entry, or system migration can alter that relationship. The synthetic data have clean timing by construction. A real deployment would need timestamp provenance, workflow review, and a sensitivity analysis around uncertain availability. The half-open time window is precise SQL. Its validity still depends on source semantics.

The sixth limitation is **generalization**. MIMIC-IV comes from one medical center, and the public 100-patient demo is small. The invented two-site experiment is not external validation. It creates artificial site differences; it does not reproduce two hospitals' populations or data collection. A real multi-site study would need common definitions, terminology mapping, local data-quality profiles, subgroup checks, and prespecified validation. An improvement in Brier after recalibration on invented site B cannot be generalized to a hospital. See [PhysioNet's MIMIC-IV description](https://physionet.org/content/mimiciv/3.1/) and [`src/research/sites.py`](../src/research/sites.py).

The seventh limitation is **incomplete provenance and run comparability**. The study manifest records code revision, spec hash, Python version, and a `dataset_snapshot`. The current snapshot hashes table names, not contents. Two historical packages report different model scores even though both record the same snapshot identifier. I cannot infer why from the public summaries. A stronger future implementation would hash versioned source manifests or content, record package versions and full configuration, and preserve immutable run inputs. This is a concrete gap exposed by the evidence, not a hypothetical warning. See [`src/research/study_service.py`](../src/research/study_service.py) and the two historical [run manifests](../outputs/public/research_synthetic/studies/synthetic_icu_mortality_24h_v1-bc1ca463/manifest.json) and [older manifest](../outputs/public/research_synthetic/studies/synthetic_icu_mortality_24h_v1-970d76be/manifest.json).

The eighth limitation is **system scale and query security**. Full-mode ingestion is scaffolded, but large event tables may need incremental builds and runtime profiling. LocalStack needs an available endpoint, bucket, and correct object paths. The SQL assistant's regex guardrail is a local safety layer and should not be a sole security control against adversarial SQL. BigQuery execution is out of scope. These are honest engineering boundaries. See [`AGENTS.md`](../AGENTS.md), [`src/ingest/check_localstack.py`](../src/ingest/check_localstack.py), and [`src/llm/sql_guardrails.py`](../src/llm/sql_guardrails.py).

Finally, no real-patient fairness or subgroup conclusion can be made. The workshop checks synthetic subgroups, but their composition is generated. The code can demonstrate how one might compute subgroup metrics. It cannot establish clinical equity or safety. The next research step would need real data permissions, clinical collaborators, subgroup definitions, adequate sample sizes, uncertainty, and governance review.

## 09. Technical Q&A

Each answer below starts with the claim I can defend. It then gives the mechanism and the limit. In practice I should answer the question asked, not recite the whole section.

### Basic questions

**Q1. What is the project?**  
**A.** It is a local clinical data warehouse with an invented-data research extension. It ingests MIMIC-IV shaped tables, builds Bronze, Silver, and Gold layers, and supports aggregate analysis. The research extension tests a prospective ICU study design on invented records. It is not a clinical decision support product. Evidence: [`README.md`](../README.md) and [`src/cli.py`](../src/cli.py).

**Q2. What did you personally do?**  
**A.** I was the sole builder, as stated for this interview document. I designed and implemented the pipeline, study workflow, and checks. I can show the modules and tests for the work. Authorship is a personal claim; the repository itself does not independently verify who typed each line.

**Q3. Did you use real MIMIC-IV records for the research results?**  
**A.** No. The saved research results use invented records made by this repository. The code can ingest the open demo or credentialed files when supplied, but these published scores are not from either source. Evidence: [`src/research/seed.py`](../src/research/seed.py) and [run manifest](../outputs/public/research_synthetic/studies/synthetic_icu_mortality_24h_v1-bc1ca463/manifest.json).

**Q4. What is the difference between the small seed and the workshop?**  
**A.** The small seed has six invented patients and checks the warehouse. The workshop normally creates 1,000 invented patients and exercises research evaluation. Their counts, tasks, and reports differ. Evidence: [`src/ingest/seed_synthetic.py`](../src/ingest/seed_synthetic.py), [`src/research/seed.py`](../src/research/seed.py), and the [dated validation report](../outputs/private/validation_report.md).

**Q5. What does Bronze mean here?**  
**A.** Bronze is the source-like layer with provenance. It makes input structure and file origin visible before cleaning. Missing optional files can produce typed placeholders, which are engineering scaffolds rather than evidence of zero clinical events. Evidence: [`src/transform/build_bronze.py`](../src/transform/build_bronze.py).

**Q6. What do Silver and Gold add?**  
**A.** Silver cleans entities, keys, and timestamps. Gold creates stable analysis tables at stated grains, such as admission and ICU stay. The registered study then builds its own stricter time-aware feature table. Evidence: [`src/transform/build_silver.py`](../src/transform/build_silver.py), [`src/transform/build_gold.py`](../src/transform/build_gold.py), and [`src/research/features.py`](../src/research/features.py).

**Q7. What is a cohort?**  
**A.** A cohort is the set of people or events that meet a written inclusion rule. Here the registered study keeps each adult patient's first ICU stay if they are alive and still in ICU at hour 24. That is narrower than “all ICU patients.” Evidence: [`src/research/cohorts.py`](../src/research/cohorts.py).

**Q8. What is the prediction time?**  
**A.** It is ICU entry plus 24 hours. The study uses earlier available measurements to predict death after that time and before hospital discharge. It does not make a prediction at ICU admission. Evidence: [study YAML](../configs/studies/icu_mortality_24h.yaml) and [time contract](12_cohort_time_contract.md).

**Q9. Why an aggregate dashboard?**  
**A.** It makes the warehouse inspectable without presenting raw patient rows as the default output. It is a research engineering display, not a clinical interface. The same caution applies to aggregate API responses. Evidence: [`dashboard/streamlit_app.py`](../dashboard/streamlit_app.py) and [`src/api/routes_analytics.py`](../src/api/routes_analytics.py).

**Q10. What can the natural language assistant do?**  
**A.** One path maps known analytics prompts to aggregate SQL; a separate study assistant drafts a typed interpretation. The study draft does not run a study. Both have narrow supported scopes. They are not general clinical reasoning systems. Evidence: [`src/llm/nl_to_sql.py`](../src/llm/nl_to_sql.py) and [`src/research/assistant.py`](../src/research/assistant.py).

### Intermediate questions

**Q11. How do you prevent future information from entering a model?**  
**A.** I define a prediction time and check both event time and availability time. A chart or lab value must occur before hour 24 and be stored by hour 24. I also exclude discharge outcomes and whole-stay summaries from predictors. These checks address known leakage paths; real timestamp semantics still need validation. Evidence: [`src/research/features.py`](../src/research/features.py) and [`src/research/tasks.py`](../src/research/tasks.py).

**Q12. Why do you need both `charttime` and `storetime`?**  
**A.** `charttime` tells me when a measurement is assigned. `storetime` tells me when its result is recorded in the source. A value can fit the observation window but arrive after the prediction time. I then exclude it. `storetime` remains a proxy for actual availability, not a verified clinician-view timestamp. Evidence: [`src/research/features.py`](../src/research/features.py).

**Q13. What happens when `storetime` is missing?**  
**A.** The registered study excludes the event. The study YAML explicitly sets unknown availability to exclude. This is conservative for leakage, but it can reduce coverage and select a different population of measurements. I report timing counts rather than silently using the value. Evidence: [study YAML](../configs/studies/icu_mortality_24h.yaml) and [`src/research/timing.py`](../src/research/timing.py).

**Q14. How do you avoid using a later ICU stay?**  
**A.** I rank all stays by patient before filtering and keep rank one. ICU chart and input events then join to the selected `stay_id`. A later stay cannot replace an ineligible first stay. The test suite includes a later-stay regression case. Evidence: [`src/research/cohorts.py`](../src/research/cohorts.py), [`src/research/features.py`](../src/research/features.py), and [`tests/test_study_platform.py`](../tests/test_study_platform.py).

**Q15. What exactly is the mortality label?**  
**A.** It is one if recorded death is after the hour-24 prediction time and no later than hospital discharge. Patients who died before or at hour 24 are excluded from this study. The label is operational and synthetic here. It is not a validated real-world mortality endpoint. Evidence: [`src/research/features.py`](../src/research/features.py).

**Q16. How do you handle missing predictor values?**  
**A.** I retain missing values through feature creation and report aggregate coverage. The model's numeric median and categorical most-frequent imputers are inside the fitted training pipeline. That avoids using test data to estimate imputations. It does not remove bias caused by why a measurement is missing. Evidence: [`src/research/features.py`](../src/research/features.py) and [`src/research/study_service.py`](../src/research/study_service.py).

**Q17. Why split by patient instead of row?**  
**A.** A patient's rows can share information. A row-level split could place related records on both sides and inflate a score. The registered study assigns `subject_id` values once before splitting rows. This controls that leakage route, but a random split is still weaker than external validation. Evidence: [`src/research/study_service.py`](../src/research/study_service.py).

**Q18. What is a Brier score?**  
**A.** It is the mean squared gap between predicted probability and a binary outcome. A low score can come partly from low event prevalence. I would compare it with a sensible baseline and inspect calibration and subgroup results. The historical registered run reports `0.218` on 120 invented test rows, not a clinical benchmark. Evidence: [historical evaluation summary](../outputs/public/research_synthetic/studies/synthetic_icu_mortality_24h_v1-bc1ca463/evaluation_summary.json).

**Q19. What does a publication checksum prove?**  
**A.** It shows whether an allowed package file changed after the checksum list was written. It does not prove the underlying data were clinically valid, that the code was secure, or that a different run used the same source rows. Evidence: [`src/research/publication.py`](../src/research/publication.py).

**Q20. What does the API expose?**  
**A.** It exposes aggregate health, analytics, cohort, and typed study operations. The study routes validate named study definitions and return aggregate previews or run summaries. They are not a general endpoint for extracting patient-level records. This is the intended and tested interface, not a claim of full security certification. Evidence: [`src/api/routes_studies.py`](../src/api/routes_studies.py) and [`tests/test_api_routes.py`](../tests/test_api_routes.py).

### Advanced questions

**Q21. Is your 24-hour model affected by immortal time or survivor selection?**  
**A.** Yes, its target population is conditional on being alive and still in ICU at hour 24. I state that condition explicitly. I do not compare it directly with an admission-time model or claim an all-admissions mortality estimate. If I wanted an admission-time question, I would move the prediction time and rebuild the features and eligibility rule. Evidence: [`src/research/cohorts.py`](../src/research/cohorts.py).

**Q22. Can you call the sepsis-like cohort a validated phenotype?**  
**A.** No. It is a transparent SQL proxy. Clinical validity would need a reference standard, code-set review, appropriate temporal rules, and performance assessment across sites. The project's [limitations document](08_limitations_and_ethics.md) says this directly. The research connection is the [NIH guidance on evaluating phenotype definitions](https://rethinkingclinicaltrials.org/chapters/conduct/electronic-health-records-based-phenotyping/evaluating-phenotype-definitions/).

**Q23. Does patient-level random splitting prove transportability?**  
**A.** No. It prevents a patient from crossing train and test in this local evaluation. It does not test another hospital, calendar period, coding system, or workflow. The invented site experiment is a mechanism demo, not real external validation. Evidence: [`src/research/study_service.py`](../src/research/study_service.py) and [`src/research/sites.py`](../src/research/sites.py).

**Q24. Why might lab event count predict mortality?**  
**A.** It may reflect illness severity, clinician concern, or care workflow. It can also change when a hospital changes ordering practices. I treat it as a predictor with provenance, not a causal risk factor. A cross-site analysis should test its stability and whether its use introduces bias. Evidence: [`src/research/tasks.py`](../src/research/tasks.py) and [`src/research/features.py`](../src/research/features.py).

**Q25. Is the study's repeated cross-validation nested?**  
**A.** No. The code runs repeated stratified folds on the development set for stability of one registered pipeline. It does not provide an unbiased estimate after broad hyperparameter or feature selection. The held-out test is separate, but it is also small and synthetic. Evidence: [`src/research/study_service.py`](../src/research/study_service.py).

**Q26. Do the coefficients explain causes of death?**  
**A.** No. They describe a fitted logistic model on transformed synthetic features. Correlation, coding, and selection can change their signs and magnitudes. The decomposition is on the log-odds score, not a causal effect. Evidence: [`src/research/interpretation.py`](../src/research/interpretation.py).

**Q27. How does the delayed-lab scenario compare models fairly?**  
**A.** The comparison fits preprocessing and logistic regression once on baseline training rows. It then scores common held-out patients under baseline and delayed-lab data. It separately reports who became ineligible and bootstraps paired metric differences. This isolates one software-defined data-availability change better than retraining every time. It still does not reproduce a real site outage. Evidence: [`src/research/comparison.py`](../src/research/comparison.py).

**Q28. What is your strongest evidence that the quality gate catches an error?**  
**A.** The code checks duplicate Bronze admission and ICU keys before cleaned tables can hide them. It also checks an impossible invented oxygen saturation value. The tests inject quality scenarios and assert the expected behavior. That is direct evidence for those fault types, not all possible EHR errors. Evidence: [`src/validation/validate_research_quality.py`](../src/validation/validate_research_quality.py) and [`tests/test_study_platform.py`](../tests/test_study_platform.py).

**Q29. What does `dataset_snapshot` hash?**  
**A.** It hashes the sorted names of Silver tables. It does not hash their rows. I would not use it to prove that two runs used identical data content. That is a known provenance limitation I would improve before making stronger reproducibility claims. Evidence: [`src/research/study_service.py`](../src/research/study_service.py).

**Q30. How would you move this toward a real multi-site study?**  
**A.** I would first define the research use and endpoint with clinicians, obtain permitted data, review each site's source workflows, map terminology, assess quality and missingness by site, and validate phenotype definitions against a reference. I would freeze a protocol and source snapshot before model evaluation. I would then use temporal and external validation, calibration, uncertainty, and subgroup analysis. The current repo provides a starting engineering structure, not those completed studies. This proposed work aligns with [fitness-for-use recommendations](https://pubmed.ncbi.nlm.nih.gov/35171985/).

### Adversarial questions

**Q31. “Your AUROC is around 0.54. Why should I care?”**  
**A.** I would not ask you to care about it as a clinical model. The value is in the traceable evaluation path: defined cohort, timing rules, leakage exclusions, held-out test, and explicit weak score. The weak score shows why the system should prevent overclaiming. Evidence: [historical run summary](../outputs/public/research_synthetic/studies/synthetic_icu_mortality_24h_v1-bc1ca463/evaluation_summary.json).

**Q32. “You say reproducible, but two packages have different scores.”**  
**A.** That is a fair challenge. Each package has a run ID and manifest, but the current snapshot is not a row-content hash. I can reproduce the procedure from code, yet I cannot prove the two historical inputs were identical from public manifests alone. I would strengthen content-level provenance and rerun a frozen input before claiming exact score reproduction. Evidence: the [newer](../outputs/public/research_synthetic/studies/synthetic_icu_mortality_24h_v1-bc1ca463/evaluation_summary.json) and [older](../outputs/public/research_synthetic/studies/synthetic_icu_mortality_24h_v1-970d76be/evaluation_summary.json) summaries.

**Q33. “Is this really MIMIC-IV research?”**  
**A.** It is a warehouse designed for MIMIC-IV shaped data and a synthetic research methods demonstration. The saved research models were not trained on real MIMIC-IV records. I would call it preparation for responsible MIMIC-IV research, not a clinical MIMIC-IV finding. Evidence: [`README.md`](../README.md), [`src/research/seed.py`](../src/research/seed.py), and the [run manifest](../outputs/public/research_synthetic/studies/synthetic_icu_mortality_24h_v1-bc1ca463/manifest.json).

**Q34. “Why did you not use a more powerful model?”**  
**A.** Because a more complex model would not solve unclear labels, unavailable data, and weak external validity. I chose an inspectable baseline for the registered study. The workshop does compare other algorithms, but those invented-data comparisons are teaching outputs. A real model search should follow a validated research question and data-quality assessment. Evidence: [`src/research/study_service.py`](../src/research/study_service.py) and [`src/research/evaluate.py`](../src/research/evaluate.py).

**Q35. “Does your SQL guardrail make the API safe?”**  
**A.** It blocks several unsafe patterns in the local aggregate query path. It is regex-based and is not a complete security boundary. For a real service I would add a parser, restricted database privileges, resource limits, and a security review. Evidence: [`src/llm/sql_guardrails.py`](../src/llm/sql_guardrails.py).

**Q36. “Can you prove that the synthetic data protect real patients?”**  
**A.** The generator reads no MIMIC-IV records, so these invented rows do not copy a restricted source through this generation path. I would not claim a formal privacy guarantee for all future inputs or exports. The publisher currently accepts only successful invented-data runs and allowlisted aggregates. Evidence: [`src/research/seed.py`](../src/research/seed.py) and [`src/research/publication.py`](../src/research/publication.py).

**Q37. “Why does an artificial site B matter?”**  
**A.** It is a controlled example of how availability and calibration can change when a data process changes. It does not tell us how the model will behave at a real hospital. I would use it to explain a research design, then ask what evidence is needed for real transferability. Evidence: [`src/research/sites.py`](../src/research/sites.py).

**Q38. “If all tests pass, why is the project not finished scientifically?”**  
**A.** Tests show that selected code paths behaved as expected on fixtures. They do not establish phenotype validity, clinical usefulness, or transportability. The warehouse's declared software scope is implemented. The scientific validation path remains open. Evidence: [`tests/test_study_platform.py`](../tests/test_study_platform.py), [`AGENTS.md`](../AGENTS.md), and the [research blueprint](11_trustworthy_research_platform_blueprint.md).

## 10. Research relevance to Professor Richesson

Professor Rachel Richesson is currently listed by the [University of Michigan Medical School](https://medschool.umich.edu/profile/7125/rachel-richesson) and the [Institute for Healthcare Policy and Innovation](https://ihpi.umich.edu/our-experts/richessr). Her profiles describe work in biomedical informatics, EHR data quality and usability, data standards, patient registries, and clinical phenotyping. Earlier Duke work is part of her research history. In the interview I should use her current affiliation unless the invitation itself identifies a different context. I should not call her a current Duke faculty member merely because an older paper or page has a Duke affiliation.

The most direct connection is **fitness for use**. Her [study of EHR fitness-for-use assessments in pragmatic trials](https://pubmed.ncbi.nlm.nih.gov/35171985/) reports concerns about reliability, missingness, site variation, and implausible values. My platform asks whether data are available and plausible for one declared prediction time. It also gives a cohort flow and a feature audit. The connection is conceptual and methodological. My synthetic checks have not been tested as fitness-for-use criteria in a real trial. A good discussion question is: “How would you decide which data-quality checks must block a study, and which should be reported as sensitivity analyses?”

The second connection is **computable phenotypes**. The [NIH Pragmatic Trials Collaboratory phenotype guidance](https://rethinkingclinicaltrials.org/chapters/conduct/electronic-health-records-based-phenotyping/evaluating-phenotype-definitions/) emphasizes explicit, reproducible, reliable, and valid definitions. My registered cohort has a clear grain and time contract. That helps reproducibility. It does not prove validity. The sepsis-like and ventilation-like SQL cohorts are transparent proxies. I should volunteer that distinction. A good question is: “What minimum evidence would make a local SQL cohort suitable for a multi-site phenotype validation study?”

The third connection is **provenance and standards**. Richesson and colleagues' [clinical research informatics review](https://pubmed.ncbi.nlm.nih.gov/25123746/) identifies quality, completeness, provenance, heterogeneous sources, explicit phenotype definitions, and governance as central issues. My Bronze provenance and study manifests are an engineering attempt to expose where results came from. The table-name-only snapshot shows where the attempt falls short. I can use that gap to discuss a concrete research direction: content-level source manifests, terminology mappings, and comparable quality profiles across sites.

The fourth connection is **EHR workflow change**. Richesson's current research context includes embedded pragmatic studies and EHR data use. An [NIH Collaboratory discussion of EHR challenges](https://rethinkingclinicaltrials.org/news/what-are-the-challenges-of-using-data-directly-from-the-ehrs/) highlights differences in systems, coding, and representation. My delayed-availability and two-site simulations show how such changes might affect a model pipeline. They are simplified demonstrations. They do not measure the frequency or impact of actual EHR changes.

The fifth connection is **responsible translation**. I can talk about moving from a working local pipeline to an evaluable research instrument. That means predefining the question, checking local data generation, reviewing code sets, measuring phenotype error, preserving provenance, and reporting uncertainty. It also means being able to say “this result is not yet supported.” I should present my project as evidence of readiness to work on these problems, not as a completed answer to them.

### A respectful research-fit answer

> “Your work on data quality, phenotyping, and fitness for use helped me see that an EHR pipeline needs a study-specific contract. I built a synthetic ICU example that makes the cohort, prediction time, and measurement availability explicit. It also exposed a provenance gap: my current snapshot does not hash data contents. I would like to study how to make these checks useful and valid across real sites, with clinical and informatics collaborators.”

This answer connects to public work without claiming a personal relationship, lab membership, or knowledge of an unpublished agenda. If she asks about a specific paper, name the paper or source accurately and discuss only what I have read. Do not invent details from a Google Scholar listing. The supplied Scholar page was not accessible during preparation; the links here point to accessible institutional, NIH Collaboratory, PhysioNet, and PubMed sources.

## 11. Interview interruptions and counterquestions

### If I am interrupted

**“What data was that?”** Answer: “Invented data generated in this repository. The open MIMIC-IV demo is a separate supported input. The scores I just mentioned were not produced from it.” Then give the artifact path if asked.

**“How many patients?”** Answer with the correct level: “The small warehouse seed has six patients. The workshop generates 1,000 invented patients by default. The historical registered study package has 800 eligible ICU patients and 120 held-out test rows.” If asked why 800, explain that the generator gives an ICU stay to roughly four of every five workshop patients, and the saved cohort flow records 800. Do not state that every future run must produce 800.

**“Which mortality?”** Answer: “The registered study predicts death after the hour-24 landmark and by hospital discharge among eligible first ICU stays. The workshop's in-hospital mortality task is a different first-admission teaching task.”

**“What was known at prediction time?”** Answer: “Demographics and admission facts in the allowlist, plus first-day measurements whose event and storage times pass the rule. Whole-stay and discharge fields are excluded from predictors.” A source field being present in a retrospective table does not mean it was usable then.

**“What did the model learn?”** Answer: “Only patterns in invented records. The linear attribution describes the fitted synthetic model's log-odds, not clinical causes.”

**“Was the phenotype validated?”** Answer: “No. The cohort and outcome rules are explicit and tested as code. Real-world sensitivity, specificity, and site validity have not been measured.”

**“Can I see the evidence?”** Answer: “Yes. The spec is in `configs/studies/icu_mortality_24h.yaml`; cohort and timing logic are in `src/research/`; tests are in `tests/test_study_platform.py`; the historical aggregate run package has a manifest and evaluation summary.” Point to Section 12 for exact links.

### How to answer a challenge without overexplaining

Use three sentences: **direct answer**, **mechanism or number**, **limit**. For example: “Yes, the model is conditional on survival to hour 24. The cohort SQL excludes death and ICU departure at or before prediction time. So its test score does not describe all ICU admissions.” If the interviewer wants detail, expand the time line or show the SQL. This style keeps the answer human and makes an AI agent less likely to merge unrelated facts.

### Counterquestions I can ask

1. “When your group evaluates a computable phenotype across sites, which evidence do you consider essential before using it for a pragmatic trial?”
2. “How do you distinguish a data-quality problem that should block analysis from one that should be handled through sensitivity analysis?”
3. “What forms of provenance are most useful when EHR interfaces or coding practices change during a study?”
4. “Would you frame delayed result availability mainly as a feature-engineering problem, a study-design problem, or both?”
5. “How do you evaluate whether a risk model remains meaningful when the measurement process differs across health systems?”
6. “For a PhD student joining this area, where is there the greatest need for methods: phenotype validation, data-quality measurement, or study-specific workflow tools?”

These are invitations to learn. They are not claims that the professor's lab currently runs a project with this exact scope. Choose one or two that fit the conversation. Do not read the full list aloud.

### Short glossary for an AI agent and for rehearsal

**Anchor or index time:** the point from which study timing starts. Here it is first ICU entry. **Prediction time:** anchor plus 24 hours. **Observation window:** the half-open first 24 hours from which eligible predictors are drawn. **Outcome window:** after prediction time through hospital discharge. **Grain:** what one row represents; the registered study uses one first ICU stay per patient. **Provenance:** where a field or result came from and how it was transformed. **Availability time:** when a measurement result can plausibly be used; this code uses `storetime` as a proxy. **Leakage:** information from outside the permitted prediction context entering predictors or evaluation. **Phenotype:** an operational rule identifying a clinical condition or population. **Proxy phenotype:** a simple rule that has not been clinically validated. **Calibration:** agreement between predicted risks and observed event frequencies. **Transportability:** whether a rule or model works in a different setting. **Fitness for use:** whether data quality is adequate for a particular question. **Synthetic invented data:** records generated by code without copying or fitting to real MIMIC-IV patient rows. **Historical run:** an existing saved artifact from a recorded code revision, not a fresh result from the current checkout.

## 12. Evidence and verification

### Claim-to-source map

| Claim to make | Primary evidence | Limit or verification need |
| --- | --- | --- |
| Warehouse has demo, full-local, and LocalStack modes | [`src/cli.py`](../src/cli.py), [`Makefile`](../Makefile), [`README.md`](../README.md) | Confirm endpoint and files before claiming an operational LocalStack run. |
| BigQuery is metadata-only here | [`src/ingest/load_bigquery_metadata.py`](../src/ingest/load_bigquery_metadata.py), [`README.md`](../README.md) | Do not claim BigQuery query execution. |
| Bronze, Silver, and Gold are implemented | [`src/transform/build_bronze.py`](../src/transform/build_bronze.py), [`src/transform/build_silver.py`](../src/transform/build_silver.py), [`src/transform/build_gold.py`](../src/transform/build_gold.py) | Implementation does not establish clinical validity. |
| Registered study is first adult ICU stay at hour 24 | [study YAML](../configs/studies/icu_mortality_24h.yaml), [`src/research/cohorts.py`](../src/research/cohorts.py) | It is conditional on survival and ICU presence at hour 24. |
| Prospective features require event and availability timing | [`src/research/features.py`](../src/research/features.py), [`src/research/timing.py`](../src/research/timing.py) | `storetime` is a proxy for true availability. |
| Model uses a task-specific allowlist | [`src/research/tasks.py`](../src/research/tasks.py), [feature registry](../configs/research/prospective_feature_registry.yaml) | The workshop uses a different feature catalog. |
| Registered study uses patient split and logistic pipeline | [`src/research/study_service.py`](../src/research/study_service.py) | Random patient split is not external validation. |
| Quality scenarios exist | [`src/research/scenarios.py`](../src/research/scenarios.py), [`src/validation/validate_research_quality.py`](../src/validation/validate_research_quality.py), [`tests/test_study_platform.py`](../tests/test_study_platform.py) | Only specified faults are tested. |
| Public study package is aggregate-only and checksum-verified | [`src/research/publication.py`](../src/research/publication.py) | Applies to the allowlisted invented-data package path. |
| Current test suite passed | `.venv/bin/pytest -q tests`, run on 2026-11-01: `23 passed in 5.98s` | Rerun after code or dependency changes. This is not a clinical validation result. |
| Stored small-seed validation had 20 passes, no failures or warnings | [`outputs/private/validation_report.md`](../outputs/private/validation_report.md) | Dated 2026-05-27. Rerun before calling it a current validation report. |
| Workshop result is a 1,000-patient invented-data snapshot | [aggregate report](../outputs/public/research_synthetic/aggregate_results/research_demo_summary.md), [`src/research/seed.py`](../src/research/seed.py) | Output is untracked in this workspace. State target and denominator with every score. |
| Historical registered run had 800 eligible rows and weak held-out scores | [manifest](../outputs/public/research_synthetic/studies/synthetic_icu_mortality_24h_v1-bc1ca463/manifest.json), [evaluation summary](../outputs/public/research_synthetic/studies/synthetic_icu_mortality_24h_v1-bc1ca463/evaluation_summary.json) | Recorded code revision differs from current checkout. Do not call it a fresh benchmark. |
| Older run reported different scores | [older evaluation summary](../outputs/public/research_synthetic/studies/synthetic_icu_mortality_24h_v1-970d76be/evaluation_summary.json) | Public artifacts do not establish the cause of the difference. |
| `dataset_snapshot` is not a data-content hash | [`src/research/study_service.py`](../src/research/study_service.py) | Inspect `_dataset_snapshot` before making any stronger reproducibility claim. |
| Professor Richesson's current affiliation and broad interests | [University of Michigan profile](https://medschool.umich.edu/profile/7125/rachel-richesson), [IHPI profile](https://ihpi.umich.edu/our-experts/richessr) | Recheck near the interview date because roles can change. |
| Her published work is relevant to data quality, provenance, phenotype definitions, and fitness for use | [2014 review](https://pubmed.ncbi.nlm.nih.gov/25123746/), [fitness-for-use study](https://pubmed.ncbi.nlm.nih.gov/35171985/), [NIH phenotype guidance](https://rethinkingclinicaltrials.org/chapters/conduct/electronic-health-records-based-phenotyping/evaluating-phenotype-definitions/) | Describe the connection as an interpretation, not an endorsement of this project. |
| MIMIC-IV demo is a real 100-patient public subset; full v3.1 is credentialed | [PhysioNet demo](https://physionet.org/content/mimic-iv-demo/2.2/), [PhysioNet v3.1](https://physionet.org/content/mimiciv/3.1/) | Do not mix either source with the invented research outputs. |

### Claims that need a fresh check before the interview

The `outputs/public/research_synthetic/` artifacts cited above exist in this workspace but are not tracked by Git at documentation time. Their relative links work locally. A fresh clone may need `make research-demo` and the relevant study commands to generate new artifacts; those new runs will have their own IDs and scores. The two saved package checksums verified locally on 2026-11-01. Checksum validity confirms file integrity against each package's checksum list, not the scientific validity of its results.

**Current software status.** Rerun the test suite and, if discussing current validation, run the configured validation path on the intended data source. The dated private report is not current by itself. **Current research metrics.** If I quote a newly run score, keep its full run ID, manifest, source version, target, denominator, split, and code revision together. A score without these details is hard to interpret. **Personal role.** I have confirmed sole-builder wording for this document. If collaborators contributed later, update that statement before using it. **Professor profile.** Recheck her institution, title, and recent work near the interview. **Real-data research.** Do not claim it unless I have actually obtained permitted access, completed the analysis, and can show an approved report.

### A safe answer template for an AI agent

1. Name the exact layer or study path. Say whether the evidence is current code, a test, or a historical artifact.
2. Answer the question in one direct sentence.
3. Give the cohort, prediction time, target, and denominator when discussing a result.
4. Cite the nearest code, spec, artifact, or external primary source in this document.
5. State the material limit. For a synthetic score, say explicitly that it is not clinical evidence.

If the evidence is absent, answer: **“The repository does not establish that claim.”** Then say which check or study would be needed. That is a stronger research answer than inventing a reassuring number.
