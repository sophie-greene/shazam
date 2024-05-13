

from multiprocessing.pool import ThreadPool
import os  # The os module is a built-in Python module
import time  # The time module is a built-in Python module
import sys
import signal

# ###########################################################
# Custom module find in file ./shazam_step.py
from shazam_step import ShazamStep
# Custom module find in file ./write_db_class.py
from write_db_class import Write2Db
# Custom module find in file ./parse_row.py
from parse_row import parse_row
# ###########################################################

class ShazamLogger():
    # Define a signal handler for interrupt signal
    def signal_handler(self, sig, frame):
        print("Interrupt received. Exiting gracefully.")
        print(self.stored)
        if not self.stored:
            save()
        sys.exit(0)
    def __init__(self, filename) -> None:
        self.subset = ['title', 'artist']
        self.stored = False
        self.db_file = filename
        self.outfile = './www'
        self.data = list()
        self.past = list()
        self.rows = list()
        signal.signal(signal.SIGINT, self.signal_handler)

    def wait_for_file(self, limit=1e12, lag=1):
        """
        The wait_for_file function waits for a file to be created.
        --------------------------------------------------
        :param outfile: Specify the file that is being waited for
        :param limit: Set a limit on the number of times the while loop will run
        :param lag: time delay in seconds,
            after every file check it sleep for `lag` seconds
        :return: True if the file exists, and false if `limit` is reached
        """
        cnt = 0
        while not os.path.exists(self.outfile):
            time.sleep(lag)
            if cnt > limit:
                return False
            cnt += 1
        return True

    def song_changed(self):
        if not self.past:
            return True
        if self.data:
            return all((self.data[k] == self.past[k]) for k in self.subset if k in self.data and k in self.past)
    
    def flow(self):
        ShazamStep(self.outfile).run()
        self.past = self.data
        self.wait_for_file()
        self.data = parse_row(self.outfile)
        os.remove(self.outfile)
        if self.data and len(self.data)>0:
            print(self.data['title'], ' by ',self.data['artist'])
        if not self.song_changed():
            time.sleep(20)
        else:
            if self.data and any(k in self.data for k in self.subset):
                self.rows.append(self.data)
    def save(self):
        wc = Write2Db([self.rows], self.db_file, encoding='utf-8')
        pool = ThreadPool(processes=1)
        async_result = pool.apply_async(wc.run)
        status = async_result.get()
        return status
    
   
    def run(self):

        while True:
            try:
                self.flow()
            except KeyboardInterrupt:
                save()
                self.stored = True
                time.sleep(10)
                break
        if not self.stored:
            save()

if __name__ == "__main__":
    print(ShazamLogger('wshazam.json').run())
