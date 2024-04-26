# import io
from os import path, startfile
from pytube import YouTube
from pytube import innertube
from pytube.exceptions import VideoUnavailable, PytubeError
from tkinter import END
from tkinter.messagebox import showinfo, showerror
from threading import Thread
from helpers import *
from PIL import Image
from io import BytesIO
from requests import get
from customtkinter import CTkImage
from data.translate import translations as translation
import fetchBearerToken

innertube.InnerTube.fetch_bearer_token = fetchBearerToken.fetch_bearer_token


class Downloader:
    """ download video, display video data, display progressbar """

    def __init__(self, widgets, app, interface):
        self.current_interface = interface
        self.stream = None
        self.use_oauth = not self.current_interface.auth_user # аутентифиция пользователя
        self.current_app = app
        self.widgets = widgets
        self.url_video = ""
        self.yt = None
        self.access_video = True
        self.file_name = ""
        self.is_download = ""
        self.path_file = "videos"
        self.current_language = self.widgets["Combobox_language"].get()
        self.access_user = self.current_interface.auth_user # пользователь аутентифицирован

    def start_get_data_thread(self):
        """Starts the download video process in a separate thread."""
        print("1 start")
        download_thread = Thread(target=self.get_data_video_thread)
        download_thread.start()

    def get_data_video_thread(self):
        """Method to download the video in a separate thread."""
        print("2 get_thread", self.access_video)
        video_data = self.get_data_video()
        if self.access_user:
            self.show_data_video(video_data)
        # else:
        #     showinfo("Not authenticated", "You need to authenticate")

    def get_data_video(self):
        """ get and pass to modul interface: title, author, image of video """
        print("3 get data")

        self.check_video_availability()
        if not self.access_user:
            return None
        print("Получение названия")
        try:
            self.file_name = self.yt.title
            video_data = {"title": self.file_name, "author": self.yt.author, "image": self.yt.thumbnail_url,
                          "access": self.access_video}
            self.current_interface.auth_user = True
            self.access_user = True
            return video_data

        except Exception as e:
            # showerror("Error..", f"YouTube link is invalid\n({e})")
            self.current_interface.auth_user = False
            self.access_user = False
            showinfo("Not authentication", "Необходимо пройти аутентификацию")
            return None

    def check_video_availability(self):
        """ Проверка, доступно ли видео для загрузки"""
        print("4 check")

        self.url_video = self.widgets["Combobox_url"].get()
        print(self.url_video)
        self.access_user = self.get_youtube_data()

    def get_youtube_data(self):
        try:
            self.yt = YouTube(self.url_video,
                              on_progress_callback=self.on_progress,
                              on_complete_callback=self.on_complete,
                              use_oauth=self.use_oauth, allow_oauth_cache=True
                              )
            if self.use_oauth:
                self.use_oauth = False
                self.current_interface.auth_user = True
            # else:
            #     self.stream = self.yt.streams

            print("Видео доступно.")
            return True
        except VideoUnavailable as e:
            self.widgets["text_info"].configure(text=translation[self.current_language]["text_info"],
                                                text_color="red")
            self.widgets["text_info"].grid(row=0, column=0, pady=10, padx=20)
            print("Видео недоступно.", e)
            return False
        except PytubeError as e:
            print("Произошла ошибка Pytube:", e)
            return False
        except Exception as e:
            print("Произошла ошибка authentication:", e)
            return False

    def show_data_video(self, data_video):
        """Display video data."""
        title = data_video["title"]
        author = data_video["author"]
        image_url = data_video["image"]

        converted_text = Helpers.split_text_by_width(widget=widgets['video_name'], text=title)
        self.widgets["video_name"].configure(text=converted_text)

        converted_text = Helpers.split_text_by_width(widget=widgets['video_author'], text=author)
        self.widgets["video_author"].configure(text=converted_text)

        response = get(image_url)
        image_data = Image.open(BytesIO(response.content))
        image = CTkImage(image_data, size=(220, 150))
        image.image = image_data
        self.widgets["video_image"].configure(image=image)
        self.widgets["video_image"].grid(row=2, column=1, padx=5, pady=10, sticky="n")  # , columnspan=4)


        # Установить видимость кнопки Download(disable / normal)
        Helpers.set_button_state(self.widgets["button_download"], data_video["access"])

    def start_download_thread(self, auth_user):
        """Starts the download video process in a separate thread."""
        download_thread = Thread(target=self.download_video_thread)
        download_thread.start()

    def download_video_thread(self):
        """Method to download the video in a separate thread."""
        if self.access_video:
            self.download_video()
            return True
        else:
            showerror("Error...", "Video is not available for download")

    def download_video(self):

        video_name = self.check_video_exists()
        self.get_youtube_data()
        try:
            self.stream = self.yt.streams.get_highest_resolution()
            self.path_file = self.widgets["path_file"].cget("text")
            self.is_download = self.stream.download(self.path_file, skip_existing=False, filename=f"{video_name}.mp4")

            self.show_path_to_file()
        except VideoUnavailable as e:
            showinfo("No download...", "Видео не доступно для загузки\n" + str(e))
        except Exception as e:
            showerror("Error...", f"Failed to upload video: {e}")

    def on_progress(self, stream, _, bytes_remaining):
        """ Вывод прогрессбар при загрузке файла """
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage = (bytes_downloaded / total_size) * 100
        self.widgets["percentage_label"].after(0, lambda: self.update_progressbar(percentage))

    def update_progressbar(self, percentage):
        count_point = choice([3, 4])
        text_download = translation[self.current_language]["Loading_progress"] + ("." * count_point)
        self.widgets["percentage_label"].configure(text=f"{text_download}\n {percentage: .2f} %")

        self.widgets["Progressbar"].set(percentage / 100)

    def on_complete(self, stream, path_file):
        showinfo("Downloaded", "Download is completed")
        self.widgets["percentage_label"].configure(text=translation[self.current_language]["Video_downloaded"])
        self.widgets["frame_path_download"].grid(row=3, column=0, padx=10, sticky="we")
        self.widgets["path_text"].configure(text=translation[self.current_language]["Open_folder"])
        # Установить state кнопки Download (disable/normal)
        Helpers.set_button_state(self.widgets["button_download"], True)
        # Разрешить смену языка
        # self.widgets["Combobox_language"].configure(state="normal")
        Helpers.set_button_state(self.widgets["Combobox_language"], True)
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
        try:
            startfile(path.dirname(self.is_download))
        except Exception as e:
            print("Ошибка при открытии папки:", e)

    def check_video_exists(self):
        """ checking if the file exists
        to add number at the end of the file"""
        count = 0
        new_file_name = file_name = Helpers.sanitize_file_name(self.file_name)
        print("file_name", new_file_name)
        while path.exists(path.join(self.path_file, new_file_name + ".mp4")):
            count += 1
            new_file_name = f"{file_name} ({count})"
            print(new_file_name)
        return new_file_name