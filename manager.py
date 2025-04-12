import os
import subprocess
import json
import getpass # gets passwords hidden

# Could even have a file that is like a vimrc where they choose options, such as if password is optional

def get_entry():
    site = input("\nEnter the site name: ")
    password = getpass.getpass("Password (input hidden): ")

def create_new_file(filename="passwords.json"):
    entries = {}

    while True:
        site, entry = get_entry()
    with open(filename, "w") as f:
        json.dump(entries)

def print_help():
    print("Required package") # TODO: dependency list (secure-remove, gpg)
    print("Current settings: ") # print settings

def menu():
    print("\n----- Password Manager Menu -----")
    print("0. Help, Settings, and Dependencies")
    print("1. Create a new file")
    print("2. Add an entry to an existing file")

    user_option = int(input("Enter an option: "))
    match user_option:
        case 0:
            print_help()
        case 1:
            create_new()
        case 2:
            pass
        case _:
            print("Invalid option")
            menu()

if __name__ == "__main__":
    print("/ / / / / / / / / / / / / / / / / / /")
    print("    GPG      PASSWORD      MANAGER   ")
    print("/ / / / / / / / / / / / / / / / / / /")
    menu()