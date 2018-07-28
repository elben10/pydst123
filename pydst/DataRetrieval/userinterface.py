from pandas import DataFrame, read_csv, Series
from pydst.Connection.request import dst_request
from . import utils
from cerberus import Validator
from io import StringIO


class DST(object):
    """Provides a simple API for interacting with Statistics Denmark.

    Args:
        lang (:obj:`str`, optional): decides languages. Can be `en` for english
            (default) or `da` for danish.

    Raises:
        :exc:`ValueError`: If lang is not `da` or `en`.

    """

    def __init__(self, lang="en"):
        self._lang = utils.check_lang(lang)

    def get_subjects(self, **kwargs):
        """
        ONE LINER

        Args:
            lang (:obj:`str`, optional):
            omitSubjectsWithoutTables (:obj:`bool` or :obj:`string`, optional)
            subjects (:obj:`str` or :obj:`list` of :obj:`str`, optional):

        Returns:

        Example:
            ...

            .. ipython::

                In [1]: from pydst import DST

                In [2]: from pandas import set_option

                In [3]: set_option('display.max_rows', 4)

                In [4]: DST().get_subjects()

                In [5]: import os

                In [6]: os.getcwd()

                !pwd # under linux/mac

                In [7]: %run ./examples/dst_get_subjects.py -i






        Todo:
            * Add documentation
            * Add examples

        """
        schema = {
            "kwargs": {
                "type": "dict",
                "schema": {
                    "lang": {
                        "type": "string",
                        "regex": "^(da|en)$",
                        "empty": False,
                    },
                    "omitSubjectsWithoutTables": {
                        "nullable": True,
                        "type": "string",
                        "regex": r"^true$",
                        "empty": False,
                    },
                    "subjects": {
                        "nullable": True,
                        "anyof": [
                            {
                                "type": "string",
                                "regex": r"^([0-9]+,)*[0-9]+$",
                                "empty": False,
                            },
                            {
                                "type": "list",
                                "schema": {
                                    "type": "string",
                                    "regex": r"^[0-9]+$",
                                    "empty": False,
                                },
                            },
                        ],
                    },
                },
            }
        }

        document = {"kwargs": kwargs}

        V = Validator(schema)
        if not V.validate(document):
            raise ValueError(V.errors)

        if kwargs.get("lang") == "da":
            kwargs["lang"] = None

        elif kwargs.get("lang") is None and self._lang == "da":
            kwargs["lang"] = None

        else:
            kwargs["lang"] = "en"

        subj_str = "subjects/"

        if isinstance(kwargs.get("subjects"), str):
            subj_str += kwargs["subjects"]
            del kwargs["subjects"]
        elif isinstance(kwargs.get("subjects"), list):
            subj_str += ",".join(kwargs["subjects"])
            del kwargs["subjects"]

        r = dst_request(subj_str, kwargs)
        return DSTSubjects(r)

    def get_tables(self, **kwargs):
        """
        Todo:
            * Add documentation
            * Add examples
            * Add test
        """
        schema = {
            "kwargs": {
                "type": "dict",
                "schema": {
                    "lang": {"type": "string", "regex": r"^(da|en)$"},
                    "subjects": {
                        "nullable": True,
                        "anyof": [
                            {
                                "nullable": True,
                                "type": "string",
                                "regex": r"^([0-9]+,)*[0-9]+$",
                                "empty": False,
                            },
                            {
                                "type": "list",
                                "schema": {
                                    "type": "string",
                                    "regex": r"^[0-9]+$",
                                    "empty": False,
                                },
                            },
                        ],
                    },
                    "pastDays": {
                        "anyof": [
                            {"nullable": True, "type": "integer", "min": 0},
                            {"type": "string", "regex": r"^[1-9][0-9]*$"},
                        ]
                    },
                    "includeInactive": {
                        "type": "string",
                        "regex": "^[Tt]rue$",
                        "empty": False,
                        "coerce": str
                        # "coerce": (bool, utils.js_boolstring_only_true)
                        #  Seems to be a bug in Cerberus
                    },
                },
            }
        }

        document = {"kwargs": kwargs}

        V = Validator(schema)
        if not V.validate(document):
            raise ValueError(V.errors)

        if kwargs.get("lang") == "da":
            kwargs["lang"] = None

        elif kwargs.get("lang") is None and self._lang == "da":
            kwargs["lang"] = None

        else:
            kwargs["lang"] = "en"

        if isinstance(kwargs.get("subjects"), list):
            kwargs["subjects"] = ",".join(kwargs["subjects"])

        r = dst_request("tables", kwargs)
        return DSTTables(r)

    def get_tableinfo(self, table_id, **kwargs):
        """
        Todo:
            * Add documentation
            * Add examples
            * Add test
        """
        schema = {
            "table_id": {"type": "string", "regex": r"^[A-Z][A-Z0-9]+$"},
            "kwargs": {
                "type": "dict",
                "schema": {"lang": {"type": "string", "regex": r"^(da|en)$"}},
            },
        }

        document = {"table_id": table_id, "kwargs": kwargs}

        V = Validator(schema)
        if not V.validate(document):
            raise ValueError(V.errors)

        if kwargs.get("lang") == "da":
            kwargs["lang"] = None

        elif kwargs.get("lang") is None and self._lang == "da":
            kwargs["lang"] = None

        else:
            kwargs["lang"] = "en"

        r = dst_request("tableinfo/{}".format(table_id), kwargs)
        return DSTTableinfo(r)

    def get_data(self, table_id, stream=False, **kwargs):
        """
        Todo:
            * Add documentation
            * Add examples
            * Add test
        """
        schema = {
            "table_id": {"type": "string", "regex": r"^[A-Z][A-Z0-9]+$"},
            "stream": {"type": "boolean"},
            "kwargs": {
                "type": "dict",
                "allow_unknown": {
                    "type": "string",
                    "regex": r"^[A-Åa-å0-9*]+$",
                },
                "schema": {
                    "lang": {"type": "string", "regex": r"^(da|en)$"},
                    "valuePresentation": {
                        "type": "string",
                        "regex": "^(Default|Code|Value|CodeAndValue)$",
                        "nullable": True,
                    },
                },
            },
        }

        document = {"table_id": table_id, "kwargs": kwargs}

        V = Validator(schema)
        if not V.validate(document):
            raise ValueError(V.errors)

        if kwargs.get("lang") == "da":
            kwargs["lang"] = None

        elif kwargs.get("lang") is None and self._lang == "da":
            kwargs["lang"] = None

        else:
            kwargs["lang"] = "en"

        if stream:
            r = dst_request("data/{}/BULK".format(table_id), kwargs)
        else:
            r = dst_request("data/{}/CSV".format(table_id), kwargs)

        return DSTData(r)

    def get_csv(self, table_id, **kwargs):
        """
        Todo:
            * Add documentation
            * Add examples
            * Add test
        """
        pass


class DSTSubjects(DataFrame):
    """
    Todo:
        * Add documentation
        * Add examples
        * Add test
    """

    _metadata = ["_response"]

    def __init__(self, response):
        super(DSTSubjects, self).__init__(
            DataFrame(utils.flatten_json_list(response.json(), "subjects"))
        )
        self._response = response


class DSTTables(DataFrame):
    """
    Todo:
        * Add documentation
        * Add examples
        * Add test
    """

    _metadata = ["_response"]

    def __init__(self, response):
        super(DSTTables, self).__init__(DataFrame(response.json()))
        self._response = response


class DSTData(DataFrame):
    """
    Todo:
        * Add documentation
        * Add examples
        * Add test
    """

    _metadata = ["_response"]

    def __init__(self, response):
        super(DSTData, self).__init__(
            read_csv(StringIO(response.text), sep=";")
        )
        self._response = response


class DSTTableinfo(object):
    """ """

    def __init__(self, response):
        self._reponse = response

    def info_general(self):
        """ """
        json = self._reponse.json()
        keys = [
            "id",
            "text",
            "description",
            "unit",
            "suppressedDataValue",
            "updated",
            "active",
            "footnote",
        ]
        return Series({k: json[k] for k in keys})

    def info_contact(self):
        """
        Todo:
            * Add documentation
            * Add examples
            * Add test
        """
        json = self._reponse.json()
        return [Series(i) for i in json["contacts"]]

    def info_docs(self):
        """
        Todo:
            * Add documentation
            * Add examples
            * Add test
        """
        json = self._reponse.json()
        return Series(json["documentation"])

    def get_variables(self):
        """
        Todo:
            * Add documentation
            * Add examples
            * Add test
        """
        json = self._reponse.json()
        return DataFrame(
            [
                {k: v for k, v in i.items() if not k == "values"}
                for i in json["variables"]
            ]
        )

    def get_variable_values(self, variable):
        """
        Todo:
            * Add documentation
            * Add examples
            * Add test
        """
        json = self._reponse.json()
        allowed_vars = [
            v for i in json["variables"] for k, v in i.items() if k == "id"
        ]
        schema = {
            "variable": {
                "type": "string",
                "regex": r"^({})$".format("|".join(allowed_vars)),
            }
        }

        document = {"variable": variable}

        V = Validator(schema, all)
        if not V.validate(document):
            raise ValueError(V.errors)

        return DataFrame(
            json["variables"][allowed_vars.index(variable)]["values"]
        )
