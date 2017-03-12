import logging
from config import ALLOWED_ORIGINS, LOGIN_REQUIRED_LIST
from urlparse import urlparse, urljoin
from flask import request, session

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

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def get_redirect_target():
    logging.debug(request.referrer)
    logging.debug(session.get('initial_referrer'))
    for target in request.args.get('next'), session.get('initial_referrer'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target
