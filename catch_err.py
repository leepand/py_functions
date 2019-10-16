level = 0
def trace(f):
    def g(*args):
        global level

        # pretty print indicating the level
        prefix = "|  " * level + "|--"
        strargs = ", ".join(repr(a) for a in args)
        print("{} {}({})".format(prefix, f.__name__, strargs))

        # increment the level before calling the function
        # and decrement it after the call
        level += 1
        try:
            result = f(*args)
        except Exception as e:
            result = e
        level -= 1

        return result
    return g
from functools import wraps

def catch_algolink_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            #response = Response(mimetype='application/json')
            #response.set_data(e.serialize_as_json())
            #response.status_code = e.get_http_status_code()
            return e
    return wrapper
