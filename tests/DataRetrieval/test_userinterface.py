import pytest
from pydst.DataRetrieval import userinterface
from requests import get


def test_lang_da_and_en_doesnt_return_error():
    assert userinterface.DST()._lang == "en"
    assert userinterface.DST(lang="da")._lang == "da"
    assert userinterface.DST(lang="en")._lang == "en"


def test_lang_es_raises_value_error():
    with pytest.raises(ValueError):
        userinterface.DST("es")


def test_get_subjects_unallowed_keyword_args_subjects_string():
    with pytest.raises(ValueError):
        userinterface.DST().get_subjects(subjects="a01")


def test_get_subjects_allowed_keyword_args_subjects_string():
    assert (
        type(userinterface.DST().get_subjects(subjects="01"))
        == userinterface.DSTSubjects
    )


def test_get_subjects_unallowed_keyword_args_subjects_list():
    with pytest.raises(ValueError):
        userinterface.DST().get_subjects(subjects=["a01"])


def test_get_subjects_allowed_keyword_args_subjects_list():
    assert (
        type(userinterface.DST().get_subjects(subjects=["01"]))
        == userinterface.DSTSubjects
    )


def test_get_subjects_unallowed_lang():
    with pytest.raises(ValueError):
        userinterface.DST().get_subjects(lang="es")


def test_get_subjects_unknown_keyword():
    with pytest.raises(ValueError):
        userinterface.DST().get_subjects(hejsa=2)


def test_get_subjects_responses_langs():
    assert (
        userinterface.DST().get_subjects()._response.content
        == get("http://api.statbank.dk/v1/subjects?lang=en").content
    )
    assert (
        userinterface.DST().get_subjects(lang="da")._response.content
        == get("http://api.statbank.dk/v1/subjects").content
    )
    assert (
        userinterface.DST(lang="da").get_subjects()._response.content
        == get("http://api.statbank.dk/v1/subjects").content
    )


def test_get_subjects_reponses_subjects():
    assert (
        userinterface.DST().get_subjects(subjects="02")._response.content
        == get("http://api.statbank.dk/v1/subjects/02?lang=en").content
    )
    assert (
        userinterface.DST().get_subjects(subjects=["02"])._response.content
        == get("http://api.statbank.dk/v1/subjects/02?lang=en").content
    )
    assert (
        userinterface.DST().get_subjects(subjects="02,05")._response.content
        == get("http://api.statbank.dk/v1/subjects/02,05?lang=en").content
    )
    assert (
        userinterface.DST().get_subjects(subjects=["02", "05"])._response.content
        == get("http://api.statbank.dk/v1/subjects/02,05?lang=en").content
    )


def test_get_tables_unallowed_lang():
    with pytest.raises(ValueError):
        userinterface.DST().get_tables(lang="es")


def test_get_tables_unallowed_keyword_args_subjects_string():
    with pytest.raises(ValueError):
        userinterface.DST().get_tables(subjects="a01")


def test_get_tables_unallowed_keyword_args_subjects_list():
    with pytest.raises(ValueError):
        userinterface.DST().get_tables(subjects=["a01"])


def test_get_tables_past_days_unallowed_pastdays():
    with pytest.raises(ValueError):
        userinterface.DST().get_tables(pastDays=None)

def test_get_tables_inactivetables():
    with pytest.raises(ValueError):
        userinterface.DST().get_tables(includeInactive='True1')

def test_get_tables_responses_langs():
    assert (
        userinterface.DST().get_tables()._response.content
        == get("http://api.statbank.dk/v1/tables?lang=en").content
    )
    assert (
        userinterface.DST().get_tables(lang="da")._response.content
        == get("http://api.statbank.dk/v1/tables").content
    )
    assert (
        userinterface.DST(lang="da").get_tables()._response.content
        == get("http://api.statbank.dk/v1/tables").content
    )

def test_get_tables_reponses_subjects():
    assert (
        userinterface.DST().get_tables(subjects="02")._response.content
        == get("http://api.statbank.dk/v1/tables?lang=en&subjects=02").content
    )
    assert (
        userinterface.DST().get_tables(subjects=["02"])._response.content
        == get("http://api.statbank.dk/v1/tables?lang=en&subjects=02").content
    )
    assert (
        userinterface.DST().get_tables(subjects="02,05")._response.content
        == get("http://api.statbank.dk/v1/tables?lang=en&subjects=02,05").content
    )
    assert (
        userinterface.DST().get_tables(subjects=["02", "05"])._response.content
        == get("http://api.statbank.dk/v1/tables?lang=en&subjects=02,05").content
    )
