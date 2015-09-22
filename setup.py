from setuptools import setup, find_packages
from os.path import dirname, join
import phone_iso3166


def readfile(filename):
    with open(join(dirname(__file__), filename), 'r') as f:
        return f.read()

setup(
    name="phone-iso3166",
    description="Phonenumber to ISO 3166-1 mapping",
    install_requires=[
    ],
    keywords="oc",
    long_description=readfile("README.rst"),
    version=phone_iso3166.__version__,
    packages=find_packages(),
    maintainer="OC dev team",
    maintainer_email="devs@oc.dk",
)
