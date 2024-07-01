#!/usr/bin/env python3

import re
import unicodedata


def normalize_string(string: str, sep: str = " "):
    """
    Normalize a label by putting the label in lower case, then replace any accentuated char by is equivalent without
    any accent. All exotics chars will be replaced by the separator.
    :param string: The label to normalize.
    :param sep: The separator which will replace exotics chars. By default it will be an empty char.
    :return: The normalized string.
    """
    # put the string to lowercase
    str_lower = string.lower()
    # Normalize the label by replacing all accentuated chars by their equivalent
    str_normalized = unicodedata.normalize('NFKD', str_lower).encode('ASCII', 'ignore')
    str_slugified = str(str_normalized, 'utf-8')
    # Replace all specials chars by a space char
    str_slugified = re.sub(u"[\W|_]", " ", str_slugified)
    # Replace all double space by a single space
    str_slugified = re.sub("[ ]{2,}", " ", str_slugified)
    # Replace all space chars by the separator in parameter
    if sep != " ":
        str_slugified = str_slugified.replace(" ", sep)
    return str_slugified.strip(sep)