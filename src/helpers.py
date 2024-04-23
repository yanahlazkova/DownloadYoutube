""" class for helper methods """
from random import choice
from widgets import widgets
from customtkinter import CTk, get_appearance_mode
import re
from tkinter.messagebox import showerror, showinfo
from data.translate import translations as translate
import winreg


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
        # appearance_mode = get_appearance_mode()
        # fg_color = "#2FA572" if appearance_mode == "Dark" else "#3B8ED0"
        if widget == widgets["Combobox_language"]:
            widget.configure(state=("normal" if state_button else "disabled"),
                             button_color=(("#3B8ED0", "#2FA572") if state_button else "gray"),
                             border_color=(("#3B8ED0", "#2FA572") if state_button else "gray"))
        else:
            widget.configure(state=("normal" if state_button else "disabled"),
                             fg_color=(("#3B8ED0", "#2FA572") if state_button else "gray"))

    @staticmethod
    def center_window(app, app_width, app_height):
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
    def select_widgets_translation(language):
        """ перебор виджетов и элементов перевода """
        return {key: translate[language][key] for key in translate[language].keys() & widgets.keys()}

    @staticmethod
    def sanitize_file_name(file_name: str):
        """ проверяет каждый символ в имени файла на его допустимость
        и заменяет недопустимые символы на '_' """
        # Список недопустимых символов в именах файлов для Windows
        invalid_chars = r'<>:"/\|?*\x00'

        # Заменяем все недопустимые символы на *
        sanitized_file_name = re.sub('[' + re.escape(invalid_chars) + ']', '_', file_name)

        return sanitized_file_name

    @staticmethod
    def find_browser_registry(browser_name):
        """ ищет путь к исполняемому файлу для указанного браузера в реестре Windows """
        # Словарь с путями к ключам реестра для разных браузеров
        browser_registry_paths = {
            "Chrome": r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe",
            "Firefox": r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\firefox.exe",
            "Edge": r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe",
            "Opera": r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\opera.exe"
        }

        try:
            # Открываем соответствующий ключ реестра
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, browser_registry_paths[browser_name]) as key:
                # Получаем значение из ключа
                value, _ = winreg.QueryValueEx(key, "")
                return value
        except FileNotFoundError:
            return None

    @staticmethod
    def show_info_window():
        showinfo("Code copied...", "The code will be copied.\nTo insert it press the keys <Ctrl + C>")
