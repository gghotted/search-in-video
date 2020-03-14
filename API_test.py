from google.cloud import speech_v1
import pickle
from google.cloud.speech_v1 import enums

def sample_long_running_recognize(storage_uri):
    """
    Transcribe long audio file from Cloud Storage using asynchronous speech
    recognition

    Args:
      storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
    """

    client = speech_v1.SpeechClient()

    # storage_uri = 'gs://cloud-samples-data/speech/brooklyn_bridge.raw'

    # Sample rate in Hertz of the audio data sent
    #sample_rate_hertz = 44100

    # The language of the supplied audio
    language_code = "ko-KR"

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    #encoding = enums.RecognitionConfig.AudioEncoding.FLAC

    audio_channel_count = 2

    enable_separate_recognition_per_channel = False

    enable_word_time_offsets = True

    config = {
        "enable_word_time_offsets": enable_word_time_offsets,
        "audio_channel_count": audio_channel_count,
        #"enable_separate_recognition_per_channel": enable_separate_recognition_per_channel,
        #"sample_rate_hertz": sample_rate_hertz,
        "language_code": language_code,
        #"encoding": encoding,
    }
    audio = {"uri": storage_uri}

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for operation to complete...")
    response = operation.result()
    print(response)
    with open('api_response/cnn_1min2.txt', 'wb') as make_file:
        pickle.dump(response, make_file)

    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))


if __name__ == '__main__':
    uri = 'gs://stt_video_storage/cnn_1min.wav'
    sample_long_running_recognize(uri)
