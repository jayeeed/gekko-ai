---
document_id: PRONAB-CV-RAG-001
title: "Pronab Chandra Roy — Academic CV and PhD Interview Knowledge Base"
document_type: "cv_profile_interview_qa"
candidate: "Pronab Chandra Roy"
target_program: "University of Michigan — Health Infrastructures and Learning Systems (HILS) PhD"
target_entry: "Fall 2027"
faculty_context: "Professor Rachel Richesson"
source: "Candidate-provided LaTeX academic CV"
source_status: "Self-reported CV; external verification not performed"
last_source_date: "2026-11-01"
language: "en"
tags:
  - academic-background
  - phd-interview
  - clinical-informatics
  - healthcare-data
  - research-experience
  - professional-experience
  - computational-phenotyping
  - longitudinal-ehr
  - knowledge-graphs
  - real-world-evidence
  - research-fit
---

# Pronab Chandra Roy — Academic CV and PhD Interview Knowledge Base

## 1. Purpose and Retrieval Instructions

This document is a CV-grounded knowledge base for answering questions during academic and PhD research conversations, particularly an introductory meeting with Professor Rachel Richesson at the University of Michigan.

It provides:

- Verified-as-stated-in-CV facts about education, research, employment, publications, projects, skills, and achievements.
- Interview-ready responses grounded in those facts.
- Connections between professional experience and prospective doctoral research.
- Clear distinctions between completed work, ongoing research, and future interests.
- Questions requiring further confirmation before making detailed claims.

### Evidence rules

**CV-supported:** Explicitly stated in the candidate-provided CV.

**Interpretation:** A reasonable explanation or synthesis of CV-supported facts, not a separately verified result.

**Proposed:** A future research direction or possible methodological extension.

**Needs confirmation:** A detail that cannot be established from the CV alone.

The RAG assistant must never convert a proposed method into a completed result, infer an unpublished experiment, invent a model metric, or attribute an unverified contribution to the candidate.

When answering technical questions about a specific project, retrieve the corresponding project-level Markdown documentation in addition to this file.

---

# 2. Canonical Candidate Profile

## 2.1 Identity and professional profile

**Name:** Pronab Chandra Roy  
**Location:** Dhaka, Bangladesh  
**Website:** https://pronab.me  
**GitHub:** https://github.com/pronabroy360  
**LinkedIn:** https://www.linkedin.com/in/pronab-ch-roy-3409091a0/

**Academic background:** Bachelor of Technology in Computer Science and Engineering from the National Institute of Technology Silchar, India.

**Current roles:**
- Research Intern, Wayne State University, remote, 2026–present.
- AI Data Engineer, ACI PLC R&D AI Lab, January 2026–present.

**Previous role:**
- Operations Data Analyst, Commure, July 2024–January 2026.

**Research interests:**
- Large language models for healthcare.
- Longitudinal electronic health record modeling.
- Patient-centric biomedical knowledge graphs.
- Reliable biomedical evidence synthesis.
- Healthcare data science.

**Prospective academic direction:** Doctoral research in clinical informatics, health data science, clinical data quality, knowledge representation, and reproducible evidence generation.

The prospective academic direction is an interpretation of the stated interests and project portfolio, not a claim of admission or an established research appointment.

## 2.2 Education

**Institution:** National Institute of Technology Silchar, India.  
**Degree:** B.Tech, Computer Science and Engineering.  
**Dates:** 2020–2024.  
**CGPA:** 8.71/10.00.  
**Standing:** Top 5% of cohort.  
**Funding:** Fully funded ICCR Scholarship, Government of India, 2020–2024.

**Undergraduate thesis:** *Advanced Image Denoising through Combined Directional Wavelet-based NLM and BM3D Technique.*

The thesis studied directional wavelet subbands combined with non-local means and BM3D.

## 2.3 Publication

**Title:** *Combining Haar Transform and Row-Column Directional RLE in Image Compression.*

**Authors:** A. D. Emon, P. C. Roy, L. D. Singh, and A. K. Saha.

**Venue:** 2023 International Conference on Informatics and Computing (ICIC), IEEE, 2023.

**Publication link:** https://ieeexplore.ieee.org/document/10382031

The CV identifies the candidate's contribution as image-compression experimentation, experimental evaluation, and manuscript preparation during the S. N. Bose Summer Internship.

Do not claim that the candidate was first author, sole algorithm designer, or principal investigator.

## 2.4 Research experience

### Wayne State University

**Role:** Research Intern, remote.  
**Dates:** 2026–present.  
**Supervisor:** Dr. Lihui Liu.  
**Area:** Graph-Based Clinical Data Mining.

**CV-supported research description:**

Studying patient-centric knowledge graphs for explainable hypoglycemia prediction in Type 1 diabetes, focusing on heterogeneous clinical information and longitudinal relationships.

**Status:** Ongoing research.

**Not established from CV alone:**
- Dataset identity.
- Exact graph schema.
- Prediction horizon.
- Hypoglycemia label definition.
- Implemented graph algorithms.
- Model architecture.
- Training results.
- Clinical validation.
- External validation.
- Candidate's exact individual code contributions.

Retrieve the Wayne State project-specific documentation before answering these questions.

### S. N. Bose Summer Internship

**Institution:** National Institute of Technology Silchar.  
**Dates:** May–July 2023.  
**Mentor:** Dr. Anish Kumar Saha.

**Contributions:**
- Conducted experiments combining Haar transform and row-column directional run-length encoding.
- Studied relationships between transform representations and encoding strategies.
- Contributed to experimental evaluation and manuscript preparation.

**Output:** Research contributing to the IEEE ICIC 2023 publication.

---

# 3. Professional Experience

## 3.1 ACI PLC — AI Data Engineer

**Organization:** ACI PLC, R&D AI Lab.  
**Dates:** January 2026–present.  
**Location:** Dhaka, Bangladesh.

**CV-supported responsibilities:**
- Python and SQL ETL/ELT pipelines.
- Analytical datasets and reusable data marts.
- Dimensional modeling.
- AWS S3 and Redshift.
- On-premises databases.
- Indexing, partition pruning, and query-plan analysis.
- NVIDIA Blackwell GPU use in data-intensive R&D workflows.

**Related project:** Healthcare RxPERT, an AI-assisted pharmaceutical research and development platform.

**Important distinction:** General data engineering responsibilities and RxPERT-specific contributions should be documented separately.

## 3.2 Commure — Operations Data Analyst

**Organization:** Commure, U.S. healthcare revenue cycle management.  
**Dates:** July 2024–January 2026.

**CV-supported responsibilities and outcomes:**
- Supported 38 U.S. healthcare-site launches.
- Automated healthcare data extraction and validation with Python and SQL.
- Reduced manual QA effort by approximately 70%.
- Worked with encounters, diagnoses, procedures, and claims.
- Worked with EHR platforms including Epic and Cerner.
- Processed HL7 and X12 837 data.
- Investigated differences in documentation, coding, and data quality across sites.

**Research relevance:** Direct practical exposure to heterogeneous clinical and administrative data and differences in how healthcare sites document and exchange information.

**Important limitation:** The CV does not claim that the candidate conducted a formal multicenter computable phenotype validation or portability study.

---

# 4. Selected Projects

## PRJ-01 — Healthcare RxPERT

**Name:** Healthcare RxPERT — AI-Assisted Pharmaceutical R&D Platform.

**Status:** Ongoing development at ACI PLC R&D AI Lab.

**Platform:** https://rxpert.acimisai.com/login

**CV-supported scope:**
- Literature evidence synthesis.
- Reference-product analysis.
- Quality Target Product Profile (QTPP) and Critical Quality Attribute (CQA) assessment.
- Active pharmaceutical ingredient selection.
- Formulation compatibility.
- Design of Experiments.
- Risk assessment.
- Structured recommendations.
- Traceable citations.
- Reproducible report generation.

**Do not claim:** Regulatory approval, clinical validation, autonomous scientific decision-making, or verified literature accuracy unless independently established.

## PRJ-02 — MIMIC-IV Clinical Data Warehouse

**Repository:** https://github.com/pronabroy360/MIMIC-IV-Clinical-DW

**CV-supported scope:**
- Layered DuckDB warehouse.
- Reproducible cohort definitions.
- First-24-hour feature extraction.
- FastAPI and Streamlit aggregate analytics.
- LocalStack S3 ingestion path.
- SQL-access guardrails.
- GitHub Actions checks.

**Research relevance:** Reproducibility, clinical data transformation, cohort construction, and temporal feature engineering.

**Do not claim:** Validated clinical phenotypes or external portability unless supported by additional evidence.

## PRJ-03 — CMS DE-SynPUF

**Repository:** https://github.com/pronabroy360/CMS-DESynPuf

**CV-supported scope:**
- Synthetic Medicare claims.
- Reproducible patient-year pipeline.
- 227,292 modeling records.
- Temporally separated training and test cohorts.
- Utilization, cost, diagnosis, and chronic-condition features.
- Predictive model comparison.
- Calibration, threshold, and feature-importance analyses.

**Important limitation:** Results from synthetic claims data cannot independently establish real-world clinical validity.

## PRJ-04 — CancerOmicsLake

**Repository:** https://github.com/pronabroy360/CancerOmicsLake

**CV-supported scope:**
- Cancer-expression data integration.
- TCGA, GTEx, and recount3.
- BRCA, LUAD, and COAD.
- 108,012 cancer–gene pairs.
- Bootstrap stability analysis.
- Mann–Whitney testing.
- False-discovery-rate correction.
- Expression, mutation, and replication evidence.
- Traceability from data processing to analytical results.

**Important limitation:** Statistical evidence and computational prioritization do not establish clinical biomarker validation.

## PRJ-05 — Databricks Medallion Lakehouse Pipeline

**Repository:** https://github.com/pronabroy360/dbricks_medallion_restaurants

**CV-supported scope:**
- Bronze, Silver, and Gold data layers.
- Apache Spark and Databricks.
- PySpark transformations.
- ETL/ELT workflows.
- Dimensional modeling.
- Delta Lake schema evolution.
- Query optimization.

**Important limitation:** This is a general data engineering project, not a healthcare dataset or validated clinical application.

---

# 5. Technical Skills

## Programming

- Python.
- SQL.

## Healthcare data

- EHR and claims data.
- HL7.
- X12 837.
- Clinical cohort construction.
- Longitudinal feature engineering.

## Statistics and modeling

- Bootstrap resampling.
- Mann–Whitney testing.
- False-discovery-rate correction.
- Predictive modeling.
- Calibration.
- Model evaluation.

## Distributed data and storage

- Apache Spark.
- Kafka.
- Airflow.
- Databricks.
- Delta Lake.
- DuckDB.
- PostgreSQL.
- Familiarity with Apache Flink.

## Infrastructure

- Linux.
- Git.
- Docker.
- AWS S3, EC2, Lambda, and Redshift.
- FastAPI.
- pytest.
- GitHub Actions.

**Retrieval rule:** A skill listed in the CV does not establish a particular level of mastery or prove that the skill was used in every project.

---

# 6. Honors and Achievements

- ICCR Scholarship, Government of India: fully funded undergraduate scholarship, 2020–2024.
- Smart India Hackathon regional winner and team lead for a computer-vision security project.
- LeetCode Knight, 1900+ rating, four Global Top 500 contest finishes.
- CodeChef 3-Star, 1600+ rating.
- DataCamp Data Engineer Certification.
- DeepLearning.AI Deep Learning Specialization.
- IBM Machine Learning with Apache Spark.

---

# 7. Academic and Career Interview Q&A

## CV-Q001 — Tell me about yourself.

**Category:** Personal introduction  
**Priority:** Critical  
**Evidence:** CV-supported; synthesis is interpretive.

**Question:** Can you briefly introduce yourself?

**Answer:**

I completed my B.Tech in Computer Science and Engineering at NIT Silchar, where I graduated with an 8.71 CGPA and ranked in the top 5% of my cohort. My early research involved image processing and led to a coauthored IEEE conference publication.

After graduation, I worked at Commure with U.S. healthcare data, including EHR and claims information across multiple sites. That experience exposed me to challenges involving documentation, coding, and data quality.

I now work as an AI Data Engineer at ACI PLC and am also conducting research at Wayne State University on patient-centric knowledge graphs for Type 1 diabetes. Across these experiences, I've become increasingly interested in the reliability of clinical data and how we can use it for reproducible, meaningful research.

**Likely follow-up:** What connects your professional experience to your research interests?

**Answer:** The common thread is working with complex data and recognizing that correct processing alone does not guarantee meaningful interpretation.

---

## CV-Q002 — Why pursue a PhD?

**Category:** Research motivation  
**Priority:** Critical  
**Evidence:** Interpretive; candidate should personalize.

**Question:** Why do you want a PhD rather than continuing in industry?

**Answer:**

My professional work has given me experience building reliable data pipelines and working with heterogeneous healthcare information. However, I want to investigate deeper methodological questions: how clinical concepts are represented in routinely collected data, how data quality affects research conclusions, and how we determine whether those conclusions remain valid across settings.

A PhD would allow me to develop and evaluate new research methods rather than focusing primarily on implementation and operational delivery.

**Follow-up:** What scientific question would you investigate?

**Answer:** One possible direction is studying how differences in clinical coding, observation availability, and temporal documentation affect the portability of computable phenotypes across institutions.

**Status:** Proposed research interest, not completed work.

---

## CV-Q003 — Why healthcare informatics?

**Category:** Research motivation  
**Priority:** Critical

**Question:** Why did you move toward healthcare informatics?

**Answer:**

My experience at Commure brought me into direct contact with encounters, diagnoses, procedures, and claims from U.S. healthcare settings. I saw that the structure and quality of these records can differ across sites.

My later projects in MIMIC-IV, claims modeling, and biomedical knowledge representation gave me opportunities to explore these issues from a research and technical perspective.

That combination motivated my interest in clinical informatics, where data engineering, clinical meaning, and research validity intersect.

---

## CV-Q004 — Why Professor Richesson's research?

**Category:** Faculty alignment  
**Priority:** Critical  
**Evidence:** Candidate's stated interests plus faculty research context; not a claim about faculty preferences.

**Question:** Why are you interested in Professor Richesson's work?

**Answer:**

I'm particularly interested in research on clinical data quality, standardization, computable phenotypes, and the use of real-world healthcare data for research.

My experience at Commure exposed me to variation in documentation and coding across sites. My MIMIC-IV and CMS projects strengthened my interest in reproducible cohort definitions and longitudinal data.

I would like to investigate how we can determine whether a clinical definition remains valid when it is transferred between institutions, especially when data capture and documentation practices differ.

---

## CV-Q005 — Why the HILS PhD?

**Category:** Program fit  
**Priority:** High  
**Evidence:** Interpretive; verify program-specific details separately.

**Question:** Why are you interested in the Health Infrastructures and Learning Systems PhD?

**Answer:**

My interests sit between technical health data systems and the clinical and organizational settings where those systems are used.

I want to study how health information is represented, validated, and reused to support reliable evidence generation. An interdisciplinary learning health systems environment is attractive because those problems require more than machine learning or database engineering alone.

---

## CV-Q006 — What is your strongest preparation for doctoral research?

**Category:** Research readiness  
**Priority:** High

**Question:** What experience best prepares you for a PhD?

**Answer:**

I would highlight the combination of early academic research, production healthcare data experience, and independent technical projects.

My undergraduate research introduced me to experimentation and scholarly writing. At Commure, I worked with real operational data-quality problems. My later healthcare projects required attention to cohort definitions, longitudinal structure, reproducibility, and evaluation.

These experiences give me a practical foundation, while also showing me where I need deeper methodological research training.

---

## CV-Q007 — What is your biggest research weakness?

**Category:** Research maturity  
**Priority:** High

**Question:** What area do you most need to develop?

**Answer:**

I have substantial experience with software and data engineering, but I want to deepen my training in rigorous clinical research design, measurement validity, causal reasoning, and external validation.

I see these as essential for moving from building technically reproducible systems to producing trustworthy scientific evidence.

**Note:** This is a suggested reflective answer. Confirm that it accurately represents the candidate's self-assessment.

---

## CV-Q008 — What is the connection among your projects?

**Category:** Research narrative  
**Priority:** Critical

**Question:** Your projects cover image processing, claims, genomics, data warehouses, and knowledge graphs. What connects them?

**Answer:**

The domains vary, but a recurring theme is extracting reliable information from complex data.

My earlier image-processing research focused on representations and algorithms. My data engineering work developed my ability to build reproducible processing systems. Healthcare and biomedical projects made me more aware that data have clinical or scientific meaning that can be lost through inappropriate transformation.

My current research interests bring those experiences together around trustworthy healthcare data representation and evidence generation.

---

# 8. Education and Undergraduate Research Q&A

## CV-Q009 — Why did you study at NIT Silchar?

**Question:** Tell me about your undergraduate education.

**Answer:**

I completed my B.Tech in Computer Science and Engineering at NIT Silchar between 2020 and 2024. I studied there with support from a fully funded ICCR scholarship and graduated with an 8.71 CGPA, placing in the top 5% of my cohort.

The program gave me a foundation in algorithms, computing, and research-oriented problem solving.

**Evidence:** CV-supported.

---

## CV-Q010 — What was your undergraduate thesis?

**Question:** What did you study in your undergraduate thesis?

**Answer:**

My thesis studied image denoising using directional wavelet subbands combined with non-local means and BM3D techniques.

The work concerned how different image representations and denoising methods could be combined.

**Follow-up:** What were your exact results?

**Answer:** Requires consultation of the thesis and experimental records. The CV does not provide quantitative findings.

---

## CV-Q011 — Tell me about your IEEE publication.

**Question:** What was your IEEE ICIC 2023 paper about?

**Answer:**

The paper was titled *Combining Haar Transform and Row-Column Directional RLE in Image Compression*.

During my S. N. Bose Summer Internship, I conducted image-compression experiments, studied relationships between transform representations and encoding strategies, and contributed to experimental evaluation and manuscript preparation.

**Follow-up:** What was your exact individual contribution?

**Answer:** The CV establishes experimentation, evaluation, and manuscript preparation. More granular authorship responsibilities require confirmation.

---

## CV-Q012 — What did your first research experience teach you?

**Question:** What did you learn from the S. N. Bose internship?

**Answer:**

It gave me early exposure to structured experimentation and preparing technical work for academic publication.

The most transferable lesson was that an algorithmic idea needs systematic evaluation and clear communication before it becomes a defensible research contribution.

**Status:** Interpretive.

---

## CV-Q013 — How is image processing relevant to healthcare data science?

**Question:** Why is your early image-processing background relevant to your current research?

**Answer:**

The clinical domain is different, but the methodological skills transfer. Image-processing research involves representations, transformations, evaluation, and understanding how methodological choices affect results.

Those same habits are useful when analyzing biomedical data, although clinical research requires additional attention to data provenance, measurement validity, and domain interpretation.

---

# 9. Wayne State Research Q&A

## CV-Q014 — What is your current research at Wayne State?

**Category:** Current research  
**Priority:** Critical

**Question:** What are you studying at Wayne State University?

**Answer:**

I am a remote research intern supervised by Dr. Lihui Liu, studying patient-centric knowledge graphs for explainable hypoglycemia prediction in Type 1 diabetes.

The focus is on heterogeneous clinical information and longitudinal relationships.

The research is ongoing, so I distinguish the research objectives from methods or results that have actually been completed.

---

## CV-Q015 — Why knowledge graphs?

**Question:** Why are you interested in patient-centric knowledge graphs?

**Answer:**

A patient-centric knowledge graph provides a way to represent patients, observations, treatments, and clinical events together with explicit relationships.

For longitudinal healthcare data, this may help preserve context that is difficult to express using simple aggregate features.

However, the usefulness of a graph must be demonstrated through appropriate comparisons and validation. A graph is not inherently more accurate or explainable.

**Evidence:** General methodological explanation; actual project implementation requires project documentation.

---

## CV-Q016 — What have you personally completed at Wayne State?

**Question:** What is your individual research contribution?

**Answer:**

The CV confirms participation in ongoing research on patient-centric knowledge graphs and longitudinal clinical relationships.

It does not establish exact code contributions, datasets, implemented algorithms, or completed experiments.

**Required response:** Retrieve the Wayne State project evidence file or ask the candidate to specify completed contributions.

**Do not invent an answer.**

---

## CV-Q017 — What makes this work clinically meaningful?

**Question:** What clinical value could this research have?

**Answer:**

A well-designed hypoglycemia prediction system could potentially support earlier identification of risk, but clinical usefulness would depend on the prediction horizon, accuracy, calibration, false-alert burden, explanation quality, and workflow context.

Those benefits are potential research motivations, not established results of the current project.

---

## CV-Q018 — How does the project connect to data quality?

**Question:** How could data-quality problems affect a patient-centric graph?

**Answer:**

Incorrect timestamps, missing observations, inconsistent units, and incomplete treatment records could produce misleading graph relationships.

A technically consistent graph can still represent incorrect clinical information. That makes provenance, temporal correctness, and source-data validation important research concerns.

---

# 10. Commure and Healthcare Data Q&A

## CV-Q019 — What did you do at Commure?

**Priority:** Critical

**Question:** What were your main responsibilities at Commure?

**Answer:**

I worked as an Operations Data Analyst in U.S. healthcare revenue cycle management from July 2024 to January 2026.

I supported 38 healthcare-site launches and worked with encounters, diagnoses, procedures, and claims across EHR platforms including Epic and Cerner.

I also automated healthcare-data extraction and validation using Python and SQL and investigated documentation, coding, and data-quality differences across sites.

---

## CV-Q020 — What does the 70% improvement mean?

**Question:** How did you reduce manual QA effort by approximately 70%?

**Answer:**

My CV reports that Python and SQL automation reduced manual QA effort by approximately 70%.

To explain the figure rigorously, I would need to describe the original manual process, the automated checks, the measurement method, and the before-and-after workload.

**Needs confirmation:** Exact measurement procedure, baseline, time period, and scope.

**Do not claim:** A 70% reduction in errors, overall operational cost, or processing latency. The stated metric is manual QA effort.

---

## CV-Q021 — What did you learn from 38 healthcare-site launches?

**Priority:** Critical

**Question:** What did supporting multiple healthcare-site launches teach you?

**Answer:**

The experience exposed me to differences in healthcare documentation, coding, and data quality across operational environments.

It helped me appreciate that two systems can exchange technically valid records while still differing in how clinical and administrative information is represented.

That observation is one reason I'm interested in studying data standardization and the validity of clinical definitions across institutions.

**Important limitation:** This was operational experience, not a formal phenotype portability study.

---

## CV-Q022 — What is the difference between HL7 and X12 837?

**Question:** What healthcare interoperability formats have you worked with?

**Answer:**

My CV lists experience with HL7 and X12 837.

HL7 standards support healthcare information exchange, while X12 837 is an electronic transaction format used to submit healthcare claims.

They serve different purposes, and understanding those differences is important when connecting clinical documentation to administrative billing workflows.

**Follow-up:** Which exact HL7 message types did you process?

**Answer:** Requires confirmation from work records.

---

## CV-Q023 — What is the difference between clinical and claims data?

**Question:** How do EHR data differ from claims data?

**Answer:**

EHR data can contain clinical documentation, observations, and treatment information. Claims data primarily represent services and diagnoses recorded for administrative and reimbursement purposes.

Both can support research, but neither is a perfect record of underlying clinical reality. Their completeness and meaning depend on the clinical and administrative processes that produced them.

---

## CV-Q024 — Did you validate computable phenotypes at Commure?

**Priority:** Critical

**Question:** Did you perform cross-site phenotype validation?

**Answer:**

My documented role involved healthcare data extraction, validation, coding differences, and operational data quality across sites.

I would not describe that work as a formal computable phenotype validation study.

Instead, it motivated my interest in researching how such variation affects phenotype definitions and cohort identification.

---

## CV-Q025 — How does your industry experience motivate phenotype portability research?

**Question:** Why are you interested in cross-institutional phenotype portability?

**Answer:**

At Commure, I encountered differences in documentation, coding, and data quality across healthcare sites.

That made me interested in a broader research question: if a clinical phenotype is transferred from one institution to another, how can we determine whether it still identifies the intended clinical population?

Possible factors include coding practices, missing observations, encounter definitions, and differences in timing.

**Status:** Proposed research direction inspired by professional experience.

---

# 11. ACI PLC and RxPERT Q&A

## CV-Q026 — What do you do at ACI PLC?

**Question:** Describe your current engineering role.

**Answer:**

I work as an AI Data Engineer in ACI PLC's R&D AI Lab.

My responsibilities include building Python and SQL ETL/ELT pipelines, analytical datasets, reusable data marts, and warehouse solutions using AWS and on-premises infrastructure.

I also work on reliability and performance improvements through indexing, partition pruning, and query-plan analysis.

---

## CV-Q027 — What is Healthcare RxPERT?

**Question:** What is RxPERT?

**Answer:**

RxPERT is an AI-assisted pharmaceutical R&D platform under development at ACI PLC.

The platform is designed to support literature evidence synthesis, reference-product analysis, QTPP/CQA assessment, API and formulation analysis, risk assessment, Design of Experiments, structured recommendations, and report generation.

My CV states that I designed multi-stage workflows for evidence processing, analysis, citations, and reproducible reports.

---

## CV-Q028 — How do you address LLM reliability?

**Question:** How would you make an AI-assisted scientific evidence system trustworthy?

**Answer:**

A reliable system should distinguish retrieved evidence from generated interpretation, preserve source provenance, verify citations, communicate uncertainty, and require expert review for consequential scientific decisions.

These are methodological principles relevant to RxPERT. Specific implemented safeguards and evaluation results must be retrieved from authorized project documentation.

---

## CV-Q029 — Why is your pharmaceutical AI experience relevant to clinical informatics?

**Question:** How does RxPERT connect to your PhD interests?

**Answer:**

Although pharmaceutical R&D and clinical informatics are different domains, both require reliable synthesis of heterogeneous biomedical evidence.

The transferable concerns include provenance, reproducibility, structured knowledge representation, and ensuring that automated outputs remain traceable to their supporting evidence.

---

# 12. MIMIC-IV, Claims, and Biomedical Analytics Q&A

## CV-Q030 — What is your MIMIC-IV project?

**Priority:** High

**Question:** What did you build with MIMIC-IV?

**Answer:**

I built a layered clinical data warehouse using DuckDB, with reproducible cohort definitions and first-24-hour feature extraction.

I also exposed aggregate analytics through FastAPI and Streamlit and added a LocalStack S3 ingestion path, SQL guardrails, and GitHub Actions checks.

The project demonstrates clinical data engineering and reproducibility, but it should not be presented as clinically validated without further evidence.

---

## CV-Q031 — What do you mean by reproducible cohorts?

**Question:** What makes a cohort definition reproducible?

**Answer:**

A reproducible cohort definition has explicit inclusion and exclusion criteria, a defined time anchor, consistent data transformations, and a process that allows the same rules to be rerun.

However, reproducing the same records does not establish that the cohort accurately represents the intended clinical condition.

---

## CV-Q032 — What is your CMS DE-SynPUF project?

**Question:** What did you study using synthetic Medicare claims?

**Answer:**

I developed a reproducible patient-year pipeline using CMS DE-SynPUF synthetic Medicare claims, producing 227,292 modeling records.

I engineered utilization, cost, diagnosis, and chronic-condition features, compared predictive models, and examined calibration, thresholds, and feature importance.

The work used temporally separated training and test cohorts.

---

## CV-Q033 — Why use temporal train/test separation?

**Question:** Why did you separate training and testing chronologically?

**Answer:**

For longitudinal prediction, temporal separation can provide a more realistic assessment of performance on later observations than an arbitrary random split.

However, temporal separation alone does not prevent leakage. Feature construction must also respect prediction-time availability.

The exact years, target definition, and leakage checks require project-level evidence.

---

## CV-Q034 — Can synthetic claims establish clinical validity?

**Question:** How much can you conclude from CMS DE-SynPUF?

**Answer:**

Synthetic claims are useful for developing and testing reproducible pipelines and modeling workflows.

However, performance on synthetic data does not establish that a model or phenotype is clinically valid for real Medicare beneficiaries.

That would require appropriate validation using real-world data and a suitable reference standard.

---

## CV-Q035 — What is CancerOmicsLake?

**Question:** Describe your cancer genomics project.

**Answer:**

CancerOmicsLake is a reproducible scientific data integration and analysis framework combining TCGA, GTEx, and recount3 evidence across BRCA, LUAD, and COAD.

The project evaluated 108,012 cancer–gene pairs using bootstrap stability analysis, Mann–Whitney testing, and false-discovery-rate correction.

It combined expression, mutation, and replication evidence for conservative gene prioritization.

---

## CV-Q036 — What did CancerOmicsLake teach you about data integration?

**Question:** What is the most important methodological lesson from CancerOmicsLake?

**Answer:**

Combining datasets is not just a technical exercise. Differences in source populations, sample handling, measurement procedures, and preprocessing can affect the validity of comparisons.

Harmonization and statistical correction are useful, but they do not automatically remove confounding or establish independent replication.

This concern is methodologically related to clinical data standardization.

---

## CV-Q037 — What is your Databricks project?

**Question:** What did you implement using Databricks?

**Answer:**

I implemented a Bronze/Silver/Gold processing pipeline using Apache Spark and Databricks.

The work included PySpark transformations, ETL/ELT workflows, dimensional modeling, Delta Lake schema evolution, and query optimization.

It demonstrates scalable data engineering skills but is not itself a clinical research project.

---

# 13. Research Methods and Scientific Judgment Q&A

## CV-Q038 — What is the difference between reproducibility and validity?

**Priority:** Critical

**Question:** Can a technically reproducible analysis still be scientifically wrong?

**Answer:**

Yes. Reproducibility means that the same procedures can produce consistent results under specified conditions.

Validity concerns whether the measurements, definitions, and conclusions represent what they are intended to represent.

For example, a SQL query can reproducibly identify patients with certain diagnosis codes while still failing to identify the intended clinical population accurately.

---

## CV-Q039 — What is computable phenotyping?

**Priority:** Critical

**Question:** What do you understand by a computable phenotype?

**Answer:**

A computable phenotype is an operational definition that uses available health data to identify patients or clinical states with specified characteristics.

It may combine diagnosis codes, procedures, medications, laboratory results, encounters, or temporal criteria.

Its usefulness depends on clear definitions, data availability, and validation against the intended clinical construct.

---

## CV-Q040 — What is phenotype portability?

**Priority:** Critical

**Question:** What does it mean for a phenotype to be portable?

**Answer:**

Phenotype portability concerns whether a computable phenotype can be transferred or adapted across data sources or institutions while preserving its intended clinical meaning and acceptable performance.

Technical execution at another institution is not enough.

Evaluation may require examining local data mappings, missingness, coding practices, cohort characteristics, and performance against suitable reference standards.

---

## CV-Q041 — How would you study phenotype portability?

**Priority:** Critical

**Question:** Suppose you could study the same phenotype at several hospitals. What would you do?

**Answer:**

I would begin with an explicit clinical definition and document the required data elements and temporal rules.

I would examine how those elements are represented at each site, including coding practices, missingness, and observation timing.

Then I would compare cohort characteristics and, where feasible, validate phenotype performance against chart review or another suitable reference standard.

I would also investigate whether observed differences reflect true patient-population differences or differences in data capture.

**Status:** Proposed research design.

---

## CV-Q042 — Why is standardization not sufficient?

**Question:** If two hospitals use the same coding standard, why might their data still differ?

**Answer:**

A shared terminology improves consistency but does not guarantee identical documentation practices or clinical meaning.

Institutions may differ in when codes are assigned, which observations are recorded, how encounters are structured, and whether data are missing.

Those differences can affect cohort membership even when the same standardized code sets are used.

---

## CV-Q043 — How do you distinguish data quality from population differences?

**Question:** If a phenotype identifies different proportions of patients at two sites, does that prove the phenotype failed?

**Answer:**

No. Different prevalence could reflect genuine differences in patient populations, healthcare utilization, or disease burden.

I would examine the underlying population characteristics and data-generating processes before attributing the difference to phenotype failure.

Where possible, validation against a suitable clinical reference standard would help distinguish those explanations.

---

## CV-Q044 — What is the role of knowledge representation?

**Question:** How could knowledge representation improve clinical research?

**Answer:**

Explicit representations can help document relationships among clinical concepts, observations, events, and time.

They may support traceability and reuse, but their value depends on correct source data, meaningful semantics, and evaluation.

A well-structured representation does not by itself establish clinical validity.

---

## CV-Q045 — How do you think about model explainability?

**Question:** What would make an AI explanation trustworthy?

**Answer:**

A useful explanation should be understandable, faithful to the model's behavior, and grounded in relevant evidence.

A plausible narrative or highlighted feature is not automatically a faithful explanation, and a predictive association does not establish causality.

Clinical evaluation should consider whether explanations support appropriate interpretation and decision-making.

---

# 14. Research Trajectory and Doctoral Fit

## CV-Q046 — What research direction interests you most?

**Priority:** Critical

**Question:** If you joined a PhD program, what would you want to study?

**Answer:**

I am especially interested in the reliability and portability of clinical data representations and computable phenotypes.

One possible direction is studying how variation in coding, missing observations, encounter timing, and documentation practices changes which patients are identified by the same clinical definition.

I would like to investigate methods for evaluating those differences and determining when local adaptation or additional validation is necessary.

**Status:** Proposed doctoral research interest.

---

## CV-Q047 — How do your current projects support that direction?

**Question:** Which of your experiences best supports this proposed research?

**Answer:**

Commure provided practical exposure to healthcare-site variation. MIMIC-IV gave me experience with reproducible clinical cohort construction. CMS DE-SynPUF provided longitudinal claims modeling experience.

My Wayne State research adds an interest in patient-centric knowledge representation, while RxPERT and CancerOmicsLake reinforce the importance of evidence provenance and data integration.

Together, these experiences motivate my interest in trustworthy clinical data use.

---

## CV-Q048 — What could you contribute to a research group?

**Question:** What strengths would you bring to a doctoral research team?

**Answer:**

I could contribute Python and SQL programming, data engineering, reproducible analytical workflows, clinical and claims data familiarity, and experience integrating heterogeneous datasets.

I also have early academic research experience and experience working on ongoing biomedical AI projects.

I would hope to combine those strengths with deeper training in clinical research methodology and validation.

---

## CV-Q049 — What do you hope to learn from a PhD?

**Question:** What skills or knowledge do you want to develop?

**Answer:**

I want to deepen my understanding of clinical research design, measurement validity, computable phenotype evaluation, and methods for assessing generalizability across healthcare settings.

I also want to become better at developing precise research questions, designing rigorous evaluations, and communicating results that can support reproducible scientific work.

---

## CV-Q050 — What would you ask Professor Richesson?

**Category:** Faculty conversation  
**Priority:** High

**Question:** What thoughtful research questions could the candidate ask?

**Suggested questions:**

1. When a computable phenotype is transferred between institutions, what evidence do you consider most important for determining whether it still identifies the intended clinical population?
2. In your research, which sources of variation are most difficult to distinguish: differences in coding, observation availability, encounter definitions, or genuine patient-population differences?
3. How do you see knowledge representation and data-quality assessment contributing to more reliable multicenter research?
4. For a student entering this area from data engineering, which methodological skills would be most important to develop first?

These are suggested conversation questions, not statements about the professor's opinions.

---

# 15. Difficult CV-Level Counterquestions

## CV-Q051 — Are you more of an engineer than a researcher?

**Question:** Your background appears engineering-heavy. Why should we see you as a prospective researcher?

**Answer:**

My experience is engineering-heavy, and I see that as a strength rather than something to hide.

Working with complex healthcare data has helped me identify methodological questions that cannot be solved by better pipelines alone.

I want to use my engineering foundation to investigate questions about clinical meaning, data validity, and generalizability through rigorous research.

---

## CV-Q052 — Have you conducted independent clinical research?

**Question:** Have you independently validated a clinical model or phenotype?

**Answer:**

My CV establishes clinical data engineering, longitudinal modeling, and ongoing research in patient-centric knowledge graphs.

It does not establish that I independently conducted a clinically validated phenotype study.

I would describe my experience accurately and explain that developing the ability to design and conduct such studies is part of my doctoral motivation.

---

## CV-Q053 — Why should we trust your project metrics?

**Question:** How can you substantiate the numbers on your CV?

**Answer:**

The numerical claims should be traceable to their original sources.

For example, the CMS project should contain evidence supporting the 227,292 modeling records, CancerOmicsLake should support the 108,012 cancer–gene pairs, and the Commure QA improvement should be supported by the original measurement method.

If a metric cannot be reproduced or verified from available evidence, I should explain its basis and limitations rather than overstate certainty.

---

## CV-Q054 — What if your research hypothesis is wrong?

**Question:** What if knowledge graphs do not improve prediction or phenotype portability?

**Answer:**

That would still be a meaningful research result if the study were well designed.

The goal should be to evaluate a hypothesis rigorously, not to guarantee that a preferred technique succeeds.

Understanding when a complex representation does not provide additional value could help guide simpler and more reliable methods.

---

## CV-Q055 — Why not focus only on LLMs?

**Question:** Your CV lists healthcare LLMs as a research interest. Why are you also interested in data quality and phenotyping?

**Answer:**

LLMs can be useful for working with biomedical information, but their outputs depend on the quality, meaning, and provenance of the underlying evidence.

I am interested in foundational questions about clinical data representation and reliability because those issues affect both traditional analytical methods and newer AI systems.

---

# 16. Cross-Project Relationships for Knowledge-Graph Retrieval

These relationships can be extracted as graph edges.

| Source node | Relationship | Target node | Explanation |
|---|---|---|---|
| Pronab Chandra Roy | STUDIED_AT | NIT Silchar | B.Tech, CSE, 2020–2024 |
| Pronab Chandra Roy | RESEARCH_INTERN_AT | Wayne State University | 2026–present |
| Pronab Chandra Roy | SUPERVISED_BY | Dr. Lihui Liu | Wayne State research |
| Pronab Chandra Roy | WORKS_AT | ACI PLC | AI Data Engineer |
| Pronab Chandra Roy | PREVIOUSLY_WORKED_AT | Commure | Operations Data Analyst |
| Pronab Chandra Roy | RESEARCHED | Patient-Centric Knowledge Graphs | Ongoing T1D research |
| Pronab Chandra Roy | DEVELOPED | MIMIC-IV Clinical Data Warehouse | CV-supported |
| Pronab Chandra Roy | DEVELOPED | CMS DE-SynPUF Pipeline | CV-supported |
| Pronab Chandra Roy | DEVELOPED | CancerOmicsLake | CV-supported |
| Pronab Chandra Roy | WORKS_ON | Healthcare RxPERT | Ongoing development |
| Pronab Chandra Roy | IMPLEMENTED | Databricks Medallion Pipeline | CV-supported |
| Pronab Chandra Roy | COAUTHORED | IEEE ICIC 2023 Paper | Publication |
| Commure Experience | MOTIVATES_INTEREST_IN | Clinical Data Quality | Interpretive |
| Commure Experience | MOTIVATES_INTEREST_IN | Phenotype Portability | Interpretive |
| MIMIC-IV Warehouse | RELATES_TO | Reproducible Cohort Construction | Methodological |
| CMS DE-SynPUF | RELATES_TO | Longitudinal Claims Modeling | Direct |
| Wayne State Research | RELATES_TO | Clinical Knowledge Representation | Direct |
| CancerOmicsLake | RELATES_TO | Biomedical Data Harmonization | Methodological |
| RxPERT | RELATES_TO | Reliable Evidence Synthesis | Direct |
| Proposed PhD Direction | FOCUSES_ON | Computable Phenotype Portability | Proposed |

**Graph ingestion note:** Interpretive and proposed relationships must retain their evidence-status metadata. Do not store them as completed research findings.

---

# 17. Questions Requiring Candidate Confirmation

These questions should be flagged during retrieval rather than answered with invented details.

## Wayne State

- What dataset is being used?
- What have you personally implemented?
- What are the graph nodes and edge types?
- What is the hypoglycemia outcome definition?
- What prediction horizon is being considered?
- Which models or experiments have actually been run?
- What results, if any, are available?
- What is the next research milestone?

## Commure

- How was the approximately 70% manual QA reduction measured?
- Which specific validation checks were automated?
- What were the most important data-quality problems encountered?
- Which HL7 message types were processed?
- What was your exact responsibility during the 38 launches?
- Which non-confidential examples can be discussed?

## MIMIC-IV

- What are the exact implemented cohort definitions?
- Which first-24-hour features were extracted?
- What validation tests were performed?
- Which execution paths used synthetic/demo data?
- Were full credentialed MIMIC-IV data used?

## CMS DE-SynPUF

- What was the precise prediction target?
- Which years were used for training and testing?
- Which models were compared?
- What performance and calibration results were observed?
- How were repeated patient-year records handled?

## CancerOmicsLake

- How were the 108,012 cancer–gene pairs counted?
- What were the actual normalization and comparison procedures?
- How was bootstrap stability calculated?
- What constitutes independent replication?
- What were the final candidate-gene results?

## RxPERT

- Which components were personally designed or implemented?
- What evidence-retrieval and citation checks exist?
- What evaluation has been completed?
- Which functions are still under development?
- Which details are confidential?

## General research readiness

- What is the strongest example of independently identifying a research problem?
- What is the strongest example of a failed experiment and what was learned?
- What research question would be the candidate's first choice for a PhD?
- What methods does the candidate most want to learn?

---

# 18. RAG Answering Policy

When the user asks a question about Pronab Chandra Roy:

1. Retrieve this CV document for canonical identity, education, dates, roles, and project summaries.
2. Retrieve the corresponding project document for implementation details, experiments, metrics, and methodological decisions.
3. Prefer project code and experimental artifacts for technical claims when available.
4. Use first-person language only when generating a simulated interview response.
5. Do not fabricate personal anecdotes, results, clinical experience, or completed research.
6. Preserve the distinction between professional operational experience and formal academic research.
7. Treat proposed research directions as proposals, not achievements.
8. If evidence is insufficient, state the limitation and identify the missing information.
9. Do not conflate the undergraduate denoising thesis with the separate IEEE image-compression publication.
10. Do not claim admission, funding, or a formal research appointment at the University of Michigan.

## Suggested retrieval aliases

- "Tell me about yourself" → CV-Q001
- "Why PhD?" → CV-Q002
- "Why clinical informatics?" → CV-Q003
- "Why Rachel Richesson?" → CV-Q004
- "Why HILS?" → CV-Q005
- "What connects your projects?" → CV-Q008
- "What is your Wayne State research?" → CV-Q014
- "What did you do at Commure?" → CV-Q019
- "What did you learn from site launches?" → CV-Q021
- "What is your MIMIC-IV project?" → CV-Q030
- "What is CMS DE-SynPUF?" → CV-Q032
- "What is CancerOmicsLake?" → CV-Q035
- "What is computable phenotyping?" → CV-Q039
- "What is phenotype portability?" → CV-Q040
- "How would you study phenotype portability?" → CV-Q041
- "What PhD research interests you?" → CV-Q046
- "What are your research strengths?" → CV-Q048
- "What questions should you ask the professor?" → CV-Q050
- "Are you an engineer or researcher?" → CV-Q051

---

# 19. Source Links

- Personal website: https://pronab.me
- GitHub profile: https://github.com/pronabroy360
- IEEE publication: https://ieeexplore.ieee.org/document/10382031
- MIMIC-IV repository: https://github.com/pronabroy360/MIMIC-IV-Clinical-DW
- CMS DE-SynPUF repository: https://github.com/pronabroy360/CMS-DESynPuf
- CancerOmicsLake repository: https://github.com/pronabroy360/CancerOmicsLake
- Databricks repository: https://github.com/pronabroy360/dbricks_medallion_restaurants
- RxPERT platform: https://rxpert.acimisai.com/login

The links are source references provided in the CV, not evidence that every linked resource has been independently inspected.

---

# 20. Final Grounding Summary

Pronab Chandra Roy is a computer science graduate from NIT Silchar with early published research in image compression, production experience in U.S. healthcare data operations, current AI data engineering responsibilities, and ongoing research in patient-centric clinical knowledge graphs.

His project portfolio includes clinical data warehousing, synthetic claims modeling, cancer genomics data integration, pharmaceutical AI workflows, and scalable data engineering.

The central research narrative is a progression from **building reliable computational and data-processing systems** toward **studying whether the clinical information and evidence those systems produce are valid, interpretable, reproducible, and portable across healthcare settings**.

This narrative is an interpretation of the candidate's stated experience and interests. It should not be represented as an established doctoral research result.

**End of document.**
