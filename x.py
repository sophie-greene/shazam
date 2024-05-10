import unittest
from unittest.mock import patch
import sys  # Importing sys library

class TestShazamLogger(unittest.TestCase):
    """
    Test cases for the shazam_logger module.
    """

    def test_assign_file_names(self):
        """
        Test the assign_file_names function.
        """
        # Case 1: Two command line arguments
        with patch.object(sys, "argv", ["test.py", "db_file", "outfile"]):  # Use sys.argv instead of os.argv
            db_file, outfile = assign_file_names()
            self.assertEqual(db_file, "db_file")
            self.assertEqual(outfile, "outfile")

        # Case 2: One command line argument
        with patch.object(sys, "argv", ["test.py", "db_file"]):  # Use sys.argv instead of os.argv
            db_file, outfile = assign_file_names()
            self.assertEqual(db_file, "db_file")
            self.assertEqual(outfile, None)

        # Case 3: No command line arguments
        with patch.object(sys, "argv", ["test.py"]):  # Use sys.argv instead of os.argv
            db_file, outfile = assign_file_names()
            self.assertEqual(db_file, "shazam.csv")
            self.assertEqual(outfile, "./outfile")

