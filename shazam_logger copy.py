"""
Module: shazam_logger

This module provides functionality to continuously monitor
the output of a Shazam shortcut command and log the results into a DB file
of the user's choice, or default CSV.
Author: Sophie Greene
Date: 2024/05/09

Dependencies:
    - os
    - re
    - subprocess
    - time
    - pandas

Functions:
    - get_row(outfile): This function runs the Shazam shortcut
        to identify the current song playing
        and returns a dictionary containing various information
        about the song, such as title, artist, lyrics, etc.
        Parameters:
            - outfile (str): Specify the output file name for the Shazam
                shortcut result.
        Returns:
            A dictionary containing the following keys:
                - Title
                - Artist
                - Lyrics Snippets
                - Lyric Snippet Synced
                - Artwork
                - Video URL
                - Shazem URL
                - Apple Music URL
    - main(): This function is the entry point of the program.
        It retrieves information about the current song using get_row(),
        continuously monitors changes in the song,
        and writes the data to a DB file.
        Notes:
            The DB file name and the output file name
            for the Shazam result can be specified as command-line arguments.
            If not provided, default names will be used.
        Returns:
           a DB with all logged shazams
"""

import os  # The os module is a built-in Python module
import subprocess  # The subprocess module is a built-in Python module
import sys  # The sys module is a built-in Python module
import time  # The time module is a built-in Python module

# ###########################################################
import pandas as pd  # The pandas module should be installed.
from bs4 import BeautifulSoup
# Please ensure both are installed in your environment.

SHAZAM_TEMPLATE = """
<output>

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

</output>
"""
SUBSET = ["artist", "title", "name"]
write_ext = {
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
read_ext = {
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

    ndf = pd.DataFrame(lst_of_dct)
    if os.path.exists(db_file):
        df = read_db(db_file, encoding="utf-8")

        df = pd.concat([df, ndf]).reset_index(
            drop=True).drop_duplicates(subset=SUBSET)
        store_db(df, db_file)
    else:
        store_db(ndf, db_file)

def match(sentence, chars):
    """
    The match function takes two arguments:
        1. sentence - a string of characters
        2. chars - a list of characters
    :param sentence: Check if the sentence contains
     all of the characters in chars
    :param chars: Check if all the characters in it are present in the sentence
    :return: A boolean value
    """
    return all(map(lambda c: c in sentence, chars))


def parse_row(outfile):
    """
    The parse_row function takes a file name as input and returns a dictionary.
    The function opens the file, reads it into memory,
    and parses the HTML string into an object that can be traversed using
    BeautifulSoup. The function then iterates through each child of
    the top-level element in this object(<output>) in our case
    and adds its name (e.g., 'title') as a key to the dictionary with its
    text content (e.g., 'title': 'Imagine', 'artist': 'John Lennon') as value.
    :param outfile: Specify the file that is to be parsed
    :return: A dictionary with the following keys:
        timestamp
        title
        artist
        isexplicit
        lyricssnippet
        lyricsnippetsynced
        artwork
        videourl
        shazamurl
        applemusicurl
        name
    """
    if not os.path.exists(outfile):
        return {}
    with open(outfile, encoding='utf-8') as f:
        row = f.read().replace('\n', '')
    # Parse the HTML string
    soup = BeautifulSoup(row, 'html.parser')
    top = next(soup.children)
    if top != 'output':
        return 
    dct = {}
    if top != 'output':
        return dct
    for c in top.children:
        dct[c.name] = c.text
    return dct


def get_row(outfile):
    """
    The get_row function takes an output file and a time as arguments.
    It then runs the shazam_step shortcut,
    which is a step in the Shazam workflow.
    The function waits for t seconds before returning True if the process
    has finished, or False otherwise.
    :param outfile: Specify the output file name
    :param t: Set the time that the program will wait before returning
    :return: A boolean value, true if the process is finished
        and false otherwise
    """
    script = ["shortcuts",
              "run",
              "shazam_step",
              "--output-path",
              outfile]
    return subprocess.run(script, None, None, check=False)

def store_db(df, db_fn, encoding='utf-8'):
    """
    The store_data function takes a dataframe, db_fn (database filename),
        and encoding as arguments.
    It splits the database filename into name and extension components.
    It then looks up the method associated with 
    the file extension in read_ext dictionary.
        - If there is a method associated with that file extension, it returns 
            the result of calling that method on the dataframe using getattr(). 
        - Otherwise, it prints an error message to stdout and stores 
        the data in a csv file.
    :param df: Store the dataframe
    :param db_fn: Store the name of the file that is being read
    :param encoding: Specify the encoding of the file
    :return: The dataframe in a csv format
    """
    name, ext = os.path.splitext(db_fn)
    name = name.split('/')[-1]
    method = read_ext[ext]
    if method:
        read_method = getattr(df, method)
        return read_method(db_fn, encoding=encoding)
    else:
        print("Unsupported file extension.")
        print('storing data in {name}.csv')
        return df.to_csv(db_fn, encoding=encoding)





def wait_for_file(outfile):
 
    """
    The wait_for_file function waits for a file to be created.
    
    :param outfile: Specify the file that is being waited for
    :return: True if the file exists and false otherwise
    """
    cnt = 0
    while not os.path.exists(outfile):
        if cnt > 1e9:
            return False
        cnt += 1
    return True





def get_data(outfile):
    """
    The get_data function is a function that gets the data from the
        get_row function and parses it into a dictionary.
    :param outfile: Specify the name of the file that will be written to
    :return: A list of dictionaries
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
            get_row(outfile, 0)
            if wait_for_file(outfile):
                c_res = parse_row(outfile)
                if c_res and 'title' in c_res:
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


def main():

    """
    The main function is the entry point for this program.
    It calls other functions to do the following:
        1) Assign file names for input and output files.
        2) Get data from a web page, write it to an output file,
            and return it as a list of lists.
        3) Append the data in memory to an existing database file on disk. 
    :return: Nothing
    """
    db_file, outfile = assign_file_names()

    data = get_data(outfile)
    try:
        append_db(data, db_file)
    except KeyboardInterrupt:
        print('KeyboardInterrupt')


if __name__ == "__main__":
    main()
