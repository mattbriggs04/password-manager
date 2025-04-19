import subprocess
import json
import getpass # gets passwords hidden

# Could even have a file that is like a vimrc where they choose options, such as if password is optional
settings = {}

def load_settings(filepath="settings.json"):
    global settings
    with open(filepath, "r") as f:
        settings = json.load(f)

def get_entry() -> tuple[str, dict[str, str]]:
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

def secure_remove(filename: str) -> bool:
    try:
        subprocess.run(["srm", filename])
        return True
    except:
        print("Failed to secure remove", filename)
        return False
    
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
    print("Current settings:", settings) # print settings

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
    print("""
_____________________________________
  ____ ____ ____    ____ __  __ ___
 / ___|  __\   _ \   |  _ \  \/  |
| |  _| |__ | |_) |  | |_) | |\/| |
| |_| |  __/   __/   |  __/| |  | |
 \____|_|  | _|      |_|   |_|  |_|
_/____/_/__/_/_______/_/___/_/__/_/___         
          PASSWORD MANAGER
""")
    load_settings()
    menu()