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
