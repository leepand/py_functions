import re

_XHTML_ESCAPE_RE = re.compile("[&<>\"']")
_XHTML_ESCAPE_DICT = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
}
unicode_type = str
_TO_UNICODE_TYPES = (unicode_type, type(None))

def to_unicode(value):  # noqa: F811
    """Converts a string argument to a unicode string.
    If the argument is already a unicode string or None, it is returned
    unchanged.  Otherwise it must be a byte string and is decoded as utf8.
    """
    if isinstance(value, _TO_UNICODE_TYPES):
        return value
    if not isinstance(value, bytes):
        raise TypeError("Expected bytes, unicode, or None; got %r" % type(value))
    return value.decode("utf-8")
to_basestring = to_unicode
def xhtml_escape(value):
    """Escapes a string so it is valid within HTML or XML.
    Escapes the characters ``<``, ``>``, ``"``, ``'``, and ``&``.
    When used in attribute values the escaped strings must be enclosed
    in quotes.
    .. versionchanged:: 3.2
       Added the single quote to the list of escaped characters.
    """
    return _XHTML_ESCAPE_RE.sub(
        lambda match: _XHTML_ESCAPE_DICT[match.group(0)], to_basestring(value)
    )
test='if(self.context["customer"] == "returning")'
print xhtml_escape(test)