# encoding: utf-8

"""
Provides Python 2/3 compatibility objects
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

import sys

NoneType = type(None)

def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass."""
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        slots = orig_vars.get('__slots__')
        if slots is not None:
            if isinstance(slots, str):
                slots = [slots]
            for slots_var in slots:
                orig_vars.pop(slots_var)
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper

# ===========================================================================
# Python 3 versions
# ===========================================================================

if sys.version_info >= (3, 0):

    from io import BytesIO

    def is_integer(obj):
        return isinstance(obj, int)

    def is_string(obj):
        """
        Return True if *obj* is a string, False otherwise.
        """
        return isinstance(obj, (str, bytes, bytearray))

    def to_unicode(text):
        """
        Return *text* as a unicode string.

        *text* can be a 7-bit ASCII string, a UTF-8 encoded 8-bit string, or
        unicode. String values are converted to unicode assuming UTF-8 encoding.
        Unicode values are returned unchanged.
        """
        # both str and unicode inherit from basestring
        if not is_string(text):
            tmpl = 'expected UTF-8 encoded string or unicode, got %s value %s'
            raise TypeError(tmpl % (type(text), text))
        # return unicode strings unchanged
        if isinstance(text, str):
            return text
        # otherwise assume UTF-8 encoding, which also works for ASCII
        return text.decode('utf-8')

# ===========================================================================
# Python 2 versions
# ===========================================================================

else:

    from StringIO import StringIO as BytesIO  # noqa

    def is_integer(obj):
        return isinstance(obj, (int, long))

    def is_string(obj):
        """
        Return True if *obj* is a string, False otherwise.
        """
        return isinstance(obj, basestring)

    def to_unicode(text):
        """
        Return *text* as a unicode string.

        *text* can be a 7-bit ASCII string, a UTF-8 encoded 8-bit string, or
        unicode. String values are converted to unicode assuming UTF-8 encoding.
        Unicode values are returned unchanged.
        """
        # both str and unicode inherit from basestring
        if not isinstance(text, basestring):
            tmpl = 'expected UTF-8 encoded string or unicode, got %s value %s'
            raise TypeError(tmpl % (type(text), text))
        # return unicode strings unchanged
        if isinstance(text, unicode):
            return text
        # otherwise assume UTF-8 encoding, which also works for ASCII
        return unicode(text, 'utf-8')
