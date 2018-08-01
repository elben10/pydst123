# -*- coding: utf-8 -*-
"""Top-level package for Pydst."""

from .DataRetrieval.userinterface import DST

from . import Connection
from . import Cli
from . import DataRetrieval
from subprocess import Popen as _Popen, PIPE as _PIPE


def _git_version():
    process = _Popen(["git", "describe"], stdout=_PIPE)
    out, _ = process.communicate()
    return ".".join(out.decode("utf-8").split("-", 1)[0][1:].split(".")[:3])


__author__ = """Jakob Jul Elben, Kristian Urup Larsen"""
__email__ = "elbenjakobjul@gmail.com, kristianuruplarsen@gmail.com"
__version__ = _git_version()
