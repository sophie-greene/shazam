"""
SCRIPT: shazam_logger

This script interacts with the Shazam app to retrieve information
    about currently playing media and stores it in a database file.
It relies on an Apple Shortcut named `shazam_step` to get the information.
The retrieved data is stored in an XML format and then parsed
    using BeautifulSoup.
The parsed data is appended to an existing database file or a new one,
    depending on user input.

Author: Sophie Greene
Date: 2024/05/09

Dependencies:
    - pandas
    - BeautifulSoup from bs4
    - lxml
    - subprocess
    - sys
    - os
    - time

Global Constants:
    - SUBSET: A list of column names used to identify duplicates when appending to the database.
    - SHAZAM_TEMPLATE: XML template used to parse Shazam data.

Global Variables:
    - WRITE_EXT: Dictionary mapping file extensions to methods
        for writing DataFrame to file.
    - READ_EXT: Dictionary mapping file extensions to methods
        for reading DataFrame from file.

Functions:
    - append_db(lst_of_dct, db_file): Appends a list of dictionaries 
        to an existing database file.
    - assign_file_names(): Assigns file names for input and output files based
        on command-line arguments.
    - get_data(outfile): Retrieves data from the Shazam app and stores it
        in a list of dictionaries.
    - shazam_step.fetch_row(outfile): Runs the `shazam_step` Apple Shortcut and
        returns a subprocess.CompletedProcess object.
    - write_db(df, db_file, encoding='utf-8'): Writes a DataFrame
        to a database file.
    - wait_for_file(outfile, limit=1e12): Waits for a file to be created.

Main Function:
    - main(): Entry point of the script. Assigns file names,
        retrieves data, and appends it to the database.

Usage:
    - python <script_name>.py [db_file] [outfile]
        - db_file: Path to the existing database file.
        - outfile: Path to the output file where Shazam data will be stored.
"""


import os  # The os module is a built-in Python module
import sys  # The sys module is a built-in Python module
import time  # The time module is a built-in Python module

# ###########################################################
# Please ensure both are installed in your environment
# lxml is needed to parse xml, use the following to install all
# pip install pandas, bs4, lxml
# or in an ipython environment:
# !pip install pandas, bs4, lxml
from bs4 import BeautifulSoup
import pandas as pd
# ###########################################################

# ###########################################################
# Custome module find in file ./shazam.py
import shazam_step
from parse_row import parse_row
# ###########################################################

SUBSET = ["artist", "title", "name"]



WRITE_EXT = {
    '.csv': 'to_csv',
    '.xls': 'to_excel',
    '.xlsx': 'to_excel',
    '.json': 'to_json',
    '.html': 'to_html',
    '.sql': 'to_sql',
    '.parquet': 'to_parquet',
    '.feather': 'to_feather',
    '.h5': 'to_hdf',
    '.hdf': 'to_hdf',
    '.dta': 'to_stata',
    '.sas7bdat': 'to_sas',
    }

READ_EXT = {
    '.csv': 'read_csv',
    '.xls': 'read_excel',
    '.xlsx': 'read_excel',
    '.json': 'read_json',
    '.html': 'read_html',
    '.sql': 'read_sql',
    '.parquet': 'read_parquet',
    '.feather': 'read_feather',
    '.h5': 'read_hdf',
    '.hdf': 'read_hdf',
    '.dta': 'read_stata',
    '.sas7bdat': 'read_sas',
}




def assign_file_names():
    """
    The assign_file_names function takes in the command line arguments
    and assigns them to variables.
    If no command line arguments are given,
    it will assign default values to the variables.
    -------------------------------------------------
    :return: A tuple of strings
    """
    if len(sys.argv) == 2:
        db_file = sys.argv[1].strip()
        outfile = None  # Assign a default value
    elif len(sys.argv) == 3:
        db_file = sys.argv[1].strip()
        outfile = sys.argv[2].strip()
    else:
        db_file = "shazam.csv"
        outfile = "./outfile"
    print("Based on your input...")
    print("db_file: ", db_file)
    print("outfile: ", outfile)
    print(f"python {sys.argv[0]}.py [db_file] [outfile]:")
    return db_file, outfile


def get_data(outfile):
    """
    The get_data function shazam's the current song on the system and store
        it in a dictionary it then waits for the song
        to change in order to repeat the process, meanwhile storing
        all the dictionaries into a list
    -----------------------------------------------------------------
    :param outfile: Pass the name of the file that will be used to store
    the xml data retrieved by `step_shazam.fetch_row(outfile)`
    :return: A list of dictionaries
    TODO: make sure data is stored when KeyboardInterrupt is raised
            using some sort of threading/queuing
    """
    p = ''
    artist = ''
    title = ''
    c_res = {}
    data = []
    shazams = 0
    cnt = 0

    while True:
        cnt += 1
        # check if the song has already been shazamed
        if len(c_res) > 0 and p == f"{c_res['artist']}{c_res['title']}":
            time.sleep(20)
            continue
        # check tha the data was not fetched
        status = shazam_step.fetch_row(outfile)
        if not status:
            time.sleep(5)
            continue
        if os.path.exists(outfile):
            c_res = parse_row(outfile)
            if len(c_res) > 0 and 'title' in c_res:
                shazams += 1
                cnt = 0
                title = c_res.get('title', '')
                artist = c_res.get('artist', '')
                print('p=', p)
                print(c_res['timestamp'], end=' ')
                print(f': Playing: {title}', end=' ')
                print(f"by {artist}")
                data.append(c_res)
                p = f"{artist}{title}"
                # print(c_res['name'], p)
            else:
                continue
    return data


def write_db(df, db_file, encoding='utf-8'):
    """
    The store_db function takes a dataframe and a file name as input.
    It then checks if the extension of the file is in write_ext,
    which is a dictionary of valid extensions for storing dataframes.
    If it is, it calls the appropriate method on df to store itself.
    otherwise it stores `df` in csv file
    ---------------------------------------------
    :param df: Pass in the dataframe to be stored
    :param db_file: Store the file name and extension of the database
    :return: 0 for success, 1 otherwise
    """
    if not isinstance(df, pd.DataFrame):
        return 1
    name, ext = os.path.splitext(db_file)
    method = WRITE_EXT.get(ext)
    if method:
        write_method = getattr(df, method)
        write_method(db_file, encoding=encoding)
    else:
        print('Unsupported file extension.')
        print('Writing file in default format CSV')
        df.to_csv(db_file, encoding='utf-8')
        print(f'Done writing file {name}.csv')
    return 0


def wait_for_file(outfile, limit=1e12, lag=1):
    """
    The wait_for_file function waits for a file to be created.
    --------------------------------------------------
    :param outfile: Specify the file that is being waited for
    :param limit: Set a limit on the number of times the while loop will run
    :param lag: time delay in seconds,
        after every file check it sleep for `lag` seconds
    :return: True if the file exists, and false if `limit` is reached
    """
    cnt = 0
    while not os.path.exists(outfile):
        time.sleep(lag)
        if cnt > limit:
            return False
        cnt += 1
    return True


def main():
    """
    The main function is the entry point for this program.
    It calls other functions to do its work, and returns an integer value
    to indicate success or failure of the program.
    Tasks:
        1. Assign file names for input and output files.
        2. Get data from a running an Apple Shortcut ,
            write it to an output file, and return it
            as a list of dictionaries.
        3. Append the data in memory (a list of dictionaries) to
            an existing database file or new file.
    -------------------------------------------------
    :return: 0 if it runs without errors 1 otherwise
    """
    db_file, outfile = assign_file_names()
    try:
        data = get_data(outfile)
    except KeyboardInterrupt:
        print('Interrupted while getting data')
    try:
        append_db(data, db_file)
    except KeyboardInterrupt:
        print('Interrupted while storing data')
        return 1
    return 0


if __name__ == "__main__":
    main()
