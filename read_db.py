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
import signal
import sys
import threading
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

class ShazamIO:
    def __init__(self, fn):
        self.fn = fn
        self.file_lock = threading.Lock()
        signal.signal(signal.SIGINT, self.signal_handler)
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
    def signal_handler(self, sig, frame):
        print("Interrupt received. Exiting gracefully.")
        sys.exit(0)

    def read_file(self):
        try:
            with open(self.fn, "r") as file:
                self.file_lock.acquire()
                data = file.read()
                self.file_lock.release()
                print("Read data:", data)
        except Exception as e:
            print("Error reading file:", e)

    def start(self):
        if not os.path.exists(self.fn):
            return None
        #   print(db_file)
        _, ext = os.path.splitext(self.fn)

        rgx = '|'.join(map(lambda c: c.strip('.'), READ_FRMT.keys()))
        rgx = rf'({rgx})'
        ft = util.detect_file_type(self.fn)
        ft = re.findall(rgx, ft)
        if len(ft) > 0:
            frmt = f'.{ft[0]}'
        else:
            frmt = ext
        self.frmt = frmt
        self.read(frmt, **kwargs)
        self.file_lock.release()
        read_thread = threading.Thread(target=self.read)
        write_thread = threading.Thread(target=self.write_file, args=("New data",))

        read_thread.start()
        write_thread.start()

        # Wait for the read thread to finish and capture the returned data
        read_thread.join()
        data = read_thread.result

        # Continue with data processing or other operations
        if data is not None:
            print("Data read from file:", data)
        else:
            print("Error reading file.")
        
        write_thread.join()

        print("Program execution completed.")


if __name__ == "__main__":
    file_handler = ShazamIO("data.txt")
    file_handler.start()


def read_db(self, db_file, **kwargs):

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
    self.file_lock.acquire()
    read(db_file, frmt, **kwargs)
    self.file_lock.release()


# print(read_db('file.json'))
