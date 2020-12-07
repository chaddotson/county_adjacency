"""Provides adjacent county information."""

from county_adjacency.adjacency import get_neighboring_counties, supported_counties
from county_adjacency.errors import CountyNotFoundError, NoSimilarCountiesError

__all__ = ["CountyNotFoundError", "get_neighboring_counties", "NoSimilarCountiesError", "supported_counties"]

__version__ = "0.1.1"
