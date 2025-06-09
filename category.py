import pandas as pd
import re

# File paths
input_file = r"C:\Users\skedare\Downloads\Sydney_Category.csv"
valid_output_path = r"C:\Users\skedare\Downloads\Sydney_Category_Valid(1).csv"
invalid_output_path = r"C:\Users\skedare\Downloads\Sydney_Category_Invalid(1).csv"

# Load the CSV file
df = pd.read_csv(r"C:\Users\skedare\Downloads\Sydney_Category.csv")

valid_rows = []
invalid_rows = []

# Helper function to validate Category ID format (e.g. 700-7400-0140)
def is_valid_category_id(cat_id):
    if pd.isna(cat_id) or not isinstance(cat_id, str):
        return False
    cat_id = cat_id.strip()
    return bool(re.fullmatch(r'\d{3}-\d{4}-\d{4}', cat_id))

# Iterate over each row
for _, row in df.iterrows():
    errors = {}

    # PLACEID: Exactly 41 characters, no spaces, not null
    placeid = str(row.get("PLACEID", "")).strip()
    if len(placeid) != 41 or pd.isna(row["PLACEID"]) or placeid != row["PLACEID"]:
        errors["PLACEID"] = "Invalid PLACEID (must be exactly 41 characters, no spaces, no nulls)"

    # CHANGETYPE: Must be exactly "UPDATE"
    changetype = str(row.get("CHANGETYPE", "")).strip()
    if changetype != "UPDATE":
        errors["CHANGETYPE"] = "Must be 'UPDATE' exactly"

    # ATTRIBUTENAME: Must be exactly "CATEGORY"
    attr_name = str(row.get("ATTRIBUTENAME", "")).strip()
    if attr_name != "CATEGORY":
        errors["ATTRIBUTENAME"] = "Must be 'CATEGORY' exactly"

    # PRIMARYCATEGORY: Must be exactly "TRUE"
    primary_cat = str(row.get("PRIMARYCATEGORY", "")).strip()
    if primary_cat != "TRUE":
        errors["PRIMARYCATEGORY"] = "Must be 'TRUE' exactly"

    # CATEGORYSYSTEMTYPE: Must be exactly "navteq-lcms"
    cat_sys_type = str(row.get("CATEGORYSYSTEMTYPE", "")).strip()
    if cat_sys_type != "navteq-lcms":
        errors["CATEGORYSYSTEMTYPE"] = "Must be 'navteq-lcms' exactly"

    # ID: Must match format 700-7400-0140 (13 characters, hyphen-separated, digits only)
    cat_id = str(row.get("ID", "")).strip()
    if not is_valid_category_id(cat_id):
        errors["ID"] = "Must be in format 700-7400-0140 (digits and hyphens only)"

    # PREVIOUSCATEGORYSYSTEMTYPE: Must be exactly "navteq-lcms"
    prev_cat_sys_type = str(row.get("PREVIOUSCATEGORYSYSTEMTYPE", "")).strip()
    if prev_cat_sys_type != "navteq-lcms":
        errors["PREVIOUSCATEGORYSYSTEMTYPE"] = "Must be 'navteq-lcms' exactly"

    # PREVIOUSID: Same format as ID
    prev_id = str(row.get("PREVIOUSID", "")).strip()
    if not is_valid_category_id(prev_id):
        errors["PREVIOUSID"] = "Must be in format 700-7400-0140 (digits and hyphens only)"

    # Append to valid or invalid list
    if errors:
        row_dict = row.to_dict()
        row_dict["Validation_Errors"] = "; ".join([f"{k}: {v}" for k, v in errors.items()])
        invalid_rows.append(row_dict)
    else:
        valid_rows.append(row.to_dict())

# Convert to DataFrames
valid_df = pd.DataFrame(valid_rows)
invalid_df = pd.DataFrame(invalid_rows)

# Export to CSV files
valid_df.to_csv(r"C:\Users\skedare\Downloads\Sydney_Category_Valid(1).csv", index=False)
invalid_df.to_csv(r"C:\Users\skedare\Downloads\Sydney_Category_Invalid(1).csv", index=False)

print("✅ Validation complete.")
print("✔ Valid entries saved to:", r"C:\Users\skedare\Downloads\Sydney_Category_Valid(1).csv")
print("✖ Invalid entries saved to:", r"C:\Users\skedare\Downloads\Sydney_Category_Invalid(1).csv")
