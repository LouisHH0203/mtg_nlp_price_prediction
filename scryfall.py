import requests

def call():
    req = requests.get('https://api.scryfall.com/cards/search?as=grid&order=name&q=%28game%3Apaper%29+legal%3Acommander')

    if req.status_code == 200:
        data = req.json()

    return data

def call_all(url='https://api.scryfall.com/cards/search?as=grid&order=name&q=%28game%3Apaper%29+legal%3Acommander'):
    all_cards = []

    while url:
        req = requests.get(url)

        if req.status_code == 200:
            data = req.json()
            all_cards.extend(data.get('data', []))
            url = data.get('next_page')
        else:
            print(f"Error: {req.status_code}")
            break

    return all_cards
