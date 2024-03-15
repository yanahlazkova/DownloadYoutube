import customtkinter
import os, tkinter
from tkinter import messagebox


# todo: you can create a class "App", "MainApp" or "Window" from this code
# to maintain multiple windows you got in your application
# for extra window it's recommended to use class TopLevel widget:
# https://customtkinter.tomschimansky.com/documentation/windows/toplevel

def open_window_message(text_title, text_message):
    messagebox.showinfo(text_title, text_message)


def open_window_error(text_error):
    messagebox.showerror("Error...", text_error)


def show_message_link(title, link):

    # todo: same method one more time
    # maybe we need a "helpers" file instead?
    def center_window(app_width, app_height):
        screen_width = app.winfo_screenwidth()
        screen_height = app.winfo_screenheight()

        x = (screen_width - app_width) // 2
        y = (screen_height - app_height) // 2

        app.geometry(f"{app_width}x{app_height}+{x}+{y}")

    def close_app():
        print("Destroying the application...", dir(app))
        app.destroy()
        # app.quit()

    def open_directory(event):
        text_link = os.path.dirname(link)
        os.startfile(text_link)

    # customtkinter.set_ctk_parent_class(tkinter.Tk)
    customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("green")

    app = customtkinter.CTk()
    app.title(title)
    # app.geometry("350x200")
    frame_app = customtkinter.CTkFrame(app)
    frame_app.pack(pady=20)

    message_label = customtkinter.CTkLabel(frame_app, text="Downloaded is completed")
    message_label.grid(row=0, column=0)

    text_label = customtkinter.CTkLabel(frame_app, text="Open folder", text_color="steelblue1", cursor="hand2")
    text_label.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
    text_label.bind("<Button-1>", open_directory)

    button = customtkinter.CTkButton(app, text="Close", command=close_app)
    button.pack()

    app.update()
    width = 250 #app.winfo_width()
    height = 200 #app.winfo_height()

    center_window(width, height)

    app.mainloop()
