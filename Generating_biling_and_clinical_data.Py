"""
Simulated Clinical & Billing Data Generator
-------------------------------------------
This script generates synthetic healthcare data for clinical and billing analytics.

Features:
- Department-specific age/diagnosis distributions
- Realistic visit types (Inpatient/Outpatient)
- Insurance/payor variation
- Outliers and missing values for data cleaning practice

Author: Aya A Saad
License: MIT
"""


import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta


# Set seed for reproducibility
RANDOM_SEED= 123
random.seed(RANDOM_SEED)
fake= Faker()
Faker.seed(RANDOM_SEED)

#Introducing Department
# Define department logic
department_mapping = {
    "Cardiology":{
        "age_range": (35, 60),
        "diagnosis_info": ["Hypertension", "Heart Failure", "Arrhythmia"],
        "reasons": ["Chest Pain", "Heart Screening", "Follow-up"],
        "charge_range": (150, 300),
    },
    "Oncology": {
        "age_range": ( 13,80 ),
        "diagnosis_info": ["Cancer", "Leukemia", "Lymphoma", "Melanoma"],
        "reasons": ["Chemo", "Biopsy", "Follow-up", "Blood test"],
        "charge_range": (500, 1200),

    },
    "Pediatrics": {
         "age_range": (1,17),
        "diagnosis_info": ["Flu", "Asthma", "Infection"],
        "reasons": ["Vaccination", "Checkup", "Fever"],
        "charge_range": (40,80),

    },
    "Neurology": {
         "age_range": (10 , 70),
        "diagnosis_info": ["Migraine", "Epilepsy", "Stroke"],
        "reasons": ["Seizure", "Numbness", "Headache"],
        "charge_range": (120, 200),

    },
    "Orthopedics": {
       "age_range": (18 ,70 ),
        "diagnosis_info":["Fracture", "Arthritis", "Back Pain"],
        "reasons": ["Injury", "Joint Pain", "Surgery Follow-up"],
        "charge_range": (120, 200),

    },

}
payer_types= ["Insurance", "Government", "Self-pay"]
claim_status_options= ["Submitted", "Approved", "Denied", "Paid"]

##limiting generated fake insurance company names to 25 name
unique_payers = list({fake.company() for _ in range(300)})[:25]

##generating patients record
def generate_patient_record(index):
    department = random.choice(list(department_mapping.keys()))
    department_info = department_mapping[department]

    age = random.randint(*department_info["age_range"])
    diagnosis = random.choice(department_info["diagnosis_info"])
    visit_reason = random.choice(department_info["reasons"])

    payer_type = random.choice(payer_types)
    payer_name = random.choice(unique_payers) if payer_type != "Self-pay" else "Self-pay"

    claim_status = (random.choice(claim_status_options[:-1]) if payer_type != "Self-pay" else "Paid")

    charge_amount = random.randint(*department_info["charge_range"])
    #validation check for charge amount- not required, just for safety
    if charge_amount <= 0:
     raise ValueError(f"Invalid charge amount: {charge_amount}")
    payment_amount = 0

## simple way to simulate that the payer(Govenment/insurance) typically pays at least 80% of the charge depends on the contract, while payer (sel-pay) pays 100%
    if claim_status == "Paid":
      if payer_type == "Self-pay":
          payment_amount = charge_amount  # 100% paid
      else:
        payment_amount = random.randint(int(charge_amount * 0.8), charge_amount)
    else:
      payment_amount = 0

    visit_date = fake.date_between(start_date='-2y', end_date='today')

  # Decide if patient is admitted (i.e., Inpatient) or not
    is_inpatient = random.choice([True, False])
    visit_type = "Inpatient" if is_inpatient else "Outpatient"
    admission_date = visit_date if is_inpatient else None
    discharge_date = (admission_date + timedelta(days=random.randint(1, 29))) if admission_date else None

    record = {
        "patient_id": random.randint(110000, 220000),
        "gender": random.choice(["Male", "Female"]),
        "age": age,
        "visit_date": visit_date.isoformat(),
        "department": department,
        "physician_id": random.randint(10000, 99999),
        "diagnosis": diagnosis,
        "visit_type": visit_type,
        "visit_reason": visit_reason,
        "appointment_id": f"A{index:05d}",
        "is_emergency": random.choice(["Yes", "No"]),
        "insurance_id": 'INS-' + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6)) if payer_type != "Self-pay" else "N/A",
        "payer_name": payer_name,
        "payer_type": payer_type,
        "claim_status": claim_status,
        "charge_amount_USD": charge_amount,
        "payment_amount_USD": payment_amount,
        "admission_date": admission_date.isoformat() if admission_date else None,
        "discharge_date": discharge_date.isoformat() if discharge_date else None,
    }

    # Introduce 7% nulls only in selected fields
    fields_to_null = [ "diagnosis", "visit_reason", "payer_name", "insurance_id"]
    for field in fields_to_null:
        if random.random() < 0.07:
            record[field] = None

    # Add outliers in charges/payments (2% chance)
    if random.random() < 0.02:
        record["charge_amount"] *= 10
        record["payment_amount"] = int(record["charge_amount"] * 0.8)

    return record

# Generate dataset

NUM_RECORDS= 6000
data= [generate_patient_record(i) for i in range(NUM_RECORDS)]

# Save to CSV
df = pd.DataFrame(data)
#df.to_csv("Simulated_Clinical_and_Billing_Data_for_Healthcare_Analytics.csv", index=False)

print("Data saved to 'Simulated_Clinical_and_Billing_Data_for_Healthcare_Analytics.csv'")