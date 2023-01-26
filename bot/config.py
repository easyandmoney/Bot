import os
from dataclasses import dataclass


@dataclass
class Config:
    api_key: str


def load() -> Config:
    return Config(
        api_key=os.environ['API_KEY'],
    )


conf = load()
