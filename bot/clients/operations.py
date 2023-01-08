import requests


class OperationsClient:
    def __init__(self, url: str) -> None:
        self.url = url

    def add(self, user_id: int, category: str, amount: int, is_income: bool):
        url = f'{self.url}/api/v1/users/{user_id}/operations/'
        payload = {
            'name': category,
            'amount': amount,
            'type_income_expenses': 'income' if is_income else 'expense',
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.request('POST', url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
