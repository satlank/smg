def _sanitizeTitle(title):
    st =''
    for c in title.lower():
        if c.isalnum():
            st += c
        else:
            st += '_'
    return st



def generateScript(release, genres):
    """Creates and returns as string a conversion script."""

    script = ''

    albumtitle = release['title']
    albumdate = release['date']
    albumartist = release['artist-credit-phrase']
    mb_albumid = release['id']

    for medium in release['medium-list']:
        mediumNum = int(medium['position'])
        for track in medium['track-list']:
            trackNum = int(track['number'])
            script += "cdparanoia -B {i}-{i}\n".format(i=trackNum)
            script += "mv track{t:02}.cdda.wav {d:03}track{t:02}.cdda.wav\n".format(d=mediumNum, t=trackNum)

    script += "\n\n"

    totalNum=1
    for medium in release['medium-list']:
        mediumNum = int(medium['position'])
        for track in medium['track-list']:
            trackNum = int(track['number'])
            rec = track['recording']
            trackTitle = rec['title']

            wav = "{:03}track{:02}.cdda.wav".format(mediumNum, trackNum)
            flac = "{:03}-{}.flac".format(
                    totalNum, _sanitizeTitle(trackTitle)
            )

            phrase = 'flac --best -V {} \\\n'.format(wav)
            phrase += '\t--tag=title="{}" \\\n'.format(trackTitle)
            for artist in rec['artist-credit']:
                phrase += '\t--tag=artist="{}" \\\n'.format(artist['artist']['name'])
            phrase += '\t--tag=albumartist="{}" \\\n'.format(albumartist
            )
            phrase += '\t--tag=date="{}" \\\n'.format(albumdate)
            phrase += '\t--tag=album="{}" \\\n'.format(albumtitle)
            for genre in genres:
                phrase += '\t--tag=genre="{}" \\\n'.format(genre)
            phrase += '\t--tag=tracknumber="{:02}" \\\n'.format(trackNum)
            phrase += '\t--tag=discnumber="{:02}" \\\n'.format(mediumNum)
            phrase += '\t--tag=musicbrainz-albumid="{}" \\\n'.format(mb_albumid)
            phrase += '\t-o "{}" \n'.format(flac)
            totalNum+=1

            script += phrase
            script += "\n"

    return script
