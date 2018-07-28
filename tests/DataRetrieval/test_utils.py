import pytest
from pydst.DataRetrieval import utils
from copy import copy


def test_that_da_or_en_returns_da_or_en():
    """Checks that da and en is returned respectively"""
    assert utils.check_lang("da") == "da"
    assert utils.check_lang("en") == "en"


def test_that_valueerror_is_raised_if_not_da_or_en():
    """Checks that an ValueError is raised if lang is not da or en"""
    with pytest.raises(ValueError):
        utils.check_lang("es")


def test_all_strings_in_list_corresponds_with_regex():
    """Checks that all strings in a list fulfill regex"""
    assert utils.check_list_regex(["hej", "ha", "h"], r"^h") is True


def test_all_strings_in_list_doesnt_corresponds_with_regex():
    """Checks that all strings in a list doesnt fulfill regex"""
    assert utils.check_list_regex(["hej", "ha", "h"], r"h$") is not True


def test_string_fulfill_regex():
    """Checks that string fulfills regex"""
    assert utils.check_regex("hej", r"^hej$") is True


def test_string_doesnt_fulfill_regex():
    """Checks that string doesnt fulfill regex"""
    assert utils.check_regex("hej", r"^hejsa$") is not True


def test_flattens_json_subjects_removes_empty_subjects():
    original = [
        {
            "id": "02",
            "description": "Befolkning og valg",
            "active": True,
            "hasSubjects": True,
            "subjects": [],
        },
        {
            "id": "03",
            "description": "Uddannelse og viden",
            "active": True,
            "hasSubjects": True,
            "subjects": [],
        },
    ]

    res = [
        {
            "id": "02",
            "description": "Befolkning og valg",
            "active": True,
            "hasSubjects": True,
        },
        {
            "id": "03",
            "description": "Uddannelse og viden",
            "active": True,
            "hasSubjects": True,
        },
    ]

    assert utils.flatten_json_list(original, "subjects") == res


def test_flattens_json_subjects_flattens_nonempty_subjects():
    original = [
        {
            "id": "02",
            "description": "Befolkning og valg",
            "active": True,
            "hasSubjects": True,
            "subjects": [
                {
                    "id": "03",
                    "description": "Uddannelse og viden",
                    "active": True,
                    "hasSubjects": True,
                    "subjects": [],
                }
            ],
        }
    ]

    res = [
        {
            "id": "03",
            "description": "Uddannelse og viden",
            "active": True,
            "hasSubjects": True,
        }
    ]

    assert utils.flatten_json_list(original, "subjects") == res


def test_merge_dict():
    assert utils.merge_dict({"hej": 2}, {"hejsa": 3}) == {"hej": 2, "hejsa": 3}
    assert utils.merge_dict({"hej": 2}, {}) == {"hej": 2}
    assert utils.merge_dict({}, {"hejsa": 3}) == {"hejsa": 3}
    assert utils.merge_dict({}, {}) == {}

#
# def test_js_boolstring_only_true():
#     assert utils.js_boolstring_only_true(True) is 'true'
#     assert utils.js_boolstring_only_true(False) is None
#
# def test_bool_to_js_boolstring():
#     assert utils.bool_to_js_boolstring(True) is 'true'
#     assert utils.bool_to_js_boolstring(False) is 'false'
