import tkinter as tk
import customtkinter
import listUrls


# from customtkinter.windows.widgets.core_widget_classes.ctk_base_class import CTkImage

class DownloadYoutube:
    app = tk.Tk()
    url_youtube = ""

    def __init__(self):
        self.text_link = customtkinter.CTkLabel(DownloadYoutube.app, text="URL: ")  # text_color="lightblue"

        url_var = tk.StringVar(value="Enter video link")
        list_urls = [url["url"] for url in listUrls.list_urls]
        self.input_link = customtkinter.CTkComboBox(DownloadYoutube.app, variable=url_var, values=list_urls,
                                                    command=DownloadYoutube.show_data_video)
        DownloadYoutube.app.columnconfigure(1, weight=1)

        self.button_OK = customtkinter.CTkButton(
            DownloadYoutube.app, text="OK", width=10,
            # command=show_video_data
        )

        self.text_title = customtkinter.CTkLabel(DownloadYoutube.app, text="Name: ")  # , text_color="blue"

        self.video_name = customtkinter.CTkTextbox(
            DownloadYoutube.app,
            text_color="lightblue",
            activate_scrollbars=False,
            state="disabled",
            wrap="word",
            height=50,
            width=300,
        )

        self.text_autor = customtkinter.CTkLabel(DownloadYoutube.app, text="Autor: ")  # , text_color="blue"

        self.video_author = customtkinter.CTkLabel(DownloadYoutube.app, text="", text_color="lightblue")

        self.text_image = customtkinter.CTkLabel(DownloadYoutube.app, text="Image: ")

        self.video_image = customtkinter.CTkLabel(DownloadYoutube.app, text="", compound="bottom")
        DownloadYoutube.app.columnconfigure(1, weight=1)

        self.button_download = customtkinter.CTkButton(
            DownloadYoutube.app,
            text="Download",
            state="disabled",
            # command=lambda: downloadFile.download,
        )
        DownloadYoutube.app.columnconfigure(0, weight=1)

    def create_widgets(self):
        self.text_link.grid(row=0, column=0, padx=10, pady=20, sticky="e")

        self.input_link.grid(row=0, column=1, padx=10, sticky="ew", columnspan=2)

        self.button_OK.grid(row=0, column=3, padx=10, sticky="e")

        self.text_title.grid(row=1, column=0, padx=10, sticky="e")

        self.video_name.grid(row=1, column=1, padx=10, sticky="w", columnspan=4, rowspan=2)

        self.text_autor.grid(row=3, column=0, padx=10, sticky="e")

        self.video_author.grid(row=3, column=1, padx=10, sticky="w", columnspan=4)

        self.text_image.grid(row=6, column=0, padx=10, sticky="e")

        self.video_image.grid(row=6, column=1, padx=20, pady=20, columnspan=4)

        self.button_download.grid(row=8, column=1, padx=20, pady=20, columnspan=2)

    def show_app(self):
        self.create_widgets()
        DownloadYoutube.app.mainloop()

    def show_data_video(self):
        current_value = self.input_link.get()
        print("Entered value:", current_value)


class Person:
    name = "Semen"
    age = 30