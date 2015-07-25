import ssl
from datetime import timedelta

from flask import Flask, session
import tweepy

DEBUG = True
SECRET_KEY = 'aewr232f3g3252423B&%#JHBRET(#TEsfawe24t23'
CK = 'yN3DUNVO0Me63IAQdhTfCA'
CS = 'c768oTKdzAjIYCmpSNIdZbGaG0t6rOhSFQP0S5uC79g'
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
import kagami.utils.nl2br
