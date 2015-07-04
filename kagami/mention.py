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
    return render_template('send.html', statuses=mention_list, page='1', npage='2', op='mention_page')


@app.route('/mention/<page>')
def mention_page(page: str):
    if not session.get('logged_in'):
        abort(401)
    auth = tweepy.OAuthHandler(app.config['CK'], app.config['CS'])
    auth.set_access_token(session.get('at'), session.get('as'))
    api = tweepy.API(auth)
    mention_list = api.mentions_timeline(page=page)
    return render_template('send.html', statuses=mention_list,
                           page=page, ppage=str(int(page)-1), npage=str(int(page)+1), op='mention_page')
