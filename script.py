import time
import json
import openai
import requests
import pandas as pd

# Set your OpenAI API key
openai.api_key = "sk-..."  # Replace with your actual OpenAI API key
MODEL_NAME = "gpt-4"  # or "gpt-3.5-turbo" if using free-tier

# Paths
# Fixed the double quote error
INPUT_PATH = "C:\\Users\\skedare\\Downloads\\Sampled_150.csv"
OUTPUT_PATH = "C:\\Users\\skedare\\Desktop\\map.xlsx"  # Fixed extra quotes

# Functions


def ask_copilot(prompt):
    try:
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Copilot Error:", e)
        return "Copilot failed to generate summary."


def build_overpass_query(lat, lon, radius=500):


query = f"""
[out:json];
(
node(around:{radius},{lat},{lon})[name][amenity];
node(around:{radius},{lat},{lon})[name][shop];
node(around:{radius},{lat},{lon})[name][tourism];
node(around:{radius},{lat},{lon})[name][building];
);
out body 5;
"""
return query.strip()


def query_overpass(query):


try:
response = requests.post("http://overpass-api.de/api/interpreter", data=query)
return response.json()
except Exception as e:
print("Overpass query error:", e)
return {"elements": []}


def get_address_from_nominatim(lat, lon):


try:
url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1"
response = requests.get(url, headers={'User-Agent': 'POI-Enricher/1.0'})
data = response.json().get('address', {})
return {
    "house_number": data.get("house_number", ""),
    "road": data.get("road", ""),
    "suburb": data.get("suburb", ""),
    "postcode": data.get("postcode", ""),
    "city": data.get("city", data.get("town", "")),
    "state": data.get("state", ""),
    "country": data.get("country", "")
}
except Exception as e:
print("Nominatim error:", e)
return {}


def enrich_pois_with_copilot(pois, lat, lon):


if not pois:
return "No POIs found nearby."

prompt = f"""
I have the following 5 Points of Interest (POIs) near latitude {lat}, longitude {lon}:

{json.dumps(pois, indent=2)}

Please summarize:
- Count of POIs
- Top POIs with name and type
- Whether the area is residential, commercial, or mixed
- A concise 2-line summary
"""
return ask_copilot(prompt)


def main():


    # Load the CSV file
df = pd.read_csv(INPUT_PATH)
results = []

# Iterate through each row of the dataframe
for index, row in df.iterrows():
lat, lon = row['Latitude'], row['Longitude']
print(f"Processing: {lat}, {lon}")

# Build and run Overpass query
overpass_query = build_overpass_query(lat, lon)
overpass_data = query_overpass(overpass_query)
elements = overpass_data.get("elements", [])[:5]

# Extract POIs
pois = []
for el in elements:
tags = el.get("tags", {})
if tags:
pois.append({
    "name": tags.get("name", "Unnamed"),
    "type": next(iter(tags.keys()), "unknown"),
    "value": next(iter(tags.values()), "unknown")
})

# Get AI summary for POIs
summary = enrich_pois_with_copilot(pois, lat, lon)

# Get address information from Nominatim API
address = get_address_from_nominatim(lat, lon)

# Append result
results.append({
    "Latitude": lat,
    "Longitude": lon,
    "Full Address": f"{address.get('house_number', '')} {address.get('road', '')}, {address.get('suburb', '')}, {address.get('city', '')}, {address.get('state', '')}, {address.get('postcode', '')}, {address.get('country', '')}",
    "Raw POIs": json.dumps(pois, indent=2),
    "GenAI Summary": summary
})

# Sleep to avoid rate-limiting
time.sleep(1.2)

# Save the results to Excel
df_result = pd.DataFrame(results)
df_result.to_excel(OUTPUT_PATH, index=False)
print(f"Enrichment complete. Output saved to: {OUTPUT_PATH}")

# Run the main function
if __name__ == "__main__":
main()
