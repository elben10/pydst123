import re
from cerberus import Validator


def check_lang(lang):
    """Checks that language is correctly specified

    If lang is either `da` or `en` lang is returned else a ValueError is
    raised.

    Args:
        lang (:obj:`str`): `da` for danish or `en` for English.


    Returns:
        :obj:`str`: `lang`.

    Raises:
        :exc:`ValueError`: If `lang` is not `da` or `en`.

    """
    if not str_in_list(lang, ['da', 'en']):
        raise ValueError('`lang` is not `da` or `en`.')

    return lang


def str_in_list(astring, alist):
    """
    Checks if `astring` is contained in `alist`.

    Args:
        astring (:obj:`str`): a string
        alist (:obj:`list`): a list

    Returns:
        :obj:`bool`: True if astring is in alist else False

    """
    if astring in alist:
        return True

    return False


def check_list_regex(alist, regex):
    return all(check_regex(i, regex) for i in alist)


def check_regex(astring, regex):
    try:
        if re.search(regex, astring).group():
            return True
    except AttributeError:
        return False

def flatten_json(json):
    res = []
    for element in json:
        if not element['subjects']:
            del element['subjects']
            res.append(element)
        else:
            res.extend(flatten_json(element['subjects']))
    return res


def flatten_json_subjects(json):
    res = []
    for element in json:
        if not element['subjects']:
            del element['subjects']
            res.append(element)
        else:
            res.extend(flatten_json(element['subjects']))
    return res


def merge_dict(dict1, dict2):
    if dict1 and dict2:
        return {**dict1, **dict2}
    elif dict1:
        return dict1
    else:
        return dict2
