from .e212_names import operators, countries
from .errors import InvalidNetwork, InvalidCountry


def network(mcc, mnc):
    '''
    Returns a tuple (country, network_name), with country specified as
    ISO-3166-1 alpha-2 code.
    '''
    mcc = int(mcc)
    mnc = int(mnc)
    try:
        return operators[mcc][mnc]
    except:
        raise InvalidNetwork('Invalid MCC {} MNC {}'.format(mcc, mnc))


def country_networks(country):
    '''
    Returns a list of tuples (mcc, mnc, network_name) with all the networks
    belonging to the specified country.
    The country must be specified as an ISO-3166-1 alpha-2 code.
    '''
    try:
        return [(m[0], m[1], operators[m[0]][m[1]][1])
                for m in countries[country]]
    except:
        raise InvalidCountry('Invalid country {}'.format(country))
