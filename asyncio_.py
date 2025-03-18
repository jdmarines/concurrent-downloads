import asyncio
import os
import typing as t
import aiohttp
import utils

async def download_and_save_pokemon(session: aiohttp.ClientSession, pokemon: dict, output_dir: str):
    """Download and save a single pokemon asynchronously."""
    content = await utils.async_maybe_download_sprite(session, pokemon["Sprite"])
    if content is not None:
        target_dir = os.path.join(output_dir, pokemon["Type1"])
        utils.maybe_create_dir(target_dir)
        filepath = os.path.join(target_dir, pokemon["Pokemon"] + ".png")
        utils.write_binary(filepath, content)

async def download_and_save_all_pokemons(pokemons: t.List[dict], output_dir: str):
    """Download and save all pokemons using asyncio."""
    async with aiohttp.ClientSession() as session:
        # Crea una lista de tareas asincrónicas
        tasks = [
            download_and_save_pokemon(session, pokemon, output_dir)
            for pokemon in pokemons
        ]
        # Espera a que se completen todas las tareas concurrentemente
        await asyncio.gather(*tasks)

@utils.timeit
def main(output_dir: str, inputs: t.List[str]):
    """Download for all inputs and place them in output_dir."""
    utils.maybe_create_dir(output_dir)
    pokemons = utils.read_pokemons(inputs)

    # Ejecuta la función principal asincrónica
    asyncio.run(download_and_save_all_pokemons(pokemons, output_dir))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", help="Directory to store the data")
    parser.add_argument("inputs", nargs="+", help="List of files with metadata")
    args = parser.parse_args()

    utils.maybe_remove_dir(args.output_dir)
    main(args.output_dir, args.inputs)
