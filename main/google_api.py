from google.cloud import videointelligence_v1p2beta1 as videointelligence
from google.cloud import speech_v1
from django.conf import settings


from .util import sec2time


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


def get_timestamp_stt_result(response):
    for result in response.results:
        for alternative in result.alternatives:
            for word in alternative.words:
                start_time = sec2time(word.start_time.seconds, word.start_time.nanos / 10 ** 3)
                end_time = sec2time(word.end_time.seconds, word.end_time.nanos / 10 ** 3)
                yield (word.word, start_time, end_time)


def recognize_by_google_ocr(video):
    storage_uri = f'gs://{settings.GS_BUCKET_NAME}/{video.name}'
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.TEXT_DETECTION]

    operation = video_client.annotate_video(
        input_uri=storage_uri,
        features=features
    )
    result = operation.result()
    return result


def get_timestamp_ocr_result(result):
    annotation_result = result.annotation_results[0]

    for text_annotation in annotation_result.text_annotations:
        text = text_annotation.text
        text_segments = text_annotation.segments
        for text_segment in text_segments:
            start_time_offset = text_segment.segment.start_time_offset
            end_time_offset = text_segment.segment.end_time_offset
            start_time = sec2time(start_time_offset.seconds,
                                  start_time_offset.nanos / (10**3))
            end_time = sec2time(end_time_offset.seconds,
                                  end_time_offset.nanos / (10**3))

            frame = text_segment.frames[0]
            vertices = frame.rotated_bounding_box.vertices
            topleft = vertices[0]
            bottomright = vertices[2]
            yield (text, start_time, end_time, topleft, bottomright)


