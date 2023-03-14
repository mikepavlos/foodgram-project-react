import re

from django.core.exceptions import ValidationError


def username_validator(value):
    if value == 'me':
        raise ValidationError(
            'Использовать имя "me" в качестве username запрещено.'
        )

    if re.search(r'^[\w.@+-]+\Z', value) is None:
        raise ValidationError(
            'Имя может содержать буквы, цифры и символы @/./+/-/_'
        )
    return value
