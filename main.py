import sounddevice
from scipy.io.wavfile import write
from pydub import AudioSegment
import requests
import os
import time
import threading
import u

fps = 44100
duration = 15

wav_save_dir = 'wav_audio_files'
mp3_save_dir = 'mp3_audio_files'


def record_audio():

    # create save dirs if not exists

    if not os.path.exists(wav_save_dir):
        os.makedirs(wav_save_dir)
    if not os.path.exists(mp3_save_dir):
        os.makedirs(mp3_save_dir)

    print('recording...')
    recording = sounddevice.rec(int(duration * fps), fps, 1)
    sounddevice.wait()
    print('Recording done')

    file_name = f'{int(round(time.time() * 1000))}'
    wav_save_path = f'{wav_save_dir}/{file_name}.wav'
    mp3_save_path = f'{mp3_save_dir}/{file_name}.mp3'
    write(wav_save_path, fps, recording)

    sound = AudioSegment.from_wav(wav_save_path)
    sound.export(mp3_save_path, 'mp3')
    os.remove(wav_save_path)


def upload_file(file_path):
    # url = 'http://localhost:3000/api/checkAudio'
    url = 'https://alertix.herokuapp.com/api/checkAudio'
    try:
        with open(file_path, "rb") as a_file:
            file_dict = {"file": a_file}
            response = requests.post(url, files=file_dict)
            print(response.status_code)
            return True
    except:
        print("An exception occurred")
        return False


def upload_files_process():
    while True:
        file_to_upload = u.get_mp3_files_in_dir(mp3_save_dir)
        if file_to_upload == '':
            print('no files to upload... waiting...')
            time.sleep(5)
            continue

        print(f'uploading file: {file_to_upload}')
        upload_success = upload_file(file_to_upload)
        print('done uploading')
        os.remove(file_to_upload)
        time.sleep(1)


t = threading.Thread(target=upload_files_process)
t.start()

while True:
    record_audio()
