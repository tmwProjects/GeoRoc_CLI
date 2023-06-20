import requests
import json
import pandas as pd
from config import base_url, headers
 
def api_query(endpoint, params=None):
    try:
        response = requests.get(f"{base_url}{endpoint}", headers=headers, params=params)
        if response.status_code == 200:
            data = json.loads(response.text)
            print(f"API query successful for endpoint:{endpoint}")
            print("+---------------------------------------------------------------------+")
            return data
        else:
            print(f"API query error for endpoint: {endpoint}, Statuscode:{response.status_code}")
            print("+---------------------------------------------------------------------+")
            print(response.text)
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error for endpoint: {endpoint}")
        print("+---------------------------------------------------------------------+")
        print(e)
        return None
    except json.JSONDecodeError as e:
        print(f"JSON decoding error for endpoint: {endpoint}")
        print("+---------------------------------------------------------------------+")
        print(e)
        return None
    except Exception as e:
        print(f"Unexpected error for endpoint: {endpoint}")
        print("+---------------------------------------------------------------------+")
        print(e)
        return None



def get_measurement_data(api_key, sampling_feature_id, json_key_list):
    base_url = f"https://api-test.georoc.eu/api/v1/queries/fulldata/{sampling_feature_id}"
    headers = {
        "accept": "application/json",
        "DIGIS-API-ACCESSKEY": api_key
    }

    try:
        response = requests.get(base_url, headers=headers)
        if response.status_code == 200:
            data = json.loads(response.text)['Data'][0]

            # Create a dictionary containing only the keys specified in json_key_list and their values from data
            df_data = {key: data[key] for key in json_key_list}

            # Convert all values in df_data to lists
            for key, value in df_data.items():
                if not isinstance(value, list):
                    df_data[key] = [value]

            # Find the longest list in df_data
            max_len = max([len(value) for value in df_data.values()])

            # Extend all the lists to the length of the longest list
            for key, value in df_data.items():
                if len(value) < max_len:
                    df_data[key] = value + [None] * (max_len - len(value))

            # Add the SampleID to df_data
            df_data['SampleID'] = [sampling_feature_id] * max_len

            # Create the DataFrame
            df = pd.DataFrame(df_data)

            return df

        else:
            print(f"Error fetching data for sample ID {sampling_feature_id}, Status code: {response.status_code}")
            print("+---------------------------------------------------------------------+")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request error for sample ID {sampling_feature_id}")
        print("+---------------------------------------------------------------------+")
        print(e)
        return None
    except json.JSONDecodeError as e:
        print(f"JSON decoding error for sample ID {sampling_feature_id}")
        print("+---------------------------------------------------------------------+")
        print(e)
        return None
    except Exception as e:
        print(f"Unexpected error for sample ID {sampling_feature_id}")
        print("+---------------------------------------------------------------------+")
        print(e)
        return None



def get_filtered_samples(
        limit=None,
        offset=None,
        setting=None,
        location1=None,
        location2=None,
        location3=None,
        rocktype=None,
        rockclass=None,
        mineral=None,
        element=None,
        elementtype=None,
        material=None,
        inclusiontype=None,
        sampletech=None,
        elements=None,
        value=None,
        **json_key_filters
):
    endpoint = "queries/samples"

    filters = {
        key: value
        for key, value in locals().items()
        if key not in ["endpoint"] and value is not None
    }

    # Add the JSON key filters
    filters.update(json_key_filters)

    try:
        data = api_query(endpoint, params=filters)
        return data
    except requests.exceptions.RequestException as e:
        print(f"Request error for endpoint: {endpoint}")
        print("+---------------------------------------------------------------------+")
        print(e)
        return None
    except json.JSONDecodeError as e:
        print(f"JSON decoding error for endpoint: {endpoint}")
        print("+---------------------------------------------------------------------+")
        print(e)
        return None
    except Exception as e:
        print(f"Unexpected error for endpoint: {endpoint}")
        print("+---------------------------------------------------------------------+")
        print(e)
        return None
