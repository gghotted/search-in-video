from pytube import YouTube
import os


class MyYoutube(YouTube):
    def download_best_video(self, download_path, filename):
        filename, _ = os.path.splitext(filename)
        video = self.get_best_video()
        video.download(download_path, filename)


    def get_best_video(self):
        video = self.streams \
                .filter(progressive=True, file_extension='mp4') \
                .order_by('resolution').desc().first()
        return video