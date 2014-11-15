import musicbrainzngs as m

_initialised = False


def _initialise():
    """Internal function to initialise the MusicBrainz library."""
    import smg.version as v
    m.set_useragent(v._NAME, v._VERSION, v._CONTACT)
    _initialised = True


def getReleaseFromMB(releaseId):
    """Retrieves release info from MusicBrainz by releaseId."""

    if not _initialised:
        _initialise()

    release = m.get_release_by_id(
            releaseId,
            includes=["recordings", "artists", "artist-credits", "artist-rels"]
    )

    return release
