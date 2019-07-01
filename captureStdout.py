import sys
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
class CaptureStdout:
    """
    Captures everything `func` prints to stdout and returns it instead.
        >>> def idiot():
        ...     print("foo")
        >>> capturestdout(idiot)()
        'foo\\n'
    **WARNING:** Not threadsafe!
    """
    def __init__(self, func):
        self.func = func
    def __call__(self, *args, **keywords):
        out = StringIO()
        oldstdout = sys.stdout
        sys.stdout = out
        try:
            self.func(*args, **keywords)
        finally:
            sys.stdout = oldstdout
        return out.getvalue()

capturestdout = CaptureStdout
def idiot():
    print("foo")
    print 'azdsd'
    print 'sdsdssss'
capturestdout(idiot)()
