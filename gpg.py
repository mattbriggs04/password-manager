import subprocess
import json

def secure_remove(filename: str) -> bool:
    try:
        subprocess.run(["srm", filename])
        return True
    except:
        print("Failed to secure remove", filename)
        return False
    
def gpg_encrypt_file(filepath: str, passphrase: str, cipher_algo: str) -> None:
    command = [
        "gpg",
        "--batch",
        "--yes",
        "--quiet",
        "--pinentry-mode", "loopback",
        "--passphrase", passphrase,
        "--cipher-algo", cipher_algo,
        "-c", filepath

    ]
    subprocess.run(command, check=True)


def gpg_decrypt_file(filepath: str, passphrase: str, cipher_algo: str) -> dict[str, str]:
    command = [
        "gpg",
        "--batch",
        "--yes",
        "--quiet",
        "--pinentry-mode", "loopback",
        "--passphrase", passphrase,
        "--cipher-algo", cipher_algo,
        "-d", filepath
    ]
    processObj = subprocess.run(command, check=True, capture_output=True)
    json_dict = json.loads(processObj.stdout.decode('utf-8'))
    return json_dict 
    

def gpg_site_info(filepath, passphrase, site):
    pass # searches the file for the site, if so, returns username and password to user