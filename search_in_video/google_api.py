from google.cloud import videointelligence_v1p2beta1 as videointelligence
from django.conf import settings

# test   
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


def recognize_by_google_ocr(video):
    storage_uri = f'gs://{settings.GS_BUCKET_NAME}/{video.name}'
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.TEXT_DETECTION]

    operation = video_client.annotate_video(
        input_uri=storage_uri,
        features=features
    )
    print('\nProcessing video for text detection.')
    result = operation.result(timeout=300)

    # The first result is retrieved because a single video was processed.
    annotation_result = result.annotation_results[0]

    # Get only the first result
    text_annotation = annotation_result.text_annotations[0]
    print('\nText: {}'.format(text_annotation.text))

    # Get the first text segment
    text_segment = text_annotation.segments[0]
    start_time = text_segment.segment.start_time_offset
    end_time = text_segment.segment.end_time_offset
    print('start_time: {}, end_time: {}'.format(
        start_time.seconds + start_time.nanos * 1e-9,
        end_time.seconds + end_time.nanos * 1e-9))

    print('Confidence: {}'.format(text_segment.confidence))

    # Show the result for the first frame in this segment.
    frame = text_segment.frames[0]
    time_offset = frame.time_offset
    print('Time offset for the first frame: {}'.format(
        time_offset.seconds + time_offset.nanos * 1e-9))
    print('Rotated Bounding Box Vertices:')
    for vertex in frame.rotated_bounding_box.vertices:
        print('\tVertex.x: {}, Vertex.y: {}'.format(vertex.x, vertex.y))
