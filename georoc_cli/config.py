# ╔════════════════════════════════════════════════════╗
# ║ Define your API key here, avoid any other changes. ║
# ╚════════════════════════════════════════════════════╝

api_key = "YOUR_API_KEY_HERE"

base_url = "https://api-test.georoc.eu/api/v1/"

headers = {
    "accept": "application/json",
    "DIGIS-API-ACCESSKEY": api_key
}

# Define all possible JSON keys
json_keys = [
    'Sample_Num', 'unique_id', 'Batches', 'References', 'SampleName', 'Location_Names', 'Location_Types', 'Loc_Data',
    'Elevation_Min', 'Elevation_Max', 'Land_Or_Sea', 'Rock_Types', 'Rock_Classes', 'Rock_Textures', 'Age_Min',
    'Age_Max', 'Materials', 'Minerals', 'Inclusion_Types', 'Location_Num', 'Latitude', 'Longitude', 'Latitude_Min',
    'Latitude_Max', 'Longitude_Min', 'Longitude_Max', 'Tectonic_Setting', 'Method', 'Comment', 'Institution',
    'Item_Name', 'Item_Group', 'Standard_Names', 'Standard_Values', 'Values', 'Units'
]

# Schlüssel aus der get_filtered_samples Funktion
get_filtered_samples_keys = [
    'limit', 'offset', 'setting', 'location1', 'location2', 'location3', 'rocktype', 'rockclass', 'mineral',
    'element', 'elementtype', 'material', 'inclusiontype', 'sampletech', 'value', 'doi', 'title', 'publicationyear',
    'firstname', 'lastname'
]
