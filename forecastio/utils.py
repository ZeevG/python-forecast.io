import sys
try:
    from urllib import urlencode  # python 2
except:
    from urllib.parse import urlencode  # python 3


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


def build_url(key, lat, lng, time=None, url_params=None):

    url = "https://api.darksky.net/forecast/{key}/{lat},{lng}"
    if time is not None:
        url += ",{time}"
        time = time.replace(microsecond=0).isoformat()  # API returns 400 if we include microseconds

    # Generate Query String
    if url_params:
        url += "?{params}"

    return url.format(key=key, lat=lat, lng=lng, time=time, params=urlencode(url_params))
