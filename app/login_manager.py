import logging

from flask_login import login_user, current_user
from flask import redirect, url_for, flash
from bcrypt import bcrypt as bt
from oauth2client import client, crypt

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


class google_oauth:
    def __init__(self, id_token):
        #https://developers.google.com/identity/sign-in/web/backend-auth
        self.id_token = id_token
        self.idinfo = {}
        try:
            self.idinfo = client.verify_id_token(id_token, WEB_CLIENT_ID)
            if self.idinfo['aud'] not in [WEB_CLIENT_ID] or self.idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                self.idinfo = {}
        except crypt.AppIdentityError:
            pass
        self.user_id = self.idinfo.get('sub')
        self.user = load_user(self.user_id or '_')
        self.error = ''

    def login(self):
        if self.user:
            self.user.authenticated = True
            return self.user
        self.error = 'Your email is not registered.'
        return None

    def signup(self):
        if self.user:
            self.error = 'Your email is already registered.'
            return None
        else:
            user = User(user_id = self.idinfo['sub'],
                        email = self.idinfo['email'],
                        first_name = self.idinfo['given_name'],
                        last_name = self.idinfo['family_name'],
                        email_verified=True)
            user.put()
            return user
