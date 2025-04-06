# 📊 Bank Marketing Data Cleaning Project

## 📌 Overview
This project involves cleaning and preparing bank marketing campaign data for storage in a PostgreSQL database. The raw data includes information on clients, campaign interactions, and economic indicators from a personal loan marketing campaign conducted by a UK bank.

## 🎯 Objectives
- Clean and transform raw marketing data into three structured tables  
- Ensure data conforms to specified formats and types  
- Prepare data for easy import into PostgreSQL  
- Establish a repeatable process for future campaigns

## 📂 Data Files
**Input:**  
- `bank_marketing.csv` — Raw data file containing all campaign records

**Output:**  
- `client.csv` — Client demographic and financial information  
- `campaign.csv` — Campaign interaction details  
- `economics.csv` — Economic indicators at time of contact

## 🧹 Data Cleaning Process

### 1️⃣ Client Data Cleaning
**Columns:**  
`client_id`, `age`, `job`, `marital`, `education`, `credit_default`, `mortgage`

**Transformations:**  
- Standardized job titles by replacing `.` with `_`  
- Cleaned education levels:  
  - Replaced `.` with `_`  
  - Converted `unknown` to `NaN`  
- Converted categorical fields to boolean (`1`/`0`):  
  - `credit_default`: 1 if `"yes"`, 0 otherwise  
  - `mortgage`: 1 if `"yes"`, 0 otherwise

**Key Decisions:**  
- Treated `"unknown"` credit defaults as 0 (not in default)  
- Treated `"unknown"` mortgages as 0 (no mortgage)

---

### 2️⃣ Campaign Data Cleaning
**Columns:**  
`client_id`, `number_contacts`, `contact_duration`, `previous_campaign_contacts`,  
`previous_outcome`, `campaign_outcome`, `last_contact_date`

**Transformations:**  
- Converted outcome fields to boolean (`1`/`0`):  
  - `previous_outcome`: 1 if `"success"`, 0 otherwise  
  - `campaign_outcome`: 1 if `"yes"`, 0 otherwise  
- Created `last_contact_date` from:  
  - `day`, `month` columns  
  - Fixed year: 2022  
- Handled invalid dates by replacing them with the most common valid date

**Key Features:**  
- Robust date parsing with error handling  
- Memory optimization using `int8` for boolean fields  
- Validated contact attempt ranges (1–56 contacts)

---

### 3️⃣ Economics Data Cleaning
**Columns:**  
`client_id`, `cons_price_idx`, `euribor_three_months`

**Transformations:**  
- Verified no missing values  
- Checked for outliers using the IQR method  
- Ensured proper numeric types

**Findings:**  
- No significant outliers detected  
- CPI range: 92.201 – 94.767  
- EURIBOR range: 0.634 – 5.045

---

## 🔍 Data Validation
Comprehensive validation checks at each stage:
- Verified value distributions before/after transformations  
- Checked for missing values  
- Validated data ranges  
- Confirmed proper data types  
- Documented all cleaning decisions

---

## 💾 Database Preparation
The cleaned data is structured for PostgreSQL with:
- Correct data types for each column  
- Consistent formatting  
- Handled missing data  
- Optimized storage types

---

## 🚀 How to Use
1. Run the cleaning notebook `notebook.ipynb`
2. Three cleaned CSV files will be generated

**Import into PostgreSQL:**
```sql
-- Example import commands
\copy client FROM 'client.csv' DELIMITER ',' CSV HEADER;
\copy campaign FROM 'campaign.csv' DELIMITER ',' CSV HEADER;
\copy economics FROM 'economics.csv' DELIMITER ',' CSV HEADER;


📊 Results Summary
Dataset	Records	Key Transformations	Output File Size
Client	41,188	2 boolean conversions, text cleanup	~1.2 MB
Campaign	41,188	Date creation, 2 booleans	~1.5 MB
Economics	41,188	Outlier detection, type validation	~0.9 MB
📝 Key Decisions
Handling Unknowns: Treated "unknown" values conservatively (as negative/false)

Date Handling: Used fixed year 2022 with robust error handling

Boolean Conversion: Used 1/0 integers for database compatibility

Outlier Treatment: Preserved original economic values after confirming no extreme outliers

🛠 Future Improvements
Automate the cleaning pipeline for future campaigns

Add data quality metrics tracking

Implement more sophisticated outlier detection

Create database schema migration scripts

✅ This project successfully transformed raw marketing data into clean, analysis-ready datasets while maintaining data integrity and following best practices for database preparation.
