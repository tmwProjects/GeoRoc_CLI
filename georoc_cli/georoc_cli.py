import argparse
import io
import os
import sys
import textwrap
from contextlib import redirect_stdout
import pandas as pd
from tqdm.auto import tqdm
from api import get_measurement_data, get_filtered_samples
from config import api_key, get_filtered_samples_keys
from utils import check_api_connection, generate_csv_filename, \
    read_description_file, display_manual, structure_data, print_random, \
    check_filter_flags, check_api_key


def main(args):
    try:
        # Check if at least one filter flag is set
        check_filter_flags(args)

        # Check if an API key is set
        check_api_key(api_key)

        # Check the connection to the API server
        check_api_connection()

        # Get filtered samples
        filtered_samples_combined = get_filtered_samples(
            **{key: getattr(args, key) for key in get_filtered_samples_keys if getattr(args, key) is not None},
            **{key: True for key in args.key}
        )

        if filtered_samples_combined is None:
            raise Exception("No response received from the API.")

        # Extract SamplingFeatureIDs
        if "Data" in filtered_samples_combined and filtered_samples_combined["Data"]:
            sampling_feature_ids = [sample["SampleID"] for sample in filtered_samples_combined["Data"]]
            print(f"The extracted SampleIDs are:", sampling_feature_ids)
            print("+---------------------------------------------------------------------+")
        else:
            print("No data found or unexpected data structure")
            print("+---------------------------------------------------------------------+")

        # Create an empty DataFrame to store all measurement data
        measurement_data = pd.DataFrame()

        # Initialize the progress bar
        progress_bar = tqdm(
            total=len(sampling_feature_ids),
            desc="Processing",
            unit="sample",
            dynamic_ncols=True,
            leave=True,
            colour="#00507d",
            #ncols=150
        )

        # Redirect the standard output to suppress intermediate prints
        with io.StringIO() as buf, redirect_stdout(buf):

            # Iterate over the list of SamplingFeatureIDs
            for sampling_feature_id in sampling_feature_ids:
                print(f"Fetching measurement data for SamplingFeatureID: {sampling_feature_id}")

                # Get the measurement data for the current SamplingFeatureID
                df = get_measurement_data(api_key, sampling_feature_id, args.key)

                # Check if the dataframe is not empty and not None
                if df is not None and not df.empty:
                    # Append the dataframe to the measurement_data DataFrame
                    measurement_data = pd.concat([measurement_data, df], ignore_index=True)

                elif df is None:
                    print(f"Error occurred while fetching data for SamplingFeatureID {sampling_feature_id}")
                    print("+---------------------------------------------------------------------+")
                else:
                    print(f"No measurement data found for SamplingFeatureID {sampling_feature_id}")
                    print("+---------------------------------------------------------------------+")

                # Update the progress bar for each completed step
                progress_bar.update(1)

            # Create the Georoc_Datasets folder if it does not exist
            output_folder = os.path.join(args.output_path, "Georoc_Datasets")
            os.makedirs(output_folder, exist_ok=True)

            # Save the combined measurement_data DataFrame
            csv_filename = generate_csv_filename()
            output_path = os.path.join(output_folder, csv_filename)
            measurement_data.to_csv(output_path, index=False)

            # Define the input and output file paths for the structure_data function
            input_file = output_path
            structured_csv_filename = f"structured_{csv_filename}"
            output_file = os.path.join(output_folder, structured_csv_filename)

            # Call the structure_data function
            structure_data(input_file, output_file)

        # Close the progress bar after the loop
        progress_bar.close()

        # Get the absolute path of the generated files
        abs_path_downloaded = os.path.abspath(output_path)
        abs_path_structured = os.path.abspath(output_file)

        print("+---------------------------------------------------------------------+")
        print(f"Your downloaded data can be found in the file '{abs_path_downloaded}'")
        print(f"Your structured data can be found in the file '{abs_path_structured}'")
        print("+---------------------------------------------------------------------+", "\n")
        print_random("random.txt")

    except Exception as e:
        print("An error occurred during the execution:")
        print("+---------------------------------------------------------------------+")
        print(str(e))
        print("+---------------------------------------------------------------------+")
        exit(1)


if __name__ == "__main__":

    title = """
                  ___
                 ( __)
                ( __)_)
              ( __)__)__)
               ( _) ___)___)
              ( _) __)
            (_)
             \033[31m/\033[0m^
          ^ \033[31m//\033[0m \\
         / \033[31m\/\033[0m   \\
        / _    _ \\
       /    _     \\
      / _  GEOROC 2.0 CLI
     /     v.0.0.1  \\
    /                \\
    """
    print(title)

    parser = argparse.ArgumentParser(
        usage="python3 %(prog)s --sample-option \"OPTION\" --key \"key1\" --key \"key2\"",
        prog="georoc_cli.py",
        epilog="═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════ \nWritten by Timm M. Wirtz",
        formatter_class=argparse.RawTextHelpFormatter,
        description=textwrap.dedent(read_description_file("parser_description.txt"))
    )

    # Add command line argument groups
    get_filtered_samples_group = parser.add_argument_group(
        "Filtered Samples Options (e.g. --location1 \"EAST AFRICAN RIFT\".)", "\n")
    json_keys_group = parser.add_argument_group(
        "For Keys Options use the flag --key (e.g. --key Latitude\")", "\n")

    # Add command line arguments for filtered_samples_keys
    for key in sorted(get_filtered_samples_keys):
        get_filtered_samples_group.add_argument(
            f"--{key}"
        )

    # Add the --json-key argument
    json_keys_group.add_argument(
        "--key",
        action="append",
        default=[],
        help=textwrap.dedent("""\
            List of keys: \n
            Sample_Num unique_id Batches References SampleName Location_Names Location_Types
            Loc_Data Elevation_Min Elevation_Max Land_Or_Sea Rock_Types Rock_Classes Rock_Textures
            Age_Min Age_Max Materials Minerals Inclusion_Types Location_Num Latitude Longitude
            Latitude_Min Latitude_Max Longitude_Min Longitude_Max Tectonic_Setting Method
            Comment Institution Item_Name Item_Group Standard_Names Standard_Values Values Units""")
    )

    parser.add_argument('-m', '--manual', action='store_true', help='Manpage for database and program')

    parser.add_argument(
        "--output-path",
        default=".",
        help="Output path for the generated CSV file (default: current directory)",
    )

    args = parser.parse_args()

    if args.manual:
        display_manual()
        sys.exit(0)

    main(args)
