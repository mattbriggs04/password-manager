
# Print string in header
def print_header(header: str) -> None:
    size = 30
    print('')
    print(f'{'-'*size}\n{header:^{size}}\n{'-'*size}')


# For printing passwords as hidden
def print_hidden(s: str, end='\n'):
    print(len(s) * '*', end=end)
        
