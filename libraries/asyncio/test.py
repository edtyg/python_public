"""
asyncio example
"""
import asyncio
import os
from random import randint

import aiohttp
from logger_client import LoggerClient

# The highest Pokemon id
MAX_POKEMON = 898


class AsyncBasics(LoggerClient):
    """async example"""

    def __init__(self, file_path, file_name, save_mode):
        LoggerClient.__init__(self, file_path, file_name, save_mode)
        self.timeout = 5

    async def get_random_pokemon_name(self):
        """gets a random pokemon"""
        async with aiohttp.ClientSession() as session:
            pokemon_id = randint(1, MAX_POKEMON)
            pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
            async with session.get(pokemon_url) as response:
                response_json = await response.json()
                pokemon_name = response_json["name"]
                return pokemon_name

    async def process_pokemon(self):
        """include sleeping time in process"""
        pokemon_name = await self.get_random_pokemon_name()
        self.logger.info(pokemon_name)
        print(pokemon_name)

    async def main(self) -> None:
        """main function"""
        tasks = []
        for _ in range(5):
            task = asyncio.create_task(self.process_pokemon())
            tasks.append(task)
            await asyncio.sleep(1)

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    full_path = os.path.realpath(__file__)
    save_path = os.path.dirname(full_path) + "/"
    FILENAME = "pokemon.log"

    client = AsyncBasics(save_path, FILENAME, "a")
    asyncio.run(client.main())
