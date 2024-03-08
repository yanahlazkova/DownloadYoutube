import os.path
import tkinter as tk
import customtkinter
import re
import windowMessage
import io
import listUrls
import downloadFile
from PIL import Image, ImageTk
import urllib.request


# from customtkinter.windows.widgets.core_widget_classes.ctk_base_class import CTkImage

class DownloadYoutube:
    app = tk.Tk()
    app.title("Download from YouTube")
    app_width = 400
    app_height = 500
    video_downloaded = downloadFile.Download("")
    theme = {
        "blue": "./themes/blue.json",
        "dark-blue": "./themes/dark-blue.json"
    }

    def __init__(self):
        self.text_link = customtkinter.CTkLabel(self.app, text="URL: ")  # text_color="lightblue"

        url_var = tk.StringVar(value="Enter video link")
        list_urls = [url["url"] for url in listUrls.list_urls]
        self.input_link = customtkinter.CTkComboBox(self.app, variable=url_var, values=list_urls)
        self.input_link.configure(command=lambda event: self.show_data_video())
        self.input_link.bind("<Return>", lambda event: self.show_data_video())
        self.input_link.bind("<Button-1>", lambda event: self.clear_variable())
        self.app.columnconfigure(1, weight=1)

        self.button_Clear = customtkinter.CTkButton(self.app, text="X", width=10, command=self.clear_all)
        self.button_OK = customtkinter.CTkButton(
            self.app, text="OK", width=10,
            command=self.show_data_video)

        self.text_title = customtkinter.CTkLabel(self.app, text="Name: ")  # , text_color="blue"

        self.video_name = customtkinter.CTkTextbox(
            self.app,
            text_color="lightblue",
            activate_scrollbars=False,
            state="disabled",
            wrap="word",
            height=50,
            width=300,
        )

        self.text_autor = customtkinter.CTkLabel(self.app, text="Autor: ")  # , text_color="blue"

        self.video_author = customtkinter.CTkLabel(self.app, text="", text_color="lightblue")

        self.text_image = customtkinter.CTkLabel(self.app, text="Image: ")

        self.video_image = customtkinter.CTkLabel(self.app, text="", compound="bottom", height=100)
        self.app.columnconfigure(1, weight=1)

        self.button_download = customtkinter.CTkButton(
            DownloadYoutube.app,
            text="Download",
            state="disabled",
            command=lambda: self.download_video(),
        )
        DownloadYoutube.app.columnconfigure(0, weight=1)

        self.path_text = customtkinter.CTkLabel(self.app, text="Path to file: ")
        self.path_to_video = customtkinter.CTkTextbox(
            self.app,
            text_color="steelblue1",
            activate_scrollbars=False,
            # state="disabled",
            wrap="word",
            height=80,
            width=300,
            cursor="hand2"
        )

    def create_widgets(self):
        self.text_link.grid(row=0, column=0, padx=10, pady=20, sticky="e")

        self.input_link.grid(row=0, column=1, padx=10, sticky="ew", columnspan=2)

        self.button_Clear.grid(row=0, column=3)

        self.button_OK.grid(row=0, column=4, padx=10, sticky="e")

        self.text_title.grid(row=1, column=0, padx=10, sticky="e")

        self.video_name.grid(row=1, column=1, padx=10, sticky="w", columnspan=4, rowspan=2)

        self.text_autor.grid(row=3, column=0, padx=10, sticky="e")

        self.video_author.grid(row=3, column=1, padx=10, sticky="w", columnspan=4)

        self.text_image.grid(row=6, column=0, padx=10, sticky="e")

        self.video_image.grid(row=6, column=1, padx=20, pady=20, columnspan=4)

        self.button_download.grid(row=8, column=1, padx=20, pady=20, columnspan=2)

    def show_app(self):
        self.create_widgets()
        self.center_window()
        DownloadYoutube.app.mainloop()

    def center_window(self):
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()

        x = (screen_width - self.app_width) // 2
        y = (screen_height - self.app_height) // 2

        self.app.geometry(f"{self.app_width}x{self.app_height}+{x}+{y}")

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
        self.video_name.configure(state="normal")

        self.video_name.delete("1.0", tk.END)
        self.video_name.insert("1.0", title)

        self.video_name.configure(state="disabled")

    def show_video_author(self, author):
        self.video_author.configure(text=author)

    def show_video_image(self, image):
        self.video_image.configure(image=None)
        response = urllib.request.urlopen(image)
        image_data = response.read()
        image = Image.open(io.BytesIO(image_data))
        image.thumbnail((250, 250))
        # image = image.resize((100))
        photo_image = ImageTk.PhotoImage(image)

        self.video_image.configure(image=photo_image)

    def button_download_isdisable(self, state_button):
        self.button_download.configure(state=state_button)

    def show_data_video(self):
        value = self.input_link.get()
        print("Selected value:", value)
        if DownloadYoutube.is_youtube_url(value):
            self.video_downloaded = downloadFile.Download(value)
            data_video = self.video_downloaded.get_data_video()
            print("data_video", [data_video])
            self.show_video_title(data_video["title"])
            self.show_video_author(data_video["author"])
            self.show_video_image(data_video["image"])
            self.button_download_isdisable("normal")

        else:
            self.clear_data()
            windowMessage.open_window_error("Url video invalid!\nEnter correct link.")

    def clear_variable(self):
        if self.input_link.get() == "Enter video link":
            self.input_link.set("")

    def clear_data(self):
        self.show_video_title("")
        self.show_video_author("")
        self.video_image.configure(image=None)
        self.button_download_isdisable("disable")
        self.path_to_video.delete("1.0", tk.END)

    def clear_all(self):
        self.input_link.set("Enter video link")
        self.clear_data()

    def download_video(self):
        print(self.video_downloaded.get_data_video())
        is_download = self.video_downloaded.download_video()
        if is_download:
            path_video = os.path.dirname(is_download)
            print("is_download: ", path_video)
            self.show_path_to_file(path_video)

    def show_path_to_file(self, path):
        self.path_text.grid(row=9, column=0, padx=10, sticky="e")
        self.path_to_video.delete("1.0", tk.END)
        self.path_to_video.insert("1.0", path)
        self.path_to_video.bind("<Button-1>", lambda event: self.open_directory(path))
        self.path_to_video.grid(row=9, column=1, padx=10, sticky="w", columnspan=4, rowspan=20)

    @staticmethod
    def open_directory(path):
        os.startfile(path)
