import datetime
import os
from api import api_query
import pandas as pd
import random
import sys


def check_api_connection():
    endpoint = "ping"
    response = api_query(endpoint)

    if response is not None:
        print("Connection to API server successful!")
        print("+---------------------------------------------------------------------+")
    else:
        print("Failed to connect to API server!")
        print("+---------------------------------------------------------------------+")
        sys.exit(1)
        
        
def check_api_key(api_key):
    if not api_key:
        print("+---------------------------------------------------------------------+")
        print("Note: No API key has yet been stored in the script \"config.py\".")
        print("To use the programme, please enter your API key or contact the ")
        print("Georoc database directly. For more detailed information, use the")
        print("\'python3 georoc_cli.py --help\' command.")
        print("+---------------------------------------------------------------------+")
        exit(1)


def generate_csv_filename():
    try:
        now = datetime.datetime.now()
        return f"georoc_dataset_{now.strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    except Exception as e:
        print("Error generating CSV filename:")
        print("+---------------------------------------------------------------------+")
        print(e)
        return None
    
    

def print_random(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        jokes = file.readlines()
    random_joke = random.choice(jokes).strip()
    print(f"\033[1m\033[3m\"{random_joke}\"\033[0m")


def read_description_file(filename):
    try:
        if not os.path.exists(filename):
            raise FileNotFoundError(f"The file '{filename}' does not exist.")
        with open(filename, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError as e:
        print("Error reading description file:")
        print("+---------------------------------------------------------------------+")
        print(e)
        return None
    except Exception as e:
        print("Error reading description file:")
        print("+---------------------------------------------------------------------+")
        print(e)
        return None



def check_filter_flags(args):
    filter_flags = [
        'limit',
        'offset',
        'setting',
        'location1',
        'location2',
        'location3',
        'rocktype',
        'rockclass',
        'mineral',
        'element',
        'elementtype',
        'material',
        'inclusiontype',
        'sampletech',
        'elements',
        'value'
    ]

    num_flags_set = sum(1 for flag in filter_flags if getattr(args, flag, None))

    if num_flags_set < 2:
        print("+---------------------------------------------------------------------+")
        print("\033[1mWarning\033[0m: Less than two filter flags were set.")
        print("Retrieving all data may result in a large amount of data.")
        print("Please specify at least two filter flags to limit the request.")
        print("+---------------------------------------------------------------------+")
        exit(1)


def display_manual():
    try:
        if not os.path.exists('manual.txt'):
            raise FileNotFoundError("The file 'manual.txt' does not exist.")

        with open('manual.txt', 'r') as file:
            content = file.read()
        sections = content.split('---')

        current_section = 0

        while True:
            # Clear the terminal screen
            os.system('cls' if os.name == 'nt' else 'clear')
            print("\033[H\033[J")

            print(sections[current_section])

            print('\n(N)ext section, (P)revious section, (Q)uit + [ENTER]:')
            choice = input().lower()

            if choice == 'n':
                if current_section < len(sections) - 1:
                    current_section += 1
                else:
                    print('This is the last section.')
            elif choice == 'p':
                if current_section > 0:
                    current_section -= 1
                else:
                    print('This is the first section.')
            elif choice == 'q':
                os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal screen
                break
            else:
                print('Invalid selection. Please try again.')

    except FileNotFoundError as e:
        print("Error displaying manual:")
        print("+---------------------------------------------------------------------+")
        print(e)
    except Exception as e:
        print("Error displaying manual:")
        print("+---------------------------------------------------------------------+")
        print(e)
        


def read_oxides_from_txt(file_path):
    oxides = []

    try:
        with open(file_path, 'r') as file:
            oxides = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"Datei '{file_path}' not found. Please check the file path.")
    except PermissionError:
        print(f"No permission to access the file '{file_path}'.")
    except IOError as e:
        print(f"Error reading the file '{file_path}': {e}")
    except Exception as e:
        print(f"Unexpected error while processing the file '{file_path}': {e}")

    return oxides


def structure_data(input_file, output_file):
    try:
        # 1. Daten einlesen
        df = pd.read_csv(input_file, low_memory=False)
    except FileNotFoundError:
        print(f"Data '{input_file}' not found. Please check the file path.")
        return
    except IOError as e:
        print(f"Error reading the file '{input_file}': {e}")
        return
    except Exception as e:
        print(f"Unexpected error while processing the file '{input_file}': {e}")
        return

    # Reading the elements/oxides from a text file
    oxide_list = read_oxides_from_txt("elements.txt")

    # Filtering the data by required columns and pivoting
    filtered_df = df[df['Item_Name'].isin(oxide_list)].pivot_table(index='SampleID', columns='Item_Name', values='Values', aggfunc='first')

    # Adding the "Longitude", "Latitude" and "Units" columns
    coord_df = df[['SampleID', 'Longitude', 'Latitude', 'Units']].drop_duplicates(subset='SampleID')
    coord_df['SampleID'] = coord_df['SampleID'].astype(int)  # Ändern des Datentyps auf int
    result = pd.merge(filtered_df.reset_index(), coord_df, on='SampleID', how='left')

    # Set all empty values (NaN) to zero
    result = result.fillna(0)

    # Adding the 'Item_Group' column
    item_group_df = df[['SampleID', 'Item_Group']].drop_duplicates(subset=['SampleID'])
    item_group_df['SampleID'] = item_group_df['SampleID'].astype(int)
    result = pd.merge(result, item_group_df, on='SampleID', how='left')
    result['Item_Group'] = result['Item_Group'].fillna('Null')
    
    # Adding the SampleName column
    sample_name_df = df[['SampleID', 'SampleName']].drop_duplicates(subset='SampleID')
    sample_name_df['SampleID'] = sample_name_df['SampleID'].astype(int)
    result = pd.merge(result, sample_name_df, on='SampleID', how='left')
    result['SampleName'] = result['SampleName'].fillna('Unbekannt')


    # Save the adjusted result as CSV
    try:
        result.to_csv(output_file, index=False)
    except IOError as e:
        print(f"Error saving the file '{output_file}': {e}")
    except Exception as e:
        print(f"Unexpected error while saving the file '{output_file}': {e}")
