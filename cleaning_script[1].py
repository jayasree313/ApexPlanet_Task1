"""
Data Cleaning & Transformation Script
Objective: Profile, clean, and transform raw e-commerce transaction data
into an analysis-ready dataset.
"""

import pandas as pd
import numpy as np
from datetime import datetime

RAW_PATH = "raw_ecommerce_transactions.csv"
CLEAN_PATH = "cleaned_dataset.csv"

# -----------------------------
# 1. LOAD DATA
# -----------------------------
df = pd.read_csv(RAW_PATH)
print("Initial shape:", df.shape)

# -----------------------------
# 2. DATA QUALITY ASSESSMENT (profiling)
# -----------------------------
print("\n--- Missing values per column ---")
print(df.isnull().sum())

print("\n--- Duplicate rows ---")
print("Full duplicates:", df.duplicated().sum())

print("\n--- Unique values in categorical fields (before cleaning) ---")
for col in ["Gender", "Country", "PaymentMethod"]:
    print(f"{col}: {df[col].dropna().unique()}")

print("\n--- Quantity summary (checking invalid entries) ---")
print(df["Quantity"].describe())

print("\n--- UnitPrice summary (checking outliers) ---")
print(df["UnitPrice"].describe())

# -----------------------------
# 3. CLEANING
# -----------------------------

# 3.1 Remove exact duplicate rows
df = df.drop_duplicates()

# 3.2 Standardize Gender
gender_map = {
    "M": "Male", "m": "Male", "Male": "Male",
    "F": "Female", "f": "Female", "Female": "Female"
}
df["Gender"] = df["Gender"].map(gender_map)
df["Gender"] = df["Gender"].fillna("Unknown")

# 3.3 Standardize Country
country_map = {
    "USA": "United States", "U.S.A": "United States", "usa": "United States",
    "United States": "United States",
    "India": "India", "india": "India", "INDIA": "India",
    "UK": "United Kingdom", "U.K.": "United Kingdom", "United Kingdom": "United Kingdom",
    "Canada": "Canada", "canada": "Canada",
    "Germany": "Germany", "germany": "Germany"
}
df["Country"] = df["Country"].map(country_map)
df["Country"] = df["Country"].fillna("Unknown")

# 3.4 Standardize PaymentMethod
payment_map = {
    "Credit Card": "Credit Card", "credit card": "Credit Card",
    "Debit Card": "Debit Card",
    "UPI": "UPI", "upi": "UPI",
    "Cash on Delivery": "Cash on Delivery", "COD": "Cash on Delivery",
    "PayPal": "PayPal", "paypal": "PayPal"
}
df["PaymentMethod"] = df["PaymentMethod"].map(payment_map)
df["PaymentMethod"] = df["PaymentMethod"].fillna("Unknown")

# 3.5 Standardize date formats (multiple formats -> single ISO format)
def parse_any_date(value):
    if pd.isna(value):
        return pd.NaT
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y", "%d-%b-%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(str(value), fmt)
        except ValueError:
            continue
    return pd.NaT  # unparseable date

df["DateOfBirth"] = df["DateOfBirth"].apply(parse_any_date)
df["PurchaseDate"] = df["PurchaseDate"].apply(parse_any_date)

# Drop rows where PurchaseDate could not be parsed (core to analysis)
df = df.dropna(subset=["PurchaseDate"])

# 3.6 Fix invalid Quantity (negative values -> absolute value, treated as entry error)
df["Quantity"] = df["Quantity"].abs()

# 3.7 Handle missing UnitPrice: impute with category median
df["UnitPrice"] = df.groupby("ProductCategory")["UnitPrice"].transform(
    lambda x: x.fillna(x.median())
)

# 3.8 Handle outliers in UnitPrice using IQR capping
Q1 = df["UnitPrice"].quantile(0.25)
Q3 = df["UnitPrice"].quantile(0.75)
IQR = Q3 - Q1
upper_bound = Q3 + 1.5 * IQR
lower_bound = max(Q1 - 1.5 * IQR, 0)
outlier_count = ((df["UnitPrice"] > upper_bound) | (df["UnitPrice"] < lower_bound)).sum()
print(f"\nOutliers capped in UnitPrice: {outlier_count}")
df["UnitPrice"] = df["UnitPrice"].clip(lower=lower_bound, upper=upper_bound)

# Recalculate TotalAmount after cleaning Quantity/UnitPrice
df["TotalAmount"] = (df["Quantity"] * df["UnitPrice"]).round(2)

# 3.9 Clean CustomerFeedback free text
df["CustomerFeedback"] = df["CustomerFeedback"].fillna("No feedback provided")
df["CustomerFeedback"] = df["CustomerFeedback"].replace("", "No feedback provided")
df["CustomerFeedback"] = df["CustomerFeedback"].replace("n/a", "No feedback provided")

# Simple rule-based sentiment categorization (feature engineering on free text)
positive_words = ["great", "excellent", "good", "love", "recommend", "5 stars", "value"]
negative_words = ["not happy", "bad", "damaged", "late", "worst", "poor"]

def tag_sentiment(text):
    t = str(text).lower()
    if any(w in t for w in negative_words):
        return "Negative"
    if any(w in t for w in positive_words):
        return "Positive"
    if t == "no feedback provided":
        return "No Feedback"
    return "Neutral"

df["FeedbackSentiment"] = df["CustomerFeedback"].apply(tag_sentiment)

# -----------------------------
# 4. FEATURE ENGINEERING
# -----------------------------

# 4.1 Customer Age from DateOfBirth
REFERENCE_DATE = datetime(2025, 1, 1)

def calculate_age(dob):
    if pd.isna(dob):
        return np.nan
    return REFERENCE_DATE.year - dob.year - ((REFERENCE_DATE.month, REFERENCE_DATE.day) < (dob.month, dob.day))

df["CustomerAge"] = df["DateOfBirth"].apply(calculate_age)
df["CustomerAge"] = df["CustomerAge"].fillna(df["CustomerAge"].median()).astype(int)

# 4.2 Age Group categorization
def age_group(age):
    if age < 18:
        return "Under 18"
    elif age < 25:
        return "18-24"
    elif age < 35:
        return "25-34"
    elif age < 45:
        return "35-44"
    elif age < 60:
        return "45-59"
    else:
        return "60+"

df["AgeGroup"] = df["CustomerAge"].apply(age_group)

# 4.3 Format dates back to a clean, consistent ISO string for storage
df["DateOfBirth"] = df["DateOfBirth"].dt.strftime("%Y-%m-%d")
df["PurchaseDate"] = df["PurchaseDate"].dt.strftime("%Y-%m-%d")

# -----------------------------
# 5. FINAL CHECKS & EXPORT
# -----------------------------
print("\nFinal shape:", df.shape)
print("\nRemaining missing values:\n", df.isnull().sum())

df.to_csv(CLEAN_PATH, index=False)
print(f"\nCleaned dataset saved to {CLEAN_PATH}")
