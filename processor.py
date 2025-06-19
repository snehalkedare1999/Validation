import pandas as pd
import re
import os
import math

# Allowed language codes
valid_language_codes = {'id', 'en'}

def validate_row(row, duplicate_placeid_mask):
    """
    Validates a single row from the input DataFrame.
    Returns a dictionary of column-specific errors.
    """
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
    elif not re.match(r'^[A-Za-z0-9&\-. ]+$', basetext):
        errors['BASETEXT'] = 'Only letters, digits, &, -, and . allowed'
    elif '  ' in basetext:
        errors['BASETEXT'] = 'No extra spaces allowed'
    elif re.search(r'\s*-\s*', basetext) and (' -' in basetext or '- ' in basetext):
        errors['BASETEXT'] = 'No space before/after hyphen allowed'
    elif re.search(r'\b(LTD|PVT)\b', basetext, flags=re.IGNORECASE):
        errors['BASETEXT'] = 'LTD and PVT not allowed in name'
    elif duplicate_placeid_mask[row.name]:
        errors["PLACEID_DUPLICATE"] = "Duplicate PLACEID found"

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


def validate_row_category(row,duplicate_placeid_mask):
    # Helper: Validate Category ID format (e.g. 700-7400-0140)
    def is_valid_category_id(cat_id):
        if pd.isna(cat_id) or not isinstance(cat_id, str):
            return False
        cat_id = cat_id.strip()
        return bool(re.fullmatch(r'\d{3}-\d{4}-\d{4}', cat_id))

    # Protected category list
    protected_categories = {
        "400-4000-4581", "400-4000-4582", "700-7800-0118", "800-8100-0172",
        "400-4100-0038", "400-4100-0039", "700-7900-0130", "800-8100-0164",
        "800-8600-0193", "900-9100-0214", "800-8200-0173", "400-4100-0226",
        "800-8000-0159", "800-8000-0325", "800-8100-0165", "700-7800-0120",
        "900-9100-0215", "900-9100-0216", "400-4100-0047", "400-4100-0037"
    }

    errors = {}

    placeid = str(row.get("PLACEID", "")).strip()
    if len(placeid) != 41 or pd.isna(row["PLACEID"]) or placeid != row["PLACEID"]:
        errors["PLACEID"] = "Must be exactly 41 chars, no spaces or nulls"

    if str(row.get("CHANGETYPE", "")).strip() != "UPDATE":
        errors["CHANGETYPE"] = "Must be 'UPDATE'"

    if str(row.get("ATTRIBUTENAME", "")).strip() != "CATEGORY":
        errors["ATTRIBUTENAME"] = "Must be 'CATEGORY'"

    # ✅ Accept only string 'TRUE' in uppercase (case-sensitive)
    if str(row.get("PRIMARYCATEGORY", "")).strip() != "TRUE":
        errors["PRIMARYCATEGORY"] = "Must be 'TRUE' (string, all caps only)"

    if str(row.get("CATEGORYSYSTEMTYPE", "")).strip() != "navteq-lcms":
        errors["CATEGORYSYSTEMTYPE"] = "Must be 'navteq-lcms'"

    cat_id = str(row.get("ID", "")).strip()
    if not is_valid_category_id(cat_id):
        errors["ID"] = "Invalid format (700-7400-0140)"

    if str(row.get("PREVIOUSCATEGORYSYSTEMTYPE", "")).strip() != "navteq-lcms":
        errors["PREVIOUSCATEGORYSYSTEMTYPE"] = "Must be 'navteq-lcms'"

    prev_id = str(row.get("PREVIOUSID", "")).strip()
    if not is_valid_category_id(prev_id):
        errors["PREVIOUSID"] = "Invalid format"
    elif prev_id in protected_categories:
        errors["PREVIOUSID"] = "Protected ID not allowed"

    if duplicate_placeid_mask[row.name]:
        errors["PLACEID_DUPLICATE"] = "Duplicate PLACEID found"
        
    return errors
    
    
#status
# Validation function
def validate_row_status(row, duplicate_placeid_mask):
    errors = {}

    # 1. PLACEID: 41 characters exactly, no nulls or extra spaces
    placeid = str(row['PLACEID']).strip()
    if len(placeid) != 41 or row['PLACEID'] != placeid:
        errors['PLACEID'] = 'Invalid format (must be 41 chars, no spaces)'

    if duplicate_placeid_mask[row.name]:
        errors['PLACEID_DUPLICATE'] = 'Duplicate PLACEID found'

    # 2. CHANGETYPE: must be exactly "UPDATE"
    changetype = str(row['CHANGETYPE']).strip()
    if changetype != "UPDATE":
        errors['CHANGETYPE'] = 'Must be UPDATE'

    # 3. ATTRIBUTENAME: must be exactly "STATUS"
    attributename = str(row['ATTRIBUTENAME']).strip()
    if attributename != "STATUS":
        errors['ATTRIBUTENAME'] = 'Must be STATUS'

    # 4. PLACESTATUS: must be exactly "INACTIVE"
    placestatus = str(row['PLACESTATUS']).strip()
    if placestatus != "INACTIVE":
        errors['PLACESTATUS'] = 'Must be INACTIVE'

    return errors


def get_geo_distance(row):
    def is_valid_coordinate(val):
        if pd.isnull(val):
            return True
        return bool(re.match(r'^-?\d+(\.\d+)?$', str(val))) and str(val).strip() == str(val)

    def haversine(lat1, lon1, lat2, lon2):
        R = 6371000  # Earth radius in meters
        try:
            lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])
        except:
            return None

        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return round(R * c, 2)
    
    lat1 = row.get("DISPLAY_GEO_POSITION_LATITUDE", "")
    lon1 = row.get("DISPLAY_GEO_POSITION_LONGITUDE", "")
    lat2 = row.get("ROUTING_GEO_POSITION_LATITUDE", "")
    lon2 = row.get("ROUTING_GEO_POSITION_LONGITUDE", "")
    # Calculate Haversine distance
    distance = haversine(lat1, lon1, lat2, lon2) if all(is_valid_coordinate(x) for x in [lat1, lon1, lat2, lon2]) else None
    
    return distance
    
    ## Helper function section ENDS
    
def validate_row_location(row, duplicate_placeids):
    ## Helper Function section start 
    # --- Validation Functions ---
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

    # --- Haversine Distance ---
    try:
        errors = []
        row_dict = row.to_dict()

        placeid = row.get("PLACEID", "")
        if not is_valid_placeid(placeid):
            errors.append("Invalid PLACEID")

        if duplicate_placeids[row.name]:
            errors.append("Duplicate PLACEID")

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

        lat1 = row.get("DISPLAY_GEO_POSITION_LATITUDE", "")
        lon1 = row.get("DISPLAY_GEO_POSITION_LONGITUDE", "")
        lat2 = row.get("ROUTING_GEO_POSITION_LATITUDE", "")
        lon2 = row.get("ROUTING_GEO_POSITION_LONGITUDE", "")

        if not is_valid_coordinate(lat1):
            errors.append("Invalid DISPLAY_GEO_POSITION_LATITUDE")
        if not is_valid_coordinate(lon1):
            errors.append("Invalid DISPLAY_GEO_POSITION_LONGITUDE")
        if not is_valid_coordinate(lat2):
            errors.append("Invalid ROUTING_GEO_POSITION_LATITUDE")
        if not is_valid_coordinate(lon2):
            errors.append("Invalid ROUTING_GEO_POSITION_LONGITUDE")

        # Check if all essential fields are missing
        essential_fields = [row.get("FULLROADNAME"), row.get("HOUSENUMBER"), row.get("POSTALCODE"),
                            lat1, lon1, lat2, lon2]
        if all(pd.isnull(val) or str(val).strip() == "" for val in essential_fields):
            errors.append("All essential fields are empty or null")
        
        error_dict = {key: f"{key} is invalid" for key in errors}

        return error_dict
    except Exception as e:
        print(e)
        return {}
        
        
        
def process_file(action,input_file, output_folder):
    """
    Validates the input CSV and generates two output files:
    - Valid records CSV
    - Invalid records CSV with validation error summary
    
    Returns:
        (valid_output_path, invalid_output_path)
    """
    # Load input
    df = pd.read_csv(input_file)
    df.columns = [col.strip() for col in df.columns]  # Remove extra spaces in headers
     # 2. Now it's safe to use df
    duplicate_placeid_mask = df.duplicated(subset=["PLACEID"], keep=False)


    # Apply validation
    if action== "name": 
        validation_results = df.apply(lambda row: validate_row(row, duplicate_placeid_mask), axis=1)
    elif action == "status":
        validation_results = df.apply(lambda row: validate_row_status(row, duplicate_placeid_mask), axis=1)

    elif action == "location":
        df["GEO_DISTANCE_METERS"] = df.apply(get_geo_distance,axis=1)
        validation_results = df.apply(lambda row: validate_row_location(row, duplicate_placeid_mask), axis=1)

    elif action=="category":
        duplicate_placeid_mask = df.duplicated(subset=["PLACEID"], keep=False)
        validation_results = df.apply(validate_row_category, axis=1, args=(duplicate_placeid_mask,))

    else:
        raise ValueError(f"Unsupported action type: {action}")


    # Split valid and invalid
    valid_df = df[validation_results.apply(lambda x: len(x) == 0)].copy()
    invalid_df = df[validation_results.apply(lambda x: len(x) > 0)].copy()

    # Add validation error summary column
    invalid_df['ValidationErrors'] = validation_results[validation_results.apply(lambda x: len(x) > 0)]\
        .apply(lambda x: '; '.join(x.keys()))

    # Generate output file names
    filename = os.path.basename(input_file)
    valid_output_path = os.path.join(output_folder, f'valid_{filename}')
    invalid_output_path = os.path.join(output_folder, f'invalid_{filename}')

    # Save output CSVs
    valid_df.to_csv(valid_output_path, index=False)
    invalid_df.to_csv(invalid_output_path, index=False)

    return valid_output_path, invalid_output_path
