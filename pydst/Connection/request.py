from requests.api import get
from requests.exceptions import HTTPError

from urllib.parse import urljoin, urlparse, urlunparse  # pragma: no cover


def dst_request(path, params=None):
    """Send get request to Statistics Denmark.

    Sends a get request to Statistics Denmark. Raises an HTTPError
        if an error message from Statistics Denmark is present.
        Otherwise a :class:`Response<requests:requests.Response>` is returned.

    Args:
        path (:obj:`str`): The path is added as the path to the base url.

        params (:obj:`dict`): The params is added as the query to the base url.
    """
    parsed = urlparse("http://api.statbank.dk/v1/")
    url = urlunparse(
        [
            parsed.scheme,
            parsed.hostname,
            urljoin(parsed.path, path),
            parsed.params,
            parsed.query,
            parsed.fragment,
        ]
    )
    r = get(url, params)

    if dst_error(r):
        http_error_msg = u"%s Client Error: %s for url: %s" % (
            r.status_code,
            r.reason,
            r.url,
        )
        http_error_msg += u"\nError message from Statistics Denmark: \n\t> %s"\
                          % r.json().get("message", "No error message.")
        raise HTTPError(http_error_msg, response=r)

    return r


def dst_error(response):
    """Checks if an error is reported from Statistics Denmark.

    Args:
        response (:class:`Response<requests:requests.Response>`):
            A HTTP reponse from requests.

    """
    key_list = list(response.headers.keys())
    if [i for i in key_list if i.startswith("StatbankAPI-Error")]:
        return True

    return False


def some_function(first, second="two", **kwargs):
    r"""Fetches and returns this thing

    :param first:
        The first parameter
    :type first: ``int``
    :param second:
        The second parameter
    :type second: ``str``
    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *extra* (``list``) --
          Extra stuff
        * *supplement* (``dict``) --
          Additional content

    """
