import unittest
import os
import pandas as pd
from unittest.mock import patch
from read_db import detect_file_type, read_frmt


class TestParseRow(unittest.TestCase):
    """
    Test suite for the 'parse_row' module.
    """

    def test_detect_file_type_existing_csv(self):
        """
        Test the detect_file_type function with an existing CSV file.
        """
        # Create a temporary CSV file
        test_csv_path = 'test.csv'
        with open(test_csv_path, 'w') as f:
            f.write('Test data\n')

        # Call the detect_file_type function
        detected_type = detect_file_type(test_csv_path)

        # Assert that the detected type matches the expected type
        self.assertEqual(detected_type, 'text/plain')

        # Remove the temporary CSV file
        os.remove(test_csv_path)

    def test_detect_file_type_nonexisting(self):
        """
        Test the detect_file_type function with a non-existing file.
        """
        # Call the detect_file_type function with a non-existing file
        detected_type = detect_file_type('non_existing.csv')

        # Assert that an empty string is returned
        self.assertEqual(detected_type, '')

    def test_read_frmt_csv(self):
        """
        Test the read_frmt function with a CSV file.
        """
        # Create a temporary CSV file with test data
        test_df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        test_file = 'test.csv'
        test_df.to_csv(test_file, index=False)

        # Test reading from CSV
        df_from_csv = read_frmt(test_file)

        # Assert that the DataFrame matches the expected DataFrame
        self.assertTrue(df_from_csv.equals(test_df))

        # Clean up temporary test file
        os.remove(test_file)

    def test_read_frmt_nonexisting(self):
        """
        Test the read_frmt function with a non-existing file.
        """
        # Test reading from a non-existing file
        df = read_frmt('non_existing.csv')

        # Assert that None is returned
        self.assertIsNone(df)


if __name__ == '__main__':
    unittest.main()
