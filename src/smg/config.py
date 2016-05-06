import lxml.etree as ET

DefaultConfigFileName = 'smg.xml'
DefaultStoreFileName = 'smg.p'

def getConfig(cfgFileName = DefaultConfigFileName):
    """Reads the config XML from the file."""
    xml = ET.parse(cfgFileName)

    cfg = dict()
    cfg['releaseId'] = xml.find('./releaseId').text.strip()
    cfg['genres'] = list()
    for el in xml.findall('./genres/genre'):
        cfg['genres'].append(el.text.strip())
    cfg['pickleFileName'] = xml.find('./pickleFileName').text.strip()

    return cfg


def createConfig(cfgFileName = DefaultConfigFileName):
    """Creates a new config file by querying the user and MusicBrainz."""

    # Get info from user
    releaseId = input("MusicBrainz ID for release : ")
    genres = list()
    while True:
        genre = input("Input Genre (empty for end): ")
        if genre == '':
            if len(genres) == 0:
                raise Exception('Must enter at least one genre')
            break
        genres.append(genre)
    pickleFileName = input("Data file name (empty for default):  ")
    if pickleFileName == '':
        pickleFileName = DefaultStoreFileName

    # Create XML structure
    cfg = ET.Element("smg")
    ET.SubElement(cfg, "releaseId").text = releaseId
    ET.SubElement(cfg, "pickleFileName").text = pickleFileName
    genresEl = ET.SubElement(cfg, "genres")
    for genre in genres:
        ET.SubElement(genresEl, "genre").text = genre

    # Dump to file
    ET.ElementTree(cfg).write(
            cfgFileName,
            encoding='utf-8',
            pretty_print=True
    )

    # Return a re-parsed version of the dumped config
    return getConfig(cfgFileName)
