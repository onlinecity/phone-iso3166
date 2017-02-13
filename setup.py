from setuptools import setup, find_packages
from os.path import dirname, join
import phone_iso3166


def readfile(filename):
    with open(join(dirname(__file__), filename), 'r') as f:
        return f.read()


setup(
    name="phone-iso3166",
    description="Phonenumber to Country (ISO 3166-1) mapping",
    install_requires=[
    ],
    keywords="phone country mobile iso3166 e164 e212 countrycode phonenumber",
    long_description=readfile("README.rst"),
    version=phone_iso3166.__version__,
    packages=find_packages(),
    maintainer="OC dev team",
    maintainer_email="devs@oc.dk",
    license='MIT',
    classifiers=(
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English'
    )
)
