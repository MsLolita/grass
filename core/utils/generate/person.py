import random
import string

import names
from random_words import RandomNicknames  # pip install RandomWords


class Person:
    def __init__(self):
        self.username = RandomNicknames().random_nick(gender=random.choice(['f', 'm'])).lower() + \
                        Person.random_string_old(3) + str(random.randint(1, 9))
        self.first_name, self.last_name = names.get_full_name().split(" ")

    @staticmethod
    def random_string_old(length, chars=string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(length))

    @staticmethod
    def random_string(length=8, chars=string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(length)) + random.choice(string.digits) + random.choice(
            string.ascii_uppercase) + random.choice(['.', '@', '!', "$"])

    def generate_email(self):
        return f"{self.username[:-random.choice(range(1, 3))].lower()}@{random.choice(['gmail.com', 'outlook.com', 'yahoo.com'])}"
