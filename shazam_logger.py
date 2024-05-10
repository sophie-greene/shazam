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
    - get_row(outfile): Runs the `shazam_step` Apple Shortcut and
        returns a subprocess.CompletedProcess object.
    - match(sentence, chars): Checks if all characters in `chars`
        are present in `sentence`.
    - parse_row(outfile): Parses the XML document generated by Shazam
        and returns a dictionary of media information.
    - read_db(db_file, encoding='utf-8'): Reads a database file 
        and returns a pandas DataFrame.
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
import subprocess  # The subprocess module is a built-in Python module
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

SUBSET = ["artist", "title", "name"]
SHAZAM_TEMPLATE = """
<root>

<timestamp>
Date
</timestamp>

<title>
Shazam Media (Title)
</title>

<artist>
Shazam Media (Artist)
</artist>

<isexplicit>
Shazam Media (Is Explicit)
</isexplicit>

<lyricssnippet>
Shazam Media (Lyrics Snippet)
</lyricssnippet>

<lyricsnippetsynced>
Shazam Media (Lyric Snippet Synced)
</lyricsnippetsynced>

<artwork>
Shazam Media (Artwork)
</artwork>

<videourl>
Shazam Media (Video URL)
</videourl>

<shazamurl>
Shazam Media (Shazam URL)
</shazamurl>

<applemusicurl>
Shazam Media (Apple Music URL)
</applemusicurl>

<name>
Shazam Media (Name)
</name>

</root>
"""

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


def append_db(lst_of_dct, db_file):
    """
    The append_db function appends a list of dictionaries to
        an existing database file.
    ------------------------------------------------------------
    :param lst_of_dct: Pass in a list of dictionaries to the function
    :param db_file: Specify the file to be written to
    :return: 0
    """
    ndf = pd.DataFrame(lst_of_dct)
    if os.path.exists(db_file):
        df = read_db(db_file, encoding="utf-8")

        df = pd.concat([df, ndf]).reset_index(
            drop=True).drop_duplicates(subset=SUBSET)
        write_db(df, db_file)
    else:
        write_db(ndf, db_file)
    return 0


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
    the xml data retrieved by `get_row(outfile)`
    :return: A list of dictionaries
    TODO: make sure data is stored when KeyboardInterrupt is raised
            using some sort of threading/queuing
    """
    p = ''
    c_res = {}
    data = []
    cnt = 0
    try:
        while True:
            if cnt > 1e9:
                break
            cnt += 1
            if len(c_res) > 0 and p == f"{c_res['artist']}{c_res['title']}":
                continue
            get_row(outfile)
            if wait_for_file(outfile):
                c_res = parse_row(outfile)
                if len(c_res) > 0 and 'title' in c_res:
                    cnt = 0
                    print('p=', p)
                    print(c_res['timestamp'], end=' ')
                    print(f': Playing: {c_res['title']}', end=' ')
                    print(f"by {c_res['artist']}")
                    data.append(c_res)
                p = f"{c_res['artist']}{c_res['title']}"
                # print(c_res['name'], p)
            else:
                time.sleep(10)
                continue
            time.sleep(10)
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
    return data


def get_row(outfile):

    """
    The get_row function runs the shazam_step shortcut
        and returns a subprocess.CompletedProcess object.
        the returned value could be None or something else
        please refer to documentation
        [subprocess](https://docs.python.org/3/library/subprocess.html)
    ------------------------------------------------
    :param outfile: Specify the path for the output file
    :return: A completedprocess object
    """
    script = ["shortcuts",
              "run",
              "shazam_step",
              "--output-path",
              outfile]
    return subprocess.run(script, None, None, check=False)

def parse_row(outfile, encoding='utf-8'):
    """
    The parse_row function parses the XML document using lxml parser.
    it uses the `SHAZAM_TEMPLATE` string as map to read the xml data
    ---------------------------------------------------------
    :param outfile: Specify the path to the xml file that will be parsed
    :return: A dictionary with keys as the tag names
        and values as the text content of those tags
    """
    soup = BeautifulSoup(SHAZAM_TEMPLATE, 'xml')
    root = soup.root
    tags = [tag  for tag in root.children if tag and tag!='root']
    print()
    try:
        with open(outfile, encoding=encoding) as f:
            row = f.read()
    except FileNotFoundError:
        return FileNotFoundError
    # print(row)
    soup = BeautifulSoup(row.replace('\n', ''), 'xml')
    root = soup.select_one('root')
    if root:
        dct = {}
        for tag in tags:
            if not tag:
                continue
            tag_content = root.find(tag)
            if tag_content:
                dct[tag] = tag_content.text
    return dct


def read_db(db_file, encoding='utf-8'):
    """
    The read_db function reads a database file and returns a pandas dataframe.
    -------------------------------------------
    :param db_file: Specify the file to be read
    :param encoding: Specify the encoding of the file
    :return: A pandas dataframe with the contents of the file
    """
    print(db_file)
    name, ext = os.path.splitext(db_file)
    name = name.split('/')[-1]
    method = READ_EXT.get(ext)
    if method:
        read_method = getattr(pd, method)
        df = read_method(db_file, encoding=encoding)
        return df


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


def wait_for_file(outfile, limit=1e12):

    """
    The wait_for_file function waits for a file to be created.
    --------------------------------------------------
    :param outfile: Specify the file that is being waited for
    :param limit: Set a limit on the number of times the while loop will run
    :return: True if the file exists, and false if `limit` is reached
    """
    cnt = 0
    while not os.path.exists(outfile):
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

    data = get_data(outfile)
    try:
        append_db(data, db_file)
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        return 1
    return 0


if __name__ == "__main__":
    main()
