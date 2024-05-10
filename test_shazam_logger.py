"""
Test module for the shazam_logger script.

This module contains test cases for the functions defined
in the shazam_logger script. It utilizes the unittest framework
for organizing and executing the tests. Each test case focuses
on validating the behavior of individual functions and their
interactions with external dependencies.

Author: Sophie Greene
Date: 2024/05/09
"""

import unittest
from unittest.mock import patch
import sys
from shazam_logger import assign_file_names, parse_row, read_db, write_db, wait_for_file


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


    @patch("shazam_logger.BeautifulSoup")
    @patch("builtins.open")
    def test_parse_row(self, mock_open, mock_beautifulsoup):
        """
        Test the parse_row function.
        """
        mock_open.return_value.__enter__.return_value.read.return_value = """
        <root>
            <artist>Test Artist</artist>
            <title>Test Title</title>
            <name>Test Name</name>
        </root>
        """
        mock_beautifulsoup.return_value.root = "root"
        result = parse_row("test.xml")
        self.assertEqual(result["artist"], "Test Artist")
        self.assertEqual(result["title"], "Test Title")
        self.assertEqual(result["name"], "Test Name")

    @patch("pandas.read_csv")
    def test_read_db(self, mock_read_csv):
        """
        Test the read_db function.
        """
        mock_read_csv.return_value = "test_data"
        result = read_db("test.csv")
        self.assertEqual(result, "test_data")


@patch("shazam_logger.pd")
def test_write_db(self, mock_pd):
    """
    Test the write_db function.
    """
    df = MagicMock()
    db_file = "test.csv"

    # Mocking read_csv method
    mock_pd.read_csv.return_value = MagicMock()

    # Calling the function with a DataFrame
    result = write_db(df, db_file)

    # Asserting that to_csv was called
    df.to_csv.assert_called_with(db_file, encoding="utf-8")
    self.assertEqual(result, 0)

    # Calling the function with a non-DataFrame
    non_dataframe = None
    result = write_db(non_dataframe, db_file)

    # Asserting that to_csv was not called
    df.to_csv.assert_not_called()
    self.assertEqual(result, 1)

    @patch("os.path.exists")
    def test_wait_for_file(self, mock_exists):
        """
        Test the wait_for_file function.
        """
        mock_exists.return_value = True
        result = wait_for_file("test.txt")
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
