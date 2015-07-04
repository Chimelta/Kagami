import ssl
from flask import Flask, session
from kagami.handler import reply_handle
from datetime import timedelta

DEBUG = True
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

import kagami.auth
import kagami.status
import kagami.mention
import kagami.user
