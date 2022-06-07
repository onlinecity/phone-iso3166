# pylint: disable=consider-using-f-string
from .e212_names import countries
from .e212_names import operators
from .errors import InvalidCountry
from .errors import InvalidNetwork


def network(mcc, mnc):
    """Return country code and network name for a mcc and mnc combination.

    The country code is returned as a ISO-3166-1 alpha-2 code.
    """
    mcc = int(mcc)
    mnc = int(mnc)
    try:
        return operators[mcc][mnc]
    except Exception as ex:
        raise InvalidNetwork("Invalid MCC {} MNC {}".format(mcc, mnc)) from ex


def country_networks(country):
    """Return tuples of all networks for a given country.

    The country must be provided as a ISO-3166-1 alpha-2 country code.
    The returned for is (mcc, mnc, network_name).
    """
    try:
        return [(m[0], m[1], operators[m[0]][m[1]][1]) for m in countries[country]]
    except Exception as ex:
        raise InvalidCountry("Invalid country {}".format(country)) from ex
