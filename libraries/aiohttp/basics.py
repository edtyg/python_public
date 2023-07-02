"""
pip install aiohttp
aiohttp.__version__
"""
import asyncio
from random import randint

import aiohttp

# The highest Pokemon id
MAX_POKEMON = 898


async def get_random_pokemon_name():
    """gets a random pokemon"""
    async with aiohttp.ClientSession() as session:
        pokemon_id = randint(1, MAX_POKEMON)
        pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
        async with session.get(pokemon_url) as response:
            response_json = await response.json()
            pokemon_name = response_json["name"]
            print(pokemon_name)
            return pokemon_name


async def main():
    """running function"""
    await get_random_pokemon_name()


asyncio.run(main())
