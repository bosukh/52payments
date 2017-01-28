import logging

from flask_login import login_user, current_user
from flask import redirect, url_for, flash
from bcrypt import bcrypt as bt

from . import login_manager
from . import WEB_CLIENT_ID
from .models import User
from .redirect_check import *

@login_manager.user_loader
def load_user(user_id):
    query = User.gql("WHERE user_id = '%s'"%str(user_id))
    return query.get()

def load_user_by_email(email):
    query = User.gql("WHERE email = '%s'"%str(email))
    return query.get()

def login_user_with_redirect(user, form, referrer):
    redirect_route = form.redirect()
    logging.debug(redirect_route)
    if redirect_route and user.is_authenticated():
        login_user(user)
        current_user = user
    else:
        return None, None
    if not check_referrer_origin(referrer) or check_referrer_auth_requirement(referrer, ['signup', 'signout', 'reset_password', 'forgot_password']):
        referrer = None;
    flash('Logged in successfully.')
    return user, referrer

def validate_user(form):
    error = None
    logging.debug(11111111111111111)
    if not form.data.get('email') or not form.data.get('password'):
        return None, 'You must enter both email and password'
    user = load_user(form.data['email'])
    if not user:
        return None, 'The given email is not registered'
    else:
        try:
            input_pw = bt.hashpw(form.data['password'], user.password)
            if input_pw == user.password:
                user.authenticated = True
            else:
                return None, 'The given password is not correct'
        except ValueError:
            return None, 'The given password is not correct'
    return user, error

def google_oauth(**kargs):
    #https://developers.google.com/identity/sign-in/web/backend-auth
    from oauth2client import client, crypt
    try:
        idinfo = client.verify_id_token(kargs['id_token'], WEB_CLIENT_ID)
        if idinfo['aud'] not in [WEB_CLIENT_ID]:
            raise crypt.AppIdentityError("Unrecognized client.")
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
    except crypt.AppIdentityError:
        return None, "Invalid Login Credentials"
    kargs['user_id'], kargs['email'] = idinfo['sub'], idinfo['email']
    kargs['first_name'], kargs['last_name'] = idinfo['given_name'], idinfo['family_name']
    user = load_user(kargs['user_id'])
    error = None
    if user and (kargs['request_type'].lower() != 'login'):
        error = 'Your email is already registered.'
    elif user and (kargs['request_type'].lower() == 'login'):
        user.authenticated = True
    elif not user and (kargs['request_type'].lower() != 'login'):
        user = User(user_id = kargs['user_id'],
                    email = idinfo['email'],
                    first_name = kargs['first_name'] or idinfo['given_name'],
                    last_name = kargs['last_name'] or idinfo['family_name'],
                    email_verified=True)
        user.put()
    else:
        error = 'Your email is not registered.'
    return user, error
