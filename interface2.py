import os.path
import tkinter
import tkinter as tk
import urllib.request

import customtkinter
import re
# import windowMessage
import io
# import listUrls
# import downloadFile
from PIL import Image, ImageTk

# import urllib.request


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()

app.geometry("400x550")
app.grid_columnconfigure(0, weight=1)

# Block enter url
frame_link = customtkinter.CTkFrame(app, border_color="green", border_width=2)
frame_link.grid(row=0, padx=10, pady=20, ipadx=5, ipady=5, sticky="ew")
# app.grid_columnconfigure(0, minsize=50)
# app.grid_columnconfigure(1, minsize=100)

# Enter url: text, input, button
text_link = customtkinter.CTkLabel(frame_link, text="Url: ")
text_link.grid(row=0, column=0, padx=(20, 0), pady=(10, 0), sticky="we")

# url_var = tk.StringVar(value="Enter video link")
url_var = ["element1", "element2", "element3"]
input_link = customtkinter.CTkComboBox(frame_link,
                                       # variable=url_var,
                                       values=url_var,
                                       width=250,
                                       border_color="green",
                                       button_color="green",
                                       dropdown_hover_color="green"

                                       )
input_link.set(url_var[0])
input_link.grid(row=0, column=1, padx=5, pady=(10, 0))

button_Clear = customtkinter.CTkButton(frame_link, text="X", width=10)
button_Clear.grid(row=0, column=2, padx=5, pady=(10, 0))

button_OK = customtkinter.CTkButton(frame_link, text="OK", width=10)
button_OK.grid(row=0, column=3, padx=5, pady=(10, 0))

# Data about video
frame_data_video = customtkinter.CTkFrame(app, border_color="green", border_width=2)
frame_data_video.grid(row=1, padx=10, pady=20, ipadx=5, ipady=5, sticky="ew")

text_title = customtkinter.CTkLabel(frame_data_video, text="Name: ")
text_title.grid(row=0, column=0, padx=(20, 0), pady=20, sticky="wen")

video_name = customtkinter.CTkLabel(frame_data_video, width=280, text="", justify="left")


def split_text_by_width(text, width, font):
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


video_name_text = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua."
text_font = video_name.cget("font")
text_title = split_text_by_width(video_name_text, 280, text_font)

video_name.grid(row=0, column=1, padx=20, pady=10, sticky="new")
video_name.configure(text=text_title)

text_author = customtkinter.CTkLabel(frame_data_video, text="Author: ")
text_author.grid(row=1, column=0, padx=(20, 0), pady=20, sticky="we")

video_author = customtkinter.CTkLabel(frame_data_video, width=280, text=text_title, justify="left")
video_author.grid(row=1, column=1, padx=20, pady=10, sticky="ew")

text_image = customtkinter.CTkLabel(frame_data_video, text="Image: ")
text_image.grid(row=2, column=0, padx=(20, 0), pady=20, sticky="we")

image_url = "https://fileinfo.com/img/ss/xl/jpeg_43.png"
response = urllib.request.urlopen(image_url)
image_data = response.read()

# Создание объекта изображения
image = Image.open(io.BytesIO(image_data))

# Создание CTkImage
# ctk_image = customtkinter.CTkImage(image)

# Создание CTkLabel для отображения изображения
# image_label = customtkinter.CTkLabel(app, image=ctk_image)
# image_label.grid(row=2, column=1, padx=(20, 0))

# from src.windowMessage import show_message_link


def show_message_link(title, link):
    def close_app():
        app_mess.destroy()

    app_mess = tkinter.Tk()
    app_mess.title(title)
    app_mess.geometry("350x200")
    message_label = customtkinter.CTkLabel(app_mess, text="Downloaded is completed")
    message_label.grid(row=0, column=0)

    text_label = customtkinter.CTkLabel(app_mess, text="Open folder", text_color="steelblue1", cursor="hand2")
    text_label.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
    # text_label.bind("<Button-1>", open_directory)

    button = customtkinter.CTkButton(app_mess, text="Close", command=close_app)
    button.grid()

    app_mess.mainloop()

def on_message():
    show_message_link("title", "./src/")


button_message = customtkinter.CTkButton(app, text="message", command=on_message)
button_message.grid()

app.mainloop()