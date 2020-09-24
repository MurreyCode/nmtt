from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
import mutagen.id3
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER

import glob


def get_artist_track(path):
    return path.split('/')[-1].split('.')[0].split('-')


def get_remixer(name):
    arranger = name.translate({ord(i): None for i in ['Remix', '(', ')']}).rstrip()
    track = name.split('(').rstrip()
    return track, arranger


if __name__ == '__main__':

    mp3_files = glob.glob('/Users/pablo/Music/Pending/*.mp3')
    track_path = mp3_files[0]
    artist_name, track_name = get_artist_track(track_path)
    clean_track, remixer = get_remixer(track_name) if 'Remix' in track_name else None

    print('Artist:', artist_name)
    print('Track:', track_name)
    meta = {
        'title': [track_name],
        'artist': [artist_name],
        'arranger': [remixer]
    }

    mp3file = MP3(track_path, ID3=EasyID3)
    # what is contained in the existing ID3 tags?
    print(mp3file)

