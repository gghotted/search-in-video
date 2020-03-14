from django.core.files.storage import FileSystemStorage
from django.conf import settings
from google.cloud import speech_v1
from datetime import time
import os


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(self.location, name))
        return name


def recognize_by_google_stt(filename):
    storage_uri = f'gs://{settings.GS_BUCKET_NAME}/{filename}'
    print(f'인식 시작, uri:{storage_uri}')
    client = speech_v1.SpeechClient()
    config = {
        "enable_word_time_offsets": True,
        "audio_channel_count": 2,
        "language_code": 'ko-KR',
    }
    audio = {"uri": storage_uri}

    operation = client.long_running_recognize(config, audio)
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
