import os
import re
import subprocess
import threading
import time
import signal
import sys

class ShazamStep():
    def __init__(self, filename):
        if re.match ('[^A-Za-z0-9]',filename):
            print('Only alphanumeric names allowed, cleaning up the filename')
        self.filename = re.sub('[^A-Za-z0-9]','',filename)
        if len(self.filename) == 0:
            self.filename = 'outfile'

    def fetch_row(self):
        """
        Run the shazam_step shortcut using subprocess
        and return a subprocess.CompletedProcess object.
        """
        script = ["shortcuts", "run", "shazam_step",
                  "-o", self.filename]
        print(f'run: {' '.join(script)}')
        return subprocess.call(script,)

    def run(self):
        """
        Create a new thread to run the fetch_row function asynchronously
        and continuously check for the existence of the output file until
        the Shazam process completes.
        """
        # Define a signal handler for interrupt signal
        def signal_handler(sig, frame):
            print("Interrupt received. Exiting gracefully.")
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)  # Register signal handler

        # Create and start a new thread for the fetch_row function
        thr_fetch_row = threading.Thread(target=self.fetch_row)
        thr_fetch_row.start()

        # Continuous check for the existence of the output file
        while True:
            if os.path.exists(self.filename):
                print("Shazamed Successfully!")
                return True
            time.sleep(1)


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 2:
        print(sys.argv[1])
        ShazamStep(sys.argv[1]).run()
    else:
        print("Usage: python script.py output_file")
