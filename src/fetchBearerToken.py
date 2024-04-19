from pytube import innertube, request
import time
import json
from modalWindow import ToplevelWindow
import os
import pathlib


# Local imports

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


    # модальное окно из модуля modalWindow
    auth = ToplevelWindow(verification_url=verification_url, user_code=user_code)
    auth.my_wait_window()
    print(auth.auth_use)
    if auth.auth_use:


        # print(f'Please open {verification_url} and input code {user_code}')
        # input('Press enter when you have completed this step.')


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
        # self.allow_cache = self.allow_oauth_cache
        # innertube.InnerTube.cache_tokens(self)
        cache_tokens(self)
        # return True
    else:
        print("No custom authentication")



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

# innertube.InnerTube.fetch_bearer_token = fetch_bearer_token

