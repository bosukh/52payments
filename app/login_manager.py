from . import login_manager
from .models import User
from . import WEB_CLIENT_ID
from flask_login import login_user
from flask import redirect, url_for

@login_manager.user_loader
def load_user(user_id):
    query = User.gql("WHERE user_id = '%s'"%user_id)
    return query.get()

def load_user_by_email(email):
    query = User.gql("WHERE email = '%s'"%email)
    return query.get()

def google_oauth(**kargs):
    #https://developers.google.com/identity/sign-in/web/backend-auth
    from oauth2client import client, crypt
    idinfo = client.verify_id_token(kargs['id_token'], WEB_CLIENT_ID)
    try:
        if idinfo['aud'] not in [WEB_CLIENT_ID]:
            raise crypt.AppIdentityError("Unrecognized client.")
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
    except crypt.AppIdentityError:
        return None, "Invalid Login Credentials"
    kargs['user_id'] = idinfo['sub']
    user = load_user_by_email(kargs['email'])
    error = None
    if user and (kargs['request_type'].lower() != 'login'):
        error = 'Your email is already registered.'
    elif user and (kargs['request_type'].lower() == 'login'):
        user.authenticated = True
    elif not user and (kargs['request_type'].lower() != 'login'):
        user = User(user_id = kargs['user_id'],
                    email = idinfo['email'],
                    first_name = kargs['first_name'] or idinfo['given_name'],
                    last_name = kargs['last_name'] or idinfo['family_name'])
        user.put()
        error = 'Successfully registered. Please login.'
    else:
        print kargs['user_id'], kargs['last_name'], kargs['first_name']
        error = 'Your email is not registered.'
    return user, error
