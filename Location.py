import pandas as pd
import re

# Load the file
input_file = r"C:\Users\skedare\Downloads\Sydney_Location.csv"
df = pd.read_csv(r"C:\Users\skedare\Downloads\Sydney_Location.csv")

valid_rows = []
invalid_rows = []

def is_valid_placeid(val):
    return isinstance(val, str) and val.strip() == val and len(val) == 41

def is_valid_keyword(val, expected):
    return isinstance(val, str) and val.strip() == expected

def is_valid_fullroadname(val):
    if pd.isnull(val):
        return True
    return bool(re.match(r'^[\w\s\-]*$', val)) and val.strip() == val

def is_valid_housenumber(val):
    if pd.isnull(val):
        return True
    return bool(re.match(r'^[A-Za-z0-9\-/]+$', str(val))) and str(val).strip() == str(val)

def is_valid_postalcode(val):
    if pd.isnull(val):
        return True
    return bool(re.match(r'^[A-Za-z0-9\s]+$', str(val)))

def is_valid_coordinate(val):
    if pd.isnull(val):
        return True
    return bool(re.match(r'^-?\d+(\.\d+)?$', str(val))) and str(val).strip() == str(val)

# Process each row
for index, row in df.iterrows():
    errors = []

    if not is_valid_placeid(row.get("PLACEID", "")):
        errors.append("Invalid PLACEID")

    if not is_valid_keyword(row.get("CHANGETYPE", ""), "UPDATE"):
        errors.append("Invalid CHANGETYPE")

    if not is_valid_keyword(row.get("ATTRIBUTENAME", ""), "LOCATION"):
        errors.append("Invalid ATTRIBUTENAME")

    if not is_valid_fullroadname(row.get("FULLROADNAME", "")):
        errors.append("Invalid FULLROADNAME")

    if not is_valid_housenumber(row.get("HOUSENUMBER", "")):
        errors.append("Invalid HOUSENUMBER")

    if not is_valid_postalcode(row.get("POSTALCODE", "")):
        errors.append("Invalid POSTALCODE")

    if not is_valid_coordinate(row.get("DISPLAY_GEO_POSITION_LATITUDE", "")):
        errors.append("Invalid DISPLAY_GEO_POSITION_LATITUDE")

    if not is_valid_coordinate(row.get("DISPLAY_GEO_POSITION_LONGITUDE", "")):
        errors.append("Invalid DISPLAY_GEO_POSITION_LONGITUDE")

    if not is_valid_coordinate(row.get("ROUTING_GEO_POSITION_LATITUDE", "")):
        errors.append("Invalid ROUTING_GEO_POSITION_LATITUDE")

    if not is_valid_coordinate(row.get("ROUTING_GEO_POSITION_LONGITUDE", "")):
        errors.append("Invalid ROUTING_GEO_POSITION_LONGITUDE")

    if errors:
        row['Error_Description'] = "; ".join(errors)
        invalid_rows.append(row)
    else:
        valid_rows.append(row)

         # ✅ New validation: at least one essential field must be present
    essential_fields = [
        row.get("FULLROADNAME"),
        row.get("HOUSENUMBER"),
        row.get("POSTALCODE"),
        row.get("DISPLAY_GEO_POSITION_LATITUDE"),
        row.get("DISPLAY_GEO_POSITION_LONGITUDE"),
        row.get("ROUTING_GEO_POSITION_LATITUDE"),
        row.get("ROUTING_GEO_POSITION_LONGITUDE"),
    ]
    if all(pd.isnull(val) or str(val).strip() == "" for val in essential_fields):
        errors.append("All essential fields are empty or null")

    if errors:
        row['Error_Description'] = "; ".join(errors)
        invalid_rows.append(row)
    else:
        valid_rows.append(row)

# Create DataFrames
valid_df = pd.DataFrame(valid_rows)
invalid_df = pd.DataFrame(invalid_rows)

# Save to Excel files
valid_df.to_csv(r"C:\Users\skedare\Downloads\Sydney_Location_Valid(1).csv", index=False)
invalid_df.to_csv(r"C:\Users\skedare\Downloads\Sydney_Location_Invalid(1).csv", index=False)

print("Validation complete. Files saved as Sydney_Location_Valid.csv and Sydney_Location_Invalid.csv")