import os
import random

alphabet = []

with open(f'{os.getcwd()}/resources/alphabet.txt', 'r') as _alphabet:
    for character in _alphabet:
        alphabet.append(character)


def digit_identifier(length: int = 10) -> str:
    """
    Generate random integers from 1 to 9 and concatenate the digits
    together for a length of zero to *length*.

    :param: int length: The amount of random digits to concatenate.
    :return: The generated digit identifier.
    :rtype: str
    """
    _identifier = [str(random.randint(1, 9)) for _ in range(0, length)]
    _identifier = ''.join(_identifier)
    return _identifier


def string_identifier(length: int = 10) -> str:
    """
    Generate random upper and lowercase characters and concatenate
    them for a length of zero to *length*.
    :param: int length: The amount of random characters to concatenate.
    :return: The generated string identifier.
    :rtype: str
    """
    _identifier = [alphabet[random.randint(0, len(alphabet) - 1)].rstrip() for _ in range(0, length)]
    _identifier = ''.join(_identifier)
    return _identifier
