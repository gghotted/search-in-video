from server.celery import app

from django.core.files import File

from .models import Video, Word
from .util import youtube_download, recognize_by_google_stt, get_timestamp

# import moviepy.editor as mp

@app.task
def plus(x, y):
    return x + y


@app.task
def recognize_video_process(video_id):
    # video = Video.objects.get(id=video_id)
    #
    # # save video file
    # if video.source_type == 'user-pc':
    #     video_file = File(open('tmp/tmp.mp4', 'rb'))
    # else:
    #     video_file = youtube_download(video.youtube_link, 'tmp/', 'tmp')
    # video_file.name = video.title + '.mp4'
    # video.video = video_file
    #
    # # save audio file
    # mp4 = mp.VideoFileClip('tmp/tmp.mp4')
    # mp4.audio.write_audiofile('tmp/tmp.wav')
    # audio_file = File(open('tmp/tmp.wav', 'rb'))
    # audio_file.name = video.title + '.wav'
    # video.audio = audio_file
    #
    # video.save()
    # print('save 완료')
    # recognize and save words
    response = recognize_by_google_stt('test2.wav')
    # for text, start_at, end_at in get_timestamp(response):
    #     Word(video=video,
    #          text=text,
    #          start_at=start_at,
    #          end_at=end_at).save()

    return
