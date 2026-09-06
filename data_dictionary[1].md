# Data Dictionary — E-commerce Customer Transactions Dataset

**Source file:** `raw_ecommerce_transactions.csv`
**Rows:** ~1,030 | **Columns:** 13
**Grain:** One row = one product transaction/order line.

| Column | Data Type | Description | Business Relevance |
|---|---|---|---|
| TransactionID | String (categorical, unique) | Unique identifier for each transaction | Primary key; used to track and de-duplicate orders |
| CustomerID | String (categorical) | Unique identifier for each customer | Links transactions to a customer for CLV, repeat-purchase analysis |
| CustomerName | String (text) | Full name of the customer | Used for personalization/CRM; not for analytics modeling |
| DateOfBirth | Date (stored as inconsistent text) | Customer's date of birth | Used to engineer `CustomerAge` for demographic segmentation |
| Gender | Categorical (M/F/Male/Female, inconsistent) | Customer's gender | Demographic segmentation, marketing targeting |
| Country | Categorical (free text, inconsistent) | Customer's country | Regional sales analysis, market expansion decisions |
| ProductCategory | Categorical | Category of purchased product | Category-level sales performance, inventory planning |
| PurchaseDate | Date (stored as inconsistent text) | Date the transaction occurred | Time-series/trend analysis, seasonality |
| Quantity | Integer | Number of units purchased | Sales volume analysis; negative values indicate data entry errors |
| UnitPrice | Float | Price per unit (local currency) | Revenue calculation; contains outliers to investigate |
| TotalAmount | Float | Quantity × UnitPrice | Core revenue metric |
| PaymentMethod | Categorical (free text, inconsistent) | Method used to pay | Payment trend analysis, fraud/risk flags |
| CustomerFeedback | Free text | Customer's written feedback/review | Sentiment analysis, NPS/quality signals |

## Known Issues (identified in profiling step)
- **Missing values** in Gender, Country, CustomerFeedback, UnitPrice, DateOfBirth
- **Duplicate rows** (~3% of dataset)
- **Inconsistent formatting**: Country (e.g. "USA"/"U.S.A"/"usa"), PaymentMethod (e.g. "UPI"/"upi"), Gender (e.g. "M"/"Male"/"m")
- **Inconsistent date formats** in DateOfBirth and PurchaseDate (mix of YYYY-MM-DD, DD/MM/YYYY, MM-DD-YYYY, etc.)
- **Outliers** in UnitPrice (~1% of records have abnormally high prices)
- **Invalid values**: negative Quantity entries (data entry errors)
- **Free text** CustomerFeedback needs categorization/sentiment tagging
