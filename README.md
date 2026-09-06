# ApexPlanet_Task1
Data wrangling on a sales transactions dataset — profiling, cleaning, and feature engineering using Python &amp; Pandas. Task 1 of Data Analytics Internship.
# Data Analytics Internship — Task 1: Data Immersion & Wrangling

## Objective
Acquire, profile, clean, and prepare a raw sales transactions dataset for analysis, 
covering the full first-mile of the analytics workflow: data understanding, 
quality assessment, cleaning, transformation, and feature engineering.

## Files
| File | Description |

| `raw_sales_data.csv` | Original, unprocessed dataset (515 rows, 10 columns) |
| `data_dictionary.md` | Documentation of each variable — type, meaning, business relevance |
| `cleaning_script.py` | Python/Pandas script for profiling, cleaning, and transformation |
| `cleaned_dataset.csv` | Final analysis-ready dataset (500 rows, 13 columns) |

## Data Quality Issues Identified
- Missing values across 4 columns (Email, DateOfBirth, Price, PaymentMethod)
- 15 exact duplicate records
- Inconsistent date formats (4 different formats mixed in OrderDate & DateOfBirth)
- Inconsistent free-text categories (19 variants of 6 real product categories)
- Outliers in unit price

## Cleaning & Transformation Steps
- Removed duplicate rows
- Standardized all dates to `YYYY-MM-DD`
- Normalized product categories (e.g. "electronics", "ELECTRONICS" → "Electronics")
- Imputed missing values (category-median for price, mode for payment method)
- Capped price outliers using the IQR method

## Feature Engineering
- `CustomerAge` — derived from Date of Birth
- `OrderValue` — Price × Quantity
- `OrderMonth` — for time-series/trend analysis

## Tools Used
Python, Pandas, NumPy

