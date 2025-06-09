# StudentAnalytics

# Data Engineer Technical Assessment – Microsoft Fabric

This repository contains a solution to the technical assessment focused on building a structured, automated data pipeline using Microsoft Fabric. The implementation follows the Medallion Architecture (Bronze → Silver → Gold) and applies automation, access control, and query development best practices.

## Overview

The objective is to simulate ingestion, transformation, and modeling of class assignment and submission data. This is achieved by ingesting raw files into a Lakehouse, transforming them through defined layers, and surfacing analytical tables to support downstream AI or reporting use cases. The sample datasets were simulated using a Python script through which CSV files were generated.

---

## Medallion Architecture

### Bronze Layer  
Raw data is ingested using a shortcut to an Azure Data Lake Gen2 folder containing the following CSV files:
- `students.csv`
- `assignments.csv`
- `courses.csv`
- `submissions.csv`
- `enrollments.csv`

### Silver Layer  
Cleaned and joined dataset based on normalized relationships among students, assignments, and submissions. Key fields include:
- `studentid`, `assignmentid`, `email`, `courseid`, `coursename`, `title`, `duedate`, `submissiondate`, `grade`

### Gold Layer  
Three analytical tables were created:
- `gold_notsubmitted`: Students who did not submit “Assignment_101”
- `gold_submissionrate`: Submission rate per course
- `gold_overdue`: Count of overdue assignments per student

---

## Queries Implemented

PySpark queries were written to answer the following business questions:
1. Which students did not submit Assignment_101?
2. What is the submission rate for each course?
3. How many overdue assignments does each student have?

All outputs follow a structured JSON format for downstream API consumption.

---

## Automation

The ingestion and transformation workflow can be automated using:
- A Python script (`trigger_pipelines.py`) to programmatically trigger Fabric pipelines via REST API
- A GitHub Actions workflow (`.github/workflows/fabric-pipeline-trigger.yml`) that runs the pipeline on every push to the `main` branch

Environment variables are managed via a `.env` file (excluded from version control).

---

## Security & Governance

### Row-Level Security  
Applied on `gold_notsubmitted` using a security predicate function to restrict data based on the logged-in user's email. Admin users can bypass the filter.

### Column-Level Security
Implemented on `gold_overdue` to restrict access to only specific columns for certain users.

### Object-Level Security
Applied on `gold_submissionrate` as non-priveleged users cannot view the table unless given priveleges.

### Dynamic Data Masking
Implemented data masking in `Email` field in `gold_notsubmitted` so that the logged in user can see their email as masked in the form of `kXXX@XXXX.com`, for example.


---

## Setup Instructions

1. Clone this repository.
2. In Microsoft Fabric, create a new Lakehouse and add a shortcut to the ADLS Gen2 `raw data` folder.
3. Open and run the notebooks in the following order:
   - `Bronze_Notebook.ipynb` – Loads raw CSVs
   - `Silver_Notebook.ipynb` – Joins and cleans the data
   - `Gold_Notebook.ipynb` – Outputs gold-layer analytical tables
4. Update the `.env` file with your pipeline and app credentials.
5. Trigger the pipeline either manually or by pushing to the `main` branch to execute via GitHub Actions.


