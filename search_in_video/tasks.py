from server.celery import app

from .models import Video


@app.task
def abstract_words_process(video_id, videofile_path):
    video = Video.objects.get(id=video_id)
    video.set_videofile(videofile_path)
    video.set_audio()
    video.save()

    video.create_words()

