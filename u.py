import os


def get_mp3_files_in_dir(dir):
    files = os.listdir(dir)
    # take only mp3 files
    files = list(filter(lambda file: (str(file).endswith('.mp3')), files))
    # take only files with a valid name (timestamp)
    files = list(filter(lambda file: (str(file).replace('.mp3', '')).isdigit(), files))
    if len(files) == 0:
        return ''

    # convert to a numbers list and get the oldest one
    oldest_file = min(list(map(lambda file: int(str(file).replace('.mp3', '')), files)))
    return f'{dir}/{oldest_file}.mp3'
