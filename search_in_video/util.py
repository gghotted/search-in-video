from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.files import File
from google.cloud import speech_v1
from datetime import time
from pytube import YouTube
import os


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(self.location, name))
        return name


def recognize_by_google_stt(filename):
    print('함수 진입')
    print(filename)
    storage_uri = f'gs://{settings.GS_BUCKET_NAME}/{filename}'
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


def get_timestamp(response):
    for result in response.results:
        for alternative in result.alternatives:
            for word in alternative.words:
                start_time = sec2time(word.start_time.seconds, word.start_time.nanos / 10 ** 3)
                end_time = sec2time(word.end_time.seconds, word.end_time.nanos / 10 ** 3)
                yield (word.word, start_time, end_time)


def sec2time(sec, micro_sec):
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return time(h, m, s, int(micro_sec))


def youtube_download(url, download_path, filename):
    yt = YouTube(url)
    video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    print(video, '다운로드 시작')
    video.download(download_path, filename=filename)
    print('다운로드 완료')
    video_file = File(open('tmp/tmp.mp4', 'rb'))
    return video_file


class VideoFileSaveManger:
    def __init__(self, save_path):
        self.vf_saver = VideoFileSaver(save_path)


    def save_by_source_type(self, source_type,
                            video_file=None, youtube_link=None):
        if source_type == 'user-pc':
            self.vf_saver.save_video_file(video_file)
        
        if source_type == 'youtube-link':
            self.vf_saver.save_video_file_by_youtube_link(youtube_link)


class VideoFileSaver:
    DEFAULT_FILENAME = 'tmp.mp4'

    def __init__(self, save_path):
        self.save_path = save_path

    
    def save_video_file(self, video_file, filename=DEFAULT_FILENAME):
        os = OverwriteStorage(self.save_path)
        os.save(filename, video_file)


    def save_video_file_by_youtube_link(self, youtube_link, filename=DEFAULT_FILENAME):
        downloader = YouTubeDownloader(youtube_link)
        downloader.download_best_video(self.save_path, filename)


class YouTubeDownloader:
    def __init__(self, url):
        self.youtube = YouTube(url)


    def download_best_video(self, download_path, filename):
        filename = self.delete_extension(filename)
        video = self.get_best_video()
        video.download(download_path, filename)


    def get_best_video(self):
        video = self.youtube.streams \
                .filter(progressive=True, file_extension='mp4') \
                .order_by('resolution').desc().first()
        return video


    def delete_extension(self, filename):
        return filename.split('.')[0]