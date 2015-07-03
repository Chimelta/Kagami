from flask import Flask, request, session, redirect, url_for, \
    abort, render_template
from Pyitap import TwProxyGetAuth
import tweepy
from reply_handler import reply_handle
import ssl

DEBUG = False
SECRET_KEY = 'aewrg32524234t*#B&%#JHBRET(#TE'
CK = '3nVuSoBZnx6U4vzUxf5w'
CS = 'Bcs59EFbbsdF6Sl9Ng71smgStWEGwXXKSjYvPVt7qys'
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('kagami.crt', 'kagami.key')

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def show():
    if session.get('logged_in'):
        auth = tweepy.OAuthHandler(app.config['CK'], app.config['CS'])
        auth.set_access_token(session.get('at'), session.get('as'))
        api = tweepy.API(auth)
        status = api.home_timeline()
        return render_template('send.html', statuses=status)
    return render_template('send.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        try:
            access_token, access_secret = TwProxyGetAuth.init_oauth(request.form['username'],
                                                                    request.form['password'],
                                                                    app.config['CK'], app.config['CS'])
        except:
            return render_template('login.html')
        session['logged_in'] = True
        session['at'] = access_token
        session['as'] = access_secret
        return redirect(url_for('show'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


@app.route('/update', methods=['POST'])
def update():
    if not session.get('logged_in'):
        abort(401)
    auth = tweepy.OAuthHandler(app.config['CK'], app.config['CS'])
    auth.set_access_token(session.get('at'), session.get('as'))
    api = tweepy.API(auth)
    api.update_status(status=request.form['text'])
    return redirect(url_for('show'))

@app.route('/reply/<status_id>', methods=['GET', 'POST'])
def reply(status_id: str):
    if not session.get('logged_in'):
        abort(401)
    auth = tweepy.OAuthHandler(app.config['CK'], app.config['CS'])
    auth.set_access_token(session.get('at'), session.get('as'))
    api = tweepy.API(auth)
    if request.method == 'POST':
        api.update_status(status=request.form['text'],
                          in_reply_to_status_id=status_id)
        return redirect(url_for('show'))
    status = api.get_status(status_id)
    me = api.me()
    return render_template('reply.html', status=status, head=reply_handle(status.text,
                                                                          me.screen_name, status.user.screen_name))

if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context=context)
