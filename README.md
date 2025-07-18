# Healthcare-data-simulation
# Simulated Clinical & Billing Data Generator

## Overview
This Python script generates a synthetic healthcare dataset that simulates clinical and billing records for healthcare analytics and data science practice.

The generated data includes patient visits across multiple departments with realistic distributions of:
- Patient ages and diagnoses based on department
- Visit types (Inpatient and Outpatient)
- Payer types (Insurance, Government, Self-pay) with corresponding billing and payment logic
- Missing values and outliers to simulate real-world data quality issues for data cleaning practice

## Features
- Department-specific patient age ranges and diagnoses
- Visit reasons aligned with departments
- Inclusion of nulls (~7%missing values) in selected fields for cleaning exercises
- Occasional outliers(~2%) in charges and payments to test anomaly detection
- Configurable number of records
- Payer names are limited to 25 synthetic companies, reused across the dataset.
- visit type-Outpatients does not have admission-discharge date, only visit date.

## Installation

This project requires Python 3.x and the following packages:

```bash
pip install faker pandas
