from customtkinter.windows.ctk_toplevel import CTkToplevel
from customtkinter import CTkToplevel
from customtkinter.windows.widgets import CTkButton, CTkEntry
from CTkToolTip import *
from classesWidgets import BaseLabel, BaseLabelText, BaseButton, BaseFrame
import webbrowser
from helpers import Helpers
# from selenium.webdriver.common.by import By
from tkinter import Menu, PhotoImage, LEFT


class ToplevelWindow(CTkToplevel):
    """
    Modal window for custom authentication
    """
    auth_use = None

    def __init__(self, verification_url: str = None,
                 user_code: str = None, *args, **kwargs):
        self.icon_edge = PhotoImage(file=".\\data\\Edge.png")
        self.icon_chrome = PhotoImage(file=".\\data\\Chrome.png")
        self.icon_firefox = PhotoImage(file=".\\data\\Firefox.png")
        self.icon_opera = PhotoImage(file=".\\data\\Opera.png")

        super().__init__(*args, **kwargs)
        self.verification_url = verification_url
        self.user_code = user_code
        self.center_window(400, 250)
        self.title("Google authentication")
        self.lift()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.after(10, self.create_widgets)
        self.resizable(False, False)
        self.grab_set()  # make other windows not clickable

    def create_widgets(self):
        self.frame = BaseFrame(master=self)
        self.frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.frame.grid_columnconfigure((0, 1), weight=1)

        self.label = BaseLabelText(master=self.frame,
                                   text="Выполните аутентификацию",
                                   width=300,
                                   wraplength=300,
                                   fg_color="transparent"
                                   )
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.label_text = BaseLabel(master=self.frame,
                                    text="Please open"
                                    )
        self.label_text.grid(row=1, column=0, padx=10, pady=5, sticky="ne")

        self.label_url = BaseLabelText(master=self.frame,
                                       text_color="steelblue1",
                                       text=str(self.verification_url),
                                       cursor="hand2"
                                       )
        self.label_url.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        self.label_url.bind("<Button-1>", lambda event: self.show_menu(event))
        # self.label_url.bind("<Button-3>", show_menu)

        self.tooltip = CTkToolTip(self.label_url)
        self.tooltip.configure(
            message='Нажмите левую кнопку мыши для выбора браузера\n Код будет скопирован в буфер.\n Для вставки используйте <Ctrl + C>',
            text_color=("#3B8ED0", "#2FA572"),
            bg_color=("#E0FFFF")
        )

        self.label_text_info = BaseLabel(master=self.frame,
                                         text="and input code"
                                         )
        self.label_text_info.grid(row=3, column=0, columnspan=2, padx=5, pady=(5, 2))

        self.entry_code = CTkEntry(master=self.frame,
                                   width=230,
                                   justify="center")

        self.entry_code.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
        self.entry_code.insert(0, self.user_code)
        self.entry_code.bind("<KeyPress>", self.ignore_keyboard)

        self.tooltip = CTkToolTip(self.entry_code)
        self.tooltip.configure(message='Copy this code: "Ctrl + C" ',
                               text_color=("#3B8ED0", "#2FA572"),
                               bg_color=("#E0FFFF")
                               )

        self.label_info_text = BaseLabelText(master=self.frame,
                                             text="Press OK when you have completed this step."
                                             )
        self.label_info_text.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self.ok_button = BaseButton(master=self.frame,
                                    width=100,
                                    text='Ok',
                                    command=self.ok_event)
        self.ok_button.grid(row=6, column=0, columnspan=1, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.cancel_button = BaseButton(master=self.frame,
                                        width=100,
                                        text='Cancel',
                                        command=self.cancel_event)
        self.cancel_button.grid(row=6, column=1, columnspan=1, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.after(150,
                   lambda: self.entry_code.focus())  # set focus to entry with slight delay, otherwise it won't work
        # self.entry_code.bind("<Return>", self._ok_event)

        self.grid_rowconfigure(0, weight=1)  # Растягиваем строку 0 по вертикали
        self.grid_columnconfigure(0, weight=1)

    def ok_event(self, event=None):
        self.auth_use = True
        self.grab_release()
        self.destroy()
        # return True

    def on_closing(self):
        self.auth_use = False
        self.grab_release()
        self.destroy()
        # return False

    def cancel_event(self):
        self.auth_use = False
        self.grab_release()
        self.destroy()
        # return False

    def show_menu(self, event):
        menu = Menu(self.label_url, tearoff=0)

        menu.add_command(label="Открыть в Edge",
                         command=lambda: self.open_browser("Edge"))
        menu.add_command(label="Открыть в Chrome",
                         command=lambda: self.open_browser("Chrome"))
        menu.add_command(label="Открыть в Firefox",
                         command=lambda: self.open_browser("Firefox"))
        menu.add_command(label="Открыть в Opera",
                         command=lambda: self.open_browser("Opera"))
        menu.add_separator()
        menu.add_command(label="Копировать", command=self.copy_url)
        x, y = event.widget.winfo_pointerxy()
        menu.tk_popup(x, y)

    def ignore_keyboard(self, event):

        if event.keysym == 'c' and event.state & 0x4:  # Проверяем, что нажата клавиша 'C' и удерживается Ctrl
            print("Copy_code")
            text = event.widget.selection_get()  # Получаем выделенный текст
            self.frame.clipboard_clear()  # Очищаем буфер обмена
            self.frame.clipboard_append(text)  # Копируем текст в буфер обмена""" Игнорирование на нажатие клавиш """
        else:
            return "break"  # Игнорируем ввод с клавиатуры

    def copy_url(self):
        print("Copy_url")
        text = str(self.verification_url)
        self.frame.clipboard_clear()
        self.frame.clipboard_append(text)
        print(text)

    def center_window(self, app_width, app_height):
        """ centering app window """

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - app_width) // 2
        y = (screen_height - app_height) // 3

        self.geometry(f"{app_width}x{app_height}+{x}+{y}")

    def open_browser(self, browser):
        print("Auth google in", browser)
        # поиск директории браузера
        browser_dir = Helpers.find_browser_registry(browser)
        Helpers.show_info_window()
        if browser_dir:
            webbrowser.register(browser, None,
                                webbrowser.BackgroundBrowser(browser_dir)
                                )
            br_dir = webbrowser.get(browser).open_new_tab(self.verification_url)
        else:
            br_dir = webbrowser.open(self.verification_url)
        print(br_dir)

        # поместим код в буфер обмена
        text = str(self.user_code)
        self.frame.clipboard_clear()
        self.frame.clipboard_append(text)

    # @staticmethod
    def my_wait_window(self):
        super().wait_window(self)
