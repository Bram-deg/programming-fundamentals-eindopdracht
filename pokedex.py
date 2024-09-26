import random
from time import sleep

import requests

from utils import print_divider


def convert_id_to_name(pokemon_id):
    """this function is used to convert the ID to a name when the user inputs an ID"""
    # Retrieve the Pokémon with the given ID
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Return the Pokémon name
        return data['name']
    else:
        # Return an error message if the request failed
        print(f'Request failed with status code {response.status_code}')

def get_pokedex_description(pokemon):
    """This function retrieves the Pokédex description for a given Pokémon."""
    # URL to retrieve the Pokémon with the given name
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
                return entry['flavor_text']
    else:
        # Return an error message if the request failed
        return f'Request failed with status code {response.status_code}'

def pokedex():
    """This function runs the Pokédex program. in a loop,
    the user can input a Pokémon name or ID to retrieve their Pokédex description."""
    print("Welcome to the Pokédex!")
    print("This program allows you to search for Pokémon and view their Pokédex descriptions.")
    print("You can also type 'random' to return the Pokédex description of a random pokemon.")
    print("Type 'stop' to return to the main menu.")
    print_divider()

    # Main loop to search for the Pokémon
    while True:
        try:
            user_input = str(input("Enter the name or id of the pokemon you are looking for: ").lower())
            # Check if the user input is a number (ID) or a string (name)
            if user_input.isdigit():
                pokemon_name = convert_id_to_name(user_input)
            else:
                pokemon_name = user_input

            # Check if the user wants a random Pokémon
            if user_input == "random":
                user_input = random.randint(1, 1025)
                pokemon_name = convert_id_to_name(user_input)

            description = get_pokedex_description(pokemon_name)
            print_divider()
            print(description)
            print_divider()
            print("Reminder: Type 'stop' to return to the main menu.")

            # Check if the user wants to stop the program
            if user_input == "stop":
                print("Thank you for using the Pokédex!")
                print("Returning to the main menu...")
                sleep(1)
                break

        # Handle exceptions
        except requests.exceptions.RequestException:
            print("Could not connect to PokéAPI. Returning to the main menu.")
            sleep(1)
            return
        except Exception:
            print(f"Error occurred: your input may be invalid.")
            sleep(1)

