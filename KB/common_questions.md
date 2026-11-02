# Common PhD Interview Questions

Suggested answers for a conversation with Professor Rachel Richesson. Keep completed work, current research, and future plans distinct.

## 1. What is a computable phenotype?

A computable phenotype is a set of rules for identifying patients or populations with a condition or characteristic using data routinely collected in EHRs or related sources. It is an EHR-based condition definition.

## 2. How would you validate a computable phenotype?

**Suggested answer:** The validation strategy depends on its purpose. If the goal is clinical classification, I would ideally define an appropriate reference standard, such as clinician-adjudicated chart review, and estimate sensitivity, specificity, positive predictive value (PPV), and negative predictive value (NPV), or whichever measures matter for the intended use. I would also examine error patterns and whether performance varies by site or subgroup.

If patient-level reference data are unavailable, I would treat that as a limitation rather than pretending distributional similarity proves validity.

**Reminder:** Do not lead with Jaccard similarity as proof of clinical validity.

## 3. Would OMOP, FHIR, and standard vocabularies make phenotype portability problems disappear?

**Suggested answer:** They remove important classes of technical heterogeneity, but they do not guarantee clinical equivalence. A common model can make an algorithm easier to implement, but sites can still differ in what gets recorded, why and when it gets recorded, which populations receive particular tests, and how faithfully local mappings represent source data. I view standardization as necessary infrastructure for portability, but not sufficient evidence of phenotype validity.

## 4. What is the most interesting part of your MIMIC-IV data warehouse?

The part most relevant to my research interests is that I tried to make cohort construction explicit and reproducible. The pipeline separates source ingestion, cleaned clinical tables, analytical marts, cohort logic, and first-24-hour feature generation. I learned that choices that look like data engineering details, such as index time, inclusion windows, ICU stay selection, and duplicate handling, are actually study-definition decisions.

## 5. Did you validate a phenotype?

Not in the clinical-validation sense. I validated pipeline logic and reproducibility, but I did not perform chart-adjudicated phenotype validation. That gap is one reason I am interested in learning rigorous phenotype validation during doctoral training.

## 6. What did you learn from the DE-SynPuf project?

Methodologically, it is useful for reproducible longitudinal pipeline design, temporal train/test separation, claims feature construction, calibration workflows, and software testing. I would not use it to make clinical-effectiveness or population-health claims because the data are synthetic.

## 7. What are you doing in your Wayne State research internship?

The central hypothesis is whether typed temporal relations add value beyond strong non-graph temporal baselines. We do not yet have evidence that they do. The project is still in the controlled-evaluation stage. We have been establishing baselines, leakage controls, dataset audits, and development splits before making graph claims.

## 8. Why use a patient-centric knowledge graph?

The hypothesis is not that a graph is automatically better. Patient data contain different event types and clinically meaningful time relations that a graph can represent explicitly. The graph only earns its complexity if controlled experiments show added predictive or explanatory value beyond simpler baselines.

## 9. How is CancerOmicsLake relevant to phenotype portability?

CancerOmicsLake is less directly related to phenotype portability, but it reflects the same engineering approach: provenance, staged transformations, quality checks, reproducibility, and keeping analytical conclusions traceable to data processing.

## 10. What is your research question?

Under what conditions does a computable phenotype that is fit for purpose in one healthcare setting remain fit for purpose when reused in another?

## 11. Tell me about yourself.

Thank you for meeting with me, Professor Richesson. My background is computer science, but my work has increasingly moved toward clinical informatics. At Commure, I supported 38 U.S. healthcare-site launches and repeatedly saw differences in EHR documentation, coding, workflows, and data quality. That made me interested in what happens when we reuse clinical definitions across institutions.

I then built MIMIC-IV and CMS claims projects around reproducible longitudinal cohorts, and I am currently studying patient-centric knowledge graphs for hypoglycemia prediction at Wayne State. Across these experiences, the question I keep returning to is: when a computable phenotype is transferred to another institution, how do we know it still represents the same clinical population?

Your work on phenotype validation, real-world data, and documenting local adaptations strongly matches that question. I would love to understand whether you see this as a useful HILS PhD direction and where you think the most important methodological gap is.

## 12. What is your EHR experience?

My role was operational rather than a formal research study, so I want to be careful not to overstate it. I worked with site-specific healthcare data used in onboarding and validation. Across sites, the same general concepts—encounters, diagnoses, procedures, and claims—could differ in how they appeared, how completely fields were populated, or where relevant information was represented.

My job involved Python and SQL extraction and validation. Some of that work was finding why expected records or mappings did not behave consistently between sites. That is where I became interested in the difference between standardization on paper and equivalence for downstream analysis.

I did not formally measure phenotype portability there. The research question came afterward: how would we quantify whether those local differences change who gets included in a clinical cohort?
