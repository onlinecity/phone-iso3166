import pytest

from phone_iso3166.country import country_prefix
from phone_iso3166.country import country_prefixes
from phone_iso3166.country import network_country
from phone_iso3166.country import phone_country
from phone_iso3166.country import phone_country_prefix
from phone_iso3166.errors import InvalidCountry
from phone_iso3166.errors import InvalidNetwork
from phone_iso3166.errors import InvalidPhone


@pytest.mark.parametrize(
    "phone_number, country_code",
    [
        (45, "DK"),
        (4566118311, "DK"),
        ("+4566118311", "DK"),
        ("+38640118311", "SI"),
        ("+38340118311", "XK"),
        ("+37740118311", "MC"),
        ("+77401183119", "KZ"),
        ("+79901185311", "RU"),
        ("+97040118311", "PS"),
    ],
)
def test_phone_country_dk(phone_number, country_code):
    assert phone_country(phone_number) == country_code


def test_country_prefixes():
    assert isinstance(country_prefixes(), dict)


@pytest.mark.parametrize(
    "country_code, calling_prefix",
    [
        ("dk", 45),
        ("DK", 45),
        ("Dk", 45),
        ("us", 1),
        ("xK", 383),
    ],
)
def test_country_prefix(country_code, calling_prefix):
    assert country_prefix(country_code) == calling_prefix


def test_country_invalid():
    with pytest.raises(InvalidCountry):
        country_prefix("dkk")


def test_invalid():
    with pytest.raises(InvalidPhone):
        phone_country(0)


def test_missing():
    with pytest.raises(InvalidPhone):
        phone_country(999)

    with pytest.raises(InvalidPhone):
        phone_country("999")


@pytest.mark.parametrize(
    "phone_number, country_code",
    [
        ("+1 202-456-1111", "US"),
        (14412921234, "BM"),
    ],
)
def test_country_lookup(phone_number, country_code):
    assert phone_country(phone_number) == country_code


@pytest.mark.parametrize(
    "mcc, mnc, country_code",
    [
        (238, 1, "DK"),  # Denmark
        (340, 1, "GP"),  # Guadeloupe
        (340, 12, "GP"),  # Also Guadeloupe
        (425, 5, "PS"),  # Palestine
        (425, 6, "PS"),  # Palestine
        (425, 7, "IL"),  # Israel
        (505, 20, "AU"),  # Australia
        (362, 31, "BQ"),  # Sint Eustatius, formerly Netherlands Antilles
        (362, 51, "SX"),  # Sint Maarten, formerly Netherlands Antillies
        (647, 0, "RE"),  # Reunion
        (647, 1, "YT"),  # Mayotte
    ],
)
def test_network_multi(mcc, mnc, country_code):
    assert network_country(mcc, mnc) == country_code


def test_network_invalid():
    with pytest.raises(InvalidNetwork):
        network_country(0, 0)


@pytest.mark.parametrize(
    "phone_number, calling_prefix, country_code",
    [
        (45, 45, "DK"),
        (4566118311, 45, "DK"),
        ("+4566118311", 45, "DK"),
        ("299 80 80 80", 299, "GL"),
        (14412921234, 1441, "BM"),
    ],
)
def test_phone_country_prefix(phone_number, calling_prefix, country_code):
    assert phone_country_prefix(phone_number) == (calling_prefix, country_code)


@pytest.mark.parametrize(
    "phone_number, country_code",
    [
        (12797597235, "US"),
        (14458883022, "US"),
        (18204000053, "US"),
    ],
)
def test_us_country(phone_number, country_code):
    assert phone_country(phone_number) == country_code
