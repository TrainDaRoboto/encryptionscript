# -*- coding: utf-8 -*-
"""
Created on Sun 1/22/23

@author: npark
"""
import os
import getpass
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# main function
def main():
    # get the file path and password from the user
    file_path = input("Enter the file path: ")
    password = getpass.getpass("Enter the password: ").encode()

    # check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist.")
        return

    # get the user's choice to encrypt or decrypt the file
    choice = input("Do you want to encrypt or decrypt the file? (e/d): ")

    if choice == "e":
        encrypt_file(file_path, password)
    elif choice == "d":
        decrypt_file(file_path, password)
    else:
        print("Invalid choice. Please enter 'e' to encrypt or 'd' to decrypt.")

# function to encrypt the file
def encrypt_file(file_path, password):
    # generate a key using the password
    salt = b'\x1f\xf3\x1a\x8c\x00\x9c\x9e\x1b\x8b\xee\x1f\xf3\x1a\x8c\x00\x9c'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256,
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)

    # read the file and encrypt its contents
    with open(file_path, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)

    # write the encrypted contents to the file
    with open(file_path, "wb") as file:
        file.write(encrypted_data)
        print(f"File {file_path} has been encrypted.")
        
#Function to decrypt file
def decrypt_file(file_path, password):
        # generate a key using the password
        salt = b'\x1f\xf3\x1a\x8c\x00\x9c\x9e\x1b\x8b\xee\x1f\xf3\x1a\x8c\x00\x9c'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256,
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        f = Fernet(key)
        # read the encrypted contents of the file
        with open(file_path, "rb") as file:
             encrypted_data = file.read()

        # decrypt the contents and write them to the file
        decrypted_data = f.decrypt(encrypted_data)
        with open(file_path, "wb") as file:
             file.write(decrypted_data)

        print(f"File {file_path} has been decrypted.")

if __name__ == '__main__': 
    main()
    
              