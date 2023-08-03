#!/usr/bin/env python3
'''
   Task 5: Encrypting passwords
   Task 6: Check valid password
'''
import bcrypt


def hash_password(password: str) -> bytes:
    '''function that expects one string argument name password
    and returns a salted, hashed password, which is a byte string.
    '''
    pass_encoded = password.encode()
    pass_hashed = bcrypt.hashpw(pass_encoded, bcrypt.gensalt())

    return pass_hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''check for validty of the password.
    It uses bcrypt library
    '''
    valid = False
    pass_encoded = password.encode()
    if bcrypt.checkpw(pass_encoded, hashed_password):
        valid = True
    return valid
