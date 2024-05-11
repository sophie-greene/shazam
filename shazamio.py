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
from multiprocessing.pool import ThreadPool
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


class ReadDb:
    def __init__(self):
        self.file_lock = threading.Lock()
        signal.signal(signal.SIGINT, self.signal_handler)

    def read(self, fn, frmt, **akwargs):
        """
        The _read function reads in a file and returns a pandas dataframe.

        :param db_file: Specify the file that is being read
        :param frmt: Specify the format of the file that is being read
        :param **kwargs: Pass a variable number of arguments to the function
        :return: A dataframe
        """
        args = akwargs if 'args' in akwargs else {'encoding': 'utf-8'}
        method = READ_FRMT.get(frmt)
        if method:
            read_method = getattr(pd, method)
            self.file_lock.acquire()
            df = read_method(fn, **args)
            self.file_lock.release()
            return df

    def signal_handler(self, sig, frame):
        print("Interrupt received. Exiting gracefully.")
        sys.exit(0)

    def read_db(self, fn):
        if not os.path.exists(fn):
            return None

        _, ext = os.path.splitext(fn)

        rgx = '|'.join(map(lambda c: c.strip('.'), READ_FRMT.keys()))
        rgx = rf'({rgx})'
        ft = util.detect_file_type(fn)
        ft = re.findall(rgx, ft)
        if len(ft) > 0:
            frmt = f'.{ft[0]}'
        else:
            frmt = ext

        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(self.read, (frmt,))
        data = async_result.get()
        if data is not None:
            return data

if __name__ == "__main__":
    if len(sys.argv) == 2:
        file_handler = ReadDb()
        print(file_handler.read_db(sys.argv[1]))
    else:
        print('command line use is read_db')
        print('Enter data file name:')
        print(f'Usage: python {sys.argv[0]} db_file')

# print(read_db('file.json'))
