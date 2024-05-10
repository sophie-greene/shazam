import os
import subprocess


def detect_file_type(fn):
    """
    The detect_file_type function takes a file path as input and returns the
		file type. The function uses the [file][file man] command 
	 	to determine the file type.
    The output of this command is parsed to extract only the file type.
	---------------------------------------------------------------
    :param fn: Pass the name and path of a file to the function
    :return: The file type if file exists, '' otherwise
	[file man](https://man7.org/linux/man-pages/man1/file.1.html)
    """
    if not os.path.exists(fn):
        return ''
    result = subprocess.run(
        ['file',
         '--mime-type',
         fn],
         capture_output=True, text=True, check=False)
    # Extract the file type from the output
    file_type = result.stdout.strip().split(': ')[-1]

    return file_type