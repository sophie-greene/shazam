"""
The 'read_data' module provides functions for file handling and
    data reading using Pandas.

Functions:
- read_frmt(db_file, **kwarg): Reads a file into a Pandas DataFrame based on its format.
- read(db_file, frmt, **kwarg): Reads a file into a Pandas DataFrame
    using a specific format.

Constants:
- READ_FRMT: A dictionary mapping file extensions to Pandas methods for
    reading data from file formats.

Usage Example:
    import read_data
    import util

    # Determine file type
    file_type = util.detect_file_type('example.csv')
    print(file_type)  # Output: 'text/csv'

    # Read file into DataFrame
    df = read_data.read_frmt('example.csv')
    print(df.head())  # Output: Displays the first few rows of the DataFrame

    # Further file handling and reading options are available using the provided functions.

Note:
- The 'util.detect_file_type' function relies on the 'file' command available
    in Unix-like systems. see util.py for details
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
import re

import pandas as pd

import util

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





def read_db(db_file, **kwargs):

    """
    The read_db function reads a database file and returns the data in a pandas DataFrame.
    
    :param db_file: Specify the path to the database file
    :param **kwargs: Pass a variable number of keyword arguments to the function
    :return: A dataframe
    """
    if not os.path.exists(db_file):
        return None
    #   print(db_file)
    _, ext = os.path.splitext(db_file)

    rgx = '|'.join(map(lambda c: c.strip('.'), READ_FRMT.keys()))
    rgx = rf'({rgx})'
    ft = util.detect_file_type(db_file)
    ft = re.findall(rgx, ft)
    if len(ft) > 0:
        frmt = f'.{ft[0]}'
    else:
        frmt = ext
    return read(db_file, frmt, **kwargs)


def read(db_file, frmt, **kwargs):
    """
    The _read function reads in a file and returns a pandas dataframe.
    
    :param db_file: Specify the file that is being read
    :param frmt: Specify the format of the file that is being read
    :param **kwargs: Pass a variable number of arguments to the function
    :return: A dataframe

    """
    args = kwargs if 'args' in kwargs else {'encoding': 'utf-8'}
    method = READ_FRMT.get(frmt)
    if method:
        read_method = getattr(pd, method)
        df = read_method(db_file, **args)
        return df
# print(read_db('file.json'))
