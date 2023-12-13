import requests
import aiohttp
import asyncio
import time


url = 'https://api.scryfall.com/cards/search?as=grid&order=name&q=%28game%3Apaper%29+legal%3Acommander'

async def make_api_call(session, url):
    try:
        async with session.get(url) as response:
            response.raise_for_status()
            return await response.json()
    except aiohttp.ClientError as e:
        print(f"Error making API call: {e}")
        return None

async def fetch_data(session, url):
    data = await make_api_call(session, url)
    return data

async def call_all_parallel(api_url, requests_per_second=10):
    all_cards = []

    async with aiohttp.ClientSession() as session:
        while api_url:
            start_time = time.time()

            tasks = [fetch_data(session, api_url)]
            done, _ = await asyncio.wait(tasks)

            for future in done:
                try:
                    data = future.result()
                    if data:
                        all_cards.extend(data.get('data', []))
                        api_url = data.get('next_page') if data.get('has_more') else None
                except Exception as e:
                    print(f"Error fetching data from {api_url}: {e}")

            elapsed_time = time.time() - start_time


            target_delay = 1 / requests_per_second
            actual_delay = max(0, target_delay - elapsed_time)


            await asyncio.sleep(actual_delay)

    return all_cards
