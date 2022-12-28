
import requests


base_url = 'http://127.0.0.1:5000'


class OperationsClient:
    def __init__(self, url: str) -> None:
        self.url = url


    def add(self, user_id: int, category: str, amount: int):
        url = f'{self.url}/api/v1/users/{user_id}/operations/'
        payload = {
            "name": category,
            "amount": amount,
        }
        headers = {"Content-Type": "application/json"}
        response = requests.request("POST", url, json=payload, headers=headers)
        response.raise_for_status()
        print(response.json())


class ApiClient:
    def __init__(self, url: str) -> None:
        self.operations = OperationsClient(url)


api = ApiClient(url=base_url)

