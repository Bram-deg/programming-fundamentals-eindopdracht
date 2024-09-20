from time import sleep

import requests
import random

def get_all_types():
    """This function retrieves all Pokémon types from the PokéAPI."""
    try:
        url = 'https://pokeapi.co/api/v2/type/'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            # exclude the unknown and stellar types these are obscure types that are no longer in the games
            types = [t['name'] for t in data['results'] if t['name'] not in ['unknown', 'stellar']]
            return types

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []




def get_random_type(types):
    """This function returns a random type from the list of all Pokémon types."""
    return random.choice(types)


def get_type_effectiveness(defending_type):
    """This function retrieves the type effectiveness data for a given Pokémon type."""
    try:
        url = f'https://pokeapi.co/api/v2/type/{defending_type}/'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            damage_relations = data['damage_relations']

            # Lijsten van types waarop dit type effectief is of niet
            double_damage_from = [d['name'] for d in damage_relations['double_damage_from']]
            half_damage_from = [d['name'] for d in damage_relations['half_damage_from']]
            no_damage_from = [d['name'] for d in damage_relations['no_damage_from']]

            return {
                'double_damage_from': double_damage_from,
                'half_damage_from': half_damage_from,
                'no_damage_from': no_damage_from
            }

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def type_trainer():
    """This function runs the Type Trainer game.
    The user has to guess which type is super effective against a random type."""
    print("Welcome to the Pokémon type trainer!")
    print("Try to guess which type is super effective against the given Pokémon type.")
    print("Hint : Type 'help' for a list of all Pokémon types.")

    # Retrieve all Pokémon types from the API
    types = get_all_types()
    if not types:
        print("There was an error fetching the types.")
        print("Returning to the main menu...")
        sleep(1)
        return

    while True:
        # Retrieve a random type
        defending_type = get_random_type(types)
        # Print the defending type
        print("*" * 50)
        print(f"The defending type is: {defending_type.capitalize()}")

        # Ask the user for an attacking type
        user_type = input("What type will you use to attack? (type 'stop' to stop the game): ").lower()

        # Check if the user wants to stop
        if user_type == 'stop':
            print("Thanks for playing!")
            print("Returning to the main menu...")
            sleep(1)
            break

        # Check if the user wants to see the list of types
        if user_type == 'help':
            print("available types:")
            print(", ".join(types))
            continue

        # Retrieve the type effectiveness data from the API
        effectiveness_data = get_type_effectiveness(defending_type)
        if effectiveness_data is None:
            print(f"Something went wrong while fetching the type effectiveness data.")
            continue

        # Check the effectiveness of the chosen type
        if user_type in effectiveness_data['double_damage_from']:
            print(f"Good job! {user_type.capitalize()} is super effective against {defending_type.capitalize()}.")
            sleep(1)
        elif user_type in effectiveness_data['half_damage_from']:
            print(f"Wrong! {user_type.capitalize()} is not very effective against {defending_type.capitalize()}.")
            sleep(1)
        elif user_type in effectiveness_data['no_damage_from']:
            print(f"Wrong! {user_type.capitalize()} does not affect {defending_type.capitalize()}.")
            sleep(1)
        elif user_type not in types:
            print(f"{user_type.capitalize()} is not a valid Pokémon type.")
            sleep(1)
        else:
            print(f"Not bad!, {user_type.capitalize()} does neutral damage against {defending_type.capitalize()}.")
            sleep(1)