# TermKey Password Manager
This utility expands upon GPG in order to create a simple password manager to run within your CLI, and is more intuitive to follow than memorizing gpg commands. This goal of this password manager was to create a secure password manager that allows the user to easily create and append to a password file that is encrypted and ensure all plaintext data is securely removed off of disk.

## Install
Clone this repository, and run `python3 manager.py` in your terminal to run the password manager. Ensure the dependencies are downloaded.

> This may be changed in the future such that users can just type `termkey` in their terminal to run the tool

## Dependencies
As of right now, there is no script to enforce dependencies. You will need:
1. GNU Privacy Guard (gpg). Typically pre-installed on most Linux distros. MacOS and Windows users will need to install gpg if they have not already.
2. srm (secure remove). Used in order to securely remove plaintext files so no important data is left on disk.

## settings.json
`settings.json` is a file to allow for you to easily change your preferred settings for using the password manager easily. This includes quality of life settings such as "hiddenPassword", which when true will hide your password while typing it (preferred), or utility settings like "encryptionAlgo", which by default is set to AES: a strong modern encryption standard.

## License
This project is under the MIT License. See `LICENSE`.
