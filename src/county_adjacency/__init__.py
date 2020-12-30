"""Provides adjacent county information."""

from county_adjacency.adjacency import get_neighboring_areas, supported_areas
from county_adjacency.errors import CountyNotFoundError, NoSimilarCountiesError

__all__ = ["CountyNotFoundError", "get_neighboring_areas", "NoSimilarCountiesError", "supported_areas"]

__version__ = "0.1.3"
