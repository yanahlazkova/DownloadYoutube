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
from requests import get, request
from customtkinter import CTkImage
from data.translate import translations as translation
import fetchBearerToken

innertube.InnerTube.fetch_bearer_token = fetchBearerToken.fetch_bearer_token


class DownloaderData:
    """ download video, display video data, display progressbar """
# поиграться с виджетами, может они нагружают систему
    def __init__(self, widgets, url_video, current_lang):
        self.widgets = widgets
        self.url_video = url_video # ссылка на видео
        self.video_data = None
        self.yt = None
        self.streams = None # для загрузки видео
        self.access_video = False # доступ к видео
        self.access_video_download = False # доступ к загрузке видео
        self.auth_user = False # пользователь аутентифицирован
        self.file_name = "" # имя файла для сохранения
        self.is_download = ""
        self.path_file = "videos" # путь к папке для загрузки виедо
        self.current_language = current_lang # текущий язык приложения


    def get_file_name(self):
        return self.file_name
    def get_video_data(self):
        """ Method to download the video data """
        print("get video data")
        # проверка доступа к видео
        # self.access_video = self.authentication_youtube()
        self.access_video = self.get_access_video()
        # self.auth_user = fetchBearerToken.fetch_bearer_token()
        if self.access_video:
            # проверка доступа к загрузке
            self.access_video_download = self.check_access_download()

            # получаем данные
            try:
                self.file_name = self.yt.title
                self.video_data = {"title": self.file_name, "author": self.yt.author, "image": self.yt.thumbnail_url,
                              "access": self.access_video_download}
                # return self.file_name
            except Exception as e:
                showerror("Error..", f"YouTube link is invalid\n({e})")

            self.show_data_video()

    def check_access_download(self):
        try:
            self.streams = self.yt.streams
            print("Видео доступно для загрузки")
            return True
        except Exception as e:
            self.widgets["text_info"].configure(text=translation[self.current_language]["text_info"],
                                                text_color="red")
            self.widgets["text_info"].grid(row=0, column=0, pady=10, padx=20)

            print("Видео недоступно для загрузки", e)
            return False

    def get_access_video(self):
        """ подключение к виедо-данным """
        try:
            self.yt = YouTube(self.url_video)
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

    def show_data_video(self):
        """Display video data."""
        title = self.video_data["title"]
        author = self.video_data["author"]
        image_url = self.video_data["image"]

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
        Helpers.set_button_state(self.widgets["button_download"], self.video_data["access"])

        return title
