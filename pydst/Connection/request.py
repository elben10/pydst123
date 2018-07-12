from requests import get
from types import MethodType
from requests.exceptions import HTTPError
from sys import version_info

if version_info[0] == 2:
    from urlparse import urljoin, urlparse, urlunparse
else:
    from urllib.parse import urljoin, urlparse, urlunparse


def dst_request(path, params=None):
    """ """
    parsed = urlparse('http://api.statbank.dk/v1/')
    url = urlunparse([parsed.scheme, parsed.hostname,
                      urljoin(parsed.path, path),
                      parsed.params, parsed.query,
                      parsed.fragment])
    return get2(url, params)


def get2(url, params=None, **kwargs):
    """ """
    r = get(url, params, **kwargs)
    r.raise_for_status_2 = MethodType(raise_for_status, r)
    return r


def raise_for_status(self):
    """Raises stored :class:`HTTPError`, if one occurred."""

    http_error_msg = ''
    if isinstance(self.reason, bytes):
        # We attempt to decode utf-8 first because some servers
        # choose to localize their reason strings. If the string
        # isn't utf-8, we fall back to iso-8859-1 for all other
        # encodings. (See PR #3538)
        try:
            reason = self.reason.decode('utf-8')
        except UnicodeDecodeError:
            reason = self.reason.decode('iso-8859-1')
    else:
        reason = self.reason

    if 400 <= self.status_code < 500:
        http_error_msg = u'%s Client Error: %s for url: %s' \
                         % (self.status_code, reason, self.url)

    elif 500 <= self.status_code < 600:
        http_error_msg = u'%s Server Error: %s for url: %s' \
                         % (self.status_code, reason, self.url)

    if isinstance(self.json(), dict) and 'errorTypeCode' in self.json().keys():
            http_error_msg += u'\nError message from Statistics Denmark:' \
                          u'\n\t> %s' % self.json().get('message')

    if http_error_msg:
        raise HTTPError(http_error_msg, response=self)
