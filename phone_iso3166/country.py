# pylint: disable=consider-using-f-string
from .e164 import mapping
from .e212 import networks
from .errors import InvalidCountry
from .errors import InvalidNetwork
from .errors import InvalidPhone


def phone_country(phone):  # pylint: disable=inconsistent-return-statements
    """Return the ISO-3166-1 country code a given phone number belongs to.

    The phone number must be specified in E.164, aka international format.
    The returned country code is of ISO-3166-1 alpha-2 code.
    """

    e164_mapping = mapping
    try:
        for digit in filter(str.isdigit, str(phone)):
            e164_mapping = e164_mapping[int(digit)]
            if isinstance(e164_mapping, str):
                return e164_mapping
    except Exception as ex:
        raise InvalidPhone("Invalid phone {}".format(phone)) from ex


def country_prefixes():
    """Return a mapping of country code to calling prefix.

    For countries with multiple prefixes, an arbitrary calling prefix is
    chosen. Many north american country codes just map to 1.
    """

    def transverse(node, path):
        if isinstance(node, dict):
            for key, value in node.items():
                for i in transverse(value, path + str(key)):
                    yield i
        else:
            yield node, 1 if node in ["US", "CA"] else int(path)

    return dict(transverse(mapping, ""))


def country_prefix(country_code):
    """Return the calling prefix for a given country.

    The country must be provided as a ISO-3166-1 alpha-2 country code.
    """
    prefixes = country_prefixes()
    try:
        return prefixes[country_code.upper()]
    except Exception as ex:
        raise InvalidCountry("Invalid country {}".format(country_code)) from ex


def phone_country_prefix(phone):  # pylint: disable=inconsistent-return-statements
    """Figure out that calling prefix and country a phone number belongs to.

    The country returned is in the form of a ISO-3166-1 alpha-2 country code.
    """
    e164_mapping = mapping
    prefix = ""
    try:
        for digit in filter(str.isdigit, str(phone)):
            e164_mapping = e164_mapping[int(digit)]
            prefix += digit
            if isinstance(e164_mapping, str):
                return (int(prefix), e164_mapping)
    except Exception as ex:
        raise InvalidPhone("Invalid phone {}".format(phone)) from ex


def network_country(mcc, mnc):
    """Return the country matching mcc and mnc.

    A few countries share mcc, so to work in more cases the mnc needs to be
    provided for a secondary lookup.

    Returns an ISO-3166-1 alpha-2 country code.
    """
    try:
        country = networks[mcc]
        if isinstance(country, str):
            return country
        return country[mnc]
    except Exception as ex:
        raise InvalidNetwork("Invalid MCC {} MNC {}".format(mcc, mnc)) from ex
