import random
from time import sleep

import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

def get_random_pokemon_sprite():
    """Fetches a random Pokémon sprite URL and name."""
    # Get the total number of Pokémon
    all_pokemon_response = requests.get('https://pokeapi.co/api/v2/pokemon-species/')
    if all_pokemon_response.status_code == 200:
        data = all_pokemon_response.json()
        total_pokemon = data['count']

        # Generate a random Pokémon ID between 1 and the total number of Pokémon
        random_id = random.randint(1, total_pokemon)

        # Fetch the sprite URL and name for the random Pokémon
        url = f'https://pokeapi.co/api/v2/pokemon/{random_id}'
        sprite_response = requests.get(url)
        if sprite_response.status_code == 200:
            data = sprite_response.json()
            sprite_url = data['sprites']['front_default']
            name = data['name']
            return sprite_url, name
    # Return None if the request failed
    return None, None

def who_is_that_pokemon():
    """The main function for the 'Who's that Pokémon?' game."""
    # Display the game instructions
    print("Welcome to who's that Pokémon!")
    print("Try to guess the Pokémon by its sprite.")
    print("If you enter the wrong name the game will end!.")
    print("*" * 50)
    # Initialize the score
    score = 0

    # Display the image and prompt the user for a guess
    while True:
        sprite_url, pokemon_name = get_random_pokemon_sprite()
        if sprite_url:
            response = requests.get(sprite_url)
            img = Image.open(BytesIO(response.content))
            plt.imshow(img)
            plt.axis('off')
            plt.show()
            pokemon_guess = input("Who's that Pokémon? ")

            # Check if the guess is correct
            if pokemon_guess.lower() == pokemon_name:
                print("Correct!")
                score += 1
                print(f"current score: {score}.")
                print("*" * 50)
            # End the game if the guess is incorrect
            else:
                print(f"Wrong! It's {pokemon_name.capitalize()}.")
                break
        else:
            print("Failed to retrieve a random Pokémon sprite.")

    # Display the final score
    print (f"Your final score is {score}.")
    # ask if the user wants to play again
    play_again = input("Do you want to play again?\n1. Yes\n2. No\n")
    if play_again == "1" or play_again.lower() == "yes":
        who_is_that_pokemon()
    elif play_again == "2" or play_again.lower() == "no":
        print("Thank you for playing Who's that Pokémon!\nReturning to the main menu.")
        sleep(1)
    else:
        print("Invalid choice.\nReturning to the main menu.")
        sleep(1)