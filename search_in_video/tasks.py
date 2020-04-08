from server.celery import app

from .models import Video
from .youtube import MyYoutube


@app.task
def create_words_process(video_id, videofile_path):
    video = Video.objects.get(id=video_id)
    if videofile_path==None and video.source_type=='youtube-link':
        yt = MyYoutube
        yt.download_best_video()
        videofile_path = yt.downloaded_file.name
    video.save_videofile_by_path(videofile_path)



