"""
A really simplistic FLASK_OAUTHLIB client.

As the documentation states, you shouldn't use FLASK_OAUTHLIB.
It doesn't list the risks though. FLASK_OAUTH LIB suffers from 
less than stellar logging and it stores things in the session.
The session in flask is cookie based, so without a plugin to move
that serverside, you should not do this.

This client has been tested against both FLASK_OAUTHLIB and AUTHLIB
providers.

This uses the authorization_code workflow designed for traditional
web app usage. This is not for SPA web apps, unless you plan to keep
all the backend centralized under your applications APIs. For SPA
you should look into using the implicit flow.

FLASK_OAUTHLIB provider setup:
- Create a client_id/secret. 
- _redirect_uris should contain space delimited URLs that are valid
  for redirection. For this example just use https://localhost:5000/authorized
- For _default_scopes setup space delimited scopes. 
  This example needs at lease "email roles" in the scope field.

AUTHLIB provider setup:
- Create client_id/client_secret
- Token_endpoint_auth_method = client_secret_post
- Grant_type = authorization_code
- Response_type = code
- scopes "email roles" space delimited
- Redirect_URI 'https://localhost:5000/authorized' these are new line delimited.

"""

import os
from dotenv import load_dotenv

from flask import Flask, session, abort, request, url_for
from flask_oauthlib.client import OAuth, OAuthException

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'DUMMY') 
app.config['SESSION_COOKIE_SECURE'] = False

# Setup Oauth Client
oauth = OAuth()
remote = oauth.remote_app(
    'SampleProv',
    consumer_key=os.environ.get('OAUTH_KEY', 'DUMMY') ,
    consumer_secret=os.environ.get('OAUTH_SECRET', 'NOTASECRET'),
    request_token_params={'scope': 'email roles'},
    base_url=os.environ.get('OAUTH_HOST', 'http://127.0.0.1:5001') + '/api/',
    request_token_url=None,
    # access_token_method='POST',
    access_token_url=os.environ.get('OAUTH_HOST', 'http://127.0.0.1:5001') + '/oauth/token',
    authorize_url=os.environ.get('OAUTH_HOST', 'http://127.0.0.1:5001') + '/oauth/authorize'
)

oauth.init_app(app)


@app.route('/')
def hello_world():
    """
    The main page which triggers the authorization flow.
    """
    return remote.authorize(
        callback=url_for('authorized', _external=True)
    )

@remote.tokengetter
def get_oauth_token():
    """
    Used by OAUTH Client to know where to fetch the remote app.
    The FLASK_OAUTHLIB client stores this in the session which defaults to cookies.
    They recommend not using this library anymore because of this and other reasons.
    
    Moving the session storage to be server side with a FLASK plugin
    is a better solution until you can convert to AUTHLIB.

    """
    return session.get('remote_oauth')

@app.route('/authorized')
def authorized():
    """
    Endpoint is redirected to on successful Oauth.
    Store the access token indicating successful login to the entire application.
    Serve the index page on successful login.
    """
    remote = oauth.remote_apps['SampleProv']
    try:
        resp = remote.authorized_response()
        app.logger.info(resp)

        if resp is None or resp.get('access_token') is None:
            return 'Access denied: reason=%s error=%s resp=%s' % (
                request.args['error'],
                request.args['error_description'],
                resp
            )
    except OAuthException:
        # If you get here, don't expect the error message to be helpful
        # Both AUTHLIB and FLASK_OAUTHCLIENT have less than stellar 
        # debug logs and error messages.
        app.logger.info('401')
        abort(401)

    # Store the access token in the session.
    # This is bad because FLASK defaults to storing this in cookies.
    # If you do plan to try this, at least move the session storage
    # in flask to be serverside with a plugin.
    # I plan to provide a simple AuthLib example in the future.
    session['remote_oauth'] = (resp['access_token'], '')

    # Now that we have the token, try making a call to the Oauth provider API.
    resp = remote.get('me')

    if resp.status >= 200 and resp.status <= 299:
        return resp.data

    return resp
