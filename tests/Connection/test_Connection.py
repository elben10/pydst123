#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pydst` package."""

import pytest
from pydst import Connection
from requests.api import get
from requests.models import Response


def test_check_if_dst_message():
    """Checks if Statistics Denmark Error is present."""
    r_true = get("http://api.statbank.dk/v1/subjects/agsaffø/")
    r_false = get("http://api.statbank.dk/v1/subjects/")
    assert Connection.request.dst_error(r_true)
    assert not Connection.request.dst_error(r_false)


def test_HTTPError_if_error_message():
    with pytest.raises(Connection.request.HTTPError):
        Connection.request.dst_request("123")


def test_requests_response_if_no_error_message():
    assert type(Connection.request.dst_request("subjects")) is Response
