import string
import random

def generate_password():
    characters = list(string.ascii_lowercase)
    random.shuffle(characters)
    password = []
    for i in range(5):
        password.append(random.choice(characters))
    random.shuffle(password)
    return ''.join(password)