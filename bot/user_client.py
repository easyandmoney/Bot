import requests

base_url = 'http://127.0.0.1:5000'


class UserClient:
    def __init__(self, url: str) -> None:
        self.url = url

    def get_user(self, user_id: int):
        url = f'{self.url}/api/v1/users/{user_id}'
        response = requests.request('GET', url)
        response.raise_for_status()

    def add_user(self, name: str, email: str):
        url = f'{self.url}/api/v1/users/'
        payload = {
            'name': name,
            'email': email,
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.request('POST', url, json=payload, headers=headers)
        response.raise_for_status()


class ApiClient:
    def __init__(self, url: str) -> None:
        self.user = UserClient(url)


api_user = ApiClient(base_url)
