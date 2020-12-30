"""Defines possible errors encountered during county adjacency discovery."""
from typing import Tuple


class CountyNotFoundError(RuntimeError):
    """Error when specified county, district, or like was not found."""

    def __init__(self, county: str, similar: Tuple[str] = None):
        """
        Create the error given the county and the list of similar counties found.

        :param county: The county requested
        :param similar: The list of similar counties found
        """
        self.county = county
        self.similar = similar if similar is not None else []

    def __str__(self):
        return f"""'{self.county}' not found. Perhaps you meant: '{"', '".join(self.similar)}'"""


class NoSimilarCountiesError(RuntimeError):
    """Error when no similar counties were found in the event of the requested county/like was not found."""

    def __init__(self, county: str):
        """
        Create the error given the county, district, like specified.

        :param county: The county requested
        """
        self.county = county

    def __str__(self):
        return f"No similar counties to '{self.county}' found."
