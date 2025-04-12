import subprocess
import json
import getpass # gets passwords hidden

# Could even have a file that is like a vimrc where they choose options, such as if password is optional
settings = {}

def get_settings(filepath="settings.json"):
    with open(filepath, "r") as f:
        settings = json.load(f.read())

def get_entry():
    info = {}
    site = input("\nSite name: ")
    siteurl = input("Site url (press enter to leave blank): ")
    username = input("Username")

    # if settings['password_hidden']
    password = getpass.getpass("Password (input hidden): ")
    notes = input("Additional Notes: ") # maybe add multi-line notes allowed

    info = {
        "siteurl": siteurl,
        "username": username,
        "password": password,
        "notes": notes,
    }
    return site, info

def create_new_file():
    filename = input("Enter a file name (press enter to name file \"passwords.json\"): ")
    if filename == "":
        filename = "passwords.json"

    entries = {}
    entry_cont = input("Would you like to add one or more entries [y/n]? ")
    sites = set()
    while entry_cont == 'y':
        site, entry = get_entry()
        if site in sites:
            print("Site already added - would you like to overwrite?")
            # TODO: if (y) overwrite
        else:
            sites.add(site)
        entry_cont = input("Would you like to add another entry [y/n]? ")

    with open(filename, "w") as f:
        print("Populating file", filename)
        json.dump(entries)

def gpg_encrypt_file(plain_filepath, encrypted_filepath):
    cipher_algo = "AES" # until I add a settings parser
    subprocess.run(["gpg", "--yes", "--cipher-algo", cipher_algo, "-o", ]) # TODO: this command

def print_help():
    print("Required package") # TODO: dependency list (secure-remove, gpg)
    print("Current settings: ") # print settings

def menu():
    print("\n------- Password Manager Menu -------")
    print("0. Help, Settings, and Dependencies")
    print("1. Create a new file")
    print("2. Add an entry to an existing file")

    # print("Change settings")

    user_option = int(input("Enter an option: "))
    match user_option:
        case 0:
            print_help()
        case 1:
            create_new_file()
        case 2:
            pass
        case _:
            print("Invalid option")
            menu()

if __name__ == "__main__":
    # make a cooler load in using ASCII art for the letters
    print("/ / / / / / / / / / / / / / / / / / /")
    print("    GPG      PASSWORD      MANAGER   ")
    print("/ / / / / / / / / / / / / / / / / / /")
    menu()