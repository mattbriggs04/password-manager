import subprocess
import json
import getpass # gets passwords hidden
import time
import os
from gpg import *
LINE_BUFFER = "\n\n\n\n"

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

def print_help():
    print("\n----------- Help & Tips -----------")
    print("In the menu, prefixing a command with \'/\' allows you to run terminal commands. \"/ls\" will list out the current directory. This may have been inspired by Minecraft...")
    print("\n----------- Required Packages -----------")
    print("\tsecure-remove\n\tgpg") # TODO: dependency list (secure-remove, gpg)
    print("\n----------- Current settings -----------") # print settings
    for k,v in settings.items():
        print(f"\t{k}: {v}")

    while True:
        input("\nType anything to exit. ")
        break

def menu() -> bool:
    print("\n----------- TermKey Menu -----------")
    print("0. Help, Settings, and Dependencies")
    print("1. Create a new file")
    print("2. Add entries to an existing file")
    print("3. Securely store a plaintext file")
    print("4. Access passwords from an encrypted file")

    user_option = input("Enter an option (-1 to exit): ")
    if (user_option[0] == '/'):
        cmd = user_option[1:]
        print(f"\n> {cmd}")
        subprocess.run(cmd, shell=True, check=True)
        time.sleep(0.5)
        return True
    
    user_option = int(user_option)
    print(LINE_BUFFER)
    match user_option:
        case -1:
            print("\nQuitting TermKey...")
            return False
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
            print("Reminder: ensure you have stored the passphrase somewhere safe (e.g. a card that you keep on yourself at all times)")
            gpg_encrypt_file(filepath, passphrase, settings["encryptionAlgo"])
        case 4:
            filepath, passphrase = get_passphrase()
            json_str = gpg_decrypt_file(filepath, passphrase, settings["encryptionAlgo"])
            print("OUTPUT CAPTURED")
            print(json_str)
        case _:
            print("Invalid option.")
        
    return True

if __name__ == "__main__":
    print(load_str)
    load_settings()
    while menu():
        print(LINE_BUFFER)