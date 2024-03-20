from os import path
import tkinter as tk
# update: import classes from libs, when you can
from customtkinter import CTk, CTkButton, CTkLabel, CTkProgressBar, CTkFrame, CTkComboBox, CTkTextbox, CTkSwitch, StringVar, set_default_color_theme, set_appearance_mode
import re
from tkinter.messagebox import showerror
from io import BytesIO
from data.listUrls import list_urls
from downloadFile import Downloader
from helpers import Helpers
from PIL import Image, ImageTk
from urllib.request import urlopen
from widgets import widgets


# update: remove styling code from here

class Interface:
    """ creates interface, place widgets into UI """
    # update: moves default congiguration to constructor
    default_color_theme = "green"
    video_downloaded = ""  # reference -> downloadFile.Download("")
    theme = {
        "blue": "./themes/blue.json",
        "dark-blue": "./themes/dark-blue.json"
    }

    def __init__(self, title: str, width: int, height: int):
        # update: moves default variables to your constructor
        self.app = CTk()

        # set basic title, styling, size etc
        self.app.title(title)
        self.app_width = width
        self.app_height = height
        self.app.geometry(f"{self.app_width}x{self.app_height}")
        self.set_default_theme()

        self.current_url = list_urls[0]["url"]

        # Enables widgets and downloader
        self.widgets = widgets
        self.downloader = Downloader(self.widgets)
        # update: add method from helpers class 
        self.split_text_by_width = Helpers().split_text_by_width

    # update: make new method for base styling

    def set_default_theme(self):
        """ applies default UI stylings """
        set_appearance_mode("Dark")
        set_default_color_theme("green")

    def create_widgets(self):
        # Block enter url
        self.widgets["frame_link"] = CTkFrame(
            self.app, border_color=self.default_color_theme, border_width=2)

        # Enter url: text, input, button
        self.widgets["text_link"] = CTkLabel(
            self.widgets["frame_link"], text="URL: ", text_color=self.default_color_theme)

        # url_var = tk.StringVar(value="Enter video link")
        urls = [url["url"] for url in list_urls]

        self.widgets["Combobox_url"] = CTkComboBox(
            self.widgets["frame_link"],
            values=urls,
            width=250,
            border_color=self.default_color_theme,
            button_color=self.default_color_theme,
            dropdown_hover_color=self.default_color_theme
        )

        # update: NEVER DO double assignings,
        # because double assignings are not readable
        # and you can easily avoid them using conscious variable names! 

        self.widgets["Combobox_url"].configure(
            command=lambda event: self.show_data_video())
        self.widgets["Combobox_url"].bind(
            "<Return>", lambda event: self.show_data_video())
        self.widgets["Combobox_url"].bind(
            "<Button-1>", lambda event: self.clear_variable())
        self.widgets["Combobox_url"].bind(
            "<FocusOut>", lambda event: self.show_placeholder())

        self.widgets["button_clear"] = CTkButton(
            self.widgets["frame_link"], text="X", width=10, command=self.clear_all)

        self.widgets["button_ok"] = CTkButton(
            self.widgets["frame_link"], text="OK", width=10,
            command=self.show_data_video)

        # Data about video
        self.widgets["frame_data_video"] =CTkFrame(
            self.app, border_color=self.default_color_theme, border_width=2)

        self.widgets["text_title"] = CTkLabel(
            # , text_color="blue"
            self.widgets["frame_data_video"], text="Name: ", text_color=self.default_color_theme)

        self.widgets["video_name"] = CTkLabel(
            self.widgets["frame_data_video"], width=280, text="", justify="left")

        self.widgets["text_autor"] = CTkLabel(
            # , text_color="blue"
            self.widgets["frame_data_video"], text="Autor: ", text_color=self.default_color_theme)

        self.widgets["video_author"] = CTkLabel(
            self.widgets["frame_data_video"],     text="", width=280)

        self.widgets["text_image"] = CTkLabel(
            self.widgets["frame_data_video"], text="Image: ", text_color=self.default_color_theme)

        self.widgets["video_image"] = CTkLabel(
            self.widgets["frame_data_video"],   text="", compound="bottom",   height=80)

        # video download block
        self.widgets["frame_download"] = CTkFrame(
            self.app,         border_color=self.default_color_theme,         border_width=2)

        self.widgets["percentage_label"] = CTkLabel(
            self.widgets["frame_download"],             text="Downloaded: 0 %")

        self.widgets["Progressbar"] = CTkProgressBar(self.widgets["frame_download"], width=200,
                                                                                      height=5)
        self.widgets["Progressbar"].set(0)

        self.widgets["button_download"] = CTkButton(
            self.widgets["frame_download"],
            text="Download",
            fg_color="gray",
            state="disabled",
            command=lambda: self.download_video(),
        )

        self.widgets["frame_path_download"] = CTkFrame(
            self.widgets["frame_download"])

        self.widgets["path_text"] = CTkLabel(self.widgets["frame_path_download"], text="Path to file: ")
        
        self.widgets["Textbox_path_to_video"] = CTkTextbox(
            self.widgets["frame_path_download"],
            text_color="steelblue1",
            activate_scrollbars=False,
            # state="disabled",
            wrap="word",
            height=55,
            width=335,
            cursor="hand2",
        )

        # widgets by setting colors
        self.widgets["frame_setting_window"] = CTkFrame(
            self.app,                     border_color=self.default_color_theme,                     border_width=2)
        self.widgets["text_radiobutton"] = CTkLabel(
            self.widgets["frame_setting_window"], text="Select theme: ", text_color=self.default_color_theme)

        self.switch_var = StringVar(value="on")
        self.widgets["Switch"] = CTkSwitch(self.widgets["frame_setting_window"], text="Light/Dark",variable=self.switch_var, onvalue="on",offvalue="off", command=self.set_theme)


    def place_widgets(self):
        # widgets by entered url video
        self.app.grid_columnconfigure(0, weight=1)
        self.widgets["frame_link"].grid(row=0, padx=10, pady=10,
                                        ipadx=5, ipady=5, sticky="ew")

        self.widgets["text_link"].grid(row=0, column=0, padx=(20, 0),
                                       pady=(10, 0), sticky="we")
        self.widgets["Combobox_url"].grid(
            row=0, column=1, padx=5, pady=(10, 0))
        self.widgets["button_clear"] .grid(
            row=0, column=2, padx=5, pady=(10, 0))
        self.widgets["button_ok"].grid(row=0, column=3, padx=5, pady=(10, 0))

        # widgets by data about video
        self.widgets["frame_data_video"].grid(
            row=1, padx=10, pady=10, ipadx=5, ipady=5, sticky="ew")
        self.widgets["text_title"].grid(row=0, column=0, padx=(
            20, 0), pady=10, sticky="wen")
        self.widgets["video_name"].grid(row=0, column=1, padx=20,
                             pady=10, ipady=5, sticky="ew")
        self.widgets["text_autor"].grid(row=1, column=0, padx=(
            20, 0), pady=10, sticky="nwe")
        self.widgets["video_author"].grid(row=1, column=1, padx=20, pady=10, sticky="w")
        self.widgets["text_image"].grid(row=2, column=0, padx=(
            20, 0), pady=10, sticky="nwe")
        self.widgets["video_image"].grid(row=2, column=1, padx=20,
                              pady=10, sticky="n")  # , columnspan=4)

        # widgets by download of video
        self.widgets["frame_download"].columnconfigure(0, weight=1)
        self.widgets["frame_download"].grid(
            row=2, column=0, padx=10, pady=10, ipadx=5, ipady=5, sticky="ew")
        self.widgets["percentage_label"].grid(row=0, column=0, pady=10, padx=20)

        self.widgets["Progressbar"].grid(row=1, column=0, padx=20,
                              pady=(0, 20), sticky="ew")
        self.widgets["button_download"].grid(row=2, column=0, padx=20, pady=(0, 10))
        self.widgets["path_text"].grid(row=0, column=0, padx=5, sticky="wn")
        self.widgets["Textbox_path_to_video"].grid(row=1, column=0, padx=5, sticky="ew")

        # widgets by setting window
        self.widgets["frame_setting_window"].grid(
            row=3, column=0, padx=10, pady=10, ipadx=5, ipady=5, sticky="ew")
        self.widgets["text_radiobutton"].grid(row=0, column=0, pady=5, sticky="e")

        self.widgets["Switch"].grid(row=1, column=0, padx=10,
                         pady=10, columnspan=2, sticky="w")

    def show_interface(self):
        """ display app window """
        self.create_widgets()
        self.place_widgets()
        self.center_window()

        # update: don't call class instance inside own class
        # Interface.app.mainloop()
        self.app.mainloop()

    # todo: this is too...
    def center_window(self):
        """ centering app window """
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()

        x = (screen_width - self.app_width) // 2
        y = (screen_height - self.app_height) // 2

        self.app.geometry(f"{self.app_width}x{self.app_height}+{x}+{y}")

        # makes the window non-resizable
        self.app.resizable(height=False, width=False)

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

    def show_video_title(self, title):
        """ конвертация Названия видео для отображения в несколько строк"""
        font = self.widgets["video_name"].cget("font")
        width = self.widgets["video_name"].cget("width")
        converted_text = self.split_text_by_width(title, width, font)
        self.widgets["video_name"].configure(text=converted_text)

    def show_video_author(self, author):
        """ display author video"""
        font = self.widgets["video_author"].cget("font")
        width = self.widgets["video_author"].cget("width")
        converted_text = self.split_text_by_width(author, width, font)
        self.widgets["video_author"].configure(text=converted_text)

    def show_video_image(self, image):
        self.widgets["video_image"].configure(image=None)
        response = urlopen(image)
        image_data = response.read()
        image = Image.open(BytesIO(image_data))
        image.thumbnail((250, 250))
        # image = image.resize((100))
        photo_image = ImageTk.PhotoImage(image)

        self.widgets["video_image"].configure(image=photo_image)

    def set_button_download_state(self, state_button):
        """ function makes state of button disable/normal """
        self.widgets["button_download"].configure(state=("normal" if state_button else "disabled"), fg_color=("green" if state_button else "gray"))

    def show_placeholder(self):
        """ функция отображает текст placeholder если поле для ввода пустое """
        if self.widgets["Combobox_url"].get() == "":
            self.widgets["Combobox_url"].set("Enter video link")

    def show_data_video(self):
        """  displaying video data  """
        self.current_url = self.widgets["Combobox_url"].get()
        if self.current_url == "" or self.current_url == "Enter video link":
            showerror("Error...", "YouTube link is invalid")
            return
        self.clear_data()
        print("Selected value:", self.current_url)
        """ checking the link and display video data """
        if self.is_youtube_url(self.current_url):
            data_video = self.downloader.get_data_video()
            print("data_video", [data_video])
            if data_video:
                self.show_video_title(data_video["title"])
                self.show_video_author(data_video["author"])
                self.show_video_image(data_video["image"])
                self.set_button_download_state(data_video["access"])
        else:
            showerror("Error...", "Url video invalid!\nEnter correct link.")

    def clear_variable(self):
        """ очистка поля ввода """
        if self.widgets["Combobox_url"].get() == "Enter video link":
            self.widgets["Combobox_url"].set("")

    def clear_data_download(self):
        """ очистка данных загрузки """
        self.widgets["frame_path_download"].grid_remove()
        self.widgets["Textbox_path_to_video"].delete("0.0", tk.END)
        self.widgets["percentage_label"].configure(text="Downloaded: 0 %")
        self.widgets["Progressbar"].set(0)

    def clear_data(self):
        """ очистка данных видео """
        self.widgets["video_name"].configure(text="")
        self.widgets["video_author"].configure(text="")
        self.widgets["video_image"].configure(image=None)
        self.set_button_download_state(False)
        self.clear_data_download()

    def clear_all(self):
        """ очистка всех данных """
        self.widgets["Combobox_url"].set("Enter video link")
        self.clear_data()

    def download_video(self):
        """ download video """
        is_download = self.downloader.start_download_thread()
        print("is_download", is_download)
        if is_download:
            path_video = path.dirname(is_download)
            self.show_path_to_file(path_video)
        else:
            self.widgets["Progressbar"].set(0)

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
        self.widgets["button_ok"].configure(fg_color=color_button)
        self.widgets["button_download"].configure(fg_color=color_button)
        self.widgets["button_clear"] .configure(fg_color=color_button)
