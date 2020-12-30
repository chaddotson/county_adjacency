County Adjacency
================

.. image:: https://github.com/chaddotson/county_adjacency/workflows/main/badge.svg
    :target: https://github.com/chaddotson/county_adjacency/actions?query=workflow%3Amain

.. image:: https://img.shields.io/pypi/v/county-adjacency.svg
    :target: https://pypi.org/project/county-adjacency/

.. image:: https://img.shields.io/pypi/pyversions/county-adjacency.svg
    :target: https://pypi.org/project/county-adjacency/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

This package provides adjacency information for US counties (or their equivalent). This data is derived
from the US Census `website`.

.. _website: https://www.census.gov/geographies/reference-files/2010/geo/county-adjacency.html

Example
-------
.. code-block:: python

    from county_adjacency import get_neighboring_areas, CountyNotFoundError, supported_areas

    try:
        print(get_neighboring_areas("San Francisco County, CA"))
    except CountyNotFoundError as error:
        print(error)

    ('Contra Costa County, CA', 'Marin County, CA', 'San Mateo County, CA')


    supported_areas()

    ('Autauga County, AL', 'Baldwin County, AL', ... , 'St. John Island, VI', 'St. Thomas Island, VI')
