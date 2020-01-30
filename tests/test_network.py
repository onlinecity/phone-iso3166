from phone_iso3166.network import network, country_networks
from phone_iso3166.errors import InvalidNetwork, InvalidCountry
import pytest


def test_network():
    c, n = network(238, 1)
    assert c == 'DK'
    assert n == 'TDC A/S'

    c, n = network(238, 2)
    assert c == 'DK'
    assert n == 'Telenor Denmark'

    c, n = network(425, 6)
    assert c == 'PS'
    assert n == 'Wataniya Palestine Mobile Telecommunications Company'


def test_country_networks():
    nets = country_networks('US')
    for n in nets:
        mcc, mnc, name0 = n
        c, name1 = network(mcc, mnc)
        assert c == 'US'
        assert name0 == name1


def test_invalid_country():
    with pytest.raises(InvalidCountry):
        country_networks('XX')


def test_invalid_network():
    with pytest.raises(InvalidNetwork):
        network(0, 0)
