from pytube import innertube, request
import time
import json
from modalWindow import ToplevelWindow
import os
import pathlib
import requests


# Local imports
access_token = None
# YouTube on TV client secrets
_client_id = innertube._client_id
_client_secret = innertube._client_secret
_cache_dir = pathlib.Path(__file__).parent.resolve() / '__cache__'
_token_file = os.path.join(_cache_dir, 'tokens.json')


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

    # token_user = check_token(self)
    # print("token_user", token_user)
    # if token_user == None:
    # модальное окно из модуля modalWindow
    auth = ToplevelWindow(verification_url=verification_url, user_code=user_code)
    auth.my_wait_window()
    if auth.auth_use:

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
        print("tokens: ", self.access_token, self.refresh_token, self.expires)
        cache_tokens(self)

        # return True
    else:
        print("No custom authentication")
        # return False


def cache_tokens(self):
    """Cache tokens to file if allowed."""
    if not self.allow_cache:
        return
    print("not allow_cache", self.access_token, self.refresh_token)

    data = {
        'access_token': self.access_token,
        'refresh_token': self.refresh_token,
        'expires': self.expires
    }
    if not os.path.exists(_cache_dir):
        os.mkdir(_cache_dir)
    with open(_token_file, 'w') as f:
        print("cache_tokens")
        json.dump(data, f)


# def check_token(self):
#     """ проверка аутентификации пользователя """
#     # Данные для запроса токена
#     scope = 'https://www.googleapis.com/auth/youtube'  # Область, для которой запрашивается токен
#     data = {
#         'client_id': _client_id,
#         'client_secret': _client_secret,
#         'scope': scope,
#         'grant_type': 'client_credentials'  # Используем client_credentials flow
#     }
#
#     # URL для запроса токена
#     token_url = 'https://oauth2.googleapis.com/token'
#
#     # Отправляем POST-запрос для получения токена
#     response = requests.post(token_url, data=data)
#
#     # Проверяем статус-код ответа
#     if response.status_code == 200:
#         # Парсим JSON-ответ и получаем токен доступа
#         token_data = response.json()
#         access_token = token_data.get('access_token')
#         expires_in = token_data.get('expires_in')  # Срок действия токена в секундах
#         expires_at = int(time.time()) + expires_in  # Вычисляем время истечения токена
#         print("Token obtained successfully.")
#         return access_token, expires_at
#     else:
#         print("Failed to obtain token.")
#         return None
# innertube.InnerTube.fetch_bearer_token = fetch_bearer_token

