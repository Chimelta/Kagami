from kagami import app
from flask import session, render_template, abort, redirect, url_for
import tweepy
from flask import request

@app.route('/user/<username>')
def user(username: str):
    if not session.get('logged_in'):
        abort(401)
    auth = tweepy.OAuthHandler(app.config['CK'], app.config['CS'])
    auth.set_access_token(session.get('at'), session.get('as'))
    api = tweepy.API(auth)
    page = '1'
    if request.args.get('page', ''):
        page = request.args.get('page', '')
    status_list = api.user_timeline(username, page=int(page))
    return render_template('user.html', head='@'+username+' ', statuses=status_list, me=session.get('me'),
                           page=page, npage=int(page)+1, ppage=int(page)-1, username=username)


@app.route('/me')
def me():
    if not session.get('logged_in'):
        abort(401)
    auth = tweepy.OAuthHandler(app.config['CK'], app.config['CS'])
    auth.set_access_token(session.get('at'), session.get('as'))
    api = tweepy.API(auth)
    username = api.me().screen_name
    return redirect(url_for('user', username=username))
