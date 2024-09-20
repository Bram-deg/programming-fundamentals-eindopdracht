from time import sleep

from pokedex import pokedex
from type_trainer import type_trainer
from who_is_that_pokemon import who_is_that_pokemon
from utils import print_main_menu


def main():
    print("Welcome to the Pokémon App!")
    while True:
        print_main_menu()
        choice = input("What do you want to do? ")
        if choice == "1":
            pokedex()
        elif choice == "2":
            who_is_that_pokemon()
        elif choice == "3":
            type_trainer()
        elif choice == "4":
            print("Thanks for playing!\nSee Ya!")
            break
        else:
            print("Invalid choice. Please try again.")
            sleep(1)


if __name__ == '__main__':
    main()