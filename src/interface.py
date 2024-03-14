import os.path
import tkinter as tk
import customtkinter
import re
import windowMessage
import io
import listUrls
import downloadFile, convertText
from PIL import Image, ImageTk
import urllib.request


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

class Interface:
    app = customtkinter.CTk()
    app.title("Download from YouTube")
    app_width = 400
    app_height = 700
    default_color_theme = "green"
    video_downloaded = "" #downloadFile.Download("")
    theme = {
        "blue": "./themes/blue.json",
        "dark-blue": "./themes/dark-blue.json"
    }

    def __init__(self):
        # Block enter url
        self.frame_link = customtkinter.CTkFrame(self.app, border_color=self.default_color_theme, border_width=2)

        # Enter url: text, input, button
        self.text_link = customtkinter.CTkLabel(self.frame_link, text="URL: ", text_color=self.default_color_theme)

        # url_var = tk.StringVar(value="Enter video link")
        list_urls = [url["url"] for url in listUrls.list_urls]
        self.input_link = customtkinter.CTkComboBox(self.frame_link,
                                                    values=list_urls,
                                                    width=250,
                                                    border_color=self.default_color_theme,
                                                    button_color=self.default_color_theme,
                                                    dropdown_hover_color=self.default_color_theme
                                                    )

        self.input_link.configure(command=lambda event: self.show_data_video())
        self.input_link.bind("<Return>", lambda event: self.show_data_video())
        self.input_link.bind("<Button-1>", lambda event: self.clear_variable())
        self.input_link.bind("<FocusOut>", lambda event: self.show_placeholder())

        self.button_Clear = customtkinter.CTkButton(self.frame_link, text="X", width=10, command=self.clear_all)
        self.button_OK = customtkinter.CTkButton(
            self.frame_link, text="OK", width=10,
            command=self.show_data_video)

        # Data about video
        self.frame_data_video = customtkinter.CTkFrame(self.app, border_color=self.default_color_theme, border_width=2)

        self.text_title = customtkinter.CTkLabel(self.frame_data_video, text="Name: ", text_color=self.default_color_theme)  # , text_color="blue"

        self.video_name = customtkinter.CTkLabel(self.frame_data_video, width=280, text="", justify="left")

        self.text_autor = customtkinter.CTkLabel(self.frame_data_video, text="Autor: ", text_color=self.default_color_theme)  # , text_color="blue"

        self.video_author = customtkinter.CTkLabel(self.frame_data_video, text="", width=280)

        self.text_image = customtkinter.CTkLabel(self.frame_data_video, text="Image: ", text_color=self.default_color_theme)

        self.video_image = customtkinter.CTkLabel(self.frame_data_video, text="", compound="bottom", height=80)
        # self.app.columnconfigure(1, weight=1)

        # Progress percentage
        self.frame_download = customtkinter.CTkFrame(self.app, border_color=self.default_color_theme, border_width=2)

        self.text_percentage_download = customtkinter.CTkLabel(self.frame_download, text="Downloaded: 0 %")
        # self.percentage_download = customtkinter.CTkLabel(self.frame_download, text="85")


        self.progressbar = customtkinter.CTkProgressBar(self.frame_download, width=200, height=5)
        self.progressbar.set(0)


        self.button_download = customtkinter.CTkButton(
            self.frame_download,
            text="Download",
            state="disabled",
            command=lambda: self.download_video(),
        )

        self.frame_path_download = customtkinter.CTkFrame(self.frame_download)


        self.path_text = customtkinter.CTkLabel(self.frame_path_download, text="Path to file: ")
        self.path_to_video = customtkinter.CTkTextbox(
            self.frame_path_download,
            text_color="steelblue1",
            activate_scrollbars=False,
            # state="disabled",
            wrap="word",
            height=55,
            width=335,
            cursor="hand2"
        )

        # widgets by setting colors
        self.frame_setting_window = customtkinter.CTkFrame(self.app, border_color=self.default_color_theme, border_width=2)
        # self.radio_var = tk.IntVar(value=1)
        self.text_radiobutton = customtkinter.CTkLabel(self.frame_setting_window, text="Select theme: ", text_color=self.default_color_theme)
        # self.themes_2 = customtkinter.CTkRadioButton(self.app, text="Dark", variable=self.radio_var, value=1, command=self.set_theme)
        # self.themes_1 = customtkinter.CTkRadioButton(self.app, text="Light", variable=self.radio_var, value=2, command=self.set_theme)
        # self.app.columnconfigure(0, weight=1)

        self.switch_var = customtkinter.StringVar(value="on")
        self.switch = customtkinter.CTkSwitch(self.frame_setting_window, text="Light/Dark", variable=self.switch_var, onvalue="on", offvalue="off", command=self.set_theme)



    def create_widgets(self):
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

        self.text_image.grid(row=2, column=0, padx=(20,0), pady=10, sticky="nwe")

        self.video_image.grid(row=2, column=1, padx=20, pady=10, sticky="n") #, columnspan=4)

        # widgets by download of video
        self.frame_download.columnconfigure(0, weight=1)
        self.frame_download.grid(row=2, column=0, padx=10, pady=10, ipadx=5, ipady=5, sticky="ew")
        self.text_percentage_download.grid(row=0, column=0, pady=10, padx=20)

        self.progressbar.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        # print(self.frame_download.grid_size())
        self.button_download.grid(row=2, column=0, padx=20, pady=(0, 10))

        # self.frame_path_download.grid(row=3, column=0, padx=20, sticky="we")
        # self.frame_path_download.columnconfigure(0, weight=1)
        self.path_text.grid(row=0, column=0, padx=5, sticky="wn")
        self.path_to_video.grid(row=1, column=0, padx=5, sticky="ew")

        # widgets by setting window
        self.frame_setting_window.grid(row=3, column=0, padx=10, pady=10, ipadx=5, ipady=5, sticky="ew")

        self.text_radiobutton.grid(row=0, column=0, pady=5, sticky="e")

        # self.themes_1.grid(row=16, column=0, padx=10, sticky="w")
        # self.themes_2.grid(row=16, column=1, padx=10, sticky="w")
        
        self.switch.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="w")




    def show_app(self):
        self.create_widgets()
        self.center_window()
        Interface.app.mainloop()

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
        font = self.video_name.cget("font")
        width = self.video_name.cget("width")
        converted_text = convertText.split_text_by_width(title, width, font)
        self.video_name.configure(text=converted_text)

    def show_video_author(self, author):
        font = self.video_author.cget("font")
        width = self.video_author.cget("width")
        converted_text = convertText.split_text_by_width(author, width, font)
        self.video_author.configure(text=converted_text)

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

    def show_placeholder(self):
        if self.input_link.get() == "":
            self.input_link.set("Enter video link")

    def show_data_video(self):
        value = self.input_link.get()
        self.clear_data()
        print("Selected value:", value)
        if self.is_youtube_url(value):
            # self.clear_data()
            self.video_downloaded = downloadFile.Download(value, progress_callback=self.set_percentage
                                                          )
            data_video = self.video_downloaded.get_data_video()
            print("data_video", [data_video])
            if data_video:
                self.show_video_title(data_video["title"])
                self.show_video_author(data_video["author"])
                self.show_video_image(data_video["image"])
                self.button_download_isdisable("normal")
        else:
            # self.clear_data()
            windowMessage.open_window_error("Url video invalid!\nEnter correct link.")

    def clear_variable(self):
        if self.input_link.get() == "Enter video link":
            self.input_link.set("")

    def clear_data_download(self):
        print("clear")
        self.frame_path_download.grid_remove()
        self.path_to_video.delete("0.0", tk.END)
        self.text_percentage_download.configure(text="Downloaded: 0 %")
        self.progressbar.set(0)


    def clear_data(self):
        self.video_name.configure(text="")
        self.video_author.configure(text="")
        self.video_image.configure(image=None)
        self.button_download_isdisable("disabled")
        self.clear_data_download()

    def clear_all(self):
        self.input_link.set("Enter video link")
        self.clear_data()

    def download_video(self):
        # print(self.video_downloaded.get_data_video())
        is_download=self.video_downloaded.download_video()
        if is_download:
            self.frame_path_download.grid(row=3, column=0, padx=20, sticky="we")
            path_video = os.path.dirname(is_download)
            print("is_download: ", path_video)
            self.show_path_to_file(path_video)
        else:
            self.progressbar.set(0)

    def show_path_to_file(self, path):
        self.path_to_video.delete("1.0", tk.END)
        self.path_to_video.insert("1.0", path)
        self.path_to_video.bind("<Button-1>", lambda event: self.open_directory(path))

    @staticmethod
    def open_directory(path):
        os.startfile(path)

    # def set_theme(self):
    #     level = self.radio_var.get()
    #     match level:
    #         case 1:
    #             # print(self.theme["dark-blue"])
    #             # customtkinter.set_default_color_theme(self.theme["dark-blue"])
    #             customtkinter.set_appearance_mode("Dark")
                
    #         case 2:
    #             # print(self.theme["blue"])
    #             # customtkinter.set_default_color_theme(self.theme["blue"])
    #             customtkinter.set_appearance_mode("Light")
                
    def set_theme(self):
        color = self.switch_var.get()
        match color:
            case "on":
                print("green", color)
                # customtkinter.set_default_color_theme("green")
                
                customtkinter.set_appearance_mode("Dark")
                self.set_color_button("green")
                
            case "off":
                print("blue", color)
                # customtkinter.set_default_color_theme("blue")
                customtkinter.set_appearance_mode("Light")
                self.set_color_button("lightblue")


                
    def set_color_button(self, color_button):
        self.button_OK.configure(fg_color=color_button)
        self.button_download.configure(fg_color=color_button)
        self.button_Clear.configure(fg_color=color_button)

    def set_percentage(self, percentage):
        current_text = self.text_percentage_download.cget("text")
        print("%: ", percentage)
        self.text_percentage_download.configure(text=f"Downloaded: {percentage} %")
        self.progressbar.set(percentage / 100)
        self.text_percentage_download.update()
        # self.progressbar

    def is_download(self):
        pass
                
