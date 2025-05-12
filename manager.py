import json
import getpass # gets passwords hidden
import os
import re
import tempfile
from gpg import *
from format import *

VERSION = "1.1"
# Used for exiting back to menu and "clearing" the terminal
LINE_BUFFER = "\n" * 45

# generated from https://www.topster.net/text-to-ascii/slant.html
load_str = r"""
   __                               __                 
  / /_  ___    _____   ____ ___    / /__  ___    __  __
 / __/ / _ \  / ___/  / __ `__ \  / //_/ / _ \  / / / /
/ /_  /  __/ / /     / / / / / / / ,<   /  __/ / /_/ / 
\__/  \___/ /_/     /_/ /_/ /_/ /_/|_|  \___/  \__, /  
                                              /____/ 
"""

settings = {} # global variable to store all of the settings, populated by load_settings()
pwd_input = getpass.getpass # global variable storing the input function used for passwords (either a hidden function or not-hidden)
def load_settings(filepath="settings.json"):
    global settings
    with open(filepath, "r") as f:
        settings = json.load(f)
    
    global pwd_input
    pwd_input = getpass.getpass if settings["hiddenPassword"] else input

def get_entry() -> tuple[str, dict[str, str]]:
    info = {}
    site = input("Site name: ")
    siteurl = input("Site url (press enter to leave blank): ")
    username = input("Username: ")

    while True:
        password = pwd_input("Password: ")
        if not settings["hiddenPassword"]:
            break
        confirm_password = pwd_input("Confirm Password: ")
        if password == confirm_password:
            break

        print("Passwords differ. Try again.")

    notes = input("Notes: ") # maybe add multi-line notes allowed

    info = {
        "siteurl": siteurl,
        "username": username,
        "password": password,
        "notes": notes,
    }
    return site, info

def add_entries(json_dict: dict[str, str], sites: set) -> None:
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

def get_filepath(prompt: str) -> str:
    while True:
        filepath = input(prompt)
        if os.path.exists(filepath) or not filepath:
            break
        print("File not found, retry")
    return filepath

def get_passphrase(confirm=False) -> tuple[str, str]:
    while True:
        passphrase = pwd_input("Enter passphrase: ")
        if not confirm:
            break

        confirm_passphrase = pwd_input("Re-enter passphrase to confirm: ")
        if passphrase == confirm_passphrase:
            break
        print("Passphrases differ, retry")

    return passphrase

def opt_help():
    print_header("Help & Tips")
    print("FAQ:")
    print("\tQ: Why is my password not typing?")
    print("\tA: Your password is typing! It is just hidden so no one else can see it. This can be turned off in settings.\n")

    print("Tips:")
    print("\t1. In the menu, prefixing a command with \'/\' allows you to run terminal commands. \"/ls\" will list out the current directory.")
    
    print_header("Required Packages")
    print("\tsecure-remove")
    print("\tgpg")

    print_header("Current Settings")
    for k,v in settings.items():
        print(f"\t{k}: {v}")

    while True:
        input("\nPress enter to exit. ")
        break

def opt_create_new():
    print_header("Create New File")
    filename = input("Enter a file name (press enter to name file \"passwords.json\"): ")
    if filename == "":
        filename = "passwords.json"

    json_dict = {}
    entry_cont_rsp = input("Would you like to add one or more entries [y/n]? ")
    if entry_cont_rsp.lower() == 'y':
        sites = set()
        add_entries(json_dict, sites)

    with open(filename, "w") as json_file:
        print("Creating file", filename)
        json.dump(obj=json_dict, fp=json_file, indent=4)
    
    if input("Would you like to securely encrypt this file (you can anytime through the menu) [y/n]? ").lower() == 'y':
        opt_encrypt()

def opt_append():
    print_header("Append to File")
    filepath = get_filepath("Enter file to append entries to: ")
    is_encrypted = False
    if re.match(r".*\.gpg$", filepath):
        print(f"{filepath} detected as encrypted.")
        is_encrypted = True
    elif input(f"Is {filepath} encrypted [y/n]? ").lower() == 'y':
        is_encrypted = True

    if is_encrypted:
        while True:
            passphrase = get_passphrase()
            json_dict, is_success = gpg_decrypt_file(filepath, passphrase, settings["encryptionAlgo"])
            if is_success:
                break

            print("Incorrect password, try again...\n")
    else:
        json_dict = get_json_dict(filepath)

    print("Add Entries")
    sites = set(json_dict.keys())
    add_entries(json_dict, sites)


    if not is_encrypted:
        with open(filepath, "w") as json_file:
            print("Appending entries to", filepath)
            json.dump(obj=json_dict, fp=json_file, indent=4)
    else:
        try:
            tmp_file = tempfile.NamedTemporaryFile(mode="w", delete=False)
            tmp_path = tmp_file.name

            json.dump(obj=json_dict, fp=tmp_file, indent=4)
            tmp_file.close()

            gpg_encrypt_file(tmp_path, passphrase, cipher_algo=settings["encryptionAlgo"])
            os.replace(f"{tmp_path}.gpg", filepath)
        finally:
            # ensure the tmp_path is always securely removed from disk
            secure_remove(tmp_path)

    input("Success! Press enter to return to menu.")

def opt_encrypt():
    print_header("Encrypt File")
    filepath = get_filepath("Enter file you want to encrypt: ")
    if not filepath:
        print("Filepath empty, exiting.")
        return
    
    passphrase = get_passphrase(confirm=True)
    gpg_encrypt_file(filepath, passphrase, settings["encryptionAlgo"])
    print(f"Encrypted {filepath} as {filepath}.gpg")

    if settings["autoSecureRemove"]:
        secure_remove(filepath)
    else:
        if input(f"Would you like to securely remove {filepath} [y/n]? ").lower() == "y":
            secure_remove(filepath)
    input("Success! Press enter to return to menu.")

def opt_decrypt():
    print_header("Decrypt File")
    filepath = get_filepath("Enter file you want to decrypt: ")
    while True:
        passphrase = get_passphrase()
        json_dict, is_success = gpg_decrypt_file(filepath, passphrase, settings["encryptionAlgo"])
        if is_success:
            break

        print("Incorrect password, try again...\n")

    print("\nFile unlocked. Select an option: ")

    print("0. Print out all stored information")
    print("1. Print out all site names")
    print("2. Get a site's credentials")

    user_option = get_user_option("Enter an option (-1 to exit): ")

    match user_option:
        case -1:
            return
        case 0:
            is_hidden = get_user_option("Would you like the passwords to be hidden [y/n]? ", inp_type=str, commands_allowed=False).lower() == 'y'
            print_password_dict(json_dict, pwds_hidden=is_hidden)
        case 1:
            print("\nSites found:")
            num = 1
            for site in json_dict:
                print(f"{num}. {site}")
                num += 1

        case 2:
            site = input("Enter a site to get the information of: ")
            print_password_dict(json_dict, pwds_hidden=False, sites=[site])

        case _:
            print("Invalid option")
    
    input ("Press enter to exit. ")

def menu() -> bool:
    print_header("TermKey Menu")
    print("0. Help, Settings, and Dependencies")
    print("1. Create a new file")
    print("2. Add entries to an existing file")
    print("3. Securely store a plaintext file")
    print("4. Access passwords from an encrypted file")

    user_option = get_user_option("Enter an option (-1 to exit): ")
    
    match user_option:
        case -1:
            print("\nQuitting TermKey...")
            return False
        case 0:
            opt_help()
        case 1:
            opt_create_new()
        case 2:
            opt_append()
        case 3:
            opt_encrypt()
        case 4:
            opt_decrypt()
        case _:
            print("Invalid option.")
        
    return True

if __name__ == "__main__":
    print(load_str)
    print(f"VERSION {VERSION}")
    load_settings()
    while menu():
        print(LINE_BUFFER)