import re


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
    if not str_in_list(lang, ["da", "en"]):
        raise ValueError("`lang` is not `da` or `en`.")

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
    """
    Checks if all strings in a list fulfills the specified regex

    Args:
        alist (:obj:`list` of :obj:`str`): a list
        regex (:obj:`str`): a regular expression

    Returns:
        :obj:`bool`: True if all strings in a list fulfills the regex else
            False.

    """
    return all(check_regex(i, regex) for i in alist)


def check_regex(astring, regex):
    """
    Checks if a string fulfills the specified regex

    Args:
        astring (:obj:`str`): a string
        regex (:obj:`str`): a regex

    Returns:
        :obj:`bool`: True if string fulfills regex else False.

    """
    try:
        if re.search(regex, astring).group():
            return True
    except AttributeError:
        return False


def flatten_json_list(json_list, recursive_element):
    """
    Merges lowest level structure.

    The ide

    Args:
        json_list (:obj:`list` of :obj:`dict`):
        recursive_element(:obj:`str`):

    Returns:
        :obj:`list`

    Todo:
        * Add documentation
        * Add introduction to example

    Examples:

        ...

        .. ipython::

            In [1]: from pydst.DataRetrieval.utils import flatten_json_list

            In [2]: json_list = [{
               ...:               'id': 1,
               ...:               'recursive': [
               ...:                             {'id': 12, 'recursive': []},
               ...:                             {'id': 13, 'recursive': []}
               ...:                            ]
               ...:             },
               ...:             {
               ...:              'id': 2,
               ...:              'recursive': []
               ...:             }]
               ...:

            In [3]: print(flatten_json_list(json_list, 'recursive'))
    """
    res = []
    for element in json_list:
        if not element[recursive_element]:
            del element[recursive_element]
            res.append(element)
        else:
            res.extend(
                flatten_json_list(element[recursive_element], recursive_element)
            )
    return res


def merge_dict(dict1=None, dict2=None):
    """
    Merges the two dictionaries

    If dict2 is empty dict1 is returned.
    If dict1 is empty dict2 is returned.
    If dict1 and dict2 is non-empty they are merged.

    Args:
        dict1 (:obj:`dict`): a dictionary
        dict2 (:obj:`dict`): another dictionary

    Returns:
        :obj:`dict`: A merged dictionary

    """
    if dict1 and dict2:
        return {**dict1, **dict2}
    elif dict1:
        return dict1
    elif dict2:
        return dict2
    else:
        return {}


# def js_boolstring_only_true(x):
#     """
#     Returns 'true' if x is True else return None
#
#     Args:
#         x (:obj:`bool`):
#
#     Returns:
#
#     """
#     if x is True:
#         return bool_to_js_boolstring(x)
#     else:
#         return ""
#
#
# def bool_to_js_boolstring(x):
#     """
#     Changes boolean values to js booleans as strings
#
#     Args:
#         x (:obj:`bool`): A boolean value
#
#     Returns:
#         :obj:`string`: Returns 'true' if x is true else 'false'
#
#     """
#     if x is True:
#         return 'true'
#     else:
#         return 'false'
