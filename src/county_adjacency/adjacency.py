from Levenshtein import ratio as levenshtein_ratio
from logging import getLogger
from operator import itemgetter
from typing import Tuple, List, Union


from county_adjacency.data import united_states_adjacency_data
from county_adjacency.errors import CountyNotFoundError, NoSimilarCountiesError

logger = getLogger(__name__)

# The threshold used to filter similar county, district or like names based on their Levenshtein ratio.
LEVENSHTEIN_THRESHOLD = 0.7

# Simple error correction measures.
__error_correction_county_formats = [
    "{county} County, {state}",
    "{county} Municipality, {state}",
    "{county} Municipio, {state}",
    "{county} District, {state}",
]


def get_neighboring_areas(
    county_or_like: str,
    attempt_error_correction: bool = True,
    use_best_match: bool = False,
) -> Tuple[str]:
    """
    Get the adjacent counties (or equivalent) given a specified county (or equivalent).

    :param county_or_like: The full name of the county, or county equivalent. ie 'San Francisco County, CA'"
    :param attempt_error_correction: Should package attempt to resolve simple naming errors. Default: True
    :param use_best_match: Indicates the package attempt to resolve more complicated naming errors. Default: False
    :return: A tuple containing the full names of the neighboring counties.
    :raises CountyNotFoundError: If the specified county was not found.
    """
    if county_or_like not in united_states_adjacency_data:
        if not attempt_error_correction:
            similar = find_similar_counties(county_or_like)
            raise CountyNotFoundError(county_or_like, similar)

        try:
            county_or_like = correct_county_name_errors(county_or_like, use_best_match)
        except NoSimilarCountiesError as e:
            raise CountyNotFoundError(county_or_like) from e

    return tuple(united_states_adjacency_data[county_or_like]["adjacent"])


def correct_county_name_errors(county_id: str, use_best_match: bool) -> str:
    """
    Attempt to correct county, district or like name errors.

    :param county_id: The created "county id"
    :param use_best_match: Accept fuzzy matches automatically.
    :return: The "county id" after correction has taken place.
    :raises NoSimilarCountiesError: In the event no similar counties are found.
    """
    best_county_id = county_id
    try:
        county, state = county_id.split(", ")
        best_county_id = correct_missing_county_or_like(county, state)

    except ValueError:
        pass

    if best_county_id is None and use_best_match:
        similar = find_similar_counties(county_id)
        best_county_id = similar[0] if len(similar) > 0 else None

    if best_county_id is None:
        raise NoSimilarCountiesError(county_id)

    return best_county_id


def correct_missing_county_or_like(county: str, state: str) -> Union[str, None]:
    """
    Attempt to correct a county missing the "County", "District" or like designator.

    :param county: The specified county
    :param state: The state of the specified county
    :return: A new county id that is in the list of supported counties.
    """
    logger.debug("Attempting to correct '%s, %s'", county, state)
    for test_format in __error_correction_county_formats:
        test_county_id = test_format.format(county=county, state=state)
        logger.debug("Trying '%s'", test_county_id)
        if test_county_id in united_states_adjacency_data:
            logger.debug("'%s' not found, suggesting '%s'.", county, test_county_id)
            return test_county_id
    return None


def find_similar_counties(county_id: str) -> Tuple[str, ...]:
    """
    Wrap finding similar county names.

    :param county_id: The id of a county: format: "County, STATE"
    :return: A tuple of county names similar to the specified.
    :raises NoSimilarCountiesError: In the event no similar counties are found.
    """
    candidates = create_ranked_candidate_counties(county_id)
    logger.debug("Found similar candidates for %s: %s", county_id, candidates)
    return next(zip(*candidates))


def create_ranked_candidate_counties(county_id: str) -> List[Tuple[str, str]]:
    """
    Create a list of the top 10 similar counties using the Levenshtein ratio.

    :param county_id: The id of a county: format: "County, STATE"
    :return: A list tuples of counties, districts, etc similar to the supplied with their Levenshtein ratio.
    :raises NoSimilarCountiesError: In the event no similar counties are found.
    """
    candidates = []
    for found in united_states_adjacency_data.keys():
        rating = levenshtein_ratio(county_id, found)
        if rating > LEVENSHTEIN_THRESHOLD:
            candidates.append((found, rating))
    if len(candidates) == 0:
        raise NoSimilarCountiesError(county_id)
    return sorted(candidates[0:10], key=itemgetter(1), reverse=True)


def supported_areas() -> Tuple[str]:
    """
    Return a tuple of supported counties.

    :return: A tuple of supported counties
    """
    return tuple(united_states_adjacency_data.keys())
