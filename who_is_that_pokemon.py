import random
from time import sleep

import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

from utils import print_divider


def get_random_pokemon_sprite():
    """Fetches a random Pokémon sprite URL and name."""
    # Generate a random Pokémon ID between 1 and 1025 (the total number of Pokémon)
    random_id = random.randint(1, 1025)

    # Fetch the sprite URL and name for the random Pokémon
    try:
        url = f'https://pokeapi.co/api/v2/pokemon/{random_id}'
        sprite_response = requests.get(url)
        if sprite_response.status_code == 200:
            data = sprite_response.json()
            # A Pokémon has multiple sprites, but we only need the front sprite
            sprite_url = data['sprites']['front_default']
            name = data['name']
            return sprite_url, name
        # Return None if the request failed (for both the sprite and the name)
        else:
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        raise

def save_score(name, score):
    with open("scoreboard.txt", "a") as file:
        file.write(f"{name}: {score}\n")

def display_high_scores():
    # Display the three highest scores from the scoreboard
    print("High scores:")
    print_divider()
    with open("scoreboard.txt", "r") as file:
        scores = file.readlines()
        # Sort the scores in descending order (highest score first)
        scores.sort(key=lambda x: int(x.split(":")[1]), reverse=True)
        for i, score in enumerate(scores[:3]):
            print(f"{i + 1}. {score.strip()}")
    print_divider()
    sleep(1)

def who_is_that_pokemon():
    """The main function for the 'Who's that Pokémon?' game.
    the user has to guess the name of a Pokémon by its sprite."""
    # Display the game instructions
    print("Welcome to who's that Pokémon!")
    print("Try to guess the Pokémon by its sprite.")
    print("If you enter the wrong name the game will end!.")
    print_divider()
    # Initialize the score and ask for the user's name
    score = 0
    name = input("Please enter your name for the scoreboard: ")

    # Display the image and prompt the user for a guess if the request is successful
    while True:
        try:
            sprite_url, pokemon_name = get_random_pokemon_sprite()
        except requests.exceptions.RequestException:
            print("Could not connect to PokéAPI. Returning to the main menu.")
            sleep(1)
            return

        if sprite_url:
            response = requests.get(sprite_url)
            # Display the sprite image using matplotlib and pillow
            img = Image.open(BytesIO(response.content))
            plt.imshow(img)
            # Hide the axis for a cleaner display
            plt.axis('off')
            plt.show()
            user_input = input("Who's that Pokémon? ")

            # Check if the guess is correct
            if user_input.lower() == pokemon_name:
                print("Correct!")
                score += 1
                print(f"current score: {score}.")
                print_divider()
            # End the game if the guess is incorrect
            else:
                print(f"Wrong! It's {pokemon_name.capitalize()}.")
                break
        else:
            print("Failed to retrieve a random Pokémon sprite.")

    # When the game ends display the final score.
    print(f"Your final score is {score}.")
    # Save the name and score to the scoreboard file
    save_score(name, score)
    # Display the 3 highest scores
    display_high_scores()
    # ask if the user wants to play again
    play_again = input("Do you want to play again?\n1. Yes\n2. No\n")
    if play_again == "1" or play_again.lower() == "yes":
        who_is_that_pokemon()
    elif play_again == "2" or play_again.lower() == "no":
        print("Thank you for playing Who's that Pokémon!\nReturning to the main menu...")
        sleep(1)
    else:
        print("Invalid choice.\nReturning to the main menu...")
        sleep(1)