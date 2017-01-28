from config import ALLOWED_ORIGINS, LOGIN_REQUIRED_LIST

def check_referrer_auth_requirement(referrer, avoid_list=[]):
    referrer = str(referrer)
    if not avoid_list:
        avoid_list = LOGIN_REQUIRED_LIST
    for route in avoid_list:
        if referrer.lower().find(route.lower()) > -1:
            return True
    return False

def check_referrer_origin(referrer):
    referrer = str(referrer)
    for url in ALLOWED_ORIGINS:
        if referrer[:len(url)] == url:
            return True
    return False
