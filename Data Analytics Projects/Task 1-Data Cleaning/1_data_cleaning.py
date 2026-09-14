"""
TASK 1: Data Cleaning in Excel/Python
--------------------------------------
Input : sample_sales_raw.csv   (messy)
Output: sample_sales_cleaned.csv  (clean, analysis-ready)
        cleaning_log.txt          (what was done, for the report)

Cleaning steps performed:
1. Standardise text columns (Region, Product) -> strip spaces, title case
2. Fix inconsistent date formats -> single ISO format (YYYY-MM-DD)
3. Handle missing values:
   - Missing Region -> "Unknown"
   - Missing Quantity / UnitPrice -> row dropped (can't compute revenue)
4. Fix bad data entries (Quantity given as text, e.g. "five")
5. Remove negative / zero Quantity or UnitPrice (data entry errors)
6. Remove exact duplicate rows
7. Add a calculated "Revenue" column (Quantity * UnitPrice)
"""
import pandas as pd
import numpy as np

log = []

def note(msg):
    print(msg)
    log.append(msg)

df = pd.read_csv("/home/claude/project/sample_sales_raw.csv")
note(f"Loaded raw file with {len(df)} rows.")

# 1. Remove exact duplicates
before = len(df)
df = df.drop_duplicates()
note(f"Removed {before - len(df)} exact duplicate rows.")

# 2. Standardise text columns
df["Region"] = df["Region"].astype(str).str.strip().str.title()
df["Region"] = df["Region"].replace({"Nan": np.nan})
df["Product"] = df["Product"].astype(str).str.strip().str.title().str.replace(r"\s+", " ", regex=True)
df["Customer"] = df["Customer"].astype(str).str.strip()
df["SalesRep"] = df["SalesRep"].astype(str).str.strip()

# 3. Fix bad Quantity entries (text like "five")
word_to_num = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
df["Quantity"] = df["Quantity"].apply(
    lambda x: word_to_num.get(str(x).strip().lower(), x)
)
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")

# 4. Parse inconsistent date formats -> ISO
df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce", dayfirst=False, format="mixed")
bad_dates = df["OrderDate"].isna().sum()
note(f"Rows with unparseable dates: {bad_dates} (dropped).")
df = df.dropna(subset=["OrderDate"])

# 5. Handle missing Region -> Unknown
missing_region = df["Region"].isna().sum()
df["Region"] = df["Region"].fillna("Unknown")
note(f"Filled {missing_region} missing Region values with 'Unknown'.")

# 6. Drop rows with missing/invalid/non-positive Quantity or UnitPrice
before = len(df)
df = df.dropna(subset=["Quantity", "UnitPrice"])
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]
note(f"Dropped {before - len(df)} rows with missing/zero/negative Quantity or UnitPrice.")

# 7. Add Revenue column
df["Revenue"] = (df["Quantity"] * df["UnitPrice"]).round(2)

# Final tidy up
df["OrderDate"] = df["OrderDate"].dt.strftime("%Y-%m-%d")
df = df.sort_values("OrderID").reset_index(drop=True)

note(f"Final cleaned row count: {len(df)}")

df.to_csv("/home/claude/project/sample_sales_cleaned.csv", index=False)
with open("/home/claude/project/cleaning_log.txt", "w") as f:
    f.write("DATA CLEANING LOG\n" + "=" * 30 + "\n")
    f.write("\n".join(log))

print("\nSaved cleaned file -> sample_sales_cleaned.csv")
print(df.head())
