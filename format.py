import subprocess

# string to hidden
def strtoh(s: str) -> str:
    return len(s) * '*'

# gets a user option and ensures the option is a valid type, and handles the ability to type commands in the manager
def get_user_option(prompt: str, inp_type=int, commands_allowed=True):
    while True:
        user_option = input(prompt)
        if (user_option and user_option[0] == '/' and commands_allowed):
            cmd = user_option[1:]
            print(f"\n$ {cmd}")
            subprocess.run(cmd, shell=True, check=True)
        else:
            try:
                user_option = inp_type(user_option)
                break
            except ValueError:
                print("Invalid option. Not of type", inp_type)
    return user_option

# searches for a site and prints out all of the info
def print_entry(entry: dict, pwds_hidden=True) -> None:
    for k, v in entry.items():
        if k == "password" and pwds_hidden:
            v = strtoh(v)
        print(f"\t{k}: {v}")

# Print string in header
def print_header(header: str) -> None:
    size = 45
    print('')
    print(f'{'-'*size}\n{header:^{size}}\n{'-'*size}')


# For printing passwords as hidden
def print_hidden(s: str, end='\n'):
    print(strtoh(s), end=end)
    
# Prints out all sites or just the specified sites of the sites list
def print_password_dict(d: dict, pwds_hidden=True, sites=set()):
    print_all_sites = len(sites) == 0

    for site, site_entry in d.items():
        if not print_all_sites and site not in sites:
            continue

        print("=" * 30)
        print(f"{site}:")
        print_entry(site_entry, pwds_hidden=pwds_hidden)
        print("=" * 30)
