""" class for helper methods """
from random import randrange, choice
from widgets import widgets
from customtkinter import CTk
import re
from tkinter.messagebox import showerror

class Helpers:
    @staticmethod
    def split_text_by_width(widget, text: str):
        """ конвертация текста для отображения в несколько строк """
        font = widget.cget("font")
        width = widget.cget("width")
        lines = []
        current_line = ""
        for word in text.split():
            test_line = current_line + word + " "
            if font.measure(test_line) <= width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        lines.append(current_line.strip())
        return "\n".join(lines)

    @staticmethod
    def set_button_state(widget: widgets, state_button: bool):
        """ function set state of button disabled/normal
        False - disabled, True - normal """
        widget.configure(state=("normal" if state_button else "disabled"),
                         fg_color=("green" if state_button else "gray"))

    @staticmethod
    def center_window(app: CTk, app_width: int, app_height: int):
        """ centering app window """
        screen_width = app.winfo_screenwidth()
        screen_height = app.winfo_screenheight()

        x = (screen_width - app_width) // 2
        y = (screen_height - app_height) // 2

        app.geometry(f"{app_width}x{app_height}+{x}+{y}")

        # makes the window non-resizable
        app.resizable(height=False, width=False)

    @staticmethod
    def is_youtube_url(url_video):
        # Регулярное выражение для проверки ссылок YouTube
        youtube_regex = (
            r'(https?://)?(www\.)?'
            r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
            r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
            r'([^&=\s%]*\?[^&=\s%]*=.+)*'
        )

        # Проверка с использованием регулярного выражения
        match = re.match(youtube_regex, url_video)

        # Возвращаем True, если строка соответствует формату ссылки YouTube, и False в противном случае
        return match is not None

    @staticmethod
    def check_link(current_url: str, placeholder: str):
        """ проверка введенных данных в combobox"""
        if current_url == "" or current_url == placeholder or (not Helpers.is_youtube_url(current_url)):
            showerror("Error...", "YouTube link is invalid\n\nEnter correct link.")
            return False
        else:
            return True

    @staticmethod
    def get_random_url(list_video: list):
        """ получение рандомного url """
        random_url = choice(list_video)
        return random_url["url"]
    @staticmethod
    def get_random_number():
        list_point = [2, 3]
        return choice(list_point)
    @staticmethod
    def show_data_video(data_video):
        """  displaying video data  """
        self.show_video_title(data_video["title"])
        self.show_video_author(data_video["author"])
        self.show_video_image(data_video["image"])
        # Установить state кнопки Download(disable / normal)
        Helpers.set_button_state(self.widgets["button_download"], data_video["access"])