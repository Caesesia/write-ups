from pwn import *
import json
from rich.console import Console
import string

printable = [ord(c) for c in string.printable]

console = Console()
context.log_level = 'error'

def encrypt(payload):
    p = remote("game1.marshack.fr", 42005)
    p.recvuntil(b": ")

    p.sendline(payload.hex().encode())

    data = json.loads(p.recvline())['ciphertext']

    p.close()
    return data


flag = b""
with console.status(f"FLAG = {flag}, Trying byte : ") as a:
    while len(flag) == 0 or flag[-1] != 125:  # 125 is the ASCII for '}'
        for c in printable:
            # set char to test
            c = c.to_bytes(1, 'big')
            # update the console status
            a.update(f"FLAG = {flag}, Trying byte : {c}")

            # Adjusting the payload padding calculation:
            # Block size is assumed to be 16 bytes
            padding_length = 16 - ((len(flag) + 1) % 16)  # Calculate how many padding bytes we need
            
            # Prepare the payload, padding and the guessed byte
            if len(flag) > 0:
                payload = b'\x10' * padding_length + flag + c
            else:
                payload = c + b'\x10' * (16 - 1)

            cipher = encrypt(payload)
            
            # Check if the first block and the targeted block are the same
            # Since the target block will be adjusted to match the oracle's padding, it should reflect the changes.
            if cipher[0:32] == cipher[32 + (32 * (len(flag) // 16)): 64 + (32 * (len(flag) // 16))]:
                # If it is, then the letter is found
                flag += c
                print(f"Flag so far: {flag.decode()}")  # Print the flag as it is built
                break

print("Final FLAG = ", flag.decode())
