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
