from . import login_manager
from .models import User
from . import WEB_CLIENT_ID
from flask_login import login_user
from flask import redirect, url_for
@login_manager.user_loader
def load_user(user_id):
    query = User.gql("WHERE user_id = '%s'"%user_id)
    return query.get()

def google_signup_auth(**kargs):
    #https://developers.google.com/identity/sign-in/web/backend-auth
    from oauth2client import client, crypt
    id_token=kargs['id_token']
    idinfo = client.verify_id_token(id_token, WEB_CLIENT_ID)
    try:
        if idinfo['aud'] not in [WEB_CLIENT_ID]:
            raise crypt.AppIdentityError("Unrecognized client.")
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")
    except crypt.AppIdentityError:
        return None, "Invalid Login Credentials"
    user_id = idinfo['sub']
    user = load_user(user_id)
    if user:
        error = 'Your email is already registered.'
    else:
        error = None
        user = User(user_id = user_id,
                    email = kargs['email'],
                    first_name = kargs['first_name'],
                    last_name = kargs['last_name'])
        user.put()
    return user, error
