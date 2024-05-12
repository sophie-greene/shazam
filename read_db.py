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

class ReadDb():
    def __init__(self, fn, **akwargs):
        self.file_lock = threading.Lock()
        signal.signal(signal.SIGINT, self.signal_handler)
        self.fn = fn
        self.akwargs = akwargs
    def signal_handler(self, sig, frame):
        print("Interrupt received. Exiting gracefully.")
        sys.exit(0)
    
    def read_db(self):
        if not os.path.exists(self.fn):
            return None
        _, ext = os.path.splitext(self.fn)

        rgx = '|'.join(map(lambda c: c.strip('.'), READ_FRMT.keys()))
        rgx = rf'({rgx})'
        ft = util.detect_file_type(self.fn)
        ft = re.findall(rgx, ft)
        if len(ft) > 0:
            frmt = f'.{ft[0]}'
        else:
            frmt = ext
        return self.read(frmt)


    def read(self, frmt):
        args = self.akwargs if 'args' in self.akwargs else {'encoding': 'utf-8'}
        method = READ_FRMT.get(frmt)
        if method:
            read_method = getattr(pd, method)
            self.file_lock.acquire()
            df = read_method(self.fn, **args)
            self.file_lock.release()
            return df

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(ReadDb(sys.argv[1]).read_db())
    else:
        print('command line use is read_db')
        print('Enter data file name:')
        print(f'Usage: python {os.path.basename(sys.argv[0])} db_file')
