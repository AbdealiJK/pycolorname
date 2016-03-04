# -*- coding: utf-8 -*-


class ColorSystem(dict):
    """
    Provides an interface for a color system.
    """

    def load(self):
        """
        Try to load the data from a pre existing cache file if it exists.
        If the cache does not exist, auto fetch the data and save it in
        the cache for future use.
        """
        raise NotImplementedError

    def refresh(self):
        """
        Refreshes the cached data from the URL provided for this color system.
        """
        raise NotImplementedError

    def request(self, *args, **kwargs):
        """
        Request a specific URL. This function is to abstract out
        whether pywikibot is being used or not. Allowing the library to
        be independant of pywikibot if necessary.

        :param url: The url to get data from
        """
        raise NotImplementedError
