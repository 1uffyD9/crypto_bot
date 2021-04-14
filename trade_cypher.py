import json
import base64
from getpass import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class TradeCypher:
    def get_key(self):
        # link : https://nitratine.net/blog/post/encryption-and-decryption-in-python/
        password_provided = getpass("[!] Please provide the password : ")
        password = password_provided.encode()  # Convert to type bytes
        salt = b'R\x87\xbfY\xba;\x0c\xe6\xd7\xa5\x9a\x16\x040\xd3F'  # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password))  # Can only use kdf once

    def encryption(self, key):
        any_string = input("[!] Add any string to encrypt: ")
        key_pairs = {
            'api_key': input("[!] Please Enter api key : "),
            'secret_key': input("[!] Please Enter secret_key : ")
        }

        f = Fernet(key)
        if not len(any_string) == 0:
            # Encrypt the bytes. The returning object is of type bytes
            print("[*] Encrypted random string : {}".format(f.encrypt(any_string.encode())))

        encrypted = f.encrypt(json.dumps(key_pairs).encode('utf-8'))
        print("[*] Encrypted key pair object : ".format(encrypted))

    def decryption(self, key, cypher_text):
        f = Fernet(key)
        plain_text = f.decrypt(cypher_text)  # Decrypt the bytes. The returning object is of type bytes
        return plain_text.decode("utf-8")


if __name__ == "__main__":
    try:
        tc = TradeCypher()
        tc.encryption(tc.get_key())
    except KeyboardInterrupt:
        print("[!] Safely exiting the program")
