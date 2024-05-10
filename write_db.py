import os

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

def write(df, db_file, frmt, **kwargs):
 
    """
    The write function is a function that writes the dataframe to a file.
    
    :param df: Pass the dataframe to be written
    :param db_file: Specify the file path of the database
    :param frmt: Determine the format of the file that is being written to
    :param **kwargs: Pass a variable number of keyword arguments to a function
    :return: The dataframe that is written to the file
    """
    args = kwargs if 'args' in kwargs else {'encoding': 'utf-8'}

    method = WRITE_FRMT.get(frmt)
    if method:
        write_method = getattr(df, method)
        write_method(db_file, **args)

def write_db(df, fn, **kwargs):

    """
    The write_db function takes a pandas DataFrame and writes it to a file.
    
    :param df: Pass the dataframe to be written
    :param fn: Specify the file name
    :param **kwargs: Pass a dictionary of arguments to the write function
    :return: True if the file is written successfully,
    """
    if not isinstance(df, pd.DataFrame):
        return False
    if len(df) == 0:
        return False
    name, frmt = os.path.splitext(fn)
    rgx = '|'.join(map(lambda c: c.strip('.'), WRITE_FRMT.keys()))
    rgx = rf'({rgx})'
    if frmt not in WRITE_FRMT:
        frmt = '.csv'
        print('Unsupported file extension.')
        print(f'Writing {name}.csv in default format CSV')

    try:
        write(df, fn, frmt, **kwargs)
        return True
    except pd.errors.ParserError:
        return False

# test_df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
# print(write_db(test_df, 'data.csv',encoding='utf-8'))
