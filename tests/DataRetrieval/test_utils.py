#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pydst` package."""

import pytest
from pydst import DataRetrieval


def test_lang_is_returned_if_da_or_en():
    """"
    Checks that lang is returned if lang is
    `da` or `en` in check_lang.
    """
    assert DataRetrieval.utils.check_lang('da') == 'da'
    assert DataRetrieval.utils.check_lang('en') == 'en'


def test_lang_raises_ValueError_if_not_da_or_en():
    """
    Checks that check_lang raises ValueError if lang
    is not `da` or `en`.
    """
    with pytest.raises(ValueError):
        DataRetrieval.utils.check_lang('es')


def test_str_in_list_returns_True():
    assert DataRetrieval.utils.str_in_list('da', ['da']) is True

def test_str_not_in_list_returns_False():
    assert DataRetrieval.utils.str_in_list('da', ['en']) is False



