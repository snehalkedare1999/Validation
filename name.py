import pandas as pd
import re

# Load Excel file
input_file = r"C:\Users\skedare\Downloads\Sydney_Name.csv"  # Update if needed
df = pd.read_csv(r"C:\Users\skedare\Downloads\Sydney_Name.csv")

# Ensure headers are stripped of whitespace
df.columns = [col.strip() for col in df.columns]

# Define valid language codes (you can expand this if needed)
valid_language_codes = {'id', 'en'}

# Validation function
def validate_row(row):
    errors = {}

    # 1. PLACEID
    placeid = str(row['PLACEID']).strip()
    if len(placeid) != 41 or row['PLACEID'] != placeid:
        errors['PLACEID'] = 'Must be exactly 41 chars, no extra spaces or nulls'

    # 2. CHANGETYPE
    changetype = str(row['CHANGETYPE']).strip()
    if changetype != "UPDATE":
        errors['CHANGETYPE'] = 'Must be "UPDATE" exactly'

    # 3. ATTRIBUTENAME
    attributename = str(row['ATTRIBUTENAME']).strip()
    if attributename != "NAME":
        errors['ATTRIBUTENAME'] = 'Must be "NAME" exactly'

    # 4. PRIMARY
    primary = str(row['PRIMARY']).strip()
    if primary != "TRUE":
        errors['PRIMARY'] = 'Must be "TRUE" exactly'

    # 5. LANGUAGECODE
    languagecode = str(row['LANGUAGECODE']).strip()
    if languagecode not in valid_language_codes:
        errors['LANGUAGECODE'] = 'Must be valid country code like "id" or "en"'

    # 6. NAMETYPE
    nametype = str(row['NAMETYPE']).strip()
    if nametype != "OFFICIAL":
        errors['NAMETYPE'] = 'Must be "OFFICIAL" exactly'

    # 7. BASETEXT
    basetext = str(row['BASETEXT']).strip()
    if pd.isna(row['BASETEXT']) or len(basetext) == 0:
        errors['BASETEXT'] = 'Cannot be empty'
        
    # 2. Only allowed characters: A-Z, a-z, 0-9, &, -, .
    elif not re.match(r'^[A-Za-z0-9&\-. ]+$', basetext):
        errors['BASETEXT'] = 'Only letters, digits, &, -, and . allowed'
    elif '  ' in basetext:
        errors['BASETEXT'] = 'No extra spaces allowed'
    elif re.search(r'\s*-\s*', basetext) and (' -' in basetext or '- ' in basetext):
        errors['BASETEXT'] = 'No space before/after hyphen allowed'
    elif re.search(r'\b(LTD|PVT)\b', basetext, flags=re.IGNORECASE):
        errors['BASETEXT'] = 'LTD and PVT not allowed in name'

    # 8. PREVIOUS_NAMETYPE
    prev_nametype = str(row['PREVIOUS_NAMETYPE']).strip()
    if prev_nametype != "OFFICIAL":
        errors['PREVIOUS_NAMETYPE'] = 'Must be "OFFICIAL" exactly'

    # 9. PREVIOUS_LANGUAGECODE
    prev_lang = str(row['PREVIOUS_LANGUAGECODE']).strip()
    if prev_lang not in valid_language_codes:
        errors['PREVIOUS_LANGUAGECODE'] = 'Must be valid country code like "id" or "en"'

    # 10. PREVIOUS_BASETEXT
    prev_basetext = str(row['PREVIOUS_BASETEXT']).strip()
    if pd.isna(row['PREVIOUS_BASETEXT']) or len(prev_basetext) == 0:
        errors['PREVIOUS_BASETEXT'] = 'Must not be empty'

    return errors

# Apply validation
validation_results = df.apply(validate_row, axis=1)

# Separate valid and invalid
valid_df = df[validation_results.apply(lambda x: len(x) == 0)].copy()
invalid_df = df[validation_results.apply(lambda x: len(x) > 0)].copy()
invalid_df['ValidationErrors'] = validation_results[validation_results.apply(lambda x: len(x) > 0)].apply(lambda x: '; '.join(x.keys()))

# Save outputs
valid_output_path = r"C:\Users\skedare\Downloads\Sydney_Name_Valid(3).csv"
invalid_output_path = r"C:\Users\skedare\Downloads\Sydney_Name_Invalid(3).csv"

valid_df.to_csv(valid_output_path, index=False)
invalid_df.to_csv(invalid_output_path, index=False)

print(f"Validation complete. Files saved as:\n✔ {r"C:\Users\skedare\Downloads\Sydney_Name_Valid(3).csv"}\n✖ {r"C:\Users\skedare\Downloads\Sydney_Name_Invalid(3).csv"}")
