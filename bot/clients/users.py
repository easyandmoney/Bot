import requests


class UserClient:
    def __init__(self, url: str) -> None:
        self.url = url

    def get_user(self, user_id: int):
        url = f'{self.url}/api/v1/users/{user_id}'
        response = requests.request('GET', url)
        response.raise_for_status()

    def get_by_tg_id(self, tg_id: int):
        url = f'{self.url}/api/v1/users/telegram/{tg_id}'
        response = requests.request('GET', url)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()

    def add_user(self, tg_id: str, name: str, email: str | None):
        url = f'{self.url}/api/v1/users/'
        payload = {
            'tg_id': tg_id,
            'name': name,
            'email': email,
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.request('POST', url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
