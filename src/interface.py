import tkinter as tk
from customtkinter import CTk, CTkButton, CTkLabel, CTkProgressBar, CTkFrame, CTkComboBox, CTkTextbox, CTkSwitch, \
    StringVar, set_default_color_theme, set_appearance_mode
from helpers import Helpers
from widgets import widgets
from data.listUrls import list_urls
from downloadFile import Downloader

set_appearance_mode("Dark")
set_default_color_theme("green")


class Interface:
    """ creates interface, place widgets into UI """
    app_width = 0
    app_height = 0
    default_color_theme = "green"
    video_downloaded = ""
    placeholder = "Enter video link"
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
        print("self.current_url", self.current_url)

        # Подключаем downloader
        # self.downloader = Downloader(self.widgets)

    def create_widgets(self):
        # Block enter url
        self.widgets["frame_link"] = self.frame_link = CTkFrame(self.app,
                                                                border_color=self.default_color_theme,
                                                                border_width=2)

        # Enter url: text, input, button
        self.widgets["text_link"] = self.text_link = CTkLabel(self.frame_link, text="URL: ",
                                                              text_color=self.default_color_theme)

        urls = [url["url"] for url in list_urls]
        combobox_var = StringVar(value=self.current_url)
        self.widgets["Combobox_url"] = self.input_link = CTkComboBox(
            self.frame_link,
            values=urls,
            variable=combobox_var,
            width=250,
            border_color=self.default_color_theme,
            button_color=self.default_color_theme,
            dropdown_hover_color=self.default_color_theme)

        self.input_link.configure(command=lambda event: self.get_data_video())
        self.input_link.bind("<Return>", lambda event: self.get_data_video())
        self.input_link.bind("<Button-1>", lambda event: self.clear_variable())
        self.input_link.bind("<FocusOut>", lambda event: self.show_placeholder())

        self.widgets["button_Clear"] = self.button_Clear = CTkButton(self.frame_link, text="X",
                                                                     width=10,
                                                                     command=self.clear_all)
        self.widgets["button_OK"] = self.button_OK = CTkButton(
            self.frame_link, text="OK", width=10,
            command=self.get_data_video)

        # Data about video
        self.widgets["frame_data_video"] = self.frame_data_video = CTkFrame(self.app,
                                                                            border_color=self.default_color_theme,
                                                                            border_width=2)

        self.widgets["text_title"] = self.text_title = CTkLabel(self.frame_data_video,
                                                                text="Name: ",
                                                                text_color=self.default_color_theme)

        self.widgets["video_name"] = self.video_name = CTkLabel(self.frame_data_video,
                                                                width=280, text="",
                                                                justify="left")

        self.widgets["text_autor"] = self.text_autor = CTkLabel(self.frame_data_video,
                                                                text="Autor: ",
                                                                text_color=self.default_color_theme)

        self.widgets["video_author"] = self.video_author = CTkLabel(self.frame_data_video,
                                                                    text="", width=280)

        self.widgets["text_image"] = self.text_image = CTkLabel(self.frame_data_video,
                                                                text="Image: ",
                                                                text_color=self.default_color_theme)

        self.widgets["video_image"] = self.video_image = CTkLabel(self.frame_data_video,
                                                                  text="", compound="bottom",
                                                                  height=80)

        # video download block
        self.widgets["frame_download"] = self.frame_download = CTkFrame(self.app,
                                                                        border_color=self.default_color_theme,
                                                                        border_width=2)

        self.widgets["percentage_label"] = self.percentage_label = CTkLabel(self.frame_download,
                                                                            text="Downloaded: 0 %", text_color="white")

        self.widgets["Progressbar"] = self.progressbar = CTkProgressBar(self.frame_download, width=200,
                                                                        height=5)
        self.progressbar.set(0)

        self.widgets["button_download"] = self.button_download = CTkButton(
            self.frame_download,
            text="Download",
            fg_color="gray",
            state="disabled",
            command=lambda: self.download_video(),
        )

        self.widgets["frame_path_download"] = self.frame_path_download = CTkFrame(
            self.frame_download)

        self.widgets["path_text"] = self.path_text = CTkLabel(self.frame_path_download,
                                                              text="Path to file: ")
        self.widgets["Textbox_path_to_video"] = self.path_to_video = CTkTextbox(
            self.frame_path_download,
            text_color="steelblue1",
            activate_scrollbars=False,
            wrap="word",
            height=55,
            width=335,
            cursor="hand2",
        )

        # widgets by setting colors
        self.widgets["frame_setting_window"] = self.frame_setting_window = CTkFrame(self.app,
                                                                                    border_color=self.default_color_theme,
                                                                                    border_width=2)
        self.widgets["text_radiobutton"] = self.text_radiobutton = CTkLabel(
            self.frame_setting_window, text="Select theme: ", text_color=self.default_color_theme)

        self.switch_var = StringVar(value="on")
        self.widgets["Switch"] = self.switch = CTkSwitch(self.frame_setting_window, text="Light/Dark",
                                                         variable=self.switch_var, onvalue="on",
                                                         offvalue="off", command=self.set_theme)

    def place_widgets(self):
        # widgets by entered url video
        self.app.grid_columnconfigure(0, weight=1)

        self.frame_link.grid(row=0, padx=10, pady=10, ipadx=5, ipady=5, sticky="ew")

        self.text_link.grid(row=0, column=0, padx=(20, 0), pady=(10, 0), sticky="we")

        self.input_link.grid(row=0, column=1, padx=5, pady=(10, 0))

        self.button_Clear.grid(row=0, column=2, padx=5, pady=(10, 0))

        self.button_OK.grid(row=0, column=3, padx=5, pady=(10, 0))

        # widgets by data about video
        self.frame_data_video.grid(row=1, padx=10, pady=10, ipadx=5, ipady=5, sticky="ew")

        self.text_title.grid(row=0, column=0, padx=(20, 0), pady=10, sticky="wen")

        self.video_name.grid(row=0, column=1, padx=20, pady=10, ipady=5, sticky="ew")

        self.text_autor.grid(row=1, column=0, padx=(20, 0), pady=10, sticky="nwe")

        self.video_author.grid(row=1, column=1, padx=20, pady=10, sticky="w")

        self.text_image.grid(row=2, column=0, padx=(20, 0), pady=10, sticky="nwe")

        self.video_image.grid(row=2, column=1, padx=20, pady=10, sticky="n")  # , columnspan=4)

        # widgets by download of video
        self.frame_download.columnconfigure(0, weight=1)
        self.frame_download.grid(row=2, column=0, padx=10, pady=10, ipadx=5, ipady=5, sticky="ew")
        self.percentage_label.grid(row=0, column=0, pady=10, padx=20)

        # self.progressbar.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.button_download.grid(row=2, column=0, padx=20, pady=(0, 10))

        self.path_text.grid(row=0, column=0, padx=5, sticky="wn")
        self.path_to_video.grid(row=1, column=0, padx=5, sticky="ew")

        # widgets by setting window
        self.frame_setting_window.grid(row=3, column=0, padx=10, pady=10, ipadx=5, ipady=5, sticky="ew")

        self.text_radiobutton.grid(row=0, column=0, pady=5, sticky="e")

        self.switch.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="w")

        Helpers.center_window(app=self.app, app_width=self.app_width, app_height=self.app_height)

    def show_placeholder(self):
        """ функция отображает текст placeholder если поле для ввода пустое """
        if self.input_link.get() == "":
            self.input_link.set(self.placeholder)

    def get_data_video(self):
        """  get video data  """
        self.clear_data()
        self.current_url = self.input_link.get()

        # Проверка указанной ссылки и вывод данных о видео
        if Helpers.check_link(self.current_url, self.placeholder):
            self.downloader = Downloader(self.widgets)
            self.downloader.start_get_data_thread()
            # self.show_data_video(data_video)

    def clear_variable(self):
        """ очистка поля ввода """
        if self.input_link.get() == self.placeholder:
            self.input_link.set("")

    def clear_data_download(self):
        """ очистка данных загрузки """
        self.frame_path_download.grid_remove()
        self.path_to_video.delete("0.0", tk.END)
        self.percentage_label.configure(text="Downloaded: 0 %", text_color="white")
        self.progressbar.set(0)
        self.progressbar.grid_remove()

    def clear_data(self):
        """ очистка данных видео """
        self.video_name.configure(text="")
        self.video_author.configure(text="")
        self.video_image.configure(image=None)
        Helpers.set_button_state(self.button_download, False)
        self.clear_data_download()

    def clear_all(self):
        """ очистка всех данных """
        self.input_link.set("Enter video link")
        self.clear_data()

    def download_video(self):
        """ download video """
        self.progressbar.set(0)
        self.progressbar.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        Helpers.set_button_state(self.button_download, False)
        self.downloader.start_download_thread()

    def set_theme(self):
        """ установка темы """
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
        self.button_OK.configure(fg_color=color_button)
        self.button_download.configure(fg_color=color_button)
        self.button_Clear.configure(fg_color=color_button)
