import os
from dataclasses import dataclass


@dataclass
class Config:
    api_key: str
    base_url: str


def load() -> Config:
    return Config(
        api_key=os.environ['API_KEY'],
        base_url=os.environ['BASE_URL'],
    )


conf = load()

