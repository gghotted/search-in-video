from pytube import YouTube
from pytube import request
import tempfile
import os


class MyYoutube(YouTube):
    def download_best_video(self, download_path=None, filename=None, tempfile=False):
        if filename:
            filename, _ = os.path.splitext(filename)
        video = self.get_best_video()

        if tempfile == True:
            filepath = self.download_as_temp(video)
            return filepath
        else:
            filepath = video.download(download_path, filename)
            return filepath


    def get_best_video(self):
        video = self.streams \
                .filter(progressive=True, file_extension='mp4') \
                .order_by('resolution').desc().first()
        return video

    
    def download_as_temp(self, video):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            for chunk in request.stream(video.url):
                f.write(chunk)
        return f.name
