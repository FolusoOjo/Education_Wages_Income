# Bridging the Gap: Education, Wages and Labour Market Outcomes in Ontario.

## Project Overview

This project analyzes how education level, gender, and immigration status influence labour-market outcomes in Ontario, Canada.
Using data from the **CIS (Canadian Income Survey)** and the **Education-Level Wage dataset**, the objective is to:
  - Measure wage returns across education levels
  - Compare outcomes between immigrants and non-immigrants
  - Analyze gender-based wage patterns
  - Explore long term income trends.
    
The final deliverables includes:
  - Cleaned Datasets
  - Merged analysis-ready dataset
  - Python-based EDA (univariate, bivariate and multivariate)
  - Interactive Tableau dashboards


## Project Structure
```text
Education_Wage_Income_Analysis/
|
│
├── raw_data/                          # Original unmodified datasets
│   ├── education_level_raw.xlsx
│   └── cis_data_raw.xlsx
│
├── cleaned_data/                      # Datasets after preprocessing
│   ├── education_level_cleaned.xlsx
│   └── cis_data_cleaned.xlsx
│
├── merged_data/                       # Final dataset used for EDA and Tableau
│   └── merged_final.xlsx              
│
├── python_scripts/                    # Python workflow scripts
│   ├── capstone_cleaning_education_level.ipynb
│   ├── capstone_cleaning_cis_data.ipynb
│   └── capstone_data_merging.ipynb    # Merges pivot outputs → merged_data/
│
├── eda/                               # All exploratory data analysis work
|   └── capstone_eda.ipynb             # Univariate, Bivariate & Multivariate analysis
|
├── requirements.txt/                  # Python dependencies
|
└── README.md                          # Project documentation



```
## How to Run the Project

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
