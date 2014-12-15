import time as Time
import sys


class UnicodeMixin(object):

    """Mixin class to handle defining the proper __str__/__unicode__
    methods in Python 2 or 3."""

    if sys.version_info[0] >= 3:  # Python 3
        def __str__(self):
            return self.__unicode__()
    else:  # Python 2
        def __str__(self):
            return self.__unicode__().encode('utf8')


class PropertyUnavailable(AttributeError):
    pass


def build_url(key, lat, lng, datetime=None, options=None):

    if datetime is None:
        url = "https://api.forecast.io/forecast/{0}/{1},{2}".format(
            key, lat, lng
        )
    else:
        url = "https://api.forecast.io/forecast/{0}/{1},{2},{3}".format(
            key, lat, lng, datetime
        )

    # Generate Query String
    if options:
        querystring = '&'.join(
            [dictKey+'='+options[dictKey] for dictKey in options]
        )
        url += '?'+querystring

    return url
