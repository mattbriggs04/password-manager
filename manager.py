import subprocess
import json
import getpass # gets passwords hidden
import time
import os
from gpg import *
from format import *
LINE_BUFFER = "\n" * 30

# generated from https://www.topster.net/text-to-ascii/slant.html
load_str = r"""
   __                               __                 
  / /_  ___    _____   ____ ___    / /__  ___    __  __
 / __/ / _ \  / ___/  / __ `__ \  / //_/ / _ \  / / / /
/ /_  /  __/ / /     / / / / / / / ,<   /  __/ / /_/ / 
\__/  \___/ /_/     /_/ /_/ /_/ /_/|_|  \___/  \__, /  
                                              /____/ 
"""
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
        filename = input("Enter the file you want to manage: ")
        if os.path.exists(filename):
            break
        print("File not found, retry")

    while True:
        passphrase = getpass.getpass("\nEnter passphrase: ")
        confirm_passphrase = getpass.getpass("Re-enter passphrase to confirm: ")
        if passphrase == confirm_passphrase:
            break
        print("Passphrases differ, retry")

    return filename, passphrase

def prompt_srm(filepath: str) -> None:
    is_srm = input("Would you like to securely remove the unencrypted file [y/n]? ")
    if is_srm.lower() == 'y':
        secure_remove(filepath)

def opt_help():
    print_header("Help & Tips")
    print("Tip 1. In the menu, prefixing a command with \'/\' allows you to run terminal commands. \"/ls\" will list out the current directory.")
    
    print_header("Required Packages")
    print("\tsecure-remove\n\tgpg") # TODO: dependency list (secure-remove, gpg

    print_header("Current Settings")
    for k,v in settings.items():
        print(f"\t{k}: {v}")

    while True:
        input("\nType anything to exit. ")
        break

# Make these wrappers, try to remove all prompt-logic from other functions that serve another purpose
def opt_encrypt():
    filepath, passphrase = get_passphrase()
    gpg_encrypt_file(filepath, passphrase, settings["encryptionAlgo"])
    print(f"Encrypted {filepath} into {filepath}.gpg")

    if settings["autoSecureRemove"]:
        res = input("Would you like to remove ")

def opt_append():
    pass

def opt_decrypt():
    filepath, passphrase = get_passphrase()
    json_dict = gpg_decrypt_file(filepath, passphrase, settings["encryptionAlgo"])
    print("output = ", json_dict)

def menu() -> bool:
    print_header("TermKey Menu")
    print("0. Help, Settings, and Dependencies")
    print("1. Create a new file")
    print("2. Add entries to an existing file")
    print("3. Securely store a plaintext file")
    print("4. Access passwords from an encrypted file")

    while True:
        user_option = input("Enter an option (-1 to exit): ")
        if (user_option and user_option[0] == '/'):
            cmd = user_option[1:]
            print(f"\n$ {cmd}")
            subprocess.run(cmd, shell=True, check=True)
        else:
            try:
                user_option = int(user_option)
                break
            except ValueError:
                print("Invalid option. Not an integer.")
    
    match user_option:
        case -1:
            print("\nQuitting TermKey...")
            return False
        case 0:
            opt_help()
        case 1:
            create_new_file()
        case 2:
            print_header("Append To File")
            append_to_file()
        case 3:
            print_header("Encrypt File")
            opt_encrypt()
        case 4:
            print_header("Decrypt File")
            opt_decrypt()
        case _:
            print("Invalid option.")
        
    return True

if __name__ == "__main__":
    print(load_str)
    load_settings()
    while menu():
        print(LINE_BUFFER)