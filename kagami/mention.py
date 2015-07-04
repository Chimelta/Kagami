from kagami import app
from flask import session, render_template, abort
import tweepy


@app.route('/mention')
def mention():
    if not session.get('logged_in'):
        abort(401)
    auth = tweepy.OAuthHandler(app.config['CK'], app.config['CS'])
    auth.set_access_token(session.get('at'), session.get('as'))
    api = tweepy.API(auth)
    mention_list = api.mentions_timeline()
    return render_template('send.html', statuses=mention_list)
