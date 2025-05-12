# TermKey Password Manager
This utility expands upon GPG in order to create a simple password manager to run within your CLI, and is more intuitive to follow than memorizing gpg commands. This goal of this password manager was to create a secure password manager that allows the user to easily create and append to a password file that is encrypted and ensure all plaintext data is securely removed off of disk.

## Install
Clone this repository, and run `python3 manager.py` in your terminal to run the password manager. Eventually, a binary may be added to be placed in your PATH environment variable so one can simply type "termkey" to run the tool.

## Dependencies
As of right now, there is no script to enforce dependencies. You will need:
1. GNU Privacy Guard (gpg). Typically installed on most Linux distros. MacOS and Windows users may need to install.
2. srm (secure remove). Used in order to securely remove plaintext files so no important data is left on disk.

## License
This project is under the MIT License. See `LICENSE`.

## settings.json
`settings.json` is a file to allow for you to easily change your preferred settings for using the password manager easily. This includes quality of life settings such as "hiddenPassword", which when true will hide your password while typing it (preferred), or utility settings like "encryptionAlgo", which by default is set to AES: a strong modern encryption standard.
