# Bridging the Gap: Education, Wages and Labour Market Outcomes in Ontario.

## Project Overview

This project analyzes how education level, gender, and immigration status influence labour market outcomes in Ontario, Canada.
Using data from the **CIS (Canadian Income Survey)** and the **Education-Level Wage dataset**, the objective is to:
  - Measure wage returns across education levels
  - Compare outcomes between immigrants and non-immigrants
  - Analyze gender-based wage patterns
  - Explore how these factors intersect over time.
    
The final deliverables include a clean dataset, exploratory data analysis (EDA), and interactive Tableau dashboards.


## Project Structure
```text
capstone-income-analysis/
|
├── README.md                          # Project documentation
│
├── raw_data/                          # Original unmodified datasets
│   ├── education_level_raw.xlsx
│   └── cis_data_raw.xlsx
│
├── cleaned_data/                      # Cleaned datasets after preprocessing
│   ├── education_level_cleaned.xlsx
│   └── cis_data_cleaned.xlsx
│
├── pivot_output/                      # Pivot tables created manually in Excel
│   ├── education_pivot_output.xlsx    # Avg hourly wage by year,education and gender
│   └── cis_pivot_output.xlsx          # Avg earnings, salary, total income
│
├── merged_data/                       # Final dataset used for EDA and Tableau
│   └── merged_final.xlsx              # Output from merging pivot files
│
├── python_scripts/                    # Python/Jupyter scripts used in workflow
│   ├── capstone_cleaning.ipynb        # Python file 1: cleans raw datasets → cleaned_data/
│   └── merging.ipynb                  # Python file 2: merges pivot outputs → merged_final.xlsx
│
├── eda/                               # All exploratory data analysis work
|   └── capstone_eda.ipynb             # Python file 3: Univariate, bivariate & multivariate analysis
|
├── requirements.txt/
|
└── README.md                          # Project documentat



```

## Full Project Workflow
1. **Data Cleaning**: this was done using jupyter notebook (capstone_cleaning.ipynb)
  - Handled missing values,
  - Standardized categorical labels mostly in the CIS data (gender, education, immigration_status)
  - Normalized column formats
  - Exported cleaned datasets

2. **Pivot Calculations**: Pivot tables were created in Excel to aggregate the cleaned datasets before merging.
  - We used the common dimensions Year, Education, Gender, Immigration Status generating a summary of the tables.
  - Education_Pivot_Output computed the average hourly wages for Men and Women, which was aggregated by year, education, gender and immigration status.
  - cis_pivot_output computed the average total income, average earning and average wage salary, which was aggregated by year, education, gender and immigration status.

3. **Dataset Merging**: The pivot outputs were merged on year, education, gender, immigration status

4. **Exploratory Data Analysis**: We performed the:
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
  - Python (Pandas, Seaborn, Matplotlib)
  - Excel (Pivot Tables)
  - Tableau (Dashboards)
  - Jupyter Notebook
  - Git and Github
    
## Team Members
  - Ameenat Ali
  - Foluso Ojo
  - Gurpreet Kaur
  - Pei- Ru Chen

## Key Insights (Summary)
  - Higher education gives higher income consistently across all groups
  - Immigrants earn less than non- immigrants, even with the same certification (education level)
  - Women earn less than men, across all education level.
  - Immigrant wwomen faces the largest income gaps
  - Wage differences remain stable over time, this suggests persistent wage gaps.

## License
This project is for academic use under St. Clair College's Capstone guidelines.
