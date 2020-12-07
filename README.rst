# County Adjacency

.. image:: https://travis-ci.org/chaddotson/county_adjacency.svg?branch=main
    :target: https://travis-ci.org/chaddotson/county_adjacency

.. code-block:: python

    from county_adjacency import get_neighboring_counties, CountyNotFoundError

    try:
        print(get_neighboring_counties("San Francisco County, CA"))
    except CountyNotFoundError as error:
        print(error)
