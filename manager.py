import subprocess
import json
import getpass # gets passwords hidden
import time
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
    username = input("Username: ")

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

    json_dict = {}
    entries = {}
    entry_cont_rsp = input("Would you like to add one or more entries [y/n]? ")
    sites = set()
    while entry_cont_rsp.lower() == 'y':
        site, entry = get_entry()
        if site in sites:
            exists_rsp = input("Site already added - would you like to overwrite [y/n]? ")
            if exists_rsp.lower() == 'y':
                json_dict[site] = entry
        else:
            sites.add(site)
            json_dict[site] = entry
        entry_cont_rsp = input("\nWould you like to add another entry [y/n]? ")

    with open(filename, "w") as json_file:
        print("Populating file", filename)
        json.dump(obj=json_dict, fp=json_file, indent=4)

def gpg_encrypt_file(filepath, passphrase):
    command = [
        "gpg",
        "--batch",
        "--yes",
        "--quiet",
        "--pinentry-mode", "loopback",
        "--passphrase", passphrase,
        "--cipher-algo", settings["encryptionAlgo"],
        "-c", filepath

    ]
    subprocess.run(command, ) # TODO: this command

    print("File successfully encrypted, would you like to securely remove the unencrypted file [y/n]?")

def gpg_decrypt_file(filepath, passphrase):
    pass

def gpg_site_info(filepath, passphrase, site):
    pass # searches the file for the site, if so, returns username and password to user

def print_help():
    print("Required package") # TODO: dependency list (secure-remove, gpg)
    print("Current settings:", settings) # print settings

def menu() -> bool:
    print("\n------- Password Manager Menu -------")
    print("0. Help, Settings, and Dependencies")
    print("1. Create a new password file")
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
            print("Quitting password manager")
            return False
        
    return True

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
    while menu():
        time.sleep(2)
        pass