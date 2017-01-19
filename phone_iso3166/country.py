from .e164 import mapping
from .e212 import networks
from .errors import InvalidPhone, InvalidNetwork, InvalidCountry


def phone_country(phone):
    '''
    Really simple function to get the ISO-3166-1 country from a phone number
    The phone number must be in E.164, aka international format.
    Returns an ISO-3166-1 alpha-2 code.
    '''
    m = mapping
    try:
        for c in filter(str.isdigit, str(phone)):
            m = m[int(c)]
            if isinstance(m, str):
                return m
    except:
        raise InvalidPhone('Invalid phone {}'.format(phone))


def country_prefixes():
    '''
    Function that return a dictionary, with an ISO-3166-1 alpha-2 code,
    as the key, and the country prefix as the value. For countries with
    multiple prefixes, an abitrary one of them is chosen, for United states
    and Canada code is denoted as 1.
    '''
    def transverse(node, path):
        if isinstance(node, dict):
            for k, v in node.items():
                for i in transverse(v, path + str(k)):
                    yield i
        else:
            yield node, 1 if node in ['US', 'CA'] else int(path)
    return dict(transverse(mapping, ''))


def country_prefix(country_code):
    '''
    Takes an ISO-3166-1 alpha-2 code. and returns the prefix for the country
    '''
    prefixes = country_prefixes()
    try:
        return prefixes[country_code.upper()]
    except:
        raise InvalidCountry('Invalid country {}'.format(country_code))


def phone_country_prefix(phone):
    '''
    Function that returns (dialingprefix, ISO-3166-1 country) from phone number
    '''
    m = mapping
    p = ''
    try:
        for c in filter(str.isdigit, str(phone)):
            m = m[int(c)]
            p += c
            if isinstance(m, str):
                return (int(p), m)
    except:
        raise InvalidPhone('Invalid phone {}'.format(phone))


def network_country(mcc, mnc):
    '''
    Get the country matching the MCC and MNC. In a few edgecases the MCC is not
    sufficient to identify the country, since some countries share MCC. However
    it's not often the case, so you could just specify MCC
    Returns an ISO-3166-1 alpha-2 code.
    '''
    try:
        c = networks[mcc]
        if isinstance(c, str):
            return c
        return c[mnc]
    except:
        raise InvalidNetwork('Invalid MCC {} MNC {}'.format(mcc, mnc))
