import pytest

from phone_iso3166.errors import InvalidCountry
from phone_iso3166.errors import InvalidNetwork
from phone_iso3166.network import country_networks
from phone_iso3166.network import network


@pytest.mark.parametrize(
    "mcc, mnc, country_code, network_name",
    [
        (238, 1, "DK", "TDC A/S"),
        (238, 2, "DK", "Telenor Denmark"),
        (425, 6, "PS", "Ooredoo Palestine"),
    ],
)
def test_network(mcc, mnc, country_code, network_name):
    assert network(mcc, mnc) == (country_code, network_name)


def test_country_networks():
    networks = country_networks("US")
    for mcc, mnc, network_name in networks:
        assert network(mcc, mnc) == ("US", network_name)


def test_invalid_country():
    with pytest.raises(InvalidCountry):
        country_networks("XX")


def test_invalid_network():
    with pytest.raises(InvalidNetwork):
        network(0, 0)
