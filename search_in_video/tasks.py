from server.celery import app

from .models import Video


@app.task
def abstract_words_process(video_id, videofile_path):
    video = Video.objects.get(id=video_id)

    video.synchronize_state('영상 업로드중..')
    video.set_videofile(videofile_path)
    video.set_audio()

    video.synchronize_state('단어 추출중(audio)..')
    video.create_words_by_audio()

    video.synchronize_state('단어 추출중(video)..')
    video.create_words_by_video()

    video.synchronize_state('완료')

