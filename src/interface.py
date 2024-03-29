import tkinter as tk
from customtkinter import CTk, CTkButton, CTkLabel, CTkProgressBar, CTkFrame, CTkComboBox, CTkTextbox, CTkSwitch, \
    StringVar, set_default_color_theme, set_appearance_mode, CTkRadioButton
from helpers import Helpers
from widgets import widgets
from data.listUrls import list_urls
from downloadFile import Downloader
import data.translate as translation

set_appearance_mode("Dark")
set_default_color_theme("green")


class Interface:
    """ creates interface, place widgets into UI """
    app_width = 0
    app_height = 0
    default_color_theme = "green"
    video_downloaded = ""
    placeholder = ""
    theme = {
        "blue": "./themes/blue.json",
        "dark-blue": "./themes/dark-blue.json"
    }

    downloader = None

    def __init__(self, title: str, width: int, height: int):
        self.app = CTk()
        self.widgets = widgets
        self.app.title(title)
        self.app_width = width
        self.app_height = height
        self.current_url = Helpers.get_random_url(list_urls)
        self.list_language = ["ua", "en", "ru"]
        self.current_language = self.list_language[1]
        self.list_placeholder = {"en": "Enter video link", "ua": "Вкажіть посилання на відео", "ru": "Вставьте ссылку на видео"}
        self.placeholder = self.list_placeholder[self.current_language]
        self.translate = {}

    def create_widgets(self):
        # Block enter url
        self.widgets["frame_link"] = CTkFrame(self.app,
                                              border_color=self.default_color_theme,
                                              border_width=2)

        # Enter url: text, input, button
        self.widgets["text_link"] = CTkLabel(self.widgets["frame_link"], text="URL: ",
                                             text_color=self.default_color_theme, anchor="w")

        urls = [url["url"] for url in list_urls]
        combobox_var = StringVar(value=self.current_url)
        self.widgets["Combobox_url"] = CTkComboBox(
            self.widgets["frame_link"],
            values=urls,
            variable=combobox_var,
            width=250,
            border_color=self.default_color_theme,
            button_color=self.default_color_theme,
            dropdown_hover_color=self.default_color_theme,
            command=lambda current_value: self.get_data_video(current_value)
        )

        # self.widgets["Combobox_url"].configure(command=lambda event: self.get_data_video())
        self.widgets["Combobox_url"].bind("<Return>", lambda event: self.get_data_video(event))
        self.widgets["Combobox_url"].bind("<Button-1>", lambda event: self.clear_variable())
        self.widgets["Combobox_url"].bind("<FocusOut>", lambda event: self.show_placeholder())

        self.widgets["button_Clear"] = CTkButton(self.widgets["frame_link"], text="X",
                                                 width=10,
                                                 command=self.clear_all)
        self.widgets["button_OK"] = CTkButton(
            self.widgets["frame_link"], text="OK", width=10,
            command=lambda: self.get_data_video(self.current_url))

        # Data about video
        self.widgets["frame_data_video"] = CTkFrame(self.app,
                                                    border_color=self.default_color_theme,
                                                    border_width=2)

        self.widgets["text_title"] = CTkLabel(self.widgets["frame_data_video"],
                                              # text="Name: ",
                                              text=translation.translations[self.current_language]["text_title"],
                                              text_color=self.default_color_theme, anchor="w")

        self.widgets["video_name"] = CTkLabel(self.widgets["frame_data_video"],
                                              width=280, text="",
                                              justify="left", anchor="w")

        self.widgets["text_author"] = CTkLabel(self.widgets["frame_data_video"],
                                              text="Autor: ",
                                              text_color=self.default_color_theme, anchor="w")

        self.widgets["video_author"] = CTkLabel(self.widgets["frame_data_video"],
                                                text="", width=280, anchor="w")

        self.widgets["text_image"] = CTkLabel(self.widgets["frame_data_video"],
                                              text="Image: ",
                                              text_color=self.default_color_theme, anchor="w")

        self.widgets["video_image"] = CTkLabel(self.widgets["frame_data_video"],
                                               text="", compound="bottom",
                                               height=150)

        # video download block
        self.widgets["frame_download"] = CTkFrame(self.app,
                                                  border_color=self.default_color_theme,
                                                  border_width=2)

        self.widgets["percentage_label"] = CTkLabel(self.widgets["frame_download"],
                                                    text="Downloaded: 0 %", text_color="white")

        self.widgets["Progressbar"] = CTkProgressBar(self.widgets["frame_download"], width=200,
                                                     height=5)
        self.widgets["Progressbar"].set(0)

        self.widgets["button_download"] = CTkButton(
            self.widgets["frame_download"],
            text="Download",
            fg_color="gray",
            state="disabled",
            command=lambda: self.download_video()
        )

        self.widgets["frame_path_download"] = CTkFrame(
            self.widgets["frame_download"])

        self.widgets["path_text"] = CTkLabel(self.widgets["frame_path_download"],
                                             text="Path to file: ")
        self.widgets["Textbox_path_to_video"] = CTkTextbox(
            self.widgets["frame_path_download"],
            text_color="steelblue1",
            activate_scrollbars=False,
            wrap="word",
            height=55,
            width=335,
            cursor="hand2",
        )

        # widgets by setting colors
        self.widgets["frame_setting_window"] = CTkFrame(self.app,
                                                        border_color=self.default_color_theme,
                                                        border_width=2)
        self.widgets["text_radiobutton"] = CTkLabel(
            self.widgets["frame_setting_window"], text="Select theme: ", text_color=self.default_color_theme,
            anchor="w")

        self.switch_var = StringVar(value="on")
        self.widgets["switch"] = CTkSwitch(self.widgets["frame_setting_window"], text="Light/Dark",
                                           variable=self.switch_var, onvalue="on",
                                           offvalue="off", command=self.set_theme)

        language_var = StringVar(value=self.current_language)
        self.widgets["Combobox_language"] = CTkComboBox(
            self.widgets["frame_setting_window"],
            values=self.list_language,
            variable=language_var,
            width=80,
            border_color=self.default_color_theme,
            button_color=self.default_color_theme,
            dropdown_text_color=self.default_color_theme,
            dropdown_hover_color=self.default_color_theme,
            command=lambda selected_language: self.on_language_change(selected_language))

    def place_widgets(self):
        # widgets by entered url video
        self.app.grid_columnconfigure(0, weight=1)

        self.widgets["frame_link"].grid(row=0, padx=10, pady=10, ipadx=5, ipady=5, sticky="ew")

        self.widgets["text_link"].grid(row=0, column=0, padx=(20, 0), pady=(10, 0), sticky="we")

        self.widgets["Combobox_url"].grid(row=0, column=1, padx=5, pady=(10, 0))

        self.widgets["button_Clear"].grid(row=0, column=2, padx=5, pady=(10, 0))

        self.widgets["button_OK"].grid(row=0, column=3, padx=5, pady=(10, 0))

        # widgets by data about video
        self.widgets["frame_data_video"].grid(row=1, padx=10, pady=10, ipadx=5, ipady=5, sticky="ew")

        self.widgets["frame_data_video"].grid_columnconfigure(0, weight=1)
        self.widgets["frame_data_video"].grid_columnconfigure(1, weight=1)

        # self.widgets["frame_data"].grid(row=0, column=1, rowspan=3, padx=5, pady=5, sticky="nsew")

        self.widgets["text_title"].grid(row=0, column=0, padx=(10, 0), pady=10, sticky="wen")

        self.widgets["video_name"].grid(row=0, column=1, padx=5, pady=10, ipady=5, sticky="ew")

        self.widgets["text_author"].grid(row=1, column=0, padx=(10, 0), pady=10, sticky="nwe")

        self.widgets["video_author"].grid(row=1, column=1, padx=5, pady=10, sticky="w")

        self.widgets["text_image"].grid(row=2, column=0, padx=(10, 0), pady=10, sticky="nwe")

        self.widgets["video_image"].grid(row=2, column=1, padx=5, pady=10, sticky="n")  # , columnspan=4)

        # widgets by download of video
        self.widgets["frame_download"].columnconfigure(0, weight=1)
        self.widgets["frame_download"].grid(row=2, column=0, padx=10, pady=10, ipadx=5, ipady=5, sticky="ew")
        self.widgets["percentage_label"].grid(row=0, column=0, pady=10, padx=20)

        # self.widgets["Progressbar"].grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.widgets["button_download"].grid(row=2, column=0, padx=20, pady=(0, 10))

        self.widgets["path_text"].grid(row=0, column=0, padx=5, sticky="wn")
        self.widgets["Textbox_path_to_video"].grid(row=1, column=0, padx=5, sticky="ew")

        # widgets by setting window
        self.widgets["frame_setting_window"].grid(row=3, column=0, padx=10, pady=10, ipadx=5, ipady=5, sticky="ew")

        self.widgets["text_radiobutton"].grid(row=0, column=0, pady=5, padx=10, sticky="w")

        self.widgets["frame_setting_window"].grid_columnconfigure(0, weight=1)
        self.widgets["frame_setting_window"].grid_columnconfigure(1, weight=1)

        self.widgets["Combobox_language"].grid(row=1, column=1, pady=5, sticky="w")

        self.widgets["switch"].grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="w")

        Helpers.center_window(app=self.app, app_width=self.app_width, app_height=self.app_height)

    def show_placeholder(self):
        """ функция отображает текст placeholder если поле для ввода пустое """
        if self.widgets["Combobox_url"].get() == "":
            self.widgets["Combobox_url"].set(self.placeholder)

    def get_data_video(self, current_link):
        """  get video data  """
        self.clear_data()
        self.current_url = current_link  # self.widgets["Combobox_url"].get()

        # Проверка указанной ссылки и вывод данных о видео
        if Helpers.check_link(self.current_url, self.placeholder):
            self.downloader = Downloader(self.widgets)
            self.downloader.start_get_data_thread()
            # self.show_data_video(data_video)

    def clear_variable(self):
        """ очистка поля ввода """
        if self.widgets["Combobox_url"].get() == self.placeholder:
            self.widgets["Combobox_url"].set("")

    def clear_data_download(self):
        """ очистка данных загрузки """
        self.widgets["frame_path_download"].grid_remove()
        self.widgets["Textbox_path_to_video"].delete("0.0", tk.END)
        self.widgets["percentage_label"].configure(text="Downloaded: 0 %", text_color="white")
        self.widgets["Progressbar"].set(0)
        self.widgets["Progressbar"].grid_remove()

    def clear_data(self):
        """ очистка данных видео """
        self.widgets["video_name"].configure(text="")
        self.widgets["video_author"].configure(text="")
        self.widgets["video_image"].configure(image=None)
        Helpers.set_button_state(self.widgets["button_download"], False)
        self.clear_data_download()

    def clear_all(self):
        """ очистка всех данных """
        self.widgets["Combobox_url"].set(self.placeholder)
        self.clear_data()

    def download_video(self):
        """ download video """
        self.widgets["Progressbar"].set(0)
        self.widgets["Progressbar"].grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.widgets["percentage_label"].configure(text="Выполняется загрузка")
        Helpers.set_button_state(self.widgets["button_download"], False)

        self.downloader.start_download_thread()

    def set_theme(self):
        """ установка светлой / темной темы """
        color = self.switch_var.get()
        match color:
            case "on":
                print("green", color)
                # set_default_color_theme("green")

                set_appearance_mode("Dark")
                self.set_color_button("green")

            case "off":
                print("blue", color)
                # set_default_color_theme("blue")
                set_appearance_mode("Light")
                self.set_color_button("lightblue")

    def set_color_button(self, color_button):
        self.widgets["button_OK"].configure(fg_color=color_button)
        self.widgets["button_download"].configure(fg_color=color_button)
        self.widgets["button_Clear"].configure(fg_color=color_button)

    def change_placeholder(self):
        placeholders = (self.list_placeholder[lang] for lang in self.list_placeholder)

        if self.widgets["Combobox_url"].get() in placeholders:
            self.widgets["Combobox_url"].set(self.placeholder)


    def on_language_change(self, selected_language):
        """Обработчик изменения языка"""
        if selected_language in translation.translations:
            self.current_language = selected_language
            # Меняем placeholder
            self.placeholder = self.list_placeholder[self.current_language]
            self.change_placeholder()
            # Проходим по всем виджетам и обновляем тексты в соответствии с текущим языком
            text_translates = translation.translations[self.current_language]
            for widget_name in text_translates:
                try:
                    self.widgets[widget_name].configure(text=text_translates[widget_name])
                except:
                    print("error", widget_name)
