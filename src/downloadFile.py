from os import path, startfile
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, PytubeError
from tkinter import END
from tkinter.messagebox import showinfo, showerror
from threading import Thread
from helpers import *
from PIL import Image, ImageTk
from urllib.request import urlopen
from io import BytesIO


class Downloader:
    """ download video, display video data, display progressbar """
    widgets = {}


    def __init__(self, widgets):
        self.widgets = widgets
        self.url_video = ""
        self.yt = None
        self.access = True
        self.file_name = ""
        self.path_file = "videos"
        self.is_download = ""

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
            self.widgets["percentage_label"].configure(text="Video not available for download", text_color="red")
            print("Видео недоступно.", e)
            return False
        except PytubeError as e:
            print("Произошла ошибка Pytube:", e)
            return False
        except Exception as e:
            print("Произошла ошибка:", e)
            return False

    def start_get_data_thread(self):
        """Starts the download video process in a separate thread."""
        download_thread = Thread(target=self.get_data_video_thread)
        download_thread.start()

    def get_data_video_thread(self):
        """Method to download the video in a separate thread."""
        if self.access:
            video_data = self.get_data_video()
            self.show_data_video(video_data)
        else:
            showerror("Error...", "Video is not available for download")

    def show_data_video(self, data_video):
        """Display video data."""
        title = data_video["title"]
        author = data_video["author"]
        image = data_video["image"]

        converted_text = Helpers.split_text_by_width(widget=widgets['video_name'], text=title)
        self.widgets["video_name"].configure(text=converted_text)

        converted_text = Helpers.split_text_by_width(widget=widgets['video_author'], text=author)
        self.widgets["video_author"].configure(text=converted_text)

        response = urlopen(image)
        image_data = response.read()
        image = Image.open(BytesIO(image_data))
        image.thumbnail((250, 250))
        photo_image = ImageTk.PhotoImage(image)

        self.widgets["video_image"].configure(image=photo_image)

        # Установить видимость кнопки Download(disable / normal)
        Helpers.set_button_state(self.widgets["button_download"], data_video["access"])


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

    def start_download_thread(self):
        """Starts the download video process in a separate thread."""
        download_thread = Thread(target=self.download_video_thread)
        download_thread.start()

    def download_video_thread(self):
        """Method to download the video in a separate thread."""
        if self.access:
            self.download_video()
            return True
        else:
            showerror("Error...", "Video is not available for download")

    def download_video(self):
        """ Проверим существует ли файл с таким названием,
         если да, добавим номер в конеце имени файла """
        video_name = self.check_video_exists()
        try:
            stream = self.streams.get_highest_resolution()
            self.is_download = stream.download("videos", skip_existing=False, filename=f"{video_name}.mp4")

            self.show_path_to_file()
        except VideoUnavailable as e:
            showerror("Error...", "Video url is unavaialable" + str(e))
        except Exception as e:
            showerror("Error...", f"Failed to upload video: {e}")

    def on_progress(self, stream, _, bytes_remaining):
        """ Вывод прогрессбар при загрузке файла """
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        print("%: ", percentage)

        self.widgets["percentage_label"].after(0, lambda: self.update_progressbar(percentage))
        # Установить state кнопки Download (disable/normal)
        Helpers.set_button_state(self.widgets["button_download"], False)

    def update_progressbar(self, percentage):
        count_point = choice([3, 4])
        text_download = "Downloading" + "." * count_point
        self.widgets["percentage_label"].configure(text=f"{text_download}\n {percentage: .2f} %")

        self.widgets["Progressbar"].set(percentage / 100)

    def on_complete(self, stream, path_file):
        showinfo("Downloaded", "Download is completed")
        self.widgets["percentage_label"].configure(text=f"Video downloaded")
        self.widgets["frame_path_download"].grid(row=3, column=0, padx=20, sticky="we")
        self.widgets["path_text"].configure(text="Video downloaded, path to file:")
        # Установить state кнопки Download (disable/normal)
        Helpers.set_button_state(self.widgets["button_download"], True)
        # Скрыть progressbar
        self.widgets["Progressbar"].grid_remove()

    def show_path_to_file(self):
        """ display path to video-file """
        self.widgets["Textbox_path_to_video"].delete("1.0", END)
        self.widgets["Textbox_path_to_video"].insert("1.0", path.dirname(self.is_download))
        self.widgets["Textbox_path_to_video"].bind("<Button-1>", self.open_directory)

    # @staticmethod
    def open_directory(self, event):
        """Открывает папку с загруженным файлом."""
        print(self.is_download)
        try:
            startfile(path.dirname(self.is_download))
        except Exception as e:
            print("Ошибка при открытии папки:", e)

    def check_video_exists(self):
        """ checking if the file exists
        to add number at the end of the file"""
        count = 0
        new_file_name = self.file_name
        print("file_name", new_file_name)
        while path.exists(path.join(self.path_file, new_file_name + ".mp4")):
            count += 1
            new_file_name = f"{self.file_name} ({count})"
            print(new_file_name)
        return new_file_name
