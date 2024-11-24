import random
import string
from datetime import datetime, timedelta


def generate_username(size: int, min_letters: int, min_digits: int) -> str:
    """Generates a random username with at least `min_letters` letters, at least `min_digits` digits, and a total size of `size`."""
    remaining_size = size - (min_letters + min_digits)

    letters_count = min_letters + random.randint(0, remaining_size)
    digits_count = size - letters_count

    username = ''.join(random.choices(string.ascii_lowercase, k=letters_count)) + \
               ''.join(random.choices(string.digits, k=digits_count))

    return username


def generate_password(length: int = 12) -> str:
    """Generates a random password of fixed length with characters from at least two categories."""
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    punctuation = string.punctuation

    all_chars = lowercase + uppercase + digits + punctuation

    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(punctuation),
    ]

    password += random.choices(all_chars, k=length - 4)
    random.shuffle(password)

    return ''.join(password)


def generate_birthdate(lower_bound: str, upper_bound: str) -> str:
    """Generate a random birthdate between the lower and upper bounds."""
    lower_date = datetime.strptime(lower_bound, '%Y-%m-%d')
    upper_date = datetime.strptime(upper_bound, '%Y-%m-%d')

    delta_days = (upper_date - lower_date).days
    random_days = random.randint(0, delta_days)
    random_date = lower_date + timedelta(days=random_days)

    return random_date.strftime('%Y-%m-%d')
