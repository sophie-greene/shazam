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
def parse_row(outfile, encoding='utf-8'):
    """
    The parse_row function parses the XML document using lxml parser.
    it uses the `SHAZAM_TEMPLATE` string as map to read the xml data
    ---------------------------------------------------------
    :param outfile: Specify the path to the xml file that will be parsed
    :return: A dictionary with keys as the tag names
        and values as the text content of those tags
    """
    soup = BeautifulSoup(SHAZAM_TEMPLATE, 'xml')
    root = soup.root
    tags = [tag.name  for tag in root.children if tag and tag.name!='root']
    try:
        with open(outfile, encoding=encoding) as f:
            row = f.read()
    except FileNotFoundError:
        return None
    # print(row)
    soup = BeautifulSoup(row.replace('\n', ''), 'xml')
    root = soup.select_one('root')
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

print(parse_row('r.txt'))