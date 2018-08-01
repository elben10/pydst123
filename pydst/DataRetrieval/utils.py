def split_kwargs(kwargs, validation_rules):
    path_kwargs_keys = validation_rules["path_args"]["schema"].keys()
    path_args = {k: v for k, v in kwargs.items() if k in path_kwargs_keys}
    query_args = {k: v for k, v in kwargs.items() if k not in path_kwargs_keys}

    return path_args, query_args


def path_query_constructor(app, norm_doc):
    path = app + "/" + "/".join(norm_doc["path_args"].values())
    query = norm_doc["query_args"]
    return path, query


def flatten_json_list(json_list, recursive_element):
    """
    Merges lowest level structure.

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
                flatten_json_list(element[recursive_element],
                                  recursive_element)
            )
    return res
