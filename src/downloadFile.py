import os.path
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, PytubeError
from tkinter.messagebox import showinfo, showerror


# import threading
class Downloader:
    """ download video, display video data, display progressbar """
    url_video = ""
    widgets = {}
    yt = None
    access = True
    file_name = ""
    path_file = "videos"

    def __init__(self, widgets):
        self.widgets = widgets

    def check_video_availability(self):
        """ Проверка, доступно ли видео для загрузки"""
        self.url_video = self.widgets["Combobox_url"].get()
        print(self.url_video)
        try:
            self.yt = YouTube(self.url_video,
                              on_progress_callback=self.on_progress,
                              on_complete_callback=self.on_complete,
                              # use_oauth=True, allow_oauth_cache=True
                              )
            self.streams = self.yt.streams

            print("Видео доступно.")
            return True
        except VideoUnavailable as e:
            showinfo("Access...", f"Video not available for download\n({e})")
            print("Видео недоступно.", e)
            return False
        except PytubeError as e:
            print("Произошла ошибка Pytube:", e)
            return False
        except Exception as e:
            print("Произошла ошибка:", e)
            return False

    def get_data_video(self):
        """ get and pass to modul interface: title, author, image of video """
        self.access = self.check_video_availability()
        print("Url: ", self.url_video)

        try:
            self.file_name = self.yt.title
            video_data = {"title": self.file_name, "author": self.yt.author, "image": self.yt.thumbnail_url,
                          "access": self.access}
            return video_data

        except Exception as e:
            showerror("Error..", f"YouTube link is invalid\n({e})")
            # return None

    def download_video(self):
        """ Проверим существует ли файл с таким названием,
         если да, добавляет номер в конеце имени файла """

        video_name = self.check_video_exists()
        try:
            stream = self.streams.get_highest_resolution()
            is_download = stream.download("videos", skip_existing=False, filename=f"{video_name}.mp4")
            return is_download
        except VideoUnavailable as e:
            showerror("Error...", "Video url is unavaialable" + str(e))
        except Exception as e:
            showerror("Error...", f"Failed to upload video: {e}")

    def on_progress(self, stream, chunk, bytes_remaining):
        """ Вывод прогрессбар при загрузке файла """
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        print("%: ", percentage)
        self.widgets["Labels"]["percentage_label"].configure(text=f"Downloaded: {percentage: .2f} %")
        self.widgets["Labels"]["percentage_label"].update()
        self.widgets["Progressbar"].set(percentage / 100)

    def on_complete(self, stream, path_file):
        showinfo("Downloaded", "Download is completed")
        self.path_file = os.path.dirname(path_file)
        print("path: ", self.path_file)

    def check_video_exists(self):
        """ checking if the file exists
        if file exists, to add number at the end of the file"""
        count = 0
        new_file_name = self.file_name
        print("file_name", new_file_name)
        while os.path.exists(os.path.join(self.path_file, new_file_name + ".mp4")):
            count += 1
            new_file_name = f"{self.file_name} ({count})"
            print(new_file_name)
        return new_file_name
