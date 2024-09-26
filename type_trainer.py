from time import sleep

import requests
import random

from utils import print_divider


def get_all_types():
    """This function retrieves all Pokémon types from the PokéAPI."""
    try:
        url = 'https://pokeapi.co/api/v2/type/'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            # exclude the unknown and stellar types, these are obscure types that are no longer in the games
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

            # Extract the types that are super effective, not very effective, and have no effect
            double_damage_from = [d['name'] for d in damage_relations['double_damage_from']]
            half_damage_from = [d['name'] for d in damage_relations['half_damage_from']]
            no_damage_from = [d['name'] for d in damage_relations['no_damage_from']]

            # Return the lists of type-effectiveness relationships
            return {
                'double_damage_from': double_damage_from,
                'half_damage_from': half_damage_from,
                'no_damage_from': no_damage_from
            }

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def show_feedback(defending_type, effectiveness_data):
    """shows the user which types would have been more effective against the defender"""
    print(f"Types that are super effective against {defending_type.capitalize()} are: {', '.join(effectiveness_data['double_damage_from'])}.")


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
        # Retrieve a random type, this will be the defending type
        defending_type = get_random_type(types)
        # Print the defending type
        print_divider()
        print(f"The defending type is: {defending_type.capitalize()}")

        # Ask the user for an attacking type
        user_input = input("What type will you use to attack? (type 'stop' to stop the game): ").lower()

        # Check if the user wants to see the list of types
        if user_input == 'help':
            print("available types:")
            print(", ".join(types))
            # After showing the list of types, ask for the user's input again.
            user_input = input("What type will you use to attack? (type 'stop' to stop the game): ").lower()

        # Check if the user wants to stop
        if user_input == 'stop':
            print("Thanks for playing!")
            print("Returning to the main menu...")
            sleep(1)
            break

        # Retrieve the type effectiveness data from the API
        effectiveness_data = get_type_effectiveness(defending_type)
        if effectiveness_data is None:
            print(f"Something went wrong while fetching the type effectiveness data.")
            continue

        # Check the effectiveness of the chosen type and provide feedback
        if user_input in effectiveness_data['double_damage_from']:
            print(f"Good job! {user_input.capitalize()} is super effective against {defending_type.capitalize()}.")
            sleep(1)
        elif user_input in effectiveness_data['half_damage_from']:
            print(f"Wrong! {user_input.capitalize()} is not very effective against {defending_type.capitalize()}.")
            show_feedback(defending_type, effectiveness_data)
            sleep(1)
        elif user_input in effectiveness_data['no_damage_from']:
            print(f"Wrong! {user_input.capitalize()} does not affect {defending_type.capitalize()}.")
            show_feedback(defending_type, effectiveness_data)
            sleep(1)
        elif user_input not in types:
            print(f"{user_input.capitalize()} is not a valid Pokémon type.")
            sleep(1)
        else:
            print(f"Not bad!, {user_input.capitalize()} does neutral damage against {defending_type.capitalize()}.")
            show_feedback(defending_type, effectiveness_data)
            sleep(1)