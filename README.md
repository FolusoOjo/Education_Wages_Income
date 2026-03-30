# Bridging the Gap: Education & Income Inequality Among Immigrants
### A comparative analysis of how education shapes income outcomes for Immigrants in Canada and the United States and where the gap Persists.

## Project Overview

This project investigates how education impacts income inequality, with a focus on immigrant populations across two countries.

The analysis combines exploratory data analysis (EDA) and machine learning techniques to identify patterns, differences, and structural gaps in labour market outcomes.

## Project Evolution.
This project was developed in two phases:

Phase 1:
Focused on Ontario, Canada using CIS and education wage data to analyze labour market outcomes and income patterns.

Phase 2:
Expanded into a cross-country comparison (Canada vs United States), introducing machine learning models to evaluate whether income patterns generalize across labour markets.

## Project Structure
```text
Education_Wage_Income/
|
│
├── phase_1_canada_eda/
|                    
├── phase_2_ml_comparison/
|
├── requirements.txt/                  
|
└── README.md                         


```
## Phase 1: Canada Analysis (EDA & Tableau)
  ### Objective
    To explore how education, gender and immigration status influence income in Ontario, Canada.

  ### Key Steps
    - Data Cleaning and Preprocessing
    - Data Merging (CIS + Education Level Dataset)
    - Exploratory Data Analysis
        - Univariate
        - Bivariate
        - Multivariate
    - Tableau Dashboard Development

  ### Outputs
    - Cleaned Datasets
    - EDA notebooks
    - Interactive Tableau Dashboard
    - Presentation Slides

### Step 1- Clone the Repository
```bash
git clone https://github.com/FolusoOjo/Education_Wages_Income.git
cd Education_Wages_Income
```

### Step 2- Install Dependencies
Ensure you have Python installed (3.10+ recommended)
```bash
pip install -r requirements.txt
```

### Step 3- Run the Notebooks
Execute these notebooks in this order:
  1. python_scripts/capstone_cleaning.ipynb
  2. python_scripts/capstone_data_merging.ipynb
  3. eda/capstone_eda.ipynb

### Step 4- Open the Tableau Dashboard
After generating the merged dataset:
  Open your Tableau dashboard file manually inside Tableau.


## Full Project Workflow
1. **Data Cleaning**: this was done using jupyter notebook (capstone_cleaning.ipynb)
  - Handled missing values,
  - Standardized categorical labels mostly in the CIS data (gender, education, immigration_status)
  - Normalized column formats
  - Exported cleaned datasets

2. **Dataset Merging**: Both datasets were merged together on similar columns such as 'year, education_level, immigrant_status' and we aggregated the CIS dataset.

3. **Exploratory Data Analysis**: We performed the:
  - Univariate Analysis (Distribution of categories and numeric variables)
  - Bivariate Analysis (income by gender, education, immigration status)
  - Multivariate analysis using FacetGrid(intersection of gender, immigration status and education)
  - This helped to identify wage gaps and structual differences between groups.

5. **Dashboard Development**: Built 3 dashbaords:
  - Overview Dashboard - Project Summary and income KPI's
  - Education and Wage Trends - Bar Charts, Line Charts, Heatmaps.
  - Labour and Income Insights - Scatter plots, comparisons and wage gaps.
  - The dashboards allow interactive filtering using immigration status.

## Technologies Used
  - Python- Pandas, Numpy, Seaborn, Matplotlib
  - Jupyter Notebook
  - Tableau- Interactive Dashboards
  - Git and Github

## Key Insights (Summary)
  - Higher education gives higher income consistently across all groups
  - Immigrants earn less than non- immigrants, even with the same certification (education level)
  - Women earn less than men, across all education level.
  - Immigrant women faces the largest income gaps
  - Wage differences remain stable over time, this suggests persistent wage gaps.

## Team Members
  - Ameenat Ali
  - Foluso Ojo
  - Gurpreet Kaur
  - Pei- Ru Chen

## License
This project is for academic use under St. Clair College's Capstone guidelines.
