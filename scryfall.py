import requests

def call():
    req = requests.get('https://api.scryfall.com/cards/search?as=grid&order=name&q=%28game%3Apaper%29+legal%3Acommander')

    if req.status_code == 200:
        data = req.json()

    return data
