# GeoRoc 2.0 CLI

## Command line interface to retrieve, filter and save GeoRoc data

Welcome to the GEOROC CLI Tool. This tool allows you to access the GEOROC database and extract specific data for your geoscience research.

This program is designed to extract primarily geochemical numerical data through the API, but is flexible enough to be tailored to other needs. 
It is capable of filtering data based on a number of parameters and exporting them to an easy-to-use CSV file. The current version is designed 
for flat JSON structures, which means that nested structures are not passed to the CSV file in a structured way.


[![License](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)
![GitHub Repo stars](https://img.shields.io/github/stars/tmwProjects/GeoRoc_CLI?style=social) 
![GitHub followers](https://img.shields.io/github/followers/tmwProjects?style=social)
<a href="https://datasci.social/@tmwProjects">
  <img src="https://img.shields.io/mastodon/follow/110580864516294518?domain=https://datasci.social&style=social" alt="Mastodon follow">
</a>
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/tmwProjects/GeoRoc_CLI) 
[![Visit my site](https://img.shields.io/badge/Visit%20my%20site-Online-important)](https://tmwprojects.github.io/)
[![Donate on Liberapay](https://img.shields.io/badge/Donate-Liberapay-yellow)](https://liberapay.com/tmwProjects/donate)
<a href="https://www.buymeacoffee.com/tmwcontactQ"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" height="20.4px"></a>

***
## Content

* [Usage](#usage)
* [Current features](#current-features)
* [Future features](#future-features)
* [Current Tasks](#current-tasks)
* [References](#references)
* [Acknowledgement](#acknowledgement)
* [License](#license)

***

```bash
$ python3 georoc_cli.py --help     

                  ___
                 ( __)
                ( __)_)
              ( __)__)__)
               ( _) ___)___)
              ( _) __)
            (_)
             /^
          ^ // \
         / \/   \
        / _    _ \
       /    _     \
      / _  GEOROC 2.0 CLI
     /     v.0.0.1  \
    /                \
    
usage: python3 georoc_cli.py --sample-option "OPTION" --key "key1" --key "key2"

   ╔╦╗╦ ╦╔═╗  ╔═╗╔═╗╔═╗╦═╗╔═╗╔═╗  ╔╦╗╔═╗╔╦╗╔═╗╔╗ ╔═╗╔═╗╔═╗
    ║ ╠═╣║╣   ║ ╦║╣ ║ ║╠╦╝║ ║║     ║║╠═╣ ║ ╠═╣╠╩╗╠═╣╚═╗║╣
    ╩ ╩ ╩╚═╝  ╚═╝╚═╝╚═╝╩╚═╚═╝╚═╝  ═╩╝╩ ╩ ╩ ╩ ╩╚═╝╩ ╩╚═╝╚═╝
   (Geochemistry of Rocks of the Oceans and Continents)

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════

    Here are a few additional notes:

    - For an appropriate more advanced use of this CLI programme, pleas use the -m flag
      for the manual in this programme. (I expand an appropriate Manuel regularly.)

    - To use the CLI program an API key is necessary which must be stored in the script config.py
      in the variable "api_key". To get the API key, please contact the DIGIS GEOROC team.

    - The Limit parameter refers to the number of SampleIDs.

    - It is necessary to use 2 - 3 sample options.

    - After executing a command, a file named "georoc_data_{Y-m-d_H-M-S}.csv" is created in the
      local folder "Georoc_Datasets" (default) with the data you want to include. If you wish, you can
      also specify a desired path. In addition, a duplicate of the dataset is created, which has been
      structured, pivoted and the NaN values replaced with zeros.

    - All parameters for the sample flags must be written in capital letters.

    - All parameters for the JSON keys must be written as they were stored in the directory.
      Here is the possibility to simply copy and paste them as desired.

    Here is an example command:

    python3 georoc_cli.py \\
    --limit "3" \\
    --location1 "EAST AFRICAN RIFT" \\
    --location2 "ETHIOPIAN RIFT" \\
    --setting "RIFT VOLCANICS" \\
    --key Item_Name \\
    --key Values \\
    --key Units \\
    --key Longitude \\
    --key Latitude

    Information about the current version:

    - The first version is designed to extract primarily geochemical numerical data through the API.
      In the command example above, you can see from the --key flags that this works well.

    - If you only want the data for a specific publication, you can use the --doi filter parameter, which works well.

    - The program is currently designed for flat JSON structures, which means that nested structures
      such as for the "References" or "Loc_Data" flag will not be passed to the csv file in a structured way.

    - The GEOROC database and the associated API interface are developed on a regular basis. If the program
      does not work as usual, visit the API documentation.

    - The program and the server need about 7 seconds to retrieve the data per sample ID. If you want
      to retrieve a lot of data, feel free to get a c[_].

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════

options:
  -h, --help            show this help message and exit
  -m, --manual          Manpage for database and program
  --output-path OUTPUT_PATH
                        Output path for the generated CSV file (default: current directory)

Filtered Samples Options (e.g. --location1 "EAST AFRICAN RIFT".):
  

  --doi DOI
  --element ELEMENT
  --elementtype ELEMENTTYPE
  --firstname FIRSTNAME
  --inclusiontype INCLUSIONTYPE
  --lastname LASTNAME
  --limit LIMIT
  --location1 LOCATION1
  --location2 LOCATION2
  --location3 LOCATION3
  --material MATERIAL
  --mineral MINERAL
  --offset OFFSET
  --publicationyear PUBLICATIONYEAR
  --rockclass ROCKCLASS
  --rocktype ROCKTYPE
  --sampletech SAMPLETECH
  --setting SETTING
  --title TITLE
  --value VALUE

For Keys Options use the flag --key (e.g. --key Latitude"):
  

  --key KEY             List of keys: 
                        
                        Sample_Num unique_id Batches References SampleName Location_Names Location_Types
                        Loc_Data Elevation_Min Elevation_Max Land_Or_Sea Rock_Types Rock_Classes Rock_Textures
                        Age_Min Age_Max Materials Minerals Inclusion_Types Location_Num Latitude Longitude
                        Latitude_Min Latitude_Max Longitude_Min Longitude_Max Tectonic_Setting Method
                        Comment Institution Item_Name Item_Group Standard_Names Standard_Values Values Units

═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════ 
```


### Usage

```Bash
$ python3 georoc_cli.py \
--limit "3" \
--location1 "EAST AFRICAN RIFT" \
--location2 "ETHIOPIAN RIFT" \
--setting "RIFT VOLCANICS" \
--key Item_Name \
--key Values \
--key Units \
--key Longitude \
--key Latitude \
--key Item_Group

                  ___
                 ( __)
                ( __)_)
              ( __)__)__)
               ( _) ___)___)
              ( _) __)
            (_)
             /^
          ^ // \
         / \/   \
        / _    _ \
       /    _     \
      / _  GEOROC 2.0 CLI
     /     v.1.0.0  \
    /                \
    
API query successful for endpoint:ping
+---------------------------------------------------------------------+
Connection to API server successful!
+---------------------------------------------------------------------+
API query successful for endpoint:queries/samples
+---------------------------------------------------------------------+
The extracted SampleIDs are: [53972, 53973, 53974]
+---------------------------------------------------------------------+
Processing: 100%|███████████████████████████████████████████████████████████████████████████████| 3/3 [00:18<00:00,  6.16s/sample]
+---------------------------------------------------------------------+
Your downloaded data can be found in the file '/your/local/path/Georoc_Datasets/georoc_dataset_2023-05-11_12-06-51.csv'
Your structured data can be found in the file '/your/local/path/Georoc_Datasets/structured_georoc_dataset_2023-05-11_12-06-51.csv'
+---------------------------------------------------------------------+

"Why are geologists never hungry? Because they lost their apatite."

```

### Current features

- Obtain desired data using filters from the API interface, if an API key has been provided by GEOROC.

### Future features

- Save data from the JSON that has deeper structures in a structured way to a CSV file.
- The possibility to store the API key not directly in the script, but separately in the directory and/or to specify the API key via CLI flag.
- The possibility of interrupting the retrieval of data by means of a shortcut.
- What other features would be helpful? Write me an issue.

### Current Tasks

- Easy to understand documentation on how to obtain certain data so that in-depth knowledge of API documentation will not be necessary.
- Documentation about installing the CLI program with requirements.txt, setup,py and related documentation.
- The possibility to store the API key not directly in the script, but separately in the directory and/or to specify the API key via CLI flag.

***

### References

**argparse**
Python Software Foundation. (n.d.). "argparse — Parser for command-line options, arguments and sub-commands." Python v3.9.2 documentation. Retrieved June 2023, from https://docs.python.org/3/library/argparse.html.

**contextlib**
Python Software Foundation. (n.d.). "contextlib — Utilities for with-statement contexts." Python v3.9.2 documentation. Retrieved June 2023, from https://docs.python.org/3/library/contextlib.html.

**datetime**
Python Software Foundation. (n.d.). "datetime — Basic date and time types." Python v3.9.2 documentation. Retrieved June 2023, from https://docs.python.org/3/library/datetime.html.

**io**
Python Software Foundation. (n.d.). "io — Core tools for working with streams." Python v3.9.2 documentation. Retrieved June 2023, from https://docs.python.org/3/library/io.html.

**json**
Python Software Foundation. (n.d.). "json — JSON encoder and decoder." Python v3.9.2 documentation. Retrieved June 2023, from https://docs.python.org/3/library/json.html.

**os**
Python Software Foundation. (n.d.). "os — Miscellaneous operating system interfaces." Python v3.9.2 documentation. Retrieved June 2023, from https://docs.python.org/3/library/os.html.

**pandas**
McKinney, W. (2010). "Data Structures for Statistical Computing in Python." Proceedings of the 9th Python in Science Conference. pp. 51-56.

**random**
Python Software Foundation. (n.d.). "random — Generate pseudo-random numbers." Python v3.9.2 documentation. Retrieved June 2023, from https://docs.python.org/3/library/random.html.

**requests**
Reitz, K. (n.d.). "Requests: HTTP for Humans." Python Library. Retrieved June 2023, from https://requests.readthedocs.io/en/master/.

**sys**
Python Software Foundation. (n.d.). "sys — System-specific parameters and functions." Python v3.9.2 documentation. Retrieved June 2023, from https://docs.python.org/3/library/sys.html.

**textwrap**
Python Software Foundation. (n.d.). "textwrap — Text wrapping and filling." Python v3.9.2 documentation. Retrieved June 2023, from https://docs.python.org/3/library/textwrap.html.

**tqdm**
da Costa-Luis, C. (n.d.). "tqdm: A Fast, Extensible Progress Bar for Python and CLI." Python Library. Retrieved June 2023, from https://tqdm.github.io/.

***

### Acknowledgement

Hey there! It's really great that you appreciate my work on GitHub! Everything you see here is a product of my voluntary efforts, and I'm all about sharing useful content. If you find value in what I do and would like to support me, you might consider buying me a coffee. Thank you so much for your generosity and support!

###### Hint: If you would like to buy me a "Coffee", please give a name/pseudonym and the project, I would like to have the possibility to thank you by name. - Thanks :)

***

### License

**MIT License**

The MIT licence is a very permissive licence created by the Massachusetts Institute of Technology. It basically allows 
you to do almost anything you want with the licensed code - you can modify it, incorporate it into your own software 
and sell your software if you want. The only condition is that you always retain the MIT licence in your copies of the 
original or modified code. In other words, you must always recognise that the original code is under the MIT licence.
