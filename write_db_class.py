from collections.abc import Iterable
from multiprocessing.pool import ThreadPool
import os
import sys
import threading
import time
import signal
import pandas as pd

from read_db import ReadDb
from abc import ABC, abstractmethod

from util import WRITE_FRMT, SUBSET


class Constant(ABC):
    @staticmethod
    @abstractmethod
    def _filter_df_args(args):
        pass


class Write2Db(Constant):

    @staticmethod
    def _is_valid_data(data):
        return isinstance(data,
                          list) and all(isinstance(val, dict) for val in data)

    @staticmethod
    def _filter_df_args(akwargs):
        valid_akwargs = {}
        valid_keys = pd.DataFrame().keys()  # Get the valid keys for DataFrame creation
        for key, value in akwargs.items():
            if key in valid_keys:
                valid_akwargs[key] = value
        return valid_akwargs

    def __init__(self, data, fn, **akwargs):
        """
        @param data: same as the data param accepted by
        pd.DataFrame
        @param fn: the file containing the original db
        """

        self.fn = fn
        self.fail = False
        self.file_lock = threading.Lock()
        self.akwargs = self._filter_df_args(akwargs)

        if len(data) == 0:
            print('empty list or iterable: nothing to write')
            self.fail = True
        if not self._is_valid_data(data):
            print('Failed to write input, Invalid type')
            self.fail = True
        try:
            self.df = pd.DataFrame(data, **self.akwargs)
        except Exception as e:  # pylint: disable=broad-except
            print(f'error : {e}')
            self.fail = True
        signal.signal(signal.SIGINT, self._signal_handler)

    @staticmethod
    def _signal_handler(self, sig, frame):
        print("Interrupt received. Exiting gracefully.")
        sys.exit(0)

    def write(self, frmt):
        self.akwargs['index'] = False
        print(f'{threading.current_thread().name}: writing ... ')
        method = WRITE_FRMT.get(frmt)
        if method:
            write_method = getattr(self.df, method)
            self.file_lock.acquire()
            # print(self.df)
            write_method(self.fn, **self.akwargs)
            self.file_lock.release()
            return True

    def write_db(self):

        orig_df = ReadDb(self.fn, **self.akwargs).read_db()

        if not isinstance(orig_df, pd.DataFrame):
            print(f'No existing file: {self.fn}')
            print(f'Creating file: {self.fn}')
        elif orig_df.shape[1] != self.df.shape[1]:
            print(orig_df.shape, self.df.shape)
            print(
                f'file: {self.fn} has an incompatibale structure with you data')
            print(f'Choose a different name')
            return False
        else:
            self.df = pd.concat([orig_df, self.df]).reset_index(
                drop=True).drop_duplicates(subset=SUBSET)
        if self.fail:
            return False

        name, frmt = os.path.splitext(self.fn)
        rgx = '|'.join(map(lambda c: c.strip(
            '.'), WRITE_FRMT))
        rgx = rf'({rgx})'
        if frmt not in WRITE_FRMT:
            frmt = '.csv'
            print('Unsupported file extension.')
            print(f'Writing {name}.csv in default format CSV')
        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(self.write, (frmt,))
        status = async_result.get()
        return status


if __name__ == "__main__":
    data = [{'timestamp': '10 May 2024 at 15:51',
             'title': 'You e Feel (Radio Edit)',
             'artist': 'Vasscon',
             'isexplicit': 'No',
             'lyricssnippet': '',
             'lyricsnippetsynced': '',
             'artwork': 'Image',
             'videourl': '',
             'shazamurl': 'https://www.shazam.com/track/82175391/you-make-me-feel-radio-edit?co=GB=shortcuts=7277=-4.9489737E-4=231796=2024-05-10T14:51:07.735Z',
             'applemusicurl': '',
             'name': 'Vasscon - You Make Me Feel (Radio Edit)'},
            {'timestamp': '10 May 2024 at 15:51',
             'title': 'Make Me Feel (Radio Edit)',
             'artist': 'Vasscon',
             'isexplicit': 'No',
             'lyricssnippet': '',
             'lyricsnippetsynced': '',
             'artwork': 'Image',
             'videourl': '',
             'shazamurl': 'https://www.shazcom/track/82175391/you-make-me-feel-radio-edit?co=GB=shortcuts=7277=-4.9489737E-4=231796=2024-05-10T14:51:07.735Z',
             'applemusicurl': '',
             'name': 'Vas - You e(Radio Edit)'}]

    print('testing .....')
    print(Write2Db(data,
                   'tmp.json', encoding='utf-8').write_db())
    data = [{'timestamp': '10 May 2024 at 15:51',
             'title': 'You e F(Radio Edit)',
             'artist': 'Vasscon',
             'isexplicit': 'No',
             'lyricssnippet': '',
             'lyricsnippetsynced': '',
             'artwork': 'Image',
             'videourl': '',
             'shazamurl': 'https://www.shazam.com/track/82175391/you-make-me-feel-radio-edit?co=GB=shortcuts=7277=-4.9489737E-4=231796=2024-05-10T14:51:07.735Z',
             'applemusicurl': '',
             'name': 'Vass You Make Me Feel (Radio Edit)'},
            {'timestamp': '10 May 2024 at 15:51',
             'title': 'Make Me Feel (Radio Edit)',
             'artist': 'Vasscon',
             'isexplicit': 'No',
             'lyricssnippet': '',
             'lyricsnippetsynced': '',
             'artwork': 'Image',
             'videourl': '',
             'shazamurl': 'https://www.shazcom/track/82175391/you-make-me-feel-radio-edit?co=GB=shortcuts=7277=-4.9489737E-4=231796=2024-05-10T14:51:07.735Z',
             'applemusicurl': '',
             'name': 'Vas - You e(Rdio Edit)'}]
    print(Write2Db(data,
                   'tmp.json', encoding='utf-8').write_db())
