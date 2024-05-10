"""
The 'read_data' module provides functions for file handling and data reading using Pandas.

Functions:
- detect_file_type(fn): Determines the file type of a given file using the 'file' command.
- read_frmt(db_file, args={'encoding':'utf-8'}): Reads a file into a Pandas DataFrame based on its format.
- read(db_file, frmt, args={'encoding':'utf-8'}): Reads a file into a Pandas DataFrame using a specific format.

Constants:
- WRITE_FRMT: A dictionary mapping file extensions to Pandas methods for writing data to file formats.
- READ_FRMT: A dictionary mapping file extensions to Pandas methods for reading data from file formats.

Usage Example:
    import read_data

    # Determine file type
    file_type = read_data.detect_file_type('example.csv')
    print(file_type)  # Output: 'text/csv'

    # Read file into DataFrame
    df = read_data.read_frmt('example.csv')
    print(df.head())  # Output: Displays the first few rows of the DataFrame

    # Further file handling and reading options are available using the provided functions.

Note:
- The 'detect_file_type' function relies on the 'file' command available
    in Unix-like systems.
- The 'read_frmt' function determines the file format based on both the
    file extension and the detected MIME type.
- This module requires the 'pandas' library to be installed.
```sh
pip install panadas
```
For more details about the 'file' command, refer to: 
https://man7.org/linux/man-pages/man1/file.1.html
"""

import os
import subprocess
import re
import pandas as pd

WRITE_FRMT = {
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

READ_FRMT = {
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


def detect_file_type(fn):

    """
    The detect_file_type function takes a file path as input and returns the
    file type. The function uses the [file](https://man7.org/linux/man-pages/man1/file.1.html) command to determine the file type.
    The output of this command is parsed to extract only the file type.
    
    :param fn: Pass the name and path of a file to the function
    :return: The file type if file exists, '' otherwise
   
    """
    if not os.path.exists(fn):
        return ''
    result = subprocess.run(
        ['file',
         '--mime-type',
         fn],
         capture_output=True, text=True, check=False)
    # Extract the file type from the output
    file_type = result.stdout.strip().split(': ')[-1]

    return file_type


def read_db(db_file, **kwargs):

    if not os.path.exists(db_file):
        return None
    #   print(db_file)
    _, ext = os.path.splitext(db_file)

    rgx = '|'.join(map(lambda c: c.strip('.'), READ_FRMT.keys()))
    rgx = rf'({rgx})'
    ft = detect_file_type(db_file)
    ft = re.findall(rgx, ft)
    if len(ft) > 0:
        frmt = f'.{ft[0]}'
    else:
        frmt = ext
    return read(db_file, frmt, **kwargs)


def read(db_file, frmt, **kwargs):

    # print(frmt)
    """
    The read function reads in a file and returns
    a pandas dataframe.
    ---------------------------------------------------
    :param db_file: Specify the file path of the database
    :param frmt: Determine which method to use
    :param args: Pass in arguments to the read method
    :return: A dataframe
    """
    args = kwargs if 'args' in kwargs else {'encoding': 'utf-8'}
    method = READ_FRMT.get(frmt)
    if method:
        read_method = getattr(pd, method)
        df = read_method(db_file, **args)
        return df
