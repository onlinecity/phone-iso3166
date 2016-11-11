Phone-ISO3166 |build-status| |coverage-status|
==============================================
Small project to map an E.164 (international) phone number to the
ISO-3166-1 alpha 2 (two letter) country code, associated with that number.

Also provides mapping for E.212 (mobile network codes, mcc+mnc) to the country.

The package has no dependencies, and works on Py2.7+, Py3 and PyPy.


Simple Usage
------------

To simply get a country code from a phone number or mcc, mnc.

.. code:: pycon


    >>> from phone_iso3166.country import *
    >>> phone_country(45)
    'DK'
    >>> phone_country('+1 202-456-1111')
    'US'
    >>> phone_country(14412921234)
    'BM'
    >>> network_country(238, 1)
    'DK'


Network names and codes
-----------------------

If you want more detailed information about the networks, such as the operator
name use the functions in `phone_iso3166.network`.

.. code:: pycon


    >>> from phone_iso3166.network import *
    >>> network(238, 1)
    ('DK', 'TDC Mobil')
    >>> country_networks('DK')
    [(238, 1, 'TDC Mobil'), (238, 2, 'Sonofon'), (238, 3, 'MIGway A/S'),
     (238, 4, 'NextGen Mobile Ltd T/A CardBoardFish'), (238, 6, 'Hi3G'),
     (238, 8, 'Nordisk Mobiltelefon Danmark A/S'), (238, 10, 'TDC Mobil'),
     (238, 43, 'MobiWeb Limited'), (238, 12, 'Lycamobile Denmark'),
     (238, 13, 'Compatel Limited'), (238, 77, 'Tele2'), (238, 20, 'Telia'),
     (238, 66, 'TT-Netvaerket P/S'), (238, 28, 'CoolTEL'),
     (238, 30, 'Interactive Digital Media GmbH')]


More information
----------------

If want more information, you can easily use the country code with other python
packages such as `pycountry`_.

.. code:: pycon


    >>> from phone_iso3166.country import phone_country
    >>> import pycountry
    >>> phone = '+55 21 3814-2121'
    >>> c = pycountry.countries.get(alpha_2=phone_country(phone))
    >>> c.name
    'Brazil'
    >>> c.official_name
    'Federative Republic of Brazil'


This package makes no attempt to understand the various input options for
phone numbers, and assumes an international phone number. If you deal in fuzzy
inputs, try `phonenumbers`_.

.. code:: pycon


    >>> from phone_iso3166.country import phone_country
    >>> import phonenumbers
    >>> import pycountry
    >>> local = phonenumbers.parse("020 8366 1177", "GB")
    >>> phonenumbers.format_number(local, phonenumbers.PhoneNumberFormat.E164)
    '+442083661177'
    >>> cc = phone_country(str(local.country_code)+str(local.national_number))
    >>> uk = pycountry.countries.get(alpha_2=cc)
    >>> uk.name
    'United Kingdom'
    >>> uk.official_name
    'United Kingdom of Great Britain and Northern Ireland'
    >>> wh = phonenumbers.parse("0012024561111", "GB")
    >>> cc_wh = phone_country(str(wh.country_code)+str(wh.national_number))
    >>> cc_wh
    'US'


.. |build-status| image:: https://travis-ci.org/onlinecity/phone-iso3166.svg?branch=master
   :target: https://travis-ci.org/onlinecity/phone-iso3166
.. |coverage-status| image:: https://img.shields.io/coveralls/onlinecity/phone-iso3166.svg
   :target: https://coveralls.io/r/onlinecity/phone-iso3166
.. _pycountry: https://pypi.python.org/pypi/pycountry
.. _phonenumbers: https://pypi.python.org/pypi/phonenumberslite
