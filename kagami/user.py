from kagami import app
from flask import session, render_template, abort, redirect, request, url_for
import tweepy


@app.route('/user/<username>')
def user(username: str):
    if not session.get('logged_in'):
        abort(401)
    auth = tweepy.OAuthHandler(app.config['CK'], app.config['CS'])
    auth.set_access_token(session.get('at'), session.get('as'))
    api = tweepy.API(auth)
    status_list = api.user_timeline(username)
    return render_template('send.html', head='@'+username+' ', statuses=status_list, me=session.get('me'))


@app.route('/me')
def me():
    if not session.get('logged_in'):
        abort(401)
    auth = tweepy.OAuthHandler(app.config['CK'], app.config['CS'])
    auth.set_access_token(session.get('at'), session.get('as'))
    api = tweepy.API(auth)
    username = api.me().screen_name
    return redirect(url_for('user', username=username))
