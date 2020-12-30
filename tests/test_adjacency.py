from pytest import raises

from unittest.mock import patch

from county_adjacency.adjacency import (
    correct_missing_county_or_like,
    united_states_adjacency_data,
    supported_areas,
    find_similar_counties,
    correct_county_name_errors,
    get_neighboring_areas,
    create_ranked_candidate_counties,
)
from county_adjacency.errors import CountyNotFoundError, NoSimilarCountiesError


def test_correct_missing_county():
    assert correct_missing_county_or_like("San Francisco", "CA") == "San Francisco County, CA"


def test_correct_missing_municipality():
    assert correct_missing_county_or_like("Saipan", "MP") == "Saipan Municipality, MP"


def test_correct_missing_municipio():
    assert correct_missing_county_or_like("Villalba", "PR") == "Villalba Municipio, PR"


def test_correct_missing_district():
    assert correct_missing_county_or_like("Eastern", "AS") == "Eastern District, AS"


def test_correct_missing_county_finds_nothing():
    assert correct_missing_county_or_like("Non Existent", "CA") is None


def test_get_supported_counties():
    with patch.dict(united_states_adjacency_data, {"Test County, TS": {}}, clear=True):
        assert supported_areas() == ("Test County, TS",)


def test_can_get_ranked_counties():
    test_data = {
        "San Francisco County, CA": {},
        "San Mateo County, CA": {},
        "San Banito County, CA": {},
    }

    with patch.dict(united_states_adjacency_data, test_data, clear=True):
        print(create_ranked_candidate_counties("San Francisco County, CA"))
        assert create_ranked_candidate_counties("San Francisco County, CA") == [
            ("San Francisco County, CA", 1.0),
            ("San Banito County, CA", 0.8444444444444444),
            ("San Mateo County, CA", 0.7727272727272727),
        ]


def test_ranked_counties_are_sorted_best_match_first():
    test_data = {
        "San Mateo County, CA": {},
        "San Francisco County, CA": {},
        "San Banito County, CA": {},
    }

    with patch.dict(united_states_adjacency_data, test_data, clear=True):
        assert create_ranked_candidate_counties("San Francisco County, CA") == [
            ("San Francisco County, CA", 1.0),
            ("San Banito County, CA", 0.8444444444444444),
            ("San Mateo County, CA", 0.7727272727272727),
        ]


def test_ranked_counties_excludes_low_matches():
    test_data = {
        "San Francisco County, CA": {},
        "San Mateo County, CA": {},
        "San Banito County, CA": {},
        "Fresno, CA": {},
    }

    with patch.dict(united_states_adjacency_data, test_data, clear=True):
        assert create_ranked_candidate_counties("San Francisco County, CA") == [
            ("San Francisco County, CA", 1.0),
            ("San Banito County, CA", 0.8444444444444444),
            ("San Mateo County, CA", 0.7727272727272727),
        ]


def test_can_get_similar_counties():
    test_data = {
        "San Francisco County, CA": {},
        "San Mateo County, CA": {},
        "San Banito County, CA": {},
        "Fresno, CA": {},
    }

    with patch.dict(united_states_adjacency_data, test_data, clear=True):
        assert find_similar_counties("San Francisco County, CA") == (
            "San Francisco County, CA",
            "San Banito County, CA",
            "San Mateo County, CA",
        )


def test_can_correct_county_name_errors_forgot_county():
    test_data = {
        "San Francisco County, CA": {},
        "San Mateo County, CA": {},
        "San Banito County, CA": {},
        "Fresno, CA": {},
    }

    with patch.dict(united_states_adjacency_data, test_data, clear=True):
        assert correct_county_name_errors("San Francisco, CA", False) == "San Francisco County, CA"


def test_can_correct_county_name_errors_best_match():
    test_data = {
        "San Francisco County, CA": {},
        "San Mateo County, CA": {},
        "San Banito County, CA": {},
        "Fresno, CA": {},
    }

    with patch.dict(united_states_adjacency_data, test_data, clear=True):
        assert correct_county_name_errors("Francisco, CA", True) == "San Francisco County, CA"


def test_can_correct_county_name_errors_fails_no_best_match():
    test_data = {
        "San Francisco County, CA": {},
        "San Mateo County, CA": {},
        "San Banito County, CA": {},
    }

    with patch.dict(united_states_adjacency_data, test_data, clear=True):
        with raises(NoSimilarCountiesError):
            correct_county_name_errors("Ventura County, CA", True)


def test_can_correct_county_name_errors_fails_skip_best_match():
    test_data = {
        "San Francisco County, CA": {},
        "San Mateo County, CA": {},
        "San Banito County, CA": {},
    }

    with patch.dict(united_states_adjacency_data, test_data, clear=True):
        with raises(NoSimilarCountiesError):
            correct_county_name_errors("Ventura County, CA", False)


def test_get_neighboring_counties_fails_if_error_correction_not_specified():
    test_data = {
        "San Francisco County, CA": {},
        "San Mateo County, CA": {},
        "San Banito County, CA": {},
    }

    with patch.dict(united_states_adjacency_data, test_data, clear=True):
        with raises(CountyNotFoundError):
            get_neighboring_areas("Ventura County, CA")


def test_get_neighboring_counties_fails_if_no_close_matches():
    test_data = {
        "San Francisco County, CA": {},
        "San Mateo County, CA": {},
        "San Banito County, CA": {},
    }

    with patch.dict(united_states_adjacency_data, test_data, clear=True):
        with raises(CountyNotFoundError):
            get_neighboring_areas(
                "Ventura County, CA",
                attempt_error_correction=True,
                use_best_match=True,
            )


def test_get_neighboring_counties_fails_but_suggests_similar_matches():
    test_data = {
        "San Francisco County, CA": {},
        "San Mateo County, CA": {},
        "San Banito County, CA": {},
    }

    with patch.dict(united_states_adjacency_data, test_data, clear=True):
        with raises(CountyNotFoundError) as e:
            get_neighboring_areas("San Francisco, CA", attempt_error_correction=False)

        assert e.value.similar == ("San Francisco County, CA",)


def test_get_neighboring_counties():
    neighbors = get_neighboring_areas("San Francisco County, CA")

    assert neighbors == (
        "Contra Costa County, CA",
        "Marin County, CA",
        "San Mateo County, CA",
    )


def test_get_neighboring_counties_forgot_county():
    neighbors = get_neighboring_areas("San Francisco, CA", attempt_error_correction=True, use_best_match=True)

    assert neighbors == (
        "Contra Costa County, CA",
        "Marin County, CA",
        "San Mateo County, CA",
    )


def test_get_neighboring_counties_best_match():
    neighbors = get_neighboring_areas("Francisco, CA", attempt_error_correction=True, use_best_match=True)

    assert neighbors == (
        "Contra Costa County, CA",
        "Marin County, CA",
        "San Mateo County, CA",
    )
