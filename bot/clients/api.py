from bot.clients.operations import OperationsClient
from bot.clients.users import UserClient
from bot.config import conf


class ApiClient:
    def __init__(self, url: str) -> None:
        self.operations = OperationsClient(url)
        self.users = UserClient(url)


api = ApiClient(url=conf.base_url)
