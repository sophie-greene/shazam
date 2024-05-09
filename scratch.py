
import os
import pandas as pd


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

def read_db(db_file, encoding='utf-8'): 
      
    """
    The read_db function reads a database file and returns a pandas dataframe.
    
    :param db_file: Specify the path of the file to be read
    :param encoding: Specify the encoding of the file
    :return: A dataframe

    """
    name, ext = os.path.splitext(db_file)
    name = name.split('/')[-1]
    method = read_ext.get(ext)
    if method:
        read_method = getattr(pd, method)
        df = read_method(db_file, encoding=encoding)
    else:
        print("Unsupported file extension.")
        print('trying to read file in csv format')
        try:
            df = pd.read_csv(db_file)
        except pd.errors.ParserError as e:
            print(f'Invalid data format {e.with_traceback}')
            return None
    return df