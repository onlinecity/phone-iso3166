from .e164 import mapping
from .e212 import networks


class InvalidPhone(Exception):
    pass


class InvalidNetwork(Exception):
    pass


def phone_country(phone):
    '''
    Really simple function to get the ISO-3166-1 country from a phone number
    The phone number must be in E.164, aka international format.
    '''
    m = mapping
    try:
        for c in filter(str.isdigit, str(phone)):
            m = m[int(c)]
            if isinstance(m, str):
                return m
    except:
        raise InvalidPhone('Invalid phone {}'.format(phone))


def network_country(mcc, mnc):
    try:
        c = networks[mcc]
        if isinstance(c, str):
            return c
        return c[mnc]
    except:
        raise InvalidNetwork('Invalid MCC {} MNC {}'.format(mcc, mnc))
