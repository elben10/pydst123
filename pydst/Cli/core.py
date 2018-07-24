# -*- coding: utf-8 -*-

"""Console script for pydst."""
import click
from pydst import DST
from cerberus import Validator
from __future__ import print_function


@click.group()
def main():
    pass


@main.command(short_help='Retrieve subjects from Statistics Denmark')
@click.option('-s', '--subjects', default=None, help='comma separated list of subjects.')
@click.option('-l', '--lang', default='en', help='`da` for danish or `en` for english')
@click.option('-o', '--omitsubjectswithouttables', default=None)
def subjects(subjects, lang, omitsubjectswithouttables):
    res = DST().get_subjects(subjects=subjects,
                                   lang=lang,
                                   omitSubjectsWithoutTables=omitsubjectswithouttables)
    print(res.to_string(index=False))
    return 0


@main.command(short_help='Retrieve information about tables at Statistics Denmark')
@click.option('-s', '--subjects', default=None, help='comma separated list of subjects.')
@click.option('-l', '--lang', default='en', help='`da` for danish or `en` for english')
@click.option('-p', '--pastdays', default=None, type=int)
@click.option('-i', '--includeinactive', default=None)
def tables(subjects, lang, pastdays, includeinactive):
    res = DST().get_tables(subjects=subjects,
                                    lang=lang,
                                    pastDays=pastdays,get https://www.python.org/ftp/python/3.5.0/Python-3.5.0.tgz
                                    includeInactive=includeinactive)
    print(res)
    return 0


@main.group(short_help='Retrieve metadata for the specified table_id from Statistics Denmark')
def tableinfo():
    pass


@tableinfo.command()
@click.argument('table_id', required=1)
@click.option('-l', '--lang', default='en', help='`da` for danish or `en` for english')
def info_general(table_id, lang):
    res = DST().get_tableinfo(table_id, lang=lang).info_general()
    print(res)


@tableinfo.command()
@click.argument('table_id', required=1)
@click.option('-l', '--lang', default='en', help='`da` for danish or `en` for english')
def info_contact(table_id, lang):
    res = DST().get_tableinfo(table_id, lang=lang).info_contact()
    print(res)


@tableinfo.command()
@click.argument('table_id', required=1)
@click.option('-l', '--lang', default='en', help='`da` for danish or `en` for english')
def info_docs(table_id, lang):
    res = DST().get_tableinfo(table_id, lang=lang).info_docs()
    print(res)


@tableinfo.command()
@click.argument('table_id', required=1)
@click.option('-l', '--lang', default='en', help='`da` for danish or `en` for english')
def variables(table_id, lang):
    res = DST().get_tableinfo(table_id, lang=lang).get_variables()
    print(res)

@tableinfo.command()
@click.argument('table_id', required=1)
@click.argument('variable', required=1)
@click.option('-l', '--lang', default='en', help='`da` for danish or `en` for english')
def variable_values(table_id, variable, lang):
    res = DST().get_tableinfo(table_id, lang=lang).get_variable_values(variable)
    print(res)


@main.command(short_help='Retrieve table data for the specified table_id from Statistics Denmark',
              context_settings={'allow_extra_args': True})
@click.argument('table_id', required=1)
@click.argument('vars', nargs=-1, type=click.UNPROCESSED, metavar='[VARS_1 ... VARS_N]')
@click.option('-l', '--lang', default='en', help='`da` for danish or `en` for english')
@click.option('-v', '--valuepresentation', default='Default')
@click.option('--stream', default=False, help='Add it', type=bool)
def data(table_id, stream, vars, lang, valuepresentation):
    """hejsaasfasj

    TODO:
        * hejsa

    """
    schema = {
        'vars': {
            'type': 'list',
            'schema': {
                'type': 'string',
                'regex': r'^[A-Åa-å0-9*]+=[A-Åa-å0-9*]+$'
            }
        }
    }

    document = {
        'vars': list(vars)
    }

    V = Validator(schema)
    if not V.validate(document):
        raise ValueError(V.errors)
    if vars:
        args = {i.split('=', 1)[0]: i.split('=', 1)[1] for i in vars}
    else:
        args = {}
    res = DST().get_data(table_id=table_id,
                         stream=stream,
                         lang=lang,
                         valuePresentation=valuepresentation,
                         **args)
    print(res)
    return 0


@main.command(short_help='Retrieve table data for the specified table_id from Statistics Denmark as CSV-file.')
def csv():
    pass

