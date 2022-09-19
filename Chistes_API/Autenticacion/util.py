'''
from binascii import unhexlify
from os import urandom
import random
import string

from django.core.exceptions import ValidationError

def hex_validator(length=0):
    def _validator(value):
        try:
            if isinstance(value, str):
                value = value.encode()

            unhexlify(value)
        except Exception:
            raise ValidationError('{0} is not valid hex-encoded data.'.format(value))

        if (length > 0) and (len(value) != length * 2):
            raise ValidationError('{0} does not represent exactly {1} bytes.'.format(value, length))

    return _validator


def random_hex(length=20):
    return urandom(length).hex()


def random_number_token(length=6):    
    rand = random.SystemRandom()

    if hasattr(rand, 'choices'):
        digits = rand.choices(string.digits, k=length)
    else:
        digits = (rand.choice(string.digits) for i in range(length))

    return ''.join(digits)

'''    