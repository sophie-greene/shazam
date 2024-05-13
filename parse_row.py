"""
parse_row - Module for parsing XML data using a template.

This module provides a function for parsing XML data based on a
    predefined template. It utilizes the BeautifulSoup library
    to navigate and extract information from XML documents.

Constants:
    SHAZAM_TEMPLATE (str): A string containing an XML template with placeholders for specific tags.

Functions:
    parse_row(fn, encoding='utf-8'): Parse an XML file using the specified template.
    
    The `parse_row` function takes the path to an XML file and optionally an encoding parameter.
        It parses the XML document using BeautifulSoup and a predefined template stored 
        in the `SHAZAM_TEMPLATE` constant. The function returns a dictionary with keys
        as tag names and values as the text content of those tags.

    Parameters:
        fn (str): The path to the XML file to be parsed.
        encoding (str, optional): The encoding of the XML file (default is 'utf-8').

    Returns:
        dict or None: A dictionary containing parsed data if the file exists and
            contains valid XML data. Returns None if the file does not exist or is empty.

Example Usage:
    >>> parsed_data = parse_row('example.xml')
    >>> print(parsed_data)
    {'timestamp': 'Date', 'title': 'Shazam Media (Title)', ...}

Notes:
    - This module requires the BeautifulSoup library to be installed.
    ```sh
        pip install bs4
    ```
    - The `SHAZAM_TEMPLATE` string serves as a map to interpret the
        XML data and extract relevant information.
"""

from bs4 import BeautifulSoup

SHAZAM_TEMPLATE = """
<root>

<timestamp>
Date
</timestamp>

<title>
Shazam Media (Title)
</title>

<artist>
Shazam Media (Artist)
</artist>

<isexplicit>
Shazam Media (Is Explicit)
</isexplicit>

<lyricssnippet>
Shazam Media (Lyrics Snippet)
</lyricssnippet>

<lyricsnippetsynced>
Shazam Media (Lyric Snippet Synced)
</lyricsnippetsynced>

<artwork>
Shazam Media (Artwork)
</artwork>

<videourl>
Shazam Media (Video URL)
</videourl>

<shazamurl>
Shazam Media (Shazam URL)
</shazamurl>

<applemusicurl>
Shazam Media (Apple Music URL)
</applemusicurl>

<name>
Shazam Media (Name)
</name>

</root>
"""


def parse_row(fn, encoding="utf-8"):
    """
    Parse an XML file using the specified template.

    This function parses an XML file using the predefined 
    template stored in the SHAZAM_TEMPLATE constant.
    It extracts information from the XML document based on the template structure.

    Parameters:
        fn (str): The path to the XML file to be parsed.
        encoding (str, optional): The encoding of the XML file (default is 'utf-8').

    Returns:
        dict or None: A dictionary containing parsed data if the file exists
        and contains valid XML data. Returns None if the file does not exist or is empty.
    """
    soup = BeautifulSoup(SHAZAM_TEMPLATE, "xml")
    root = soup.findChildren()
    tags = [tag.name for tag in root if tag and tag != "root"]
    try:
        with open(fn, encoding=encoding) as f:
            row = f.read()
    except FileNotFoundError:
        return None
    soup = BeautifulSoup(row.replace("\n", ""), "xml")
    root = soup.select_one("root")
    if root:
        dct = {}
        for tag in tags:
            if not tag:
                continue
            tag_content = root.find(tag)
            if tag_content:
                dct[tag] = tag_content.text
        if len(dct) != 0:
            return dct


#print(parse_row('r.txt'))
