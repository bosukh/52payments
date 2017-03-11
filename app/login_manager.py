import logging

from flask_login import login_user, current_user
from flask import redirect, url_for, flash, session
from bcrypt import bcrypt as bt
from oauth2client import client, crypt
from functools import wraps

from . import login_manager
from . import WEB_CLIENT_ID
from .models.User import UserModel
from .redirect_check import *

def redirect_loggedin_user(redirect_path):
    '''
    Decorator function to redirect logged in user to another page.
    Current usage: When user is logged in, "login" and "signup" pages --> "my_account"
    '''
    def handler_decorator(handler):
        @wraps(handler)
        def decorated_function(*args, **kwargs):
            if session.get('user_id'):
                return redirect(url_for(redirect_path))
            return handler(*args, **kwargs)
        return decorated_function
    return handler_decorator

@login_manager.user_loader
def load_user(user_id):
    query = UserModel.gql("WHERE user_id = '%s'"%str(user_id))
    return query.get()

def load_user_by_email(email):
    query = UserModel.gql("WHERE email = '%s'"%str(email))
    return query.get()

def login_user_with_redirect(user, form = None, redirect_path = None):
    if form:
        redirect_path = form.redirect()
    if redirect_path and user.is_authenticated():
        login_user(user)
        #current_user = user
    else:
        return None, None
    if not check_referrer_origin(redirect_path) or check_referrer_auth_requirement(redirect_path, ['signup', 'logout', 'reset-password', 'forgot-password']):
        redirect_path = None;
    flash('Logged in successfully.')
    return user, redirect_path

class NormalAuth:
    def __init__(self, form):
        '''
        Login or signup user given the form.
        The form is either LoginForm or SignUpForm.
        The form field validation is done before calling this method.
        '''
        self.data = form.data
        self.user = load_user(self.data.get('email', '_'))
        self.error = ''
        try:
            self.redirect = form.redirect()
        except AttributeError:
            self.redirect = url_for('index')

    def login(self):
        if not self.user:
            self.error =  'The given email is not registered'
        else:
            try:
                input_pw = bt.hashpw(self.data.get('password', '_'), self.user.password)
                if input_pw == self.user.password:
                    self.user.authenticated = True
                    self.user, self.redirect = login_user_with_redirect(self.user, redirect_path = self.redirect)
                    return self.user
            except Exception as e:
                logging.debug(e)
            self.error =  'The given password is not correct'
        return None

    def signup(self):
        if self.user:
            self.error = 'Your email is already registered.'
        else:
            self.data.pop('password_2', None)
            self.data['user_id'] = self.data.get('email')
            try:
                orig_password = self.data.get('password', '')
                self.data['password'] = bt.hashpw(orig_password, bt.gensalt())
                self.user = UserModel(**self.data)
                self.user.put()
                self.data['password'] = orig_password
                return self.login()
            except Exception as e:
                logging.debug(e)
            self.error = 'The given information is invalid'

class GoogleOauth:
    def __init__(self, id_token):
        '''
        https://developers.google.com/identity/sign-in/web/backend-auth
        Google Oauth login. Given the id_token, retrieve user information from google.
        Use the retrieved info to login or signup user.
        '''
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
        self.redirect = session.get('initial_referrer') or url_for('index')

    def login(self):
        if self.user:
            self.user.authenticated = True
            self.user, self.redirect =  login_user_with_redirect(self.user, redirect_path = self.redirect)
            return self.user
        self.error = 'Your email is not registered.'
        return None

    def signup(self):
        if self.user:
            self.error = 'Your email is already registered.'
            return None
        else:
            self.user = UserModel(user_id = self.idinfo['sub'],
                        email = self.idinfo['email'],
                        first_name = self.idinfo['given_name'],
                        last_name = self.idinfo['family_name'],
                        email_verified=True)
            self.user.put()
            return self.login()
