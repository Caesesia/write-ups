import socket
import base64
import string
import time

HOST = "game1.marshack.fr"
PORT = 42005

def send_payload(payload):
    """Envoie une chaîne au serveur et récupère la réponse chiffrée."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(payload.encode() + b"\n")
        response = s.recv(4096).strip()  # Augmenter la taille du buffer
        return base64.b64decode(response)

def find_block_size():
    """Détermine la taille des blocs de chiffrement."""
    base_len = len(send_payload(""))
    for i in range(1, 40):
        new_len = len(send_payload("A" * i))
        if new_len > base_len:
            return new_len - base_len
    return None

def ecb_attack():
    """Extrait le flag caractère par caractère."""
    block_size = find_block_size()
    assert block_size is not None, "Impossible de détecter la taille des blocs."
    
    known_flag = "fl@g{This_1s_"
    
    for i in range(150):  # On suppose un flag de moins de 100 caractères
        pad_length = (block_size - (len(known_flag) + 1) % block_size) % block_size
        ref_block = send_payload("A" * pad_length)[:block_size * (len(known_flag) // block_size + 1)]

        for c in string.printable:
            test_block = send_payload("A" * pad_length + known_flag + c)[:block_size * ((len(known_flag) + 1) // block_size + 1)]
            
            print(f"Test: {c} -> {test_block}")  # Debug: voir les tests
            
            if test_block == ref_block:
                known_flag += c
                print(f"Flag en cours : {known_flag}")
                break
            
            time.sleep(0.05)  # Éviter le blocage du serveur

        if known_flag.endswith("}"):  # On suppose que le flag est entre {}
            break

    print(f"Flag trouvé : {known_flag}")

ecb_attack()
