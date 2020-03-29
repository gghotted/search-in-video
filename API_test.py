from google.cloud import speech_v1
import pickle
from google.cloud.speech_v1 import enums

def sample_long_running_recognize(storage_uri):
    storage_uri = f'gs://{settings.GS_BUCKET_NAME}/{filename}'
    client = speech_v1.SpeechClient()
    config = {
        "enable_word_time_offsets": True,
        "audio_channel_count": 2,
        "language_code": 'ko-KR',
    }
    audio = {"uri": storage_uri}

    operation = client.long_running_recognize(config, audio)
    print(dir(operation))
    print(f'인식 시작, uri:{storage_uri}')
    result = operation.result()
    print('인식 끝')


if __name__ == '__main__':
    uri = 'gs://stt_video_storage/test.wav'
    sample_long_running_recognize(uri)
