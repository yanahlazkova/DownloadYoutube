import io
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

#
innertube.InnerTube.fetch_bearer_token = fetchBearerToken.fetch_bearer_token


#
#
class Downloader:
    """ download video, display video data, display progressbar """

    # поиграться с виджетами, может они нагружают систему
    def __init__(self, widgets, url_video, current_lang, file_name):
        self.widgets = widgets
        self.url_video = url_video  # ссылка на видео
        # self.video_data = None
        # self.yt = None
        # self.streams = None  # для загрузки видео
        # self.access_video = False  # доступ к видео
        # self.access_video_download = True  # доступ к загрузке видео
        # self.auth_user = False  # пользователь аутентифицирован
        self.file_name = file_name  # имя файла для сохранения
        self.is_download = ""
        self.path_file = "videos"  # путь к папке для загрузки виедо
        self.current_language = current_lang  # текущий язык приложения

    #     def get_video_data(self):
    #         """ Method to download the video data
    #             Для получения данных о видео нужно: video_data
    #             - запустить аутентификацию пользователя (модульное окно):
    #                 - если аутентификация НЕ прошла успешно (пользователь не аутентифицирован или закрыл окно),
    #                   вывести сообщение "Нужна аутентификация"
    #             - если аутентификация прошла УСПЕШНО:
    #                 - получить данные о видео
    #                 - проверить доступно ли видео для загрузки
    #                 - вывести данные о видео
    #         """
    #         print("get video data")
    #         # проверка доступа к видео
    #         # self.access_video = self.authentication_youtube()
    #         self.access_video = self.get_access_video()
    #         # self.auth_user = fetchBearerToken.fetch_bearer_token()
    #         if self.access_video:
    #             # проверка доступа к загрузке
    #             self.access_video_download = self.check_access_download()
    #
    #             # получаем данные
    #             try:
    #                 self.file_name = self.yt.title
    #                 self.video_data = {"title": self.file_name, "author": self.yt.author, "image": self.yt.thumbnail_url,
    #                               "access": self.access_video_download}
    #             except Exception as e:
    #                 showerror("Error..", f"YouTube link is invalid\n({e})")
    #
    #             self.show_data_video()
    #
    #     def check_access_download(self):
    #         try:
    #             self.streams = self.yt.streams
    #             print("Видео доступно для загрузки")
    #             return True
    #         except Exception as e:
    #             self.widgets["text_info"].configure(text=translation[self.current_language]["text_info"],
    #                                                 text_color="red")
    #             self.widgets["text_info"].grid(row=0, column=0, pady=10, padx=20)
    #
    #             print("Видео недоступно для загрузки", e)
    #             return False
    #
    #     def get_access_video(self):
    #         """ подключение к виедо-данным """
    #         try:
    #             self.yt = YouTube(self.url_video,
    #                               on_progress_callback=self.on_progress,
    #                               on_complete_callback=self.on_complete,
    # )
    #             print("Видео доступно.")
    #             return True
    #         except VideoUnavailable as e:
    #             self.widgets["text_info"].configure(text=translation[self.current_language]["text_info"],
    #                                                 text_color="red")
    #             self.widgets["text_info"].grid(row=0, column=0, pady=10, padx=20)
    #             print("Видео недоступно.", e)
    #             return False
    #         except PytubeError as e:
    #             print("Произошла ошибка Pytube:", e)
    #             return False
    #         except Exception as e:
    #             print("Произошла ошибка authentication:", e)
    #             return False
    #
    #     def show_data_video(self):
    #         """Display video data."""
    #         title = self.video_data["title"]
    #         author = self.video_data["author"]
    #         image_url = self.video_data["image"]
    #
    #         converted_text = Helpers.split_text_by_width(widget=widgets['video_name'], text=title)
    #         self.widgets["video_name"].configure(text=converted_text)
    #
    #         converted_text = Helpers.split_text_by_width(widget=widgets['video_author'], text=author)
    #         self.widgets["video_author"].configure(text=converted_text)
    #
    #         response = get(image_url)
    #         image_data = Image.open(BytesIO(response.content))
    #         image = CTkImage(image_data, size=(220, 150))
    #         image.image = image_data
    #         self.widgets["video_image"].configure(image=image)
    #         self.widgets["video_image"].grid(row=2, column=1, padx=5, pady=10, sticky="n")  # , columnspan=4)
    #
    #         # Установить видимость кнопки Download(disable / normal)
    #         Helpers.set_button_state(self.widgets["button_download"], self.video_data["access"])

    def start_download_thread(self):
        # аутентификаXция для получения доступа к данным
        print("start_download")
        """Starts the download video process in a separate thread."""
        download_thread = Thread(target=self.download_video)
        download_thread.start()
        # self.auth_user = self.authentication_youtube()
        # check_auth_user = self.check_auth(self.url_video)
        # print("auth_user", self.auth_user)
        # if self.auth_user:
        #
        # else:
        #     showinfo("No authentication", "Необходимо аутентифицироваться")
        #     return

    # def download_video_thread(self):
    #     """Method to download the video in a separate thread."""
    #     if self.access_video_download:
    #         self.download_video()
    #         return True
    #     else:
    #         showerror("Error...", "Video is not available for download")

    def download_video(self):
        print("auth...")
        video_name = self.check_video_exists()
        self.path_file = self.widgets["path_file"].cget("text")

        try:
            self.is_download = YouTube(self.url_video,
                                       on_progress_callback=self.on_progress,
                                       on_complete_callback=self.on_complete,
                                       use_oauth=True,
                                       allow_oauth_cache=True).streams.get_highest_resolution().download(self.path_file,
                                                                                                         skip_existing=False,
                                                                                                         filename=f"{video_name}.mp4")
            self.show_path_to_file()

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
        # print("download video", self.auth_user)

        # try:
        #
        # except VideoUnavailable as e:
        #     showerror("Error...", "Video url is unavaialable" + str(e))
        # except Exception as e:
        #     showerror("Error...", f"Failed to upload video: {e}")
        # if self.auth_user:
        #             else:
        #     print("необходимо пойти аутентификацию")

    # def authentication_youtube(self):
    #     print(self.url_video)
    #     print("auth...")
    #
    #     try:
    #         self.yt = YouTube(self.url_video,
    #                           on_progress_callback=self.on_progress,
    #                           on_complete_callback=self.on_complete,
    #                           use_oauth=True, allow_oauth_cache=True
    #                           )
    #         # print("авторизация", self.yt.check_availability())
    #         print("Видео доступно.")
    #         return True
    #     except VideoUnavailable as e:
    #         self.widgets["text_info"].configure(text=translation[self.current_language]["text_info"],
    #                                             text_color="red")
    #         self.widgets["text_info"].grid(row=0, column=0, pady=10, padx=20)
    #         print("Видео недоступно.", e)
    #         return False
    #     except PytubeError as e:
    #         print("Произошла ошибка Pytube:", e)
    #         return False
    #     except Exception as e:
    #         print("Произошла ошибка authentication:", e)
    #         return False

    # @staticmethod
    # def check_auth(url):
    #     """Check if the user has successfully authenticated."""
    #     print("check auth")
    #     url = 'https://www.googleapis.com/youtube/v3/channels'
    #     access_token = fetchBearerToken.access_token
    #     headers = {'Authorization': f'Bearer {access_token}'}
    #     params = {'part': 'snippet', 'mine': 'true'}
    #
    #     response = get(url, headers=headers, params=params)
    #
    #     if response.status_code == 200:
    #         # Аутентификация успешна
    #         print("Authentication successful!")
    #         return True
    #     else:
    #         # В случае неудачи можно вывести статус код и сообщение об ошибке
    #         print(f"Authentication failed. Status code: {response.status_code}, Error: {response.text}")
    #         return False

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
        print(self.file_name)
        count = 0
        new_file_name = file_name = Helpers.sanitize_file_name(self.file_name)
        print("file_name", new_file_name)
        while path.exists(path.join(self.path_file, new_file_name + ".mp4")):
            count += 1
            new_file_name = f"{file_name} ({count})"
            print(new_file_name)
        return new_file_name
