from . import utils
from . import validation
from pydst.Connection.request import dst_request

from cerberus import Validator
from io import StringIO
from pandas import DataFrame, read_csv, Series


class DST(object):
    """Provides a simple API for interacting with Statistics Denmark.

    Args:
        lang (:obj:`str`, optional): decides languages. Can be `en` for english
            (default) or `da` for danish.
    Raises:
        :exc:`ValueError`: If lang is not `da` or `en`.
    """

    def __init__(self, lang="en"):
        self._lang = lang

    def subjects(self, **kwargs):
        """
        Retrieve table subjects from Statistics Denmark


        Kwargs:
            subjects (:obj:`bool`): hejsa

        Returns:

        """
        schema = validation.validation_schema["subjects"]
        path_args, query_args = utils.split_kwargs(kwargs, schema)
        document = {"path_args": path_args, "query_args": query_args}

        v = validation.ExtendedValidator(schema, lang=self._lang)

        if v.validate(document) is False:
            raise ValueError(v.errors)

        normalized_document = v.normalized(document)
        path, query = utils.path_query_constructor(
            "subjects", normalized_document
        )

        r = dst_request(path, query)
        return RequestDataFrame(r)

    def tables(self, **kwargs):
        schema = validation.validation_schema["tables"]
        path_args, query_args = utils.split_kwargs(kwargs, schema)
        document = {"path_args": path_args, "query_args": query_args}

        v = validation.ExtendedValidator(schema, lang=self._lang)

        if v.validate(document) is False:
            raise ValueError(v.errors)

        normalized_document = v.normalized(document)
        path, query = utils.path_query_constructor(
            "tables", normalized_document
        )

        r = dst_request(path, query)
        return RequestDataFrame(r)

    def tableinfo(self, table_id, **kwargs):
        schema = validation.validation_schema["tableinfo"]
        path_args, query_args = utils.split_kwargs(kwargs, schema)
        document = {
            "path_args": {"table_id": table_id, **path_args},
            "query_args": query_args,
        }

        v = validation.ExtendedValidator(
            schema, lang=self._lang, allow_unknown={"type": "string"}
        )

        if v.validate(document) is False:
            raise ValueError(v.errors)

        normalized_document = v.normalized(document)
        path, query = utils.path_query_constructor(
            "tableinfo", normalized_document
        )

        r = dst_request(path, query)
        return Tableinfo(r)

    def data(self, table_id, **kwargs):
        schema = validation.validation_schema["data"]
        path_args, query_args = utils.split_kwargs(kwargs, schema)
        document = {
            "path_args": {"table_id": table_id, **path_args},
            "query_args": query_args,
        }

        v = validation.ExtendedValidator(
            schema, lang=self._lang, allow_unknown={"type": "string"}
        )

        if v.validate(document) is False:
            raise ValueError(v.errors)

        normalized_document = v.normalized(document)
        path, query = utils.path_query_constructor("data", normalized_document)

        r = dst_request(path, query)
        return RequestDataFrame(r)


class RequestDataFrame(DataFrame):
    _metadata = ["_response"]

    def __init__(self, response):
        if response.url.startswith("http://api.statbank.dk/v1/subjects"):
            super(RequestDataFrame, self).__init__(
                DataFrame(utils.flatten_json_list(response.json(), "subjects"))
            )
        elif response.url.startswith("http://api.statbank.dk/v1/tables"):
            super(RequestDataFrame, self).__init__(DataFrame(response.json()))
        elif response.url.startswith("http://api.statbank.dk/v1/data"):
            super(RequestDataFrame, self).__init__(
                read_csv(StringIO(response.text), sep=";")
            )
        self._response = response


class Tableinfo(object):
    """ """

    def __init__(self, response):
        self._reponse = response

    def __repr__(self):
        return repr(self.info_general())

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

    def info_variables(self):
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

    def info_variable_values(self, variable):
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

        v = Validator(schema)
        if not v.validate(document):
            raise ValueError(v.errors)

        return DataFrame(
            json["variables"][allowed_vars.index(variable)]["values"]
        )

