import secrets
import string
from .database import exists

#hash table to store the generated codes and their corresponding URLs

def random_code_generator(length):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def generate_unique_code(length):
    while True:
        code = random_code_generator(length)
        if not exists(code):
            return code