"""
Unit tests for the shazam_step module.

This module contains unit tests for the functions defined in the shazam_step module. 
It tests the functionality of the 'fetch_row' and 'run_fetch_row' functions.

Tested Functions:
- test_fetch_row: Tests the fetch_row function.
- test_run_fetch_row: Tests the run_fetch_row function.

Usage:
1. Run this module to execute all the unit tests.

Example:
```python
python test_shazam_step.py
"""

import unittest
from unittest.mock import patch, MagicMock
import shazam_step

class TestShazamStep(unittest.TestCase):
    """
    Unit tests for the shazam_step module.

    This class contains unit tests for the functions defined in the shazam_step module. 
    It tests the functionality of the 'fetch_row' and 'run_fetch_row' functions.

    Test Cases:
    - test_fetch_row: Tests the fetch_row function.
    - test_run_fetch_row: Tests the run_fetch_row function.
    """

    @patch('shazam_step.subprocess.run')
    def test_fetch_row(self, mock_subprocess_run):
        """
        Test case for the fetch_row function.

        This test case checks whether the fetch_row function
        correctly runs the Shazam process using subprocess.run.

        It mocks the subprocess.run method to simulate the execution 
        of the Shazam process and asserts that the function returns 
        the expected subprocess.CompletedProcess object.

        """
        # Define the output file path
        outfile = 'output.csv'
        
        # Define the expected command to run the Shazam process
        expected_command = ["shortcuts", "run", "shazam_step", "--output-path", outfile]
        
        # Create a MagicMock object representing the expected result
        expected_result = MagicMock(returncode=0)
        
        # Mock the subprocess.run method with the expected result
        mock_subprocess_run.return_value = expected_result

        # Call the fetch_row function
        result = shazam_step.fetch_row(outfile)

        # Assert that subprocess.run was called with the expected command and arguments
        mock_subprocess_run.assert_called_once_with(expected_command, capture_output=True, text=True, check=False)
        
        # Assert that the result matches the expected subprocess.CompletedProcess object
        self.assertEqual(result, expected_result)

    @patch('shazam_step.os.path.exists')
    @patch('shazam_step.threading.Thread')
    def test_run_fetch_row(self, mock_thread, mock_os_path_exists):
        """
        Test case for the run_fetch_row function.

        This test case checks whether the run_fetch_row function
        correctly creates a new thread for the fetch_row function
        and continuously checks for the existence of the output file.

        It mocks the os.path.exists method to simulate the existence 
        of the output file during the test and asserts that the function 
        returns True when the output file exists.

        """
        # Define the output file path
        outfile = 'output.csv'
        
        # Mock the os.path.exists method to simulate file existence
        mock_os_path_exists.side_effect = [False, False, True]

        # Call the run_fetch_row function
        result = shazam_step.run_fetch_row(outfile)

        # Assert that threading.Thread was called to create a new thread
        mock_thread.assert_called_once()
        
        # Assert that the function returns True when the output file exists
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
