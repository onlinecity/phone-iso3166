import dataclasses
import os
import re
import tempfile
import time
import typing
from collections import defaultdict
from datetime import timedelta
from pathlib import Path
from pprint import pformat

import requests
from bs4 import BeautifulSoup


def get_wiki_page(url: str) -> Path:
    """Download a page.

    Stores the downloaded page in the OS temp dir, for up to 5 days, to allow
    for faster iteration when improving the script.
    """
    tmp_dir = Path(tempfile.gettempdir())
    outfile = tmp_dir / Path(os.path.basename(url))
    now = time.time()
    max_age = timedelta(days=5) / timedelta(seconds=1)
    if outfile.exists() and outfile.stat().st_mtime > now - max_age:
        print(f"{outfile} exists and is recent")
        return outfile

    print(f"downloading {url} to {outfile}")
    with open(outfile, "bw+") as fout:
        page_resp = requests.get(url)
        fout.write(page_resp.content)

    return outfile


OPERATOR_NAME_CLEANER = re.compile(r"\s+(\[.+\])?$")
COUNTRY_HEADER = re.compile(r"[A-Z]{2}-[A-Z]{2}|[A-Z]{2}")

# Some countries share MCC, and since the dataset groups by MCC, it can make
# it difficult to figure out the correct country for those MCCs.
# This provides a small override table to correct for those cases.
OVERRIDES = {
    # Guadaloupe is grouped with other French Overseas territories
    ("340", "01"): "GP",
    ("340", "02"): "GP",
    ("340", "03"): "GP",
    ("340", "08"): "GP",
    ("340", "09"): "GP",
    ("340", "20"): "GP",
    # The Former Netherlands Antilles is still grouped in one table
    ("362", "31"): "BQ",
    ("362", "33"): "CW",
    ("362", "51"): "SX",
    ("362", "54"): "CW",
    ("362", "59"): "BQ",
    ("362", "60"): "BQ",
    ("362", "63"): "CW",
    ("362", "68"): "CW",
    ("362", "69"): "CW",
    ("362", "74"): "CW",
    ("362", "76"): "BQ",
    ("362", "78"): "BQ",
    ("362", "91"): "CW",
    ("362", "94"): "CW",
    # Israeli MCC+MNCs used by a Palestinian operator
    ("425", "05"): "PS",
    ("425", "06"): "PS",
    # Australia is grouped with Christmas and Cook Islands
    ("505", "01"): "AU",
    ("505", "02"): "AU",
    ("505", "03"): "AU",
    ("505", "04"): "AU",
    ("505", "07"): "AU",
    ("505", "10"): "AU",
    ("505", "11"): "AU",
    ("505", "13"): "AU",
    ("505", "14"): "AU",
    ("505", "16"): "AU",
    ("505", "17"): "AU",
    ("505", "18"): "AU",
    ("505", "19"): "AU",
    ("505", "20"): "AU",
    ("505", "21"): "AU",
    ("505", "22"): "AU",
    ("505", "23"): "AU",
    ("505", "24"): "AU",
    ("505", "25"): "AU",
    ("505", "26"): "AU",
    ("505", "27"): "AU",
    ("505", "28"): "AU",
    ("505", "30"): "AU",
    ("505", "31"): "AU",
    ("505", "32"): "AU",
    ("505", "33"): "AU",
    ("505", "34"): "AU",
    ("505", "35"): "AU",
    ("505", "36"): "AU",
    ("505", "37"): "AU",
    ("505", "38"): "AU",
    ("505", "39"): "AU",
    ("505", "40"): "AU",
    ("505", "41"): "AU",
    ("505", "42"): "AU",
    ("505", "43"): "AU",
    ("505", "44"): "AU",
    ("505", "45"): "AU",
    ("505", "46"): "AU",
    ("505", "47"): "AU",
    ("505", "48"): "AU",
    ("505", "49"): "AU",
    ("505", "50"): "AU",
    ("505", "51"): "AU",
    ("505", "52"): "AU",
    ("505", "53"): "AU",
    ("505", "54"): "AU",
    ("505", "61"): "AU",
    ("505", "62"): "AU",
    ("505", "68"): "AU",
    ("505", "71"): "AU",
    ("505", "72"): "AU",
    ("505", "88"): "AU",
    ("505", "90"): "AU",
    # Reunion and Mayotte is also grouped
    ("647", "00"): "RE",
    ("647", "01"): "RE",
    ("647", "02"): "RE",
    ("647", "03"): "RE",
    ("647", "04"): "RE",
    ("647", "10"): "RE",
}


@dataclasses.dataclass
class OperatorEntry:
    """Container for scraped information about network operators.

    The basic building block we use to build our datasets from.
    """

    mcc: str
    mnc: str
    country_code: str
    name: str


def extract_page(path: Path) -> typing.Iterator[OperatorEntry]:
    """Yield MCC, MNC, country code and operator name entries from a page.

    Scrapes the wikipedia page that mostly follows a rigid structure.
    """
    with open(path, encoding="utf8") as fin:
        soup = BeautifulSoup(fin.read(), features="lxml")

    for country_header in soup.find_all("h4"):
        possible_countries = COUNTRY_HEADER.findall(country_header.text.strip())

        table_rows = country_header.find_next_sibling("table").find_all("tr")
        for row in table_rows:
            columns = row.find_all("td")
            if not columns:
                continue

            # Skip networks that are not in operation anymore.
            if columns[4].text.strip() == "Not operational":
                continue

            mcc = columns[0].text.strip()
            if len(mcc) != 3:
                mcc = mcc[-3:]

            mnc = columns[1].text.strip()

            # Some MNC entries on the wiki pages, define ranges with a hyphen
            # for now we can just skip them, but perhaps in time we should
            # expand them to the full ranges.
            if "-" in mnc:
                continue

            # Some MNC entries on the wiki pages, have unknown MNCs, which is
            # _problematic_ to say the least.
            if mnc == "?":
                continue

            # Due to the structure of the wiki dataset, we have no direct
            # mapping between MCC+MNC and country codes, only potential country
            # codes. If we have more than one potential country code, but no
            # rule for what the country should be in this case, raise an error.
            if len(possible_countries) != 1 and (mcc, mnc) not in OVERRIDES:
                raise ValueError(
                    f"missing override for: {mcc}:{mnc}, options: {possible_countries}"
                )

            if (mcc, mnc) in OVERRIDES:
                country_code = OVERRIDES[(mcc, mnc)]
            else:
                country_code = possible_countries[0]

            operator_name = OPERATOR_NAME_CLEANER.sub("", columns[3].text)

            yield OperatorEntry(
                mcc=mcc,
                mnc=mnc,
                country_code=country_code,
                name=operator_name,
            )


def main() -> None:
    """Extract information from a bunch of wiki pages to build the datasets from.

    While wiki is imperfect, the mappings between the datasets are not perfect
    either as some MCCs belong to government entities that are disputed, and some
    MCCs are shared by multiple countries.
    This makes a simple general mapping impossible and the code has to be able
    to handle a bunch of exceptions and just try to do a best effort mapping.
    """
    files = [
        "https://en.wikipedia.org/wiki/Mobile_network_codes_in_ITU_region_2xx_(Europe)",
        "https://en.wikipedia.org/wiki/Mobile_Network_Codes_in_ITU_region_3xx_(North_America)",
        "https://en.wikipedia.org/wiki/Mobile_network_codes_in_ITU_region_4xx_(Asia)",
        "https://en.wikipedia.org/wiki/Mobile_Network_Codes_in_ITU_region_5xx_(Oceania)",
        "https://en.wikipedia.org/wiki/Mobile_Network_Codes_in_ITU_region_6xx_(Africa)",
        "https://en.wikipedia.org/wiki/Mobile_Network_Codes_in_ITU_region_7xx_(South_America)",
    ]

    paths = [get_wiki_page(filename) for filename in files]

    extracted_pages = (values for path in paths for values in extract_page(path))

    operator_by_plmn = defaultdict(dict)
    for operator in extracted_pages:
        operator_by_plmn[int(operator.mcc)][int(operator.mnc)] = (
            operator.country_code,
            operator.name,
        )
    operator_by_plmn = dict(operator_by_plmn)

    countriesdict = defaultdict(list)
    for mcc, mncs in operator_by_plmn.items():
        for mnc, country in mncs.items():
            countriesdict[country[0]].append((mcc, mnc))
    countriesdict = dict(countriesdict)

    with open("phone_iso3166/e212_names.py", "w", encoding="utf8") as fout:
        fout.write("# pylint: disable=too-many-lines\n")
        fout.write("#!/usr/bin/env python\n")
        fout.write("# -*- coding: utf-8 -*-\n")
        fout.write("# Generated by get_e212.py\n")
        fout.write("# Based on https://en.wikipedia.org/wiki/Mobile_country_code\n")
        fout.write("operators = \\\n")
        fout.write(pformat(operator_by_plmn))

        fout.write("\n\n\ncountries = \\\n")
        fout.write(pformat(countriesdict))
        fout.write("\n")

    def reduce_operators(
        operators: typing.Dict[int, typing.Tuple[str, str]],
    ) -> typing.Union[str, typing.Dict[int, str]]:

        countries = {each[0] for each in operators.values()}
        if len(countries) == 1:
            return countries.pop()

        return {mnc: operator[0] for mnc, operator in operators.items()}

    plmns_to_country = {}
    for mcc, operator in operator_by_plmn.items():
        plmns_to_country[mcc] = reduce_operators(operator)

    with open("phone_iso3166/e212.py", "w", encoding="utf8") as fout:
        fout.write("# Generated by get_e212.py\n")
        fout.write("networks = ")
        fout.write(pformat(plmns_to_country))
        fout.write("\n")


if __name__ == "__main__":
    main()
