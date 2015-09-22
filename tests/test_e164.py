from phone_iso3166.e164 import get_country, InvalidPhone
import pytest


def test_get_country_dk():
    assert get_country(45) == 'DK'
    assert get_country(4566118311) == 'DK'
    assert get_country('+4566118311') == 'DK'


def test_invalid():
    with pytest.raises(InvalidPhone):
        get_country(0)


def test_missing():
    with pytest.raises(InvalidPhone):
        get_country(999)
    with pytest.raises(InvalidPhone):
        get_country('999')


def test_whitehouse():
    # White house comment line
    assert get_country('+1 202-456-1111') == 'US'


def test_bermuda():
    # Bermuda city hall
    assert get_country(14412921234) == 'BM'
