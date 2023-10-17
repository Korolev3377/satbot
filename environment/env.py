import os

path = os.environ.get("BOT_TOKEN")
with open(path, 'r') as file:
    TOKEN = file.read()
