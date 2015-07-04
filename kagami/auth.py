from kagami import app
from Pyitap import TwProxyGetAuth
from flask import render_template, url_for, session, redirect, request
import tweepy


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
        auth = tweepy.OAuthHandler(app.config['CK'], app.config['CS'])
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth)
        session['me'] = api.me().screen_name
        return redirect(url_for('show'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))
