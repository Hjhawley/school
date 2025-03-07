import requests
import os
import json
from PIL import Image

# Directory to save images
IMAGE_DIR = "pokemon_sprites"
os.makedirs(IMAGE_DIR, exist_ok=True)

# Function to fetch Pokémon data
def get_pokemon_data(pokemon_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        types = [t["type"]["name"] for t in data["types"]]
        sprite_url = data["sprites"]["front_default"]
        return types, sprite_url
    else:
        print(f"Error fetching data for ID {pokemon_id}")
        return None, None

# Dictionary to store type mappings
pokemon_types = {}

# Fetch first 50 Pokémon
for pokemon_id in range(1, 1026):
    types, sprite_url = get_pokemon_data(pokemon_id)
    
    if types and sprite_url:
        # Save type mapping
        pokemon_types[str(pokemon_id).zfill(3)] = types
        
        # Download and save sprite
        sprite_response = requests.get(sprite_url)
        if sprite_response.status_code == 200:
            img_path = os.path.join(IMAGE_DIR, f"{str(pokemon_id).zfill(3)}.png")
            with open(img_path, "wb") as f:
                f.write(sprite_response.content)
        
        print(f"Saved {pokemon_id}.png with types {types}")

# Save type mappings to JSON
with open("pokemon_types.json", "w") as f:
    json.dump(pokemon_types, f, indent=4)

print("Done! Images saved in 'pokemon_sprites', type mappings in 'pokemon_types.json'.")
