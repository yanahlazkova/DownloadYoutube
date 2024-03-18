import os.path
from os import path
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, PytubeError
from tkinter.messagebox import showinfo, showerror


# import threading


class Downloader:
    """ download video, display video data """
    url_video = ""
    widgets = {}
    yt = None
    access = True
    file_name = ""
    path_file = "videos"

    # to review: it seems like too complicated logic for a simple constuctor
    # check, if you really need it
    def __init__(self, widgets):  # progressbar, percentage):
        self.widgets = widgets
        # self.progressbar = self.widgets["Progressbar"]
        # self.label_percentage = self.widgets["Labels"]["percentage_label"]

    def check_video_availability(self):

        self.url_video = self.widgets["Combobox_url"].get()
        print(self.url_video)
        try:
            self.yt = YouTube(self.url_video,
                              on_progress_callback=self.on_progress,
                              on_complete_callback=self.on_complete)  # , use_oauth=True, allow_oauth_cache=True)
            self.stream = self.yt.streams

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
            showerror("Error..", "YouTube link is invalid")
            # return None

    def download_video(self):
        """ Проверим сколько файлов уже загружено с таким названием"""
        video_name = self.check_video_exists()
        try:
            stream = self.yt.streams.get_highest_resolution()
            is_download = stream.download("videos", skip_existing=False, filename=f"{video_name}.mp4")
            return is_download
        except VideoUnavailable as e:
            showerror("Error...", "Video url is unavaialable" + str(e))
        except Exception as e:
            showerror("Error...", f"Failed to upload video: {e}")

    # todo: you progress bar is not filled correctly, see videos 1 and 3
    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        print("%: ", percentage)
        self.widgets["Labels"]["percentage_label"].configure(text=f"Downloaded: {percentage: .2f} %")
        self.widgets["Labels"]["percentage_label"].update()
        self.widgets["Progressbar"].set(percentage / 100)

    # @staticmethod
    def on_complete(self, stream, path_file):
        showinfo("Downloaded", "Download is completed")
        self.path_file = path.dirname(path_file)
        print("path: ", self.path_file)

    def check_video_exists(self):
        """ checking if the file exists """
        count = 0
        new_file_name = self.file_name
        print("file_name", new_file_name)
        while os.path.exists(os.path.join(self.path_file, new_file_name + ".mp4")):
            count += 1
            new_file_name = f"{self.file_name} ({count})"
            print(new_file_name)
        return new_file_name
