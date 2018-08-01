from collections import OrderedDict
from cerberus import Validator


class ExtendedValidator(Validator):
    def __init__(self, *args, **kwargs):
        self._lang = kwargs['lang']
        super(ExtendedValidator, self).__init__(*args, **kwargs)

    def _normalize_coerce_join_list(self, value):
        if isinstance(value, list):
            return ','.join(value)
        else:
            return value

    def _normalize_coerce_bool_to_str(self, value):
        if isinstance(value, bool):
            return str(value).lower()
        else:
            return value

    def _normalize_coerce_lang(self, value):
        if value == 'da':
            return None
        else:
            return value

    def _normalize_default_setter_lang(self, document):
        if self._lang == 'da':
            return None
        else:
            return 'en'


def lang_rules():
    return {
        'type': 'string',
        'regex': '^(en)$',
        'default_setter': 'lang',
        'nullable': True,
        'coerce': 'lang'
    }



validation_schema = {
    'subjects': {
        'path_args': {
            'type': 'dict',
            'schema': {
                'subjects': {
                    'type': 'string',
                    'coerce': 'join_list',
                }
            }
        },
        'query_args': {
            'type': 'dict',
            'schema': {
                'lang': lang_rules(),
                'omitSubjectsWithoutTables': {
                    'type': 'string',
                    'regex': r'^true$',
                    'coerce': 'bool_to_str'
                }
            }
        },
    },
    'tables': {
        'path_args': {
            'type': 'dict',
            'schema': {

            }
        },
        'query_args': {
            'type': 'dict',
            'schema': {
                'includeInactive': {
                    'type': 'string',
                    'regex': r'^true$',
                    'coerce': 'bool_to_str'
                },
                'lang': lang_rules(),
                'pastDays': {
                    'type': 'string',
                    'regex': r'^[1-9][0-9]+$',
                    'coerce': str,
                },
                'subjects': {
                    'type': 'string',
                    'regex': r'^([0-9]+,)*[0-9]+$',
                    'coerce': 'join_list',
                }
            }
        }
    },
    'tableinfo': {
        'path_args': {
            'type': 'dict',
            'schema': {
                'table_id': {
                    'type': 'string',
                    'regex': r'^[A-Z][A-Z0-9]+$',
                    'required': True,
                }
            }
        },
        'query_args': {
            'type': 'dict',
            'schema': {
                'lang': lang_rules()
            }
        }
    },
    'data': {
        'path_args': {
            'type': 'dict',
            'schema': {
                'table_id': {
                    'type': 'string',
                    'regex': r'^[A-Z][A-Z0-9]+$',
                    'required': True,
                },
                'format': {
                    'type': 'string',
                    'regex': r'^(CSV|BULK)$',
                    'default': 'CSV',
                }
            }
        },
        'query_args': {
            'type': 'dict',
            'schema': {
                'lang': lang_rules(),
                'valuePresentation': {
                    'type': 'string',
                    'regex': r'^(Default|Code|Value|CodeAndValue)$'
                },
                'timeOrder': {
                    'type': 'string',
                    'regex': r'^(Ascending|Descending)$',
                    'default': None,
                    'nullable': True
                }
            }
        }
    }
}
