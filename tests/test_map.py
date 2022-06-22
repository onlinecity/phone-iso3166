from pycountry import countries

from phone_iso3166.e164 import mapping


def extract_country_codes(prefix_tree):
    for country_code in prefix_tree.values():
        if isinstance(country_code, dict):
            yield from extract_country_codes(country_code)
        else:
            yield country_code


def test_verify_iso3166():
    for contry_code in extract_country_codes(mapping):
        if contry_code in ("DG", "XK"):
            # Some places have calling prefixes, but are not recognized as
            # countries in their own right. This leads to edgecases.
            continue
        country = countries.get(alpha_2=contry_code)
        assert country is not None
        assert country.alpha_2 == contry_code
