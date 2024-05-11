import os

import pandas as pd
from read_db import read_db
from write_db import write_db

SUBSET = ["artist", "title", "name"]
def append_db(lst_of_dct, db_file):
    """
    The append_db function appends a list of dictionaries to
        an existing database file.
    ------------------------------------------------------------
    :param lst_of_dct: Pass in a list of dictionaries to the function
    :param db_file: Specify the file to be written to
    :return: 0
    """
    ndf = pd.DataFrame(lst_of_dct)
    if os.path.exists(db_file):
        df = read_db(db_file, encoding="utf-8")

        df = pd.concat([df, ndf]).reset_index(
            drop=True).drop_duplicates(subset=SUBSET)
        write_db(df, db_file)
    else:
        write_db(ndf, db_file)
    return 0

def append(df):
    """
    The append_db function appends a list of dictionaries to
        an existing database file.
    ------------------------------------------------------------
    :param lst_of_dct: Pass in a list of dictionaries to the function
    :param db_file: Specify the file to be written to
    :return: 0
    """
    write_db(df, db_file)
  
    return 0