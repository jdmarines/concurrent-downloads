import concurrent.futures
import os
import typing as t
import requests
import utils

def download_and_save_pokemon(pokemon, output_dir):
    """Download and save a single pokemon."""
    with requests.Session() as session:
        content = utils.maybe_download_sprite(session, pokemon["Sprite"])
        if content is not None:
            target_dir = os.path.join(output_dir, pokemon["Type1"])
            utils.maybe_create_dir(target_dir)
            filepath = os.path.join(target_dir, pokemon["Pokemon"] + ".png")
            utils.write_binary(filepath, content)

def download_and_save_all_pokemons(pokemons, output_dir):
    """Download and save all pokemons using multithreading."""
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        
        futures = [executor.submit(download_and_save_pokemon, pokemon, output_dir) for pokemon in pokemons]

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()  
            except Exception as exc:
                print(f"Error al descargar un Pokémon: {exc}")

@utils.timeit
def main(output_dir: str, inputs: t.List[str]):
    """Download for all inputs and place them in output_dir."""
    utils.maybe_create_dir(output_dir)
    pokemons = utils.read_pokemons(inputs)
    download_and_save_all_pokemons(pokemons, output_dir)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", help="Directory to store the data")
    parser.add_argument("inputs", nargs="+", help="List of files with metadata")
    args = parser.parse_args()

    utils.maybe_remove_dir(args.output_dir)
    main(args.output_dir, args.inputs)

