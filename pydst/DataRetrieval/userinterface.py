# -*- coding: utf-8 -*-

from pandas import DataFrame, read_csv, Series
from pydst.Connection.request import dst_request
from pydst.DataRetrievals import utils
from cerberus import Validator
from requests.compat import is_py2

if is_py2:  # pragma: no cover
    from StringIO import StringIOe  # pragma: no cover
else:  # pragma: no cover
    from io import StringIO  # pragma: no cover


class DST(object):
    def __init__(self, lang='en'):
        self._lang = utils.check_lang(lang)

    def get_subjects(self, **kwargs):
        schema = {
            'kwargs': {
                'type': 'dict',
                'schema': {
                    'subjects': {
                        'nullable': True,
                        'anyof': [
                            {
                                'type': 'string',
                                'regex': r'^([0-9]+,)*[0-9]+$',
                                'nullable': True,
                            },
                            {
                                'type': 'list',
                                'schema': {
                                    'type': 'string',
                                    'regex': r'^[0-9]+$',
                                }
                            }
                        ]
                    },
                    'lang': {
                        'type': 'string',
                        'regex': '^(da|en)$',
                    },
                    'omitSubjectsWithoutTables': {
                        'nullable': True,
                        'type': 'string',
                        'regex': r'^true$'
                    }
                }
            }
        }

        document = {
            'kwargs': kwargs,
        }

        V = Validator(schema)
        if not V.validate(document):
            raise ValueError(V.errors)

        if kwargs.get('lang') == 'da':
            kwargs['lang'] = None

        elif kwargs.get('lang') is None and self._lang == 'da':
            kwargs['lang'] = None

        else:
            kwargs['lang'] = 'en'

        subj_str = 'subjects/'

        if isinstance(kwargs.get('subjects'), str):
            subj_str += kwargs['subjects']
            del kwargs['subjects']
        elif isinstance(kwargs.get('subjects'), list):
            subj_str += ','.join(kwargs['subjects'])
            del kwargs['subjects']

        r = dst_request(subj_str, kwargs)
        return DSTSubjects(r)

    def get_tables(self, **kwargs):
        schema = {
            'kwargs': {
                'type': 'dict',
                'schema': {
                    'lang': {
                        'type': 'string',
                        'regex': r'^(da|en)$',
                    },
                    'subjects': {
                        'nullable': True,
                        'anyof': [
                            {
                                'nullable': True,
                                'type': 'string',
                                'regex': r'^([0-9]+,)*[0-9]+$'
                            },
                            {
                                'type': 'list',
                                'schema': {
                                    'type': 'string',
                                    'regex': r'^[0-9]+$'
                                }
                            },
                        ]
                    },
                    'pastDays': {
                        'nullable': True,
                        'anyof': [
                            {
                                'nullable': True,
                                'type': 'integer',
                                'min': 0
                            },
                            {
                                'type': 'string',
                                'regex': r'^[1-9][0-9]*$'
                            }
                        ]
                    },
                    'includeInactive': {
                        'type': 'string',
                        'regex': r'^true$',
                        'nullable': True
                    }

                }
            }
        }

        document = {
            'kwargs': kwargs
        }

        V = Validator(schema)
        if not V.validate(document):
            raise ValueError(V.errors)

        if kwargs.get('lang') == 'da':
            kwargs['lang'] = None

        elif kwargs.get('lang') is None and self._lang == 'da':
            kwargs['lang'] = None

        else:
            kwargs['lang'] = 'en'

        if isinstance(kwargs.get('subjects'), list):
            kwargs['subjects'] = ','.join(kwargs['subjects'])

        r = dst_request('tables', kwargs)
        return DSTTables(r, )

    def get_tableinfo(self, table_id, **kwargs):
        schema = {
            'table_id': {
                'type': 'string',
                'regex': r'^[A-Z][A-Z0-9]+$',
            },
            'kwargs': {
                'type': 'dict',
                'schema': {
                    'lang': {
                        'type': 'string',
                        'regex': r'^(da|en)$',
                    }
                }
            }
        }

        document = {
            'table_id': table_id,
            'kwargs': kwargs
        }

        V = Validator(schema)
        if not V.validate(document):
            raise ValueError(V.errors)

        if kwargs.get('lang') == 'da':
            kwargs['lang'] = None

        elif kwargs.get('lang') is None and self._lang == 'da':
            kwargs['lang'] = None

        else:
            kwargs['lang'] = 'en'

        r = dst_request('tableinfo/{}'.format(table_id), kwargs)
        return DSTTableinfo(r)

    def get_data(self, table_id, stream=False, **kwargs):
        schema = {
            'table_id': {
                'type': 'string',
                'regex': r'^[A-Z][A-Z0-9]+$',
            },
            'stream': {
                'type': 'boolean'
            },
            'kwargs': {
                'type': 'dict',
                'allow_unknown': {
                    'type': 'string',
                    'regex': r'^[A-Åa-å0-9*]+$'
                },
                'schema': {
                    'lang': {
                        'type': 'string',
                        'regex': r'^(da|en)$',
                    },
                    'valuePresentation': {
                        'type': 'string',
                        'regex': '^(Default|Code|Value|CodeAndValue)$',
                        'nullable': True
                    },
                }
            }
        }

        document = {
            'table_id': table_id,
            'kwargs': kwargs,
        }

        V = Validator(schema)
        if not V.validate(document):
            raise ValueError(V.errors)

        if kwargs.get('lang') == 'da':
            kwargs['lang'] = None

        elif kwargs.get('lang') is None and self._lang == 'da':
            kwargs['lang'] = None

        else:
            kwargs['lang'] = 'en'

        if stream:
            r = dst_request('data/{}/BULK'.format(table_id), kwargs)
        else:
            r = dst_request('data/{}/CSV'.format(table_id), kwargs)

        return DSTData(r)

    def get_csv(self, table_id, **kwargs):
        pass


class DSTSubjects(DataFrame):

    _metadata = ['_response']

    def __init__(self, response):
        super(DSTSubjects, self)\
            .__init__(DataFrame(utils.flatten_json_subjects(response.json())))
        self._response = response


class DSTTables(DataFrame):

    _metadata = ['_response']

    def __init__(self, response):
        super(DSTTables, self)\
            .__init__(DataFrame(response.json()))
        self._response = response


class DSTData(DataFrame):
    _metadata = ['_response']

    def __init__(self, response):
        super(DSTData, self) \
            .__init__(read_csv(StringIO(response.text), sep=';'))
        self._response = response


class DSTTableinfo(object):
    def __init__(self, response):
        self._reponse = response

    def info_general(self):
        json = self._reponse.json()
        keys = ['id', 'text', 'description', 'unit', 'suppressedDataValue', 'updated', 'active', 'footnote']
        return Series({k: json[k] for k in keys})

    def info_contact(self):
        json = self._reponse.json()
        return [Series(i) for i in json['contacts']]

    def info_docs(self):
        json = self._reponse.json()
        return Series(json['documentation'])

    def get_variables(self):
        json = self._reponse.json()
        return DataFrame([{k: v for k, v in i.items() if not k == 'values'} for i in json['variables']])

    def get_variable_values(self, variable):
        json = self._reponse.json()
        allowed_vars = [v for i in json['variables'] for k, v in i.items() if k == 'id']
        schema = {
            'variable': {
                'type': 'string',
                'regex': r'^({})$'.format('|'.join(allowed_vars))
            }
        }

        document = {
            'variable': variable
        }

        V = Validator(schema, all)
        if not V.validate(document):
            raise ValueError(V.errors)

        return DataFrame(json['variables'][allowed_vars.index(variable)]['values'])


