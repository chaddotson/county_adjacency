from pathlib import Path
from json import dump

__data = None

# https://www.census.gov/geographies/reference-files/2010/geo/county-adjacency.html

DATA_FILE_ENCODING = "ISO8859-1"

data = {}
with open(
    Path(__file__).parent / "county_adjacency" / "data" / "county_adjacency.txt",
    "r",
    encoding=DATA_FILE_ENCODING,
) as f:
    contents = f.read().splitlines()

    current_mark = ""

    for i, line in enumerate(contents):

        tab_delimited = [_.strip('"') for _ in contents[i].split("\t")]

        if not len(tab_delimited) == 4:
            continue

        mark_county, mark_county_fips, adjacent_county, adjacent_county_fips = tab_delimited

        if not mark_county == "":
            current_mark = mark_county
            data[current_mark] = dict(fips=mark_county_fips, adjacent=[])
            continue

        if current_mark == adjacent_county:
            continue

        data[current_mark]["adjacent"].append(adjacent_county)

    with open(
        Path(__file__).parent / "county_adjacency" / "data" / "county_adjacency.json",
        "w",
    ) as f:
        dump(data, f, indent=4)
