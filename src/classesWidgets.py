"""Классы виджетов для наследования свойств """
from customtkinter import CTkFrame, CTkButton, CTkLabel, CTkProgressBar, CTkRadioButton, CTkComboBox, CTkTextbox, \
    CTkSwitch, CTk


class BaseFrame(CTkFrame):
    def __init__(self, master=None, **kwargs):
        # Устанавливаем общие аргументы для всех фреймов
        self.border_width = kwargs.pop("border_width", 2)
        self.border_color = kwargs.pop("border_color", ("#3B8ED0", "#2FA572"))

        super().__init__(master, **kwargs)

        # Применяем общие аргументы к каждому фрейму
        self.configure(border_width=self.border_width, border_color=self.border_color)


class BaseButton(CTkButton):
    def __init__(self, master=None, **kwargs):
        # Устанавливаем общие аргументы для всех кнопок
        self.fg_color = kwargs.pop("fg_color", ("#3B8ED0", "#2FA572"))
        self.hover_color = kwargs.pop("hover_color", ("#87CEFA", "#106A43"))
        self.text_color = kwargs.pop("text_color", ("gray98", "#DCE4EE"))
        self.text_color_disabled = kwargs.pop("text_color_disabled", ("gray78", "gray68"))

        super().__init__(master, **kwargs)

        # Применяем общие аргументы к каждой кнопке
        self.configure(fg_color=self.fg_color,
                       hover_color=self.hover_color,
                       text_color=self.text_color,
                       text_color_disabled=self.text_color_disabled)


class BaseComboBox(CTkComboBox):
    def __init__(self, master=None, **kwargs):
        # Устанавливаем общие аргументы
        self.fg_color = kwargs.pop("fg_color", ("#F9F9FA", "#343638"))
        self.border_color = kwargs.pop("border_color", ("#3B8ED0", "#2FA572"))
        self.button_color = kwargs.pop("button_color", ("#3B8ED0", "#2FA572"))
        self.button_hover_color = kwargs.pop("button_hover_color", ("#87CEFA", "#106A43"))
        self.text_color = kwargs.pop("text_color", ("gray10", "gray80"))
        self.text_color_disabled = kwargs.pop("text_color_disabled", ("gray50", "gray45"))

        super().__init__(master, **kwargs)

        # Применяем общие аргументы
        self.configure(fg_color=self.fg_color,
                       border_color=self.border_color,
                       button_color=self.button_color,
                       button_hover_color=self.button_hover_color,
                       text_color=self.text_color,
                       text_color_disabled=self.text_color_disabled)

class BaseLabelText(CTkLabel):
    def __init__(self, master=None, **kwargs):
        # Устанавливаем общие аргументы
        self.text_color = kwargs.pop("text_color", ("#3B8ED0", "#2FA572"))

        super().__init__(master, **kwargs)

        self.configure(text_color=self.text_color)

class BaseSwitch(CTkSwitch):
    def __init__(self, master=None, **kwargs):
        # Устанавливаем общие аргументы
        self.fg_color = kwargs.pop("fg_color", ("#87CEFA", "#4A4D50"))
        self.progress_color = kwargs.pop("progress_color", ("#87CEFA", "#2FA572"))
        self.button_color = kwargs.pop("button_color", ("#1F6AA5", "#D5D9DE"))
        self.button_hover_color = kwargs.pop("button_hover_color", ("#4A4D50", "gray100"))
        self.text_color = kwargs.pop("text_color", ("#6495ED", "gray80"))

        super().__init__(master, **kwargs)

        self.configure(fg_color=self.fg_color,
                       progress_color=self.progress_color,
                       button_color=self.button_color,
                       button_hover_color=self.button_hover_color,
                       text_color=self.text_color)

class BaseProgressBar(CTkProgressBar):
    def __init__(self, master=None, **kwargs):
        # Устанавливаем общие аргументы
        self.fg_color = kwargs.pop("fg_color", ("#939BA2", "#4A4D50"))
        self.progress_color = kwargs.pop("progress_color", ("#3B8ED0", "#2FA572"))
        self.border_color = kwargs.pop("border_color", ("gray", "gray"))

        super().__init__(master, **kwargs)

        self.configure(fg_color=self.fg_color,
                       progress_color=self.progress_color,
                       border_color=self.border_color)