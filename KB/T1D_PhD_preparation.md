# PhD interview preparation: temporal event graphs and hypoglycemia prediction

> **Evidence boundary:** This module describes the project as documented in the latest **locally recorded pushed revision**, commit `eb49dd1` on branch `codex/manuscript-draft-2026-10-20`, dated **20 October 2026**. The remote branch could not be queried live because the local environment could not resolve `github.com`. The public `main` page was visible, but it is an earlier project snapshot. Later local, unpushed files are outside this module. Do not call this the project's current result without checking the remote again. [S1] [S2] [S3]
>
> **Use:** This is a preparation module for a prospective PhD interview. It is also a bounded source for an AI question-answering agent. It is not a clinical protocol, a published paper, or a claim that a prediction system is ready for use.

## One-page answer guide

| If asked… | Say this first | Boundary to add |
| --- | --- | --- |
| What is the project? | I study whether connecting recorded insulin and carbohydrate events to recent CGM readings helps predict a low CGM reading in the next 30 minutes. | It is a retrospective development study of a specific representation and endpoint. |
| What is the main result? | In the 20 October snapshot, the tested temporal event graph beat an equally sized late-fusion event-sequence model in five development folds at one seed and four folds at a second seed. | This does not prove that graph relations have clinical meaning or that the graph beats a converged CGM-only model. |
| Did typed clinical relations help? | A one-fold pilot favored generic routing over modality-typed routing. | Both models already knew event modality; this pilot tested routing, not access to new clinical knowledge. |
| Is the model clinically useful? | That has not been established. | Final holdout performance, external validation, alert burden, warning time, calibration, and explanation fidelity were not reported in this snapshot. |
| What is the scientific contribution? | The strongest current contribution is an auditable, patient-disjoint comparison with matched event inputs, windows, parameter count, and training budget. | Novelty for a knowledge graph or hypoglycemia prediction in general is not claimed. |
| What was my role? | I led the research direction and can explain the design, implementation, and analysis choices. | The pushed manuscript leaves formal authorship and contribution declarations unconfirmed. State personal actions only if personally true. |

**Answer labels used below.** **Implemented** means committed code or an executed procedure documented in the snapshot. **Observed in development** means a reported result from completed development predictions; the raw predictions were not pushed. **Planned** means proposed but not reported as completed. **Unverified** means the snapshot does not establish the fact.

**The sentence to memorize:** “The graph did better than one matched late-fusion sequence implementation under a one-epoch retrospective development protocol. The evidence does not yet isolate a graph-relation effect, prove clinical explanation quality, or establish performance on the reserved final group.” [S1] [S4]

## 01. Project identity

### The research question

The working project asks whether explicit links between recorded treatment events and continuous glucose monitoring, or **CGM**, observations improve short-horizon prediction of a low reading in people with type 1 diabetes, or **T1D**. The completed comparison is narrower. It tests one temporal event-to-CGM graph against one event-sequence model on the same observations and windows, with 36,883 parameters each and one training epoch. Relation types and explanation quality remain wider research questions. [S1] [S4]

### What exists in the selected snapshot

**Implemented:** The repository contains release auditing, canonicalization, eligibility and window indexing, event preparation, model training, prediction archiving, and evaluation utilities. The pushed working manuscript has a results snapshot and a verification record. It is a draft. It is not a peer-reviewed publication. It is not a final clinical model. [S1] [S2] [S3]

**Observed in development:** The principal one-epoch comparison was complete for five validation folds at training seed `20261003`. Four of five folds were complete at seed `20261004`. The graph had higher participant-macro average precision, or **AP**, and lower participant-macro Brier score in all nine completed matched fold-seed pairs. A separate one-fold routing pilot favored generic over modality-typed routing. [S1] [S4]

**Planned:** A final selected pipeline was to be trained on the 652 development participants and evaluated once on 183 reserved participants. Further goals included stronger controls, more training, external validation, reporting-delay tests, and explanation evaluation. The selected snapshot reports none of these as completed final-performance results. [S1] [S6]

### How to state personal involvement

The interview script uses the voice of a research lead: “I framed the question, organized the auditable pipeline, and examined what the controlled results can and cannot show.” This reflects the role selected for this preparation module. It is **not** independent proof of who wrote each file, trained each run, obtained access, or owns formal authorship. The pushed manuscript still contains placeholders for authors, affiliations, ethics, funding, and contributions. Before an interview, replace any first-person claim that is broader than your actual work. If asked for an exact contribution, name a concrete decision, code component, analysis, or verification step you personally performed. [S1] [S2]

### Why the evidence boundary matters

## 02. Interview explanations

### A 25-second opening

“I am studying how to predict a near-term low CGM reading in type 1 diabetes from recent glucose and recorded treatment events. My main method links insulin and carbohydrate records to nearby CGM observations in a temporal graph. In the pushed 20 October development snapshot, that graph beat one matched event-sequence model on patient-disjoint validation folds. The result is promising for that specific comparison. It does not yet prove a clinical graph advantage or a useful alert system.” [S1] [S4]

### A natural two-minute version

“My project starts from a practical data problem. A CGM gives a detailed glucose trace. A person may also have recorded basal insulin, boluses, and carbohydrate entries. Those records occur at different times. They may be incomplete or arrive late. If I simply put them into a model without checking time and provenance, I may get an impressive result that is not valid at prediction time.

“I built the study around an explicit prediction point. At an eligible CGM reading, the model sees about two hours of past glucose and only recorded events in that same historical interval. It predicts whether any of the next six five-minute CGM readings is below 70 mg/dL. The future must be completely observed for the label to count. Patients are separated across training and validation groups.

“The main comparison gives both models the same 24 CGM slots and up to 64 recent events. One model connects each event to an observed CGM slot at or after the event and passes messages into a glucose sequence. The other encodes CGM and event sequences separately, then combines them at the prediction head. Both have 36,883 parameters and the same one-epoch training budget. In the 20 October snapshot, the graph did better on participant-macro average precision and Brier score in all five folds at the first seed and four completed folds at a second seed.

“I do not interpret that as proof that the graph has discovered causal treatment relations. The sequence comparator fuses information later, so the difference could reflect alignment or optimization. In a separate pilot, a graph with modality-specific routing did slightly worse than generic routing. I still need a stronger time-aligned non-graph control, a matched CGM-only comparison, convergence checks, an untouched final evaluation, and tests of whether explanations reflect the trained model. My main value at this stage is a clear question, a reproducible data contract, and an honest reading of a bounded result.” [S1] [S4]

## 03. Problem and motivation

### The health problem in plain words

In T1D, glucose can fall below a safe range. A CGM samples interstitial glucose repeatedly and provides a trace of recent movement. A near-term warning could be useful, but usefulness depends on more than ranking probabilities. The warning must arrive early enough. It must avoid excessive false alerts. It must remain trustworthy when records are missing or delayed. This project measures a retrospective CGM threshold outcome first. It does not show that acting on its prediction prevents harm. [S1] [S7]

### Why glucose history is not the whole story

The recent CGM path is usually the strongest immediate clue to a low. Yet basal insulin, bolus insulin, and recorded carbohydrates may change how that path should be read. For example, a falling glucose trace after a bolus could carry a different interpretation from the same trace after a recorded carbohydrate intake. This is a modeling motivation, **not** a claim that the present data measure the full causal effect of insulin or food. Recorded events can be absent, wrong, duplicated, entered later, or measured at a coarser level than physiology requires. [S1] [S8]

### Why the “knowledge graph” claim needs care

### The informatics problem under the machine-learning problem

## 04. Data and methodology

### Source release and analytic population

**Observed in development:** The analysis uses the Loop study public dataset, release `2023-01-31`, from the Jaeb public dataset collection. It is a secondary retrospective analysis of that release. The analytic population is not the same as the 558 new Loop users in the original prospective effectiveness paper. The release roster had 919 participants. CGM source records appeared for 851. Requiring participant-level presence of CGM, basal, bolus, and a nonempty carbohydrate record left 835 candidate participants. This condition says the modalities exist somewhere for a participant. It does **not** say every two-hour prediction history includes all three event types. [S1] [S11]

The shared eligibility index had 56,375,850 windows across 835 participants. The development group held 652 people and 44,028,064 windows, with 1,296,297 positive labels. A separate group of 183 people was reserved for final model-performance evaluation. The full index and aggregate coverage audit included that group, so it is more accurate to say its **model performance** remained unopened than to call the group wholly unseen in every sense. The 44 million windows overlap within participants. They are not 44 million independent observations. [S1] [S6]

### Canonicalization and provenance

**Implemented:** Raw device records are ordered by UTC within participant partitions. Exact re-exports are collapsed with release-specific keys. A deterministic representative, the lowest source record identifier, is retained. Provenance remains available for audit. Calibration CGM records are excluded. If different canonical CGM values share one participant and UTC timestamp, that timestamp is ambiguous and is excluded from the primary measurement stream. By contrast, distinct non-CGM events at the same timestamp remain distinct instances. Merging them would erase potentially separate entries. [S1] [S11] [S12]

The manuscript reports 111,118,148 CGM source rows, 19,628,647 exact duplicates removed, 58,403 canonical calibration rows excluded, and 2,226,685 ambiguous CGM **timestamps** excluded. The non-conflicting stream had 86,977,148 CGM timestamps across 851 participants. The 835-person candidate group contained 86,418,499 non-conflicting numeric CGM timestamps. These counts have different units. Do not subtract ambiguous timestamps as though each were one source row. In the development event cache, 40,473,171 canonical basal, bolus, and food records remained; 13,867 had an unknown permitted model value. An unknown value is represented as unknown, not as a true zero dose or zero carbohydrate. [S1] [S11]

Source glucose was labeled in mmol/L. The implementation used a fixed conversion factor of `18.0182` to express mg/dL. The primary range policy kept observed numeric values after duplicate, calibration, and ambiguity rules. It did not claim that every retained extreme was within a device-validated physiological range. That tradeoff avoids an arbitrary hidden cutoff, while leaving range sensitivity as an important unfinished analysis. Raw values and times remain traceable. [S1] [S12]

### Logical time grid and eligible histories

**Implemented:** Prediction indices are observed CGM times. The code recognizes a logical five-minute grid when adjacent observations are within one second of an integer multiple of 300 seconds. A gap produces missing slots. An irregular interval can restart a grid run. The pipeline does not silently round a reading onto a new time or interpolate a future outcome. The ±1-second tolerance was chosen from development chronology and coverage audits. [S1] [S13]

At time `t`, history is `(t−120 minutes, t]`. On a complete five-minute grid this gives 24 slots, approximately `t−115` through `t`. A window needs at least 22 observed slots and no run of more than two consecutive missing slots. The last three observed required positions, `t−10`, `t−5`, and `t`, must each be at or above 70 mg/dL. This is a modeling rule to avoid issuing a new incident-low prediction during an ongoing low. It is not a clinical proof of recovery. Missing CGM slots in the executed full-history models have zero payload **and a separate observation mask**. The earlier draft protocol discussed carry-forward filling; the reported neural comparison instead used the zero-plus-mask representation. [S1] [S7]

### Outcome definition

The primary binary label is

```text
y(t) = 1 if any CGM(t + k × 5 minutes) < 70 mg/dL, for k = 1,…,6;
y(t) = 0 if all six future CGM values are observed and none is < 70;
y(t) is undefined and excluded if any required future slot is unobserved.
```

Exactly 70 is not low. Even if a low appears among a partially observed future, that window is excluded under the primary rule. The symmetrical complete-future requirement avoids giving positives a different coverage rule from negatives. It also selects better-monitored periods, so the estimate does not automatically represent all real-world time. The label says “any low reading within 30 minutes.” It does not identify a sustained episode, severe symptoms, or a full 30 minutes of warning. [S1] [S7]

### Event eligibility and availability

An event is admissible by **occurrence time** only if it falls in `(t−120 minutes, t]`. The newest 64 recorded instances are kept. The model uses newest-first event order. The 64-event limit was selected after a development audit: 16 events would have truncated 39.272% of windows; 64 events truncated 17,720, about 0.040%. A truncated older event is not the same as evidence that it never happened. The retained token carries a validity flag, modality, a hashed subtype, normalized age, normalized value, and known-value information. Export-provenance channels are zeroed for both neural models. [S1] [S14]

The reported models assume each event was usable at occurrence time. The upload audit could not validate actual first-usable times, so this is optimistic retrospective replay. A later delay study would need the same policy for all comparators. [S1] [S8]

### Splits and leakage controls

Five deterministic development configurations have disjoint train, validation, and internal development-test participant groups within each configuration. Validation groups together cover the 652 development people once. Training groups overlap between configurations, so fold estimates are correlated. The repository calls them “outer” folds, but they are exploratory development comparisons, not an untouched nested cross-validation campaign. The reserved 183-person final-performance group is separate. The split manifest has a recorded checksum. [S1] [S6]

| Fold | Train people | Validation people | AP-defined people | Internal development-test people | Validation windows | Positive labels |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 395 | 130 | 130 | 127 | 8,885,621 | 274,044 |
| 1 | 381 | 141 | 140 | 130 | 9,386,356 | 270,499 |
| 2 | 387 | 124 | 124 | 141 | 8,395,597 | 229,814 |
| 3 | 398 | 130 | 129 | 124 | 9,167,239 | 264,561 |
| 4 | 395 | 127 | 127 | 130 | 8,193,251 | 257,379 |

An input graph at `t` must contain only historical measurements and permitted events. No future CGM value, future episode node, future label, or target-derived edge may be available to its encoder. Training-only fitting must apply to learned transforms. Identical patient membership, window IDs, labels, and input-content fingerprints are checked for paired model archives. This is the practical meaning of “same-information comparison.” [S1] [S15]

## 05. Architecture and implementation

### Data flow from source to score

The pipeline can be explained as a sequence of contracts:

```text
Loop source tables
  → source audit and UTC/provenance checks
  → canonical CGM and event instances
  → logical five-minute grid and eligible-window index
  → patient-disjoint development manifest
  → 24 CGM slots + masks, and up to 64 event tokens
  → graph or sequence neural encoder
  → probability for each identical prediction window
  → participant-keyed prediction archive
  → AP, Brier, and paired participant analyses
```

**Implemented:** Pushed modules `loop_adapter.py`, `temporal_eligibility.py`, `window_index.py`, `event_cache.py`, `manifest.py`, `metrics.py`, and `archive.py` handle source mapping, windows, events, splits, scoring, and prediction checks. The pushed `kaggle_event_sequence_gru` directory contains earlier neural workflows. The exact graph-versus-sequence source and protected prediction archives described by the manuscript are **not in this commit**. Its manuscript build reads aggregates; it does not retrain models. The architecture below comes from the manuscript, and the nine comparisons cannot be rerun from pushed files alone. [S1] [S2] [S4] [S9]

### Canonical records and window indexing

### Event token construction

Each retained event is a 17-channel token. The channels are: one validity flag; three indicators for basal, bolus, and food; eight stable hashed subtype indicators; normalized age; numeric value; a known-value flag; and two export-provenance channels. The last two channels are set to zero in both reported neural variants. Hashing maps many possible subtype strings into eight fixed positions. Different subtypes can collide, so the hash is a compact code, not an ontology. [S1] [S14]

Age is divided by 120 minutes. Glucose is divided by 100. Event values are divided by fixed constants of 10 for basal, 25 for bolus, and 150 for food. These are numerical scaling choices, not patient-specific physiological estimates. Only permitted normal-bolus quantities are modeled as known delivered amounts. Unvalidated extended-bolus amounts are not silently treated as delivered. Basal values are recorded pump state, not reconstructed insulin exposure. The model does not compute insulin-on-board or carbohydrate-on-board kinetics. [S1] [S14]

### The graph model

For each prediction window, the graph has CGM-slot representations and retained event representations. A two-to-64 projection followed by `tanh` embeds glucose plus mask. A 17-to-64 projection embeds each event token. Each event points to the nearest **observed** CGM slot at or after its occurrence, no later than `t`. Missing CGM slots are not edge targets. The link means “this event occurred before this nearby observation.” It does not mean “this event caused this glucose value.” [S1] [S9]

For an edge, the model combines the event embedding, destination CGM embedding, normalized time difference, and three modality indicators. That gives 132 input channels. Three message experts each use a `132 → 14` linear layer, ReLU, then `14 → 64` projection. In the reported **generic** graph, every edge message is the mean of the three expert outputs. Messages aimed at the same CGM slot are summed and scaled by the square root of the number of incoming events, with a minimum divisor of one. The slot receives a residual update followed by `tanh`. A 64-channel GRU reads 24 fused slots from oldest to newest. A `64 → 32 → 1` head with ReLU produces a logit, then a probability. Total trainable parameters: **36,883**. [S1] [S9]

The separate **typed** graph uses the same input, topology, experts, and parameter count. It selects one expert by basal, bolus, or food type. The generic graph also receives modality indicators. The experiment therefore tests whether hard routing by type helps. It does not test whether supplying otherwise absent modality information helps. The type label can be reconstructed from the event token. A more ambitious semantic graph would require additional independently justified relations and checks that those relations mean what the study says they mean. [S1] [S9]

### The sequence comparator

The non-graph comparator sees the same 24 CGM slots, masks, and 64-event limit. A CGM GRU uses 66 hidden channels. The event tokens pass through a `17 → 27` projection with ReLU and then a 67-channel event GRU. The final valid event state is used. If there are no events, the event state is zero. The CGM and event states are concatenated. A `133 → 24 → 1` head with ReLU gives the risk logit. Its trainable parameter count is also **36,883**. [S1] [S9]

### Training and archive checks

The matched fits used AdamW, learning rate `0.0002`, weight decay `0.0001`, unweighted binary cross-entropy with logits, batch size at most `4,096`, and one pass through assigned training windows. Batches streamed by participant and partition. They were not independently shuffled across every window. The main five-fold seed ran on Apple MPS. The second seed completed four pairs by the evidence date. An earlier CUDA fold-0 pair is discussed separately because hardware and execution conditions differed. [S1] [S16]

The documented run recorded settings, fingerprints, counts, checkpoints, and participant-keyed predictions. Pushed `neural_contract.py` checks content digests, membership, window identity, score range, chronology, and checkpoint configuration. The pushed archive comparator can recompute paired measures **when protected predictions are supplied**. Those predictions and the nine underlying paired-audit JSON files are not in the pushed commit. The pushed CSV and verification JSON support an aggregate audit, not a fresh independent prediction-level reproduction. [S2] [S4] [S15] [S16]

## 06. Evaluation and results

### What each metric answers

**Participant-macro AP** asks how well each person's positive windows are ranked above their negative windows, then gives each eligible person equal weight. AP uses threshold-grouped tied scores and stepwise precision-recall integration in the corrected metric version. It is not trapezoidal area under the precision-recall curve. A participant with no positive labels has undefined AP and is excluded from the AP mean. Two development people had this property. The AP denominator is therefore **650**, while Brier uses all **652** development people. [S1] [S17]

**Brier score** is mean squared error between a predicted probability and the binary outcome. Lower is better. Participant-macro Brier averages each person's score equally. Pooled Brier averages windows and can give people with more windows more weight. The table below uses macro Brier for the principal neural comparison. AP and Brier can disagree: a model may rank cases better but have worse probability calibration or overall squared error. No single metric proves alert usefulness. [S1] [S17]

The reported 95% intervals are paired participant bootstrap intervals from 10,000 resamples of **fixed fitted predictions**. Both models are resampled using the same participant draws. This respects within-person window dependence better than resampling millions of windows as independent units. It still omits uncertainty from model refitting, hyperparameter selection, seeds, and population shift. Overlapping fold training sets also make fold effects dependent. Do not describe these as confidence intervals for a universal graph advantage. [S1] [S4]

### Five completed folds at seed `20261003`

**Observed in development:** Positive AP differences favor the graph. Negative Brier differences favor the graph. The values are rounded from the full-precision pushed snapshot. [S1] [S4]

| Fold | Graph macro AP | Sequence macro AP | Graph − sequence AP | Graph − sequence macro Brier |
| --- | ---: | ---: | ---: | ---: |
| 0 | 0.475384 | 0.394764 | +0.080620 | −0.001953 |
| 1 | 0.460125 | 0.378379 | +0.081746 | −0.002153 |
| 2 | 0.453164 | 0.379705 | +0.073460 | −0.001930 |
| 3 | 0.471442 | 0.360977 | +0.110465 | −0.002562 |
| 4 | 0.474226 | 0.387856 | +0.086370 | −0.001964 |

The descriptive unweighted mean of the five AP differences is `+0.086532`. The corresponding mean Brier difference is `−0.002113`. The graph's descriptive mean AP is `0.466868`; the sequence model's is `0.380336`. These are arithmetic summaries of fold estimates. They are not a pooled participant-level AP, a final holdout result, or a meta-analytic estimate. Graph AP was higher for 597 of 650 participants with defined AP. Graph Brier was lower for 615 of 652 participants. [S1] [S4]

### Four completed folds at seed `20261004`

The second seed also favored the graph in each completed pair. Its AP differences were `+0.078540`, `+0.090208`, `+0.070275`, and `+0.106387` for folds 0 through 3. The corresponding macro-Brier differences were `−0.002178`, `−0.002430`, `−0.001721`, and `−0.002504`. Fold 4 did not have a completed paired audit in the 20 October snapshot. It must not be silently counted as completed or inferred from the first seed. The two seeds reuse the same validation people. They do not double the independent sample size. [S1] [S4]

The earlier CUDA fold-0 comparison produced graph AP `0.474481` versus sequence AP `0.389901`, a difference of `+0.084580`. The Apple MPS refit at the same nominal seed and fold also favored the graph, but its numbers were not identical. This is directional execution robustness, not exact cross-hardware reproducibility or a second cohort. [S1]

### Typed routing and historical controls

In a **separate one-fold CUDA pilot**, generic routing achieved macro AP `0.474481` and macro Brier `0.021522`. Typed routing achieved AP `0.471859` and Brier `0.021619`. Typed minus generic AP was `−0.002622`, with interval `(−0.003386, −0.001909)`. Typed minus generic Brier was `+0.000097`, with interval `(+0.000076, +0.000121)`. Typed AP was higher for 35 people and lower for 95. Because both routes saw the same modality information, this is evidence against the tested **routing constraint** under that pilot schedule. It is not a verdict on all clinical relation modeling. The manuscript says local recovery of the typed pilot's raw predictions was not confirmed. [S1] [S2]

### The defensible result statement

“In the pushed 20 October retrospective development snapshot, one temporal event-to-CGM graph outperformed one parameter-matched late-fusion sequence comparator on nine completed patient-disjoint validation fold-seed pairs. The separate one-fold typed-routing pilot favored generic routing. These findings motivate stronger controls. They do not prove that graph relations, clinical semantics, auxiliary events, explanations, or deployment alerts add value.” [S1] [S4]

## 07. Design decisions

The design choices below answer different threats to validity. A good interview explanation names both the reason for a choice and its cost. None is a universal clinical rule. [S1] [S7] [S10]

| Decision | Why it was made | Cost or next control |
| --- | --- | --- |
| Patient-disjoint folds | Keep correlated windows from one person out of both training and validation within a fold. | Fold training sets overlap. A separate chronological within-person study would answer a different question. |
| Six fully observed future slots | Avoid treating missing future glucose as a confirmed negative. | Evaluates better-monitored periods. A partial-future analysis needs an explicit censoring model. |
| Three recent non-low readings | Avoid predicting a low already in progress. | Excludes some post-low risk; test a predeclared alternate recovery gate. |
| Five-minute logical grid with ±1-second tolerance | Preserve observed source readings while recognizing small timestamp drift. | Irregular runs and gaps reduce eligible time. Do not silently round or interpolate targets. |
| Zero CGM payload plus mask | Mark an unobserved slot without inventing a reading. | Compare training-only imputation or continuous-time methods under identical availability. |
| Individual event tokens | Preserve type, age, value, and instance order that totals would lose. | Sparse or erroneous records can add noise. The two-hour and 64-event caps bound the represented history. |
| Identical input membership and 36,883 parameters | Reduce data and model-size confounding in the graph-versus-sequence pair. | Fusion position, computation, and learning rate of progress still differ. A time-aligned non-graph control is needed. |
| Generic versus typed experts | Test whether a hard modality-routing constraint helps on the same topology and parameter count. | Type is already in the token. A routing result cannot prove new clinical knowledge. |
| Participant-macro AP plus Brier | Give people equal weight in ranking and probability-error summaries. | AP omits people without positives; neither measure establishes alert burden or lead time. |
| Provenance and checksums | Trace repeated exports, conflicts, units, patient membership, and model inputs. | Adds engineering work and still cannot prove event logging is complete. |

The strongest next experiment depends on the question. A time-aligned non-graph control tests whether the graph's early alignment matters. A matched CGM-only control tests whether treatment records add value. A longer and replicated schedule tests whether the one-epoch difference survives adequate optimization. These should be run without opening the reserved final-performance group for model selection. [S1] [S10]

## 08. Limitations and failures

**Mechanism is unresolved.** The graph fuses event information into CGM positions before recurrent reading. The comparator fuses two separately encoded streams near the output. A difference can come from alignment, message aggregation, widths, or one-epoch optimization. Exact parameter equality does not isolate graph structure. A graph can also beat this event-sequence model without beating a strong CGM-only model. Earlier CGM diagnostics used different schedules and cannot settle that question. [S1] [S9]

**Training and uncertainty are bounded.** Principal fits ran one epoch. Convergence was not shown. A historical joint sequence model improved substantially between epochs 1 and 2. Only four second-seed folds were complete. Fold training sets overlap, and both seeds reuse participants. The narrow participant-bootstrap intervals condition on fixed predictions. They exclude retraining, architecture search, and transport to a new cohort. Millions of overlapping windows do not replace independent people. [S1] [S4]

**The data do not capture full physiology.** Repeated exports, conflicting CGM timestamps, unknown event values, incomplete logging, subtype-hash collisions, the two-hour lookback, and the 64-event cap all matter. The primary range policy retained numeric extremes without a device-specific validity cutoff. Basal records represent pump state; the model did not reconstruct delivered insulin exposure or insulin-on-board. A missing meal entry is not evidence that no meal occurred. [S1] [S11] [S14]

**Availability is an optimistic assumption.** The model replayed each recorded event at its occurrence time. The upload audit could not establish when the event first became usable. A later-entered carbohydrate record could therefore appear too early in this retrospective setup. Simulated delay would test sensitivity to a chosen scenario. It would not measure actual entry latency. [S1] [S8]

**The target and cohort are narrow.** A single future CGM value below 70 qualifies when all six future slots are observed. This is neither a severe clinical event nor a sustained episode. Complete-future and recent non-low gates select the evaluated periods. Participant selection required source presence for key modalities. The pushed snapshot has no verified demographic subgroup table, no final-performance result for the reserved 183 people, and no external validation. [S1] [S7]

**Explanations and clinical utility are unverified.** A temporal graph edge is not a causal treatment effect. No completed independent explanation-faithfulness study, clinician review, alert threshold, false-alert burden, lead-time analysis, or prospective benefit appears in the snapshot. The negative typed-routing pilot and earlier event-summary failures are useful constraints: more modalities or relation labels do not automatically help. They do not show that insulin or food are generally uninformative. [S1] [S18]

## 09. Technical Q&A

Each answer below is deliberately self-contained. An AI agent may quote or paraphrase one answer, but should keep its evidence label and limitation. “This snapshot” always means the pushed 20 October 2026 evidence snapshot.

### Basic questions

**Q01. What is the one-sentence project aim?** **Implemented research framing:** Test whether timestamped links from recorded treatment events to recent CGM readings help predict a CGM value below 70 mg/dL within 30 minutes. **Limit:** The completed experiment tests one graph against one sequence implementation. [S1]

**Q02. What is type 1 diabetes here?** **Context:** It is the population named by the Loop study release and the working research question. **Limit:** The model does not infer a new T1D diagnosis or create a computable T1D phenotype. [S1]

**Q03. What is predicted?** **Implemented:** A binary label for any observed CGM value `<70 mg/dL` in the next six five-minute slots. **Limit:** It is not a sustained episode label. [S1] [S7]

**Q04. What is the input history?** **Implemented:** Twenty-four nominal five-minute CGM positions in `(t−120, t]`, with observation masks. **Limit:** The two-hour support does not model all delayed physiology. [S1]

**Q05. What makes an index eligible?** **Implemented:** Enough recent CGM coverage, no long missing run, and three observed non-low readings at `t−10`, `t−5`, and `t`. **Limit:** This is a protocol gate, not clinical recovery. [S1] [S7]

**Q06. What happens to an incomplete future?** **Implemented:** The label is excluded if any of the six required future slots is missing. **Limit:** This selects well-observed periods. [S1]

**Q07. How many participants were in development?** **Observed in development:** 652. Another 183 were reserved for final model-performance evaluation. **Limit:** The reserved group's aggregate eligibility was audited, so “never inspected at all” is inaccurate. [S1]

**Q08. What is the headline comparison?** **Observed in development:** One temporal event graph versus one late-fusion event-sequence model, with matched inputs, windows, parameter count, and one-epoch schedule. **Limit:** Fusion strategy still differs. [S1]

**Q09. What was the headline direction?** **Observed in development:** The graph had higher macro AP and lower macro Brier in all nine completed matched fold-seed pairs. **Limit:** This is development evidence, not final or external validation. [S1] [S4]

**Q10. Is the graph a validated clinical knowledge graph?** **Unverified:** No validated external ontology or independent clinical relation semantics were tested. **Implemented:** Edges are deterministic temporal links from events to CGM slots. [S1] [S5]

### Intermediate questions

**Q11. Why use patient-disjoint folds?** **Implemented:** They keep one person's correlated windows out of both training and validation within a fold. **Limit:** The five training sets overlap across folds. [S1] [S6]

**Q12. Why is the AP denominator 650 rather than 652?** **Observed in development:** Two development people had no positive outcome windows, making their person-level AP undefined. Brier still includes all 652. [S1]

**Q13. How were duplicates treated?** **Implemented:** Exact re-exports were collapsed with release-specific keys and a deterministic source representative. **Limit:** Distinct records at one time were not automatically collapsed. [S1] [S11]

**Q14. Were future glucose values interpolated?** **Implemented:** No. A complete future is required for the primary label. **Limit:** This narrows evaluable time. [S1] [S7]

**Q15. What does an unknown event value mean?** **Implemented:** It has a known-value mask of zero. Its numeric placeholder is not a claim of zero dose or zero carbohydrates. [S1] [S14]

**Q16. How is an event linked to glucose?** **Implemented:** It points to the nearest observed CGM slot at or after occurrence, no later than index time. **Limit:** This is temporal assignment, not causal attribution. [S1]

**Q17. What does “generic routing” mean?** **Implemented:** The message for each edge is the mean output of three experts. **Limit:** Generic routing still sees modality indicators, so it is not type-blind. [S1]

**Q18. What does “typed routing” mean?** **Implemented:** One expert is selected by basal, bolus, or food type. **Observed in development:** It underperformed generic routing in a one-fold pilot. [S1]

**Q19. Why match 36,883 parameters?** **Implemented:** It controls a simple model-size confounder. **Limit:** It does not equalize computation, fusion, or optimization. [S1]

**Q20. What was the optimizer?** **Implemented:** AdamW, learning rate `0.0002`, weight decay `0.0001`, and unweighted binary cross-entropy with logits for the principal fits. **Limit:** One fixed schedule does not prove convergence. [S1]

**Q21. Were windows randomly shuffled?** **Implemented:** Batches streamed by participant and partition; the reported runs did not independently shuffle all windows. **Limit:** Training order could affect one-epoch comparisons. [S1]

**Q22. Why use source fingerprints?** **Implemented:** They help verify paired runs consumed the intended frozen input content and membership. **Limit:** A matching hash cannot prove the scientific target is clinically useful. [S15]

**Q23. What was the primary release?** **Observed in development:** Loop public dataset release `2023-01-31`. **Limit:** The exact custodian release citation and reuse terms still needed author confirmation in the draft. [S1] [S2]

**Q24. Is the original prospective Loop study the same as this analysis?** **Observed in development:** No. The project is a secondary retrospective analysis with a distinct analytic population and endpoint. **Limit:** The original study's ethics approval is not automatically approval of this analysis. [S1]

**Q25. What does a 95% bootstrap interval mean here?** **Implemented:** It describes participant-resampling variation for fixed predictions. **Limit:** It omits model retraining, seed, and external-cohort uncertainty. [S1] [S4]

### Advanced questions

**Q26. What exactly is the graph-minus-sequence estimand?** **Observed in development:** A difference in participant-macro AP or Brier on identical validation windows between two fitted implementations under the declared schedule. **Limit:** It is not an isolated causal effect of graph edges as a model family. [S1]

**Q27. Why can early fusion confound the result?** **Method reasoning:** The graph injects event messages into CGM slots before its GRU, while the comparator joins separate final states at the head. **Limit:** A matched time-aligned non-graph control is needed to separate alignment from message passing. [S1] [S9]

**Q28. What does the typed pilot isolate?** **Implemented:** It holds input, topology, expert bank, and parameter count fixed while changing expert routing. **Limit:** It is one fold and one epoch, with local raw-prediction recovery unconfirmed in the manuscript snapshot. [S1] [S2]

**Q29. Why is a type edge not new information?** **Method reasoning:** Basal, bolus, or food type is already encoded in the event token. Selecting an expert by that type changes inductive bias, not data access. [S1]

**Q30. How would you test relation value more directly?** **Planned:** Compare graph, time-aligned non-graph, generic and typed routing, event-disabled variants, and constrained relation perturbations on the same windows and schedule. **Limit:** These decisive controls were not completed in the selected snapshot. [S1] [S10]

**Q31. How would you test event value beyond CGM?** **Planned:** Compare a strong matched CGM-only model with an event-enabled version under equal training and model-selection opportunities. **Limit:** Historical CGM results cannot be treated as this exact control. [S1]

**Q32. How might event logging create bias?** **Method reasoning:** People who log meals or insulin more fully may differ from those who do not. Presence may correlate with device behavior or engagement. **Limit:** The snapshot does not quantify this bias. [S1]

**Q33. How might future coverage create bias?** **Method reasoning:** Requiring six future CGM readings selects periods with better monitoring. **Limit:** Reported performance does not automatically extend to sensor gaps or disrupted use. [S1]

**Q34. What is temporal leakage in this task?** **Method reasoning:** It occurs if post-`t` information, a retrospectively entered event not available at `t`, or target-derived structures enter model inputs. **Implemented:** Future CGM is excluded from model features. **Limit:** Actual event arrival times were not validated. [S1] [S8]

**Q35. Can occurrence time equal availability time?** **Unverified:** The Loop upload audit could not establish that. **Implemented assumption:** The reported retrospective replay treats recorded events as immediately available. [S1] [S8]

**Q36. Would a simulated delay solve availability?** **Planned:** It would measure performance under a stated artificial delay. **Limit:** It would not estimate real-world reporting latency without observed arrival data. [S1]

**Q37. Why use a square-root count divisor for messages?** **Implemented:** It scales the sum when several events target one CGM slot, reducing raw count growth. **Limit:** It is an architectural choice, not a physiological dose-response law. [S1]

**Q38. Why not treat each event edge as a treatment effect?** **Method reasoning:** Assignment uses timing only. Confounding, delayed action, logging error, and feedback from the closed-loop system prevent a causal reading. [S1]

**Q39. What would demonstrate explanation faithfulness?** **Planned:** Compare prediction changes after removing selected evidence against matched random removals, and audit whether dependent features also change. **Limit:** The selected snapshot reports no completed independent faithfulness evaluation. [S1] [S18]

**Q40. What would demonstrate clinical usefulness?** **Planned:** Freeze a threshold on development data, simulate alerts chronologically, measure false-alert burden, episode detection, lead time, calibration, and external performance. **Limit:** AP and Brier alone cannot establish it. [S1] [S7]

**Q41. Why avoid pooling nine fold-seed pairs as independent?** **Method reasoning:** The same validation people appear under both seeds, and fold training sets overlap. **Limit:** A naive pooled interval would overstate independent information. [S1]

**Q42. Why did the earlier two-epoch sequence matter?** **Observed in development:** Its AP improved substantially from epoch 1 to epoch 2. **Inference:** One-epoch graph-versus-sequence gaps may partly reflect learning speed. [S1]

**Q43. Why is the final group called reserved rather than fully untouched?** **Observed in development:** Aggregate eligibility and label-coverage audits included it, but no model-performance result was reported. **Limit:** Avoid claiming zero inspection of any kind. [S1]

**Q44. What would external validation require?** **Planned:** Freeze source-trained preprocessing, model, calibration, and threshold; harmonize available fields; then score a distinct dataset without tuning to its outcomes. **Limit:** No such evaluation appears in the selected snapshot. [S7]

**Q45. Does an interval excluding zero prove a general graph effect?** **No.** **Observed in development:** It supports a paired difference for fixed fitted predictions and participants. **Limit:** It does not resolve architecture, refitting, or transportability. [S1] [S4]

### Adversarial questions

**Q46. Are you calling an ordinary temporal link a knowledge graph?** **Answer:** The repository name uses that phrase, but the executed model is a temporal event graph. I do not claim a validated ontology or causal clinical relation. [S1] [S5]

**Q47. Could the sequence model simply be weak?** **Answer:** Yes. It is parameter matched and equally informed, but it fuses late and may optimize differently. Stronger aligned sequence controls remain necessary. [S1]

**Q48. Could your graph just exploit more data?** **Answer:** The paired graph and sequence fits use the same retained windows, CGM values and masks, and event tokens. Their representations differ. That controls data membership, not all architectural effects. [S1] [S15]

**Q49. Did you peek at the final holdout?** **Answer:** The snapshot reports aggregate coverage audits involving the reserved group, but no model-performance evaluation on its 183 people. I would describe its performance as unopened, not every characteristic as unseen. [S1]

**Q50. Why should I trust millions of windows?** **Answer:** I do not treat them as millions of independent patients. Participant-macro metrics and participant bootstrap address some dependence. The independent-person count and overlapping fold design still limit inference. [S1]

**Q51. Does the result show that insulin and meals improve prediction?** **Answer:** No. It shows one multimodal graph beat one multimodal sequence comparator. A strong matched CGM-only contrast is needed for incremental event value. [S1]

**Q52. Why did typed routing lose if your theory values clinical relations?** **Answer:** The tested type labels were already in the inputs, and hard expert selection may have constrained learning. The negative pilot narrows the claim and motivates better relation controls. [S1]

**Q53. Could a future event leak through the data tables?** **Answer:** The event contract filters occurrence times to `≤t`. Actual availability at `t` is not verified, which is a separate retrospective replay limitation. [S1] [S8]

**Q54. Are the explanations clinically meaningful?** **Answer:** That is unverified. A visible edge is a time link, not a clinician-approved causal explanation. Faithfulness and human review are future evaluations. [S1] [S18]

**Q55. Can this model recommend insulin?** **Answer:** No. It estimates a CGM threshold risk under retrospective assumptions. It does not estimate treatment effects or a dosing policy. [S1]

**Q56. Is your result novel?** **Answer:** Broad graph and event-aware diabetes prediction ideas predate this study. The candidate contribution is the auditable matched comparison and the specific empirical question. A systematic absence-of-prior-work claim is not established. [S1] [S10]

**Q57. Why quote a positive result when a later run might disagree?** **Answer:** The document is explicitly frozen to the 20 October pushed snapshot. I would check newer pushed evidence before describing today's project status. [S1] [S2]

**Q58. Are your confidence intervals too narrow?** **Answer:** They can be narrow because they resample participants around fixed predictions. They do not include retraining, seed variation, or architecture search, so I would never present them as total uncertainty. [S1] [S4]

**Q59. Why did you not evaluate severe hypoglycemia?** **Answer:** The source CGM threshold alone cannot establish a clinical severe event that requires assistance. The reported endpoint is a narrower observed glucose condition. [S1] [S7]

**Q60. What is the next decisive experiment?** **Planned:** Train a time-aligned non-graph control and a strong CGM-only control under the same frozen windows, input policy, and adequate training schedule. Then test whether any graph advantage survives. [S1] [S10]

## 10. Research relevance to Professor Rachel Richesson

The provided Scholar URL identifies Professor Rachel Richesson as the interview reference. This module keeps the connection focused. Her published work and teaching material emphasize explicit computable definitions, data quality, standards, and the use of real-world clinical data for research. A PubMed-indexed article coauthored by Richesson discusses heterogeneous EHR sources, explicit phenotype definitions, governance, and data quality. A Duke-hosted transcript explains a computable phenotype as a specified rule built from data fields and temporal logic. These are relevant **methodological themes**. They are not evidence that she has studied this Loop graph or would endorse it. [P1] [P2]

A second bridge is data provenance. The project records duplicate handling, conflicting timestamps, unit conversion, source identifiers, modality presence, and availability assumptions. Those details decide whether an apparent finding is reproducible. They also affect transport to a different dataset. An interview answer might say: “I am interested in prediction models, but my experience here taught me that data definitions and quality rules determine what a model result means. I would like to study methods that make those rules portable and testable across real-world sources.” That is a research interest statement, not a claim of prior collaboration. [S1] [P1]

## 11. Interview interruptions

If interrupted after the headline result, say: “The graph beat one matched late-fusion sequence model in the completed development pairs. The key limit is that I still need a time-aligned non-graph control.” If asked for numbers, say: “All five first-seed folds favored the graph on macro AP and Brier; four second-seed folds were complete. The first-seed mean AP difference was about `+0.0865`.” If asked about readiness, say: “There is no reported final holdout, external, alert, or explanation-fidelity result in this snapshot.” [S1] [S4]

If challenged on “knowledge graph,” say: “The evaluated edges are deterministic time associations. I call the executed model a temporal event graph.” If challenged on the typed pilot, say: “Type was already in both variants' inputs. Hard type routing lost in one fold, so I do not claim a typed-relation benefit.” If asked about a newer result, say: “This document is pinned to the 20 October pushed snapshot; I would verify the newer archive before changing the answer.” [S1]

Expect follow-ups on boundaries. The history is `(t−120, t]`; the outcome uses six fully observed slots at `t+5` through `t+30`; exactly 70 is negative. Basal is recorded pump state, not modeled insulin exposure. A bootstrap interval resamples participants with predictions fixed. These exact definitions usually matter more than another layer name. [S1]

**Useful counterquestions:**

1. “What evidence would you want before calling a device-derived prediction target portable across health systems?”
2. “How would you audit data quality when event occurrence and actual availability times differ?”
3. “Which next validation would be most informative for a retrospective ranking result without measured alert performance?”
4. “How do you judge whether an easy-to-compute outcome matches the clinical decision it is meant to support?”
5. “Would your program support research that combines phenotype and provenance methods with controlled model comparisons?”

These questions explore research fit. They do not assume agreement with the present graph architecture.

## 12. Evidence and verification

### Source hierarchy and claim ledger

The pushed manuscript and CSV report results; the verification JSON records aggregate checks. Protected predictions and the nine paired-audit JSON files are absent from the pushed commit. The comparisons cannot be recomputed from pushed material alone. [S1] [S2] [S4]

| Claim | Status at evidence boundary | Best source | What still needs checking |
| --- | --- | --- | --- |
| The analytic development set has 652 people, 44,028,064 windows, and 1,296,297 positive labels. | Observed in development | [S1], section 3.1 | Independent rebuild from release and protected index if preparing a submission. |
| The final-performance group has 183 people and no reported performance evaluation. | Observed in development | [S1], sections 2.1 and 4.1; [S6] | Confirm no later pushed final evaluation before any current-status answer. |
| The index label is any `<70 mg/dL` value in six fully observed future slots. | Implemented | [S1], section 2.3; [S7] | Check target code and any newer protocol version before reuse. |
| Main graph and sequence comparators each have 36,883 parameters. | Implemented and verified in the snapshot | [S1], sections 2.6–2.8; [S2] | Recount if architecture code changes. |
| Graph beat the sequence model in five first-seed and four second-seed completed validation pairs. | Reported development result | [S4], nine aggregate rows; [S1], section 3 | Protected predictions and paired-audit JSON are not pushed; independently recheck them before publication. |
| Typed routing underperformed generic routing in a one-fold pilot. | Observed in development with archive limit | [S1], section 3.4; [S2] | Recover and independently audit raw typed-pilot predictions if needed. |
| Events were usable at occurrence time in the retrospective replay. | Implemented assumption | [S1], section 2.4; [S8] | Measure actual availability in a suitable source or report delay scenarios as simulations. |
| The graph's edges have causal or validated clinical meaning. | Unverified | [S1], sections 2.6 and 4 | Requires a separately justified relation model and validation. |
| The model improves useful alerts or patient outcomes. | Unverified | [S1], section 4 | Requires alert, calibration, external, and prospective evidence. |
| Formal author roles, local ethics determination, and funding are known. | Unverified | [S1], Declarations; [S2] | Obtain author-approved declarations. |

### Committed project sources

- <a id="s1"></a> **[S1]** [Working manuscript, evidence snapshot 20 October 2026](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/manuscript/manuscript.md). Main narrative, operational definitions, tables, discussion, and declaration placeholders.
- <a id="s2"></a> **[S2]** [Manuscript README](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/manuscript/README.md) and [verification record](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/manuscript/verification.json). Snapshot scope, nine paired comparisons, checked contracts, and verification limits.
- <a id="s3"></a> **[S3]** [Committed repository README](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/README.md). Earlier implementation orientation. It predates the manuscript result and must not override the latter's dated results.
- <a id="s4"></a> **[S4]** [Full-precision results snapshot](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/manuscript/results_snapshot.csv). Nine graph-versus-sequence fold-seed rows with AP and Brier contrasts and conditional bootstrap intervals.
- <a id="s5"></a> **[S5]** [Graph schema](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/docs/graph_schema.md). Proposed semantic and provenance boundaries; do not confuse its proposed schema with the executed neural graph.
- <a id="s6"></a> **[S6]** [Model split record](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/docs/loop_model_split.md). Participant counts, reserved group policy, and manifest checksum.
- <a id="s7"></a> **[S7]** [Research protocol](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/docs/research_protocol.md). Proposed label and later alert-analysis definitions. Where its early filling proposal differs from executed models, [S1] governs this module.
- <a id="s8"></a> **[S8]** [Upload-linkage audit](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/docs/loop_upload_linkage_audit.md). Why observed event availability could not be established.
- <a id="s9"></a> **[S9]** [Earlier neural training workflow](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/kaggle_event_sequence_gru/train_controlled.py) and [controlled comparison entrypoint](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/kaggle_event_sequence_gru/ONE_CELL_CONTROLLED_COMPARISON.py). These pushed files do **not** contain the exact graph-versus-sequence training implementation; use [S1] for its reported architecture.
- <a id="s10"></a> **[S10]** [Decisive experiment specification](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/docs/decisive_experiments.md). Planned controls separating timing, information, architecture, and relation effects.
- <a id="s11"></a> **[S11]** [Loop release audit](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/docs/loop_release_audit.md) and [canonicalization specification](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/docs/loop_canonicalization_spec.md). Source fields, duplicate logic, chronology, and provenance.
- <a id="s12"></a> **[S12]** [CGM range policy](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/docs/loop_cgm_range_policy.md). Primary numeric-value and sensitivity policy.
- <a id="s13"></a> **[S13]** [Temporal eligibility specification](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/docs/loop_temporal_eligibility_spec.md). Logical grid and window rules.
- <a id="s14"></a> **[S14]** [Event-instance cache contract](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/docs/loop_event_instance_cache.md) and [event sequence contract](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/docs/loop_event_sequence_contract.md). Event instances, missing values, ordering, and truncation; [S1] governs the reported 64-event neural configuration.
- <a id="s15"></a> **[S15]** [Neural content and checkpoint guards](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/src/t1d_tkg/neural_contract.py), [manifest utility](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/src/t1d_tkg/manifest.py), and [prediction archive validator](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/src/t1d_tkg/archive.py).
- <a id="s16"></a> **[S16]** [Controlled neural experiment record](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/docs/loop_controlled_neural_experiments.md) and [archive comparator](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/scripts/compare_controlled_neural_archives.py).
- <a id="s17"></a> **[S17]** [Metric implementation](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/src/t1d_tkg/metrics.py) and [uncertainty implementation](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/src/t1d_tkg/uncertainty.py).
- <a id="s18"></a> **[S18]** [Explanation helper code](https://github.com/pronabroy360/Temporal-Patient-Centric-Knowledge-Graph-for-Explainable-Hypoglycemia-Prediction-in-T1D/blob/eb49dd1/src/t1d_tkg/explanations.py). Software support is not a completed explanation-fidelity evaluation.

### Small external source set

- <a id="p1"></a> **[P1]** Richesson and colleagues, [“Clinical research informatics and electronic health record data”](https://pubmed.ncbi.nlm.nih.gov/25123746/). Use for the broad methodological connection to heterogeneous sources, phenotype definitions, governance, standards, and data quality.
- <a id="p2"></a> **[P2]** Duke-hosted [“What Is a Computable Phenotype?” transcript](https://dcricollab.dcri.duke.edu/sites/NIHKR/KR/What%20Is%20a%20Computable%20Phenotype_transcript.pdf), featuring Rachel Richesson. Use for the need to specify computable event definitions, fields, and temporal logic. Do not imply that the Loop target has been deployed as an EHR phenotype.

### Glossary for a human or AI reader

| Term | Meaning in this module |
| --- | --- |
| AP | Stepwise average precision; a ranking summary from precision and recall. Person-level AP is undefined without positive labels. |
| Brier score | Average squared difference between predicted probability and binary outcome. Lower is better. |
| CGM | Continuous glucose monitoring; the timestamped glucose source for history and labels. |
| Canonicalization | Release-specific rules that choose a consistent representation of repeated or conflicting source records. |
| Development fold | One patient-disjoint train, validation, and internal test configuration used for exploration. |
| Event instance | One retained recorded basal, bolus, or food occurrence with its own time and provenance. |
| Event availability | The first time a system could have used a recorded event. It was not validated for this Loop comparison. |
| Graph edge | A deterministic link from an event to a nearby observed CGM slot; not a treatment-effect claim. |
| Holdout | The 183-person group reserved for final model-performance evaluation in the selected snapshot. |
| Incident-within-horizon target | Any future threshold crossing after an eligible non-low index, subject to complete future coverage. |
| Macro metric | A measure calculated within each person, then averaged with equal person weight. |
| Occurrence-time replay | Retrospective assumption that a recorded event was usable when it happened. |
| Provenance | Source identity and transformation history needed to trace an analytic value. |
| Typed routing | Message expert selected by event modality; tested separately from the main graph-versus-sequence comparison. |

### Safe answer rule for an AI agent

When a question asks for a fact outside this evidence boundary, answer: **“The pushed 20 October 2026 snapshot does not establish that.”** Then state the closest supported fact and name the missing verification. If a question asks for a current result, check the latest remote commit before using this module. If a question asks whether the graph is causal, clinically validated, externally validated, explanation-faithful, or proven novel, do not infer yes from the development AP table. If a question requests personal authorship, ethics approval, or funding details, ask the researcher to supply them. Never turn a planned experiment into an observed finding.

[S1]: #s1
[S2]: #s2
[S3]: #s3
[S4]: #s4
[S5]: #s5
[S6]: #s6
[S7]: #s7
[S8]: #s8
[S9]: #s9
[S10]: #s10
[S11]: #s11
[S12]: #s12
[S13]: #s13
[S14]: #s14
[S15]: #s15
[S16]: #s16
[S17]: #s17
[S18]: #s18
[P1]: #p1
[P2]: #p2
