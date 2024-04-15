from classesWidgets import BaseButton, BaseLabelText, BaseLabel
from customtkinter.windows.ctk_toplevel import CTkToplevel
from customtkinter import CTkLabel, CTkButton
from helpers import Helpers
from classesWidgets import BaseButton, BaseLabel, BaseLabelText


def open_modal_window(self, parent_window=None, url=None, kod=None):
    print("modal window", url, kod)
    modal_window = CTkToplevel(parent_window)
    modal_window.title("Authenticate")
    Helpers.center_window(modal_window, 300, 200)
    modal_window.grab_set()
    create_widgets(master=modal_window, url=url, kod=kod)
    modal_window.mainloop()


def create_widgets(master, url, kod):
    print("Create_widgets")
    widget_label_info = BaseLabelText(master, text="Open page")
    widget_label_info.grid(row=0, column=0)

    widget_label_url = BaseLabel(master, text=url, text_color="steelblue1", cursor="hand2")
    widget_label_url.grid(row=1, column=0)

    widget_button_ok = BaseButton(master, text="OK", command=lambda event: ok_event)
    widget_button_ok.grid(row=2, column=0)

    master.grid_columnconfigure(0, weight=1)  # Растягиваем колонку
    master.grid_rowconfigure(0, weight=1)  # Растягиваем строку
    master.grid_rowconfigure(1, weight=1)  # Растягиваем строку
    master.grid_rowconfigure(2, weight=1)  # Растягиваем строку

def ok_event(master, event):
    master.grab_release()
    master.destroy()
