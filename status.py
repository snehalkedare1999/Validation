import pandas as pd

# Load the file
file_path = r"C:\Users\skedare\Documents\workspace\python-project\input file\Sydney_Status.csv"
df = pd.read_csv(r"C:\Users\skedare\Documents\workspace\python-project\input file\Sydney_Status.csv")

# Rename columns for easier reference
df.columns = [col.strip() for col in df.columns]

# Validation function
def validate_row(row):
    errors = {}

    # 1. PLACEID: 41 characters exactly, no nulls or extra spaces
    placeid = str(row['PLACEID']).strip()
    if len(placeid) != 41 or row['PLACEID'] != placeid:
        errors['PLACEID'] = 'Invalid'

    # 2. CHANGETYPE: must be exactly "UPDATE", case sensitive, no spaces/nulls
    changetype = str(row['CHANGETYPE']).strip()
    if changetype != "UPDATE":
        errors['CHANGETYPE'] = 'Invalid'

    # 3. ATTRIBUTENAME: must be exactly "STATUS", case sensitive, no spaces/nulls
    attributename = str(row['ATTRIBUTENAME']).strip()
    if attributename != "STATUS":
        errors['ATTRIBUTENAME'] = 'Invalid'

    # 4. PLACESTATUS: must be exactly "INACTIVE", case sensitive, no spaces/nulls
    placestatus = str(row['PLACESTATUS']).strip()
    if placestatus != "INACTIVE":
        errors['PLACESTATUS'] = 'Invalid'

    return errors

# Apply validation
validation_results = df.apply(validate_row, axis=1)

# Separate valid and invalid rows
valid_rows = df[validation_results.apply(lambda x: len(x) == 0)].copy()
invalid_rows = df[validation_results.apply(lambda x: len(x) > 0)].copy()

# Add error details to invalid rows
invalid_rows['ValidationErrors'] = validation_results[validation_results.apply(lambda x: len(x) > 0)].apply(lambda x: ', '.join(x.keys()))

# Export to Excel
valid_output = r"C:\Users\skedare\Downloads\Sydney_status_valid.xlsx"
invalid_output = r"C:\Users\skedare\Downloads\Sydney_Status_Invalid(4).csv"

valid_rows.to_csv(valid_output, index=False)
invalid_rows.to_csv(invalid_output, index=False)

print(f"Validation complete. Files saved as '{r"C:\Users\skedare\Downloads\Sydney_status_valid.xlsx"}' and '{r"C:\Users\skedare\Downloads\Sydney_Status_Invalid(4).csv"}'.")
