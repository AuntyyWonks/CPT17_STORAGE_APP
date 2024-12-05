from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Use a secure random key in production
oauth = OAuth(app)

oauth.register(
    name='oidc',
    # authority=  url for cognito
    # client_id= clientID,
    # client_secret='client_secret'
    # server_metadata_url='cognito openid-configuration',
    client_kwargs={'scope': 'openid email phone'}  # Include 'openid' for standard OIDC scopes
)

@app.route('/')
def index():
    user = session.get('user')
    if user:
        return f'Hello, {user["email"]}. <a href="/logout">Logout</a>'
    else:
        return 'Welcome! Please <a href="/login">Login</a>.'

@app.route('/login')
def login():
    # Redirect to Cognito's login page
    redirect_uri = url_for('authorize', _external=True)
    return oauth.oidc.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    # Retrieve the access token from Cognito
    token = oauth.oidc.authorize_access_token()
    user = oauth.oidc.parse_id_token(token)  # Parse the ID token to get user info
    session['user'] = user  # Store user info in session
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # Remove user info from the session and redirect to home page
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
