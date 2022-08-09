# pylint: disable=consider-using-f-string
import typing

from .e164 import mapping
from .e212 import networks
from .errors import InvalidCountry
from .errors import InvalidNetwork
from .errors import InvalidPhone


def phone_country(phone: typing.Union[str, int]) -> str:
    """Return the ISO-3166-1 country code a given phone number belongs to.

    The phone number must be specified in E.164, aka international format.
    The returned country code is of ISO-3166-1 alpha-2 code.
    """

    def traverse_tree(
        key: typing.Iterable[int],
        tree: dict,
    ) -> str:
        next_key, *remaining_keys = key
        next_element: typing.Union[str, typing.Dict[int, str]] = tree[next_key]
        if isinstance(next_element, dict):
            return traverse_tree(remaining_keys, next_element)

        return next_element

    if not isinstance(phone, str):
        phone = str(phone)

    try:
        return traverse_tree(
            (int(digit) for digit in phone if digit.isdigit()),
            mapping,
        )
    except (KeyError, ValueError) as ex:
        raise InvalidPhone("Invalid phone {}".format(phone)) from ex


def country_prefixes() -> typing.Dict[str, int]:
    """Return a mapping of country code to calling prefix.

    For countries with multiple prefixes, an arbitrary calling prefix is
    chosen. Many north american country codes just map to 1.
    """

    def traverse(
        node: typing.Union[dict, str],
        path: str,
    ) -> typing.Iterator[typing.Tuple[str, int]]:
        if isinstance(node, dict):
            for key, value in node.items():
                yield from traverse(value, path + str(key))
        else:
            yield node, 1 if node in ["US", "CA"] else int(path)

    return dict(traverse(mapping, ""))


def country_prefix(country_code: str) -> int:
    """Return the calling prefix for a given country.

    The country must be provided as a ISO-3166-1 alpha-2 country code.
    """
    prefixes = country_prefixes()
    try:
        return prefixes[country_code.upper()]
    except Exception as ex:
        raise InvalidCountry("Invalid country {}".format(country_code)) from ex


def phone_country_prefix(
    phone: typing.Union[str, int],
) -> typing.Tuple[int, str]:
    """Figure out that calling prefix and country a phone number belongs to.

    The country returned is in the form of a ISO-3166-1 alpha-2 country code.
    """

    def traverse_tree(
        key: typing.Iterable[int],
        tree: dict,
        key_so_far: str = "",
    ) -> typing.Tuple[int, str]:
        next_key, *remaining_keys = key
        next_element: typing.Union[str, typing.Dict[int, str]] = tree[next_key]
        key_so_far = key_so_far + str(next_key)
        if isinstance(next_element, dict):
            return traverse_tree(
                remaining_keys,
                next_element,
                key_so_far,
            )

        return int(key_so_far), next_element

    if not isinstance(phone, str):
        phone = str(phone)

    try:
        return traverse_tree(
            (int(digit) for digit in phone if digit.isdigit()),
            mapping,
        )
    except (KeyError, ValueError) as ex:
        raise InvalidPhone("Invalid phone {}".format(phone)) from ex


def network_country(mcc: int, mnc: int) -> str:
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
