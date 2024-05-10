"""
The 'shazam_step' module provides utility functions for running the Shazam process asynchronously.

Functions:
- fetch_row(outfile):
  This function runs the 'shazam_step' shortcut using subprocess
    and returns a subprocess.CompletedProcess object.

  Parameters:
  - outfile (str): Specify the path for the output file.

  Returns:
  - A subprocess.CompletedProcess object representing
        the execution status of the 'shazam_step' process.

- run_fetch_row(outfile):
  This function creates a new thread to run the
    'fetch_row' function asynchronously and continuously checks for
    the existence of the output file until
    the Shazam process completes.

  Parameters:
  - outfile (str): Specify the path for the output file.

  Returns:
  - True if the Shazam process completes successfully.
  - False otherwise

Usage:
1. Import the module: `import shazam_step`
2. Call the `run_fetch_row(outfile)` function with
    the desired output file path to run
    the Shazam process asynchronously
    and wait for its completion.
"""
import os
import pandas as pd


class ShazamDataFrame(pd.DataFrame):
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
    
    def read(self, db_file, encoding='utf-8'):
      """
      The read function reads a database file and returns a pandas dataframe.
      -------------------------------------------
      :param db_file: Specify the file to be read
      :param encoding: Specify the encoding of the file
      :return: A pandas dataframe with the contents of the file
      """
      print(db_file)
      name, ext = os.path.splitext(db_file)
      name = name.split('/')[-1]
      method = ShazamDataFrame.READ_EXT.get(ext)
      if method:
          read_method = getattr(pd, method)
          df = read_method(db_file, encoding=encoding)
          return df
      else:
         raise self.errors.