import random
from time import sleep

import requests

def get_pokemon_name(pokemon_id):
    """this function is used to convert the ID to a name when the user inputs an ID"""
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['name']
    else:
        print(f'Request failed with status code {response.status_code}')

def get_pokedex_description(pokemon):
    """This function retrieves the Pokédex description for a given Pokémon."""
    # URL to retrieve the Pokémon species data
    url = f'https://pokeapi.co/api/v2/pokemon-species/{pokemon}'
    response = requests.get(url)
    # Check if the Pokémon exists
    if response.status_code == 404:
        return f'{pokemon.capitalize()} is not a Pokémon.'
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        # Filter for the English PokéDex description
        descriptions = data['flavor_text_entries']
        for entry in descriptions:
            if entry['language']['name'] == 'en':
                # Return the English PokéDex description and print a header
                print(f"PokéDex description for {pokemon.capitalize()}")
                print("*" * 50)
                return entry['flavor_text']
    else:
        # Return an error message if the request failed
        return f'Request failed with status code {response.status_code}'

def pokedex():
    """This function runs the Pokédex program. in a loop,
    the user can input a Pokémon name or ID to retrieve the Pokédex description."""
    print("Welcome to the Pokédex!")
    print("This program allows you to search for Pokémon and view their Pokédex descriptions.")
    print("You can also type 'random' to return the Pokédex description of a random pokemon.")
    print("Type 'stop' to return to the main menu.")
    print("*" * 50)

    # Main loop to search for the Pokémon
    while True:
        try:
            pokemon_input = str(input("Enter the name or id of the pokemon you are looking for: ").lower())
            # Check if the user wants to stop the program
            if pokemon_input == "stop":
                print("Thank you for using the Pokédex!")
                print("Returning to the main menu...")
                sleep(1)
                break

            # Check if the user input is a number (ID) or a string (name)
            if pokemon_input.isdigit():
                pokemon_name = get_pokemon_name(pokemon_input)
            else:
                pokemon_name = pokemon_input

            # Check if the user wants a random Pokémon
            if pokemon_input == "random":
                random_pokemon = requests.get('https://pokeapi.co/api/v2/pokemon-species/').json()['count']
                pokemon_input = random.randint(1, int(random_pokemon))
                pokemon_name = get_pokemon_name(pokemon_input)

            description = get_pokedex_description(pokemon_name)
            print(description)
            print("*" * 50)
            print("Reminder: Type 'stop' to return to the main menu.")

        # Handle exceptions
        except Exception as e:
            print(f"An error has occurred: Perhaps your input was invalid.")