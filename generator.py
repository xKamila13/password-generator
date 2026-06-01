import random
import string

LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*_+-=?"

def generate_password(length=12, hard=False):

    pool = LOWERCASE + UPPERCASE + DIGITS

    guaranteed = [
        random.choice(LOWERCASE),
        random.choice(UPPERCASE),
        random.choice(DIGITS),
    ]

    if hard:
        pool += SYMBOLS
        guaranteed.append(random.choice(SYMBOLS))

    remaining = length - len(guaranteed)
    random_chars = [random.choice(pool) for _ in range(remaining)]

    all_chars = guaranteed + random_chars
    random.shuffle(all_chars)

    password = "".join(all_chars)
    return password, None


def evaluate_strength(password):

    has_lower   = any(c in LOWERCASE for c in password)
    has_upper   = any(c in UPPERCASE for c in password)
    has_digit   = any(c in DIGITS    for c in password)
    has_symbol  = any(c in SYMBOLS   for c in password)
    length      = len(password)

    if has_symbol and length >= 12:
        return {"label": "Hard",   "color": "#44BB44", "value": 1.00}
    elif has_symbol and length >= 7:
        return {"label": "Hard",   "color": "#44BB44", "value": 0.85}
    elif has_lower and has_upper and has_digit and length >= 12:
        return {"label": "Medium", "color": "#FFCC00", "value": 0.60}
    else:
        return {"label": "Easy",   "color": "#FF8800", "value": 0.35}