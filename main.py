#!venv/bin/python
from flask import Flask, request, session, redirect, url_for, \
    abort, render_template, flash
from Pyitap import TwProxyGetAuth
import tweepy

DEBUG = True
SECRET_KEY = 'aewrg32524234t*#B&%#JHBRET(#TE'
CK = '3nVuSoBZnx6U4vzUxf5w'
CS = 'Bcs59EFbbsdF6Sl9Ng71smgStWEGwXXKSjYvPVt7qys'

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def show():
    return render_template('send.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        session['logged_in'] = True
        try:
            access_token, access_secret = TwProxyGetAuth.init_oauth(request.form['username'],
                                                                    request.form['password'],
                                                                    app.config['CK'], app.config['CS'])
        except:
            return render_template('login.html')
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


if __name__ == '__main__':
    app.run(host='0.0.0.0')