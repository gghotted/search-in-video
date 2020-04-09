from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.files import File
from google.cloud import speech_v1
from datetime import time
from pytube import YouTube
import os
import tempfile


def recognize_by_google_stt(audio):
    print('함수 진입')
    
    print(audio.name)
    storage_uri = f'gs://{settings.GS_BUCKET_NAME}/{audio.name}'
    client = speech_v1.SpeechClient()
    config = {
        "enable_word_time_offsets": True,
        "audio_channel_count": 2,
        "language_code": 'ko-KR',
    }
    audio = {"uri": storage_uri}
    print('operation start')
    operation = client.long_running_recognize(config, audio)
    print(f'인식 시작, uri:{storage_uri}')
    result = operation.result()
    print('인식 끝')

    return result


def get_timestamp(response):
    for result in response.results:
        for alternative in result.alternatives:
            for word in alternative.words:
                start_time = sec2time(word.start_time.seconds, word.start_time.nanos / 10 ** 3)
                end_time = sec2time(word.end_time.seconds, word.end_time.nanos / 10 ** 3)
                yield (word.word, start_time, end_time)


def sec2time(sec, micro_sec):
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return time(h, m, s, int(micro_sec))


def load_as_tempfile(file):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        for chunk in file.chunks():
            f.write(chunk)
    return f.name