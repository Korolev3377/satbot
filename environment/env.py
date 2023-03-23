import os
from abc import ABC

class Env(ABC):
    path = os.environ.get("BOT_TOKEN")
    with open(path, 'r') as file:
        token = file.read()
    TOKEN = token
