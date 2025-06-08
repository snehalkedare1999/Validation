import pandas as pd
import re

input_file = r"C:\Users\skedare\Downloads\Los Angeles_Name.csv"
output_file = r"C:\Users\skedare\Documents\workspace\python-project\temp.xlsx"
country_code_required = "id"  # Change to 'en' for USA if needed

#  Load the data
df = pd.read_csv(input_file)

def validate_basetext(text):
    if pd.isna(text):
        return False
    text = text.strip()
    
    # Check for disallowed special characters
    if re.search(r"[^a-zA-Z0-9\s&,\-'\.]", text):
        return False
    # Check for space around hyphen
    if re.search(r"\s-\s|\s-|- ", text):
        return False
    return True

# === 7. BASETEXT – validation ===
df['BASETEXT_valid'] = df['BASETEXT'].apply(validate_basetext)

# === 8. PREVIOUS_NAMETYPE – must be "OFFICIAL" ===
df['PREVIOUS_NAMETYPE_valid'] = df['PREVIOUS_NAMETYPE'] == "OFFICIAL"

# === 9. PREVIOUS_LANGUAGECODE – must match expected code ===
df['PREVIOUS_LANGUAGECODE_valid'] = df['PREVIOUS_LANGUAGECODE'] == country_code_required

# === 10. PREVIOUS_BASETEXT – must not be empty ===
df['PREVIOUS_BASETEXT_valid'] = df['PREVIOUS_BASETEXT'].notna() & df['PREVIOUS_BASETEXT'].astype(str).str.strip().ne("")

# === Combine all validations ===
validation_columns = [col for col in df.columns if col.endswith('_valid')]
df['ROW_VALID'] = df[validation_columns].all(axis=1)

# === Save results ===
output_file = "validated_output.xlsx"
df.to_excel(output_file, index=False)
print(f"Validation complete. Output saved to {output_file}")
