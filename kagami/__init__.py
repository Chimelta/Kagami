import ssl
from flask import Flask, session
from datetime import timedelta
import tweepy

DEBUG = False
SECRET_KEY = 'aewrg32524234t*#B&%#JHBRET(#TE'
CK = '3nVuSoBZnx6U4vzUxf5w'
CS = 'Bcs59EFbbsdF6Sl9Ng71smgStWEGwXXKSjYvPVt7qys'
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('kagami.crt', 'kagami.key')

app = Flask(__name__)
app.config.from_object(__name__)


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=31)


def get_api(consumer_key: str, consumer_secret: str, access_token: str, access_secret: str):
    tw_auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    tw_auth.set_access_token(access_token, access_secret)
    return tweepy.API(tw_auth)


import kagami.auth
import kagami.status
import kagami.mention
import kagami.user
