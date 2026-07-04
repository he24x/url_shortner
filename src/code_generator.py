import secrets
import string

def random_code_generator(length):
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

if __name__ == "__main__":
    for i in range(10):
        code = random_code_generator(8)
        print(code)