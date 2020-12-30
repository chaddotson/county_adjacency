# County Adjacency

.. image:: https://github.com/chaddotson/county_adjacency/workflows/testing/badge.svg
    :target: https://github.com/chaddotson/county_adjacency/actions?query=workflow%3Atesting

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black


.. code-block:: python

    from county_adjacency import get_neighboring_counties, CountyNotFoundError

    try:
        print(get_neighboring_counties("San Francisco County, CA"))
    except CountyNotFoundError as error:
        print(error)
