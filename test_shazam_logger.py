"""
Test module for the shazam_logger script.

This module contains test cases for the functions defined
    in the shazam_logger script.
It utilizes the unittest framework for organizing and executing the tests.
Each test case focuses on validating the behavior of individual functions
and their interactions with external dependencies.

Author: Sophie Greene
Date: 2014/05/08

Dependencies:
    - unittest
    - patch from unittest.mock
    - shazam_logger module

Attributes:
    - mock_read_db: A MagicMock object mocking the read_db function.
    - mock_write_db: A MagicMock object mocking the write_db function.
    - mock_sys: A MagicMock object mocking the sys module.
    - mock_parse_row: A MagicMock object mocking the parse_row function.
    - mock_wait_for_file: A MagicMock object mocking
        the wait_for_file function.
    - mock_get_row: A MagicMock object mocking the get_row function.
    - mock_subprocess: A MagicMock object mocking the subprocess module.
    - mock_beautifulsoup: A MagicMock object mocking the BeautifulSoup class.

Methods:
    - test_append_db: Test case for the append_db function.
    - test_assign_file_names: Test case for the assign_file_names function.
    - test_get_data: Test case for the get_data function.
    - test_get_row: Test case for the get_row function.
    - test_match: Test case for the match function.
    - test_parse_row: Test case for the parse_row function.
    - test_read_db: Test case for the read_db function.
    - test_write_db: Test case for the write_db function.
    - test_wait_for_file: Test case for the wait_for_file function.
"""

import unittest
from unittest.mock import patch, MagicMock
import shazam_logger


class TestShazamLogger(unittest.TestCase):
    """
    Test cases for the shazam_logger module.
    """

    @patch('shazam_logger.read_db')
    @patch('shazam_logger.write_db')
    def test_append_db(self, mock_write_db, mock_read_db):
        """
        Test the append_db function.
        """
        lst_of_dct = [{'artist': 'Artist 1',
                       'title': 'Title 1',
                       'name': 'Name 1'},
                      {'artist': 'Artist 2',
                       'title': 'Title 2',
                       'name': 'Name 2'}]
        db_file = 'test.db'

        # Mocking read_db to return a DataFrame
        mock_read_db.return_value = MagicMock()

        # Mocking write_db
        shazam_logger.append_db(lst_of_dct, db_file)

        # Asserting that write_db was called
        mock_write_db.assert_called()

    @patch('shazam_logger.sys')
    def test_assign_file_names(self, mock_sys):
        """
        Test the assign_file_names function.
        """
        mock_sys.argv = ['test.py', 'db_file', 'outfile']
        db_file, outfile = shazam_logger.assign_file_names()

        # Asserting that the correct values are assigned
        self.assertEqual(db_file, 'db_file')
        self.assertEqual(outfile, 'outfile')

    @patch('shazam_logger.get_row')
    @patch('shazam_logger.wait_for_file')
    @patch('shazam_logger.parse_row')
    def test_get_data(self, mock_parse_row, mock_wait_for_file, mock_get_row):
        """
        Test the get_data function.
        """
        outfile = 'test.xml'

        # Mocking functions and setting up return values
        mock_parse_row.return_value = {'artist': 'Artist', 'title': 'Title'}
        mock_wait_for_file.return_value = True
        mock_get_row.return_value = MagicMock()

        # Calling the function
        data = shazam_logger.get_data(outfile)

        # Asserting that the data list is populated
        self.assertNotEqual(len(data), 0)

    @patch('shazam_logger.subprocess')
    def test_get_row(self, mock_subprocess):
        """
        Test the get_row function.
        """
        outfile = 'test.xml'
        shazam_logger.get_row(outfile)

        # Asserting that subprocess.run was called
        mock_subprocess.run.assert_called()

    def test_match(self):
        """
        Test the match function.
        """
        sentence = 'This is a test sentence.'
        chars = 'aeiou'

        # Testing when all characters are present
        result = shazam_logger.match(sentence, chars)
        self.assertTrue(result)

        # Testing when not all characters are present
        chars = '12345'
        result = shazam_logger.match(sentence, chars)
        self.assertFalse(result)

    @patch('shazam_logger.BeautifulSoup')
    def test_parse_row(self, mock_beautifulsoup):
        """
        Test the parse_row function.
        """
        outfile = 'test.xml'
        soup = MagicMock()
        soup.root = MagicMock()
        soup.root.children = ['artist', 'title', 'name']
        mock_beautifulsoup.return_value = soup

        # Mocking file read
        with patch('builtins.open',
                   unittest.mock.mock_open(read_data='')) as mock_file:
            result = shazam_logger.parse_row(outfile)
            # Asserting that the correct keys are in the result dictionary
            self.assertIn('artist', result)
            self.assertIn('title', result)
            self.assertIn('name', result)

    @patch('shazam_logger.pd')
    def test_read_db(self, mock_pd):
        """
        Test the read_db function.
        """
        db_file = 'test.db'

        # Mocking read_csv method
        mock_pd.read_csv.return_value = MagicMock()

        # Calling the function
        result = shazam_logger.read_db(db_file)

        # Asserting that read_csv was called
        mock_pd.read_csv.assert_called()

    @patch('shazam_logger.pd')
    def test_write_db(self, mock_pd):
        """
        Test the write_db function.
        """
        df = MagicMock()
        db_file = 'test.db'

        # Calling the function
        shazam_logger.write_db(df, db_file)

        # Asserting that to_csv was called
        df.to_csv.assert_called()

    @patch('shazam_logger.os')
    def test_wait_for_file(self, mock_os):
        """
        Test the wait_for_file function.
        """
        outfile = 'test.xml'

        # Mocking os.path.exists
        mock_os.path.exists.return_value = False
        result = shazam_logger.wait_for_file(outfile)

        # Asserting that it returns False if the file doesn't exist
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
