from typing import Union, Tuple, Optional

from customtkinter.windows.widgets import CTkButton, CTkLabel, CTkEntry
from classesWidgets import BaseLabel, BaseLabelText, BaseButton, BaseFrame
from customtkinter.windows.widgets.theme import ThemeManager
from customtkinter.windows.ctk_toplevel import CTkToplevel
from customtkinter.windows.widgets.font import CTkFont
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By


class ModalWindow(CTkToplevel):
    """
    Dialog with extra window, message, entry widget, cancel and ok button.
    For detailed information check out the documentation.
    """

    def __init__(self,
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 entry_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 entry_border_color: Optional[Union[str, Tuple[str, str]]] = None,
                 entry_text_color: Optional[Union[str, Tuple[str, str]]] = None,

                 verification_url: str = None,
                 user_code: str = None,

                 title: str = "Authentication",
                 font: Optional[Union[tuple, CTkFont]] = None,
                 text: str = "Выполните аутентификацию"):
        super().__init__(fg_color=fg_color)
        self.verification_url = verification_url
        self.user_code = user_code
        self.center_window(400, 250)

        self._fg_color = ThemeManager.theme["CTkToplevel"]["fg_color"] if fg_color is None else self._check_color_type(
            fg_color)
        self._text_color = ThemeManager.theme["CTkLabel"][
            "text_color"] if text_color is None else self._check_color_type(button_hover_color)
        self._button_fg_color = ThemeManager.theme["CTkButton"][
            "fg_color"] if button_fg_color is None else self._check_color_type(button_fg_color)
        self._button_hover_color = ThemeManager.theme["CTkButton"][
            "hover_color"] if button_hover_color is None else self._check_color_type(button_hover_color)
        self._button_text_color = ThemeManager.theme["CTkButton"][
            "text_color"] if button_text_color is None else self._check_color_type(button_text_color)
        self._entry_fg_color = ThemeManager.theme["CTkEntry"][
            "fg_color"] if entry_fg_color is None else self._check_color_type(entry_fg_color)
        self._entry_border_color = ThemeManager.theme["CTkEntry"][
            "border_color"] if entry_border_color is None else self._check_color_type(entry_border_color)
        self._entry_text_color = ThemeManager.theme["CTkEntry"][
            "text_color"] if entry_text_color is None else self._check_color_type(entry_text_color)

        self._user_input: Union[str, None] = None
        self._running: bool = False
        self._title = title
        self._text = text
        self._font = font

        self.title(self._title)

        self.lift()  # lift window on top
        self.attributes("-topmost", True)  # stay on top
        self.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.after(10,
                   self._create_widgets)  # create widgets with slight delay, to avoid white flickering of background
        self.resizable(False, False)
        self.grab_set()  # make other windows not clickable

    def _create_widgets(self):
        # self.grid_columnconfigure((0, 1), weight=1)
        # self.rowconfigure(0, weight=1)

        self.frame = BaseFrame(master=self)
        self.frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.frame.grid_columnconfigure((0, 1), weight=1)

        self._label = BaseLabelText(master=self.frame,
                                    width=300,
                                    wraplength=300,
                                    fg_color="transparent",
                                    # text_color=self._text_color,
                                    text=self._text,
                                    font=self._font
                                    )
        self._label.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

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
        self.label_url.bind("<Button-1>", lambda event: self.open_authentication(event))

        self.label_text_info = BaseLabel(master=self.frame,
                                             text="and input code"
                                             )
        self.label_text_info.grid(row=3, column=0, columnspan=2, padx=5, pady=(5, 2))

        self._entry = CTkEntry(master=self.frame,
                               width=230,
                               fg_color=self._entry_fg_color,
                               border_color=self._entry_border_color,
                               text_color=self._entry_text_color,
                               font=self._font,
                               justify="center")

        self._entry.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
        self._entry.insert(0, self.user_code)
        self._entry.bind("<KeyPress>", self.ignore_keyboard)

        self.label_info_text = BaseLabelText(master=self.frame,
                                             text="Press OK when you have completed this step."
                                             )
        self.label_info_text.grid(row=5, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

        self._ok_button = BaseButton(master=self.frame,
                                    width=100,
                                    text='Ok',
                                    font=self._font,
                                    command=self._ok_event)
        self._ok_button.grid(row=6, column=0, columnspan=1, padx=(10, 10), pady=(0, 10), sticky="ew")

        self._cancel_button = BaseButton(master=self.frame,
                                        width=100,
                                        text='Cancel',
                                        font=self._font,
                                        command=self._cancel_event)
        self._cancel_button.grid(row=6, column=1, columnspan=1, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.after(150, lambda: self._entry.focus())  # set focus to entry with slight delay, otherwise it won't work
        self._entry.bind("<Return>", self._ok_event)

        self.grid_rowconfigure(0, weight=1)  # Растягиваем строку 0 по вертикали
        self.grid_columnconfigure(0, weight=1)

    def _ok_event(self, event=None):
        # self._user_input = self._entry.get()
        self.grab_release()
        self.destroy()
        return True

    def _on_closing(self):
        self.grab_release()
        self.destroy()
        return False

    def _cancel_event(self):
        self.grab_release()
        self.destroy()
        return False

    def ignore_keyboard(self, event):
        """ Игнорирование на нажатие клавиш """
        return "break"  # Игнорируем ввод с клавиатуры

    def center_window(self, app_width, app_height):
        """ centering app window """

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width - app_width) // 2
        y = (screen_height - app_height) // 3

        self.geometry(f"{app_width}x{app_height}+{x}+{y}")

    def open_authentication(self, event):
        print("Auth google")
        # page = open(self.verification_url)
        driver = webdriver.Firefox()
        driver.get(self.verification_url)
        input_element = driver.find_element(By.NAME, "code")
        input_element.send_keys(self.user_code)