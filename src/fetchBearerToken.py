from pytube import innertube, request
import time
import json
from classesWidgets import BaseFrame, BaseLabel, BaseButton, BaseComboBox, BaseLabelText, BaseProgressBar, BaseSwitch
import windowAuthentication
from tkinter.messagebox import showinfo
# from interface import Interface
from customtkinter.windows.ctk_toplevel import CTkToplevel


# YouTube on TV client secrets
_client_id = innertube._client_id
_client_secret = innertube._client_secret


def fetch_bearer_token(self):
    """Fetch an OAuth token."""

    print("Я подключаю гугл")
    # Subtracting 30 seconds is arbitrary to avoid potential time discrepencies
    start_time = int(time.time() - 30)
    data = {
        'client_id': _client_id,
        'scope': 'https://www.googleapis.com/auth/youtube'
    }
    response = request._execute_request(
        'https://oauth2.googleapis.com/device/code',
        'POST',
        headers={
            'Content-Type': 'application/json'
        },
        data=data
    )
    response_data = json.loads(response.read())
    verification_url = response_data['verification_url']
    user_code = response_data['user_code']

    # модальное окно из модуля windowAuthentication
    auth = windowAuthentication.ModalWindow(verification_url=verification_url, user_code=user_code)


    print(f'Please open {verification_url} and input code {user_code}')
    input('Press enter when you have completed this step.')


    data = {
        'client_id': _client_id,
        'client_secret': _client_secret,
        'device_code': response_data['device_code'],
        'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
    }
    response = request._execute_request(
        'https://oauth2.googleapis.com/token',
        'POST',
        headers={
            'Content-Type': 'application/json'
        },
        data=data
    )
    response_data = json.loads(response.read())

    self.access_token = response_data['access_token']
    self.refresh_token = response_data['refresh_token']
    self.expires = start_time + response_data['expires_in']
    self.cache_tokens()


innertube.InnerTube.fetch_bearer_token = fetch_bearer_token


# def open_modal(url_auth, kod_aut):
#     print("Open modal")
#     modal_window = CTkToplevel()
#     modal_window.grab_set()  # Установка фокуса на модальное окно
#     modal_window.title("Authentication")
#     modal_window.geometry("200x100")
#     #inputDialog (modul ctk_input_dialog.py
#     label = BaseLabelText(modal_window, text="You need to authenticate\nPlease open")
#     label.pack()
#
#     button_Ok = BaseButton(modal_window, text="OK", command=ok_event)
#     button_Ok.pack()
#
#
# def ok_event(event=None):
#     print(event)
#     # self._user_input = self._entry.get()
#     event.grab_release()
#     event.destroy()



