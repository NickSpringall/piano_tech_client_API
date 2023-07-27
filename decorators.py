import functools
from flask_jwt_extended import get_jwt_identity

def check_if_technician(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user = get_jwt_identity()
        if 'technician' in user:
            return (fn(*args, **kwargs))
        else:
            return {"error": "unauthorised user"}, 403
    return wrapper


def check_if_technician_or_logged_in_client(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        user = get_jwt_identity()
        idd = kwargs['id']
        
        if 'technician' in user:
            return (fn(*args, **kwargs))
        elif user == ('client' + str(kwargs['id'])):
            return (fn(*args, **kwargs))
        else:
            return {"error": "unauthorised user"}, 403
    return wrapper