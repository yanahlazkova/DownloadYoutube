import customtkinter
import os
from tkinter import messagebox


def open_window_message(text_title, text_message):
    messagebox.showinfo(text_title, text_message)


def open_window_error(text_error):
    messagebox.showerror("Error...", text_error)

def show_message_link(title, message, link):
    def center_window(app, app_width, app_height):
        screen_width = app.winfo_screenwidth()
        screen_height = app.winfo_screenheight()

        x = (screen_width - app_width) // 2
        y = (screen_height - app_height) // 2

        app.geometry(f"{app_width}x{app_height}+{x}+{y}")

    def close_app():
        app.destroy()

    def open_directory(event):
        text_link = os.path.dirname(link)
        os.startfile(text_link)

    # customtkinter.set_ctk_parent_class(customtkinter.CTk)
    customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("green")

    app = customtkinter.CTk()
    app.title(title)
    # app.geometry("350x200")

    message_label = customtkinter.CTkLabel(app, text=message)
    message_label.grid(row=0, column=0)

    text_label = customtkinter.CTkLabel(app, text="Open folder", text_color="steelblue1", cursor="hand2")
    text_label.grid(row=1, column=0, padx=20, pady=20)
    text_label.bind("<Button-1>", open_directory)

    button = customtkinter.CTkButton(app, text="Close", command=close_app)
    button.grid(pady=20)
    app.update()
    center_window(app, app.winfo_width(), app.winfo_height())
    app.mainloop()