"""
The 'shazam_step' module provides utility functions for running the Shazam process asynchronously.

Functions:
- get_row(outfile): 
  This function runs the 'shazam_step' shortcut using subprocess
    and returns a subprocess.CompletedProcess object.
  
  Parameters:
  - outfile (str): Specify the path for the output file.
  
  Returns:
  - A subprocess.CompletedProcess object representing
        the execution status of the 'shazam_step' process.

- run_get_row(outfile):
  This function creates a new thread to run the
    'get_row' function asynchronously and continuously checks for
    the existence of the output file until
    the Shazam process completes.
  
  Parameters:
  - outfile (str): Specify the path for the output file.
  
  Returns:
  - 0 if the Shazam process completes successfully.
  - 1 otherwise

Usage:
1. Import the module: `import shazam_step`
2. Call the `run_get_row(outfile)` function with 
    the desired output file path to run 
    the Shazam process asynchronously
    and wait for its completion.

Example:
```python
import shazam_step

# Run the Shazam process asynchronously 
# and wait for its completion
shazam_step.run_get_row('output.csv')
"""

import os
import threading
import subprocess
import time


def get_row(outfile):
    """
    The get_row function runs the shazam_step shortcut
    and returns a subprocess.CompletedProcess object.
    Please refer to the documentation for subprocess.

    :param outfile: Specify the path for the output file
    :return: A CompletedProcess object
    """
    script = ["shortcuts",
              "run",
              "shazam_step",
              "--output-path",
              outfile]
    return subprocess.run(script, capture_output=True, text=True, check=False)


def run_get_row(outfile):
    """
    This function creates a new thread for the get_row function
    and continuously checks for the existence of 
    the output file until the shazam process completes.

    :param outfile: Specify the path for the output file.
    :return: 0 if the shazam process completes successfully.
             1 otherwise
    """
    # Create a new thread for get_row function
    thr_get_row = threading.Thread(target=get_row, args=(outfile,))

    # Start the thread for get_row function
    thr_get_row.start()

    # Continuous check for the existence of the output file
    while True:
        try:
            print('Shazaming!.....')
            if os.path.exists(outfile):
                print('Success!')
                return 0
            time.sleep(1)
        except Exception: # pylint: disable=broad-except
            return 1
