from datetime import datetime

import orjson
import requests


class OperationsClient:
    def __init__(self, url: str) -> None:
        self.url = url

    def add(
        self,
        user_id: int,
        category: str,
        amount: int,
        is_income: bool,
        payment_date: datetime,
    ):
        url = f'{self.url}/api/v1/users/{user_id}/operations/'
        payload = {
            'name': category,
            'amount': amount,
            'type_income_expenses': 'income' if is_income else 'expense',
            'payment_date': payment_date,
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.request('POST', url, data=orjson.dumps(payload), headers=headers)
        response.raise_for_status()
        return response.json()

# adding func connected with the backend
    def get_expenses(
        self,
        user_id: int,
        payment_date: str,
    ):
        url = f'{self.url}/api/v1/users/{user_id}/operations/{payment_date}'
        headers = {'Content-Type': 'application/json'}
        response = requests.request('GET', url=url, headers=headers)
        response.raise_for_status()
        return response.json()
