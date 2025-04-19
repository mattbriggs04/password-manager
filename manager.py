import subprocess
import json
import getpass # gets passwords hidden
import time
import os
# Could even have a file that is like a vimrc where they choose options, such as if password is optional
settings = {}

def load_settings(filepath="settings.json"):
    global settings
    with open(filepath, "r") as f:
        settings = json.load(f)

def secure_remove(filename: str) -> bool:
    try:
        subprocess.run(["srm", filename])
        return True
    except:
        print("Failed to secure remove", filename)
        return False
    

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

def get_entries(json_dict: dict[str, str], sites: set) -> None:
    entry_cont_rsp = 'y'
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

def create_new_file() -> None:
    filename = input("Enter a file name (press enter to name file \"passwords.json\"): ")
    if filename == "":
        filename = "passwords.json"

    json_dict = {}
    entry_cont_rsp = input("Would you like to add one or more entries [y/n]? ")
    if entry_cont_rsp.lower() == 'y':
        sites = set()
        get_entries(json_dict, sites)

    with open(filename, "w") as json_file:
        print("Populating file", filename)
        json.dump(obj=json_dict, fp=json_file, indent=4)

def get_json_dict(json_file: str):
    if os.path.exists(json_file):
        with open(json_file, "r") as jf:
            try:
                json_dict = json.load(jf)
            except:
                json_dict = {}
    else:
        json_dict = {}
    
    return json_dict

def append_to_file() -> None:
    filename = input("Enter a file to add an entry to (press enter to name file \"passwords.json\"): ")
    if filename == "":
        filename = "passwords.json"

    json_dict = get_json_dict(filename)
    sites = set()
    for k in json_dict.keys():
        sites.add(k)
    
    get_entries(json_dict, sites)

    with open(filename, "w") as json_file:
        print("Populating file", filename)
        json.dump(obj=json_dict, fp=json_file, indent=4)

def get_passphrase() -> tuple[str, str]:
    while True:
        passphrase = getpass.getpass("\nEnter a passphrase: ")
        confirm_passphrase = getpass.getpass("Re-enter passphrase to confirm: ")
        if passphrase == confirm_passphrase:
            break
        print("Passphrases differ, retry")

    while True:
        filename = input("Enter a file to secure (press enter to select \"passwords.json\"): ")
        if filename == "":
            filename = "passwords.json"
        
        if os.path.exists(filename):
            break
        print("File not found, retry")

    return filename, passphrase

def gpg_encrypt_file(filepath, passphrase):

    print("Reminder: ensure you have stored the passphrase somewhere safe (e.g. a card that you keep on yourself at all times)")
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
    subprocess.run(command, check=True)

    is_srm = input("File successfully encrypted, would you like to securely remove the unencrypted file [y/n]?")
    if is_srm.lower() == 'y':
        secure_remove(filepath)

def gpg_decrypt_file(filepath, passphrase):
    pass

def gpg_site_info(filepath, passphrase, site):
    pass # searches the file for the site, if so, returns username and password to user

def print_help():
    print("\n----- Help -----")
    print("Required package") # TODO: dependency list (secure-remove, gpg)
    print("Current settings:", settings) # print settings

def menu() -> bool:
    print("\n------- Password Manager Menu -------")
    print("0. Help, Settings, and Dependencies")
    print("1. Create a new file")
    print("2. Add entries to an existing file")
    print("3. Securely store a plaintext file")
    print("4. Access passwords from encrypted file")

    user_option = int(input("Enter an option (-1 to exit): "))
    match user_option:
        case 0:
            print_help()
        case 1:
            print("\n------- Create New File -------")
            create_new_file()
        case 2:
            print("\n------- Append To File -------")
            append_to_file()
        case 3:
            filepath, passphrase = get_passphrase()
            gpg_encrypt_file(filepath, passphrase)
        case _:
            print("Quitting password manager")
            return False
        
    return True

if __name__ == "__main__":
    print(r"""
_____________________________________
  ____ ____ ____    ___/ /__/ /__/ /___
 / ___|  __\   _ \   |  _  \  \/  |
| |  _| |__ | |_) |  | |_) | |\/| |
| |_| |  __/   __/   |  __/| |  | |
 \____|_|  | _|      |_|   |_|  |_|
_/____/_/__/_/_______/_/___/_/__/_/___         
          PASSWORD MANAGER
""")
    load_settings()
    while menu():
        time.sleep(1.5)