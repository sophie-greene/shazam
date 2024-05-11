import os
import threading
import time

import pandas as pd

from read_db import read_db
import util
SUBSET = ["artist", "title", "name"]
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



def write(df, fn, frmt, **kwargs):
 
    """
    The write function is a function that writes the dataframe to a file.
    
    :param df: Pass the dataframe to be written
    :param db_file: Specify the file path of the database
    :param frmt: Determine the format of the file that is being written to
    :param **kwargs: Pass a variable number of keyword arguments to a function
    :return: The dataframe that is written to the file
    """
    method = WRITE_FRMT.get(frmt)
    if method:
        write_method = getattr(df, method)
        write_method(fn, **kwargs)

def write_db(df, fn, **kwargs):

    """
    The write_db function takes a pandas DataFrame and writes it to a file.
    
    :param df: Pass the dataframe to be written
    :param fn: Specify the file name
    :param **kwargs: Pass a dictionary of arguments to the write function
    :return: True if the file is written successfully,
    """
    args = kwargs if 'args' in kwargs else {'encoding': 'utf-8'}
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
        
    # Create a new thread for fetch_row function
    thr_fetch_row = threading.Thread(target=write, args=(df,fn,frmt,), kwargs=args)

    # Start the thread for fetch_row function
    thr_fetch_row.start()
    while True:
        try:
            print(f'{threading.current_thread().name}: Writting Data!.....')
            if os.path.exists(fn):
                print('{threading.current_thread().name}: done!')
                return True
            time.sleep(1)
        except Exception: # pylint: disable=broad-except
            return False

def append_db(lst_of_dct, fn):
    print('Preparing to write your data ....')
    df = pd.DataFrame(lst_of_dct)
    if len(lst_of_dct) == 0:
        print('No data to write')
        return False
    if not os.path.exists(fn):
        write_db(df, fn)
        return True
    odf = read_db(fn, encoding="utf-8")
    df = pd.concat([odf, df]).reset_index(
            drop=True).drop_duplicates(subset=SUBSET)
    write_db(df, fn)
    return True

# Create a new thread and pass write to it
thd_write = threading.Thread(target=my_function)

# Start the thread
thd_write.start()

# Main thread continues execution
for i in range(3):
    print("Executing in main thread:", threading.current_thread().name)
    time.sleep(1)

# Wait for the thread to finish
my_thread.join()

print("Main thread and child thread execution completed.")



import threading
import time
import signal
import sys

# Lock for file access
file_lock = threading.Lock()

def read_file():
    try:
        with open("data.txt", "r") as file:
            file_lock.acquire()
            data = file.read()
            file_lock.release()
            print("Read data:", data)
    except Exception as e:
        print("Error reading file:", e)

def write_file():
    try:
        with open("data.txt", "a") as file:
            file_lock.acquire()
            file.write("New data\n")
            file_lock.release()
            print("Data written to file")
    except Exception as e:
        print("Error writing to file:", e)

def signal_handler(sig, frame):
    print("Interrupt received. Exiting gracefully.")
    sys.exit(0)

if __name__ == "__main__":
    # Register signal handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)

    # Start reading and writing threads
    read_thread = threading.Thread(target=read_file)
    write_thread = threading.Thread(target=write_file)

    read_thread.start()
    write_thread.start()

    # Wait for threads to complete
    read_thread.join()
    write_thread.join()

    print("Program execution completed.")



# test_df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
# print(write_db(test_df, 'data.csv',encoding='utf-8'))
