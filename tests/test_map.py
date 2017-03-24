from pycountry import countries
from phone_iso3166.e164 import mapping


def flatten(m):
    for i in m.values():
        if isinstance(i, dict):
            # yield from flatten(i)
            for c in flatten(i):
                yield c
        else:
            yield i


def exempt(c):
    '''
    Some countries we might wanna accept even though pycountry does not
    recognize it.
    Such is the case with Diego Garcia. It has an official ISO 3166-1 code of
    DG, and ITU code of 246, yet pycountry does know it, because it's not a
    real country.
    '''
    return c not in ['DG', 'XK']


def test_verify_iso3166():
    for c in filter(exempt, flatten(mapping)):
        country = countries.get(alpha_2=c)
        assert country
        assert country.alpha_2 == c
