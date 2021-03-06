from glob import glob
from os.path import join, dirname
from dotenv import load_dotenv
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3

from src.enrich_meta import enrich_meta


def get_artist_track(path):
    return path.split('/')[-1].split('.')[0].split('-')


def get_remixer(name):
    arranger = name.translate({ord(i): None for i in ['Remix', '(', ')']}).rstrip()
    track = name.split('(').rstrip()
    return track, arranger


def save_meta(path, meta):
    try:
        file = MP3(path, ID3=EasyID3)
        for key, value in meta.items():
            file[key] = value
        print(file)
        file.save()
    except Exception as exception:
        print(exception.__traceback__)


if __name__ == '__main__':

    dotenv_path = join(dirname(__file__), 'configs/.env')
    load_dotenv(dotenv_path)

    mp3_files = glob('/Users/pablo/Music/Pending/*.mp3')
    track_path = mp3_files[0]
    artist_name, track_name = get_artist_track(track_path)

    print('Artist:', artist_name)
    print('Track:', track_name)

    clean_track, remixer = get_remixer(track_name) if 'Remix' in track_name else track_name, None

    metadata = {
        'title': [track_name],
        'artist': [artist_name],
        'arranger': [remixer]
    }

    metadata = enrich_meta(metadata)
    save_meta(track_path, metadata)

    # TODO: Move enriched files from Pending folder to Collection folder
