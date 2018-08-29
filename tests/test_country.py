from phone_iso3166.country import (
    phone_country, phone_country_prefix, network_country, country_prefixes,
    country_prefix
)
from phone_iso3166.errors import InvalidNetwork, InvalidPhone, InvalidCountry
import pytest


def test_phone_country_dk():
    assert phone_country(45) == 'DK'
    assert phone_country(4566118311) == 'DK'
    assert phone_country('+4566118311') == 'DK'
    assert phone_country('+38640404040') == 'SI'
    assert phone_country('+38340404040') == 'XK'
    assert phone_country('+37740404040') == 'MC'


def test_country_prefixes():
    assert isinstance(country_prefixes(), dict)


def test_country_prefix():
    assert country_prefix('dk') == 45
    assert country_prefix('DK') == 45
    assert country_prefix('Dk') == 45
    assert country_prefix('us') == 1


def test_country_invalid():
    with pytest.raises(InvalidCountry):
        country_prefix('dkk')


def test_invalid():
    with pytest.raises(InvalidPhone):
        phone_country(0)


def test_missing():
    with pytest.raises(InvalidPhone):
        phone_country(999)
    with pytest.raises(InvalidPhone):
        phone_country('999')


def test_whitehouse():
    # White house comment line
    assert phone_country('+1 202-456-1111') == 'US'


def test_bermuda():
    # Bermuda city hall
    assert phone_country(14412921234) == 'BM'


def test_network_dk():
    assert network_country(238, 1) == 'DK'


def test_network_multi():
    assert network_country(340, 1) == 'GP'   # Guadeloupe
    assert network_country(340, 12) == 'MQ'  # Martinique


def test_network_invalid():
    with pytest.raises(InvalidNetwork):
        network_country(0, 0)


def test_phone_country_prefix():
    assert phone_country_prefix(45) == (45, 'DK')
    assert phone_country_prefix(4566118311) == (45, 'DK')
    assert phone_country_prefix('+4566118311') == (45, 'DK')
    assert phone_country_prefix('299 80 80 80') == (299, 'GL')
    assert phone_country_prefix(14412921234) == (1441, 'BM')
